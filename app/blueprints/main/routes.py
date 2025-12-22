# app/blueprints/main/routes.py

from flask import jsonify, request
from app.models.job import Job
from app.models.category import Category
from app.models.country import Country
from app.models.company import Company
from app import db
from . import main_bp

@main_bp.route('/')
def index():
    # TODO: Add Redis caching for homepage data
    
    latest_jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).limit(20).all()
    featured_categories = Category.query.filter_by(parent_id=None).limit(10).all()
    
    return jsonify({
        'page': 'homepage',
        'latest_jobs': [{'id': j.id, 'title': j.title, 'slug': j.slug, 'company': j.company.name} for j in latest_jobs],
        'featured_categories': [{'id': c.id, 'name': c.name, 'slug': c.slug} for c in featured_categories]
    })

@main_bp.route('/remote-jobs')
def remote_jobs():
    # TODO: Add Redis caching for remote jobs listing
    
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    remote_jobs_query = Job.query.filter_by(is_active=True, is_remote=True).order_by(Job.created_at.desc())
    pagination = remote_jobs_query.paginate(page=page, per_page=per_page, error_out=False)
    
    jobs = pagination.items
    
    return jsonify({
        'page': 'remote_jobs',
        'seo_title': 'Remote Jobs - Work From Anywhere',
        'jobs': [{'id': j.id, 'title': j.title, 'slug': j.slug, 'company': j.company.name} for j in jobs],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })

@main_bp.route('/jobs-for-international-graduates')
def international_graduates():
    # TODO: Add Redis caching for international graduate jobs
    
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    grad_jobs_query = Job.query.filter_by(is_active=True).filter(
        (Job.visa_sponsorship == True) | (Job.is_remote == True)
    ).order_by(Job.created_at.desc())
    
    pagination = grad_jobs_query.paginate(page=page, per_page=per_page, error_out=False)
    jobs = pagination.items
    
    return jsonify({
        'page': 'international_graduates',
        'seo_title': 'Jobs for International Graduates',
        'jobs': [{'id': j.id, 'title': j.title, 'slug': j.slug, 'company': j.company.name, 'visa_sponsorship': j.visa_sponsorship} for j in jobs],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })

@main_bp.route('/visa-sponsored-jobs')
def visa_sponsored_jobs():
    # TODO: Add Redis caching for visa sponsored jobs
    
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    visa_jobs_query = Job.query.filter_by(is_active=True, visa_sponsorship=True).order_by(Job.created_at.desc())
    pagination = visa_jobs_query.paginate(page=page, per_page=per_page, error_out=False)
    
    jobs = pagination.items
    
    return jsonify({
        'page': 'visa_sponsored_jobs',
        'seo_title': 'Visa Sponsored Jobs - Companies Offering Work Visas',
        'jobs': [{'id': j.id, 'title': j.title, 'slug': j.slug, 'company': j.company.name, 'country': j.country.name if j.country else None} for j in jobs],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })
