from litestar_saq import monitored_job
from typing import Literal, Any
from app.utils.parse_gps import gps
from app.utils.calculate_colors import color
from app.utils.media_processing import process_media_image
from litestar.exceptions import ValidationException
from saq.types import Context
from app.utils.storage import storage_bb
from app.db.models.services.spot import SpotMediaService, SpotService
from app.db.models.services.visit import VisitService, VisitMediaService
from app.db.session import get_db_session
from geoalchemy2.functions import ST_Point
from app.db.enum_schemas import UploadStatusEnum

GPS_FIELD_NAME = 'gps'
ORDER_FIELD_NAME = 'sort_order'
KEY_NAME = 'media_key'
PALETTE_NAME = 'color_palette'

@monitored_job(1.0)
async def process_post_media(ctx: Context, *, post_type: Literal['spot','visit'], post_id: int, sort_order: int, obj_key: str):
    is_uploaded: bool = False 
    new_obj_key: str = ''
    try:
        processed_media = await process_media_image(storage=storage_bb, obj_key=obj_key, need_exif=True, need_colors=True)

        compressed_file: Any | None = processed_media.get('compressed_file', None)
        mimetype: str | None = processed_media.get('mimetype', None)
        exif: dict[str,str] | None = processed_media.get('exif', None)
        palette_rgb: list[tuple[int, int, int]] | None = processed_media.get('color_palette')
 
        if not compressed_file or not mimetype or not exif:
            raise ValidationException(f'Failed to process media. Invalid data for {post_type}_{post_id} - {obj_key}')
        
        coordinates = await gps.get_lat_long(exif=exif)

        if not coordinates:
            raise ValidationException(f'No GPS data for {post_type}_{post_id} - {obj_key}')

        new_obj_key = await storage_bb.generate_file_name(mimetype=mimetype, id=post_id, is_post=True, folder=post_type)
        is_uploaded = await storage_bb.upload_file_s3(object_key=new_obj_key, file=compressed_file, mimetype=mimetype)

        if not is_uploaded:
            raise Exception(f'Failed to upload media: {new_obj_key}')
        
        post_id_field = f'{post_type}_id'
        return {
            post_id_field: post_id,
            ORDER_FIELD_NAME: sort_order,
            GPS_FIELD_NAME: coordinates,
            KEY_NAME: new_obj_key,
            PALETTE_NAME: palette_rgb
        }    
    except Exception:
        raise


@monitored_job(1.0)
async def finalize_media_results(ctx: Context, *, data: list[dict], 
                                 user_id: str, post_type: Literal['spot','visit'], 
                                 post_id: int):
    
    media_service = None
    post_service = None
    try:
        coords: list[dict[str, float]] = []
        palette_list: list[list[tuple[int, int, int]]] = []

        for item in data:
            coord = item.pop(GPS_FIELD_NAME, None)
            palette = item.pop(PALETTE_NAME, None)
            if coord:
                coords.append(coord)
            if palette:
                palette_list.append(palette)

        if not coords:
            raise ValidationException('Invalid GPS data')

        avg_coords = await gps.average_location(coords=coords)
        if not avg_coords:
            raise ValidationException('Distance between media varies greatly')

        point = ST_Point(avg_coords.get(gps.LOCATION_KEY_LON), avg_coords.get(gps.LOCATION_KEY_LAT), 4326)

        averaged = await color.average_palettes(palette_list)  
        color_tags = await color.palette_to_color_tags(averaged)

        update_fields = {
            'coordinates': point,
            'color_palette': color_tags,
            'status': UploadStatusEnum.SUCCESS
        }

        async with get_db_session() as session:
            if post_type == 'spot':
                media_service = SpotMediaService(session=session)
                post_service = SpotService(session=session)   
            else: 
                media_service = VisitMediaService(session=session)
                post_service = VisitService(session=session)


            if media_service and post_service:
                media = await media_service.create_many(data=data)
                updated_spot = await post_service.update(data=update_fields, item_id=post_id)
                
    except Exception:
        if (media or updated_spot) and post_service:
            await post_service.delete(item_id=post_id)
        raise

        

