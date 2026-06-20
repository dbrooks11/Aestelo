from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import (AuthUser)
from collections.abc import AsyncGenerator
from app.schemas.auth import AuthServiceSignupSchema
from argon2 import PasswordHasher 
from litestar.di import NamedDependency

ph = PasswordHasher()
class AuthService(SQLAlchemyAsyncRepositoryService[AuthUser]):
    """Repository for managing Authentication"""
    class AuthRepo(SQLAlchemyAsyncRepository[AuthUser]):

        model_type = AuthUser
    
    repository_type = AuthRepo

    async def create_account(self, data: AuthServiceSignupSchema) -> None:
        account_structure = {
        "username": data.username,
        "email": data.email,
        "password_hash": ph.hash(data.password),
        "profile": {
            "info": {},
            "settings": {},
            "role": {},
            "subscription": {},
            "collection": [{"name": "Default", "is_default": True}]
            }
        }
        await self.create(data=account_structure)

async def provide_auth_service(db_session: NamedDependency[AsyncSession]) -> AsyncGenerator[AuthService]:
    async with AuthService.new(session=db_session) as service:
        yield service



