from litestar.controller import Controller
from litestar import Request, post
from app.lib.validation import validate
from app.schemas.s3 import FileUploadSchema
from app.utils.storage import storage_private
from litestar.params import JSONBody


class ObjectStorageController(Controller):
    path = "/s3"

    @post("/presign-urls")
    async def presign_urls(
        self, data: JSONBody[list[FileUploadSchema]], request: Request
    ) -> list[dict[str, str]]:
        if len(data) > validate.MAX_NUM_FILES_POST:
            raise Exception("Too many files")

        user_id: str = request.user.id

        presigned_urls: list = []
        for file in data:
            extension = await storage_private.verify_file_type(
                mimetype=file.content_type, is_post=False
            )
            obj_key = await storage_private.generate_file_name(
                extension=extension, id=user_id
            )
            presigned_urls.append(
                await storage_private.generate_presigned_put_url(
                    mimetype=file.content_type, obj_key=obj_key
                )
            )

        return presigned_urls
