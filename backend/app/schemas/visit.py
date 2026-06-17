from app.schemas.base import CamelizedBaseSchema
from pydantic import Field
from typing import Optional
from app.lib.validation import validate

class VisitSchemaBase(CamelizedBaseSchema):
    spot_id: int
    caption: Optional[str] = Field(default=None, min_length=validate.MIN_POST_DESCRIPTION_LENGTH, max_length=validate.MAX_POST_DESCRIPTION_LENGTH)
    hashtags: Optional[list[str]] = Field(default=[], min_length=validate.MIN_POST_HASHTAG_COUNT, max_length=validate.MAX_POST_HASHTAG_COUNT)


class VisitInputWithMediaSchema(VisitSchemaBase):
    media: list[str] = Field(min_length=validate.MIN_POST_MEDIA_COUNT, max_length=validate.MAX_POST_MEDIA_COUNT)


class VisitMediaInsert(CamelizedBaseSchema):
    visit_id: int
    uploaded_by: str
    sort_order: int
    media_key: str
