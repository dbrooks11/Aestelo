from litestar.controller import Controller
from litestar.datastructures import UploadFile, URL
from litestar import get, Request, post
from typing import Annotated
from litestar.enums import RequestEncodingType
from litestar.params import Body
from app.utils.storage import ObjectStorage
from app.settings import settings

MAX_NUM_OF_FILES=10
MAX_FILE_SIZE = 10 * 1024 * 1024  #20MB

class ObjectStorageController(Controller):
    path='/s3'

    @post('/presign-urls')
    async def presign_urls(self, data: Annotated[list[UploadFile], Body(media_type=RequestEncodingType.MULTI_PART)], request:Request) -> list[dict[str,str]]:
        if len(data) > MAX_NUM_OF_FILES:
            raise Exception('Too many files')
        
        user_id: str = request.user.id
 
        storage = ObjectStorage(
            bucket=settings.storage_bb.BUCKET_NAME,
            endpoint=settings.storage_bb.BUCKET_ENDPOINT,
            access_key_id=settings.storage_bb.APP_KEY_ID,
            secret_access_key=settings.storage_bb.APP_KEY
        )

        presigned_urls: list = []
        for file in data:  
            print(file.headers)
            presigned_urls.append(await storage.generate_presigned_put_url(mimetype=file.content_type, user_id=user_id))

        return presigned_urls