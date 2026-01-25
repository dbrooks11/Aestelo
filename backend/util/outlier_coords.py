from geopy.distance import distance
from models import Spot, Visit
from util.storage import delete_file_s3
from extensions import db
from celery import shared_task
from datetime import datetime, timezone
from sqlalchemy.orm import joinedload
from flask import current_app

long = 'longitude'
lat = 'latitude'

@shared_task
def average_location(coords, post_type_id: int, post_type: str):
    if not coords:
        return reject_post_type(post_type_id=post_type_id, post_type=post_type)
    
    avg_lat = sum(c[lat] for c in coords) / len(coords)
    avg_long = sum(c[long] for c in coords) / len(coords)

    threshold_meters = 30
    filtered = [
        c for c in coords
        if distance((c[lat], c[long]), (avg_lat, avg_long)).m <= threshold_meters
    ]

    if not filtered:
        reject_post_type(post_type_id=post_type_id, post_type=post_type) 

    avg_lat = sum(c[lat] for c in filtered) / len(filtered)
    avg_long = sum(c[long] for c in filtered) / len(filtered)


    return {lat: avg_lat, long: avg_long}


@shared_task
def average_location_batch(results, post_type_id: int, post_type:str):
    
    for coords in results:
        result_lat = coords.get(lat)
        result_long = coords.get(long)
        print(results)
        print(result_lat)
        print(result_long)
        if result_long is None or result_lat is None:
            raise Exception('Invalid GPS data')
        
    try:
        if not results:
            raise Exception('Invalid Data provided')
        
        avg_lat = sum(c[lat] for c in results) / len(results)
        avg_long = sum(c[long] for c in results) / len(results)

        threshold_meters = 30
        filtered = [
            c for c in results
            if distance((c[lat], c[long]), (avg_lat, avg_long)).m <= threshold_meters
        ]

        if not filtered:
            raise Exception('Failed to determine GPS data') 

        final_lat = sum(c[lat] for c in filtered) / len(filtered)
        final_long = sum(c[long] for c in filtered) / len(filtered)

        # TODO: change query to use count instaed of joinedLoad
        #TODO: incrmement/de-increment spot/visit count on profile
        item = None
        if post_type == 'spot':
            Model = Spot
        elif post_type == 'visit':
            Model = Visit
            
        item = Model.query.filter_by(id=post_type_id).options(
            joinedload(Model.media)
        ).first()

        media_count = len(item.media)

        if not item:
            raise Exception(f'Failed to create {post_type}')
        
        if item:
            item.coordinates = f'POINT({final_long} {final_lat})'
            item.date_posted = datetime.now(timezone.utc)
            item.total_num_of_photos = media_count
            item.status = 'success'
            db.session.commit()

        return {lat: final_lat, long: final_long}

    except Exception as e:
        db.session.rollback()
        reject_post_type(post_type_id=post_type_id, post_type=post_type)
        raise Exception(str(e))


def reject_post_type(post_type_id: int, post_type: str):
    try:
        Model = None
        if(post_type == 'spot'):
            Model = Spot

        if(post_type == 'visit'):
            Model = Visit     
        
        item = None
        if Model:
            item = db.session.query(Model).filter_by(id=post_type_id).options(
                joinedload(Model.media)
            ).first()
        if not item:
            return
        
        media_list = item.media or [] 
        for media in media_list:
            status = delete_file_s3(file_path=media.photo_path)
            if not status:
                current_app.logger.warning(f"Failed to delete S3 file: {media.photo_path}")

        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        try:
            failed_item = Model.query.get(post_type_id)
            failed_item.status = 'failed'
            db.session.commit()
        except Exception:
            db.session.rollback()
        current_app.logger.error(f"Error rejecting {post_type} {post_type_id}: {str(e)}")
        raise e