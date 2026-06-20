from advanced_alchemy.repository import SQLAlchemyAsyncRepository, ErrorMessages
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import UserProfile, AuthUser
from app.schemas.user import UserProfileEditSchema
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from sqlalchemy.orm import joinedload
from app.services.auth import AuthService
from advanced_alchemy.filters import ExistsFilter
from litestar.exceptions import ValidationException
from litestar.di import NamedDependency

class UserProfileService(SQLAlchemyAsyncRepositoryService[UserProfile]):
    """Handles database operations for users"""

    class UserProfileRepo(SQLAlchemyAsyncRepository[UserProfile]):
        """Repository for managing User profile information"""
        model_type=UserProfile

    repository_type = UserProfileRepo
    auth_service = AuthService
    
    async def get_profile_me(self, user_id: str) -> UserProfile:
        return await self.get(item_id=user_id, 
                              error_messages=ErrorMessages({
                                'not_found': 'Failed to fetch profile'
                            }),
                            load=[joinedload(UserProfile.auth)]
                        )

    async def update_profile(self, user_id: str, data: UserProfileEditSchema) -> UserProfile:
        profile = await self.get(user_id)

        temp_data: dict = {}
        username = data.username
        if username and username != profile.auth.username:       
            profile.auth.username = username
        
        data_dump: dict = data.model_dump(exclude={'username'}, exclude_none=True)
        for key, value in data_dump.items():
            prev_value = getattr(profile, key, None)
            if prev_value != value:
                temp_data[key] = value
        
        return await self.update(data=temp_data, item_id=user_id, error_messages=ErrorMessages(
                {'other': 'Failed to update profile'}
            ))

    async def delete_profile(self, user_id: str) -> UserProfile:
        return await self.delete(user_id)



async def provide_user_service(db_session: NamedDependency[AsyncSession]) -> AsyncGenerator[UserProfileService, None]:
    async with UserProfileService.new(session=db_session) as service:
        yield service
