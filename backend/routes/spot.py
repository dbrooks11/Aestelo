from flask import Blueprint, request, jsonify
from exstensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.spot import Spot
from schemas.spot_schema import spot_schema
from util.outlier_coords import average_location_batch
from util.storage import generate_presigned_url
from util.celery_task import process_photos_with_metadata
from marshmallow import ValidationError
from celery.result import AsyncResult, GroupResult
from celery import chord,group
from exstensions import celery
from sqlalchemy.orm import joinedload

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
        per_page = request.args.get('per_page', default=10, type=int)

        spots = Spot.query.filter_by(user_profile_id=current_user).options(joinedload(Spot.spot_media)).order_by(Spot.date_posted.desc())

        paginated_spots = spots.paginate(
            page=page,
            per_page=per_page
        )

        results = spot_schema.dump(paginated_spots.items, many=True)

        return jsonify({
            'spots': results,
            'total': paginated_spots.total,
            'total_pages': paginated_spots.pages,
            'current_page': paginated_spots.page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500