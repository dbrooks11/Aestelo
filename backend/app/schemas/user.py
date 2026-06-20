from typing import Annotated

from pydantic import Field, field_validator

from app.lib.validation import validate
from app.schemas.auth import username_invalidation
from app.schemas.base import CamelizedBaseSchema


class UserProfileEditSchema(CamelizedBaseSchema):
    """Schema to validate edits to a user's profile.
    This is also used within the UserService
    """

    username: Annotated[
        str | None,
        Field(
            default=None,
            min_length=validate.USERNAME_MIN_LENGTH,
            max_length=validate.USERNAME_MAX_LENGTH,
        ),
    ]
    bio: str | None = None

    @field_validator("username", mode="after")
    @classmethod
    def validate_username(cls, value):
        return username_invalidation(value)

    @field_validator("bio", mode="after")
    def validate_bio(cls, value):
        if "\x00" in value:
            raise ValueError("Bio contains invalid characters")
        return value


class UserProfileEditMediaSchema(CamelizedBaseSchema):
    avatar: str | None = Field(default=None)
    banner: str | None = Field(default=None)
