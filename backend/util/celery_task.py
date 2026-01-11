from celery import shared_task
from models.spot import SpotMedia
from models.visit import VisitMedia
from util.photo_processing import photo_processing_one_img_metadata,get_decimal_coordinates
from util.storage import s3, delete_file_s3, download_file, upload_to_s3
import os
from typing import Literal
from exstensions import db

@shared_task(bind=True, ignore_result=False)
def process_photos_with_metadata(self, key: str, post_type_id: int, user_id: str, upload_s3_foldername: str, post_type: Literal['spot', 'visit'], order: int):

    bucket = os.environ.get('R2_BUCKET_NAME')
    local_file_path = None

    try:
        metadata = s3.head_object(Bucket=bucket, Key=key)
        file_size = metadata.get('ContentLength')
        
        if file_size > 20 * 1024 * 1024:
            delete_file_s3(file_path=key)
            raise Exception (f" File {key} is too big ({file_size}). It has been removed.")
        
        local_file_path = download_file(file_path=key)

        result = photo_processing_one_img_metadata(
                file=local_file_path,
                current_user_id=user_id
            )
        print(f'This is the reulst of celery processing: {result}')
        
        latitude, longitude = get_decimal_coordinates(result.get('gps'))

        if not latitude or not longitude:
            raise Exception( f'No location data provided for {key}')

        print(f'These are the coords: {longitude},{latitude}')

        uploaded_filepath = upload_to_s3(file_obj=result.get('file'), folder=upload_s3_foldername)

        if(post_type == 'spot'):
            media = SpotMedia(
                spot_id=post_type_id,
                uploaded_by=user_id,
                sort_order=order,
                photo_path=uploaded_filepath,
                photo_type=result.get('type'),
                width=result.get('width'),
                height=result.get('height')
            )
        
        if(post_type == 'visit'):
            media = VisitMedia(
                visit_id=post_type_id,
                uploaded_by=user_id,
                sort_order=order,
                photo_path=uploaded_filepath,
                photo_type=result.get('type'),
                width=result.get('width'),
                height=result.get('height')
            )
        
        db.session.add(media)
        db.session.commit()
        return {
            'longitude': longitude, 
            'latitude': latitude
        }
    except Exception as e:
        db.session.rollback()
        if local_file_path and os.path.exists(local_file_path):
            os.remove(local_file_path)
        raise Exception(str(e))