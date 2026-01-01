import os
from flask.logging import default_handler
from logging.config import dictConfig
from dotenv import load_dotenv
from botocore.client import Config
from datetime import timedelta



load_dotenv('env_backend/.env.backend_cloudflare')
load_dotenv('env_backend/.env.backend_supabase')
load_dotenv('env_backend/.env.backend_sightengine')
load_dotenv('env_backend/.env.backend_sendgrid')
load_dotenv('env_backend/.env.backend_celery')
load_dotenv('env_backend/.env.development')

class Config:
    # Flask
    ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = ENV == 'development'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG_TB_ENABLED = os.environ.get('DEBUG_TB_ENABLED')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }
    
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=600) #todo: change access token time (current set to 10 hours for development)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_ALG = os.environ.get('JWT_ALG')
    
    #COOKIES
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False  # Only send over HTTPS (False in dev) #todo: set to True in production
    JWT_COOKIE_HTTPONLY = True  
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_COOKIE_CSRF_PROTECT = True  
    JWT_REFRESH_COOKIE_PATH = os.environ.get('JWT_REFRESH_COOKIE_PATH')
    JWT_ACCESS_COOKIE_PATH = os.environ.get('JWT_ACCESS_COOKIE_PATH')
    JWT_SESSION_COOKIE = os.environ.get('JWT_SESSION_COOKIE')

    # Cloudflare R2 (NEW)
    R2_ACCOUNT_ID = os.environ.get('R2_ACCOUNT_ID')
    R2_ACCESS_KEY_ID = os.environ.get('R2_ACCESS_KEY_ID')
    R2_SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY')
    R2_BUCKET_NAME = os.environ.get('R2_BUCKET_NAME')
    R2_ENDPOINT_URL = os.environ.get('R2_ENDPOINT_URL')
    R2_PUBLIC_URL = os.environ.get('R2_PUBLIC_URL')

    #CELERY
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

    #SIGHTENGINE
    SIGHTENGINE_WORKFLOW_ID = os.environ.get('SIGHTENGINE_WORKFLOW_ID')
    SIGHTENGINE_API_USER = os.environ.get('SIGHTENGINE_API_USER')
    SIGHTENGINE_API_SECRET =os.environ.get('SIGHTENGINE_API_SECRET')

    #IMAGE HANDLING
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024



    

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    # Add production-specific settings here

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def configure_logging(app):
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter': 'default'
            }
        },
        'root': {
            'level': 'INFO', #root level for development
            'handlers': ['console']
        }
    })
    
    app.logger.removeHandler(default_handler)

