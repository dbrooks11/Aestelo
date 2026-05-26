from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig
from app.db.models import Visit, VisitMedia


class VisitDTO(SQLAlchemyDTO[Visit]):
    """SQLAlchemy Visit DTO.

    Includes only the minimum data needed to display a user's visits.

    Default configs:
        rename_strategy=camel.
        forbid_unknown_fields=True
    """
    config = SQLAlchemyDTOConfig(
        include={'id', 'caption','hashtags', 'total_num_of_photos','like_count', 'save_count', 
                 'share_count', 'media.sort_order','media.media_key', 'spot.id'},
        rename_strategy='camel',
        forbid_unknown_fields=True,
        max_nested_depth=1
    )
