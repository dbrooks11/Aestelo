
from app import db
from exstensions import supabase
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.user_schema import username_only,ValidationError
from models.user import UserProfile, UserInfo, UserSettings, UserRole


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods = ['POST'])
def signup():

    token  = request.headers.get('Authorization', '').replace('Bearer ', '')

    try:
        user = supabase.auth.get_user(token)
    except Exception:
        return jsonify({'error': 'Invalid token'}),401

    id = user.user.id
    email = user.user.email

    if UserProfile.query.get(id):
        return jsonify({'error': 'Profile already exists'}), 400

    try:
        new_user = UserProfile(id = id)
        db.session.add(new_user)

        new_user_info = UserInfo(user_profile_id = id ,
                                email = email if email else None)
        db.session.add(new_user_info)

        new_user_settings = UserSettings(user_profile_id = id)
        db.session.add(new_user_settings)

        new_user_role = UserRole(user_profile_id = id)
        db.session.add(new_user_role)

        db.session.commit()
        return jsonify({'message':'Account created successfully'}), 201
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Profile could not be created'}), 500
    
    

@auth_bp.route('/complete-profile', methods=['PATCH'])
@jwt_required()
def complete_profile():
    current_user = get_jwt_identity()
    data = request.get_json()
    
    new_username = data.get('username')
    if not new_username:
        return jsonify({'error': 'No username provided'}), 400

    try:
        username_only.load(data, partial =True)
    except ValidationError as error:
        return jsonify({"error": error.messages}), 400
    try:
        username_update = UserProfile.query.filter_by(id=current_user).update({'username': new_username})
        if not username_update:
            return jsonify({'error': 'Profile does not exist'}), 404

    
        db.session.commit()
        return jsonify({'id': current_user, 'username': new_username}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Failed to complete profile'}), 500
