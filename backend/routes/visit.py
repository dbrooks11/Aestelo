from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from app import db
from models.user import UserProfile
from models.block_profile import BlockProfile
from models.followers_and_following import Follow
from models.visit import Visit, VisitMedia
from models.post import Post
from models.location import Location
from schemas.visit_schema import visit_schema, visit_media_schema,ValidationError
from schemas.location_schema import location_schema
from routes.auth_required_wrapper import auth_required, admin_required
from util.photo_processing import photo_processing, get_decimal_coordinates
from util.validation import photo_validation
from util.storage import upload_to_r2
from util.outlier_coords import average_location


visit_bp = Blueprint('visit', __name__, url_prefix='/visit')

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
    


visit_bp.route('/upload-photos', methods = ['POST'])
@auth_required
def upload_photos():
    current_user = request.current_user.user.id

    files = request.files.getlist('photos')

    if not files or len(files) == 0:
        return jsonify({'error':'No photos provided'}), 400

    max_photo_count = 10
    if len(files) > max_photo_count:
        return jsonify({'error': f'Maximum {max_photo_count} photos per visit'})
    
    photo_bytes = [pht.read() for pht in files]

    validated_bytes, errors = photo_validation(photo_bytes)

    if errors:
       return jsonify({'error': 'photos rejected', 'details': errors}), 400

    result, status = photo_processing(validated_bytes)

    if status != 200:
        return jsonify(result), status

    uploaded_photos = []
    failed_photos = []
    gps_coords = []
    errors = []
    pht_count = 0

    try:
        for pht_data in result['photos']:
            pht_count +=1
            
            gps = pht_data['gps']
            if not gps:
                lat, long, alt = None, None, None
            else:
                lat, long, alt = get_decimal_coordinates(gps)
  
            if not lat or not long:
                failed_photo_url = upload_to_r2(pht_data['photo'], current_user, folder='failed_photos')
                failed_photos.append({
                    'failed_photo_url': failed_photo_url,
                    'reason': 'No GPS metadata found',
                    'photo_number': pht_count
                })
                errors.append(f'Photo {pht_count}: No GPS metadata found')
                continue
   
            gps_coords.append({
                'latitude': lat,
                'longitude': long,
                'altitude': alt
            })
        
            photo_url = upload_to_r2(pht_data['photo'], current_user, folder='visits')
            thumb_url = upload_to_r2(pht_data['thumbnail'], current_user, folder = 'visit_thumbnails')
                
            uploaded_photos.append({
                'photo_url': photo_url,
                'thumbnail_url': thumb_url,
                'width': pht_data['width'],
                'height': pht_data['height'],
                'latitude': lat,
                'longitude':long,
                'altitude': alt,
                'gps': gps,
                'order': pht_count
            })

        max_meter_distance = 30
        avg_location = average_location(gps_coords)
        if avg_location is None:
            return jsonify({
                'error': 'Photos are from different locations',
                'message': f'All photos must be taken at the same location (within {max_meter_distance} meters of each other).',
                'suggestion': 'Please select photos taken at the same place, or create separate posts for different locations.'
            }), 400
        
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
                'message': 'photos uploaded successfully',
                'photos': uploaded_photos,
                'location': avg_location,
                'photo_count': len(uploaded_photos)
            }), 200
    
    except Exception:
        return jsonify({'error':'Failed to upload photos'}), 500
    


@visit_bp.route('/create/under-post/<int:post_id>', methods = ['POST'])
@auth_required
def create_visit(post_id):
    current_user = request.current_user.user.id
    current_user_profile = UserProfile.query.get(current_user)
    post = Post.query.get(post_id)

    if not current_user_profile:
        return jsonify({'error':'Profile does not exist'})
    
    if not post or post.is_deleted or post.is_removed:
        return jsonify({'error': 'Post does not exist'}), 404
    
    data = request.get_json()
    if not (data.get('photos') or data.get('location') or data.get('photo_count')):
        return jsonify({'error':'Invalid data provided'}), 400
    
    avg_location = data['location']

    coords_post_visit = [post.refined_location, avg_location]
    avg_location_post_visit = average_location(coords_post_visit)

    #checks if the distance between the visit location and post location is far so user dont create falsey visits
    if avg_location_post_visit is None:
        return({'error':'Visit was not made at post location'}), 500
    

    spotify_song = data.get('spotify_track_id')
    caption = data.get('caption')
    hashtags = data.get('hashtags', [])
    photos = data['photos']
    num_of_photos = data['photo_count']

    try:
        try:
            #Load visit data to verify and create visit
            data_to_load = { 
                'refined_location': avg_location,
                'spotify_track_id': spotify_song,
                'caption': caption,
                'hashtags': hashtags,
                'num_of_photos': num_of_photos 
            }
            visit_schema.load(data_to_load, partial = True)
        except ValidationError as error:
            return jsonify({"error": error.messages}), 400
        
        new_visit = Visit(
            post_id = post.post_id,
            user_profile_id = current_user_profile.id,
            refined_location = avg_location,
            spotify_track_id = spotify_song,
            caption = caption,
            hashtags = hashtags,
        )

        db.session.add(new_visit)
        db.session.flush()

        for position, pht_data in enumerate(photos, start=1):
            try:

                #creates media for each post and makes media info in database
                visit_media_to_load = { 
                    'index': position,
                    'media_url': pht_data['photo_url'],
                    'media_type': 'photo',
                    'width':pht_data['width'],
                    'height':pht_data['height'] 
                }
                visit_media_schema.load(visit_media_to_load, partial = True)
            except ValidationError as error:
                return jsonify({"error": error.messages}), 400
            
            new_visit_media = VisitMedia(
                visit_id = new_visit.visit_id,
                uploaded_by = current_user_profile.id,
                media_url = pht_data['photo_url'],
                media_type = 'photo',
                width = pht_data['width'],
                height = pht_data['height']
            )

            db.session.add(new_visit_media)
            db.session.flush()

            try:

                #cehcks location data and makes location info database
                location_data_to_load = {
                    "latitude": pht_data['latitude'],
                    "longitude": pht_data['longitude'],
                    "altitude": pht_data.get('altitude'),
                }

                location_schema.load(location_data_to_load, partial = True)
            except ValidationError as error:
                return jsonify({"error": error.messages}), 400
            

            location = Location(
                visit_media_id = new_visit_media.visit_media_id,
                latitude = pht_data['latitude'],
                longitude = pht_data['longitude'],
                altitude = pht_data.get('altitude')
            )
            db.session.add(location)

        current_user_profile.visit_count += 1
        db.session.commit()

        return visit_schema.dump(new_visit), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create post: {str(e)}'}), 500
            





    




