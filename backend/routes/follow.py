from extensions import db
from models.user import UserProfile
from sqlalchemy import exists
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Follow
from util.decorators import profile_both_check_banned_removed, block_and_follow_check
from schemas.user_schema import partial_schema

follow_bp = Blueprint('follow', __name__, url_prefix='/profile/follow')

#done latency route test
#FOLLOW A USER
@follow_bp.route('/<string:id>/follow-profile', methods = ['POST'])
@jwt_required()
@profile_both_check_banned_removed
@block_and_follow_check
def follow_profile(id, user_profile, current_user_profile):

    if user_profile.id == current_user_profile.id:
        return jsonify({'error': 'Cannot follow yourself'}), 409
    
    is_following = db.session.query(exists().where((Follow.follower_id == current_user_profile.id) & (Follow.following_id == user_profile.id))).scalar()
    
    if is_following:
        return jsonify({'error': 'Profile already followed'}), 409

    try:
        new_follow = Follow(follower_id = current_user_profile.id, following_id = user_profile.id)
        
        UserProfile.query.filter_by(id=current_user_profile.id).update({'following_count': UserProfile.following_count + 1}, synchronize_session=False)
        
        UserProfile.query.filter_by(id=user_profile.id).update({'follower_count': UserProfile.follower_count + 1}, synchronize_session=False)


        db.session.add(new_follow)
        db.session.commit()
        return jsonify({'message': 'Profile successfully followed',
                        'profile_followed': {
                            'id': user_profile.id,
                            'follower_count': user_profile.follower_count
                        },
                        'id': current_user_profile.id,
                        'current_user_following': current_user_profile.following_count
                        }), 201
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Failed to follow profile'}), 500

#done latency route test
#UNFOLLOW A USER
@follow_bp.route('/<string:id>/unfollow-profile', methods = ['DELETE'])
@jwt_required()
@profile_both_check_banned_removed
def unfollow_profile(id, user_profile, current_user_profile):

    if user_profile.id == current_user_profile.id:
        return jsonify({'error': 'Action not permitted'}), 409
    
    try:
        deleted = Follow.query.filter_by(follower_id = current_user_profile.id,
                                         following_id = user_profile.id).delete(synchronize_session=False)
        
        if deleted == 0:
            db.session.rollback() 
            return jsonify({'error': 'You are not following this profile'}), 409
        
        UserProfile.query.filter_by(id = current_user_profile.id).update({'following_count': UserProfile.following_count - 1}, synchronize_session=False)
        UserProfile.query.filter_by(id = user_profile.id).update({'follower_count': UserProfile.follower_count - 1}, synchronize_session=False)
        
        db.session.commit()
        return jsonify({'message': 'Profile successfully unfollowed',
                        'profile_unfollowed': {
                            'id': user_profile.id,
                            'follower_count': user_profile.follower_count
                        },
                        'id': current_user_profile.id,
                        'current_user_following': current_user_profile.following_count
                        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Could not unfollow profile'}), 500


#done latency test
#GET ALL FOLLOWERS OF A USER (PAGINATED)
@follow_bp.route('/<string:id>/followers', methods = ['GET'])
@jwt_required()
@profile_both_check_banned_removed
def get_followers(id, user_profile, current_user_profile):
    
    if (current_user_profile.id != user_profile.id) and (user_profile.is_private):
        is_following = db.session.query(exists().where((Follow.follower_id == current_user_profile.id) & (Follow.following_id == user_profile.id))).scalar()
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

        followers_list = partial_schema.dump(paginated_followers.items, many = True)

        return jsonify({
            "followers": followers_list,
            "total": paginated_followers.total,
            "total_pages": paginated_followers.pages,
            "current_page": paginated_followers.page
        }), 200
    
    except Exception:
        return jsonify({'error': 'Failed to fetch followers'}), 500
    

#GET LIST OF PEOPLE THE USER IS FOLLOWING(PAGINATED)
@follow_bp.route('/<string:id>/following', methods = ['GET'])
@jwt_required()
@profile_both_check_banned_removed
def get_following(id, user_profile, current_user_profile):
    
    if (current_user_profile.id != user_profile.id) and (user_profile.is_private):
        is_following = db.session.query(exists().where((Follow.follower_id == current_user_profile.id) & (Follow.following_id == user_profile.id))).scalar()
        
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

        following_list = partial_schema.dump(paginated_following.items, many = True)

        return jsonify({
            'following_list':following_list,
            'total': paginated_following.total,
            'total_pages': paginated_following.pages,
            'current_page':paginated_following.page
        }), 200
    
    except Exception:
        return jsonify({'error': 'Failed to fetch following list'}), 500