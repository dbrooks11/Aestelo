
import random
from datetime import datetime, timezone

from app.extensions import db
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
from models import (
    AuthUser,
    Collection,
    TokenBlackList,
    UserInfo,
    UserProfile,
    UserRole,
    UserSettings,
    UserSubscription,
)
from schemas import ValidationError
from schemas.auth_schema import AuthUserSchema
from sqlalchemy import exists, select
from utils.database import safe_transaction
from utils.loggin_config import get_logger
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
logger = get_logger(__name__)

dummy_hash = generate_password_hash('secure_timing_attack_prevention_string')


@auth_bp.route('/signup', methods = ['POST'])
def signup():

    data = request.get_json()

    if(data.get("name")):
        return jsonify({'error': 'Invalid(b)'}), 401

    email = data.get('email', None)
    password = data.get('password', None)
    confirm_password = data.get('confirm_password', None)

    if not all([email, password, confirm_password]):
        return jsonify({'error': 'Email, Password, and Confirmed Password are required'}), 401

    logger.info("Signup attempt", email=email)

    if db.session.execute(select(AuthUser).where(AuthUser.email == email)).first():
        return jsonify({'error': 'Account already exist'}), 409
    
    try:
        AuthUserSchema().validate(data, partial=True)
    except ValidationError as error:
        return jsonify({'error': error}), 400

    try:
        with safe_transaction():
            username = ''
            attempts = 0
            while attempts < 3:
                username = f'user{random.randint(1, 999999999999999999999999)}'
                
                username_exists = db.session.execute((select(exists().where(AuthUser.username == username)))).first()
                
                if not username_exists:
                    break
        
                attempts += 1
            
            if not username:
                return jsonify({'error': 'Server busy, please try again'}), 500
            
            auth_user = AuthUser(email=email, username=username, password_encrypted=generate_password_hash(password))
            profile = UserProfile(username=username)

            auth_user.user_profile = profile 
            profile.user_info = UserInfo(email=email)
            profile.user_settings = UserSettings()
            profile.user_role = UserRole()
            profile.user_subscription = UserSubscription()
            
            profile.collection.append(
                Collection(name='Default', is_default=True)
            )

            db.session.add(auth_user)

        logger.info("Signup successful", 
                   email=email,
                   username=username)
        return jsonify({'message':'Account created successfully'}), 201
    except Exception as e:
        logger.error("Signup failed", 
                    email=email,
                    username=username,
                    error=str(e),
                    exc_info=True)
        return jsonify({'error': 'Account could not be created'}), 500
    

@auth_bp.route('/login', methods = ['POST'])
def login():

    data = request.get_json()

    if(data.get("name")):
        return jsonify({'error': 'Invalid input'}), 401
    
    login_method = data.get("email") or data.get("username")
    if not login_method:
        return jsonify({'error': 'Email or username required'}), 401
    
    try:
        AuthUserSchema().validate(data, partial=True)
    except ValidationError as error:
        return jsonify({'error': error}), 400
    
    try:
        
        authenticate_user = db.session.scalars(select(AuthUser).where(
                (AuthUser.email == login_method) |
                (AuthUser.username == login_method)
            )).first()

        if authenticate_user:
            user_hash = authenticate_user.password_encrypted
        else:
            user_hash = dummy_hash

        password = data.get("password", None)
        password_check = check_password_hash(user_hash, password)

        if not all([authenticate_user, password_check]):
            return jsonify({'error': 'Invalid email or password'}),401
        
        with safe_transaction():
            authenticate_user.last_sign_in_at = datetime.now(timezone.utc)

        access_token = create_access_token(identity=authenticate_user.id)
        refresh_token = create_refresh_token(identity=authenticate_user.id)

        response =  jsonify({
            'message': 'Login successful',
        })

        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        current_app.logger.info('Login-email endpoint successful')
        return response, 200
    except Exception as e:
        logger.error(
            login_method=login_method,
            error=str(e),
            exc_info=True
        )
        return jsonify({'error': 'Failed to login'}), 500


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
        logger.info("Logout successful")
        return response, 200
    except Exception:
        logger.error("Logout failed")
        return jsonify({'error': 'Failed to logout'}), 500


@auth_bp.route('/refresh', methods = ['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)

        response = jsonify({'refresh': True})
        set_access_cookies(response, access_token)
        return response, 200
    except Exception as e:
        logger.error("Refresh failed",
                     user_id=current_user,
                     error=str(e))
        return jsonify({"Refresh failed"}), 500