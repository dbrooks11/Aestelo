from app.schemas.base import CamelizedBaseSchema
import re
from typing import Annotated, Optional
from typing_extensions import Self
from pydantic import EmailStr,model_validator, Field, field_validator
from app.lib.validation import (PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH, EMAIL_MIN_LENGTH,
                                EMAIL_MAX_LENGTH, USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH, RESERVED_USERNAMES,
                                EMAIL_BLOCKED_DOMAINS, EMAIL_BLOCKED_PATTERNS, USERNAME_VALID_PATTERN)


def username_invalidation(value):
    if value:
        if value in RESERVED_USERNAMES or not re.match(USERNAME_VALID_PATTERN, value):
            raise ValueError('Invalid username')
        
        if USERNAME_MIN_LENGTH > len(value) > USERNAME_MAX_LENGTH:
            raise ValueError(f'Username must be {USERNAME_MIN_LENGTH} - {USERNAME_MAX_LENGTH} characters')
    return value


class AuthBase(CamelizedBaseSchema):
    username: Annotated[Optional[str], Field(default=None, min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH)]
    email: Annotated[EmailStr, Field(min_length=EMAIL_MIN_LENGTH, max_length=EMAIL_MAX_LENGTH)]
    password: Annotated[str, Field(min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH)]
    
    @field_validator('email', mode='after')
    @classmethod
    def validate_email(cls, value):
        if value in EMAIL_BLOCKED_DOMAINS:
            raise ValueError('Invalid email domain')
        
        if not value or value in EMAIL_BLOCKED_DOMAINS or value in EMAIL_BLOCKED_PATTERNS:
            raise ValueError('Invalid email')
            
        return value

class LoginRequest(AuthBase):

    @model_validator(mode='after')
    def check_email_and_username(self) -> Self:
        if self.email and self.username:
            raise ValueError('Only Username or Email is allowed')
        
        if not self.email and not self.username:
            raise ValueError('Email or Username is required')
        
        return self
    
    @field_validator('username', mode='after')
    @classmethod
    def validate_username(cls, value):
        return username_invalidation(value)

class SignupRequest(AuthBase):
    confirm_password: Annotated[str, Field(min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH)]
    
    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self