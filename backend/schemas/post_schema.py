from app import ma
from marshmallow import (fields, Schema, validates, 
                         validates_schema, ValidationError, validate)
from models.post import Post,PostMedia

class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True
        include_fk = True
        exclude = ('is_deleted','deleted_at','num_reports','is_removed','removed_at')

    post_id = fields.Integer(dump_only=True)
    date_posted = fields.DateTime(dump_only=True)
    total_num_of_photos = fields.Integer(validate=[(validate.Range(min=0,max=5))], dump_only=True)
    average_rating = fields.Float(validate=[(validate.Range(min=0.0, max=5.0))], dump_only=True)
    total_num_of_ratings = fields.Integer(validate=[(validate.Range(min=0))], dump_only=True)
    last_rated_at = fields.DateTime(dump_only=True)
    save_count = fields.Integer(validate=[(validate.Range(min=0))], dump_only=True)
    share_count = fields.Integer(validate=[(validate.Range(min=0))], dump_only=True)
    trending_score = fields.Integer(validate=[(validate.Range(min=0))], dump_only=True)


class PostMediaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PostMedia
        load_instance = True
        include_fk = True
        
    post_media_id = fields.Int(dump_only=True)
    media_url = fields.Str(dump_only=True)
    width = fields.Int(validate=validate.Range(min=500, max=1080), dump_only=True)
    height = fields.Int(validate=validate.Range(min=500, max=1350), dump_only=True)
    verified_status = fields.Str(dump_only=True)

    @validates('media_type')
    def validate_media_type(self, value):
        allowed = ['image']
        if value not in allowed:
            raise ValidationError(f"Media type must be: {allowed}")
        return value

    @validates('verified_status')
    def validate_status(self, value):
        allowed = ['pending', 'verified', 'rejected']
        if value not in allowed:
            raise ValidationError(f"Status must be one of: {allowed}")
        return value
