from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models import Spot


class SpotDTO(SQLAlchemyDTO[Spot]):
    """SQLAlchemy Spot DTO.

    Includes only the minimum data needed to display a user's spots.

    Default configs:
        rename_strategy=camel.
        forbid_unknown_fields=True
    """

    config = SQLAlchemyDTOConfig(
        include={
            "id",
            "name",
            "description",
            "profile.auth.username",
            "accessibility",
            "hashtags",
            "latitude",
            "longitude",
            "total_num_of_photos",
            "visit_count",
            "average_rating",
            "total_num_of_ratings",
            "save_count",
            "share_count",
            "media.0.sort_order",
            "media.0.media_url",
            "visited",
            "rated",
            "saved",
        },
        rename_strategy="camel",
        forbid_unknown_fields=True,
        max_nested_depth=2,
    )
