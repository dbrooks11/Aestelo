from exstensions import db
from sqlalchemy import (Column, ForeignKey, BigInteger, 
                     Index, UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
from .schema_types import *

class BlockProfile(db.Model):
    __tablename__ = 'block_profile'
    __table_args__ = (Index('idx_block_profile_blocker_blocked','blocker_id','blocked__id'),
                      UniqueConstraint('blocker_id','blocked_id', name = 'block_profile_unique'),
                      {schema : block_profile_schema})
    block_profile_id = Column(BigInteger, primary_key=True)
    blocker_id = Column(UUID(as_uuid=True), ForeignKey(f'{user_profile_schema}.user_profile_id'), nullable=False)
    blocked_id = Column(UUID(as_uuid=True), ForeignKey(f'{user_profile_schema}.user_profile_id'), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()