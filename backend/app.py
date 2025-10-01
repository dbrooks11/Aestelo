from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
limiter = Limiter(
    get_remote_address,
    default_limits=["100 per day", "20 per hour"],
    storage_uri="memory://", #This URI is only meant for testing/development and 
                            #should be replaced with an appropriate storage of your choice before moving to production.
    )

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    
    CORS(app)

     # Register blueprints
    # from routes.auth import auth_bp
    # from routes.profile import profile_bp

    # app.register_blueprint(auth_bp, url_prefix='/api/auth')
    # app.register_blueprint(profile_bp, url_prefix='/api/profile')

    # Create tables
    with app.app_context():
        db.engine.connect()
        db.create_all()

    @app.route('/')
    def health_check():
        return {'status': 'healthy', 'message': 'Aestelo API is running'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)