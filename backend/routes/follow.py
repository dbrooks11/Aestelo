from flask import Blueprint, request, jsonify
from app import db
from models.user import UserProfile
from models.followers_and_following import Follow
from routes.auth_required_wrapper import auth_required

follow_bp = Blueprint('follow', __name__, url_prefix='/profile/follow')


@follow_bp.route('/<string:username>/follow-user', methods = ['POST'])
@auth_required
def follow_user(username):
    current_user = request.current_user.user.id
    user_profile = UserProfile.query.filter_by(username = username).first()

    if not user_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    if user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    if user_profile.id == current_user:
        return jsonify({'error': 'Cannot follow yourself'}), 400
    
    is_following = Follow.query.filter_by(follower_id = current_user,
                                          following_id = user_profile.id).first()
    if is_following:
        return jsonify({'error': 'Profile already followed'}), 409

    try:
        new_follow = Follow(follower_id = current_user,
                             following_id = user_profile.id)
        user_profile.follower_count += 1
        current_user_profile = UserProfile.query.get(current_user)
        current_user_profile.following_count += 1
        db.session.add(new_follow)
        db.session.commit()
        return jsonify({'message': 'Profile successfully followed'}), 201
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Failed to follow profile'}), 500


@follow_bp.route('/<string:username>/unfollow-user', methods = ['DELETE'])
@auth_required
def unfollow_user(username):
    current_user = request.current_user.user.id
    user_profile = UserProfile.query.filter_by(username = username).first()

    if not user_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    if user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    if user_profile.id == current_user:
        return jsonify({'error': 'Cannot unfollow yourself'}), 400
    
    is_following = Follow.query.filter_by(follower_id = current_user,
                                        following_id = user_profile.id).first()
    
    if not is_following:
        return jsonify({'error':'You are not following this profile'}), 404
    
    try:
        current_user_profile = UserProfile.query.get(current_user)
        db.session.delete(is_following)
        current_user_profile.following_count -= 1
        user_profile.follower_count -= 1
        db.session.commit()
        return jsonify({'message':'Profile unfollowed successfully'}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Could not unfollow profile'}), 500

            
    