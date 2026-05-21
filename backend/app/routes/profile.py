from litestar.controller import Controller
from litestar.di import Provide
from typing import Annotated
from litestar import get, post, patch, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.services.user import provide_user_service, UserProfileService
from app.db.models.dto.user import UserProfileDTO, UserProfileEditDTO
from app.db.models.user import UserProfile
from app.schemas.user import UserProfileEdit
from litestar.params import Body
from litestar.enums import RequestEncodingType

class ProfileController(Controller):
    path='/profile'
    dependencies = {'profile_service': Provide(provide_user_service)}

    @get(return_dto=UserProfileDTO)
    async def profile_me(self, request: Request, profile_service: UserProfileService) -> UserProfile:
        user_id = request.user.id
        return await profile_service.get_profile_me(user_id=user_id)

    @patch('/edit', return_dto=UserProfileEditDTO)
    async def edit_profile(self, data: Annotated[UserProfileEdit, Body(media_type=RequestEncodingType.MULTI_PART)], request: Request, profile_service: UserProfileService) -> UserProfile:
        user_id = request.user.id
        return await profile_service.update_profile(user_id=user_id, data=data)