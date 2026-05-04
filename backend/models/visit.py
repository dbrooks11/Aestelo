import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from extensions import db
from geoalchemy2 import Geography
from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models import CollectionItem, Spot, UserProfile, Likes

class Visit(db.Model):
    __tablename__ = "visit"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    
    # Use strings for ForeignKeys to break circular imports
    spot_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("spot.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("user_profile.id"), 
        nullable=False, 
        index=True
    )
    
    coordinates: Mapped[Optional[Geography]] = mapped_column(
        Geography(geometry_type='POINT', srid=4326, spatial_index=True)
    )

    music_track_id: Mapped[Optional[str]] = mapped_column(Text, ForeignKey("music_track.id"), nullable=True)
    caption: Mapped[Optional[str]] = mapped_column(Text) # limit to 200 chars in app logic
    hashtags: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    date_posted: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    
    like_count: Mapped[int] = mapped_column(BigInteger, default=0)
    save_count: Mapped[int] = mapped_column(BigInteger, default=0)
    share_count: Mapped[int] = mapped_column(BigInteger, default=0)

    total_num_of_photos: Mapped[Optional[int]] = mapped_column(Integer)

    num_of_edits: Mapped[int] = mapped_column(Integer, default=0)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    deleted_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True))
    
    num_reports: Mapped[int] = mapped_column(Integer, default=0)
    is_removed: Mapped[bool] = mapped_column(Boolean, default=False)
    removed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    removed_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID)

    status: Mapped[str] = mapped_column(Text, default='processing')

    collection_item: Mapped['CollectionItem'] = relationship('CollectionItem', back_populates='visit')
    media: Mapped[list["VisitMedia"]] = relationship(
        "VisitMedia", 
        back_populates="visit", 
        cascade="all, delete-orphan"
    )
    user_profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="visit")
    spot: Mapped["Spot"] = relationship("Spot", back_populates="visit")
    likes: Mapped["Likes"] = relationship('Likes', back_populates='visit')
    
    @classmethod
    def active(cls):
        return cls.query.filter_by(is_deleted=False, is_removed=False)

    def save(self):
        db.session.add(self)
        db.session.commit()


class VisitMedia(db.Model):
    __tablename__ = "visit_media"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    visit_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("visit.id", ondelete='CASCADE'), nullable=False)
    uploaded_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("user_profile.id"), 
        nullable=False
    )

    sort_order: Mapped[Optional[int]] = mapped_column(Integer)
    photo_path: Mapped[Optional[str]] = mapped_column(Text)
    photo_type: Mapped[str] = mapped_column(Text, default='photo') 
    width: Mapped[Optional[int]] = mapped_column(Integer)
    height: Mapped[Optional[int]] = mapped_column(Integer)

    visit: Mapped["Visit"] = relationship("Visit", back_populates="media")
    user_profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="visit_media")

    def save(self):
        db.session.add(self)
        db.session.commit()