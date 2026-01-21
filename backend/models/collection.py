from exstensions import db
from sqlalchemy import (Column, ForeignKey, BigInteger, Text, DateTime, Boolean, func)
from sqlalchemy.dialects.postgresql import UUID
from models.spot import Spot
from models.visit import Visit
from models.user import UserProfile


class Collection(db.Model):
    id = Column(BigInteger, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(UserProfile.id), index=True)
    name = Column(Text)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_public = Column(Boolean, default=False)
    is_default = Column(Boolean, default=False)


class CollectionItem(db.Model):
    id = Column(BigInteger, primary_key=True)
    collection_id = Column(BigInteger, ForeignKey(Collection.id))
    spot_id = Column(BigInteger, ForeignKey(Spot.id), nullable=True)
    visit_id = Column(BigInteger, ForeignKey(Visit.id), nullable=True)
    saved_by = Column(UUID(as_uuid=True), nullable=False)
    saved_at = Column(DateTime(timezone=True), server_default=func.now())