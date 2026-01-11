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


    name = fields.Str(validate= [validate.Regexp(r"^(?!.*[-']{2})[a-zA-Z ][-a-zA-Z ']*[a-zA-Z ]$",error="Name can only contain letters")])
    description = fields.Str(validate=[validate.Length(max = 200)])
    accessibility = fields.Bool()
    hashtags = fields.List(
        fields.Str(validate=validate.Regexp(r'^[a-zA-Z0-9_]+$', error="Hashtags can only contain letters, numbers, and underscores")),
        validate=validate.Length(max=10)
    )
   

    @validates('hashtags')
    def validate_hashtags(self, value, **kwargs):
        if value:
            checked_tags = []

            for hashtag in value:
                tag_length = 50
                if len(hashtag) > tag_length:
                    raise ValidationError(f'Each hashtag must be {tag_length} characters or less')
                
                if hashtag in checked_tags:
                    raise ValidationError(f'Duplicate hashtags are not allowed. Duplicated tag: {hashtag}')
                
                checked_tags.append(hashtag)
        return value

    @validates('name')
    def validate_first_name(self, value, **kwargs):
        if not value or value.strip() == '' or len(value) == 0:
            raise ValidationError("Spot name can not be empty")
        
        if "  " in value:
            raise ValidationError("Invalid spot name")
        
        if value.startswith(("'", '-')) or value.endswith(("'", '-')):
            raise ValidationError("Name cannot start or end with an apostrophe or a hyphen")
        
        spot_name_length = 40
        if(len(value) > spot_name_length):
            raise ValidationError(f'Spot name must be {spot_name_length} characters or less')
        
        return value.strip()
    
    @validates('description')
    def validate_bio(self,value, **kwargs):
        if '\x00' in value:
            raise ValidationError('Description contains invalid characters')
        
        spot_description_length = 200
        if len(value) > spot_description_length:
            raise ValidationError(f'Spot description must be {spot_description_length} characters or less')

        return value.strip()

    def get_coordinates(self, obj):
        if not obj.coordinates:
            return None
    
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