from app.schemas.base import CamelizedBaseSchema
from pydantic import Field, field_validator, FileUrl
from typing import Optional, Annotated
from app.schemas.auth import username_invalidation

class UserProfileEdit(CamelizedBaseSchema):
    """Schema to validate edits to a user's profile.
    This is also used within the UserService
    """
    avatar: Optional[str] = Field(default=None)
    banner: Optional[str] = Field(default=None)
    username: Annotated[Optional[str], Field(default=None)]
    bio: Optional[str] = Field(default=None)

    @field_validator('username', mode='after')
    @classmethod
    def validate_username(cls, value):
        return username_invalidation(value)
    
    @field_validator('bio', mode='after')
    def validate_bio(cls ,value):
        if '\x00' in value:
            raise ValueError('Bio contains invalid characters')
        return value