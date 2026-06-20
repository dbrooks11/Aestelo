from litestar.controller import Controller
from litestar.exceptions import ValidationException
from litestar.di import Provide
from litestar import get, patch, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.user import provide_user_service, UserProfileService
from app.dto.user import UserProfileDTO, UserProfileEditInfoDTO, UserProfileEditMediaDTO
from app.models import UserProfile, AuthUser
from app.schemas.user import UserProfileEditSchema, UserProfileEditMediaSchema
from app.plugins import plugins
from app.lib.validation import validate
from litestar.di import NamedDependency
from litestar.params import JSONBody


class UserController(Controller):
    path = "/profile"
    dependencies = {"profile_service": Provide(provide_user_service)}

    @get(return_dto=UserProfileDTO)
    async def profile_me(
        self, request: Request, profile_service: NamedDependency[UserProfileService]
    ) -> UserProfile:
        user_id: str = request.user.id

        return await profile_service.get_profile_me(user_id=user_id)

    @patch("/edit", return_dto=UserProfileEditInfoDTO)
    async def edit_profile(
        self,
        db_session: NamedDependency[AsyncSession],
        data: JSONBody[UserProfileEditSchema],
        request: Request,
        profile_service: NamedDependency[UserProfileService],
    ) -> UserProfile:
        user_id: str = request.user.id
        stmt = select(1).where(
            AuthUser.username == data.username, AuthUser.id != user_id
        )
        username_exists = await db_session.scalar(stmt)
        if username_exists:
            raise ValidationException(
                f"Username '{data.username}' is already taken", status_code=409
            )
        updated_profile = await profile_service.update_profile(
            user_id=user_id, data=data
        )
        return updated_profile

    @patch("/edit-media", return_dto=UserProfileEditMediaDTO)
    async def edit_profile_media(
        self,
        data: JSONBody[UserProfileEditMediaSchema],
        request: Request,
        profile_service: NamedDependency[UserProfileService],
    ) -> UserProfile | None:
        user_id: str = request.user.id
        if data.model_dump(exclude_none=True):
            profile = await profile_service.get_profile_me(user_id=user_id)
            queue = plugins.saq.get_queue("profile_processing")
            items: list = []
            for field, obj_key in data:
                if obj_key:
                    items.append(
                        {
                            "field": field,
                            "obj_key": obj_key,
                            "prev_key": getattr(profile, field, None),
                            "user_id": user_id,
                        }
                    )
            if len(items) > validate.MAX_NUM_FILES_PROFILE:
                raise ValidationException("Too many files")
            result: list[dict[str, str]] = []
            if items:
                result = await queue.map(
                    "process_profile_media",
                    items,
                    retries=3,
                    timeout=30,
                    retry_delay=1,
                    retry_backoff=True,
                )
            flatted_data: dict | None = (
                {key: value for dic in result for key, value in dic.items()}
                if result
                else None
            )
            return UserProfile(**flatted_data) if flatted_data else None
