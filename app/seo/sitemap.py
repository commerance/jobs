# app/seo/sitemap.py

import os
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from app.models.job import Job
from app.models.blog import BlogPost
from app.models.category import Category
from app.models.country import Country

BASE_URL = os.environ.get('BASE_URL', 'https://example.com')

def generate_static_urls():
    urls = []
    
    static_pages = [
        {'loc': '/', 'changefreq': 'daily', 'priority': '1.0'},
        {'loc': '/remote-jobs', 'changefreq': 'daily', 'priority': '0.9'},
        {'loc': '/jobs-for-international-graduates', 'changefreq': 'daily', 'priority': '0.9'},
        {'loc': '/visa-sponsored-jobs', 'changefreq': 'daily', 'priority': '0.9'},
    ]
    
    for page in static_pages:
        urls.append({
            'loc': f"{BASE_URL}{page['loc']}",
            'lastmod': datetime.utcnow().strftime('%Y-%m-%d'),
            'changefreq': page['changefreq'],
            'priority': page['priority']
        })
    
    return urls

def generate_category_urls():
    urls = []
    
    categories = Category.query.filter_by(parent_id=None).all()
    
    for category in categories:
        urls.append({
            'loc': f"{BASE_URL}/jobs/{category.slug}",
            'lastmod': category.updated_at.strftime('%Y-%m-%d'),
            'changefreq': 'daily',
            'priority': '0.8'
        })
        
        subcategories = Category.query.filter_by(parent_id=category.id).all()
        for sub in subcategories:
            urls.append({
                'loc': f"{BASE_URL}/jobs/{category.slug}/{sub.slug}",
                'lastmod': sub.updated_at.strftime('%Y-%m-%d'),
                'changefreq': 'daily',
                'priority': '0.7'
            })
    
    return urls

def generate_country_urls():
    urls = []
    
    countries = Country.query.all()
    
    for country in countries:
        urls.append({
            'loc': f"{BASE_URL}/jobs/jobs-in/{country.slug}",
            'lastmod': country.updated_at.strftime('%Y-%m-%d'),
            'changefreq': 'daily',
            'priority': '0.8'
        })
    
    return urls

def generate_job_urls():
    urls = []
    
    jobs = Job.query.filter_by(is_active=True).all()
    
    for job in jobs:
        urls.append({
            'loc': f"{BASE_URL}/jobs/job/{job.slug}",
            'lastmod': job.updated_at.strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '0.6'
        })
    
    return urls

def generate_blog_urls():
    urls = []
    
    posts = BlogPost.query.filter_by(is_published=True).all()
    
    for post in posts:
        urls.append({
            'loc': f"{BASE_URL}/blog/{post.slug}",
            'lastmod': post.updated_at.strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.5'
        })
    
    return urls

def generate_sitemap():
    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    all_urls = []
    all_urls.extend(generate_static_urls())
    all_urls.extend(generate_category_urls())
    all_urls.extend(generate_country_urls())
    all_urls.extend(generate_job_urls())
    all_urls.extend(generate_blog_urls())
    
    for url_data in all_urls:
        url = SubElement(urlset, 'url')
        
        loc = SubElement(url, 'loc')
        loc.text = url_data['loc']
        
        lastmod = SubElement(url, 'lastmod')
        lastmod.text = url_data['lastmod']
        
        changefreq = SubElement(url, 'changefreq')
        changefreq.text = url_data['changefreq']
        
        priority = SubElement(url, 'priority')
        priority.text = url_data['priority']
    
    xml_string = tostring(urlset, encoding='unicode', method='xml')
    return f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_string}'
