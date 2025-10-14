from functools import wraps
from flask import jsonify, request
from models.user import UserProfile
from models.post import Post
from models.visit import Visit
from models.followers_and_following import Follow
from models.block_profile import BlockProfile
from sqlalchemy import exists
from exstensions import db

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
        
        kwargs['user_profile'] = user_profile
        return func(*args, **kwargs)
    return decorator


def profile_both_check_banned_removed(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        current_user = request.current_user.user.id
        profile_id = kwargs.get('id')
        user_profile = UserProfile.query.get(profile_id)
        current_user_profile = UserProfile.query.get(current_user)

        if user_profile is None or current_user_profile is None:
            return jsonify({'error': 'Profile not found'}), 404
        
        if user_profile.is_deleted or current_user_profile.is_deleted:
            return jsonify({'error': 'Profile does not exist'}), 404
        
        if user_profile.is_banned or current_user_profile.is_banned:
            return jsonify({'error':'Profile unavailable'}),404
        
        kwargs['user_profile'] = user_profile
        kwargs['current_user_profile'] = current_user_profile
        return func(*args, **kwargs)
    
    return decorator


def block_and_follow_check(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        user_profile = kwargs.get('user_profile')
        current_user_profile = kwargs.get('current_user_profile')

        is_blocked = db.session.query(exists().where((BlockProfile.blocker_id ==user_profile.id) & (BlockProfile.blocked_id == current_user_profile.id))).scalar()

        is_current_user_blocking = db.session.query(exists().where((BlockProfile.blocker_id == current_user_profile.id) & (BlockProfile.blocked_id == user_profile.id))).scalar()
        
        if is_blocked or is_current_user_blocking:
            return jsonify({'error': 'Profile unavailable'}), 404
        
        if (current_user_profile.id != user_profile.id) and (user_profile.is_private):
            is_following = db.session.query(exists().where((Follow.follower_id == current_user_profile.id) & (Follow.following_id == user_profile.id))).scalar()
            if not is_following:
                return jsonify({'error': 'Profile is private'}), 403
    
    return decorator


def profile_current_check_post(func):
    @wraps
    def decorator(*args, **kwargs):
        current_user = request.current_user.user.id
        current_user_profile = UserProfile.query.get(current_user)
        post_id = kwargs.get('post_id')
        post = Post.query.get(post_id)
        
        if current_user_profile is None:
            return jsonify({'error': 'Profile not found'}), 404
        
        if current_user_profile.is_deleted:
            return jsonify({'error': 'Profile does not exist'}), 404
        
        if current_user_profile.is_banned:
            return jsonify({'error':'Profile unavailable'}),404
        
        if post.user_profile_id != current_user:
            return jsonify({'error': 'Action not permitted'}), 403
        
        if post is None or post.is_deleted or post.is_removed:
            return jsonify({'error': 'Post not found'}), 404

        kwargs['current_user_profile'] = current_user_profile
        kwargs['post'] = post
        return func(*args, **kwargs)
    return decorator
    
    
def profile_current_check_visit(func):
    @wraps
    def decorator(*args, **kwargs):
        current_user = request.current_user.user.id
        current_user_profile = UserProfile.query.get(current_user)
        visit_id = kwargs.get('visit_id')
        visit = Visit.query.get(visit_id)

        if current_user_profile is None:
            return jsonify({'error': 'Profile not found'}), 404
        
        if current_user_profile.is_deleted:
            return jsonify({'error': 'Profile does not exist'}), 404
        
        if current_user_profile.is_banned:
            return jsonify({'error':'Profile unavailable'}),404
        
        if visit.user_profile_id != current_user:
            return jsonify({'error': 'Action not permitted'}), 403
        
        if visit is None or visit.is_deleted or visit.is_removed:
            return jsonify({'error': 'Visit not found'}), 404
        
        kwargs['current_user_profile'] = current_user_profile
        kwargs['visit'] = visit
        return func(*args, **kwargs)
    return decorator