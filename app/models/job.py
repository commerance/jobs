# app/models/job.py

from datetime import datetime
from app import db
from sqlalchemy.sql import func

class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    responsibilities = db.Column(db.Text, nullable=True)
    requirements = db.Column(db.Text, nullable=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=True, index=True)
    city = db.Column(db.String(100), nullable=True)
    is_remote = db.Column(db.Boolean, default=False, nullable=False, index=True)
    visa_sponsorship = db.Column(db.Boolean, default=False, nullable=False, index=True)
    experience_level = db.Column(db.String(50), nullable=True)
    degree_required = db.Column(db.String(100), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), index=True)
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    expires_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Job {self.title}>'
