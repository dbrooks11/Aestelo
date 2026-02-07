import os
import tempfile
from typing import Literal

from botocore.exceptions import BotoCoreError
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from config import Config
from extensions import db
from models import SpotMedia, VisitMedia

from util.photo_processing import (
    get_decimal_coordinates,
    photo_processing_one_img_metadata,
)
from util.storage import download_file_from_s3, s3, upload_to_s3

SSD_TEMP_DIR = os.environ.get('SSD_TMP_DIR', '/tmp')
MAX_FILE_SIZE = Config.MAX_FILE_SIZE

if not os.path.exists(SSD_TEMP_DIR):
    os.makedirs(SSD_TEMP_DIR, exist_ok=True)

def remove_file_ssd(file_paths: list = []):
    if file_paths:
        for file in file_paths:
            if file and os.path.exists(file):
                os.remove(file)


@shared_task(name='process_photos_metadata', bind=True, ignore_result=False, acks_late=True, time_limit=300, soft_time_limit=270, retry_backoff=True, max_retries=3,
autoretry_for=(ConnectionError, TimeoutError, BotoCoreError), )
def process_photos_with_metadata(self, key: str, post_type_id: int, user_id: str, upload_s3_foldername: str, post_type: Literal['spot', 'visit'], order: int):
    uploaded_filepath = None
    local_file_path = None
    result_path = None
    bucket = os.environ.get('R2_BUCKET_NAME')
    file_paths = []

    if post_type == 'spot':
        MediaModel = SpotMedia
        fk_field = 'spot_id'
    elif post_type == 'visit':
        MediaModel = VisitMedia
        fk_field = 'visit_id'

    try:
        existing_media = MediaModel.query.filter_by(**{fk_field: post_type_id, "sort_order": order}
        ).first()

        if existing_media:
            uploaded_filepath = existing_media.photo_path
            return {"success": True, "path": uploaded_filepath, "duplicate": True}

        metadata = s3.head_object(Bucket=bucket, Key=key)
        file_size = metadata.get('ContentLength')

        if file_size > MAX_FILE_SIZE:
            return {'success': False, 'error': 'File too big', 'key': key}
        try:
            with tempfile.NamedTemporaryFile(delete=False, dir=SSD_TEMP_DIR) as tmp:
                local_file_path = tmp.name
                download_file_from_s3(key, local_file_path)

            result = photo_processing_one_img_metadata(file_path=local_file_path, current_user_id=user_id)
            result_path = result.get('file_path')
            file_paths = [local_file_path, result_path]
            
            latitude, longitude = get_decimal_coordinates(gps_info=result.get('gps'), key=key)
            if latitude is None or longitude is None:
                return {'success': False, 'error': 'No GPS metadata', 'key': key}

            # TODO: add check for if file is already uploaded to s3 incase a celery worker does a retry
            uploaded_filepath = upload_to_s3(file=result_path, folder=upload_s3_foldername)

            
            
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
            return {
                'success': True,
                'longitude': longitude, 
                'latitude': latitude,
                'path': uploaded_filepath
            }
        finally:
            remove_file_ssd(file_paths)

    except SoftTimeLimitExceeded:
        db.session.rollback()
        remove_file_ssd(file_paths)
        return {
            'success': False,
            'path': uploaded_filepath, 
            'key': key 
        }

    except Exception as e:
        db.session.rollback()
        remove_file_ssd(file_paths)
        return {
            'success': False, 
            'error': str(e), 
            'path': uploaded_filepath, 
            'key': key 
        }
    
        