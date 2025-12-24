# app/blueprints/jobs/routes.py

from flask import render_template, request, abort, current_app
from app.models.job import Job
from app.models.category import Category
from app.models.country import Country
from app.models.company import Company
from sqlalchemy.orm import joinedload
from . import jobs_bp

@jobs_bp.route('/')
def all_jobs():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('JOBS_PER_PAGE', 50)
    
    remote = request.args.get('remote', type=str)
    visa = request.args.get('visa', type=str)
    experience = request.args.get('experience', type=str)
    
    # Eager load related data to prevent N+1 queries in the template
    query = Job.query.options(
        joinedload(Job.company),
        joinedload(Job.country),
        joinedload(Job.category)
    ).filter_by(is_active=True)
    
    if remote == 'true':
        query = query.filter_by(is_remote=True)
    
    if visa == 'true':
        query = query.filter_by(visa_sponsorship=True)
    
    if experience:
        query = query.filter_by(experience_level=experience)
    
    query = query.order_by(Job.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    jobs = pagination.items
    
    # Using remote_jobs.html as a generic list template
    # Ideally, you should duplicate remote_jobs.html to create a generic 'jobs/index.html'
    return render_template('remote_jobs.html', 
                         jobs=jobs, 
                         pagination=pagination, 
                         title="All Jobs")

@jobs_bp.route('/<category_slug>')
def jobs_by_category(category_slug):
    category = Category.query.filter_by(slug=category_slug).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('JOBS_PER_PAGE', 50)
    
    remote = request.args.get('remote', type=str)
    visa = request.args.get('visa', type=str)
    experience = request.args.get('experience', type=str)
    
    query = Job.query.options(
        joinedload(Job.company),
        joinedload(Job.country)
    ).filter_by(is_active=True, category_id=category.id)
    
    if remote == 'true':
        query = query.filter_by(is_remote=True)
    
    if visa == 'true':
        query = query.filter_by(visa_sponsorship=True)
    
    if experience:
        query = query.filter_by(experience_level=experience)
    
    query = query.order_by(Job.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    jobs = pagination.items
    
    return render_template('remote_jobs.html', 
                         jobs=jobs, 
                         pagination=pagination,
                         title=f"{category.name} Jobs",
                         category=category)

@jobs_bp.route('/<category_slug>/<sub_category_slug>')
def jobs_by_subcategory(category_slug, sub_category_slug):
    parent_category = Category.query.filter_by(slug=category_slug).first_or_404()
    sub_category = Category.query.filter_by(slug=sub_category_slug, parent_id=parent_category.id).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('JOBS_PER_PAGE', 50)
    
    remote = request.args.get('remote', type=str)
    visa = request.args.get('visa', type=str)
    experience = request.args.get('experience', type=str)
    
    query = Job.query.options(
        joinedload(Job.company),
        joinedload(Job.country)
    ).filter_by(is_active=True, category_id=sub_category.id)
    
    if remote == 'true':
        query = query.filter_by(is_remote=True)
    
    if visa == 'true':
        query = query.filter_by(visa_sponsorship=True)
    
    if experience:
        query = query.filter_by(experience_level=experience)
    
    query = query.order_by(Job.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    jobs = pagination.items
    
    return render_template('remote_jobs.html', 
                         jobs=jobs, 
                         pagination=pagination,
                         title=f"{sub_category.name} Jobs",
                         category=sub_category,
                         parent_category=parent_category)

@jobs_bp.route('/jobs-in/<country_slug>')
def jobs_by_country(country_slug):
    country = Country.query.filter_by(slug=country_slug).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('JOBS_PER_PAGE', 50)
    
    remote = request.args.get('remote', type=str)
    visa = request.args.get('visa', type=str)
    experience = request.args.get('experience', type=str)
    
    query = Job.query.options(
        joinedload(Job.company),
        joinedload(Job.category)
    ).filter_by(is_active=True, country_id=country.id)
    
    if remote == 'true':
        query = query.filter_by(is_remote=True)
    
    if visa == 'true':
        query = query.filter_by(visa_sponsorship=True)
    
    if experience:
        query = query.filter_by(experience_level=experience)
    
    query = query.order_by(Job.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    jobs = pagination.items
    
    return render_template('remote_jobs.html', 
                         jobs=jobs, 
                         pagination=pagination,
                         title=f"Jobs in {country.name}",
                         country=country)

@jobs_bp.route('/jobs-in/<country_slug>/<city>')
def jobs_by_city(country_slug, city):
    country = Country.query.filter_by(slug=country_slug).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('JOBS_PER_PAGE', 50)
    
    remote = request.args.get('remote', type=str)
    visa = request.args.get('visa', type=str)
    experience = request.args.get('experience', type=str)
    
    query = Job.query.options(
        joinedload(Job.company),
        joinedload(Job.category)
    ).filter_by(is_active=True, country_id=country.id, city=city)
    
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
        # Optional: Render a "no jobs found" page instead of 404
        pass
    
    return render_template('remote_jobs.html', 
                         jobs=jobs, 
                         pagination=pagination,
                         title=f"Jobs in {city}, {country.name}",
                         country=country,
                         city=city)

@jobs_bp.route('/job/<job_slug>')
def job_detail(job_slug):
    # Eager load all relationships for the detail page
    job = Job.query.options(
        joinedload(Job.company),
        joinedload(Job.category),
        joinedload(Job.country)
    ).filter_by(slug=job_slug, is_active=True).first_or_404()
    
    related_jobs = Job.query.options(
        joinedload(Job.company),
        joinedload(Job.country)
    ).filter_by(
        is_active=True,
        category_id=job.category_id
    ).filter(Job.id != job.id).limit(5).all()
    
    # Generate Schema.org JSON-LD
    from app.seo.schema import generate_job_schema
    job_schema = generate_job_schema(job)
    
    return render_template('job_detail.html', 
                         job=job, 
                         related_jobs=related_jobs,
                         job_schema=job_schema)
