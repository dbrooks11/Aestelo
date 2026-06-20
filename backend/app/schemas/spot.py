from pydantic import Field

from app.lib.validation import validate
from app.schemas.base import CamelizedBaseSchema


class SpotSchemaBase(CamelizedBaseSchema):
    name: str
    description: str | None = Field(
        default=None,
        min_length=validate.MIN_POST_DESCRIPTION_LENGTH,
        max_length=validate.MAX_POST_DESCRIPTION_LENGTH,
    )
    accessibility: bool
    hashtags: list[str] | None = Field(
        default=[],
        min_length=validate.MIN_POST_HASHTAG_COUNT,
        max_length=validate.MAX_POST_HASHTAG_COUNT,
    )


class SpotInputWithMediaSchema(SpotSchemaBase):
    media: list[str] = Field(
        min_length=validate.MIN_POST_MEDIA_COUNT,
        max_length=validate.MAX_POST_MEDIA_COUNT,
    )


class SpotMediaInsert(CamelizedBaseSchema):
    spot_id: int
    uploaded_by: str
    sort_order: int
    media_key: str


class SpotRatingSchema(CamelizedBaseSchema):
    rating: int = Field(ge=1, le=5)


class SpotRatingGetData(CamelizedBaseSchema):
    user_id: str
    spot_id: int
