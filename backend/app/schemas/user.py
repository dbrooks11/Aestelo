from app.schemas.base import CamelizedBaseSchema
from pydantic import Field, field_validator
from typing import Optional, Annotated
from app.schemas.auth import username_invalidation
from app.lib.validation import validate

class UserProfileEditSchema(CamelizedBaseSchema):
    """Schema to validate edits to a user's profile.
    This is also used within the UserService
    """
    username: Annotated[Optional[str], Field(default=None, min_length=validate.USERNAME_MIN_LENGTH, max_length=validate.USERNAME_MAX_LENGTH)]
    bio: Optional[str] = None

    @field_validator('username', mode='after')
    @classmethod
    def validate_username(cls, value):
        return username_invalidation(value)
    
    @field_validator('bio', mode='after')
    def validate_bio(cls ,value):
        if '\x00' in value:
            raise ValueError('Bio contains invalid characters')
        return value
    
class UserProfileEditMediaSchema(CamelizedBaseSchema):
    avatar: Optional[str] = Field(default=None)
    banner: Optional[str] = Field(default=None)