from flask import Blueprint, request, jsonify
from app import db
from models.user import UserProfile
from models.block_profile import BlockProfile
from models.followers_and_following import Follow
from schemas.user_schema import UserProfileSchema, ValidationError
from routes.auth_required_wrapper import auth_required

profile_bp = Blueprint('profile',__name__, url_prefix='/profile')

@profile_bp.route('/profile/me', methods = ['GET','PATCH'])
@auth_required
def profile_me():
    user_id = request.current_user.user.id

    my_profile = UserProfile.query.get(user_id)
    profile_schema = UserProfileSchema()

    if not my_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    if request.method == 'GET':
        try:
            return jsonify({'my_profile': profile_schema.dump(my_profile)}), 200
        except Exception as e:
            return jsonify({"error": e.messages}), 500
    
    if request.method == 'PATCH':
        try:
            data = profile_schema.load(request.get_json(), partial=True)
            
            # Update fields (schema already filtered dump_only fields)
            for field, value in data.items():
                setattr(my_profile, field, value)
            
            db.session.commit()
            return profile_schema.dump(my_profile), 200
            
        except ValidationError as e:
            db.session.rollback()
            return jsonify({'error': e.messages}), 400
        except Exception:
            db.session.rollback()
            return jsonify({'error': 'Failed to update profile'}), 500



@profile_bp.route('/profile/<string:username>', methods = ['GET'])
@auth_required
def user_profile(username):
    user_profile = UserProfile.query.filter_by(username = username).first()
    current_user = request.current_user.user.id
    profile_schema = UserProfileSchema()

    is_blocked = BlockProfile.query.filter_by(blocker_id = user_profile.id,
                                              blocked_id = current_user).first()
    is_current_user_blocking = BlockProfile.query.filter_by(blocker_id = current_user,
                                                            blocked_id = user_profile.id).first()

    if not user_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
     #check if the user they are trying to veiw is banned
    if user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    if is_blocked or is_current_user_blocking:
        return jsonify({'error': 'Profile unavailable'}), 404
    
    #checks if the profile the user is veiwing is themselves
    if user_profile.id == current_user:
        try:
            return jsonify({'me': profile_schema.dump(user_profile)}), 200
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
            return jsonify({'user_profile':user_profile.to_dict_private()}), 200
        except Exception:
            return jsonify({'error': 'Failed to fetch profile'}), 500
    return jsonify({'user_profile':profile_schema.dump(user_profile)}), 200
    