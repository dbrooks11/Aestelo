from flask import request, jsonify
from exstensions import supabase
from functools import wraps
from models.user import UserRole


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        try:
            user = supabase.auth.get_user(token)
            request.current_user = user
            return func(*args, **kwargs)
        except Exception:
            return jsonify({'error': 'Unauthorized'}), 401
            
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = request.current_user.user.id
        user_role = UserRole.query.get(current_user)
        try:
            if not user_role:
                return jsonify({'error': 'Access denied'}), 403
        
            if user_role.is_admin or user_role.is_moderator or user_role.is_owner:
                return func(*args, **kwargs)
            else:
                return jsonify({'error':'Access denied'}), 403
        except Exception:
            return jsonify({'error':'Unauthorized. Access denied'}), 403
    return wrapper