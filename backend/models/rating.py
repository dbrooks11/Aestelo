import uuid
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.user import UserProfile, Spot
from datetime import datetime
from extensions import db
from sqlalchemy import (ForeignKey, BigInteger, Integer, DateTime, UniqueConstraint,func)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID




class Rating(db.Model):
    __table_args__ = (UniqueConstraint('user_id', 'spot_id', name='unique_rating'),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id'), nullable=False)
    spot_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('spot.id'), nullable=False)
    rating_choice: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user_profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="rating")
    spot: Mapped["Spot"] = relationship("Spot", back_populates='rating')

    def save(self):
        db.session.add(self)
        db.session.commit()
