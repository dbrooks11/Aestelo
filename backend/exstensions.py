from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
mg = Migrate()
limiter = Limiter(
    get_remote_address,
    default_limits=["100 per day", "30 per hour"],
    storage_uri="memory://", #This URI is only meant for testing/development and 
                            #should be replaced with an appropriate storage of your choice before moving to production.
    )