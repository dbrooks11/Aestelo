import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions import db

if TYPE_CHECKING:
    from models.user import UserProfile

class Report(db.Model):
    __tablename__ = "report" 

    report_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    
    reporter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("user_profile.id"), 
        nullable=False
    )
    
    reported_type: Mapped[str] = mapped_column(Text, nullable=False)  # 'user', 'spot', 'visit'
    reported_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    status: Mapped[str] = mapped_column(Text, default='pending')
    reviewed_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True))
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )

    user_profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="report")