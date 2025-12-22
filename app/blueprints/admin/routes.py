# app/blueprints/admin/routes.py

from flask import jsonify, request, abort
from app.models.job import Job
from app.models.company import Company
from app.models.blog import BlogPost
from app.models.category import Category
from app.models.country import Country
from app import db
from datetime import datetime
from . import admin_bp

@admin_bp.route('/')
def dashboard():
    total_jobs = Job.query.count()
    active_jobs = Job.query.filter_by(is_active=True).count()
    total_companies = Company.query.count()
    total_posts = BlogPost.query.count()
    
    return jsonify({
        'page': 'admin_dashboard',
        'stats': {
            'total_jobs': total_jobs,
            'active_jobs': active_jobs,
            'total_companies': total_companies,
            'total_posts': total_posts
        }
    })

@admin_bp.route('/jobs')
def list_jobs():
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    jobs_query = Job.query.order_by(Job.created_at.desc())
    pagination = jobs_query.paginate(page=page, per_page=per_page, error_out=False)
    
    jobs = pagination.items
    
    return jsonify({
        'page': 'admin_jobs',
        'jobs': [{
            'id': j.id,
            'title': j.title,
            'slug': j.slug,
            'company': j.company.name,
            'is_active': j.is_active,
            'created_at': j.created_at.isoformat()
        } for j in jobs],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })

@admin_bp.route('/jobs/create', methods=['POST'])
def create_job():
    data = request.get_json()
    
    job = Job(
        title=data['title'],
        slug=data['slug'],
        description=data['description'],
        responsibilities=data.get('responsibilities'),
        requirements=data.get('requirements'),
        country_id=data.get('country_id'),
        city=data.get('city'),
        is_remote=data.get('is_remote', False),
        visa_sponsorship=data.get('visa_sponsorship', False),
        experience_level=data.get('experience_level'),
        degree_required=data.get('degree_required'),
        category_id=data['category_id'],
        company_id=data['company_id'],
        is_active=data.get('is_active', True),
        expires_at=datetime.fromisoformat(data['expires_at']) if data.get('expires_at') else None
    )
    
    db.session.add(job)
    db.session.commit()
    
    return jsonify({
        'message': 'Job created successfully',
        'job_id': job.id
    }), 201

@admin_bp.route('/jobs/<int:job_id>/edit', methods=['PUT'])
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    data = request.get_json()
    
    job.title = data.get('title', job.title)
    job.slug = data.get('slug', job.slug)
    job.description = data.get('description', job.description)
    job.responsibilities = data.get('responsibilities', job.responsibilities)
    job.requirements = data.get('requirements', job.requirements)
    job.country_id = data.get('country_id', job.country_id)
    job.city = data.get('city', job.city)
    job.is_remote = data.get('is_remote', job.is_remote)
    job.visa_sponsorship = data.get('visa_sponsorship', job.visa_sponsorship)
    job.experience_level = data.get('experience_level', job.experience_level)
    job.degree_required = data.get('degree_required', job.degree_required)
    job.category_id = data.get('category_id', job.category_id)
    job.company_id = data.get('company_id', job.company_id)
    job.is_active = data.get('is_active', job.is_active)
    
    if data.get('expires_at'):
        job.expires_at = datetime.fromisoformat(data['expires_at'])
    
    job.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Job updated successfully',
        'job_id': job.id
    })

@admin_bp.route('/jobs/<int:job_id>/delete', methods=['DELETE'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    db.session.delete(job)
    db.session.commit()
    
    return jsonify({
        'message': 'Job deleted successfully'
    })

@admin_bp.route('/companies')
def list_companies():
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    companies_query = Company.query.order_by(Company.created_at.desc())
    pagination = companies_query.paginate(page=page, per_page=per_page, error_out=False)
    
    companies = pagination.items
    
    return jsonify({
        'page': 'admin_companies',
        'companies': [{
            'id': c.id,
            'name': c.name,
            'slug': c.slug,
            'website': c.website,
            'created_at': c.created_at.isoformat()
        } for c in companies],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })

@admin_bp.route('/companies/create', methods=['POST'])
def create_company():
    data = request.get_json()
    
    company = Company(
        name=data['name'],
        slug=data['slug'],
        description=data.get('description'),
        website=data.get('website'),
        country_id=data.get('country_id')
    )
    
    db.session.add(company)
    db.session.commit()
    
    return jsonify({
        'message': 'Company created successfully',
        'company_id': company.id
    }), 201

@admin_bp.route('/blog')
def list_blog_posts():
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    posts_query = BlogPost.query.order_by(BlogPost.created_at.desc())
    pagination = posts_query.paginate(page=page, per_page=per_page, error_out=False)
    
    posts = pagination.items
    
    return jsonify({
        'page': 'admin_blog',
        'posts': [{
            'id': p.id,
            'title': p.title,
            'slug': p.slug,
            'is_published': p.is_published,
            'created_at': p.created_at.isoformat()
        } for p in posts],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })

@admin_bp.route('/blog/create', methods=['POST'])
def create_blog_post():
    data = request.get_json()
    
    post = BlogPost(
        title=data['title'],
        slug=data['slug'],
        content=data['content'],
        meta_title=data.get('meta_title'),
        meta_description=data.get('meta_description'),
        is_published=data.get('is_published', False)
    )
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify({
        'message': 'Blog post created successfully',
        'post_id': post.id
    }), 201
