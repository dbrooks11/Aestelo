from flask import Blueprint, request, jsonify, current_app
from io import BytesIO
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import exists
from exstensions import db
from models.block_profile import BlockProfile
from models.followers_and_following import Follow
from models.music_track import MusicTrack
from models.auth import AuthUser
from schemas.music_schema import music_track_schema
from schemas.user_schema import user_profile_schema, profile_can_edit, partial_schema ,profile_viewing, ValidationError
from util.music_track import set_track
from util.storage import upload_to_r2, delete_file_r2
from util.photo_processing import photo_processing_one_img
from util.decorators import profile_check_current__banned_removed

profile_bp = Blueprint('profile',__name__, url_prefix='/profile')

#done testing
@profile_bp.route('/me', methods = ['GET','PATCH'])
@jwt_required()
@profile_check_current__banned_removed
def profile_me(user_profile):

    if request.method == 'GET':
        try:
            return jsonify({'my_profile': user_profile_schema.dump(user_profile)}), 200
        except Exception:
            return jsonify({'error': 'Failed to fetch profile'}), 500
    
    if request.method == 'PATCH':
        
        try:
            form_data = request.form.to_dict()
            
            try:
                validate_data = profile_can_edit.load(form_data, partial=True)    
            except ValidationError as e:
                return jsonify({'error': e.messages}),400
            
            form_files = request.files
            profile_photo_compressed = None
            profile_banner_compressed = None
            profile_photo_filepath = None
            profile_banner_filepath = None

            old_photo_path = user_profile.profile_photo
            old_banner_path = user_profile.profile_banner
            
            try:
                if 'profile_photo' in form_files:
                    profile_photo_compressed: list | BytesIO = photo_processing_one_img(form_files.get('profile_photo'), is_banner=False, current_user_id=user_profile.id)

                    if isinstance(profile_photo_compressed, list):
                        return jsonify({'error': {'profile_photo': profile_photo_compressed[0]}}),400
                    
                    try:
                        profile_photo_filepath: str = upload_to_r2(file_obj=profile_photo_compressed, user_id=user_profile.id, folder='profile_photo')
                    except Exception as e:
                        return jsonify({'error': str(e)})

                if 'profile_banner' in form_files:
                    profile_banner_compressed: list | BytesIO = photo_processing_one_img(form_files.get('profile_banner'), is_banner=True, current_user_id=user_profile.id)

                    if isinstance(profile_banner_compressed, list):
                        return jsonify({'error': {'profile_banner': profile_banner_compressed[0]}}), 400
                    
                    try:
                        profile_banner_filepath: str = upload_to_r2(file_obj=profile_banner_compressed, user_id=user_profile.id, folder='profile_banner')
                    except Exception as e:
                        return jsonify({'error': str(e)})
                    
            except Exception as e:
                current_app.logger.error(f"Image processing failed: {str(e)}")
                return jsonify({'error': f'Image processing failed: {str(e)}'}), 500

            
            file_dict = {
                "profile_photo": profile_photo_filepath,
                "profile_banner": profile_banner_filepath

            }

            try:
                validate_files = profile_can_edit.load(file_dict, partial = True)
            except ValidationError as e:
                return jsonify({'error': e.messages}),400
            
            for key, value in validate_data.items():
                if key == 'username':
                    auth_user = AuthUser.query.get(user_profile.id)
                    auth_user.username = validate_data['username']
                setattr(user_profile,key, value)

            if profile_photo_filepath:
                user_profile.profile_photo = profile_photo_filepath
            if profile_banner_filepath:
                user_profile.profile_banner = profile_banner_filepath

            db.session.commit() 

            try:
                if profile_photo_filepath and old_photo_path:
                    delete_file_r2(old_photo_path)
                if profile_banner_filepath and old_banner_path:
                    delete_file_r2(old_banner_path)
            except Exception as e:
                current_app.logger.warning(f"Failed to delete old images: {str(e)}")
                return jsonify({'error': str(e)})
                
            return jsonify({'message': 'profile updated',
                            'updated_fields': {'profile_banner': validate_files['profile_banner'],
                                               'profile_photo': validate_files['profile_photo'],
                                               'username': form_data.get('username'),
                                               'bio': form_data.get('bio')}}), 200
        except Exception:
            db.session.rollback()
            current_app.logger.error(f"Database Update Failed: {str(e)}")

            try:
                if profile_photo_filepath: 
                    delete_file_r2(profile_photo_filepath)
                if profile_banner_filepath: 
                    delete_file_r2(profile_banner_filepath)
            except:
                pass

            return jsonify({'error': 'Failed to update profile'}), 500
        

#Partially done, test blocking and following functionality
@profile_bp.route('/<string:id>', methods = ['GET'])
@jwt_required()
@profile_check_current__banned_removed
def user_profile(id, user_profile):
    
    is_blocked = db.session.query(exists().where((BlockProfile.blocker_id ==user_profile.id) & (BlockProfile.blocked_id == id))).scalar()

    is_current_user_blocking = db.session.query(exists().where((BlockProfile.blocker_id == id) & (BlockProfile.blocked_id == user_profile.id))).scalar()
    
    if is_blocked or is_current_user_blocking:
        return jsonify({'error': 'Profile unavailable'}), 404
    
    #checks if the profile the user is veiwing is themselves
    if user_profile.id == id:
        try:
            return jsonify({'me': user_profile_schema.dump(user_profile)}), 200
        except Exception:
            return jsonify({'error': 'Failed to fetch profile'}), 500
    
    #check if current user is a follower of the person's profile they are trying to view
    is_following = db.session.query(exists().where((Follow.follower_id == user_profile.id) & (Follow.following_id == id))).scalar()

    #if user profile is private, check if the person that is trying to view it is following them
    if user_profile.is_private and not is_following:
        try:
            return jsonify({'user_profile':partial_schema.dump(user_profile)}), 200
        except Exception:
            return jsonify({'error': 'Failed to fetch profile'}), 500
        
    return jsonify({'user_profile':profile_viewing.dump(user_profile)}), 200
    
    
#TODO: test when music is added       
# @profile_bp.route('/add-track', methods = ['POST'])
# @jwt_required()
# @profile_check_current__banned_removed
# def add_track_profile(user_profile):
    
#     if not user_profile.is_prem_account:
#         return jsonify({'message':'Premium account required'}), 403
    
#     track_data = request.get_json()

#     if not track_data or 'music_track_id' not in track_data:
#         return jsonify({'error':'Invalid track data'}), 400

#     try:
#         track = MusicTrack.query.get(track_data.get('music_track_id'))

#         if track:
#             track.times_used += 1
#             user_profile.music_track_id = track.music_track_id
#         else:
#             new_track = set_track(track_data=track_data)
#             user_profile.music_track_id = new_track.music_track_id
#             db.session.add(new_track)
        
#         result = music_track_schema.dump(track) if track else music_track_schema.dump(new_track)
#         db.session.commit()
#         return jsonify({'message':'Track added successfully',
#                         'track': result}), 201
#     except Exception:
#         db.session.rollback()
#         return jsonify({'error':'Failed to add track'}), 500


# @profile_bp.route('/remove-track', methods = ['DELETE'])
# @jwt_required()
# @profile_check_current__banned_removed
# def remove_track_profile(user_profile):
#     if not user_profile.is_prem_account:
#         return jsonify({'message':'Premium account required'}), 403
    
#     if user_profile.music_track_id is None:
#         return jsonify({'message':'No track playing on your profile. Please add a track first.'}), 400

#     try:
#         user_profile.music_track_id = None
#         db.session.commit()
#         return jsonify({'message':'Track removed successfully'}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error':'Failed to remove track',
#                         'errors': str(e)}), 500
    
