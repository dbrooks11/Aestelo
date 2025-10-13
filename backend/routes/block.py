from app import db
from models.user import UserProfile
from flask import Blueprint, request, jsonify
from models.block_profile import BlockProfile
from models.followers_and_following import Follow
from routes.auth_required_wrapper import auth_required
from schemas.user_schema import UserProfileSchema, partial_schema

block_bp = Blueprint('block', __name__, url_prefix='/block')


@block_bp.route('/<string:id>/block-profile', methods = ['POST'])
@auth_required
def block_profile(id):
    current_user = request.current_user.user.id
    user_profile = UserProfile.query.get(id)

    if user_profile is None:
        return jsonify({'error': 'Profile not found'}), 404
    
    if user_profile.is_deleted:
        return jsonify({'error': 'Profile does not exist'}), 404
    
    if user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    if current_user == user_profile.id:
        return jsonify({'error': 'Action not permitted'}), 409
    
    is_blocked = BlockProfile.query.filter_by(blocker_id = current_user,
                                              blocked_id = user_profile.id).exists()
    if is_blocked:
        return jsonify({'error': 'Profile already blocked'}), 409 
    
    try:
        new_blocked = BlockProfile(
            blocker_id = current_user,
            blocked_id = user_profile.id
        )
        db.session.add(new_blocked)
        
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
            
        
        db.session.commit()
        return jsonify({'message':'Profile blocked successfully'}), 201
    except Exception:
        db.session.rollback()
        return jsonify({'error':'Failed to block profile'}), 500

       
@block_bp.route('/<string:id>/unblock-profile', methods = ['DELETE'])
@auth_required
def unblock_profile(username):
    current_user = request.current_user.user.id
    user_profile = UserProfile.query.filter_by(username = username).first()

    if user_profile is None:
        return jsonify({'error': 'Profile not found'}), 404
    
    if user_profile.is_deleted:
        return jsonify({'error': 'Profile does not exist'}), 404
    
    if user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404
    
    if current_user == user_profile.id:
        return jsonify({'error': 'Action not permitted'}), 409
    
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
    

@block_bp.route('/me/show-blocked-profiles', methods = ['GET'])
@auth_required
def get_blocked_profiles():
    current_user = request.current_user.user.id
    current_user_profile = UserProfile.query.get(current_user)

    if current_user_profile is None:
        return jsonify({'error': 'Profile not found'}), 404
    
    if current_user_profile.is_deleted:
        return jsonify({'error': 'Profile does not exist'}), 404
    
    if current_user_profile.is_banned:
        return jsonify({'error':'Profile unavailable'}),404

    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=50, type=int)
        if per_page > 50:
            per_page = 50

        block_query = db.session.query(UserProfile).join(BlockProfile, BlockProfile.blocked_id == UserProfile.id).filter(BlockProfile.blocker_id == current_user)

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
    