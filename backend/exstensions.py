from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_debugtoolbar import DebugToolbarExtension
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from sqlalchemy import MetaData


convention = {
    "ix": 'ix_%(column_0_name)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata_db = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata_db)
ma = Marshmallow()
jwt = JWTManager()
mg = Migrate()
toolbar = DebugToolbarExtension()
limiter = Limiter(
    get_remote_address,
    default_limits=["10000 per day", "10000 per hour"],
    storage_uri="memory://", #This URI is only meant for testing/development and 
                            #should be replaced with an appropriate storage of your choice before moving to production.
    )
