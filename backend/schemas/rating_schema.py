from app import ma
from marshmallow import (fields, validate)
from models.rating import Rating


class RatingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rating
        load_instance = True
        include_fk = True
    
    rating_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    user_profile_id = fields.UUID(dump_only=True)  
    post_id = fields.Int(dump_only=True)

    rating_choice = fields.Int(validate=validate.Range(min=1, max=5))