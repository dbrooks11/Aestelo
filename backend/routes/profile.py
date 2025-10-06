from flask import Blueprint, request, jsonify
from app import db
from models.user import UserProfile
from models.block_profile import BlockProfile
from models.followers_and_following import Follow
# from schemas.profile_schema import ProfileSchema
from routes.auth_required_wrapper import auth_required

profile_bp = Blueprint('profile',__name__, url_prefix='/profile')

@profile_bp.route('/profile/me', methods = ['GET','PATCH'])
@auth_required
def profile_me():
    user_id = request.current_user.user.id

    my_profile = UserProfile.query.get(user_id)

    if not my_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    if request.method == 'GET':
        try:
            return jsonify({'my_profile': my_profile.to_dict()}), 200
        except Exception:
            return jsonify({'error': 'Failed to get profile'}), 500
    
    if request.method == 'PATCH':
        try:
            data = request.get_json()

            can_edit = ('banner_theme','profile_image','bio','instagram','facebook','twitter_x',
                        'tiktok','is_private','show_online_status')
            
            for edit_field in can_edit:
                if edit_field in data:
                    setattr(my_profile, edit_field, data[edit_field])
            db.session.commit()
            jsonify({'message':'Fields updated successfully'}), 200
        except Exception as e:
            error = getattr(e,'messages', str(e))
            return jsonify({'error': error}), 500



@profile_bp.route('/profile/<string:username>', methods = ['GET'])
@auth_required
def user_profile(username):
    user_profile = UserProfile.query.filter_by(username = username).first()
    current_user = request.current_user.user.id

    is_blocked = BlockProfile.query.filter_by(blocker_id = user_profile.id,
                                              blocked_id = current_user).first()
    is_current_user_blocking = BlockProfile.query.filter_by(blocker_id = current_user,
                                                            blocked_id = user_profile.id).first()

    if is_blocked or is_current_user_blocking:
        return jsonify({'error': 'Profile unavailable'}), 404
   
    if not user_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    #checks if the profile the user is veiwing is themselves
    if user_profile.id == current_user:
        return jsonify({'me': user_profile.to_dict()}), 200
    
    
    #check if the user they are trying to veiw is banned
    if user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    #check if current user is a follower of the person's profile they are trying to view
    is_following = Follow.query.filter_by(follower_id = current_user,
                                          following_id = user_profile.id).first()

    #if user profile is private, check if the person that is trying to view it is following them
    if user_profile.is_private:
        if is_following:
            jsonify({'user_profile':user_profile.to_dict_public()}), 200
        else:
            return jsonify({'user_profile':user_profile.to_dict_private()}), 200
    
    return jsonify({'user_profile':user_profile.to_dict_public()}), 200
    