import uuid

from extensions import db
from sqlalchemy import BigInteger, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class BlockProfile(db.Model):
    __tablename__ = 'block_profile'
    __table_args__ = (Index(None,'blocker_id','blocked_id', unique=True),)
                      
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    blocker_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id'), nullable=False)
    blocked_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id'), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()