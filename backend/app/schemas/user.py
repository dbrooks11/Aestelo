from app.schemas.base import CamelizedBaseSchema
from litestar.datastructures.upload_file import UploadFile
from pydantic import Field, field_validator
import re
from typing import Optional, Annotated
from app.lib.validation import (USERNAME_MAX_LENGTH, USERNAME_MIN_LENGTH, USERNAME_VALID_PATTERN, RESERVED_USERNAMES)
from app.schemas.auth import username_invalidation

class UserProfileEdit(CamelizedBaseSchema):
    avatar: Optional[UploadFile] = Field(default=None)
    banner: Optional[UploadFile] = Field(default=None)
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