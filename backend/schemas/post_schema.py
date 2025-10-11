from app import ma
from marshmallow import (fields, validates, 
                         ValidationError, validate, pre_load)
from models.post import Post,PostMedia

class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True
        include_fk = True
        exclude = ('is_deleted','deleted_at','num_reports','is_removed','removed_at')

    post_id = fields.Integer(dump_only=True)
    refined_location = fields.Float(dump_only=True)
    date_posted = fields.DateTime(dump_only=True, format='%b %d, %Y')
    total_num_of_photos = fields.Integer(validate=[(validate.Range(min=0,max=5))], dump_only=True)
    average_rating = fields.Float(validate=[(validate.Range(min=0.0, max=5.0))], dump_only=True)
    total_num_of_ratings = fields.Integer(validate=[(validate.Range(min=0))], dump_only=True)
    last_rated_at = fields.DateTime(dump_only=True)
    save_count = fields.Integer(validate=[(validate.Range(min=0))], dump_only=True)
    share_count = fields.Integer(validate=[(validate.Range(min=0))], dump_only=True)
    num_of_edits = fields.Int(dump_only=True, validate=validate.Range(max=1, error='Post can only be edited once'))
    trending_score = fields.Integer(validate=[(validate.Range(min=0))], dump_only=True)


    name = fields.Str(validate= [validate.Regexp(r"^[a-zA-Z\s]+$",error="Name can only contain letters")])
    description = fields.Str(validate=[validate.Regexp(r"^(?!.*<[^>]+>)[\p{L}\p{N}\p{P}\p{Zs}\n\r\t]$")])

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

    @validates('name')
    def validate_first_name(self, value):
        if not value or value.strip() == '':
            return value
        
        if "  " in value:
            raise ValidationError("Invalid post name")
        
        if value.startswith(("'", '-')) or value.endswith(("'", '-')):
            raise ValidationError("Name cannot start or end with apostrophe or hyphen")
        
        return value.strip()

    @pre_load
    def strip_strings(self, data, **kwargs):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()
        return data


class PostMediaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PostMedia
        load_instance = True
        include_fk = True
        
    post_media_id = fields.Int(dump_only=True)

    thumbnail_url = fields.Str(dump_only=True)
    thumb_media_type = fields.Str(dump_only=True)

    media_url = fields.Str(dump_only=True)
    media_type = fields.Str(dump_only=True)
    width = fields.Int(validate=validate.Range(min=600, max=1080), dump_only=True)
    height = fields.Int(validate=validate.Range(min=600, max=1350), dump_only=True)

    @validates('media_type')
    def validate_media_type(self, value):
        allowed = ['photo']
        if value not in allowed:
            raise ValidationError(f"Media type must be: {allowed}")
        return value
    
    @validates('thumb_media_type')
    def validate_thumb_type(self, value):
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


post_schema = PostSchema()
post_media_schema = PostMediaSchema()