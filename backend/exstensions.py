from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_debugtoolbar import DebugToolbarExtension
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from supabase import create_client
import os


db = SQLAlchemy()
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
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)