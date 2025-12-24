# app/blueprints/blog/routes.py

from flask import render_template, request, current_app
from app.models.blog import BlogPost
from . import blog_bp

@blog_bp.route('/')
def blog_index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('BLOG_PER_PAGE', 10)
    
    posts_query = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_at.desc())
    pagination = posts_query.paginate(page=page, per_page=per_page, error_out=False)
    
    posts = pagination.items
    
    return render_template('blog_index.html', 
                         posts=posts, 
                         pagination=pagination,
                         title="Career Advice & Blog")

@blog_bp.route('/<post_slug>')
def blog_post_detail(post_slug):
    post = BlogPost.query.filter_by(slug=post_slug, is_published=True).first_or_404()
    
    recent_posts = BlogPost.query.filter_by(is_published=True).filter(
        BlogPost.id != post.id
    ).order_by(BlogPost.created_at.desc()).limit(3).all()
    
    # Generate SEO Schema
    from app.seo.schema import generate_blog_schema
    blog_schema = generate_blog_schema(post)
    
    return render_template('blog_detail.html', 
                         post=post, 
                         related_posts=recent_posts,
                         blog_schema=blog_schema)
