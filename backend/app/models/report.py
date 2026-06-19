from typing import TYPE_CHECKING, Optional
import uuid
from advanced_alchemy.extensions.litestar import base
from sqlalchemy import UUID, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from advanced_alchemy.types import DateTimeUTC

if TYPE_CHECKING:
    from app.models import UserProfile

class Report(base.BigIntAuditBase):
    __tablename__ = "report" 
    
    reporter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("user_profile.id"), 
        nullable=False
    )
    
    reported_type: Mapped[str] = mapped_column(Text, nullable=False)  # 'user', 'spot', 'visit'
    reported_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    reviewed_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True))
    reviewed_at: Mapped[Optional[DateTime]] = mapped_column(DateTimeUTC)

    profile: Mapped["UserProfile"] = relationship(back_populates="report")