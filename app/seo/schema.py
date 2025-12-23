# app/seo/schema.py

import os
from datetime import datetime

BASE_URL = os.environ.get('BASE_URL', 'https://example.com')
ORGANIZATION_NAME = os.environ.get('ORGANIZATION_NAME', 'JobHunt Platform')
ORGANIZATION_LOGO = os.environ.get('ORGANIZATION_LOGO', f'{BASE_URL}/static/logo.png')

def generate_job_schema(job):
    schema = {
        '@context': 'https://schema.org',
        '@type': 'JobPosting',
        'title': job.title,
        'description': job.description,
        'datePosted': job.created_at.isoformat(),
        'identifier': {
            '@type': 'PropertyValue',
            'name': job.company.name if job.company else ORGANIZATION_NAME,
            'value': str(job.id)
        },
        'hiringOrganization': {
            '@type': 'Organization',
            'name': job.company.name if job.company else 'Unknown Company',
            'sameAs': job.company.website if job.company and job.company.website else None
        }
    }
    
    if job.expires_at:
        schema['validThrough'] = job.expires_at.isoformat()
    
    if job.is_remote:
        schema['jobLocationType'] = 'TELECOMMUTE'
        schema['applicantLocationRequirements'] = {
            '@type': 'Country',
            'name': 'Worldwide'
        }
    else:
        if job.country:
            job_location = {
                '@type': 'Place',
                'address': {
                    '@type': 'PostalAddress',
                    'addressCountry': job.country.iso_code
                }
            }
            
            if job.city:
                job_location['address']['addressLocality'] = job.city
            
            schema['jobLocation'] = job_location
            
            schema['applicantLocationRequirements'] = {
                '@type': 'Country',
                'name': job.country.name
            }
    
    if job.experience_level:
        schema['experienceRequirements'] = {
            '@type': 'OccupationalExperienceRequirements',
            'experienceLevel': job.experience_level
        }
    
    if job.degree_required:
        schema['educationRequirements'] = {
            '@type': 'EducationalOccupationalCredential',
            'credentialCategory': job.degree_required
        }
    
    if job.category:
        schema['industry'] = job.category.name
    
    employment_types = []
    if job.is_remote:
        employment_types.append('FULL_TIME')
    else:
        employment_types.append('FULL_TIME')
    
    if employment_types:
        schema['employmentType'] = employment_types
    
    return schema

def generate_blog_schema(post):
    schema = {
        '@context': 'https://schema.org',
        '@type': 'BlogPosting',
        'headline': post.title,
        'description': post.meta_description if post.meta_description else post.title,
        'datePublished': post.created_at.isoformat(),
        'dateModified': post.updated_at.isoformat(),
        'mainEntityOfPage': {
            '@type': 'WebPage',
            '@id': f"{BASE_URL}/blog/{post.slug}"
        },
        'author': {
            '@type': 'Organization',
            'name': ORGANIZATION_NAME
        },
        'publisher': {
            '@type': 'Organization',
            'name': ORGANIZATION_NAME,
            'logo': {
                '@type': 'ImageObject',
                'url': ORGANIZATION_LOGO
            }
        }
    }
    
    return schema

def generate_breadcrumb_schema(items):
    if not items:
        return None
    
    item_list_elements = []
    
    for index, item in enumerate(items, start=1):
        item_list_elements.append({
            '@type': 'ListItem',
            'position': index,
            'name': item['name'],
            'item': item['url']
        })
    
    schema = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': item_list_elements
    }
    
    return schema

def generate_organization_schema():
    schema = {
        '@context': 'https://schema.org',
        '@type': 'Organization',
        'name': ORGANIZATION_NAME,
        'url': BASE_URL,
        'logo': ORGANIZATION_LOGO,
        'sameAs': []
    }
    
    return schema

def generate_website_schema():
    schema = {
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        'name': ORGANIZATION_NAME,
        'url': BASE_URL,
        'potentialAction': {
            '@type': 'SearchAction',
            'target': {
                '@type': 'EntryPoint',
                'urlTemplate': f"{BASE_URL}/jobs?q={{search_term_string}}"
            },
            'query-input': 'required name=search_term_string'
        }
    }
    
    return schema
