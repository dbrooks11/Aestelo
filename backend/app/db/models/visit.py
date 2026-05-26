
from typing import TYPE_CHECKING, Optional
import uuid
from app.db.enum_schemas import UploadStatusEnum
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
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models import CollectionItem, Likes, Spot, UserProfile



class Visit(base.BigIntAuditBase):
    __tablename__ = "visit"
    __table_args__ = (Index('ix_visit_hashtags', 'hashtags', postgresql_using='gin'))
    
    spot_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("spot.id", ondelete='CASCADE'), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("user_profile.id", ondelete='CASCADE'), 
        nullable=False, 
        index=True
    )
    
    coordinates: Mapped[Optional[Geography]] = mapped_column(
        Geography(geometry_type='POINT', srid=4326, spatial_index=True)
    )

    caption: Mapped[Optional[str]] = mapped_column(String(2500))
    hashtags: Mapped[Optional[list[str]]] = mapped_column(ARRAY(Text))
    
    like_count: Mapped[int] = mapped_column(BigInteger, default=0)
    save_count: Mapped[int] = mapped_column(BigInteger, default=0)
    share_count: Mapped[int] = mapped_column(BigInteger, default=0)

    total_num_of_photos: Mapped[Optional[int]] = mapped_column(Integer)

    num_of_edits: Mapped[int] = mapped_column(Integer, default=0)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    deleted_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True))
    
    num_reports: Mapped[int] = mapped_column(Integer, default=0)
    is_removed: Mapped[bool] = mapped_column(Boolean, default=False)
    removed_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    removed_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID)

    status: Mapped[UploadStatusEnum] = mapped_column(Enum(UploadStatusEnum), default=UploadStatusEnum.PROCESSING)

    collection_item: Mapped['CollectionItem'] = relationship(back_populates='visit')
    media: Mapped[list["VisitMedia"]] = relationship( 
        back_populates="visit", 
        cascade="all, delete-orphan"
    )
    profile: Mapped["UserProfile"] = relationship(back_populates="visit", lazy='joined')
    spot: Mapped["Spot"] = relationship(back_populates="visit", lazy="joined")
    likes: Mapped["Likes"] = relationship(back_populates='visit', lazy='selectin')
    media: Mapped[list["VisitMedia"]] = relationship(back_populates='visit' , lazy='selectin')
    

class VisitMedia(base.BigIntBase):
    __tablename__ = "visit_media"

    visit_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("visit.id", ondelete='CASCADE'), nullable=False)
    uploaded_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("user_profile.id", ondelete='CASCADE'), 
        nullable=False
    )

    sort_order: Mapped[Optional[int]] = mapped_column(Integer)
    media_key: Mapped[Optional[str]] = mapped_column(Text)

    visit: Mapped["Visit"] = relationship(back_populates="media", lazy='joined')

