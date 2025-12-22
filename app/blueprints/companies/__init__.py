# app/blueprints/companies/__init__.py

from flask import Blueprint

companies_bp = Blueprint('companies', __name__, url_prefix='/company')

from . import routes
