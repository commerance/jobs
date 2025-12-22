# app/blueprints/companies/routes.py

from flask import jsonify, request
from app.models.company import Company
from app.models.job import Job
from app import db
from . import companies_bp

@companies_bp.route('/<company_slug>')
def company_profile(company_slug):
    # TODO: Add Redis caching for company profile
    
    company = Company.query.filter_by(slug=company_slug).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    jobs_query = Job.query.filter_by(is_active=True, company_id=company.id).order_by(Job.created_at.desc())
    pagination = jobs_query.paginate(page=page, per_page=per_page, error_out=False)
    
    jobs = pagination.items
    
    return jsonify({
        'page': 'company_profile',
        'company': {
            'id': company.id,
            'name': company.name,
            'slug': company.slug,
            'description': company.description,
            'website': company.website,
            'country': {
                'id': company.country.id,
                'name': company.country.name,
                'slug': company.country.slug
            } if company.country else None
        },
        'jobs': [{'id': j.id, 'title': j.title, 'slug': j.slug, 'category': j.category.name} for j in jobs],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })
