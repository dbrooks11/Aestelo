from saq.types import Context
from app.utils.storage import ObjectStorage
from app.utils.media_processing import process_media_image
from app.db.models.services.user import UserProfileService
from app.schemas.user import UserProfileEdit
from app.db.session import get_db_session
from litestar_saq import monitored_job
from app.settings import settings


@monitored_job()
async def process_profile_media(ctx: Context, *, user_id: str, field: str, obj_key: str):
    storage_bb = ObjectStorage(
        bucket=settings.storage_bb.BUCKET_NAME,
        endpoint=settings.storage_bb.BUCKET_ENDPOINT,
        access_key_id=settings.storage_bb.APP_KEY_ID,
        secret_access_key=settings.storage_bb.APP_KEY
    )

    uploaded: bool = False

    try:
        processed_file_data = await process_media_image(storage=storage_bb, obj_key=obj_key, need_exif=True) #TODO: set exif to false

        processed_file = processed_file_data.get('compressed_file') # type: ignore
        if not processed_file:
            raise Exception('No file to use')

        mimetype: str = processed_file_data.get('mimetype') # type: ignore

        new_obj_key: str = await storage_bb.generate_file_name(folder=field, mimetype=mimetype, id=user_id, is_post=False)

        uploaded: bool = await storage_bb.upload_file_s3(object_key=new_obj_key, file=processed_file, mimetype=mimetype)

        if not uploaded:
            raise Exception(f'Upload failed for: {field} - {obj_key}')
        if uploaded:
            async with get_db_session() as session:
                profile_service = UserProfileService(session=session)
                await profile_service.update_profile(data=UserProfileEdit.model_validate({field: new_obj_key}), user_id=user_id)
        
        return {'field': field, 'obj_key': new_obj_key}
    
    except Exception:
        if uploaded and obj_key:
            await storage_bb.delete_file_s3(key=new_obj_key)
        raise