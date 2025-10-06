from flask import request, jsonify
from exstensions import supabase
from functools import wraps


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
