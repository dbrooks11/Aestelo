import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Spot, UserProfile
from datetime import datetime

from extensions import db
from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Rating(db.Model):
    __tablename__ = 'rating'
    __table_args__ = (UniqueConstraint('user_id', 'spot_id'), 
                      CheckConstraint('rating_choice >= 1 AND rating_choice <= 5', name='rating_range'),
                      )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id'), nullable=False)
    spot_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('spot.id', ondelete='CASCADE'), nullable=False)
    rating_choice: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user_profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="rating")
    spot: Mapped["Spot"] = relationship("Spot", back_populates='rating')

    def save(self):
        db.session.add(self)
        db.session.commit()
