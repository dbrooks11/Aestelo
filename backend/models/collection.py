import uuid
from typing import TYPE_CHECKING, Optional

from flask import current_app

if TYPE_CHECKING:
    from models import Spot, UserProfile, Visit
from datetime import datetime

from .extensions import db
from sqlalchemy import (
    ARRAY,
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Collection(db.Model):
    __tablename__ = 'collection'
    __table_args__ = (UniqueConstraint('user_id', 'name'),)
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    preview_thumbnails: Mapped[Optional[list[str]]] = mapped_column(ARRAY(Text), default=[])
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id', ondelete='CASCADE'), index=True)
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

    user_profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="collection")
    collection_item: Mapped[list["CollectionItem"]] = relationship("CollectionItem", back_populates="collection")

    @property
    def preview_thumbnail_urls(self):
        if not self.preview_thumbnails or len(self.preview_thumbnails) == 0:
            return None
        
        urls = []
        for thumbnail in self.preview_thumbnails:
            urls.append(f"{current_app.config['R2_PUBLIC_URL']}/{thumbnail}")
        
        return urls


class CollectionItem(db.Model):
    __tablename__ = 'collection_item'
    __table_args__ = (UniqueConstraint('collection_id', 'spot_id'),
                      UniqueConstraint('collection_id', 'visit_id'),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    collection_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('collection.id', ondelete='CASCADE'), nullable=False)
    spot_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('spot.id', ondelete='CASCADE'), nullable=True)
    visit_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('visit.id', ondelete='CASCADE'), nullable=True)
    saved_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    saved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    collection: Mapped["Collection"] = relationship("Collection", back_populates='collection_item')
    spot: Mapped["Spot"] = relationship("Spot", back_populates='collection_item')
    visit: Mapped['Visit'] = relationship('Visit', back_populates='collection_item')