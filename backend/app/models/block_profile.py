import uuid

from advanced_alchemy.extensions.litestar import base
from sqlalchemy import UUID, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class BlockProfile(base.BigIntBase):
    __tablename__ = "block_profile"
    __table_args__ = (
        UniqueConstraint(
            "blocker_id", "blocked_id", name="uq_block_profile_blocker_blocked"
        ),
        Index(None, "blocker_id", "blocked_id", unique=True),
    )

    blocker_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user_profile.id"), nullable=False
    )
    blocked_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user_profile.id"), nullable=False
    )
