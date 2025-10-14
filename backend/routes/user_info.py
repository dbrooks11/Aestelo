from flask import Blueprint, request, jsonify
from app import db
from models.user import UserProfile, UserInfo
from schemas.user_schema import user_info_schema, ValidationError
from routes.auth_required_wrapper import auth_required
from util.decorators import profile_check_current__banned_removed

user_info_bp = Blueprint('user_info', __name__, url_prefix='/profile/info')


@user_info_bp.route('/me', methods = ['GET'])
@auth_required
@profile_check_current__banned_removed
def get_info(user_profile):
    try:
        user_info = UserInfo.query.filter_by(user_profile_id = user_profile.id).first()

        if not user_info:
            return jsonify({'error': 'Information not found'}), 404

        result = user_info_schema.dump(user_info)

        return jsonify({
            "information": result
        }), 200
    
    except Exception:
        return jsonify({'error': 'Failed to fetch information'}), 500
    

@user_info_bp.route('/me/edit', methods = ['PATCH'])
@auth_required
@profile_check_current__banned_removed
def edit_info(user_profile):
    try:
        user_info = UserInfo.query.filter_by(user_profile_id = user_profile.id).first()

        data = request.get_json()

        try:
            user_info_schema.load(data,instance=user_info, partial = True, session=db.session)
        except ValidationError as error:
            return jsonify({"error": error.messages}), 400
                
        db.session.commit()
        return jsonify({'message':'Info updated successfully',
                        'updated_info': user_info_schema.dump(user_info)}), 200
    except Exception as e:
        db.session.rollback()
        error = getattr(e,'messages', str(e))
        return jsonify({'error': error}), 500
    

    