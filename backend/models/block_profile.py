import uuid
from extensions import db
from sqlalchemy import (ForeignKey, BigInteger,Index, UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

class BlockProfile(db.Model):
    __tablename__ = 'block_profile'
    __table_args__ = (Index('idx_block_profile_blocker_id_blocked_id','blocker_id','blocked_id'), 
                      UniqueConstraint('blocker_id','blocked_id', name = 'block_profile_unique'))
                      
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    blocker_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id'), nullable=False)
    blocked_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id'), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()