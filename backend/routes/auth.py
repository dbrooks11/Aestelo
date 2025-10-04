from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db
from models.user import UserProfile, UserSettings
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

    if UserProfile.query.get(id = id) or UserSettings.query.filter_by(email = email) or UserSettings.query.filter_by(phone_number = phone_number):
        return jsonify({'error': 'Account already exist'}), 400

    new_user = UserProfile(id = id)
    new_user = UserSettings(email = email, phone_number = phone_number)

    
