import os
from datetime import datetime, timezone

from celery import chord, group
from celery.result import AsyncResult, GroupResult
from app.extensions  import celery, db
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from marshmallow import ValidationError
from models import CollectionItem, Rating, Spot, UserProfile, Visit
from schemas.spot_schema import spot_schema
from sqlalchemy import Numeric, case, cast, func
from sqlalchemy.orm import joinedload
from utils import (
    average_location_batch,
    generate_presigned_url,
    process_photos_with_metadata,
)

spot_bp = Blueprint('spot', __name__, url_prefix='/spot')

def generate_task_token(user_id: str, task_id: str, group_id:str):
    token = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))

    return token.dumps({
        'user_id': user_id,
        'task_id': task_id,
        'group_id': group_id
    })

@spot_bp.route('/task/progress', methods=['POST'])
@jwt_required()
def spot_task_progress():
    data = request.get_json()
    task_id = data.get('task_id')

    if(task_id):
        task = AsyncResult(task_id)
        return jsonify({'state': task.state,
                        'progress': task.info.get('progress', 0)}), 200
    
    
@spot_bp.route('/status/<task_token>', methods=['GET'])
@jwt_required()
def get_batch_progress(task_token):
    if not task_token:
        return ({'error': 'invalid'}), 400

    current_user = get_jwt_identity()
    
    serializer = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))

    try:
        data = serializer.loads(task_token, max_age=3600)
    except SignatureExpired:
        return jsonify({'error': 'Token expired'}), 401
    except BadSignature:
        return jsonify({'error': 'Invalid Token'}), 401

    if not data or data.get('user_id') != current_user:
        return jsonify({'error': 'Access denied'}), 403

    chord_id = data.get('task_id') 
    group_id = data.get('group_id')

    chord_result = AsyncResult(chord_id, app=celery)
    if not chord_result:
        return jsonify({'state': 'PENDING', 'progress': 0}), 200
    
    if chord_result.ready():
        if chord_result.successful():
            return jsonify({'state': 'SUCCESS', 'progress': 100}), 200
        else:
            return jsonify({'state': 'FAILURE', 'error': str(chord_result.result)}), 200
        
    group_result = GroupResult.restore(group_id)

    if not group_result:
        return jsonify({'state': 'PENDING', 'progress': 0}), 200
    
    results = group_result.results
    total_tasks = len(results)
    cumulative_progress = 0
    completed_count = 0

    for task in results:
        if task.ready():
            if task.successful():
                cumulative_progress += 100
                completed_count += 1
            else:
                cumulative_progress += 0 
        else:
            if task.state == 'PROCESSING':
                info = task.info
                if isinstance(info, dict):
                    cumulative_progress += info.get('progress', 0)
            elif task.state == 'SUCCESS':
                cumulative_progress += 100
                completed_count += 1

    progress = int(cumulative_progress / total_tasks) if total_tasks > 0 else 0

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
            user_id = current_user,
            name=data.get('name'),
            description=data.get('description'),
            accessibility=data.get('accessibility'),
            hashtags=data.get('hashtags')
        )

        db.session.add(spot)
        db.session.commit()

        type = 'spot'
    
        if(keys):
            photo_tasks = [
                process_photos_with_metadata.s(
                    key=key, post_type_id=spot.id, user_id=current_user, upload_s3_foldername=f'{type}/{type}_{spot.id}',post_type=type, order=order
                    ) for order, key in enumerate(keys, start=1)
            ]

            job_group = group(photo_tasks)
            callback_task = average_location_batch.s(post_type_id=spot.id, post_type=type)

            #TODO: add task ids to model for persistence
            task = chord(job_group)(callback_task)
            group_res = task.parent.save()
            
            token = generate_task_token(current_user, task.id, group_res.id)
        
        return jsonify({'message': 'Your spot is being created',
                        'name': data.get('name'),
                        'post_type': 'spot',
                        'task_token': token}), 201
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

        username_and_collections = UserProfile.query.options(
            joinedload(UserProfile.collection)
        ).get(current_user)

        is_saved = db.session.query(CollectionItem).filter(
            CollectionItem.spot_id == Spot.id,
            CollectionItem.saved_by == current_user
        ).exists()

        has_visited = db.session.query(Visit).filter(
            Visit.spot_id == Spot.id,
            Visit.user_id == current_user
        ).exists()

        spots = db.session.query(
            Spot, Rating, is_saved.label('is_saved'), has_visited.label('has_visited')
        ).outerjoin(
            Rating, 
            (Rating.user_id==current_user) & (Rating.spot_id==Spot.id)
        ).filter(
            Spot.user_id==current_user,
            Spot.status == 'success'
        ).options(
            joinedload(Spot.media)
        ).order_by(Spot.date_posted.desc())

        paginated_spots = spots.paginate(
            page=page,
            per_page=per_page
        )

        results =[]

        if username_and_collections.collection:
            collections = [{'id': c.id, 'name': c.name, 'is_default': c.is_default} for c in username_and_collections.collection]

        for spot, rating, is_saved, has_visited in paginated_spots.items:
            spot_data = spot_schema.dump(spot)

            spot_data['rating_choice'] = rating.rating_choice if rating else None
            spot_data['username'] = username_and_collections.username
            spot_data['is_saved'] = is_saved
            spot_data['has_visited'] = has_visited

            results.append(spot_data)


        return jsonify({
            'spots': results,
            'collections': collections,
            'total': paginated_spots.total,
            'total_pages': paginated_spots.pages,
            'current_page': paginated_spots.page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# TODO: add check for if a user made a visit at a spot. updated queires to return new values when query finishes
@spot_bp.route('/rate/<spot_id>', methods=['POST', 'DELETE'])
@jwt_required()
def rate_spot(spot_id):
    current_user = get_jwt_identity()

    if not spot_id:
        return jsonify({'error': 'Invalid data'}), 400
    
    is_rated = db.session.query(Rating).filter(Rating.spot_id == spot_id, Rating.user_id == current_user).first()

    if request.method == 'POST':
        data = request.get_json()
        rate = data.get('rating_choice')

        if not rate or not isinstance(rate, int) or not (1 <= rate <= 5):
            return jsonify({'error': 'Invalid rating (1-5 required)'}), 400

        if is_rated and is_rated.rating_choice == rate:
            return jsonify({'message': 'Rating unchanged'}), 200
        
        try: 

            if is_rated:
                Spot.query.filter_by(id=spot_id).update({
                    'average_rating': case(
                        (Spot.total_num_of_ratings == 0, rate),
                    else_=func.round(cast((((Spot.average_rating * Spot.total_num_of_ratings) - is_rated.rating_choice) + rate) / (Spot.total_num_of_ratings), Numeric), 1)
                    )
                })
                is_rated.rating_choice = rate
                is_rated.created_at = datetime.now(timezone.utc)
            
            else:
                rating = Rating(
                    user_id=current_user,
                    spot_id=spot_id,
                    rating_choice=rate,
                    created_at=datetime.now(timezone.utc)
                )

                Spot.query.filter_by(id=spot_id).update({
                    'total_num_of_ratings': Spot.total_num_of_ratings + 1,
                    'average_rating': case(
                        (Spot.total_num_of_ratings == 0, rate),
                    else_=func.round(cast(((Spot.average_rating * Spot.total_num_of_ratings) + rate) / (Spot.total_num_of_ratings + 1), Numeric), 1)
                    )
                })

                db.session.add(rating)
            db.session.commit()

            updated_spot = Spot.query.with_entities(Spot.average_rating, Spot.total_num_of_ratings).filter_by(id=spot_id).first()
            return jsonify({'message': 'Rating added/updated successfully',
                            'rating': rate,
                            'new_average': updated_spot[0],
                            'new_total_ratings': updated_spot[1]}), 201
        except Exception as e:
            current_app.logger.error(str(e))
            return jsonify({'error': 'This spot is already rated'}), 409

    elif request.method == 'DELETE':
        try:
            if is_rated:
                Spot.query.filter_by(id=spot_id).update({
                    'total_num_of_ratings': Spot.total_num_of_ratings - 1,
                    'average_rating': case(
                        (Spot.total_num_of_ratings <= 1, 0),
                    else_=func.round(cast(
                        ((Spot.average_rating * Spot.total_num_of_ratings) - is_rated.rating_choice) / (Spot.total_num_of_ratings - 1), Numeric
                    ), 1)
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
            current_app.logger.error(str(e))
            return jsonify({'error': 'Failed to remove rating'}), 500
        




    