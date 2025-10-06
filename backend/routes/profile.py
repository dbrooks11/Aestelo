from flask import Blueprint, request, jsonify
from app import db
from models.user import UserProfile
from schemas.profile_schema import ProfileSchema
from auth_required_wrapper import auth_required

profile_bp = Blueprint('profile',__name__, url_prefix='/profile')

@profile_bp.route('/profile/me', methods = ['GET','PUT'])
@auth_required
def profile_me():
    user_id = request.current_user.user.id

    my_profile = UserProfile.query.get(user_id)

    if not my_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    if request.method == 'GET':
        return jsonify({'my_profile': my_profile.to_dict()})
    
    if request.method == 'PUT':
        data = request.get_json()

        can_edit = ('banner_theme','profile_image','bio','instagram','facebook','twitter_x',
                    'tiktok','is_private','show_online_status')
        
        for edit_field in can_edit:
            if edit_field in data:
                setattr(my_profile, edit_field, data[edit_field])

@profile_bp.route('/profile/<string:username>', methods = ['GET'])
@auth_required
def user_profile(username):
    user_profile = UserProfile.query.filter_by(username = username).first()
    current_user = request.current_user.user.id
    current_user_profile = UserProfile.query.get(id)


    if not user_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    #checks if the profile the user is veiwing is themselves
    if user_profile.id == current_user:
        return jsonify({'me': user_profile.to_dict()}), 200

    #if user profile is private, check if the person that is trying to view it is following them
    if user_profile.is_private:
        if user_profile.id in current_user_profile.followers:
            jsonify({'user_profile':user_profile.to_dict_public}), 200
        else:
            return jsonify({'user_profile':user_profile.to_dict_private}), 200

    if user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    return jsonify({'user_profile':user_profile.to_dict_public()}), 200
    