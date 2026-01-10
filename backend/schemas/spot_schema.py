from exstensions import ma
from marshmallow import (fields, validates, 
                         ValidationError, validate, pre_load)
from models.spot import Spot,SpotMedia
from geoalchemy2.shape import to_shape

class SpotSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Spot
        include_fk = True
        exclude = ('is_deleted','deleted_at','num_reports','is_removed','removed_at')

    user_profile_id = fields.UUID(dump_only=True)
    spot_id = fields.Integer(dump_only=True)
    coordinates = fields.Method("get_coordinates")
    date_posted = fields.DateTime(dump_only=True)
    total_num_of_photos = fields.Integer(validate=[(validate.Range(min=0,max=5))])
    total_visits = fields.Integer(dump_only = True)
    average_rating = fields.Float(validate=[(validate.Range(min=0.0, max=5.0))], dump_only=True)
    total_num_of_ratings = fields.Integer(validate=[(validate.Range(min=0))], dump_only=True)
    last_rated_at = fields.DateTime(dump_only=True)
    save_count = fields.Integer(validate=[(validate.Range(min=0))], dump_only=True)
    share_count = fields.Integer(validate=[(validate.Range(min=0))], dump_only=True)
    num_of_edits = fields.Int(validate=validate.Range(max=1, error='Spot can only be edited once'))
    trending_score = fields.Integer(validate=[(validate.Range(min=0))], dump_only=True)


    name = fields.Str(validate= [validate.Regexp(r"^[a-zA-Z\s]+$",error="Name can only contain letters")])
    description = fields.Str(validate=[validate.Length(max = 200)])
    hashtags = fields.List(
        fields.Str(validate=validate.Regexp(r'^[a-zA-Z0-9_#]+$', error="Hashtags can only contain letters, numbers, and underscores")),
        validate=validate.Length(max=10)
    )

    @validates('hashtags')
    def validate_hashtags(self, value, **kwargs):
        if value:
            for hashtag in value:
                if len(hashtag) > 100:
                    raise ValidationError("Each hashtag must be 100 characters or less")
                if hashtag.count('#') > 1:
                    raise ValidationError("Hashtag can only contain one #")
                if hashtag[0] != '#':
                    raise ValidationError("Hashtags must begin with a #")
        return value

    @validates('name')
    def validate_first_name(self, value, **kwargs):
        if not value or value.strip() == '':
            return value
        
        if "  " in value:
            raise ValidationError("Invalid spot name")
        
        if value.startswith(("'", '-')) or value.endswith(("'", '-')):
            raise ValidationError("Name cannot start or end with apostrophe or hyphen")
        
        return value.strip()
    
    @validates('description')
    def validate_bio(self,value, **kwargs):
        if '\x00' in value:
            raise ValidationError('Description contains invalid characters')
        return value

    @pre_load
    def strip_strings(self, data, **kwargs):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()
        return data

    def get_coordinates(self, obj):
        if not obj.coordinates:
            return None
        
        # to_shape converts the binary WKBElement to a Python Shapely object
        point = to_shape(obj.coordinates)
        return {
            "latitude": point.y,
            "longitude": point.x
        }
class SpotMediaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SpotMedia
        include_fk = True
        
    spot_media_id = fields.Int(dump_only=True)

    thumbnail_url = fields.URL()
    thumb_media_type = fields.Str()
    index = fields.Int(validate=validate.Range(min=1))
    photo_url = fields.URL()
    photo_type = fields.Str()
    width = fields.Int(validate=validate.Range(min=500, max=1080))
    height = fields.Int(validate=validate.Range(min=500, max=1350))

    @validates('photo_type')
    def validate_photo_type(self, value, **kwargs):
        allowed = ['photo']
        if value not in allowed:
            raise ValidationError(f"Photo type must be: {allowed}")
        return value
    
    @validates('thumb_media_type')
    def validate_thumb_type(self, value, **kwargs):
        allowed = ['photo']
        if value not in allowed:
            raise ValidationError(f"Thumbnail Media type must be: {allowed}")
        return value
    
    @pre_load
    def strip_strings(self, data, **kwargs):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()
        return data


spot_schema = SpotSchema()
spot_media_schema = SpotMediaSchema()
partial_schema = SpotSchema(only =('name','description','hashtags','accessibility'))