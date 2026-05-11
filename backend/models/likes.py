import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from app.extensions  import db
from sqlalchemy import BigInteger, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models import UserProfile, Visit



class Likes(db.Model):
    __tablename__ = 'likes'
    __table_args__ = (UniqueConstraint('user_id', 'visit_id'),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id'), nullable=False)
    visit_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('visit.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user_profile: Mapped["UserProfile"] = relationship('UserProfile', back_populates='likes')
    visit: Mapped["Visit"] = relationship('Visit', back_populates='likes')