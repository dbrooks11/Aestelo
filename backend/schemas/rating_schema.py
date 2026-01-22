from extensions import ma
from models.rating import Rating


class RatingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rating
        load_instance = True
        include_fk = True
