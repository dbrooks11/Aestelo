from functools import wraps
from flask import jsonify, request
from models.user import UserProfile
from models.post import Post
from models.visit import Visit

def profile_active_not_permitted(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        current_user = request.current_user.user.id
        profile_id = kwargs.get('id')
        user_profile = UserProfile.query.get(profile_id)

        if user_profile is None:
            return jsonify({'error': 'Profile not found'}), 404
        
        if user_profile.is_deleted:
            return jsonify({'error': 'Profile does not exist'}), 404
        
        if user_profile.is_banned:
            return jsonify({'error':'Profile unavailable'}),404
        
        if current_user == user_profile.id:
            return jsonify({'error': 'Action not permitted'}), 409
        
        kwargs['user_profile'] = user_profile
        kwargs['current_user'] = current_user
        return func(*args, **kwargs)
    return decorator


def profile_check_current__banned_removed(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        current_user = request.current_user.user.id
        profile_id = kwargs.get('id', None)
        user_profile = UserProfile.query.get(profile_id if profile_id else current_user)

        if user_profile is None:
            return jsonify({'error': 'Profile not found'}), 404
        
        if user_profile.is_deleted:
            return jsonify({'error': 'Profile does not exist'}), 404
        
        if user_profile.is_banned:
            return jsonify({'error':'Profile unavailable'}),404
        
        kwargs['user_profile']
        return func(*args, **kwargs)
    return decorator


    