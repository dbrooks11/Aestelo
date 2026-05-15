import os
from datetime import timedelta
from dotenv import load_dotenv
from kombu import Queue

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JSON_SORT_KEYS = False
    MAX_CONTENT_LENGTH = 200 * 1024 * 1024
    MAX_FILE_SIZE = 20 * 1024 * 1024
    ALLOWED_POST_FORMATS = {
        'image/jpeg': 'jpg',
        'image/jpg': 'jpg',
        'image/heic': 'heic',
        'image/heif': 'heif',
    }
    ALLOWED_MIME_TYPES = {
        'image/jpeg': 'jpg',
        'image/jpg': 'jpg',
        'image/png': 'png',
        'image/webp': 'webp',
        'image/heic': 'heic',
        'image/heif': 'heif',
    }
    
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

    # Cloudflare R2
    R2_ACCESS_KEY_ID = os.environ.get('R2_ACCESS_KEY_ID')
    R2_SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY')
    R2_BUCKET_NAME = os.environ.get('R2_BUCKET_NAME')
    R2_ENDPOINT = os.environ.get('R2_S3_API')
    R2_PUBLIC_URL = os.environ.get('R2_PUBLIC_DEV_URL')
    
    
    #CELERY
    CELERY = dict(
        broker_url=os.getenv('CELERY_BROKER_URL'),
        result_backend=os.getenv('CELERY_RESULT_BACKEND'),
        task_ignore_result=False,
    )

    CELERY_WORKER_PREFETCH_MULTIPLIER = 1 
    CELERY_TASK_QUEUES = (
        Queue('default', routing_key='default'),
        Queue('media_processing')
    )

    CELERY_TASK_ROUTES = {
        'process_photos_metadata': {'queue': 'media_processing'},
        'location_batch': {'queue': 'media_processing'}
        # 'app.tasks.send_email': {'queue': 'default'}, can be added when emails and such are set up
    }

class DevelopmentConfig(Config):
    #Flask
    DEBUG = True
    DEBUG_TB_ENABLED = True
    JWT_COOKIE_SECURE = False

    #Celery
    CELERY = dict(
        broker_url='redis://redis:6379/0',
        result_backend='redis://redis:6379/0',
        task_ignore_result=False,
    )

class ProductionConfig(Config):
    DEBUG = False
    JWT_COOKIE_SECURE = True
    R2_PUBLIC_URL = os.environ.get('R2_CUSTOM_DOMAIN')


config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

    
 

