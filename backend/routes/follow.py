from flask import Blueprint, request, jsonify
from app import db
from models.user import UserProfile
from models.followers_and_following import Follow
from schemas.profile_schema import ProfileSchema
from auth_required_wrapper import auth_required

follow_bp = Blueprint('follow', __name__, url_prefix='/follow')


@follow_bp.route('/<string:username>/follow-user', methods = ['POST'])
@auth_required
def follow_user(username):
    current_user = request.current_user.user.id
    user_profile = UserProfile.query.filter_by(username = username).first()

    if not user_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    if user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    if user_profile.is_private:
        return jsonify({'error':'Profile is private'}),404

    try:
        will_follow = Follow(follower_id = current_user,
                             following_id = user_profile.id)
