from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from app import db
from models.user import UserProfile
from models.block_profile import BlockProfile
from models.followers_and_following import Follow
from models.visit import Visit
from schemas.user_schema import ProfileSchema
from schemas.visit_schema import visit_schema, ValidationError
from routes.auth_required_wrapper import auth_required, admin_required
from util.image_processing import image_processing, get_decimal_coordinates
from util.validation import image_validation
from util.storage import upload_to_r2
from util.outlier_coords import average_location

visit_bp = Blueprint('visit', __name__, '/visit')

@visit_bp.route('/<string:username>/profile-visits', methods = ['GET'])
@auth_required
def get_profile_visit_all(username):
    current_user = request.current_user.user.id
    user_profile = UserProfile.query.filter_by(username=username).first()

    if not user_profile:
        return jsonify({'error':'Profile not found'}), 404

    if user_profile.is_banned:
        return jsonify({'error':'Profile does not exist'}), 404
    
    is_blocked = BlockProfile.query.filter_by(blocker_id = user_profile.id,
                                              blocked_id = current_user).first()
    is_current_user_blocking = BlockProfile.query.filter_by(blocker_id = current_user,
                                                            blocked_id = user_profile.id).first()

    if is_blocked or is_current_user_blocking:
        return jsonify({'error':'Profile unavailable'}), 404


    if (current_user != user_profile.id) and (user_profile.is_private):
        is_following = Follow.query.filter_by(follower_id = current_user,
                                        following_id = user_profile.id).first()
        if not is_following:
            return jsonify({'error': 'Profile is private'}), 403
        
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)

        visit_query = Visit.query.filter_by(user_profile_id = user_profile.id)

        paginated_visit = visit_query.paginate(
            page=page,
            per_page=per_page
        )
        
        result = visit_schema.dump(paginated_visit, many=True)

        jsonify({
            'visits': result,
            'total': paginated_visit.total,
            'total_pages':paginated_visit.pages,
            'current_page':paginated_visit.page,
        }), 200

    except Exception:
        return jsonify({'error': 'Failed to fetch visit'}), 500
    
    

@visit_bp.route('/<string:username>/profile-visit/<int:visit_id>', methods = ['GET'])
@auth_required
def get_profile_visit(username, visit_id):
    current_user = request.current_user.user.id
    user_profile = UserProfile.query.filter_by(username = username).first()

    
    if not user_profile:
        return jsonify({'error':'Profile not found'}), 404

    if user_profile.is_banned:
        return jsonify({'error':'Profile does not exist'}), 404
    
    is_blocked = BlockProfile.query.filter_by(blocker_id = user_profile.id,
                                              blocked_id = current_user).first()
    is_current_user_blocking = BlockProfile.query.filter_by(blocker_id = current_user,
                                                            blocked_id = user_profile.id).first()

    if is_blocked or is_current_user_blocking:
        return jsonify({'error':'Profile unavailable'}), 404


    if (current_user != user_profile.id) and (user_profile.is_private):
        is_following = Follow.query.filter_by(follower_id = current_user,
                                        following_id = user_profile.id).first()
        if not is_following:
            return jsonify({'error': 'Profile is private'}), 403

    try:
        visit = Visit.query.get(visit_id = visit_id)
        result = visit_schema.dump(visit)
        if not visit or (visit.user_profile_id != user_profile.id) or visit.is_deleted or visit.is_removed:
            return jsonify({'error': 'Visit not found'}), 404

        return jsonify({'visit': result})
    except Exception:
        return jsonify({'error': 'Failed to fetch visit'}), 500



@visit_bp.route('/profile_visit/<int:visit_id>/edit', methods = ['PATCH'])
@auth_required
def edit_visit(visit_id):
    current_user = request.current_user.user.id
    current_user_profile = UserProfile.query.get(current_user)
    visit = Visit.active().filter_by(user_profile_id = current_user, visit_id = visit_id).first()

    if not current_user_profile:
        return jsonify({'error':'Profile not found'}), 404

    if current_user_profile.is_banned:
        return jsonify({'error':'Profile does not exist'}), 404
    
    if not visit:
        return jsonify({'error': 'Visit not found'}), 404
    
    try:
        data = request.get_json()
        visit.num_of_edits += 1

        try:
            visit_schema.load(data, partial = True)
        except ValidationError as error:
            return jsonify({"error": error.messages}), 400

        can_edit = ('spotify_track_id','caption','hashtags')

        for field in can_edit:
            if field in data:
                setattr(visit,field,data[field])
        
        db.session.commit()
        return jsonify({'message':'Visit updated successfully',
                        'updated_visit': visit_schema.dump(visit)}), 200

    except Exception:
        db.session.rollback()
        return jsonify({'error':'Failed to update visit'}), 500



visit_bp.route('/profile-visit/<int:visit_id>/delete', methods = ['DELETE'])
@auth_required
def delete_visit(visit_id):
    current_user = request.current_user.user.id
    current_user_profile = UserProfile.query.get(current_user)
    visit = Visit.active().filter_by(user_profile_id = current_user, visit_id = visit_id).first()

    if not current_user_profile:
        return jsonify({'error':'Profile not found'}), 404

    if current_user_profile.is_banned:
        return jsonify({'error':'Profile does not exist'}), 404
    
    if (not visit) or visit.is_deleted or visit.is_removed:
        return jsonify({'error':'Visit does not exist'}), 404

    try:
        visit.is_deleted = True
        visit.deleted_at = datetime.now(timezone.utc)
        current_user_profile.visit_count -= 1
        return jsonify({'message':'Visit deleted successfully'}), 200

    except Exception:
        db.session.rollback()
        return jsonify({'error':'Failed to delete visit'}), 500
    

@visit_bp.route('admin/profile-visit/<int:visit_id>/remove', methods = ['DELETE'])
@auth_required
@admin_required
def remove_post_admin(visit_id):
    current_user = request.current_user.user.id
    visit = Visit.active().filter_by(user_profile_id = current_user, visit_id = visit_id).first()
    
    if not visit:
        return jsonify({'error': 'Visit unavailable'}), 404
    
    try:
        visit.is_removed = True
        visit.removed_at = datetime.now(timezone.utc)
        db.session.commit()
        return jsonify({'message':'Visit removed successfully'}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error':'Failed to remove Visit'}), 500
    



visit_bp.route('/upload-images', methods = ['POST'])
@auth_required
def upload_images():
    current_user = request.current_user.user.id

    files = request.files.getlist('images')

    if not files or len(files) == 0:
        return jsonify({'error':'No images provided'}), 400

    max_image_count = 10
    if len(files) > max_image_count:
        return jsonify({'error': f'Maximum {max_image_count} images per visit'})
    
    image_bytes = [img.read() for img in files]

    validated_bytes, errors = image_validation(image_bytes)

    if errors:
       return jsonify({'error': 'Images rejected', 'details': errors}), 400

    result, status = image_processing(validated_bytes)

    if status != 200:
        return jsonify(result), status

    uploaded_images = []
    failed_images = []
    gps_coords = []
    errors = []
    img_count = 0

    try:
        for img_data in result['images']:
            img_count +=1
            
            gps = img_data['gps']
            if gps:
                lat,long,alt = get_decimal_coordinates(gps)
                if lat and long:
                    gps_coords.append({
                        'latitude': lat,
                        'longitude': long,
                        'altitude': alt})
                else:
                    img_count -= 1
                    failed_image_url = upload_to_r2(img_data['image'], current_user, folder='failed_images')
                    failed_images.append({'failed_image_url': failed_image_url})
                    errors.append(f'Failed to get metadata of Image {img_count}')
                    continue
            
            image_url = upload_to_r2(img_data['image'], current_user, folder='visits')
            thumb_url = upload_images(img_data['thumbnail'], current_user, folder = 'visit_thumbnails')
                
            uploaded_images.append({
                'image_url': image_url,
                'thumbnail_url': thumb_url,
                'width': img_data['width'],
                'height': img_data['height'],
                'latitude': lat,
                'longitude':long,
                'altitude': alt,
                'gps': gps,
                'order': img_count
            })

        max_meter_distance = 30
        avg_location = average_location(gps_coords)
        if avg_location is None:
            return jsonify({
                'error': 'Images are from different locations',
                'message': f'All images must be taken at the same location (within {max_meter_distance} meters of each other).',
                'suggestion': 'Please select photos taken at the same place, or create separate posts for different locations.'
            }), 400
        
        if errors:
            return jsonify({
                'message': f'{img_count}/{len(files)} images were uploaded successfully',
                'uploaded_images': uploaded_images,
                'failed_images': failed_images,
                'location': avg_location,
                'image_count': len(uploaded_images),
                'error': errors
            }), 200
        else:
            return jsonify({
                'message': 'Images uploaded successfully',
                'images': uploaded_images,
                'location': avg_location,
                'image_count': len(uploaded_images)
            }), 200
    
    except Exception:
        return jsonify({'error':'Failed to upload images'}), 500




