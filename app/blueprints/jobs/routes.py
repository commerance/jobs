# app/blueprints/jobs/routes.py
from flask import render_template, request, abort, current_app
from app.models.job import Job
from app.models.category import Category
from app.models.country import Country
from sqlalchemy.orm import joinedload
from . import jobs_bp

@jobs_bp.route('/')
def all_jobs():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['JOBS_PER_PAGE']
    
    # Filter logic (simplified for brevity, keep your existing filter logic)
    query = Job.query.options(joinedload(Job.company)).filter_by(is_active=True)
    # ... (Add your remote/visa/experience filters here) ...
    
    query = query.order_by(Job.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    jobs = pagination.items
    
    # You need a generic job list template here. 
    # If you don't have 'jobs/index.html', create it based on remote_jobs.html
    return render_template('remote_jobs.html', jobs=jobs, pagination=pagination, title="All Jobs")

@jobs_bp.route('/job/<job_slug>')
def job_detail(job_slug):
    job = Job.query.options(
        joinedload(Job.company), 
        joinedload(Job.category), 
        joinedload(Job.country)
    ).filter_by(slug=job_slug, is_active=True).first_or_404()
    
    related_jobs = Job.query.options(joinedload(Job.company)).filter_by(
        is_active=True,
        category_id=job.category_id
    ).filter(Job.id != job.id).limit(5).all()
    
    # SEO Schema generation (optional, if you have the helper function)
    from app.seo.schema import generate_job_schema
    job_schema = generate_job_schema(job)
    
    return render_template('job_detail.html', 
                         job=job, 
                         related_jobs=related_jobs,
                         job_schema=job_schema)

# ... (Apply similar render_template changes to category/country routes) ...
