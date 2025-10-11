from flask import Blueprint, request, jsonify
from app import db
from models.user import UserProfile, UserInfo
from schemas.user_schema import user_info_schema, ValidationError
from routes.auth_required_wrapper import auth_required

user_info_bp = Blueprint('user_info', __name__, url_prefix='/profile/info')


@user_info_bp.route('/me', methods = ['GET'])
@auth_required
def get_info():
    current_user = request.current_user.user.id
    current_user_profile = UserProfile.query.get(current_user)

    if not current_user_profile or current_user_profile.is_banned:
        return jsonify({'error':'Profile does not exist'}), 404

    try:
        user_info = UserInfo.query.filter_by(user_profile_id = current_user_profile.id)

        if not user_info:
            return jsonify({'error': 'Settings not found'}), 404


        result = user_info_schema.dump(user_info)

        return jsonify({
            "Info": result
        }), 200
    
    except Exception:
        return jsonify({'error': 'Failed to fetch info'}), 500
    

@user_info_bp.route('/me/edit', methods = ['PATCH'])
@auth_required
def edit_info():
    current_user = request.current_user.user.id
    user_info = UserInfo.query.filter_by(user_profile_id = current_user).first()

    try:
        data = request.get_json()

        try:
            user_info_schema.load(data, partial = True)
        except ValidationError as error:
            return jsonify({"error": error.messages}), 400

        can_edit = ('first_name','last_name','email','date_of_birth','age','gender','height_ft','height_in', 'state','city')

        for field in can_edit:
            if field in data:
                setattr(user_info, field, data[field])
                
        db.session.commit()
        return jsonify({'message':'Info updated successfully',
                        'updated_info': user_info_schema.dump(user_info)}), 200
    except Exception as e:
        db.session.rollback()
        error = getattr(e,'messages', str(e))
        return jsonify({'error': error}), 500
    

    