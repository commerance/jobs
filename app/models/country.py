# app/models/country.py

from datetime import datetime
from app import db
from sqlalchemy.sql import func

class Country(db.Model):
    __tablename__ = 'countries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    iso_code = db.Column(db.String(3), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    jobs = db.relationship('Job', backref='country', lazy='dynamic')
    companies = db.relationship('Company', backref='country', lazy='dynamic')
    
    def __repr__(self):
        return f'<Country {self.name}>'
