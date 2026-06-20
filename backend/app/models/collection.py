from typing import TYPE_CHECKING
import uuid
if TYPE_CHECKING:
    from app.models import Spot, UserProfile, Visit

from advanced_alchemy.extensions.litestar import base
from sqlalchemy import (
    ARRAY,
    UUID,
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from advanced_alchemy.types import DateTimeUTC


class Collection(base.BigIntAuditBase):
    __tablename__ = 'collection'
    __table_args__ = (UniqueConstraint('user_id', 'name'),)
    
    preview_thumbnails: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id', ondelete='CASCADE'), index=True)
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

    profile: Mapped["UserProfile"] = relationship(back_populates="collection")
    collection_item: Mapped[list["CollectionItem"]] = relationship(back_populates="collection")

    #TODO: remove property and add to schema serialization
    # @property
    # def preview_thumbnail_urls(self):
    #     if not self.preview_thumbnails or len(self.preview_thumbnails) == 0:
    #         return None
        
    #     urls = []
    #     for thumbnail in self.preview_thumbnails:
    #         urls.append(f"{current_app.config['R2_PUBLIC_URL']}/{thumbnail}")
        
    #     return urls


class CollectionItem(base.BigIntBase):
    __tablename__ = 'collection_item'
    __table_args__ = (UniqueConstraint('collection_id', 'spot_id', name='uq_collection_item_collection_spot'),
                      UniqueConstraint('collection_id', 'visit_id', name='uq_collection_item_collection_visit'),)

    collection_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('collection.id', ondelete='CASCADE'), nullable=False)
    spot_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('spot.id', ondelete='CASCADE'), nullable=True)
    visit_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('visit.id', ondelete='CASCADE'), nullable=True)
    saved_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    saved_at: Mapped[DateTime] = mapped_column(DateTimeUTC, server_default=func.now())
    
    collection: Mapped["Collection"] = relationship(back_populates='collection_item')
    spot: Mapped["Spot"] = relationship(back_populates='collection_item')
    visit: Mapped['Visit'] = relationship(back_populates='collection_item')