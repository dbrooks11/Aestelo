
import os

import models
from flask import Flask, jsonify
from flask_cors import CORS
from flask_talisman import Talisman
from middleware.logging_middleware import configure_logging_middleware
from middleware.request_time_middleware import configure_request_time
from models.token_blacklist import TokenBlackList
from routes import register_blueprints
from sqlalchemy import select
from utils.loggin_config import configure_logging

from backend.app.config import config_dict
from backend.app.extensions import celery_init_app, db, jwt, limiter, ma, mg


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    if config_name == 'production':
        assert os.environ.get('SECRET_KEY'), "SECRET_KEY environment variable is required"
        assert not app.debug, "DEBUG must be False in production"
    

    extensions(app)
    configure_logging(app)
    configure_logging_middleware(app)
    configure_request_time(app)
    register_blueprints(app)
    register_jwt_handlers(app)
    configure_security(app)

    with app.app_context():
        @app.route('/')
        def health_check():
            return {
            'status': 'healthy', 
            'message': 'Aestelo API is running', 
            'env': config_name
        }   

        return app

def extensions(app):
    celery_init_app(app)
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    mg.init_app(app, db, compare_type=True)

def configure_security(app):

    origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
    mobile_ip = os.getenv('IP_FOR_MOBILE_TESTING')
    if mobile_ip:
        origins.append(mobile_ip)
    
    production_domain = os.getenv('PRODUCTION_DOMAIN')
    if production_domain:
        origins.append(production_domain)

    CORS(app, 
         origins=origins,
         supports_credentials=True,
         allow_headers=["Content-Type", "X-CSRF-TOKEN", "X-CSRF-Token", "x-csrf-token"],
         methods=["GET", "POST", "PUT", "DELETE", "PATCH"])

    #TODO: set content security policy for scripts in my app
    if not app.debug:
        Talisman(app,
            force_https=True,
            strict_transport_security=True,
            strict_transport_security_include_subdomains=True,
            content_security_policy=None, 
            frame_options='DENY'
        )


def register_jwt_handlers(app):
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
        token = db.session.execute(select(TokenBlackList).where(TokenBlackList.jti == jti)).first()
        return token is not None  # True => revoked