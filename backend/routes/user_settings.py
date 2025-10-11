from flask import Blueprint, request, jsonify
from app import db
from models.user import UserProfile, UserSettings
from schemas.user_schema import user_settings_schema, ValidationError
from routes.auth_required_wrapper import auth_required

user_settings_bp = Blueprint('user_settings', __name__, url_prefix='/profile/settings')


@user_settings_bp.route('/me', methods = ['GET'])
@auth_required
def get_settings():
    current_user = request.current_user.user.id
    current_user_profile = UserProfile.query.get(current_user)

    if not current_user_profile or current_user_profile.is_banned:
        return jsonify({'error':'Profile does not exist'}), 404

    try:
        user_settings = UserSettings.query.filter_by(user_profile_id = current_user)


        result = user_settings_schema.dump(user_settings)

        return jsonify({
            "settings": result
        }), 200

    except Exception:
        return jsonify({'error': 'Failed to fetch settings'}), 500
    

@user_settings_bp.route('/me/edit', methods = ['PATCH'])
@auth_required
def edit_settings():
    current_user = request.current_user.user.id
    user_settings = UserSettings.query.filter_by(user_profile_id = current_user).first()

    try:

        data = request.get_json()

        try:
            user_settings_schema.load(data, partial = True)
        except ValidationError as error:
            return jsonify({"error": error.messages}), 400

        can_edit = ('language_preference','email_notifications',
                    'push_notifications','location_sharing',
                    'data_usage_consent','marketing_consent',
                    'theme_preference')

        for field in can_edit:
            if field in data:
                setattr(user_settings,field,data[field])

        db.session.commit()
        return jsonify({'message':'Settings updated successfully',
                        'updated_settings': user_settings_schema.dump(user_settings)}), 200
    except Exception as e:
        db.session.rollback()
        error = getattr(e,'messages', str(e))
        return jsonify({'error': error}), 500

