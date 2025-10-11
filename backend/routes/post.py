from flask import Blueprint, request, jsonify
from app import db
from models.user import UserProfile
from models.block_profile import BlockProfile
from models.post import Post, PostMedia
from models.followers_and_following import Follow
from models.location import Location
from routes.auth_required_wrapper import auth_required, admin_required
from datetime import datetime, timezone
from schemas.post_schema import post_schema,post_media_schema, ValidationError
from schemas.location_schema import location_schema
from util.image_processing import image_processing, get_decimal_coordinates
from util.validation import image_validation
from util.storage import upload_to_r2
from util.outlier_coords import average_location

post_bp = Blueprint('post', __name__, url_prefix='/post')


@post_bp.route('/<string:username>/profile-posts', methods = ['GET'])
@auth_required
def get_profile_post_all(username):
    current_user = request.current_user.user.id
    user_profile = UserProfile.query.filter_by(username = username).first()

    if not user_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    if user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    is_blocked = BlockProfile.query.filter_by(blocker_id = user_profile.id,
                                              blocked_id = current_user).first()
    is_current_user_blocking = BlockProfile.query.filter_by(blocker_id = current_user,
                                                            blocked_id = user_profile.id).first()

    if is_blocked or is_current_user_blocking:
        return jsonify({'error': 'Profile unavailable'}), 404
    
    if (current_user != user_profile.id) and (user_profile.is_private):
        is_following = Follow.query.filter_by(follower_id = current_user,
                                        following_id = user_profile.id).first()
        if not is_following:
            return jsonify({'error': 'Profile is private'}), 403
    
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)

        post_query = Post.active().filter_by(user_profile_id = user_profile.id)

        paginated_post = post_query.paginate(
            page = page,
            per_page=per_page
        )

        post_list = post_schema.dump(paginated_post.items, many=True)

        return jsonify({
            'posts': post_list,
            'total': paginated_post.total,
            'total_pages': paginated_post.pages,
            'current_page': paginated_post.page
        }), 200
    
    except Exception:
        return jsonify({'error': 'Failed to fetch post'}), 500


@post_bp.route('/<string:username>/profile-post/<int:post_id>', methods = ['GET'])
@auth_required
def get_profile_post(username, post_id):
    current_user = request.current_user.user.id
    user_profile = UserProfile.query.filter_by(username = username).first()
    
    if not user_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    if user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    is_blocked = BlockProfile.query.filter_by(blocker_id = user_profile.id,
                                              blocked_id = current_user).first()
    is_current_user_blocking = BlockProfile.query.filter_by(blocker_id = current_user,
                                                            blocked_id = user_profile.id).first()

    if is_blocked or is_current_user_blocking:
        return jsonify({'error': 'Profile unavailable'}), 404
    
    if (current_user != user_profile.id) and (user_profile.is_private):
        is_following = Follow.query.filter_by(follower_id = current_user,
                                        following_id = user_profile.id).first()
        if not is_following:
            return jsonify({'error': 'Profile is private'}), 403
        
    try:
        post = Post.query.get(post_id)
        result = post_schema.dump(post)
        if not post or (post.user_profile_id != user_profile.id) or post.is_deleted or post.is_removed:
             return jsonify({'error': 'Post not found'}), 404
        return jsonify({'post': result}), 200

    except Exception:
        return jsonify({'error':'Failed to fetch post'}), 500
    

@post_bp.route('/profile-post/<int:post_id>/edit', methods = ['PATCH'])
@auth_required
def edit_post(post_id):
    current_user = request.current_user.user.id
    my_profile = UserProfile.query.get(current_user)
    post = Post.active().filter_by(user_profile_id = current_user, post_id = post_id).first()

    if not my_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    if not post:
        return jsonify({'error': 'You cannot edit this post'}), 403

    try:
        data = request.get_json()
        post.num_of_edits += 1
        
        try:
            post_schema.load(data, partial = True)
        except ValidationError as error:
            return jsonify({"error": error.messages}), 400

        can_edit = ('description','name', 'accessibility')

        for edit_field in can_edit:
            if edit_field in data:
                setattr(post, edit_field, data[edit_field])
        
        
        db.session.commit()
        return jsonify({'message':'Post updated successfully',
                        'updated_post': post_schema.dump(post)}), 200
    except Exception as e:
        db.session.rollback()
        error = getattr(e,'messages', str(e))
        return jsonify({'error': error}), 500


@post_bp.route('/profile-post/<int:post_id>/delete', methods = ['DELETE'])
@auth_required
def delete_post(post_id):
    current_user = request.current_user.user.id
    current_user_profile = UserProfile.query.get(current_user)
    post = Post.active().filter_by(user_profile_id = current_user, post_id =post_id).first()

    if not current_user_profile:
        return jsonify({'error':'Profile not found'}), 404

    if current_user_profile.is_banned:
        return jsonify({'error':'Profile does not exist'}), 404
    
    if (not post) or post.is_deleted or post.is_removed:
        return jsonify({'error':'Post does not exist'}), 404
    
    try:
        post.is_deleted = True
        post.deleted_at = datetime.now(timezone.utc)
        db.session.commit()
        return jsonify({'message':'Post deleted successfully'}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error':'Failed to delete post'}), 500
    


@post_bp.route('admin/profile-post/<int:post_id>/remove', methods = ['DELETE'])
@auth_required
@admin_required
def remove_post_admin(post_id):
    current_user = request.current_user.user.id
    post = Post.active().filter_by(user_profile_id = current_user, post_id = post_id).first()
    
    if not post:
        return jsonify({'error': 'Post unavailable'}), 404
    
    try:
        post.is_removed = True
        post.removed_at = datetime.now(timezone.utc)
        db.session.commit()
        return jsonify({'message':'Post removed successfully'}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error':'Failed to remove post'}), 500
    
    

@post_bp.route('/upload-images', methods=['POST'])
@auth_required
def upload_images():
    current_user_id = request.current_user.user.id

    files = request.files.getlist('images')
    
    if not files or len(files) == 0:
        return jsonify({'error': 'No images provided'}), 400
    
    max_image_count = 5
    if len(files) > max_image_count:
        return jsonify({'error': f'Maximum {max_image_count} images per post'}), 400
    
    image_bytes = [img.read() for img in files]

    validated_bytes, errors = image_validation(*image_bytes)
    if errors:
        return jsonify({'error': 'Images rejected', 'details': errors}), 400
    
    result, status = image_processing(*validated_bytes)
    if status != 200:
        return jsonify(result), status

    uploaded_images = []
    gps_coords = []
    errors = []
    img_count = 0

    try:
        for img_data in result['images']:
            img_count +=1
            image_url = upload_to_r2(img_data['image'], current_user_id, folder='posts')
            thumb_url = upload_to_r2(img_data['thumbnail'], current_user_id, folder= 'post_thumbnails')
            
            gps = img_data.get('gps')
            if gps:
                lat,long,alt = get_decimal_coordinates(gps)
                if lat and long:
                    gps_coords.append({
                        'latitude': lat,
                        'longitude': long,
                        'altitude': alt})
                else:
                    img_count -= 1
                    errors.append(f'Failed to get metadata of Image {img_count}')
                    continue

            
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
        avg_location = average_location(gps_coords) if gps_coords else None
        if avg_location is None:
            return jsonify({
                'error': 'Photos are from different locations',
                'message': f'All images must be taken at the same location (within {max_meter_distance} meters of each other).',
                'suggestion': 'Please select photos taken at the same place, or create separate posts for different locations.'
            }), 400

        return jsonify({
            'message': 'Images uploaded successfully',
            'images': uploaded_images,
            'location': avg_location,
            'image_count': len(uploaded_images),
            'error': errors
        }), 200
    
    except Exception:
        return jsonify({'error':'Failed to upload images'}), 500
    

@post_bp.route('/create', methods = ['POST'])
@auth_required
def create_post():
    current_user = request.current_user.user.id
    current_user_profile = UserProfile.query.get(current_user)

    data = request.get_json()

    if not (data.get('images') or data.get('location') or data.get('image_count')):
        return jsonify({'error':'Invalid data provided'}), 400

    post_name = data.get('name')
    post_description = data.get('description')
    accessibility = data.get('accessibility')
    tags = data.get('tags', [])
    images = data['images']
    avg_location = data['location']
    num_of_images = data['image_count']

    try:

        try:
            data_to_load = {
                "name": post_name, 
                "refined_location": avg_location,
                "description": post_description,
                "total_num_of_images": num_of_images, 
                "tags": tags
            }
            post_schema.load(data_to_load, partial = True)
        except ValidationError as error:
            return jsonify({"error": error.messages}), 400

        new_post = Post(
            user_profile_id=current_user,
            name=post_name,
            refined_location = avg_location,
            description=post_description,
            total_num_of_photos= num_of_images,
            accessibility=accessibility,
            tags=tags
        )
        db.session.add(new_post)
        db.session.flush()

        for img_data in images:

            media_data_to_load = {
                "thumbnail_url": img_data['thumbnail_url'],
                "thumb_media_type": 'image',
                "media_url": img_data['image_url'],
                "media_type": 'image',
                "width": img_data['width'],
                "height": img_data['height']
            }
            try:
                post_media_schema.load(media_data_to_load, partial = True)
            except ValidationError as error:
                return jsonify({"error": error.messages}), 400

            post_media = PostMedia(
                post_id=new_post.post_id,
                uploaded_by=current_user,
                media_url=img_data['image_url'],     
                thumbnail_url=img_data['thumbnail_url'],
                media_type='image',
                thumb_media_type='image',
                width=img_data['width'],
                height=img_data['height'],
            )
            db.session.add(post_media)
            db.session.flush()

            try:

                location_data_to_load = {
                    "is_visit": False,
                    "latitude": img_data['latitude'],
                    "longitude": img_data['longitude'],
                    "altitude": img_data.get('altitude') 
                }
                location_schema.load(location_data_to_load, partial = True)
            except ValidationError as error:
                return jsonify({"error": error.messages}), 400

            location = Location(
                post_media_id=post_media.post_media_id,
                is_visit=False,
                latitude=img_data['latitude'],
                longitude=img_data['longitude'],
                altitude=img_data.get('altitude'),
                is_long_lat=img_data['gps'] is not None,
            )
            db.session.add(location)
            db.session.flush()

        current_user_profile.post_count += 1
        db.session.commit()

        return post_schema.dump(new_post), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create post: {str(e)}'}), 500

