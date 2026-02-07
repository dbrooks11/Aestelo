import uuid
from typing import TYPE_CHECKING

from extensions import db
from sqlalchemy import (
    BigInteger,
    ForeignKey,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models import UserProfile



class Follow(db.Model):
    __tablename__ = "follow"
    __table_args__ = (Index(None, "follower_id", "following_id", unique=True),)
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    follower_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id'), nullable=False) #who is following
    following_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id'), nullable=False) # who is being followed

    follower: Mapped["UserProfile"] = relationship("UserProfile", foreign_keys="Follow.follower_id", back_populates="follower")
    following: Mapped["UserProfile"] = relationship("UserProfile", foreign_keys="Follow.following_id",  back_populates="following")
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        