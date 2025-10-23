import os
from datetime import timedelta
import boto3
from botocore.client import Config

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
    JWT_SECRET_KEY = os.environ.get('SUPABASE_JWT_SECRET')
    JWT_ALGORITHM = 'HS256'
    
    # CORS
    CORS_ORIGINS = ['http://localhost:5000', 'http://localhost:5173']  # Add your frontend URLs

    # Cloudflare R2 (NEW)
    R2_ACCOUNT_ID = os.environ.get('R2_ACCOUNT_ID')
    R2_ACCESS_KEY_ID = os.environ.get('R2_ACCESS_KEY_ID')
    R2_SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY')
    R2_BUCKET_NAME = os.environ.get('R2_BUCKET_NAME')
    R2_ENDPOINT_URL = os.environ.get('R2_ENDPOINT_URL')
    R2_PUBLIC_URL = os.environ.get('R2_PUBLIC_URL')

    #SIGHTENGINE
    SIGHTENGINE_API_USER = os.environ.get('SIGHTENGINE_API_USER')
    SIGHTENGINE_API_SECRET =os.environ.get('SIGHTENGINE_API_SECRET')

    #SPOTIFY
    SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

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