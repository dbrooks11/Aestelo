from exstensions import db
from datetime import datetime, timezone
from sqlalchemy import (Column, ForeignKey, BigInteger, Integer, DateTime, UniqueConstraint, Index)
from sqlalchemy.dialects.postgresql import UUID
from .schema_types import *



class Rating(db.Model):
    __tablename__ = "rating"
    __table_args__ = (Index('idx_rating_post_id','post_id')
                    ,UniqueConstraint('user_profile_id', 'post_id', name='unique_rating'), 
                    {'schema': rating_schema})
    
    rating_id = Column(BigInteger, primary_key=True)
    user_profile_id = Column(UUID(as_uuid=True), ForeignKey(f'{user_profile_schema}.user_profile.id'), nullable=False)
    post_id = Column(BigInteger, ForeignKey(f'{post_schema}.post.post_id'), nullable=False)
    rating_choice = Column(Integer, default=0, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    

    def to_dict(self):
        return {
            'post_id': self.post_id,
            'user_profile_id': self.user_profile_id,
            'rating_id': self.rating_id,
            'rating_choice': self.rating_choice,
            'created_at': self.created_at
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
