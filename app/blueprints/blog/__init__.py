# app/blueprints/blog/__init__.py

from flask import Blueprint

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')

from . import routes
