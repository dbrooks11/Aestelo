
from ..exstensions import db
import uuid
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from flask_jwt_extended import(
    create_access_token, 
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    jwt_required, 
    get_jwt, 
    get_jwt_identity
)
import random
from sqlalchemy import exists, select
from werkzeug.security import check_password_hash, generate_password_hash
from ..schemas.user_schema import ValidationError
from ..schemas.auth_schema import username_pass_only,email_pass_only,email_pass_confirm_pass
from ..models.user import UserProfile, UserInfo, UserSettings, UserRole, UserSubscription
from ..models.token_blacklist import TokenBlackList
from ..models.auth import AuthUser


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods = ['POST'])
def signup():

    data = request.get_json()

    email = data.get('email', '')
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', None)

    if email is None or password is None or confirm_password is None:
        return jsonify({'error': 'Email, Password, and Confirmed Password are required'}), 400

    if AuthUser.query.filter_by(email = email).first():
        return jsonify({'error': 'Account already exist'}), 409
    
    try:
        validate_auth = email_pass_confirm_pass.load(data)
    except ValidationError as error:
        # return jsonify('error', err.messages), 404
        error_messages = []
        for field, messages in error.messages.items():
            if isinstance(messages, list):
                error_messages.extend(messages)
            else:
                error_messages.append(str(messages))
        return jsonify({"error": ". ".join(error_messages)}), 400

    try:
        username = ''
        attempts = 0
        while attempts < 3:
            username = f'user{random.randint(1, 999999999999999999999999)}'
            
            username_exists = db.session.query(exists().where((AuthUser.username == username))).scalar()
            
            if not username_exists:
                break
    
            attempts += 1

        user_id = uuid.uuid4()

        new_user = AuthUser(
            id = user_id,
            username = username,
            email = validate_auth['email'],
            password_encrypted = generate_password_hash(validate_auth['password'])
        )
        db.session.add(new_user)

        new_user_profile = UserProfile(
            id = user_id,
            username = username
        )
        db.session.add(new_user_profile)
        db.session.flush()

        new_user_info = UserInfo(
            user_profile_id = user_id,
            email = validate_auth['email'])
        db.session.add(new_user_info)

        new_user_settings = UserSettings(
            user_profile_id = user_id
        )
        db.session.add(new_user_settings)

        new_user_role = UserRole(
            user_profile_id = user_id
        )
        db.session.add(new_user_role)

        new_user_sub = UserSubscription(
            user_profile_id = user_id
        )
        db.session.add(new_user_sub)

        db.session.commit()
        return jsonify({'message':'Account created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"ERROR: {e}") 
        print(f"Error type: {type(e)}")
        return jsonify({'error': 'Account could not be created'}), 400
    


@auth_bp.route('/login-email', methods = ['POST'])
def login_email():

    data = request.get_json()

    email = data.get('email', None)
    password = data.get('password', None)

    if email is None or password is None:
        return jsonify({'error': 'Email and Password are required'}), 404
    
    try:
        validate_login = email_pass_only.load(data, partial = True)
    except ValidationError as error:
        error_messages = []
        for field, messages in error.messages.items():
            if isinstance(messages, list):
                error_messages.extend(messages)
            else:
                error_messages.append(str(messages))
        return jsonify({"error": ". ".join(error_messages)}), 400

    authenticate_user = AuthUser.query.filter_by(email = validate_login['email']).first()

    if authenticate_user is None:
        return jsonify({'error': 'Invalid email or password'}),404
    
    if check_password_hash(authenticate_user.password_encrypted, validate_login['password']) is False:
        return jsonify({'error':'Wrong Password'}), 400
    
    authenticate_user.last_sign_in_at = datetime.now(timezone.utc)
    db.session.commit()

    access_token = create_access_token(identity=authenticate_user.id)
    refresh_token = create_refresh_token(identity=authenticate_user.id)

    response =  jsonify({
        'message': 'Login successful',
    })

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response, 200


@auth_bp.route('/login-username', methods = ['POST'])
def login_username():

    data = request.get_json()

    username = data.get('username', None)
    password = data.get('password', None)

    if username is None or password is None:
        return jsonify({'error': 'Username and Password are required'}), 400
    
    try:
        validate_login = username_pass_only.load(data)
    except ValidationError as error:
        error_messages = []
        for field, messages in error.messages.items():
            if isinstance(messages, list):
                error_messages.extend(messages)
            else:
                error_messages.append(str(messages))
        return jsonify({"error": ". ".join(error_messages)}), 400

    authenticate_user = AuthUser.query.filter_by(username = validate_login['username']).first()

    if authenticate_user is None:
        return jsonify({'error': 'Invalid Username or Password'}), 400
    
    if check_password_hash(authenticate_user.password_encrypted, validate_login['password']) is False:
        return ({'error': 'Incorrect Password'}), 400
    
    authenticate_user.last_sign_in_at = datetime.now(timezone.utc)
    db.session.commit()

    access_token = create_access_token(identity=authenticate_user.id)
    refresh_token = create_refresh_token(identity=authenticate_user.id)

    response =  jsonify({
        'message': 'Login successful',
    })

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response, 200
    

@auth_bp.route('/logout', methods = ['POST'])
@jwt_required()
def logout():
    try: 
        jwt = get_jwt()
        jti = jwt['jti']

        token_block = TokenBlackList(jti=jti)
        token_block.save()

        response = jsonify({'message': 'Logout successful'})
        unset_jwt_cookies(response)
        return response, 200
    except Exception:
        return jsonify({'error': 'Failed to logout'}), 400


@auth_bp.route('/refresh', methods = ['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    response = jsonify({'refresh': True})
    set_access_cookies(response, access_token)
    return response, 200


@auth_bp.route('/verify', methods = ['GET'])
@jwt_required()
def verify():
    return jsonify({'authenticated': True})