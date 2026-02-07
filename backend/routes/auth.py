
import random
from datetime import datetime, timezone

from extensions import db
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from models import AuthUser, TokenBlackList, UserProfile
from schemas import ValidationError
from schemas.auth_schema import (
    email_pass_confirm_pass,
    email_pass_only,
    username_pass_only,
)
from sqlalchemy import exists
from sqlalchemy.orm import load_only
from util import DatabaseService
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

dummy_hash = generate_password_hash('secure_timing_attack_prevention_string')


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
        email_pass_confirm_pass.load(data)
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

        DatabaseService.create_user_with_stack(
            db.session, 
            email=email, 
            username=username,
            password_encrypted=generate_password_hash(password)
        )

        current_app.logger.info('Successful Signup')
        return jsonify({'message':'Account created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Signup endpoint ERROR: {e}')
        return jsonify({'error': 'Account could not be created'}), 400
    

# TODO: Merge username route and email route into one
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
        user_hash = dummy_hash

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
        user_hash = dummy_hash

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
        db.session.rollback()
        return jsonify({'error': 'Failed to logout'}), 500


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
    current_user = get_jwt_identity()

    try:
        user = UserProfile.query.options(load_only(UserProfile.username,
                                                    UserProfile.profile_photo
                                                )).get(current_user)

        if not user:
            return jsonify({'error': 'Failed to authenticate'}), 401
        
        return jsonify({
            'user': {
                'id': current_user,
                'username': user.username,
                'profile_photo_url': user.profile_photo_url
            }
        }), 200
    except Exception:
        return jsonify({'error': 'Failed to authenticate'}), 500