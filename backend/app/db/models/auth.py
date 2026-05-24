from typing import TYPE_CHECKING, Optional

from advanced_alchemy.extensions.litestar import base
from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models import UserProfile

class AuthUser(base.UUIDAuditBase):
    __tablename__ = "auth_user"

    username: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    last_signed_in: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    locked_until: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))

    profile: Mapped["UserProfile"] = relationship(back_populates='auth')


