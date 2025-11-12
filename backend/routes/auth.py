
from app import db
from exstensions import supabase
from flask import Blueprint, request, jsonify
from flask_jwt_extended import(
    create_access_token, 
    create_refresh_token,
    jwt_required, 
    get_jwt, 
    get_jwt_identity
)
from werkzeug.security import check_password_hash, generate_password_hash
from schemas.user_schema import username_only,ValidationError
from schemas.auth_schema import username_pass_only,email_pass_only,email_pass_confirm_pass
from models.user import UserProfile, UserInfo, UserSettings, UserRole
from models.auth import AuthUser


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods = ['POST'])
def signup():

    data = request.get_json()

    email = data.get('email', None)
    if email: 
        email = email.strip()

    password = data.get('password', None)
    if password:
        password = password.strip()
        
    confirm_password = data.get('confirm_password', None)

    if email is None or password or confirm_password is None:
        return jsonify({'error': 'Email, Password, and Confirmed Password are required'}), 400

    if AuthUser.query.filter_by(email = email).first():
        return jsonify({'error': 'Account already exist'}), 404
    
    try:
        validate_auth = email_pass_confirm_pass.load(data)
    except ValidationError as err:
        return jsonify('error', err)

    try:
        new_user = AuthUser(
            email = validate_auth['email'],
            password_encrypted = generate_password_hash(validate_auth['password'])
        )
        db.session.add(new_user)

        new_user_info = UserInfo(email = validate_auth['email'])
        db.session.add(new_user_info)

        db.session.commit()
        return jsonify({'message':'Account created successfully'}), 201
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Profile could not be created'}), 500
    

@auth_bp.route('/login-email', methods = ['GET'])
def login_email():

    data = request.get_json()

    email = data.get('email', None)
    password = data.get('password', None)

    if email is None or password is None:
        return jsonify({'error': 'Email and Password are required'}), 404
    
    try:
        validate_login = email_pass_only.load(data)
    except ValidationError as err:
        return jsonify({'error': err})

    authenticate_user = AuthUser.query.filter_by(email = validate_login['email']).first()

    if authenticate_user is None:
        return jsonify({'error': 'Invalid email or password'}),404
    
    if check_password_hash(authenticate_user.password_encrypted, validate_login['password']) is False:
        return jsonify({'error':'Wrong Password'}), 400
    
    access_token = create_access_token(identity=authenticate_user.id)
    refresh_token = create_refresh_token(identity=authenticate_user.id)

    return jsonify({
        'message': 'Login successful',
        'tokens': {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    }), 200

@auth_bp.route('/login-username', methods = ['PATCH'])
def login_username():

    data = request.get_json()

    username = data.get('username', None)
    password = data.get('password', None)

    if username is None or password is None:
        return jsonify({'error': 'Username and Password are required'}), 400
    
    try:
        validate_login = username_pass_only.load(data)
    except ValidationError as err:
        return jsonify({'error': err})

    authenticated_user = AuthUser.query.filter_by(username = validate_login['username']).first()

    if authenticated_user is None:
        return jsonify({'error': 'Invalid Username or Password'}), 400
    
    if check_password_hash(authenticated_user.password_encrypted, validate_login['password']) is False:
        return ({'error': 'Incorrect Password'}), 400

    access_token = create_access_token(identity=authenticated_user.id)
    refresh_token = create_refresh_token(identity=authenticated_user.id)
    
    return jsonify({
        'message': 'Login successful',
        'tokens': {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    }), 200
    
    

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
