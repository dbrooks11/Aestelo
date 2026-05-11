from backend.app.extensions import ma
from marshmallow import fields
from models import Collection, CollectionItem

from schemas import SpotSchema, VisitSchema


class CollectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Collection

    preview_thumbnails = fields.List(fields.Str(),attribute='preview_thumbnail_urls', dump_only=True)


class CollectionItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CollectionItem
        exclude = ('id', 'saved_by', 'saved_at')
    
    spot = fields.Nested(SpotSchema)
    visit = fields.Nested(VisitSchema)


collection_schema = CollectionSchema()
collection_item_schema = CollectionItemSchema()