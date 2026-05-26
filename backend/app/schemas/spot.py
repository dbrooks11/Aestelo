from app.schemas.base import CamelizedBaseSchema
from pydantic import Field, field_validator
from typing import Optional, Annotated
from app.lib.validation import validate

class SpotSchemaBase(CamelizedBaseSchema):
    name: str
    description: Optional[str] = Field(default=None, min_length=validate.MIN_POST_DESCRIPTION_LENGTH, max_length=validate.MAX_POST_DESCRIPTION_LENGTH)
    accessibility: bool
    hashtags: Optional[list[str]] = Field(default=[], min_length=validate.MIN_POST_HASHTAG_COUNT, max_length=validate.MAX_POST_HASHTAG_COUNT)


class SpotInputWithMediaSchema(SpotSchemaBase):
    media: list[str] = Field(min_length=validate.MIN_POST_MEDIA_COUNT, max_length=validate.MAX_POST_MEDIA_COUNT)


class SpotMediaInsert(CamelizedBaseSchema):
    spot_id: int
    uploaded_by: str
    sort_order: int
    media_key: str


