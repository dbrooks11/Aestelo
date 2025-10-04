from flask import request, jsonify
from exstensions import supabase


def auth_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        try:
            user = supabase.auth.get_user(token)
            request.current_user = user
            func(*args, **kwargs)
        except Exception:
            return jsonify({'error': 'Unauthorized'}), 401
            
    return wrapper
