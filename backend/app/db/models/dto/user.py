from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig
from app.db.models.user import UserProfile
from app.settings import settings


class UserProfileDTO(SQLAlchemyDTO[UserProfile]):
    """SQLAlchemy Profile DTO.

    Includes only the minimum data needed for the user's profile.

    Default configs:
        rename_strategy=camel.
        forbid_unknown_fields=True
    """
    config = SQLAlchemyDTOConfig(
        include={'avatar_url', 'banner_url', 'bio', 'auth.username', 'spot_count','visit_count',
                 'follower_count', 'following_count'},
        rename_strategy='camel',
        rename_fields={'avatar_url': 'avatar', 'banner_url': 'banner'},
        forbid_unknown_fields=True
    )


class UserProfileEditDTO(SQLAlchemyDTO[UserProfile]):
    """SQLAlchemy Profile Edit DTO.

    Includes only the minimum data needed for the user to edit their profile.

    Default configs:
        rename_strategy=camel.
        forbid_unknown_fields=True
    """
    config = SQLAlchemyDTOConfig(
        include={'avatar_url', 'banner_url','bio', 'auth.username'},
        rename_strategy='camel',
        rename_fields={'avatar_url': 'avatar', 'banner_url': 'banner'},
        forbid_unknown_fields=True
    )