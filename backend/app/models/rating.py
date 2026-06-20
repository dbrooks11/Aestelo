from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from app.models import Spot, UserProfile

from advanced_alchemy.extensions.litestar import base
from sqlalchemy import (
    UUID,
    BigInteger,
    CheckConstraint,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Rating(base.BigIntAuditBase):
    __tablename__ = "rating"
    __table_args__ = (
        UniqueConstraint("user_id", "spot_id", name="uq_rating_user_id_spot_id"),
        CheckConstraint(
            "rating_choice >= 1 AND rating_choice <= 5", name="rating_range"
        ),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user_profile.id"), nullable=False
    )
    spot_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("spot.id", ondelete="CASCADE"), nullable=False
    )
    rating_choice: Mapped[int] = mapped_column(Integer, nullable=False)

    profile: Mapped["UserProfile"] = relationship(back_populates="rating")
    spot: Mapped["Spot"] = relationship(back_populates="rating")
