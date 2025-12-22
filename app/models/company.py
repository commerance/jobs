# app/models/company.py

from datetime import datetime
from app import db
from sqlalchemy.sql import func

class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    website = db.Column(db.String(255), nullable=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    jobs = db.relationship('Job', backref='company', lazy='dynamic')
    
    def __repr__(self):
        return f'<Company {self.name}>'
