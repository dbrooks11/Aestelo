from flask import Blueprint, request, jsonify
from app import db
from models.user import UserProfile, UserInfo, UserSettings, UserRole, UserSubscription
from exstensions import supabase, db
from auth_required_wrapper import auth_required

auth_bp = Blueprint('auth', __name__, url_prefix='auth')

@auth_bp.route('/signup', methods = ['POST'])
def signup():

    token  = request.headers.get('Authorization', '').replace('Bearer ', '')

    try:
        user = supabase.auth.get_user(token)
    except Exception:
        return jsonify({'error': 'Invalid token'}),401

    id = user.user.id
    email = user.user.email
    phone_number = user.user.phone

    if UserProfile.query.get(id):
        return jsonify({'error': 'Profile already exists'}), 400

    try:
        new_user = UserProfile(id = id)
        new_user.save()

        new_user_info = UserInfo(user_profile_id = id ,
                                email = email if email else None, 
                                phone_number = phone_number if phone_number else None)
        new_user_info.save()

        new_user_settings = UserSettings(user_profile_id = id)
        new_user_settings.save()

        new_user_role = UserRole(user_profile_id = id)
        new_user_role.save()

        return jsonify({'message':'Account created successfully'}), 201
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Profile could not be created'}), 500
    
    

@auth_bp.route('/complete-profile', methods = ['PATCH'])
@auth_required
def complete_profile():

    is_profile = request.current_user.user.id
    data = request.get_json()
    username = data.get('username')

    if not is_profile:
        return jsonify({'error': 'Profile does not exist'}), 404
    
    if not username:
        return jsonify({'error': 'Please enter an Username'}), 400
    
    if UserProfile.query.filter_by(username = username).first():
        return jsonify({'error':'Username is already taken'}), 409

    try:
        user_profile_finish = UserProfile.query.get(is_profile)

        user_profile_finish.username = username
        db.session.commit()
        return jsonify({'message': 'Username successfully added'}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Failed to complete profile'}), 500
    

    
@auth_bp.route('/me', methods=['GET'])
@auth_required
def me():
    user_id = request.current_user.user.id
    profile = UserProfile.query.get(user_id)
    
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    return jsonify({
        'id': profile.id,
        'username': profile.username,
        'profile_complete': profile.username is not None
    }), 200
        