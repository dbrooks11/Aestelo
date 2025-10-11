from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.user import UserProfile
from models.block_profile import BlockProfile
from models.followers_and_following import Follow
from models.visit import Visit
from schemas.user_schema import ProfileSchema
from schemas.visit_schema import visit_schema, ValidationError
from routes.auth_required_wrapper import auth_required, admin_required

visit_bp = Blueprint('visit', __name__, '/visit')

@visit_bp.route('/<string:username>/profile-visits', methods = ['GET'])
@auth_required
def get_profile_visit_all(username):
    current_user = request.current_user.user.id
    user_profile = UserProfile.query.filter_by(username=username).first()

    if not user_profile:
        return jsonify({'error':'Profile not found'}), 404

    if user_profile.is_banned:
        return jsonify({'error':'Profile does not exist'}), 404
    
    is_blocked = BlockProfile.query.filter_by(blocker_id = user_profile.id,
                                              blocked_id = current_user).first()
    is_current_user_blocking = BlockProfile.query.filter_by(blocker_id = current_user,
                                                            blocked_id = user_profile.id).first()

    if is_blocked or is_current_user_blocking:
        return jsonify({'error':'Profile unavailable'}), 404


    if (current_user != user_profile.id) and (user_profile.is_private):
        is_following = Follow.query.filter_by(follower_id = current_user,
                                        following_id = user_profile.id).first()
        if not is_following:
            return jsonify({'error': 'Profile is private'}), 403
        
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)

        visit_query = Visit.query.filter_by(user_profile_id = user_profile.id)

        paginated_visit = visit_query.paginate(
            page=page,
            per_page=per_page
        )
        
        result = visit_schema.dump(paginated_visit, many=True)

        jsonify({
            'visits': result,
            'total': paginated_visit.total,
            'total_pages':paginated_visit.pages,
            'current_page':paginated_visit.page,
        }), 200

    except Exception:
        return jsonify({'error': 'Failed to fetch visit'}), 500
    
    
@visit_bp.route('/<string:username>/profile-visit/<int:visit_id>', methods = ['GET'])
@auth_required
def get_profile_visit(username, visit_id):
    current_user = request.current_user.user.id
    user_profile = UserProfile.query.filter_by(username = username).first()

    
    if not user_profile:
        return jsonify({'error':'Profile not found'}), 404

    if user_profile.is_banned:
        return jsonify({'error':'Profile does not exist'}), 404
    
    is_blocked = BlockProfile.query.filter_by(blocker_id = user_profile.id,
                                              blocked_id = current_user).first()
    is_current_user_blocking = BlockProfile.query.filter_by(blocker_id = current_user,
                                                            blocked_id = user_profile.id).first()

    if is_blocked or is_current_user_blocking:
        return jsonify({'error':'Profile unavailable'}), 404


    if (current_user != user_profile.id) and (user_profile.is_private):
        is_following = Follow.query.filter_by(follower_id = current_user,
                                        following_id = user_profile.id).first()
        if not is_following:
            return jsonify({'error': 'Profile is private'}), 403

    try:
        visit = Visit.query.get(visit_id = visit_id)
        result = visit_schema.dump(visit)
        if not visit or (visit.user_profile_id != user_profile.id) or visit.is_deleted or visit.is_removed:
            return jsonify({'error': 'Visit not found'}), 404

        return jsonify({'visit': result})
    except Exception:
        return jsonify({'error': 'Failed to fetch visit'}), 500
        
@visit_bp.route('/profile_visit/<int:visit_id>/edit', methods = ['PATCH'])
@auth_required
def edit_visit(visit_id):
    current_user = request.current_user.user.id
    current_user_profile = UserProfile.query.get(current_user)
    visit = Visit.query.filter_by(user_profile_id = current_user, visit_id = visit_id).first()

    if not current_user_profile:
        return jsonify({'error':'Profile not found'}), 404

    if current_user_profile.is_banned:
        return jsonify({'error':'Profile does not exist'}), 404
    
    if not visit:
        return jsonify({'error': 'Visit not found'}), 404
    
    try:
        data = request.get_json()

        try:
            visit_schema.load(data, partial = True)
        except ValidationError as error:
            return jsonify({"error": error.messages}), 400

        can_edit = (')
