from io import BytesIO
import logging
from app.extensions  import db
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import AuthUser, BlockProfile, Follow, UserProfile
from schemas.user_schema import (
    ValidationError,
    UserProfileSchema
)
from sqlalchemy import exists, select
from sqlalchemy.orm import load_only
from utils import delete_file_s3, photo_processing_one_img, upload_to_s3
from utils.decorators import profile_check_current__banned_removed

profile_bp = Blueprint('profile',__name__, url_prefix='/profile')
root_logger = logging.getLogger("root")

@profile_bp.route('/me', methods = ['GET','PATCH'])
@jwt_required()
def profile_me():
    current_user = get_jwt_identity()
    try:
        user_profile = db.session.scalars(select(UserProfile.me).where(UserProfile.id == current_user)).first()
        return jsonify({'my_profile': UserProfileSchema.dump(user_profile)}), 200
    except Exception as e:
        error_msg = "Failed to fetch profile"
        root_logger.error(error_msg,
                     error = str(e),
                     exec_info=True)
        return jsonify({'error': error_msg}), 500
    
    
    

@profile_bp.route('/me/edit', methods = ['PATCH'])
@jwt_required()
def edit_profile():
    current_user = get_jwt_identity()

    # Use background job instead
    try:
        form_data = request.form.to_dict()

        if not form_data.items:
            return jsonify({'error': 'Invalid data'}), 403
        
        if form_data.get('username') == user_profile.username:
            form_data.pop('username')
        else:
            form_data['username'] = form_data.get('username').lower()
        
        if form_data.get('bio') == user_profile.bio:
            form_data.pop('bio')


        if form_data:
            try:
                validate_data = UserProfileSchema.load(form_data, partial=True) 
            except ValidationError as e:
                current_app.logger.error(f"Data could not be validated: {str(e)}")
                print(e.messages)
                return jsonify({'error': e.messages}),400
        

        form_files = request.files
        photo_list = request.files.getlist('profile_photo')
        banner_list = request.files.getlist('profile_banner')

        if len(photo_list) > 1:
            return jsonify({'error': 'You can only upload one profile photo at a time.'}), 400

        if len(banner_list) > 1:
            return jsonify({'error': 'You can only upload one banner at a time.'}), 400
        
        profile_photo_compressed: list | BytesIO = None
        profile_banner_compressed: list | BytesIO = None
        new_photo_path: str | None = None
        new_banner_path: str | None = None

        old_photo_path = user_profile.profile_photo
        old_banner_path = user_profile.profile_banner

        photo_field_name: str = 'profile_photo'
        banner_field_name: str = 'profile_banner'

        try:
            if photo_field_name in form_files:
                if form_files[photo_field_name].filename:
                    photo_file = form_files.get(photo_field_name)
                    if photo_file:
                        profile_photo_compressed: list | BytesIO = photo_processing_one_img(photo_file, is_banner=False, current_user_id=user_profile.id)

                        if isinstance(profile_photo_compressed, list):
                            return jsonify({'error': {photo_field_name: profile_photo_compressed[0]}}),400
                        
                        new_photo_path: str = upload_to_s3(file_obj=profile_photo_compressed, folder=f'{photo_field_name}/{current_user}')
                

            if banner_field_name in form_files:
                if form_files[banner_field_name].filename:
                    banner_file = form_files.get(banner_field_name)
                    if banner_file:
                        profile_banner_compressed: list | BytesIO = photo_processing_one_img(banner_file, is_banner=True, current_user_id=user_profile.id)

                        if isinstance(profile_banner_compressed, list):
                            return jsonify({'error': {banner_field_name: profile_banner_compressed[0]}}), 400
                        
                        
                        new_banner_path: str = upload_to_s3(file_obj=profile_banner_compressed,folder=f'{banner_field_name}/{current_user}')
                
        except Exception as e:
            current_app.logger.error(f"Image processing failed: {str(e)}")
            return jsonify({'error': f'Image processing failed: {str(e)}'}), 500

        if form_data:
            for key, value in validate_data.items():
                if key == 'username':
                    auth_user = AuthUser.query.options(load_only(AuthUser.username)).get(user_profile.id)
                    if auth_user:
                        auth_user.username = value
                if hasattr(user_profile, key):    
                    setattr(user_profile,key, value)

        if new_photo_path:
            user_profile.profile_photo = new_photo_path
        if new_banner_path:
            user_profile.profile_banner = new_banner_path

        db.session.commit() 

        try:
            if new_photo_path and old_photo_path:
                delete_file_s3(old_photo_path)
            if new_banner_path and old_banner_path:
                delete_file_s3(old_banner_path)
        except Exception as e:
            current_app.logger.warning(f"Failed to delete old images: {str(e)}")
            return jsonify({'error': str(e)})
            
        return jsonify({'message': 'profile updated',
                        'updated_fields': UserProfileSchema.dump(user_profile)}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Database Update Failed: {str(e)}")

        try:
            if new_photo_path: 
                delete_file_s3(new_photo_path)
            if new_banner_path: 
                delete_file_s3(new_banner_path)
        except:
            pass

        return jsonify({'error': 'Failed to update profile'}), 500

@profile_bp.route('/<string:id>', methods = ['GET'])
@jwt_required()
@profile_check_current__banned_removed
def user_profile(id, user_profile):
    
    is_blocked = db.session.query(exists().where((BlockProfile.blocker_id ==user_profile.id) & (BlockProfile.blocked_id == id))).scalar()

    is_current_user_blocking = db.session.query(exists().where((BlockProfile.blocker_id == id) & (BlockProfile.blocked_id == user_profile.id))).scalar()
    
    if is_blocked or is_current_user_blocking:
        return jsonify({'error': 'Profile unavailable'}), 404
    
    #checks if the profile the user is veiwing is themselves
    if user_profile.id == id:
        try:
            return jsonify({'me': UserProfileSchema.dump(user_profile)}), 200
        except Exception:
            return jsonify({'error': 'Failed to fetch profile'}), 500
    
    #check if current user is a follower of the person's profile they are trying to view
    is_following = db.session.query(exists().where((Follow.follower_id == user_profile.id) & (Follow.following_id == id))).scalar()

    #if user profile is private, check if the person that is trying to view it is following them
    if user_profile.is_private and not is_following:
        try:
            return jsonify({'user_profile':UserProfileSchema.dump(user_profile)}), 200
        except Exception:
            return jsonify({'error': 'Failed to fetch profile'}), 500
        
    return jsonify({'user_profile':UserProfileSchema.dump(user_profile)}), 200
    
