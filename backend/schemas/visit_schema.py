# schemas/visit.py
from app import ma
from models.visit import Visit, VisitMedia
from marshmallow import validates, ValidationError, fields, validate, pre_load

class VisitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Visit
        load_instance = True
        include_fk = True
        exclude = ('is_deleted', 'deleted_at', 'is_removed', 'num_reports', 'deleted_by')  
   
    visit_id = fields.Int(dump_only=True)
    refined_location = fields.Dict(dump_only=True)
    date_posted = fields.DateTime(dump_only=True)
    like_count = fields.Int(dump_only=True)
    share_count = fields.Int(dump_only=True)
    num_of_edits = fields.Int(dump_only=True, validate=validate.Range(max=3, error='Visit can only be edited 3 times'))
    user_profile_id = fields.UUID(dump_only=True) 
    spotify_track_id = fields.Str(dump_only=True)
    
    # Required fields
    post_id = fields.Int(required=True)
  
    caption = fields.Str(validate=validate.Length(max=250))
    hashtags = fields.List(
        fields.Str(validate=validate.Regexp(r'^[a-zA-Z0-9_#]+$', error="Hashtags can only contain letters, numbers, and underscores")),
        validate=validate.Length(max=20)
    )
    
    
    @validates('hashtags')
    def validate_hashtags(self, value):
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
    def validate_edit_count(self, value):
        if value > 3:
            raise ValidationError("Maximum 3 edits allowed per visit")
        return value
    
    @pre_load
    def strip_strings(self, data, **kwargs):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()
        return data

class VisitMediaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VisitMedia
        load_instance = True
        include_fk = True
 
    visit_media_id = fields.Int(dump_only=True)
    media_url = fields.Str(dump_only=True, validate=validate.URL())  
    upload_date = fields.DateTime(dump_only=True, format='%b %d, %Y')
    uploaded_by = fields.UUID(dump_only=True) 
    visit_id = fields.Int(required=True)
    total_num_of_photos = fields.Int(dump_only=True)
    
    index = fields.Int(dump_only=True, validate=validate.Range(min=1))
    location_id = fields.Int()
    width = fields.Int(validate=validate.Range(min=500, max=1080), dump_only=True)
    height = fields.Int(validate=validate.Range(min=500, max=1350), dump_only=True)
    
    @validates('media_type')
    def validate_media_type(self, value):
        allowed = ['photo']
        if value not in allowed:
            raise ValidationError(f"Media type must be one of: {allowed}")
        return value

    @validates('verified_status')
    def validate_status(self, value):
        allowed = ['pending', 'verified', 'rejected']
        if value not in allowed:
            raise ValidationError(f"Status must be one of: {allowed}")
        return value
    
    @pre_load
    def strip_strings(self, data, **kwargs):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()
        return data

visit_schema = VisitSchema()
visit_media_schema = VisitMediaSchema()