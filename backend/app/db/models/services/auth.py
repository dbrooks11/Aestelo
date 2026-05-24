from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession
from models.auth import AuthUser

class AuthRepository(SQLAlchemyAsyncRepository[AuthUser]):
    """Repository for managing Authentication"""
    model_type=AuthUser

