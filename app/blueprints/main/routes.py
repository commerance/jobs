# app/blueprints/main/routes.py
from flask import render_template, request, current_app
from app.models.job import Job
from app.models.category import Category
from sqlalchemy.orm import joinedload
from . import main_bp

@main_bp.route('/')
def index():
    # Eager load company to prevent N+1 queries
    latest_jobs = Job.query.options(joinedload(Job.company))\
        .filter_by(is_active=True)\
        .order_by(Job.created_at.desc())\
        .limit(20).all()
        
    featured_categories = Category.query.filter_by(parent_id=None).limit(10).all()
    
    return render_template('home.html', 
                         latest_jobs=latest_jobs, 
                         categories=featured_categories)

@main_bp.route('/remote-jobs')
def remote_jobs():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['JOBS_PER_PAGE']
    
    remote_jobs_query = Job.query.options(joinedload(Job.company))\
        .filter_by(is_active=True, is_remote=True)\
        .order_by(Job.created_at.desc())
        
    pagination = remote_jobs_query.paginate(page=page, per_page=per_page, error_out=False)
    remote_jobs = pagination.items
    categories = Category.query.filter_by(parent_id=None).all()
    
    return render_template('remote_jobs.html', 
                         remote_jobs=remote_jobs, 
                         pagination=pagination,
                         categories=categories)

@main_bp.route('/jobs-for-international-graduates')
def international_graduates():
    # Note: You need to create a 'job_list.html' or similar template for this
    # For now, we are reusing remote_jobs logic or a generic list view
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['JOBS_PER_PAGE']
    
    query = Job.query.options(joinedload(Job.company)).filter_by(is_active=True).filter(
        (Job.visa_sponsorship == True) | (Job.is_remote == True)
    ).order_by(Job.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    jobs = pagination.items
    
    # Assuming a generic 'job_list.html' exists, or reuse existing structure
    return render_template('remote_jobs.html', 
                         remote_jobs=jobs, 
                         pagination=pagination,
                         title="Jobs for International Graduates")

@main_bp.route('/visa-sponsored-jobs')
def visa_sponsored_jobs():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['JOBS_PER_PAGE']
    
    query = Job.query.options(joinedload(Job.company), joinedload(Job.country))\
        .filter_by(is_active=True, visa_sponsorship=True)\
        .order_by(Job.created_at.desc())
        
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    jobs = pagination.items
    
    return render_template('remote_jobs.html', 
                         remote_jobs=jobs, 
                         pagination=pagination,
                         title="Visa Sponsored Jobs")
