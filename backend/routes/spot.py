from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from exstensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.spot import Spot
from models.user import UserProfile
from models.rating import Rating
from schemas.spot_schema import spot_schema
from util.outlier_coords import average_location_batch
from util.storage import generate_presigned_url
from util.celery_task import process_photos_with_metadata
from marshmallow import ValidationError
from celery.result import AsyncResult, GroupResult
from celery import chord,group
from exstensions import celery
from sqlalchemy.orm import joinedload, load_only
from sqlalchemy import case

spot_bp = Blueprint('spot', __name__, url_prefix='/spot')

@spot_bp.route('/task/progress', methods=['POST'])
@jwt_required()
def spot_task_progress():
    data = request.get_json()
    task_id = data.get('task_id')

    if(task_id):
        task = AsyncResult(task_id)
        return jsonify({'state': task.state,
                        'progress': task.info.get('progress', 0)}), 200
    
    
@spot_bp.route('/status/<group_id>', methods=['GET'])
@jwt_required()
def get_batch_progress(group_id):
    group_result = GroupResult.restore(group_id, app=celery)

    if not group_result:
        return jsonify({'state': 'UNKNOWN', 'progress': 0}), 200

    if group_result.ready():
        if group_result.successful():
            return jsonify({'state': 'SUCCESS', 'progress': 100}), 200
        else:
            try:
                group_result.join()
            except Exception as e:
                return jsonify({'state': 'FAILURE', 'error': str(e)}), 200
            return jsonify({'state': 'FAILURE'}), 200

    total_tasks = len(group_result.children) if group_result.children else 0
    cumulative_progress = 0
    completed_count = 0

    if total_tasks > 0:
        for task in group_result.children:
            if task.ready():
                cumulative_progress += 100
                completed_count += 1
            elif task.state == 'PROCESSING':
                info = task.info
                if isinstance(info, dict):
                    cumulative_progress += info.get('progress', 0)
            else:
                pass
        
        progress = int(cumulative_progress / total_tasks)
    else:
        progress = 0

    return jsonify({
        'state': 'PROCESSING',
        'progress': progress,
        'completed': completed_count,
        'total': total_tasks
    }), 200

@spot_bp.route('/presigned-url', methods=['POST'])
@jwt_required()
def get_presigned_url_spot():
    current_user = get_jwt_identity()
    data = request.get_json()
    presigned_urls = []

    try:
        for metadata in data:
            filename = metadata.get('fileName')
            filetype = metadata.get('fileType')
            if(filename):
                presigned_urls.append(generate_presigned_url(filename=filename, filetype=filetype, user_id=current_user, folder='quarantine_spot', expires_in=600))
        return jsonify({'message': presigned_urls}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@spot_bp.route('/create', methods = ['POST'])
@jwt_required()
def create_spot():
    current_user = get_jwt_identity()

    try:
        data = request.get_json()
        keys = data.get('keys')

        if(not keys or len(keys) == 0):
            return jsonify({'error':'No photos provided'}), 400

        data.pop('keys')

        try:
            spot_schema.load(
                data=data,
                partial=True
            )
        except ValidationError as e:
            return jsonify({'error': e.messages}), 400

        spot = Spot(
            user_profile_id = current_user,
            name=data.get('name'),
            description=data.get('description'),
            accessibility=data.get('accessibility'),
            hashtags=data.get('hashtags')
        )

        db.session.add(spot)
        db.session.commit()
    
        if(keys):
            photo_tasks = [
                process_photos_with_metadata.s(
                    key=key, post_type_id=spot.id, user_id=current_user, upload_s3_foldername=f'spot/spot_{spot.id}',post_type='spot', order=order
                    ) for order, key in enumerate(keys, start=1)
            ]

            job_group = group(photo_tasks)
            callback_task = average_location_batch.s(post_type_id=spot.id, post_type='spot')

            task = chord(job_group)(callback_task)
            group_res = task.parent
            group_res.save()
        
        return jsonify({'message': 'Your spot is being created',
                        'name': data.get('name'),
                        'post_type': 'spot',
                        'task_id': group_res.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500



@spot_bp.route('/me', methods=['GET'])
@jwt_required()
def get_user_spots():
    current_user = get_jwt_identity()

    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=12, type=int)

        username = UserProfile.query.with_entities(UserProfile.username).filter_by(id=current_user).first()

        spots = db.session.query(Spot, Rating).outerjoin(
            Rating, 
            (Rating.user_profile_id==current_user) & (Rating.spot_id==Spot.id)
        ).filter(
            Spot.user_profile_id==current_user
        ).options(
            joinedload(Spot.spot_media)
        ).order_by(Spot.date_posted.desc())

        paginated_spots = spots.paginate(
            page=page,
            per_page=per_page
        )

        results =[]

        for spot, rating in paginated_spots.items:
            spot_data = spot_schema.dump(spot)

            spot_data['rating_choice'] = rating.rating_choice if rating else None
            spot_data['username'] = username[0]
            

            results.append(spot_data)


        return jsonify({
            'spots': results,
            'total': paginated_spots.total,
            'total_pages': paginated_spots.pages,
            'current_page': paginated_spots.page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# TODO: add check for if a user made a visit at a spot
@spot_bp.route('/rate/<spot_id>', methods=['POST', 'DELETE'])
@jwt_required()
def rate_spot(spot_id):
    current_user = get_jwt_identity()
  
    is_rated = Rating.query.filter_by(spot_id=spot_id, user_profile_id=current_user).first()

    if request.method == 'POST':
        data = request.get_json()
        rate = data.get('rating_choice')

        if not rate or not isinstance(rate, int) or not (1 <= rate <= 5) :
            return jsonify({'error': 'Invalid rating (1-5 required)'}), 400

        if is_rated and is_rated.rating_choice == rate:
            return jsonify({'message': 'Rating unchanged'}), 200
        
        try: 

            if is_rated:
                Spot.query.filter_by(id=spot_id).update({
                    'average_rating': case(
                        (Spot.total_num_of_ratings == 0, rate),
                    else_=(((Spot.average_rating * Spot.total_num_of_ratings) - is_rated.rating_choice) + rate) / (Spot.total_num_of_ratings)
                    )
                })
                is_rated.rating_choice = rate
                is_rated.created_at = datetime.now(timezone.utc)
            
            else:
                rating = Rating(
                    user_profile_id=current_user,
                    spot_id=spot_id,
                    rating_choice=rate,
                    created_at=datetime.now(timezone.utc)
                )

                Spot.query.filter_by(id=spot_id).update({
                    'total_num_of_ratings': Spot.total_num_of_ratings + 1,
                    'average_rating': case(
                        (Spot.total_num_of_ratings == 0, rate),
                    else_=((Spot.average_rating * Spot.total_num_of_ratings) + rate) / (Spot.total_num_of_ratings + 1)
                    )
                })

                db.session.add(rating)
            db.session.commit()

            updated_spot = Spot.query.with_entities(Spot.average_rating, Spot.total_num_of_ratings).filter_by(id=spot_id).first()
            return jsonify({'message': 'Rating added/updated successfully',
                            'rating': rate,
                            'new_average': updated_spot[0],
                            'new_total_ratings': updated_spot[1]}), 201
        except Exception:
            return jsonify({'error': 'This spot is already rated'}), 500

    elif request.method == 'DELETE':
        try:
            if is_rated:
                Spot.query.filter_by(id=spot_id).update({
                    'total_num_of_ratings': Spot.total_num_of_ratings - 1,
                    'average_rating': case(
                        (Spot.total_num_of_ratings <= 1, 0),
                    else_=(
                        ((Spot.average_rating * Spot.total_num_of_ratings) - is_rated.rating_choice) / (Spot.total_num_of_ratings - 1)
                    )
                    )
                })
                db.session.delete(is_rated)
                db.session.commit()

                updated_spot = Spot.query.with_entities(Spot.average_rating, Spot.total_num_of_ratings).filter_by(id=spot_id).first()
                return jsonify({'message': 'Rating removed successfully',
                                'new_average': updated_spot[0],
                                'new_total_ratings': updated_spot[1]}), 200
            else:
                return jsonify({'message': 'No rating to remove'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500