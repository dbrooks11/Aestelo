


from flask import Flask, jsonify
from flask_cors import CORS
from .config import Config
from colorama import init
import backend.models
from backend.models.token_blacklist import TokenBlackList
from .exstensions import db, ma, jwt, limiter,mg, toolbar
from .routes import register_blueprints
# from logging.config import dictConfig
from .routes.logging_wrapper import handle_errors


# dictConfig({
#     "version": 1,
#     "formatters": {
#         "default": {
#             "format": "[%(asctime)s] %(levelname)s in %(module)s - %(message)s",
#             "datefmt": "%B %d, %Y | %I:%M:%S %p",
#         }
#     },
#     "handlers": {
#         "file": {
#             "class": "logging.FileHandler",
#             "filename": "app_logs.log",
#             "formatter": "default",
#         },
#     },
#     "root": {
#         "level": "DEBUG",  
#         "handlers": ["file"],  
#     },
# })


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_global_error_handler(app)
    app.config['DEBUG_TB_ENABLED'] = True
    init(autoreset=True)
    app.json.sort_keys = False
    
    toolbar.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    mg.init_app(app, db)

    
    #todo: TEMPORARY CORS Attributes
    CORS(app, 
     origins=["http://localhost:5173", "http://127.0.0.1:5173", "null"],
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
     supports_credentials=True)
    
    
    # Register blueprints
    register_blueprints(app)

    # Create tables
    with app.app_context():
        
        
        # db.drop_all()   #todo: TEMPORARY for testing
        db.create_all()

        #jwt hanlders
        @jwt.expired_token_loader
        def expired_token_callback(jwt_header, jwt_data):
            return jsonify({
                "error": "expired",
                "message": "Session has expired"
            }), 401

        @jwt.invalid_token_loader
        def invalid_token_callback(error):
            return jsonify({
                "error": "invalid",
                "message": "Verification failed"
            }), 401

        @jwt.unauthorized_loader
        def missing_token_callback(error):
            return jsonify({
                "error": "authorization required",
                "message": "Request does not contain a valid token"
            }), 401
        
        @jwt.token_in_blocklist_loader
        def token_in_blocklist_callback(jwt_header, jwt_data):
            jti = jwt_data['jti']
            token = db.session.query(TokenBlackList).filter(TokenBlackList.jti == jti).scalar()
            return token is not None  # True => revoked
        
        
        @app.route('/')
        def health_check():
            return {'status': 'healthy', 'message': 'Aestelo API is running'}   

        return app
    

def register_global_error_handler(app):
        for endpoint, func in app.view_functions.items():
            if endpoint not in ('static',): 
                app.view_functions[endpoint] = handle_errors(func)


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)