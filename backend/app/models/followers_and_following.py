import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models import UserProfile
from advanced_alchemy.extensions.litestar import base


class Follow(base.BigIntBase):
    __tablename__ = "follow"
    __table_args__ = (
        UniqueConstraint(
            "follower_id", "following_id", name="uq_follow_follower_following"
        ),
        Index(None, "follower_id", "following_id", unique=True),
    )

    follower_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user_profile.id"), nullable=False
    )  # who is following
    following_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user_profile.id"), nullable=False
    )  # who is being followed

    follower: Mapped["UserProfile"] = relationship(
        foreign_keys="Follow.follower_id", back_populates="follower"
    )
    following: Mapped["UserProfile"] = relationship(
        foreign_keys="Follow.following_id", back_populates="following"
    )
