from datetime import datetime, timezone

from celery import shared_task
from app.extensions import db
from flask import current_app
from geopy.distance import distance
from models import Spot, Visit
from sqlalchemy.orm import joinedload

from utils.storage import delete_file_s3

long = 'longitude'
lat = 'latitude'

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


@shared_task(name='location_batch')
def average_location_batch(results, post_type_id: int, post_type:str):
    
    try:
        failed_items = [r for r in results if not r.get('success')]
        if failed_items:
            error_msg = failed_items[0].get('error', 'Unknown worker error')
            raise Exception(f"Batch failed: {error_msg}")

        if not results:
            raise Exception('No results returned from workers')
        
        avg_lat = sum(c[lat] for c in results) / len(results)
        avg_long = sum(c[long] for c in results) / len(results)

        threshold_meters = 30
        filtered = [
            c for c in results
            if distance((c[lat], c[long]), (avg_lat, avg_long)).m <= threshold_meters
        ]

        if len(filtered) != len(results):
            outlier_count = len(results) - len(filtered)
            raise Exception(f"GPS Validation Failed: {outlier_count} photo(s) were more than {threshold_meters}m from the group average.")

        if not filtered:
            raise Exception('Failed to determine GPS data') 

        final_lat = sum(c[lat] for c in filtered) / len(filtered)
        final_long = sum(c[long] for c in filtered) / len(filtered)

        #TODO: incrmement/de-increment spot/visit count on profile
        item = None
        if post_type == 'spot':
            Model = Spot
        elif post_type == 'visit':
            Model = Visit
            
        item = Model.query.filter_by(id=post_type_id).options(
            joinedload(Model.media)
        ).first()

        if not item:
            raise Exception(f'{post_type} {post_type_id} not found')
        
        item.coordinates = f'POINT({final_long} {final_lat})'
        item.date_posted = datetime.now(timezone.utc)
        item.total_num_of_photos = len(item.media)
        item.status = 'success'
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        reject_post_type(post_type_id=post_type_id, post_type=post_type, results=results)
        raise Exception(str(e))


def reject_post_type(post_type_id: int, post_type: str, results: list = None):
    Model = None
    try:
        if(post_type == 'spot'):
            Model = Spot
        elif(post_type == 'visit'):
            Model = Visit     
        
        if not Model:
            return
        
        item = db.session.query(Model).filter_by(id=post_type_id).options(
            joinedload(Model.media)
        ).first()

        if not item:
            return
        
        media_list = item.media or [] 
        for media in media_list:
            delete_file_s3(file_path=media.photo_path)
            
        if results:
            for r in results:
                path = r.get('path')
                if path:
                    delete_file_s3(file_path=path)
                    

        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        try:
            failed_item = Model.query.get(post_type_id)
            if failed_item:
                failed_item.status = 'failed'
                db.session.commit()
        except Exception:
            db.session.rollback()
        current_app.logger.error(f"Error rejecting {post_type} {post_type_id}: {str(e)}")
        raise e