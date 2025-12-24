
from flask import Flask, jsonify
from flask_talisman import Talisman
from flask_cors import CORS
from config import Config, configure_logging
from colorama import init
import models
from models.token_blacklist import TokenBlackList
from exstensions import db, ma, jwt, limiter,mg, toolbar
from routes import register_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['DEBUG_TB_ENABLED'] = True
    init(autoreset=True)
    app.json.sort_keys = False
    configure_logging(app)

    
    toolbar.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    mg.init_app(app, db, compare_type=True)

    
    #todo: TEMPORARY CORS Attributes
    CORS(app, 
     origins=["http://localhost:5173", 
              "http://127.0.0.1:5173",
              "null"],
     allow_headers=[
              "Content-Type", 
              "X-CSRF-TOKEN",
              "X-CSRF-Token",  
              "x-csrf-token"],
     methods=["GET", 
              "POST", 
              "PUT", 
              "DELETE", 
              "PATCH", 
              "OPTIONS"],
     supports_credentials=True)
    
    if not app.debug:
        Talisman(app,
            force_https=True,  
            strict_transport_security=True,  
            strict_transport_security_max_age=31536000,
            strict_transport_security_include_subdomains=True,
            content_security_policy=None,  
            frame_options='DENY', 
            )
    
    # Register blueprints
    register_blueprints(app)

    # Create tables
    with app.app_context():

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



#todo: remove these for production
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)