
from typing import TYPE_CHECKING, Optional
import uuid
from app.db.enums import UploadStatusEnum
from geoalchemy2 import Geography, Geometry
from geoalchemy2.functions import ST_X, ST_Y
from advanced_alchemy.extensions.litestar import base
from sqlalchemy import (
    ARRAY,
    UUID,
    BigInteger,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Enum,
    Text,
    cast,
    String,
    Index,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship, query_expression
from app.lib.validation import validate
from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKBElement
from typing import cast
from shapely.geometry import Point
from advanced_alchemy.types import DateTimeUTC
from sqlalchemy.ext.hybrid import hybrid_property
from app.settings import settings

if TYPE_CHECKING:
    from app.models import CollectionItem, Rating, UserProfile, Visit
   

class Spot(base.BigIntAuditBase):
    __tablename__ = "spot"
    __table_args__= (Index('ix_spot_color_palette', 'color_palette', postgresql_using='gin'),
                     Index('ix_spot_hashtags', 'hashtags', postgresql_using='gin'),)

    visited: Mapped[Optional[bool]] = query_expression()
    rated: Mapped[Optional[bool]] = query_expression()
    saved: Mapped[Optional[bool]] = query_expression()

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("user_profile.id"), 
        nullable=False, 
        index=True
    )

    name: Mapped[str] = mapped_column(Text)
    coordinates: Mapped[Optional[WKBElement]] = mapped_column(
        Geography(geometry_type='POINT', srid=4326, spatial_index=True)
    )
    color_palette: Mapped[Optional[ARRAY]] = mapped_column(ARRAY(Text))

    description: Mapped[Optional[str]] = mapped_column(String(validate.MAX_POST_DESCRIPTION_LENGTH))
    total_num_of_photos: Mapped[Optional[int]] = mapped_column(Integer)

    visit_count: Mapped[int] = mapped_column(Integer, default=0) 
    average_rating: Mapped[float] = mapped_column(Float, default=0.0)
    total_num_of_ratings: Mapped[int] = mapped_column(Integer, default=0)

    save_count: Mapped[int] = mapped_column(Integer, default=0)
    share_count: Mapped[int] = mapped_column(Integer, default=0)
    
    hashtags: Mapped[Optional[list[str]]] = mapped_column(ARRAY(Text)) 
    accessibility: Mapped[bool] = mapped_column(Boolean, default=False) 
    num_of_edits: Mapped[int] = mapped_column(Integer, default=0)
    
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(DateTimeUTC)
    num_reports: Mapped[int] = mapped_column(Integer, default=0)
    is_removed: Mapped[bool] = mapped_column(Boolean, default=False)
    removed_at: Mapped[Optional[DateTime]] = mapped_column(DateTimeUTC)
    status: Mapped[Enum] = mapped_column(Enum(UploadStatusEnum), default=UploadStatusEnum.PROCESSING)

    profile: Mapped["UserProfile"] = relationship(back_populates="spot", lazy='joined')
    collection_item: Mapped["CollectionItem"] = relationship(back_populates="spot", lazy='selectin')
    media: Mapped[list["SpotMedia"]] = relationship(
        cascade="all, delete-orphan",
        lazy='selectin',
    )
    visit: Mapped[list["Visit"]] = relationship(
        back_populates="spot", 
        cascade="all, delete-orphan",
        lazy='selectin'
    )
    rating: Mapped[list["Rating"]] = relationship(
        back_populates="spot", 
        cascade="all, delete-orphan",
        lazy='selectin'
    )

    @hybrid_property
    def longitude(self) -> float:
        """Extracts X coordinate via Shapely in Python."""
        if self.coordinates is not None:
            point = cast(Point, to_shape(self.coordinates))
            return point.x
        return 0.0

    @hybrid_property
    def latitude(self) -> float:
        """Extracts Y coordinate via Shapely in Python."""
        if self.coordinates is not None:
            point = cast(Point, to_shape(self.coordinates))
            return point.y
        return 0.0

class SpotMedia(base.BigIntBase):
    __tablename__ = "spot_media"

    spot_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("spot.id", ondelete='CASCADE'), index=True)
    uploaded_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("user_profile.id"), 
        index=True
    )

    sort_order: Mapped[int] = mapped_column(BigInteger)
    media_key: Mapped[Optional[str]] = mapped_column(Text)


    @hybrid_property
    def media_url(self) -> str | None:
        if self.media_key:
            return f"https://{settings.storage.SUB_DOMAIN}/{self.media_key}"
        return None