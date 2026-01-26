import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()
load_dotenv('env_backend/.env.backend_cloudflare')
load_dotenv('env_backend/.env.backend_supabase')
load_dotenv('env_backend/.env.backend_sightengine')
load_dotenv('env_backend/.env.backend_sendgrid')
load_dotenv('env_backend/.env.backend_celery')
load_dotenv('env_backend/.env.development')

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JSON_SORT_KEYS = False
    MAX_CONTENT_LENGTH = 200 * 1024 * 1024
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }

    # JWT Core
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=120)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_COOKIE_CSRF_PROTECT = True
    
    # Default Security (Override in Prod)
    JWT_COOKIE_SECURE = False 

    # Cloudflare R2
    R2_ACCESS_KEY_ID = os.environ.get('R2_ACCESS_KEY_ID')
    R2_SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY')
    R2_BUCKET_NAME = os.environ.get('R2_BUCKET_NAME')
    R2_PUBLIC_URL = os.environ.get('R2_PUBLIC_URL')

    #CELERY
    CELERY = dict(
        broker_url=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
        result_backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
        task_ignore_result=False,
    )

    #SIGHTENGINE
    SIGHTENGINE_WORKFLOW_ID = os.environ.get('SIGHTENGINE_WORKFLOW_ID')
    SIGHTENGINE_API_USER = os.environ.get('SIGHTENGINE_API_USER')
    SIGHTENGINE_API_SECRET =os.environ.get('SIGHTENGINE_API_SECRET')

class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_TB_ENABLED = True
    JWT_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = 'Strict'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    CELERY = dict(
        broker_url=os.environ.get('CELERY_BROKER_URL_PROD'),
        result_backend=os.environ.get('CELERY_RESULT_BACKEND_PROD'),
        task_ignore_result=False,
    )

config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

    
 

