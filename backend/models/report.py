from exstensions import db
from sqlalchemy import Column, ForeignKey, BigInteger, String, Integer, Float, Text, DateTime, Boolean, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from .schema_types import *

class Report(db.Model):
    __tablename__ = "report"
    __table_args__ = {'schema': report_schema}  # Moderation data is private
    
    report_id = Column(BigInteger, primary_key=True, autoincrement=True)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey(f'{user_profile_schema}.user_profile.id'), nullable=False)
    
    # What's being reported
    reported_type = Column(String(20), nullable=False)  # 'user', 'post', 'visit'
    reported_id = Column(String(50), nullable=False)  # The ID of whatever is reported
    
    # Report details
    reason = Column(String(50), nullable=False)  # 'spam', 'harassment', 'inappropriate', etc.
    description = Column(Text)  # Optional elaboration
    
    # Moderation tracking
    status = Column(String(20), default='pending')  # 'pending', 'reviewed', 'dismissed', 'actioned'
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey(f'{user_profile_schema}.user_profile.id'), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.now(timezone.utc))