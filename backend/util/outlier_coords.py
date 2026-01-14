from geopy.distance import distance
from models.spot import Spot
from models.visit import Visit
from util.storage import delete_file_s3
from exstensions import db
from celery import shared_task
from datetime import datetime, timezone
from sqlalchemy.orm import joinedload

@shared_task
def average_location(coords, post_type_id: int, post_type: str):
    if not coords:
        return reject_post_type(post_type_id=post_type_id, post_type=post_type)
    
    avg_lat = sum(c['latitude'] for c in coords) / len(coords)
    avg_long = sum(c['longitude'] for c in coords) / len(coords)

    threshold_meters = 30
    filtered = [
        c for c in coords
        if distance((c['latitude'], c['longitude']), (avg_lat, avg_long)).m <= threshold_meters
    ]

    if not filtered:
        reject_post_type(post_type_id=post_type_id, post_type=post_type) 

    avg_lat = sum(c['latitude'] for c in filtered) / len(filtered)
    avg_long = sum(c['longitude'] for c in filtered) / len(filtered)


    return {'latitude': avg_lat, 'longitude': avg_long}


@shared_task
def average_location_batch(results, post_type_id: int, post_type:str):
    coords = [
        r for r in results 
        if r and isinstance(r, dict) and r.get('latitude') is not None and r.get('longitude') is not None
    ]
    try:
        if not coords:
            return reject_post_type(post_type_id=post_type_id, post_type=post_type)
        
        avg_lat = sum(c['latitude'] for c in coords) / len(coords)
        avg_long = sum(c['longitude'] for c in coords) / len(coords)

        threshold_meters = 30
        filtered = [
            c for c in coords
            if distance((c['latitude'], c['longitude']), (avg_lat, avg_long)).m <= threshold_meters
        ]

        if not filtered:
            return reject_post_type(post_type_id=post_type_id, post_type=post_type) 

        final_lat = sum(c['latitude'] for c in filtered) / len(filtered)
        final_long = sum(c['longitude'] for c in filtered) / len(filtered)

        item = None
        if post_type == 'spot':
            item = Spot.query.filter_by(id = post_type_id).options(
                joinedload(Spot.spot_media)
            ).first()
            media_count = len(item.spot_media)
        elif post_type == 'visit':
            item = Visit.query.filter_by(id=post_type_id).options(
                joinedload(Visit.visit_media)
            ).first()
            media_count = len(item.visit_media)
        
        if item:
            item.coordinates = f'POINT({final_long} {final_lat})'
            item.date_posted = datetime.now(timezone.utc)
            item.total_num_of_photos = media_count
            item.status = 'success'
            db.session.commit()

        return {'latitude': final_lat, 'longitude': final_long}

    except Exception as e:
        db.session.rollback()
        try:
            reject_post_type(post_type_id=post_type_id, post_type=post_type)
        except Exception as e:
            raise Exception(str(e))
        raise Exception(str(e))


def reject_post_type(post_type_id: int, post_type: str):
    try:
        if(post_type == 'spot'):
            spot = Spot.query.filter_by(id=post_type_id).options(
                joinedload(Spot.spot_media)
            ).first()
            if spot:
                if spot.spot_media:
                    for media in spot.spot_media:
                        delete_file_s3(media.photo_path)
                
                db.session.delete(spot)
                db.session.commit()

        if(post_type == 'visit'):
            visit = Visit.query.filter_by(id=post_type_id).options(
                joinedload(Visit.visit_media)
            ).first()
            if visit:
                if visit.visit_media:
                    for media in visit.visit_media:
                        delete_file_s3(media.photo_path)
                
                db.session.delete(visit)
                db.session.commit()
    except Exception:
        raise Exception(f'Deletion of {post_type} {post_type_id} failed')