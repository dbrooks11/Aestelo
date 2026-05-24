from sqlalchemy import UUID
from typing import Union
from advanced_alchemy.repository import SQLAlchemyAsyncRepository, ErrorMessages
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import UserProfile
from app.schemas.user import UserProfileEdit
from collections.abc import AsyncGenerator
from sqlalchemy.orm import selectinload, joinedload

class UserProfileService(SQLAlchemyAsyncRepositoryService[UserProfile]):
    """Handles database operations for users"""

    class UserProfileRepository(SQLAlchemyAsyncRepository[UserProfile]):
        """Repository for managing User profile information"""
        model_type=UserProfile

    repository_type = UserProfileRepository
    
    async def get_profile_me(self, user_id: str) -> UserProfile:
        return await self.get(item_id=user_id, 
                              error_messages=ErrorMessages({
                                'not_found': 'Failed to fetch profile'
                            }),
                            load=[joinedload(UserProfile.auth)]
                        )

    async def update_profile(self, user_id: str, data: UserProfileEdit) -> UserProfile:
        profile = await self.get(user_id, load=[selectinload(UserProfile.auth)])

        username = data.username
        if username and username != profile.auth.username:
            profile.auth.username = username

        for key, value in data:
            if getattr(profile, key, None) != value:
                setattr(profile, key, value)

        return await self.update(data=profile, error_messages=ErrorMessages(
            {'other': 'Failed to update profile'}
        ))

    async def delete_profile(self, user_id: str) -> UserProfile:
        return await self.delete(user_id)



async def provide_user_service(db_session: AsyncSession) -> AsyncGenerator[UserProfileService, None]:
    async with UserProfileService.new(session=db_session) as service:
        yield service
