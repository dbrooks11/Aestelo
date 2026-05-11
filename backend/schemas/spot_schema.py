from app.extensions import ma
from geoalchemy2.shape import to_shape
from marshmallow import ValidationError, fields, validate, validates
from models.spot import Spot, SpotMedia

from schemas.user_schema import UserProfileSimpleSchema


class SpotMediaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SpotMedia
        include_fk = True
        exclude = ('spot_id', 'uploaded_by', 'id', 'photo_type', 'photo_path')

    photo_path_url = fields.Str(attribute='photo_path_url', dump_only=True)

class SpotSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Spot
        include_fk = True
        exclude = ('is_deleted','deleted_at','num_reports','is_removed','removed_at', 'trending_score', 'num_of_edits','status')

    coordinates = fields.Method("get_coordinates")

    media = fields.Nested(SpotMediaSchema, many=True)
    username = fields.Pluck(UserProfileSimpleSchema, 'username', attribute='user_profile')

    name = fields.Str(validate= [validate.Regexp(r"^([a-zA-Z](?!.*[-' ]{2})[a-zA-Z-' ]*[a-zA-Z]|[a-zA-Z])$",error="Name can only contain letters")])
    description = fields.Str(validate=[validate.Length(max = 200)])
    accessibility = fields.Bool()
    hashtags = fields.List(
        fields.Str(validate=validate.Regexp(r'^[a-zA-Z0-9_]+$', error="Hashtags can only contain letters, numbers, and underscores")),
        validate=validate.Length(max=15, error='Spot can not have more than 15 tags')
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
    


spot_schema = SpotSchema()
spot_media_schema = SpotMediaSchema()
partial_schema = SpotSchema(only =('name','description','hashtags','accessibility'))