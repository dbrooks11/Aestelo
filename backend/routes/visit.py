from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from exstensions import db
from models.user import UserProfile
from models.visit import Visit, VisitMedia
from models.spot import Spot
from schemas.visit_schema import visit_schema, visit_media_schema,partial_schema,ValidationError
from routes.auth_required_wrapper import admin_required
from util.photo_processing import photo_processing, get_decimal_coordinates
from util.validation import photo_validation
from util.storage import upload_to_s3
from util.outlier_coords import average_location
from util.decorators import (profile_both_check_banned_removed, block_and_follow_check, profile_current_check_visit, 
                             profile_check_current__banned_removed)


visit_bp = Blueprint('visit', __name__, url_prefix='/visit')

@visit_bp.route('/<string:id>/profile-visit/all', methods = ['GET'])
@jwt_required()
@profile_both_check_banned_removed
@block_and_follow_check
def get_profile_visit_all(id, user_profile, current_user_profile):
        
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)

        visit_query = Visit.active().filter_by(user_id = user_profile.id)

        paginated_visit = visit_query.paginate(
            page=page,
            per_page=per_page
        )
        
        result = visit_schema.dump(paginated_visit.items, many=True)

        return jsonify({
            'visits': result,
            'total': paginated_visit.total,
            'total_pages':paginated_visit.pages,
            'current_page':paginated_visit.page,
        }), 200

    except Exception:
        return jsonify({'error': 'Failed to fetch visit'}), 500
    


@visit_bp.route('/<string:id>/profile-visit/<int:visit_id>', methods = ['GET'])
@jwt_required()
@profile_both_check_banned_removed
@block_and_follow_check
def get_profile_visit(id, visit_id, user_profile, current_user_profile):

    try:
        visit = Visit.active().filter_by(user_id = user_profile.id, visit_id = visit_id).first()
        result = visit_schema.dump(visit)

        if visit is None or (visit.user_id != user_profile.id):
            return jsonify({'error': 'Visit not found'}), 404
        
        return jsonify({'visit': result}), 200
    except Exception:
        return jsonify({'error': 'Failed to fetch visit'}), 500



@visit_bp.route('/profile-visit/<int:visit_id>/edit', methods = ['PATCH'])
@jwt_required()
@profile_current_check_visit
def edit_visit(visit_id, visit, current_user_profile):
    
    edit_limit = 3
    if visit.num_of_edits >= edit_limit:
        return jsonify({'error': f'Visit edit limit reached. Cannot edit a visit more than {edit_limit} times.'}), 403
    
    try:
        data = request.get_json()

        try:
            valid = partial_schema.load(data, partial = True)
        except ValidationError as error:
            return jsonify({"error": error.messages}), 400

        for key,value in valid.items():
            setattr(visit, key, value)

        visit.num_of_edits += 1
        db.session.commit()
        return jsonify({'message':'Visit updated successfully',
                        'updated_visit_fields': valid}), 200

    except Exception:
        db.session.rollback()
        return jsonify({'error':'Failed to update visit'}), 500



@visit_bp.route('/profile-visit/<int:visit_id>/delete', methods = ['DELETE'])
@jwt_required()
@profile_current_check_visit
def delete_visit(visit_id, visit, current_user_profile):
    try:
        visit.is_deleted = True
        visit.deleted_at = datetime.now(timezone.utc)

        UserProfile.query.filter_by(id = current_user_profile.id).update({'visit_count': UserProfile.visit_count - 1}, synchronize_session=False)
    
        db.session.commit()
        return jsonify({'message':'Visit deleted successfully'}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error':'Failed to delete visit'}), 500
    

@visit_bp.route('admin/<string:id>/profile-visit/<int:visit_id>/remove', methods = ['DELETE'])
@jwt_required()
@admin_required
@profile_both_check_banned_removed
def remove_post_admin(id,visit_id, user_profile, current_user_profile):
    visit = Visit.query.get(visit_id)
    
    if visit is None or visit.is_deleted or visit.is_removed:
        return jsonify({'error': 'Visit not found'}), 404
    
    try:
        visit.is_removed = True
        visit.removed_at = datetime.now(timezone.utc)
        visit.removed_by = current_user_profile.id

        UserProfile.query.filter_by(id = user_profile.id).update({'visit_count': UserProfile.visit_count - 1}, synchronize_session=False)

        db.session.commit()
        return jsonify({'message':'Visit removed by admin successfully'}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error':'Failed to remove Visit'}), 500
    


@visit_bp.route('/upload-photos', methods = ['POST'])
@jwt_required()
def upload_photos():
    current_user = get_jwt_identity()

    files = request.files.getlist('photo')

    if not files or len(files) == 0:
        return jsonify({'error':'No photos provided'}), 400

    max_photo_count = 10
    if len(files) > max_photo_count:
        return jsonify({'error': f'Maximum {max_photo_count} photos per visit'})
    
    photo_bytes = [pht.read() for pht in files]

    # validated_bytes, errors = photo_validation(*photo_bytes)
    # if errors:
    #    return jsonify({'error': 'photos rejected', 'details': errors}), 400

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
                failed_photo_url = upload_to_s3(pht_data['photo'], current_user, folder='failed_photos')
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
                'suggestion': 'Please select photos taken at the same place, or create separate spots for different locations.'
            }), 400
        
        uploaded_photos = []
        for pht_data_r2 in proccessed_photos:
            photo_url = upload_to_s3(pht_data_r2['photo_bytes'], current_user, folder='visits')
            thumb_url = upload_to_s3(pht_data_r2['thumbnail_bytes'], current_user, folder = 'visit_thumbnails')
            
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
    


@visit_bp.route('/create/under-spot/<int:spot_id>', methods = ['POST'])
@jwt_required()
def create_visit(spot_id):
    current_user = get_jwt_identity()
    current_user_profile = UserProfile.query.get(current_user)
    spot = Spot.query.get(spot_id)

    if current_user_profile is None:
        return jsonify({'error': 'Profile not found'}), 404
    
    if current_user_profile.is_deleted:
        return jsonify({'error': 'Profile does not exist'}), 404
    
    if current_user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    if spot is None or spot.is_deleted or spot.is_removed:
        return jsonify({'error': 'Spot does not exist'}), 404
    
    data = request.get_json()

    if not isinstance(data, dict):
    # This handles None (no data) or a string (malformed data)
        return jsonify({'error': 'Invalid or malformed data provided'}), 400
    
    if data.get('photos') is None or data.get('location') is None or data.get('photo_count') is None:
        return jsonify({'error':'Invalid data provided'}), 400
    
    avg_location = data.get('location', {})

    coords_spot_visit = [spot.refined_location, avg_location]
    avg_location_spot_visit = average_location(coords_spot_visit)

    #checks if the distance between the visit location and spot location is far so user dont create falsey visits
    max_meter_distance = 30
    if avg_location_spot_visit is None:
        return jsonify({
                'error': 'Visit is from a different location than the spot',
                'message': f'Visit must be taken at the same location (within {max_meter_distance} of the spot).',
                'suggestion': 'Please make sure visit is taken at the same place'
            }), 400
    

    music_song = data.get('music_track_id')
    caption = data.get('caption')
    hashtags = data.get('hashtags', [])
    photos = data.get('photos')
    avg_location = data.get('location')
    num_of_photos = data.get('photo_count')


    try:
        try:
            #Load visit data to verify and create visit
            data_to_load = { 
                'refined_location': avg_location,
                'music_track_id': music_song,
                'caption': caption,
                'hashtags': hashtags,
                'total_num_of_photos': num_of_photos 
            }
            valid_visit_data = visit_schema.load(data_to_load, partial = True)
        except ValidationError as error:
            return jsonify({"error": error.messages}), 400
        
        new_visit = Visit(
            spot_id = spot.spot_id,
            user_id = current_user_profile.id,
            refined_location = valid_visit_data.get('refined_location'),
            music_track_id = valid_visit_data.get('music_track_id'),
            caption = valid_visit_data.get('caption'),
            total_num_of_photos = valid_visit_data.get('total_num_of_photos'),
            hashtags = valid_visit_data.get('hashtags',[])
        )

        db.session.add(new_visit)
        db.session.flush()

        for position, pht_data in enumerate(photos, start=1):
            try:

                #creates media for each post and makes media info in database
                visit_media_to_load = { 
                    'index': position,
                    "thumbnail_url": pht_data.get('thumbnail_url'),
                    "thumb_media_type": 'photo',
                    'photo_url': pht_data.get('photo_url'),
                    'photo_type': 'photo',
                    'width':pht_data.get('width'),
                    'height':pht_data.get('height') 
                }
                valid_media_data = visit_media_schema.load(visit_media_to_load, partial = True)
            except ValidationError as error:
                return jsonify({"error": error.messages}), 400
            
            new_visit_media = VisitMedia(
                visit_id = new_visit.visit_id,
                uploaded_by = current_user_profile.id,
                index = position,
                photo_url=valid_media_data.get('photo_url'),     
                thumbnail_url=valid_media_data.get('thumbnail_url'),
                photo_type='photo',
                thumb_media_type='photo',
                width = valid_media_data.get('width'),
                height = valid_media_data.get('height')
            )

            db.session.add(new_visit_media)
            db.session.flush()

           

            #cehcks location data and makes location info database
            location_data_to_load = {
                "latitude": pht_data.get('latitude'),
                "longitude": pht_data.get('longitude'),
                "altitude": pht_data.get('altitude'),
            }

            

    
        UserProfile.query.filter_by(id = current_user_profile.id).update({'visit_count': UserProfile.visit_count + 1}, synchronize_session=False)

        Spot.query.filter_by(spot_id = spot_id).update({'total_visits': Spot.total_visits + 1}, synchronize_session=False)

        db.session.commit()
        return visit_schema.dump(new_visit), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create spot: {str(e)}'}), 500
            





    




