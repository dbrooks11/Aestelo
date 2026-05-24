
from typing import TYPE_CHECKING, Optional
import uuid
from app.db.schemas import MediaTypeEnum, UploadStatusEnum
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
    String,
    Text,
    cast,
)
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship

if TYPE_CHECKING:
    from models import CollectionItem, Rating, UserProfile, Visit
   

class Spot(base.BigIntAuditBase):
    __tablename__ = "spot"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("user_profile.id"), 
        nullable=False, 
        index=True
    )

    name: Mapped[str] = mapped_column(Text)
    coordinates: Mapped[Optional[Geography]] = mapped_column(
        Geography(geometry_type='POINT', srid=4326, spatial_index=True)
    )
    latitude: Mapped[int] = column_property(ST_Y(cast(coordinates, Geometry)))
    longitude: Mapped[int] = column_property(ST_X(cast(coordinates, Geometry)))

    description: Mapped[Optional[str]] = mapped_column(Text)
    total_num_of_photos: Mapped[Optional[int]] = mapped_column(Integer)

    visit_count: Mapped[int] = mapped_column(Integer, default=0) 
    average_rating: Mapped[float] = mapped_column(Float, default=0.0)
    total_num_of_ratings: Mapped[int] = mapped_column(Integer, default=0)

    save_count: Mapped[int] = mapped_column(Integer, default=0)
    share_count: Mapped[int] = mapped_column(Integer, default=0)
    
    hashtags: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String)) 
    accessibility: Mapped[bool] = mapped_column(Boolean, default=False) 
    num_of_edits: Mapped[int] = mapped_column(Integer, default=0)
    
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    num_reports: Mapped[int] = mapped_column(Integer, default=0)
    is_removed: Mapped[bool] = mapped_column(Boolean, default=False)
    removed_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(Text, default=UploadStatusEnum.PROCESSING)

    profile: Mapped["UserProfile"] = relationship(back_populates="spot")
    collection_item: Mapped["CollectionItem"] = relationship(back_populates="spot")
    media: Mapped[list["SpotMedia"]] = relationship(
        back_populates="spot", 
        cascade="all, delete-orphan"
    )
    visit: Mapped[list["Visit"]] = relationship(
        back_populates="spot", 
        cascade="all, delete-orphan"
    )
    rating: Mapped[list["Rating"]] = relationship(
        back_populates="spot", 
        cascade="all, delete-orphan"
    )

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
    media_type: Mapped[str] = mapped_column(Text, default=MediaTypeEnum.PHOTO) 
    width: Mapped[Optional[int]] = mapped_column(Integer)
    height: Mapped[Optional[int]] = mapped_column(Integer)

    spot: Mapped["Spot"] = relationship(back_populates="media")