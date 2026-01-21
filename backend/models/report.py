from exstensions import db
from sqlalchemy import Column, ForeignKey, BigInteger, DateTime, Text, func
from sqlalchemy.dialects.postgresql import UUID
from models.user import UserProfile

class Report(db.Model):
    __table_args__ = () 
    
    report_id = Column(BigInteger, primary_key=True, autoincrement=True)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey(UserProfile.id), nullable=False)
    
    # What's being reported
    reported_type = Column(Text, nullable=False)  # 'user', 'spot', 'visit'
    reported_id = Column(UUID(as_uuid=True), nullable=False)  # The ID of whatever is reported
    
    # Report details
    reason = Column(Text, nullable=False)  # 'spam', 'harassment', 'inappropriate', etc.
    description = Column(Text)  # Optional elaboration
    
    # Moderation tracking
    status = Column(Text, default='pending')  # 'pending', 'reviewed', 'dismissed', 'actioned'
    reviewed_by = Column(UUID(as_uuid=True))
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()