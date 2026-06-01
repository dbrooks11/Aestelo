from app.schemas.base import CamelizedBaseSchema

class FileUploadSchema(CamelizedBaseSchema):
    filename: str
    content_type: str