
from flask import Flask, jsonify
from flask_talisman import Talisman
from flask_cors import CORS
from config import Config, configure_logging
from colorama import init
import models
from models import listeners
from models.token_blacklist import TokenBlackList
from exstensions import db, ma, jwt, limiter,mg, celery_init_app
from routes import register_blueprints
from flask import g, request
from PIL import Image
import time
import os



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['DEBUG_TB_ENABLED'] = True
    init(autoreset=True)
    app.json.sort_keys = False
    configure_logging(app)
    app.config.from_mapping(
        CELERY=dict(
            broker_url=os.getenv('CELERY_BROKER_URL'),
            result_backend=os.getenv('CELERY_RESULT_BACKEND'),
            task_ignore_result=False,
        ),
    )

    celery_init_app(app)
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    mg.init_app(app, db, compare_type=True)

    # Register blueprints
    register_blueprints(app)
    
    Image.MAX_IMAGE_PIXELS = 100_000_000

    
    #todo: TEMPORARY CORS Attributes
    mobile_ip=os.getenv('IP_FOR_MOBILE_TESTING')
    CORS(app, 
     origins=["http://localhost:5173", 
              "http://127.0.0.1:5173",
              mobile_ip,
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