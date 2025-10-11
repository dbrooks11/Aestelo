from flask import Blueprint, request, jsonify
from app import db
from models.user import UserProfile
from models.followers_and_following import Follow
from models.block_profile import BlockProfile
from routes.auth_required_wrapper import auth_required

block_bp = Blueprint('block', __name__, url_prefix='/block')


@block_bp.route('/<string:username>/block-profile', methods = ['POST'])
@auth_required
def block_profile(username):
    current_user = request.current_user.user.id
    user_profile = UserProfile.query.filter_by(username = username).first()

    if not user_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    if user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    if current_user == user_profile.id:
        return jsonify({'error': 'Cannot block yourself'}), 500
    
    is_blocked = BlockProfile.query.filter_by(blocker_id = current_user,
                                              blocked_id = user_profile.id).first()
    if is_blocked:
        return jsonify({'error': 'Profile already blocked'}), 409 
    
    try:
        new_blocked = BlockProfile(
            blocker_id = current_user,
            blocked_id = user_profile.id
        )
        
        is_following_user = Follow.query.filter_by(follower_id = current_user,
                                              following_id = user_profile.id).first()
        is_user_follow_them = Follow.query.filter_by(follower_id = user_profile.id,
                                                     following_id = current_user).first()
        
        current_user_profile = UserProfile.query.get(current_user)

        if is_following_user:
            db.session.delete(is_following_user)
            current_user_profile.following_count -= 1
            user_profile.follower_count -= 1
        
        if is_user_follow_them:
            db.session.delete(is_user_follow_them)
            current_user_profile.follower_count -= 1
            user_profile.following_count -= 1
            
        db.session.add(new_blocked)
        db.session.commit()
        return jsonify({'message':'Profile blocked successfully'}), 201
    except Exception:
        db.session.rollback()
        return jsonify({'error':'Failed to block profile'}), 500

       
@block_bp.route('/<string:username>/unblock-profile', methods = ['DELETE'])
@auth_required
def unblock_profile(username):
    current_user = request.current_user.user.id
    user_profile = UserProfile.query.filter_by(username = username).first()

    if not user_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    if user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    if current_user == user_profile.id:
        return jsonify({'error': 'Cannot unblock yourself'}), 500
    
    is_blocked = BlockProfile.query.filter_by(blocker_id = current_user,
                                              blocked_id = user_profile.id).first()
    if not is_blocked:
        return jsonify({'error': 'Profile already unblocked'}), 409 
    
    try:
        db.session.delete(is_blocked)
        db.session.commit()
        return jsonify({'message':'Profile unblocked successfully'}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error':'Failed to unblock profile'}), 500
    

@block_bp.route('/me/show-blocked-profiles', methods = ['GET'])
@auth_required
def get_blocked_profiles():
    current_user = request.current_user.user.id
    current_user_profile = UserProfile.query.get(current_user)

    if not current_user_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    if current_user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404

    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=50, type=int)

        block_query = db.session.query(UserProfile).join(BlockProfile, BlockProfile.blocked_id == UserProfile.id).filter(BlockProfile.blocker_id == current_user)

        paginated_blocks = block_query.paginate(
            page = page,
            per_page = per_page
        )

        block_list = [{
            'id': block.id,
            'banner_theme':block.banner_theme,
            'username':block.username,
            'profile_photo':block.profile_photo
        }
        for block in paginated_blocks.items]

        return jsonify({
            'blocked_profiles':block_list,
            'total':paginated_blocks.total,
            'total_pages':paginated_blocks.pages,
            'current_page':paginated_blocks.page
        }), 200
    
    except Exception:
        return jsonify({'error':'Failed to fetch block list'})
    