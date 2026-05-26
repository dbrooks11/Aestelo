from litestar.controller import Controller
from litestar.di import Provide
from typing import Annotated, Any
from litestar import get, post, patch, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.services.user import provide_user_service, UserProfileService
from app.db.models.dto.user import UserProfileDTO, UserProfileEditDTO
from app.db.models.user import UserProfile
from app.schemas.user import UserProfileEditSchema
from app.plugins import plugins
from app.settings import settings
from app.utils.storage import ObjectStorage


class ProfileController(Controller):
    path='/profile'
    dependencies = {'profile_service': Provide(provide_user_service)}

    @get(return_dto=UserProfileDTO)
    async def profile_me(self, request: Request, profile_service: UserProfileService) -> UserProfile:
        user_id = request.user.id
        return await profile_service.get_profile_me(user_id=user_id)

    @patch('/edit', return_dto=UserProfileEditDTO)
    async def edit_profile(self, data: UserProfileEditSchema, request: Request, profile_service: UserProfileService) -> UserProfile:
        user_id = request.user.id
        storage = ObjectStorage(
            bucket=settings.storage_bb.BUCKET_NAME,
            endpoint=settings.storage_bb.BUCKET_ENDPOINT,
            access_key_id=settings.storage_bb.APP_KEY_ID,
            secret_access_key=settings.storage_bb.APP_KEY
        )
        data_dict = data.model_dump(exclude_none=True, exclude_unset=True)
        profile_media = {
            'avatar': data_dict.pop('avatar', None),
            'banner': data_dict.pop('banner', None)
        }

        profile = await profile_service.get_profile_me(user_id=user_id)
        queue = plugins.saq.get_queue('profile_processing')

        items = []
        for field, obj_key in profile_media.items():
            if obj_key:
                items.append({'field': field, 'obj_key': obj_key, 'prev_key': getattr(profile, field, None), 'user_id': user_id, 'storage': storage})
        results: list[Any] = []
        if items:
            results = await queue.map(
                        "process_profile_media",
                        items,
                        retries=3,
                        timeout=30,
                        retry_delay=1,
                        retry_backoff=True
                    )
        updated_profile = await profile_service.update_profile(user_id=user_id, data=UserProfileEditSchema.model_validate(data_dict))
        
        if results:
            for result in results:
                for field, item in result.items():
                    if field in updated_profile:
                        setattr(updated_profile, field, item)
        
        return updated_profile

