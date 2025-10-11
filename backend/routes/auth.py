from flask import Blueprint, request, jsonify
from app import db
from models.user import UserProfile, UserInfo, UserSettings, UserRole
from exstensions import supabase
from routes.auth_required_wrapper import auth_required
from schemas.user_schema import user_profile_schema, ValidationError

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
    phone_number = user.user.phone

    if UserProfile.query.get(id):
        return jsonify({'error': 'Profile already exists'}), 400

    try:
        new_user = UserProfile(id = id)
        db.session.add(new_user)

        new_user_info = UserInfo(user_profile_id = id ,
                                email = email if email else None, 
                                phone_number = phone_number if phone_number else None)
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
    
    

@auth_bp.route('/complete-profile', methods = ['PATCH'])
@auth_required
def complete_profile():

    user_id = request.current_user.user.id
    user_profile_finish = UserProfile.query.get(user_id)

    if not user_id:
        return jsonify({'error': 'Profile does not exist'}), 404
    
    try:
        validate = user_profile_schema.load(request.get_json(), partial = True)
    except ValidationError as error:
        return jsonify({"error": error.messages}), 400

    try:
        for field, value in validate.items():
            setattr(user_profile_finish, field, value)
        
        db.session.commit()
        return user_profile_schema.dump(user_profile_finish), 200
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
        