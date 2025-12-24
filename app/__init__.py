# app/__init__.py

import os
from flask import Flask
from app.config import config
from app.database import db
from app.extensions import login_manager

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    login_manager.init_app(app)
    
    from app.blueprints.main import main_bp
    from app.blueprints.jobs import jobs_bp
    from app.blueprints.companies import companies_bp
    from app.blueprints.blog import blog_bp
    from app.blueprints.admin import admin_bp
    from app.blueprints.auth import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    
    from app.seo import seo_bp
    app.register_blueprint(seo_bp)
    
    from app.errors import register_error_handlers
    register_error_handlers(app)
    
    return app
