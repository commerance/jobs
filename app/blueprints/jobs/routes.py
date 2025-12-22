# app/blueprints/jobs/routes.py

from flask import jsonify, request, abort
from app.models.job import Job
from app.models.category import Category
from app.models.country import Country
from app.models.company import Company
from app import db
from . import jobs_bp

@jobs_bp.route('/')
def all_jobs():
    # TODO: Add Redis caching for all jobs listing
    
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    remote = request.args.get('remote', type=str)
    visa = request.args.get('visa', type=str)
    experience = request.args.get('experience', type=str)
    
    query = Job.query.filter_by(is_active=True)
    
    if remote == 'true':
        query = query.filter_by(is_remote=True)
    
    if visa == 'true':
        query = query.filter_by(visa_sponsorship=True)
    
    if experience:
        query = query.filter_by(experience_level=experience)
    
    query = query.order_by(Job.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    jobs = pagination.items
    
    return jsonify({
        'page': 'all_jobs',
        'jobs': [{'id': j.id, 'title': j.title, 'slug': j.slug, 'company': j.company.name} for j in jobs],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })

@jobs_bp.route('/<category_slug>')
def jobs_by_category(category_slug):
    # TODO: Add Redis caching for category jobs
    
    category = Category.query.filter_by(slug=category_slug).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    remote = request.args.get('remote', type=str)
    visa = request.args.get('visa', type=str)
    experience = request.args.get('experience', type=str)
    
    query = Job.query.filter_by(is_active=True, category_id=category.id)
    
    if remote == 'true':
        query = query.filter_by(is_remote=True)
    
    if visa == 'true':
        query = query.filter_by(visa_sponsorship=True)
    
    if experience:
        query = query.filter_by(experience_level=experience)
    
    query = query.order_by(Job.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    jobs = pagination.items
    
    return jsonify({
        'page': 'jobs_by_category',
        'category': {'id': category.id, 'name': category.name, 'slug': category.slug},
        'jobs': [{'id': j.id, 'title': j.title, 'slug': j.slug, 'company': j.company.name} for j in jobs],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })

@jobs_bp.route('/<category_slug>/<sub_category_slug>')
def jobs_by_subcategory(category_slug, sub_category_slug):
    # TODO: Add Redis caching for subcategory jobs
    
    parent_category = Category.query.filter_by(slug=category_slug).first_or_404()
    sub_category = Category.query.filter_by(slug=sub_category_slug, parent_id=parent_category.id).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    remote = request.args.get('remote', type=str)
    visa = request.args.get('visa', type=str)
    experience = request.args.get('experience', type=str)
    
    query = Job.query.filter_by(is_active=True, category_id=sub_category.id)
    
    if remote == 'true':
        query = query.filter_by(is_remote=True)
    
    if visa == 'true':
        query = query.filter_by(visa_sponsorship=True)
    
    if experience:
        query = query.filter_by(experience_level=experience)
    
    query = query.order_by(Job.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    jobs = pagination.items
    
    return jsonify({
        'page': 'jobs_by_subcategory',
        'parent_category': {'id': parent_category.id, 'name': parent_category.name, 'slug': parent_category.slug},
        'sub_category': {'id': sub_category.id, 'name': sub_category.name, 'slug': sub_category.slug},
        'jobs': [{'id': j.id, 'title': j.title, 'slug': j.slug, 'company': j.company.name} for j in jobs],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })

@jobs_bp.route('/jobs-in/<country_slug>')
def jobs_by_country(country_slug):
    # TODO: Add Redis caching for country jobs
    
    country = Country.query.filter_by(slug=country_slug).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    remote = request.args.get('remote', type=str)
    visa = request.args.get('visa', type=str)
    experience = request.args.get('experience', type=str)
    
    query = Job.query.filter_by(is_active=True, country_id=country.id)
    
    if remote == 'true':
        query = query.filter_by(is_remote=True)
    
    if visa == 'true':
        query = query.filter_by(visa_sponsorship=True)
    
    if experience:
        query = query.filter_by(experience_level=experience)
    
    query = query.order_by(Job.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    jobs = pagination.items
    
    return jsonify({
        'page': 'jobs_by_country',
        'country': {'id': country.id, 'name': country.name, 'slug': country.slug},
        'jobs': [{'id': j.id, 'title': j.title, 'slug': j.slug, 'company': j.company.name, 'city': j.city} for j in jobs],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })

@jobs_bp.route('/jobs-in/<country_slug>/<city>')
def jobs_by_city(country_slug, city):
    # TODO: Add Redis caching for city jobs
    
    country = Country.query.filter_by(slug=country_slug).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    remote = request.args.get('remote', type=str)
    visa = request.args.get('visa', type=str)
    experience = request.args.get('experience', type=str)
    
    query = Job.query.filter_by(is_active=True, country_id=country.id, city=city)
    
    if remote == 'true':
        query = query.filter_by(is_remote=True)
    
    if visa == 'true':
        query = query.filter_by(visa_sponsorship=True)
    
    if experience:
        query = query.filter_by(experience_level=experience)
    
    query = query.order_by(Job.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    jobs = pagination.items
    
    if not jobs and page == 1:
        abort(404)
    
    return jsonify({
        'page': 'jobs_by_city',
        'country': {'id': country.id, 'name': country.name, 'slug': country.slug},
        'city': city,
        'jobs': [{'id': j.id, 'title': j.title, 'slug': j.slug, 'company': j.company.name} for j in jobs],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })

@jobs_bp.route('/job/<job_slug>')
def job_detail(job_slug):
    # TODO: Add Redis caching for job detail page
    
    job = Job.query.filter_by(slug=job_slug, is_active=True).first_or_404()
    
    related_jobs = Job.query.filter_by(
        is_active=True,
        category_id=job.category_id
    ).filter(Job.id != job.id).limit(5).all()
    
    return jsonify({
        'page': 'job_detail',
        'job': {
            'id': job.id,
            'title': job.title,
            'slug': job.slug,
            'description': job.description,
            'responsibilities': job.responsibilities,
            'requirements': job.requirements,
            'company': {
                'id': job.company.id,
                'name': job.company.name,
                'slug': job.company.slug,
                'website': job.company.website
            },
            'category': {
                'id': job.category.id,
                'name': job.category.name,
                'slug': job.category.slug
            },
            'country': {
                'id': job.country.id,
                'name': job.country.name,
                'slug': job.country.slug
            } if job.country else None,
            'city': job.city,
            'is_remote': job.is_remote,
            'visa_sponsorship': job.visa_sponsorship,
            'experience_level': job.experience_level,
            'degree_required': job.degree_required,
            'created_at': job.created_at.isoformat(),
            'expires_at': job.expires_at.isoformat() if job.expires_at else None
        },
        'related_jobs': [{'id': j.id, 'title': j.title, 'slug': j.slug, 'company': j.company.name} for j in related_jobs]
    })
