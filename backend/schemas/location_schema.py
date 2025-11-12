from marshmallow import (fields, validate)
from ..exstensions import ma
from ..models.location import Location, BusinessLocationDetails

class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        include_fk = True

    latitude = fields.Float(required=True, validate=[(validate.Range(min=-90, max=90))])
    longitude = fields.Float(required=True, validate=[(validate.Range(min=-180.0, max=180.0))])
    created_on = fields.DateTime(dump_only=True)
    altitude = fields.Float(validate=[(validate.Range(min=-1000.0, max=30000.0))])

class BusinessLocationDetailsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BusinessLocationDetails
        include_fk = True

location_schema = LocationSchema()
business_location_schema = BusinessLocationDetailsSchema()