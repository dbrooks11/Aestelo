from exstensions import db
from sqlalchemy import Column, ForeignKey, BigInteger, String, DateTime, UniqueConstraint, Index, func
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID

class Report(db.Model):
    __table_args__ = (Index('idx_report_item', 'reported_type', 'reported_id'), 
                    Index('idx_report_status', 'status'),
                    UniqueConstraint('reporter_id', 'reported_type', 'reported_id', name='unique_report'),
                    ) 
    
    report_id = Column(BigInteger, primary_key=True, autoincrement=True)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey('user_profile.id'), nullable=False)
    
    # What's being reported
    reported_type = Column(String(20), nullable=False)  # 'user', 'spot', 'visit'
    reported_id = Column(String(50), nullable=False)  # The ID of whatever is reported
    
    # Report details
    reason = Column(String(50), nullable=False)  # 'spam', 'harassment', 'inappropriate', etc.
    description = Column(String(500))  # Optional elaboration
    
    # Moderation tracking
    status = Column(String(20), default='pending')  # 'pending', 'reviewed', 'dismissed', 'actioned'
    reviewed_by = Column(UUID(as_uuid=True))
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            'report_id': self.report_id,
            'reporter_id': self.reporter_id,
            'reported_type': self.reported_type,
            'reported_id': self.reported_id,
            'reason': self.reason,
            'description': self.description,
            'status': self.status,
            'reviewed_by': self.reviewed_by,
            'reviewed_at': self.reviewed_at,
            'created_at': self.created_at
    }

    def save(self):
        db.session.add(self)
        db.session.commit()