
from exstensions import db
import uuid
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, current_app
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
from sqlalchemy import exists
from werkzeug.security import check_password_hash, generate_password_hash
from schemas.user_schema import ValidationError
from schemas.auth_schema import username_pass_only,email_pass_only,email_pass_confirm_pass
from models.user import UserProfile, UserInfo, UserSettings, UserRole, UserSubscription
from models.token_blacklist import TokenBlackList
from models.auth import AuthUser

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/signup', methods = ['POST'])
def signup():

    data = request.get_json()

    if(data.get("name")):
        return jsonify({'error': 'Invalid(b)'}), 401

    email = data.get('email', None)
    password = data.get('password', None)
    confirm_password = data.get('confirm_password', None)

    if email is None or password is None or confirm_password is None:
        return jsonify({'error': 'Email, Password, and Confirmed Password are required'}), 401

    if AuthUser.query.filter_by(email = email).first():
        return jsonify({'error': 'Account already exist'}), 409
    
    try:
        validate_auth = email_pass_confirm_pass.load(data)
    except ValidationError as error:
        error_messages = []
        for field, messages in error.messages.items():
            if isinstance(messages, list):
                error_messages.extend(messages)
            else:
                error_messages.append(str(messages))
        current_app.logger.error('Signup endpoint failed due to validation error of info')
        return jsonify({"error": ". ".join(error_messages)}), 401

    try:
        username = ''
        attempts = 0
        while attempts < 3:
            username = f'user{random.randint(1, 999999999999999999999999)}'
            
            username_exists = db.session.query(exists().where((AuthUser.username == username))).scalar()
            
            if not username_exists:
                break
    
            attempts += 1
        
        if not username:
            return jsonify({'error': 'Server busy, please try again'}), 500

        user_id = uuid.uuid4()

        new_user = AuthUser(
            id = user_id,
            username = username,
            email = validate_auth['email'],
            password_encrypted = generate_password_hash(validate_auth['password'])
        )

        new_user_profile = UserProfile(
            id=user_id,
            username=username,
            user_info=UserInfo(email=validate_auth['email']),
            user_settings=UserSettings(),
            user_role=UserRole(),
            user_subscription=UserSubscription()
        )

        db.session.add(new_user)
        db.session.add(new_user_profile)
        db.session.commit()

        current_app.logger.info('Successful Signup')
        return jsonify({'message':'Account created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Signup endpoint ERROR: {e}')
        return jsonify({'error': 'Account could not be created'}), 400
    


@auth_bp.route('/login-email', methods = ['POST'])
def login_email():

    data = request.get_json()

    if(data.get("name")):
        return jsonify({'error': 'Invalid input'}), 401
    
    try:
        validate_login = email_pass_only.load(data, partial = True)
    except ValidationError as error:
        error_messages = []
        for field, messages in error.messages.items():
            if isinstance(messages, list):
                error_messages.extend(messages)
            else:
                error_messages.append(str(messages))
        current_app.logger.error('Login-email endpoint failed due to validation error of info')
        return jsonify({"error": ". ".join(error_messages)}), 401

    authenticate_user = AuthUser.query.filter_by(email = validate_login['email']).first()

    if authenticate_user:
        user_hash = authenticate_user.password_encrypted
    else:
        #dummy password hash
        user_hash = 'scrypt:32768:8:1$6k9S8X1d$d067215201772658f8b461876f827918e974e628464a4d6f6580f585d564850c18d1796120e2e5055b41d214a1a511855e90538053513a967732d84784136939'

    password_check = check_password_hash(user_hash, validate_login['password'])

    if authenticate_user is None or password_check is False:
        return jsonify({'error': 'Invalid email or password'}),401
    
    authenticate_user.last_sign_in_at = datetime.now(timezone.utc)
    db.session.commit()

    access_token = create_access_token(identity=authenticate_user.id)
    refresh_token = create_refresh_token(identity=authenticate_user.id)

    response =  jsonify({
        'message': 'Login successful',
    })

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    current_app.logger.info('Login-email endpoint successful')
    return response, 200


@auth_bp.route('/login-username', methods = ['POST'])
def login_username():

    data = request.get_json()

    if(data.get("name")):
        return jsonify({'error', 'Invalid input'}), 401
    
    try:
        validate_login = username_pass_only.load(data)
    except ValidationError as error:
        error_messages = []
        for field, messages in error.messages.items():
            if isinstance(messages, list):
                error_messages.extend(messages)
            else:
                error_messages.append(str(messages))
        current_app.logger.error('Login-username endpoint failed due to validation error of info')
        return jsonify({"error": ". ".join(error_messages)}), 401

    authenticate_user = AuthUser.query.filter_by(username = validate_login['username']).first()

    if authenticate_user:
        user_hash = authenticate_user.password_encrypted
    else:
        #dummy password hash
        user_hash = 'scrypt:32768:8:1$6k9S8X1d$d067215201772658f8b461876f827918e974e628464a4d6f6580f585d564850c18d1796120e2e5055b41d214a1a511855e90538053513a967732d84784136939'

    password_check = check_password_hash(user_hash, validate_login['password'])

    if authenticate_user is None or password_check is False:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    authenticate_user.last_sign_in_at = datetime.now(timezone.utc)
    db.session.commit()

    access_token = create_access_token(identity=authenticate_user.id)
    refresh_token = create_refresh_token(identity=authenticate_user.id)

    response =  jsonify({
        'message': 'Login successful',
    })

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    current_app.logger.info('Login-username endpoint successful')
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
        current_app.logger.info('Logout endpoint successful')
        return response, 200
    except Exception:
        current_app.logger.error('Logout endpoint failed')
        return jsonify({'error': 'Failed to logout'}), 400


@auth_bp.route('/refresh', methods = ['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    response = jsonify({'refresh': True})
    set_access_cookies(response, access_token)
    return response, 200


@auth_bp.route('/authenticate', methods = ['GET'])
@jwt_required()
def verify():
    current_user_id = get_jwt_identity()

    user = db.session.query(UserProfile.username, UserProfile.profile_photo).filter_by(id = current_user_id).first()

    if not user:
        return jsonify({'error': 'User not found'}), 401

    return jsonify({
        'user': {
            'id': current_user_id,
            'username': user.username,
            'profile_photo': user.profile_photo
        }
    }), 200