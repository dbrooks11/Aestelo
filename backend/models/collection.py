from exstensions import db
from sqlalchemy import (Column, ForeignKey, BigInteger, Text, DateTime, Boolean, func)
from sqlalchemy.dialects.postgresql import UUID


class Collection(db.Model):
    id = Column(BigInteger, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user_profile.id'))
    name = Column(Text)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_public = Column(Boolean, default=False)