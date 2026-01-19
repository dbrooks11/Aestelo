from exstensions import ma
from marshmallow import (fields, validate)
from models.rating import Rating


class RatingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rating
        load_instance = True
        include_fk = True

    rating_choice = fields.Int(validate=validate.Range(min=1, max=5))


rating_schema = RatingSchema()