from marshmallow import (fields, validate)
from app import ma
from models.location import Location, LocationCoreData, BusinessLocationDetails

class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True
        include_fk = True
        exclude = ('verified_status', 'is_long_lat')
    is_visit = fields.Boolean()
    longitude = fields.Float(required=True, validate=[(validate.Range(min=-180.0, max=180.0))])
    latitude = fields.Float(required=True, validate=[(validate.Range(min=-90, max=90))])
    created_on = fields.DateTime(required=True, format='%b %d, %Y')
    #  altitude = fields.Float(validate=[(validate.Range(min=0.0, max=30000.0))])


class LocationCoreDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LocationCoreData
        load_instance = True
        include_fk = True


class BusinessLocationDetailsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BusinessLocationDetails
        load_instance = True
        include_fk = True

location_schema = LocationSchema()
location_coredata_schema = LocationCoreDataSchema()
business_location_schema = BusinessLocationDetailsSchema()