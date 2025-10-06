from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.user import UserProfile
from models.block_profile import BlockProfile
from models.post import Post
from models.followers_and_following import Follow
from routes.auth_required_wrapper import auth_required


post_bp = Blueprint('post', __name__, url_prefix='/post')


@post_bp.route('/<string:username>/profile-posts', methods = ['GET'])
@auth_required
def get_profile_post_all(username):
    current_user = request.current_user.user.id
    user_profile = UserProfile.query.filter_by(username = username).first()

    if not user_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    if user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    is_blocked = BlockProfile.query.filter_by(blocker_id = user_profile.id,
                                              blocked_id = current_user).first()
    is_current_user_blocking = BlockProfile.query.filter_by(blocker_id = current_user,
                                                            blocked_id = user_profile.id).first()

    if is_blocked or is_current_user_blocking:
        return jsonify({'error': 'Profile unavailable'}), 404
    
    if (current_user != user_profile.id) and (user_profile.is_private):
        is_following = Follow.query.filter_by(follower_id = current_user,
                                        following_id = user_profile.id).first()
        if not is_following:
            return jsonify({'error': 'Profile is private'}), 403
    
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)

        post_query = Post.query.filter_by(user_profile_id = user_profile.id)

        paginated_post = post_query.paginate(
            page = page,
            per_page=per_page
        )

        post_list = [{
            'all_post': post.to_dict()
        }
        for post in paginated_post.items]

        return jsonify({
            'posts': post_list,
            'total': paginated_post.total,
            'total_pages': paginated_post.pages,
            'current_page': paginated_post.page
        }), 200
    
    except Exception:
        return jsonify({'error': 'Failed to fetch post'}), 500


@post_bp.route('/<string:username>/profile-post/<bigint:post_id>', methods = ['GET'])
@auth_required
def get_profile_post(username, post_id):
    current_user = request.current_user.user.id
    user_profile = UserProfile.query.filter_by(username = username).first()
    
    if not user_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    if user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    is_blocked = BlockProfile.query.filter_by(blocker_id = user_profile.id,
                                              blocked_id = current_user).first()
    is_current_user_blocking = BlockProfile.query.filter_by(blocker_id = current_user,
                                                            blocked_id = user_profile.id).first()

    if is_blocked or is_current_user_blocking:
        return jsonify({'error': 'Profile unavailable'}), 404
    
    if (current_user != user_profile.id) and (user_profile.is_private):
        is_following = Follow.query.filter_by(follower_id = current_user,
                                        following_id = user_profile.id).first()
        if not is_following:
            return jsonify({'error': 'Profile is private'}), 403

    try:
        post = Post.query.get(post_id)
        return jsonify({'post': post.to_dict()}), 200

    except Exception:
        return jsonify({'error':'Failed to fetch post'}), 500
    

@post_bp.route('/<string:username>/profile-post/<bigint:post_id>/edit', methods = ['PATCH'])
@auth_required
def edit_post(username, post_id):
    
    

   
    

