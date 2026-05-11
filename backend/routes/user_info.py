from .extensions import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import AuthUser, UserInfo
from schemas.user_schema import ValidationError, user_info_schema
from utils.decorators import profile_check_current__banned_removed

user_info_bp = Blueprint('user_info', __name__, url_prefix='/profile/info')

#done route testing
@user_info_bp.route('/me', methods = ['GET'])
@jwt_required()
@profile_check_current__banned_removed
def get_info(user_profile):
    try:
        user_info = UserInfo.query.filter_by(user_id = user_profile.id).first()

        if not user_info:
            return jsonify({'error': 'Information not found'}), 404

        result = user_info_schema.dump(user_info)

        return jsonify({
            "information": result
        }), 200
    
    except Exception:
        return jsonify({'error': 'Failed to fetch information'}), 500
    
#done route testing
@user_info_bp.route('/me/edit', methods = ['PATCH'])
@jwt_required()
@profile_check_current__banned_removed
def edit_info(user_profile):
    current_user = get_jwt_identity()

    try:
        user_info = UserInfo.query.filter_by(user_id = user_profile.id).first()

        data = request.get_json()

        try:
            valid = user_info_schema.load(data,partial = True)
        except ValidationError as error:
            return jsonify({"error": error.messages}), 400
        
        if valid.get('email'):
            auth_user = AuthUser.query.get(current_user)
            auth_user.email = valid['email']
        
        for key,value in valid.items():
            setattr(user_info,key,value)
                
        db.session.commit()
        return jsonify({'message':'Info updated successfully',
                        'updated_info': valid}), 200
    except Exception as e:
        db.session.rollback()
        error = getattr(e,'messages', str(e))
        return jsonify({'error': error}), 500
    

    