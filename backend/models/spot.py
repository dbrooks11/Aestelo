import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from extensions import db
from flask import current_app
from geoalchemy2 import Geography
from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship

if TYPE_CHECKING:
    from models import CollectionItem, Rating, UserProfile, Visit
   

class Spot(db.Model):
    __tablename__ = "spot"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
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
    date_posted: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        index=True
    )
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
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    num_reports: Mapped[int] = mapped_column(Integer, default=0)
    is_removed: Mapped[bool] = mapped_column(Boolean, default=False)
    removed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(Text, default='processing')

    trending_score: Mapped[float] = column_property(
        (4 * share_count) + (2 * save_count) + ((1 * average_rating) + (1.5 * total_num_of_ratings))
    )

    user_profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="spot")
    collection_item: Mapped["CollectionItem"] = relationship("CollectionItem", back_populates="spot")
    media: Mapped[list["SpotMedia"]] = relationship(
        "SpotMedia", 
        back_populates="spot", 
        cascade="all, delete-orphan"
    )
    visit: Mapped[list["Visit"]] = relationship(
        "Visit", 
        back_populates="spot", 
        cascade="all, delete-orphan"
    )
    rating: Mapped[list["Rating"]] = relationship(
        "Rating", 
        back_populates="spot", 
        cascade="all, delete-orphan"
    )

    @classmethod
    def active(cls):
        return cls.query.filter_by(is_deleted=False, is_removed=False)

    def save(self):
        db.session.add(self)
        db.session.commit()


class SpotMedia(db.Model):
    __tablename__ = "spot_media"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    spot_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("spot.id", ondelete='CASCADE'), index=True)
    uploaded_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("user_profile.id"), 
        index=True
    )

    sort_order: Mapped[int] = mapped_column(BigInteger)
    photo_path: Mapped[str] = mapped_column(Text)
    photo_type: Mapped[str] = mapped_column(Text, default='photo')
    width: Mapped[Optional[int]] = mapped_column(Integer)
    height: Mapped[Optional[int]] = mapped_column(Integer)

    spot: Mapped["Spot"] = relationship("Spot", back_populates="media")
    user_profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="spot_media")

    def save(self):
        db.session.add(self)
        db.session.commit()

    @property
    def photo_path_url(self) -> Optional[str]:
        if not self.photo_path:
            return None
        return f"{current_app.config['R2_PUBLIC_URL']}/{self.photo_path}"