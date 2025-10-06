from flask import Flask
from flask_cors import CORS
from config import Config
from exstensions import db, ma, jwt, limiter,mg

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    mg.init_app(app, db)

    
    #todo: TEMPORARY CORS Attributes
    CORS(app, 
     origins=["http://localhost:5173", "http://127.0.0.1:5173", "null"],
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=True)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.profile import profile_bp
    from routes.follow import follow_bp
    from routes import (auth, profile, user_settings, visit, post)
    from models import (location, user, post, rating, visit, report)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(follow_bp, url_prefix = '/profile/follow')

    # Create tables
    with app.app_context():
        db.drop_all()   #* temporary for testing
        db.create_all()

        @app.route('/')
        def health_check():
            return {'status': 'healthy', 'message': 'Aestelo API is running'}
        
        return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)