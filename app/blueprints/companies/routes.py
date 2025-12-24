# app/blueprints/companies/routes.py
from flask import render_template, request, abort, current_app
from app.models.company import Company
from app.models.job import Job
from sqlalchemy.orm import joinedload
from . import companies_bp

@companies_bp.route('/<company_slug>')
def company_profile(company_slug):
    company = Company.query.filter_by(slug=company_slug).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    jobs_query = Job.query.filter_by(is_active=True, company_id=company.id)\
        .order_by(Job.created_at.desc())
    
    pagination = jobs_query.paginate(page=page, per_page=per_page, error_out=False)
    jobs = pagination.items
    
    from app.seo.schema import generate_organization_schema
    company_schema = generate_organization_schema() # Adjust to pass specific company data if needed
    
    return render_template('company_detail.html', 
                         company=company, 
                         jobs=jobs, 
                         pagination=pagination,
                         company_schema=company_schema)
