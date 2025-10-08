from flask import Blueprint, request, jsonify
from app import db
from models.user import UserProfile
from models.followers_and_following import Follow
from routes.auth_required_wrapper import auth_required

follow_bp = Blueprint('follow', __name__, url_prefix='/profile/follow')


#FOLLOW A USER
@follow_bp.route('/<string:username>/follow-profile', methods = ['POST'])
@auth_required
def follow_profile(username):
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
        return jsonify({'message': 'Profile successfully followed',
                        'profile_followed': {
                            'username': user_profile.username,
                            'follower_count': user_profile.follower_count
                        },
                        'current_user_following': current_user_profile.following_count
                        }), 201
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Failed to follow profile'}), 500


#UNFOLLOW A USER
@follow_bp.route('/<string:username>/unfollow-profile', methods = ['DELETE'])
@auth_required
def unfollow_profile(username):
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
        return jsonify({'message': 'Profile successfully unfollowed',
                        'profile_unfollowed': {
                            'username': user_profile.username,
                            'follower_count': user_profile.follower_count
                        },
                        'current_user_following': current_user_profile.following_count
                        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Could not unfollow profile'}), 500


#GET ALL FOLLOWERS OF A USER (PAGINATED)
@follow_bp.route('/<string:username>/followers', methods = ['GET'])
@auth_required
def get_followers(username):
    current_user = request.current_user.user.id
    user_profile = UserProfile.query.filter_by(username = username).first()

    if not user_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    if user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    if (current_user != user_profile.id) and (user_profile.is_private):
        is_following = Follow.query.filter_by(follower_id = current_user,
                                        following_id = user_profile.id).first()
        if not is_following:
            return jsonify({'error': 'Profile is private'}), 403
    
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=50, type=int)

        follower_query = db.session.query(UserProfile).join(Follow, Follow.follower_id ==UserProfile.id).filter(Follow.following_id == user_profile.id)

        paginated_followers = follower_query.paginate(
            page = page,
            per_page = per_page
        )

        followers_list = [{
            'id': str(follower.follower_id),
            'banner_theme':follower.banner_theme,
            'username': follower.username,
            'profile_image': follower.profile_image
        }
        for follower in paginated_followers.items]

        return jsonify({
            "followers": followers_list,
            "total": paginated_followers.total,
            "total_pages": paginated_followers.pages,
            "current_page": paginated_followers.page
        }), 200
    
    except Exception:
        return jsonify({'error': 'Failed to fetch followers'}), 500
    

#GET LIST OF PEOPLE THE USER IS FOLLOWING(PAGINATED)
@follow_bp.route('/<string:username>/following', methods = ['GET'])
@auth_required
def get_following(username):
    current_user = request.current_user.user.id
    user_profile = UserProfile.query.filter_by(username = username).first()

    if not user_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    if user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    if (current_user != user_profile.id) and (user_profile.is_private):
        is_following = Follow.query.filter_by(follower_id = current_user,
                                        following_id = user_profile.id).first()
        if not is_following:
            return jsonify({'error': 'Profile is private'}), 403
        
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=50, type=int)

        following_query = db.session.query(UserProfile).join(Follow, Follow.following_id == UserProfile.id).filter(Follow.follower_id == user_profile.id)

        paginated_following = following_query.paginate(
            page =page,
            per_page = per_page
        )

        following_list = [{
            'id': str(following.id),
            'banner_theme': following.banner_theme,
            'username': following.username,
            'profile_image': following.profile_image
        }
        for following in paginated_following.items]

        return jsonify({
            'following_list':following_list,
            'total': paginated_following.total,
            'total_pages': paginated_following.pages,
            'current_page':paginated_following.page
        }), 200
    
    except Exception:
        return jsonify({'error': 'Failed to fetch following list'}), 500