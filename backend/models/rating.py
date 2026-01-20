from exstensions import db
from datetime import datetime, timezone
from sqlalchemy import (Column, ForeignKey, BigInteger, Integer, DateTime, UniqueConstraint, Index, func)
from sqlalchemy.dialects.postgresql import UUID




class Rating(db.Model):
    __table_args__ = (Index('idx_rating_spot_id','spot_id')
                    ,UniqueConstraint('user_profile_id', 'spot_id', name='unique_rating'), 
                   )
    
    rating_id = Column(BigInteger, primary_key=True)
    user_profile_id = Column(UUID(as_uuid=True), ForeignKey('user_profile.id'), nullable=False)
    spot_id = Column(BigInteger, ForeignKey('spot.id'), nullable=False)
    rating_choice = Column(Integer, default=0, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    

    def to_dict(self):
        return {
            'spot_id': self.spot_id,
            'user_profile_id': self.user_profile_id,
            'rating_id': self.rating_id,
            'rating_choice': self.rating_choice,
            'created_at': self.created_at
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
