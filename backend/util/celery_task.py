from celery import shared_task
import tempfile
from models import SpotMedia,VisitMedia
from util.photo_processing import photo_processing_one_img_metadata,get_decimal_coordinates
from util.storage import s3, download_file_from_s3, upload_to_s3
import os
from typing import Literal
from extensions import db


@shared_task(bind=True, ignore_result=False)
def process_photos_with_metadata(self, key: str, post_type_id: int, user_id: str, upload_s3_foldername: str, post_type: Literal['spot', 'visit'], order: int):
    uploaded_filepath = None
    local_file_path = None
    bucket = os.environ.get('R2_BUCKET_NAME')

    try:
        metadata = s3.head_object(Bucket=bucket, Key=key)
        file_size = metadata.get('ContentLength')

        if file_size > (20 * 1024 * 1024):
            return {'success': False, 'error': 'File too big', 'key': key}
        try:
            with tempfile.NamedTemporaryFile(suffix='.tmp',delete=False) as tmp:
                local_file_path = tmp.name
                download_file_from_s3(key, local_file_path)

            result = photo_processing_one_img_metadata(file=local_file_path, current_user_id=user_id)
            
            latitude, longitude = get_decimal_coordinates(gps_info=result.get('gps'), key=key)
            if latitude is None or longitude is None:
                return {'success': False, 'error': 'No GPS metadata', 'key': key}

            uploaded_filepath = upload_to_s3(file_obj=result.get('file'), folder=upload_s3_foldername)

            if post_type == 'spot':
                MediaModel = SpotMedia
                fk_field = 'spot_id'
            elif post_type == 'visit':
                MediaModel = VisitMedia
                fk_field = 'visit_id'
            
            media = MediaModel(**{
                fk_field: post_type_id,
                'uploaded_by': user_id,
                'sort_order': order,
                'photo_path': uploaded_filepath,
                'photo_type': result.get('type'),
                'width': result.get('width'),
                'height': result.get('height')
            })
            
            db.session.add(media)
            db.session.commit()

            if os.path.exists(local_file_path):
                os.remove(local_file_path)

            return {
                'success': True,
                'longitude': longitude, 
                'latitude': latitude,
                'path': uploaded_filepath
            }
        finally:
            if local_file_path and os.path.exists(local_file_path):
                os.remove(local_file_path)

    except Exception as e:
        db.session.rollback()
        if local_file_path and os.path.exists(local_file_path):
            os.remove(local_file_path)
        return {
            'success': False, 
            'error': str(e), 
            'path': uploaded_filepath, 
            'key': key 
        }