# app/config.py

import os

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://localhost/jobsearch')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20
    }
    
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_TYPE = 'redis'
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_KEY_PREFIX = 'jobsearch:'
    
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    PREFERRED_URL_SCHEME = 'https'
    
    INDEXABLE = True
    CANONICAL_BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')
    
    ORGANIZATION_NAME = os.environ.get('ORGANIZATION_NAME', 'JobSearch Platform')
    ORGANIZATION_LOGO = os.environ.get('ORGANIZATION_LOGO', '')
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    JOBS_PER_PAGE = 50
    BLOG_PER_PAGE = 20


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    
    SESSION_COOKIE_SECURE = False
    
    SQLALCHEMY_ECHO = False
    
    INDEXABLE = False


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    
    SESSION_COOKIE_SECURE = True
    
    SQLALCHEMY_ECHO = False
    
    INDEXABLE = True
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    if not SECRET_KEY:
        raise ValueError('SECRET_KEY environment variable must be set in production')


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/jobsearch_test'
    
    SESSION_COOKIE_SECURE = False
    
    INDEXABLE = False
    
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
