from litestar_saq import monitored_job
from typing import Literal, Any
from app.utils.gps import gps
from app.settings import settings
from app.utils.media import process_media_image
from litestar.exceptions import ValidationException, InternalServerException
from saq.types import Context
from app.utils.storage import storage, storage_private
from app.services.spot import SpotMediaService, SpotService
from app.services.visit import VisitService, VisitMediaService
from app.db.session import get_db_session
from geoalchemy2.functions import ST_Point
from app.db.enums import UploadStatusEnum
import asyncio


media_semaphore = asyncio.Semaphore(settings.misc.MAX_CONCURRENT_IMAGES)

GPS_FIELD_NAME = "gps"
ORDER_FIELD_NAME = "sort_order"
KEY_NAME = "media_key"
POST_TYPE_NAME = "post_type"
UPLOADED_BY_FIELD = "uploaded_by"


async def process_post_media(
    post_type: Literal["spot", "visit"],
    post_id: int,
    sort_order: int,
    obj_key: str,
    user_id: str,
):

    async with media_semaphore:
        is_uploaded: bool = False
        new_obj_key: str = ""
        try:
            processed_media = await process_media_image(
                storage=storage_private,
                obj_key=obj_key,
                need_exif=True,
                need_colors=True,
            )

            compressed_file: Any | None = processed_media.get("compressed_file", None)
            original_mimetype: str | None = processed_media.get(
                "original_mimetype", None
            )
            new_mimetype: str | None = processed_media.get("new_mimetype", None)
            exif: dict[str, str] | None = processed_media.get("exif", None)

            if not all([compressed_file, original_mimetype, new_mimetype, exif]):
                raise ValidationException(
                    detail="Failed to process media. Invalid data"
                )

            coordinates = await gps.get_lat_long(exif=exif)

            if not coordinates:
                raise ValidationException(detail="No GPS data found")

            valid_extension = await storage.verify_file_type(
                mimetype=original_mimetype, is_post=True
            )
            new_obj_key = await storage.generate_file_name(
                id=post_id, folder=post_type, extension=valid_extension
            )
            is_uploaded = await storage.upload_file_s3(
                object_key=new_obj_key, file=compressed_file, mimetype=new_mimetype
            )  # type: ignore

            if not is_uploaded:
                raise InternalServerException(detail="Failed to upload media")

            post_id_field = f"{post_type}_id"
            return {
                post_id_field: post_id,
                UPLOADED_BY_FIELD: user_id,
                ORDER_FIELD_NAME: sort_order,
                GPS_FIELD_NAME: coordinates,
                KEY_NAME: new_obj_key,
            }

        except ValidationException:
            raise
        except Exception:
            if is_uploaded and new_obj_key:
                await storage.delete_file_s3(key=new_obj_key)
            raise


@monitored_job(1.0)
async def process_post_pipeline(
    ctx: Context,
    *,
    tasks: list[dict[str, str | int]],
    post_type: Literal["spot", "visit"],
    post_id: int,
    user_id: str,
):
    queued_task: list = []
    media_data: list[dict | BaseException] = []

    try:
        for task in tasks:
            sort_order: int | None = task.get(ORDER_FIELD_NAME)  # type: ignore
            key: str | None = task.get("obj_key")  # type: ignore
            if sort_order and key:
                queued_task.append(
                    process_post_media(
                        post_type=post_type,
                        post_id=post_id,
                        sort_order=sort_order,
                        obj_key=key,
                        user_id=user_id,
                    )
                )

        if not queued_task:
            return

        media_data = await asyncio.gather(*queued_task, return_exceptions=True)

        media_service = None
        post_service = None

        coords: list[dict[str, float]] = []

        for item in media_data:
            if isinstance(item, BaseException):
                raise item
            coord = item.pop(GPS_FIELD_NAME, None)
            if coord:
                coords.append(coord)  # type: ignore

        if not coords:
            raise ValidationException(detail="Invalid GPS data")

        avg_coords = await gps.average_location(coords=coords)
        if not avg_coords:
            raise ValidationException(
                detail="Distance between media varies greatly. Please make sure that all media was taken within proximity of each other"
            )

        async with get_db_session() as session:
            if post_type == "spot":
                spot_data: dict = {}
                post_service = SpotService(session=session)
                media_service = SpotMediaService(session=session)
                point = ST_Point(
                    avg_coords.get(gps.LOCATION_KEY_LON),
                    avg_coords.get(gps.LOCATION_KEY_LAT),
                    4326,
                )
                spot_data["coordinates"] = point
                spot_data["status"] = UploadStatusEnum.SUCCESS
                await post_service.update_spot(data=spot_data, spot_id=post_id)
            else:
                post_service = VisitService(session=session)
                media_service = VisitMediaService(session=session)

            if media_service and post_service:
                await media_service.create_many(data=media_data)

    except:
        if media_data:
            for item in media_data:
                key = None
                if not isinstance(item, BaseException):
                    key = item.get(KEY_NAME)
                if key and isinstance(key, str):
                    await storage.delete_file_s3(key=key)

        async with get_db_session() as session:
            if post_type == "spot":
                post_service = SpotService(session=session)
                await post_service.update_spot(
                    data={"status": UploadStatusEnum.FAILED}, spot_id=post_id
                )
            else:
                post_service = VisitService(session=session)
        raise
