from exstensions import db
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy import (Column, ForeignKey, BigInteger, 
                        String, Integer, Float, Text, DateTime, Boolean)
from sqlalchemy.dialects.postgresql import UUID
from .schema_types import *



class Follow(db.Model):
    __tablename__ = 'follow'
    __table_args__ = {'schema': follow_schema} 
    follow_id = Column(BigInteger, primary_key=True)
    follower_id = Column(UUID(as_uuid=True), ForeignKey(f'{user_profile_schema}.user_profile.id')) # Who is following
    following_id = Column(UUID(as_uuid=True), ForeignKey(f'{user_profile_schema}.user_profile.id')) # Who is being followed
    