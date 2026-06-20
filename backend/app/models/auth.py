from typing import TYPE_CHECKING

from advanced_alchemy.extensions.litestar import base
from advanced_alchemy.types import DateTimeUTC
from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.lib.validation import validate

if TYPE_CHECKING:
    from app.models import UserProfile


class AuthUser(base.UUIDAuditBase):
    __tablename__ = "auth_user"

    username: Mapped[str] = mapped_column(
        String(validate.USERNAME_MAX_LENGTH), unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    last_signed_in: Mapped[DateTime | None] = mapped_column(DateTimeUTC)
    locked_until: Mapped[DateTime | None] = mapped_column(DateTimeUTC)

    profile: Mapped["UserProfile"] = relationship(back_populates="auth", lazy="joined")
