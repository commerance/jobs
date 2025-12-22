# app/blueprints/blog/routes.py

from flask import jsonify, request
from app.models.blog import BlogPost
from app import db
from . import blog_bp

@blog_bp.route('/')
def blog_index():
    # TODO: Add Redis caching for blog index
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    posts_query = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_at.desc())
    pagination = posts_query.paginate(page=page, per_page=per_page, error_out=False)
    
    posts = pagination.items
    
    return jsonify({
        'page': 'blog_index',
        'posts': [{
            'id': p.id,
            'title': p.title,
            'slug': p.slug,
            'meta_description': p.meta_description,
            'created_at': p.created_at.isoformat()
        } for p in posts],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })

@blog_bp.route('/<post_slug>')
def blog_post_detail(post_slug):
    # TODO: Add Redis caching for blog post detail
    
    post = BlogPost.query.filter_by(slug=post_slug, is_published=True).first_or_404()
    
    recent_posts = BlogPost.query.filter_by(is_published=True).filter(
        BlogPost.id != post.id
    ).order_by(BlogPost.created_at.desc()).limit(5).all()
    
    return jsonify({
        'page': 'blog_post_detail',
        'post': {
            'id': post.id,
            'title': post.title,
            'slug': post.slug,
            'content': post.content,
            'meta_title': post.meta_title,
            'meta_description': post.meta_description,
            'created_at': post.created_at.isoformat(),
            'updated_at': post.updated_at.isoformat()
        },
        'recent_posts': [{
            'id': p.id,
            'title': p.title,
            'slug': p.slug
        } for p in recent_posts]
    })
