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

    
    
    CORS(app)
    # Register blueprints
    # from routes.auth import auth_bp
    # from routes.profile import profile_bp
    from models import location, user, post

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