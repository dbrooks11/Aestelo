
import os
import time
from datetime import datetime, timezone
import uuid
import models
from backend.app.config import config_dict
from backend.app.extensions import celery_init_app, db, jwt, limiter, ma, mg
from flask import Flask, g, jsonify, request
from flask_cors import CORS
from flask_talisman import Talisman
from utils.loggin_config import configure_logging
from models.token_blacklist import TokenBlackList
from sqlalchemy import select
from routes import register_blueprints


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
    register_blueprints(app)
    register_jwt_handlers(app)
    configure_security(app)

    @app.before_request
    def assign_request_id():
        g.request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
        g.start_time = datetime.now(timezone.utc)

    @app.after_request
    def add_request_id_header(response):
        response.headers['X-Request-ID'] = g.request_id
        return response
    
    @app.before_request
    def start_timer():
        g.start = time.time()

    @app.after_request
    def log_request(response):
        if request.path.startswith('/static'): 
            return response
        now = time.time()
        duration = round(now - g.start, 2)
        duration_ms = round((now - g.start) * 1000, 2)
        print(f"⏱️ {request.method} {request.path} took {duration}s/{duration_ms}ms")
        return response

 
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