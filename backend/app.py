from flask import Flask
from flask_cors import CORS
from config import Config
from exstensions import db, ma, jwt, limiter,mg
from logging.config import dictConfig
from routes.logging_wrapper import handle_errors


dictConfig({
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            "datefmt": "%B %d, %Y %I:%M:%S %p",
        }
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "app_logs.log",
            "formatter": "default",
        },
    },
    "root": {
        "level": "DEBUG",  
        "handlers": ["file"],  
    },
})


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_global_error_handler(app)

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
    from routes.block import block_bp
    from routes.post import post_bp
    from routes.visit import visit_bp
    from models import (location, user, post, rating, visit, report,followers_and_following)

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(follow_bp)
    app.register_blueprint(block_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(visit_bp)

    # Create tables
    with app.app_context():
        db.drop_all()   #todo: TEMPORARY for testing
        db.create_all()

        @app.route('/')
        def health_check():
            return {'status': 'healthy', 'message': 'Aestelo API is running'}
        

        return app
    

def register_global_error_handler(app):
        for endpoint, func in app.view_functions.items():
            if endpoint not in ('static',):  # skip static routes
                app.view_functions[endpoint] = handle_errors(func)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)