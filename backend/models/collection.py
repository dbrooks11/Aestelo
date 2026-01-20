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
    is_default = Column(Boolean, default=False)


class CollectionItem(db.Model):
    id = Column(BigInteger, primary_key=True)
    collection_id = Column(BigInteger, ForeignKey('collection.id'))
    spot_id = Column(BigInteger, ForeignKey('spot.id'), nullable=True)
    visit_id = Column(BigInteger, ForeignKey('visit.id'), nullable=True)
    saved_by = Column(UUID(as_uuid=True), nullable=False)
    saved_at = Column(DateTime(timezone=True), server_default=func.now())