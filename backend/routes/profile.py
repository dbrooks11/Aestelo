from flask import Blueprint, request, jsonify
from app import db
from models.user import UserProfile
from models.block_profile import BlockProfile
from models.followers_and_following import Follow
from models.spotify_track import SpotifyTrack
from schemas.spotify_schema import spotify_track_schema
from schemas.user_schema import user_profile_schema, ValidationError
from routes.auth_required_wrapper import auth_required
from util.spotify_track import  set_track

profile_bp = Blueprint('profile',__name__, url_prefix='/profile')

@profile_bp.route('/profile/me', methods = ['GET','PATCH'])
@auth_required
def profile_me():
    current_user = request.current_user.user.id

    my_profile = UserProfile.query.get(current_user)

    if my_profile is None:
        return jsonify({'error': 'Profile not found'}), 404
    
    if request.method == 'GET':
        try:
            return jsonify({'my_profile': user_profile_schema.dump(my_profile)}), 200
        except ValidationError as e:
            return jsonify({'error': e.messages}), 400
        except Exception:
            return jsonify({'error': 'Failed to fetch profile'}), 500
    
    if request.method == 'PATCH':
        try:
            try:
                data = user_profile_schema.load(request.get_json(), partial=True)
            except ValidationError as e:
                return jsonify({'error': e.messages}),400

            # Update fields (schema already filtered dump_only fields)
            for field, value in data.items():
                setattr(my_profile, field, value)
            
            db.session.commit()
            return user_profile_schema.dump(my_profile), 200
        
        except Exception:
            db.session.rollback()
            return jsonify({'error': 'Failed to update profile'}), 500
        
        
@profile_bp.route('/add-track', methods = ['POST'])
@auth_required
def add_track_profile():
    current_user = request.current_user.user.id
    current_user_profile = UserProfile.query.get(current_user)

    if current_user_profile is None:
        return jsonify({'error': 'Profile not found'}), 404
    
    if current_user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    if not current_user_profile.is_prem_account:
        return jsonify({'message':'Premium account required'}), 403
    
    track_data = request.get_json()

    if not track_data or 'spotify_track_id' not in track_data:
        return jsonify({'error':'Invalid track data'}), 400

    try:
        track = SpotifyTrack.query.get(track_data['spotify_track_id'])

        if track:
            track.times_used += 1
            current_user_profile.spotify_track_id = track.spotify_track_id
        else:
            new_track = set_track(track_data=track_data)
            current_user_profile.spotify_track_id = new_track.spotify_track_id
            db.session.add(new_track)
        
        result = spotify_track_schema.dump(track) if track else spotify_track_schema.dump(new_track)
        db.session.commit()
        return jsonify({'message':'Track added successfully',
                        'track': result}), 201
    except Exception:
        db.session.rollback()
        return jsonify({'error':'Failed to add track'}), 500


@profile_bp.route('/remove-track', methods = ['DELETE'])
@auth_required
def remove_track_profile():
    current_user = request.current_user.user.id
    current_user_profile = UserProfile.query.get(current_user)

    if current_user_profile is None:
        return jsonify({'error': 'Profile not found'}), 404
    
    if current_user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    if not current_user_profile.is_prem_account:
        return jsonify({'message':'Premium account required'}), 403
    
    if current_user_profile.spotify_track_id is None:
        return jsonify({'message':'No track playing on your profile. Please add a track first.'}), 400

    try:
        current_user_profile.spotify_track_id = None
        db.session.commit()
        return jsonify({'message':'Track removed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':'Failed to remove track',
                        'errors': str(e)}), 500
    

    



@profile_bp.route('/profile/<string:username>', methods = ['GET'])
@auth_required
def user_profile(username):
    user_profile = UserProfile.query.filter_by(username = username).first()
    current_user = request.current_user.user.id

    if user_profile is None:
        return jsonify({'error': 'Profile not found'}), 404
    
     #check if the user they are trying to veiw is banned
    if user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    is_blocked = BlockProfile.query.filter_by(blocker_id = user_profile.id,
                                              blocked_id = current_user).first()
    is_current_user_blocking = BlockProfile.query.filter_by(blocker_id = current_user,
                                                            blocked_id = user_profile.id).first()

    
    if is_blocked or is_current_user_blocking:
        return jsonify({'error': 'Profile unavailable'}), 404
    
    #checks if the profile the user is veiwing is themselves
    if user_profile.id == current_user:
        try:
            return jsonify({'me': user_profile_schema.dump(user_profile)}), 200
        except ValidationError as e:
            return jsonify({'error': e.messages}), 400
        except Exception:
            return jsonify({'error': 'Failed to fetch profile'}), 500
    
    #check if current user is a follower of the person's profile they are trying to view
    is_following = Follow.query.filter_by(follower_id = current_user,
                                          following_id = user_profile.id).first()

    #if user profile is private, check if the person that is trying to view it is following them
    if user_profile.is_private and not is_following:
        try:
            return jsonify({'user_profile':user_profile_schema.dump(user_profile.to_dict_private())}), 200
        except Exception:
            return jsonify({'error': 'Failed to fetch profile'}), 500
        
    return jsonify({'user_profile':user_profile_schema.dump(user_profile)}), 200
    