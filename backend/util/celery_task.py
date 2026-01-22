from celery import shared_task
from models import SpotMedia,VisitMedia
from util.photo_processing import photo_processing_one_img_metadata,get_decimal_coordinates
from util.storage import s3, delete_file_s3, download_file, upload_to_s3
from util.outlier_coords import reject_post_type
import os
from typing import Literal
from extensions import db


@shared_task(bind=True, ignore_result=False)
def process_photos_with_metadata(self, key: str, post_type_id: int, user_id: str, upload_s3_foldername: str, post_type: Literal['spot', 'visit'], order: int):

    bucket = os.environ.get('R2_BUCKET_NAME')
    local_file_path = None

    try:
        metadata = s3.head_object(Bucket=bucket, Key=key)
        file_size = metadata.get('ContentLength')

        #TODO: make worker download file to temp folder and not ram
        
        if file_size > 20 * 1024 * 1024:
            delete_file_s3(file_path=key)
            raise Exception (f" File {key} is too big ({file_size}). It has been removed.")
        
        local_file_path = download_file(file_path=key)

        result = photo_processing_one_img_metadata(
                file=local_file_path,
                current_user_id=user_id
            )
        print(f'This is result from photo preocessing: {result}')
        latitude, longitude = get_decimal_coordinates(gps_info=result.get('gps'), key=key)
        print(f'This is lat and long: lat {latitude}, long {longitude}')
        uploaded_filepath = upload_to_s3(file_obj=result.get('file'), folder=upload_s3_foldername)

        if(post_type == 'spot'):
            is_duplicate = db.session.query(SpotMedia.query.filter_by(spot_id=post_type_id, photo_path=uploaded_filepath).exists()
            ).scalar()

            if not is_duplicate:
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
            is_duplicate = db.session.query(VisitMedia.query.filter_by(visit_id=post_type_id, photo_path=uploaded_filepath).exists()
            ).scalar()

            if not is_duplicate:
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
        try:
            reject_post_type(post_type_id=post_type_id, post_type=post_type)
        except Exception as e:
            raise Exception(str(e))
        raise Exception(str(e))