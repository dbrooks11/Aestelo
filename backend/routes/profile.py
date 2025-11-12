from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import exists
from ..exstensions import db
from ..models.block_profile import BlockProfile
from ..models.followers_and_following import Follow
from ..models.music_track import MusicTrack
from ..models.auth import AuthUser
from ..schemas.music_schema import music_track_schema
from ..schemas.user_schema import user_profile_schema, profile_can_edit, partial_schema ,profile_viewing, ValidationError
from ..util.music_track import set_track
from ..util.decorators import profile_check_current__banned_removed

profile_bp = Blueprint('profile',__name__, url_prefix='/profile')

#done testing
@profile_bp.route('/me', methods = ['GET','PATCH'])
@jwt_required()
@profile_check_current__banned_removed
def profile_me(user_profile):
    current_user = get_jwt_identity()

    if request.method == 'GET':
        try:
            return jsonify({'my_profile': user_profile_schema.dump(user_profile)}), 200
        except Exception:
            return jsonify({'error': 'Failed to fetch profile'}), 500
    
    if request.method == 'PATCH':
        
        try:
            try:
                data = request.get_json()
                valid = profile_can_edit.load(data, partial=True)    
            except ValidationError as e:
                return jsonify({'error': e.messages}),400
            
            if valid.get('username'):
                auth_user = AuthUser.query.get(current_user)
                auth_user.username = valid['username']
            
            for key, value in valid.items():
                setattr(user_profile,key, value)

            db.session.commit() 
            return jsonify({'updated_profile_fields': valid}), 200
        except Exception:
            db.session.rollback()
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
    
    
#todo: test when music is added       
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
    
