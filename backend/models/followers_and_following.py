import uuid
from extensions import db
from sqlalchemy import (Column, ForeignKey, BigInteger, 
                     Index, UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models import UserProfile



class Follow(db.Model):
    __tablename__ = "follow"
    __table_args__ = (
    Index('idx_follow_follower_id_following_id', "follower_id", "following_id"),    
    UniqueConstraint('follower_id', 'following_id', name='unique_follow')
    )
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    follower_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id'), nullable=False)
    following_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id'), nullable=False)

    id = Column(BigInteger, primary_key=True)
    follower_id = Column(UUID(as_uuid=True), ForeignKey('user_profile.id')) # Who is following
    following_id = Column(UUID(as_uuid=True), ForeignKey('user_profile.id')) # Who is being followed

    follower: Mapped["UserProfile"] = relationship("UserProfile", foreign_keys="Follow.follower_id", back_populates="follower")

    following: Mapped["UserProfile"] = relationship("UserProfile", foreign_keys="Follow.following_id",  back_populates="following")
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        