from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models.user import UserProfile


class UserProfileDTO(SQLAlchemyDTO[UserProfile]):
    """SQLAlchemy Profile DTO.

    Includes only the minimum data needed for the user's profile.

    Default configs:
        rename_strategy=camel.
        forbid_unknown_fields=True
    """

    config = SQLAlchemyDTOConfig(
        include={
            "avatar_url",
            "banner_url",
            "bio",
            "auth.username",
            "spot_count",
            "visit_count",
            "follower_count",
            "following_count",
            "created_at",
        },
        rename_strategy="camel",
        rename_fields={"avatar_url": "avatar", "banner_url": "banner"},
        forbid_unknown_fields=True,
    )


class UserProfileEditInfoDTO(SQLAlchemyDTO[UserProfile]):
    """SQLAlchemy Profile Edit DTO.

    Includes only the minimum data needed for the user to edit their profile info.

    Default configs:
        rename_strategy=camel.
        forbid_unknown_fields=True
    """

    config = SQLAlchemyDTOConfig(
        include={"bio", "auth.username"},
        rename_strategy="camel",
        forbid_unknown_fields=True,
    )


class UserProfileEditMediaDTO(SQLAlchemyDTO[UserProfile]):
    """SQLAlchemy Profile Edit Media DTO.

    Includes only the minimum data needed for the user to edit the media on their profile.

    Default configs:
        rename_strategy=camel.
        forbid_unknown_fields=True
    """

    config = SQLAlchemyDTOConfig(
        include={"avatar_url", "banner_url"},
        rename_strategy="camel",
        rename_fields={"avatar_url": "avatar", "banner_url": "banner"},
        forbid_unknown_fields=True,
    )
