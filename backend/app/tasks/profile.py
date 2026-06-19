from saq.types import Context
from app.utils.media import process_media_image
from app.services.user import UserProfileService
from app.db.session import get_db_session
from litestar_saq import monitored_job
from app.utils.storage import storage, storage_private



@monitored_job()
async def process_profile_media(ctx: Context, *, user_id: str, field: str, obj_key: str, prev_key: str):
    uploaded: bool = False
    new_obj_key: str = ''

    try:
        processed_file_data = await process_media_image(storage=storage_private, obj_key=obj_key, need_exif=False, need_colors=False)

        processed_file = processed_file_data.get('compressed_file')
        original_mimetype: str | None = processed_file_data.get('original_mimetype')
        mimetype: str | None = processed_file_data.get('new_mimetype')

        if not processed_file or not original_mimetype or not mimetype:
            raise Exception('Invalid file')

        valid_extension = await storage.verify_file_type(mimetype=original_mimetype, is_post=False)
        new_obj_key = await storage.generate_file_name(folder=field, id=user_id, extension=valid_extension)

        uploaded = await storage.upload_file_s3(object_key=new_obj_key, file=processed_file, mimetype=mimetype)

        if not uploaded:
            raise Exception(f'Upload failed for: {field} - {obj_key}')
        
        updated = None
        async with get_db_session() as session:
            profile_service = UserProfileService(session=session)
            updated = await profile_service.update(data={field: new_obj_key}, item_id=user_id)
        if prev_key and updated:
            await storage.delete_file_s3(key=prev_key)
        
        return {field: new_obj_key}
    
    except Exception:
        if uploaded and new_obj_key:
            await storage.delete_file_s3(key=new_obj_key)
        raise