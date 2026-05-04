import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from extensions import db
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models import UserProfile



class AuthUser(db.Model):
    __tablename__ = "auth_user"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    password_encrypted: Mapped[str] = mapped_column(String(255), nullable=False)

    email_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    email_confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    email_change_sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    password_change_sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    password_confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_sign_in_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    failed_login_attempts: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    locked_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    user_profile: Mapped["UserProfile"] = relationship("UserProfile" , back_populates='auth', uselist=False)