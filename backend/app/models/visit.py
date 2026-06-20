
from typing import TYPE_CHECKING
import uuid
from app.db.enums import UploadStatusEnum
from geoalchemy2 import Geography
from advanced_alchemy.extensions.litestar import base
from sqlalchemy import (
    Index,
    ARRAY,
    UUID,
    BigInteger,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from advanced_alchemy.types import DateTimeUTC

if TYPE_CHECKING:
    from app.models import CollectionItem, Likes, Spot, UserProfile



class Visit(base.BigIntAuditBase):
    __tablename__ = "visit"
    __table_args__ = (Index('ix_visit_hashtags', 'hashtags', postgresql_using='gin'),)
    
    spot_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("spot.id", ondelete='CASCADE'), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("user_profile.id", ondelete='CASCADE'), 
        nullable=False, 
        index=True
    )
    
    coordinates: Mapped[Geography | None] = mapped_column(
        Geography(geometry_type='POINT', srid=4326, spatial_index=True)
    )

    caption: Mapped[str | None] = mapped_column(String(2500))
    hashtags: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    
    like_count: Mapped[int] = mapped_column(BigInteger, default=0)
    save_count: Mapped[int] = mapped_column(BigInteger, default=0)
    share_count: Mapped[int] = mapped_column(BigInteger, default=0)

    total_num_of_photos: Mapped[int | None] = mapped_column(Integer)

    num_of_edits: Mapped[int] = mapped_column(Integer, default=0)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[DateTime | None] = mapped_column(DateTimeUTC)
    deleted_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    
    num_reports: Mapped[int] = mapped_column(Integer, default=0)
    is_removed: Mapped[bool] = mapped_column(Boolean, default=False)
    removed_at: Mapped[DateTime | None] = mapped_column(DateTimeUTC)
    removed_by: Mapped[uuid.UUID | None] = mapped_column(UUID)

    status: Mapped[UploadStatusEnum] = mapped_column(Enum(UploadStatusEnum), default=UploadStatusEnum.PROCESSING)

    collection_item: Mapped['CollectionItem'] = relationship(back_populates='visit')
    media: Mapped[list["VisitMedia"]] = relationship( 
        cascade="all, delete-orphan",
        lazy='selectin'
    )
    profile: Mapped["UserProfile"] = relationship(back_populates="visit", lazy='joined')
    spot: Mapped["Spot"] = relationship(back_populates="visit", lazy="joined")
    likes: Mapped["Likes"] = relationship(back_populates='visit', lazy='selectin')
    

class VisitMedia(base.BigIntBase):
    __tablename__ = "visit_media"

    visit_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("visit.id", ondelete='CASCADE'), nullable=False)
    uploaded_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("user_profile.id", ondelete='CASCADE'), 
        nullable=False
    )

    sort_order: Mapped[int | None] = mapped_column(Integer)
    media_key: Mapped[str | None] = mapped_column(Text)


