from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from models.user import UserInfo
from schemas.user_schema import user_info_schema, ValidationError
from util.decorators import profile_check_current__banned_removed

user_info_bp = Blueprint('user_info', __name__, url_prefix='/profile/info')

#done route testing
@user_info_bp.route('/me', methods = ['GET'])
@jwt_required()
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
    
#done route testing
@user_info_bp.route('/me/edit', methods = ['PATCH'])
@jwt_required()
@profile_check_current__banned_removed
def edit_info(user_profile):
    try:
        user_info = UserInfo.query.filter_by(user_profile_id = user_profile.id).first()

        data = request.get_json()

        try:
            valid = user_info_schema.load(data,partial = True)
        except ValidationError as error:
            return jsonify({"error": error.messages}), 400
        
        for key,value in valid.items():
            setattr(user_info,key,value)
                
        db.session.commit()
        return jsonify({'message':'Info updated successfully',
                        'updated_info': valid}), 200
    except Exception as e:
        db.session.rollback()
        error = getattr(e,'messages', str(e))
        return jsonify({'error': error}), 500
    

    