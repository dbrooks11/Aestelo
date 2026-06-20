from typing import TYPE_CHECKING
import uuid
from advanced_alchemy.extensions.litestar import base
from sqlalchemy import UUID, BigInteger, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from advanced_alchemy.types import DateTimeUTC

if TYPE_CHECKING:
    from app.models import UserProfile, Visit


class Likes(base.BigIntBase):
    __tablename__ = "likes"
    __table_args__ = (
        UniqueConstraint("user_id", "visit_id", name="uq_likes_user_id_visit_id"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user_profile.id"), nullable=False
    )
    visit_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("visit.id"), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(DateTimeUTC, server_default=func.now())

    profile: Mapped["UserProfile"] = relationship(back_populates="likes")
    visit: Mapped["Visit"] = relationship(back_populates="likes")
