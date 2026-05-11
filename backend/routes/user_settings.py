from .extensions import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import UserSettings
from schemas.user_schema import ValidationError, user_settings_schema
from utils.decorators import profile_check_current__banned_removed

user_settings_bp = Blueprint('user_settings', __name__, url_prefix='/profile/settings')

#done route testing
@user_settings_bp.route('/me', methods = ['GET'])
@jwt_required()
@profile_check_current__banned_removed
def get_settings(user_profile):
    try:
        user_settings = UserSettings.query.filter_by(user_id = user_profile.id).first()

        result = user_settings_schema.dump(user_settings)

        return jsonify({
            "settings": result
        }), 200

    except Exception:
        return jsonify({'error': 'Failed to fetch settings'}), 500
    
#done route testing
@user_settings_bp.route('/me/edit', methods = ['PATCH'])
@jwt_required()
@profile_check_current__banned_removed
def edit_settings(user_profile):
    
    try:
        user_settings = UserSettings.query.filter_by(user_id = user_profile.id).first()

        data = request.get_json()

        try:
            valid = user_settings_schema.load(data, partial = True)
        except ValidationError as error:
            return jsonify({"error": error.messages}), 400

        for key, value in valid.items():
            setattr(user_settings,key, value)

        db.session.commit()
        return jsonify({'message':'Settings updated successfully',
                        'updated_settings': valid}), 200
    except Exception as e:
        db.session.rollback()
        error = getattr(e,'messages', str(e))
        return jsonify({'error': error}), 500

