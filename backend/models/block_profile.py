from exstensions import db
from sqlalchemy import (Column, ForeignKey, BigInteger, 
                     Index, UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
class BlockProfile(db.Model):
    __table_args__ = (Index('idx_block_profile_blocker_blocked','blocker_id','blocked_id'),
                      Index('idx_block_profile_blocked', 'blocked_id'), 
                      UniqueConstraint('blocker_id','blocked_id', name = 'block_profile_unique'))
                      
    
    id = Column(BigInteger, primary_key=True)
    blocker_id = Column(UUID(as_uuid=True), ForeignKey('user_profile.id'), nullable=False)
    blocked_id = Column(UUID(as_uuid=True), ForeignKey('user_profile.id'), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()