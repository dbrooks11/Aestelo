import uuid
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from models import UserProfile
from datetime import datetime
from extensions import db
from sqlalchemy import (ForeignKey, BigInteger, Text, DateTime, Boolean,UniqueConstraint, func)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID


class Collection(db.Model):
    __table_args__ = (UniqueConstraint('user_id', 'name'),)
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id'), index=True)
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

    user_profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="collection")


class CollectionItem(db.Model):
    __table_args__ = (UniqueConstraint('collection_id', 'spot_id'),
                      UniqueConstraint('collection_id', 'visit_id'),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    collection_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('collection.id'), nullable=False)
    spot_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('spot.id'), nullable=True)
    visit_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('visit.id'), nullable=True)
    saved_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    saved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    