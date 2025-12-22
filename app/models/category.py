# app/models/category.py

from datetime import datetime
from app import db
from sqlalchemy.sql import func

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    jobs = db.relationship('Job', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'
