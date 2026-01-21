from exstensions import db
from sqlalchemy import (Column, ForeignKey, BigInteger, Integer, DateTime, UniqueConstraint, Index, func)
from sqlalchemy.dialects.postgresql import UUID
from models.user import UserProfile
from models.spot import Spot



class Rating(db.Model):
    __table_args__ = (Index('idx_rating_spot_id','spot_id')
                    ,UniqueConstraint('user_id', 'spot_id', name='unique_rating'), 
                   )
    
    rating_id = Column(BigInteger, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(UserProfile.id), nullable=False)
    spot_id = Column(BigInteger, ForeignKey(Spot.id), nullable=False)
    rating_choice = Column(Integer, default=0, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()
