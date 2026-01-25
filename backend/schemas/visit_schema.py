from extensions import ma
from models.visit import Visit, VisitMedia
from marshmallow import validates, ValidationError, fields, validate, pre_load
from geoalchemy2.shape import to_shape
class VisitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Visit
        include_fk = True
        exclude = ('is_deleted', 'deleted_at', 'is_removed', 'num_reports', 'deleted_by')  
   
    coordinates = fields.Method("get_coordinates")
    num_of_edits = fields.Int(validate=validate.Range(max=3, error='Visit can only be edited 3 times'))
    caption = fields.Str(validate=[validate.Length(max=200)])
    hashtags = fields.List(
        fields.Str(validate=validate.Regexp(r'^[a-zA-Z0-9_]+$', error="Hashtags can only contain letters, numbers, and underscores")),
        validate=validate.Length(max=20)
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
    
    @validates('num_of_edits')
    def validate_edit_count(self, value, **kwargs):
        if value > 3:
            raise ValidationError("Maximum 3 edits allowed per visit")
        return value
    
    @validates('caption')
    def validate_bio(self,value, **kwargs):
        if '\x00' in value:
            raise ValidationError('Caption contains invalid characters')
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

class VisitMediaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VisitMedia
        include_fk = True
 
    index = fields.Int( validate=validate.Range(min=1))
    width = fields.Int(validate=validate.Range(min=500, max=1080))
    height = fields.Int(validate=validate.Range(min=500, max=1350))
    
    @validates('photo_type')
    def validate_media_type(self, value, **kwargs):
        allowed = ['photo']
        if value not in allowed:
            raise ValidationError(f"Photo type must be one of: {allowed}")
        return value
    
    @pre_load
    def strip_strings(self, data, **kwargs):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()
        return data

visit_schema = VisitSchema()
visit_media_schema = VisitMediaSchema()
partial_schema = VisitSchema(only = ('music_track_id','caption','hashtags'))