#!/usr/bin/env python3
"""
African AI Strategies Portal - Vercel Serverless Function
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
from pathlib import Path

# Get absolute paths for better compatibility
try:
    BASE_DIR = Path(__file__).parent.parent
    TEMPLATE_DIR = str(BASE_DIR / 'templates')
    STATIC_DIR = str(BASE_DIR / 'static')
except Exception:
    # Fallback for serverless environment
    TEMPLATE_DIR = '../templates'
    STATIC_DIR = '../static'

# Initialize Flask app with proper paths for Vercel
app = Flask(__name__,
           template_folder=TEMPLATE_DIR,
           static_folder=STATIC_DIR,
           static_url_path='/static')
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Sample data for demo
COUNTRIES_DATA = [
    {"code": "KE", "name": "Kenya", "status": "published"},
    {"code": "NG", "name": "Nigeria", "status": "published"},
    {"code": "ZA", "name": "South Africa", "status": "published"},
    {"code": "EG", "name": "Egypt", "status": "published"},
    {"code": "MA", "name": "Morocco", "status": "draft"},
    {"code": "GH", "name": "Ghana", "status": "draft"},
    {"code": "RW", "name": "Rwanda", "status": "published"},
    {"code": "TN", "name": "Tunisia", "status": "under_development"}
]

THEMES_DATA = [
    {"name": "Skills Development", "frequency": 8, "countries": ["KE", "NG", "ZA", "EG", "MA", "GH", "RW", "TN"], "percentage": 100.0},
    {"name": "Innovation", "frequency": 7, "countries": ["KE", "NG", "ZA", "EG", "MA", "GH", "RW"], "percentage": 87.5},
    {"name": "Infrastructure", "frequency": 6, "countries": ["KE", "NG", "ZA", "EG", "RW", "TN"], "percentage": 75.0},
    {"name": "Agriculture", "frequency": 6, "countries": ["KE", "NG", "ZA", "MA", "GH", "RW"], "percentage": 75.0},
    {"name": "Healthcare", "frequency": 5, "countries": ["KE", "NG", "ZA", "EG", "RW"], "percentage": 62.5},
    {"name": "Education", "frequency": 5, "countries": ["KE", "NG", "ZA", "GH", "TN"], "percentage": 62.5},
    {"name": "Ethics", "frequency": 4, "countries": ["KE", "ZA", "EG", "MA"], "percentage": 50.0},
    {"name": "Financial Services", "frequency": 4, "countries": ["KE", "NG", "ZA", "RW"], "percentage": 50.0}
]

# Sample Kenya strategy data
KENYA_STRATEGY = {
    "country_code": "KE",
    "country_name": "Kenya",
    "strategy_title": "Kenya National Artificial Intelligence Strategy 2022-2027",
    "publication_date": "2022-03-15",
    "status": "published",
    "vision": "To be a globally competitive AI-driven economy that harnesses artificial intelligence for sustainable development",
    "mission": "To create an enabling environment for AI development, adoption, and innovation that drives economic growth and improves quality of life for all Kenyans",
    "strategic_pillars": [
        {
            "name": "AI Infrastructure and Ecosystem",
            "description": "Building robust digital infrastructure and creating an enabling environment for AI development",
            "key_initiatives": [
                "National AI Research Institute",
                "AI Innovation Hubs",
                "Digital Infrastructure Development",
                "Public-Private Partnerships"
            ]
        },
        {
            "name": "Human Capital Development",
            "description": "Developing AI skills and capabilities across all sectors of society",
            "key_initiatives": [
                "AI Education Curriculum",
                "Professional Training Programs",
                "Research Scholarships",
                "Industry-Academia Collaboration"
            ]
        },
        {
            "name": "AI for Development",
            "description": "Leveraging AI to address development challenges and improve service delivery",
            "key_initiatives": [
                "AI in Healthcare",
                "Smart Agriculture Solutions",
                "Digital Government Services",
                "Financial Inclusion"
            ]
        },
        {
            "name": "Ethics and Governance",
            "description": "Ensuring responsible AI development and deployment",
            "key_initiatives": [
                "AI Ethics Framework",
                "Regulatory Sandbox",
                "Data Protection Measures",
                "Algorithmic Accountability"
            ]
        }
    ],
    "key_sectors": [
        "Healthcare", "Agriculture", "Education", "Financial Services", 
        "Manufacturing", "Transportation", "Energy", "Government"
    ],
    "timeline": {
        "2022": "Strategy Launch and Foundation Setting",
        "2023": "Infrastructure Development and Pilot Programs",
        "2024": "Scaling and Implementation",
        "2025": "Expansion and Integration",
        "2026": "Optimization and Enhancement",
        "2027": "Evaluation and Next Phase Planning"
    }
}

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', 
                         countries=COUNTRIES_DATA, 
                         themes=THEMES_DATA)

@app.route('/api/countries')
def api_countries():
    """API endpoint for countries data"""
    return jsonify(COUNTRIES_DATA)

@app.route('/api/themes')
def api_themes():
    """API endpoint for themes data"""
    return jsonify(THEMES_DATA)

@app.route('/api/country/<country_code>')
def api_country_detail(country_code):
    """API endpoint for specific country data"""
    if country_code.upper() == 'KE':
        return jsonify(KENYA_STRATEGY)
    else:
        # Return basic info for other countries
        country = next((c for c in COUNTRIES_DATA if c['code'] == country_code.upper()), None)
        if country:
            return jsonify({
                "country_code": country['code'],
                "country_name": country['name'],
                "status": country['status'],
                "message": "Detailed strategy data coming soon!"
            })
        else:
            return jsonify({"error": "Country not found"}), 404

@app.route('/country/<country_code>')
def country_detail(country_code):
    """Country detail page"""
    if country_code.upper() == 'KE':
        return render_template('country.html', strategy=KENYA_STRATEGY)
    else:
        country = next((c for c in COUNTRIES_DATA if c['code'] == country_code.upper()), None)
        if country:
            return render_template('country.html', 
                                 strategy={
                                     "country_code": country['code'],
                                     "country_name": country['name'],
                                     "status": country['status'],
                                     "message": "Detailed strategy analysis coming soon!"
                                 })
        else:
            return render_template('404.html'), 404

@app.route('/compare')
def compare():
    """Strategy comparison page"""
    return render_template('compare.html', countries=COUNTRIES_DATA)

@app.route('/api/compare')
def api_compare():
    """API endpoint for comparison data"""
    return jsonify({
        "countries": COUNTRIES_DATA,
        "themes": THEMES_DATA,
        "comparison_matrix": {
            "themes": [theme["name"] for theme in THEMES_DATA],
            "countries": [country["code"] for country in COUNTRIES_DATA if country["status"] == "published"]
        }
    })

@app.route('/search')
def search():
    """Search page"""
    return render_template('search.html')

@app.route('/api/search')
def api_search():
    """API endpoint for search functionality"""
    query = request.args.get('q', '').lower()
    results = []
    
    # Search in countries
    for country in COUNTRIES_DATA:
        if query in country['name'].lower():
            results.append({
                "type": "country",
                "title": country['name'],
                "url": f"/country/{country['code']}",
                "description": f"AI Strategy - {country['status'].replace('_', ' ').title()}"
            })
    
    # Search in themes
    for theme in THEMES_DATA:
        if query in theme['name'].lower():
            results.append({
                "type": "theme",
                "title": theme['name'],
                "url": f"/themes#{theme['name'].lower().replace(' ', '-')}",
                "description": f"Found in {theme['frequency']} countries ({theme['percentage']:.1f}%)"
            })
    
    return jsonify({"query": query, "results": results})

@app.route('/analysis')
def analysis():
    """Analysis and insights page"""
    return render_template('analysis.html', themes=THEMES_DATA)

@app.route('/api/analysis')
def api_analysis():
    """API endpoint for analysis data"""
    return jsonify({
        "themes_analysis": THEMES_DATA,
        "country_status": {
            "published": len([c for c in COUNTRIES_DATA if c['status'] == 'published']),
            "draft": len([c for c in COUNTRIES_DATA if c['status'] == 'draft']),
            "under_development": len([c for c in COUNTRIES_DATA if c['status'] == 'under_development'])
        },
        "regional_insights": {
            "total_countries": len(COUNTRIES_DATA),
            "coverage_percentage": 75.0,
            "top_themes": THEMES_DATA[:5]
        }
    })

@app.route('/network')
def network():
    """Network visualization page"""
    return render_template('network.html')

@app.route('/api/network')
def api_network():
    """API endpoint for network visualization data"""
    nodes = []
    links = []
    
    # Add country nodes
    for country in COUNTRIES_DATA:
        nodes.append({
            "id": country['code'],
            "name": country['name'],
            "type": "country",
            "status": country['status']
        })
    
    # Add theme nodes
    for theme in THEMES_DATA:
        nodes.append({
            "id": theme['name'],
            "name": theme['name'],
            "type": "theme",
            "frequency": theme['frequency']
        })
        
        # Add links between themes and countries
        for country_code in theme['countries']:
            links.append({
                "source": country_code,
                "target": theme['name'],
                "type": "implements"
            })
    
    return jsonify({"nodes": nodes, "links": links})

@app.route('/timeline')
def timeline():
    """Timeline visualization page"""
    return render_template('timeline.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# For Vercel serverless deployment
from werkzeug.middleware.proxy_fix import ProxyFix

# Apply ProxyFix middleware for better Vercel compatibility
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

if __name__ == '__main__':
    app.run(debug=True)

# Export the Flask app for Vercel
# This is the key for Vercel to recognize the app
def handler(event, context):
    return app

# Make sure the app is available at module level
application = app
