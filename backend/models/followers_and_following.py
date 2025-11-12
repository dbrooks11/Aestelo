from ..exstensions import db
from sqlalchemy import (Column, ForeignKey, BigInteger, 
                     Index, UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
from .schema_types import *



class Follow(db.Model):
    __tablename__ = 'follow'
    __table_args__ = (
    Index('idx_follow_follower', 'follower_id'),   
    Index('idx_follow_following', 'following_id'),   
    UniqueConstraint('follower_id', 'following_id', name='unique_follow'),
    {'schema': follow_schema})
    
    follow_id = Column(BigInteger, primary_key=True)
    follower_id = Column(UUID(as_uuid=True), ForeignKey(f'{user_profile_schema}.user_profile.id')) # Who is following
    following_id = Column(UUID(as_uuid=True), ForeignKey(f'{user_profile_schema}.user_profile.id')) # Who is being followed
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        