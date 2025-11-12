from ..exstensions import db
from ..models.user import UserProfile
from sqlalchemy import exists
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models.block_profile import BlockProfile
from ..models.followers_and_following import Follow
from ..schemas.user_schema import partial_schema
from ..util.decorators import profile_active_not_permitted, profile_check_current__banned_removed

block_bp = Blueprint('block', __name__, url_prefix='/block')

#done latency route test
@block_bp.route('/<string:id>/block-profile', methods = ['POST'])
@jwt_required()
@profile_active_not_permitted
def block_profile(id, user_profile, current_user):

    is_blocked = db.session.query(exists().where((BlockProfile.blocker_id == current_user) & (BlockProfile.blocked_id == user_profile.id))).scalar()
    if is_blocked:
        return jsonify({'error': 'Profile already blocked'}), 409 
    
    try:
        new_blocked = BlockProfile(
            blocker_id = current_user,
            blocked_id = user_profile.id)
        
        
        is_following_user = Follow.query.filter_by(follower_id = current_user,
                                              following_id = user_profile.id).first()
        is_user_follow_them = Follow.query.filter_by(follower_id = user_profile.id,
                                                     following_id = current_user).first()

        current_user = UserProfile.query.get(current_user)
        if is_following_user:
            db.session.delete(is_following_user)
            current_user.following_count -= 1
            user_profile.follower_count -= 1
        
        if is_user_follow_them:
            db.session.delete(is_user_follow_them)
            current_user.follower_count -= 1
            user_profile.following_count -= 1
            
        db.session.add(new_blocked)
        db.session.commit()
        return jsonify({'message':'Profile blocked successfully',
                        'profile_blocked': partial_schema.dump(user_profile)}), 201
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Failed to block profile'}), 409 

#done latency route test       
@block_bp.route('/<string:id>/unblock-profile', methods = ['DELETE'])
@jwt_required()
@profile_active_not_permitted
def unblock_profile(id, user_profile, current_user):
    is_blocked = BlockProfile.query.filter_by(blocker_id = current_user,
                                              blocked_id = user_profile.id).first()
    if is_blocked is None:
        return jsonify({'error': 'Profile already unblocked'}), 409 
    
    try:
        db.session.delete(is_blocked)
        db.session.commit()
        return jsonify({'message':'Profile unblocked successfully'}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error':'Failed to unblock profile'}), 500
    
#done latency route test
@block_bp.route('/me/show-blocked-profiles', methods = ['GET'])
@jwt_required()
@profile_check_current__banned_removed
def get_blocked_profiles(user_profile):
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=50, type=int)
        if per_page > 50:
            per_page = 50

        block_query = db.session.query(UserProfile).join(BlockProfile, BlockProfile.blocked_id == UserProfile.id).filter(BlockProfile.blocker_id == user_profile.id)

        paginated_blocks = block_query.paginate(
            page = page,
            per_page = per_page
        )

        block_list = partial_schema.dump(paginated_blocks.items, many=True)

        return jsonify({
            'blocked_profiles':block_list,
            'total':paginated_blocks.total,
            'total_pages':paginated_blocks.pages,
            'current_page':paginated_blocks.page
        }), 200
    
    except Exception:
        return jsonify({'error':'Failed to fetch block list'})
    