from functools import wraps
from flask_jwt_extended import get_jwt_identity
from models import UserRole
from flask import jsonify


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
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