from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db
from models.user import UserProfile, UserInfo, UserSettings, UserRole, UserSubscription
from exstensions import supabase, db

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
        
