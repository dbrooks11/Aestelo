from app import db
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import UserProfile
from models.post import Post, PostMedia
from models.location import Location
from routes.auth_required_wrapper import admin_required
from datetime import datetime, timezone
from schemas.post_schema import post_schema,post_media_schema, ValidationError, partial_schema
from schemas.location_schema import location_schema
from util.photo_processing import photo_processing, get_decimal_coordinates
from util.validation import photo_validation
from util.storage import upload_to_r2
from util.outlier_coords import average_location
from util.decorators import (profile_both_check_banned_removed, block_and_follow_check,
                             profile_current_check_post)

post_bp = Blueprint('post', __name__, url_prefix='/post')

#done latency route test
@post_bp.route('/<string:id>/profile-post/all', methods = ['GET'])
@jwt_required()
@profile_both_check_banned_removed
@block_and_follow_check
def get_profile_post_all(id, user_profile, current_user_profile):
    
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)

        post_query = Post.active().filter_by(user_profile_id = user_profile.id)

        paginated_post = post_query.paginate(
            page = page,
            per_page=per_page
        )

        result = post_schema.dump(paginated_post.items, many=True)

        return jsonify({
            'posts': result,
            'total': paginated_post.total,
            'total_pages': paginated_post.pages,
            'current_page': paginated_post.page
        }), 200
    
    except Exception:
        return jsonify({'error': 'Failed to fetch post'}), 500

#done latency route test
@post_bp.route('/<string:id>/profile-post/<int:post_id>', methods = ['GET'])
@jwt_required()
@profile_both_check_banned_removed
@block_and_follow_check
def get_profile_post(id, post_id, user_profile, current_user_profile):
        
    try:
        post = Post.active().filter_by(user_profile_id = user_profile.id, post_id = post_id).first()
        result = post_schema.dump(post)

        if post is None or (post.user_profile_id != user_profile.id):
             return jsonify({'error': 'Post not found'}), 404
        
        return jsonify({'post': result}), 200

    except Exception:
        return jsonify({'error':'Failed to fetch post'}), 500
    
#done latency test route
@post_bp.route('/profile-post/<int:post_id>/edit', methods = ['PATCH'])
@jwt_required()
@profile_current_check_post
def edit_post(post_id, current_user_profile, post):
    
    edit_limit = 3
    if post.num_of_edits >= edit_limit:
        return jsonify({'error': f'Post edit limit reached. Cannot edit a post more than {edit_limit} times.'}), 403

    try:
        data = request.get_json()

        try:
            valid = partial_schema.load(data, partial = True)
        except ValidationError as error:
            return jsonify({"error": error.messages}), 400
        
        for key,value in valid.items():
            setattr(post,key,value)

        post.num_of_edits += 1
        db.session.commit()
        return jsonify({'message':'Post updated successfully',
                        'updated_post_fields': valid}), 200
    except Exception as e:
        db.session.rollback()
        error = getattr(e,'messages', str(e))
        return jsonify({'Failed to edit post': error}), 500

#done latency test route
@post_bp.route('/profile-post/<int:post_id>/delete', methods = ['DELETE'])
@jwt_required()
@profile_current_check_post
def delete_post(post_id, current_user_profile, post):

    try:
        post.is_deleted = True
        post.deleted_at = datetime.now(timezone.utc)

        current_user_profile.post_count -= 1
        db.session.commit()
        return jsonify({'message':'Post deleted successfully'}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error':'Failed to delete post'}), 500
    

@post_bp.route('admin/<string:id>/profile-post/<int:post_id>/remove', methods = ['DELETE'])
@jwt_required()
@admin_required
@profile_current_check_post
def remove_post_admin(id, post_id, current_user_profile, post):
    user_profile = UserProfile.query.get(id)
    
    try:
        post.is_deleted = True
        post.deleted_at = datetime.now(timezone.utc).strftime('%b %d, %Y')

        UserProfile.query.filter_by(id = user_profile.id).update({'post_count': UserProfile.post_count - 1}, synchronize_session=False)
        
        db.session.commit()
        user_profile.post_count -= 1
        return jsonify({'message':'Post removed by admin successfully'}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error':'Failed to remove Post'}), 500
    
    
#done latency test route
@post_bp.route('/upload-photos', methods=['POST'])
@jwt_required()
def upload_photos():  
    current_user = get_jwt_identity()

    files = request.files.getlist('photo')
    
    if not files or len(files) == 0:
        return jsonify({'error': 'No photos provided'}), 400
    
    max_photo_count = 5
    if len(files) > max_photo_count:
        return jsonify({'error': f'Maximum {max_photo_count} photos per post'}), 400
    
    photo_bytes = [pht.read() for pht in files]

    # validated_bytes, errors = photo_validation(*photo_bytes)
    # if errors:
    #     return jsonify({'error': 'photos rejected', 'details': errors}), 400
    
    result, status = photo_processing(*photo_bytes)
    if status != 200:
        return jsonify(result), status

    proccessed_photos = []
    failed_photos = []
    gps_coords = []
    errors = []
    pht_count = 0

    try:
        for pht_data in result['photos']:
            pht_count +=1
            lat, long, alt = None, None, None

            gps = pht_data['gps']
            lat, long, alt = get_decimal_coordinates(gps)
            if not lat or not long:
                failed_photo_url = upload_to_r2(pht_data['photo'], current_user, folder='failed_photos')
                failed_photos.append({
                    'failed_photo_url': failed_photo_url,
                    'reason': 'No metadata found',
                    'photo_number': pht_count
                })
                errors.append(f'Photo {pht_count}: No metadata found')
                continue

            gps_coords.append({
                'latitude': lat,
                'longitude': long,
                'altitude': alt
            })
            
            proccessed_photos.append({
                'photo_bytes': pht_data['photo'],
                'thumbnail_bytes': pht_data['thumbnail'],
                'width': pht_data['width'],
                'height': pht_data['height'],
                'latitude': lat,
                'longitude':long,
                'altitude': alt,
                'gps': gps,
                'order': pht_count
            })
        
        if not proccessed_photos:
            return jsonify({'error':'No valid photos submitted'})

        max_meter_distance = 30
        avg_location = average_location(gps_coords)
        if avg_location is None:
            return jsonify({
                'error': 'Photos are from different locations',
                'message': f'All photos must be taken at the same location (within {max_meter_distance} meters of each other).',
                'suggestion': 'Please select photos taken at the same place, or create separate posts for different locations.'
            }), 400
        
        uploaded_photos = []
        for pht_data_r2 in proccessed_photos:
            photo_url = upload_to_r2(pht_data_r2['photo_bytes'], current_user, folder='posts')
            thumb_url = upload_to_r2(pht_data_r2['thumbnail_bytes'], current_user, folder = 'post_thumbnails')
            
            uploaded_photos.append({
                'photo_url': photo_url,
                'thumbnail_url': thumb_url,
                'width': pht_data_r2['width'],
                'height': pht_data_r2['height'],
                'latitude': pht_data_r2['latitude'],
                'longitude':pht_data_r2['longitude'],
                'altitude': pht_data_r2['altitude'],
                'order': pht_data_r2['order']
            })
                
        
        if errors:
            return jsonify({
                'message': f'{len(uploaded_photos)}/{len(files)} photos were uploaded successfully',
                'uploaded_photos': uploaded_photos,
                'failed_photos': failed_photos,
                'location': avg_location,
                'photo_count': len(uploaded_photos),
                'error': errors
            }), 200
        else:
            return jsonify({
                'message': 'Photos uploaded successfully',
                'photos': uploaded_photos,
                'location': avg_location,
                'photo_count': len(uploaded_photos)
            }), 200
    
    except Exception as e:
        error = getattr(e,'messages', str(e))
        return jsonify({'error': error}), 500
        # return jsonify({'error':'Failed to upload photos'}), 500
    

#done latency test route
@post_bp.route('/create', methods = ['POST'])
@jwt_required()
def create_post():
    current_user = get_jwt_identity()
    current_user_profile = UserProfile.query.get(current_user)

    if current_user_profile is None:
        return jsonify({'error': 'Profile not found'}), 404
    
    if current_user_profile.is_deleted:
        return jsonify({'error': 'Profile does not exist'}), 404
    
    if current_user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404

    data = request.get_json()
    if not isinstance(data, dict):
    # This handles None (no data) or a string (malformed data)
        return jsonify({'error': 'Invalid or malformed JSON data provided'}), 400

    if data.get('photos') is None or data.get('location') is None or data.get('photo_count') is None:
        return jsonify({'error':'Invalid data provided'}), 400
    

    post_name = data.get('name')
    post_description = data.get('description')
    accessibility = data.get('accessibility')
    hashtags = data.get('hashtags', [])
    photos = data.get('photos')
    avg_location = data.get('location')
    num_of_photos = data.get('photo_count')

    try:

        try:
            data_to_load = {
                "name": post_name, 
                "refined_location": avg_location,
                "description": post_description,
                "total_num_of_photos": num_of_photos,
                "accessibility": accessibility, 
                "hashtags": hashtags
            }
            valid_post_data = post_schema.load(data_to_load, partial = True)
        except ValidationError as error:
            return jsonify({"error": error.messages}), 400

        new_post = Post(
            user_profile_id=current_user_profile.id,
            name=valid_post_data.get('name'),
            refined_location = valid_post_data.get('refined_location'),
            description= valid_post_data.get('description'),
            total_num_of_photos= valid_post_data.get('total_num_of_photos'),
            accessibility= valid_post_data.get('accessibility'),
            hashtags=valid_post_data.get('hashtags'),
            date_posted = datetime.now(timezone.utc)
        )
        db.session.add(new_post)
        db.session.flush()


        for position, pht_data in enumerate(photos, start=1):
            media_data_to_load = {
                "thumbnail_url": pht_data.get('thumbnail_url'),
                "thumb_media_type": 'photo',
                "photo_url": pht_data.get('photo_url'),
                "photo_type": 'photo',
                "width": pht_data.get('width'),
                "height": pht_data.get('height')
            }
            try:
                valid_media_data = post_media_schema.load(media_data_to_load, partial = True)
            except ValidationError as error:
                return jsonify({"error": error.messages}), 400

            post_media = PostMedia(
                post_id=new_post.post_id,
                uploaded_by=current_user_profile.id,
                index = position,
                photo_url=valid_media_data.get('photo_url'),     
                thumbnail_url=valid_media_data.get('thumbnail_url'),
                photo_type='photo',
                thumb_media_type='photo',
                width=valid_media_data.get('width'),
                height=valid_media_data.get('height'),
            )
            db.session.add(post_media)
            db.session.flush()

            try:

                location_data_to_load = {
                    "latitude": pht_data.get('latitude'),
                    "longitude": pht_data.get('longitude'),
                    "altitude": pht_data.get('altitude') 
                }
                valid_location_data = location_schema.load(location_data_to_load, partial = True)
            except ValidationError as error:
                return jsonify({"error": error.messages}), 400

            location = Location(
                post_media_id=post_media.post_media_id,
                latitude=valid_location_data.get('latitude'),
                longitude=valid_location_data.get('longitude'),
                altitude=valid_location_data.get('altitude'),
            )
            db.session.add(location)
        current_user_profile.post_count += 1
        db.session.commit()
        
        return post_schema.dump(new_post), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create post: {str(e)}'}), 500

