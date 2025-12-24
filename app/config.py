# app/config.py
import os
from sqlalchemy.pool import NullPool

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://localhost/jobsearch')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Caching - Fallback to SimpleCache if no Redis URL provided (Common in serverless)
    REDIS_URL = os.environ.get('REDIS_URL')
    if REDIS_URL:
        CACHE_TYPE = 'redis'
        CACHE_REDIS_URL = REDIS_URL
    else:
        CACHE_TYPE = 'SimpleCache'
        
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_KEY_PREFIX = 'jobsearch:'
    
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PREFERRED_URL_SCHEME = 'https'
    
    ORGANIZATION_NAME = os.environ.get('ORGANIZATION_NAME', 'JobSearch Platform')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    JOBS_PER_PAGE = 50
    BLOG_PER_PAGE = 20

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20
    }

class ProductionConfig(BaseConfig):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    
    # SERVERLESS CRITICAL FIX: Use NullPool to prevent connection exhaustion
    SQLALCHEMY_ENGINE_OPTIONS = {
        'poolclass': NullPool,
    }
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError('SECRET_KEY environment variable must be set in production')

class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/jobsearch_test'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
