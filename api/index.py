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

# Initialize Flask app with proper paths for Vercel
app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

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
            "description": "Develop robust digital infrastructure and supportive ecosystem for AI",
            "key_actions": [
                "Expand broadband connectivity nationwide",
                "Establish AI research centers",
                "Create AI innovation hubs",
                "Develop data governance frameworks"
            ]
        },
        {
            "name": "Human Capital Development",
            "description": "Build AI skills and capabilities across all sectors",
            "key_actions": [
                "Integrate AI in education curriculum",
                "Establish AI training programs",
                "Support AI research and development",
                "Create AI certification programs"
            ]
        }
    ],
    "priority_sectors": [
        {
            "name": "Agriculture",
            "ai_applications": ["Precision farming", "Crop monitoring", "Market intelligence"],
            "expected_impact": "Increase agricultural productivity by 30%"
        },
        {
            "name": "Healthcare",
            "ai_applications": ["Medical diagnosis", "Drug discovery", "Telemedicine"],
            "expected_impact": "Improve healthcare access and quality"
        }
    ],
    "key_initiatives": [
        {
            "name": "Kenya AI Innovation Hub",
            "description": "Establish world-class AI research and innovation center",
            "budget": "USD 50 million",
            "timeline": {"start": "2022", "end": "2025"},
            "expected_outcomes": ["100 AI startups incubated", "500 AI researchers trained"]
        }
    ],
    "funding_strategy": {
        "total_budget": "USD 200 million over 5 years"
    }
}

@app.route('/')
def index():
    """Main dashboard page"""
    countries = COUNTRIES_DATA
    stats = {
        'total_countries': len(countries),
        'total_strategies': len([c for c in countries if c['status'] == 'published']),
        'last_updated': datetime.now().strftime('%Y-%m-%d')
    }
    return render_template('index.html', countries=countries, stats=stats)

@app.route('/country/<country_code>')
def country_detail(country_code):
    """Individual country strategy page"""
    if country_code == 'KE':
        return render_template('country.html', country=KENYA_STRATEGY)
    else:
        return render_template('404.html'), 404

@app.route('/api/countries')
def api_countries():
    """API endpoint for countries list"""
    return jsonify(COUNTRIES_DATA)

@app.route('/api/country/<country_code>/strategy')
def api_country_strategy(country_code):
    """API endpoint for country strategy data"""
    if country_code == 'KE':
        return jsonify(KENYA_STRATEGY)
    return jsonify({'error': 'Country not found'}), 404

@app.route('/api/cross-cutting')
def api_cross_cutting():
    """API endpoint for cross-cutting analysis"""
    analysis = {
        "analysis_date": datetime.now().isoformat(),
        "countries_analyzed": [c["code"] for c in COUNTRIES_DATA],
        "total_themes": len(THEMES_DATA),
        "theme_analysis": {theme["name"]: {
            "countries": theme["countries"],
            "frequency": theme["frequency"],
            "percentage": theme["percentage"],
            "related_themes": [],
            "key_initiatives": [],
            "common_approaches": []
        } for theme in THEMES_DATA},
        "insights": [
            "Skills Development is the most universal theme across all African AI strategies",
            "Innovation and Infrastructure are prioritized by 75%+ of countries",
            "Agriculture remains a key focus area for most African nations"
        ],
        "collaboration_opportunities": [
            {
                "theme": "Skills Development",
                "countries": ["KE", "NG", "ZA", "EG", "MA", "GH", "RW", "TN"],
                "collaboration_type": "Joint training programs and certification",
                "potential_impact": "High"
            }
        ]
    }
    return jsonify(analysis)

@app.route('/api/mind-map/<country_code>')
def api_mind_map(country_code):
    """API endpoint for mind map data"""
    if country_code == 'KE':
        mind_map_data = {
            "name": "Kenya AI Strategy",
            "type": "root",
            "children": [
                {
                    "name": "Strategic Pillars",
                    "type": "category",
                    "children": [
                        {"name": "AI Infrastructure", "type": "pillar", "size": 3},
                        {"name": "Human Capital", "type": "pillar", "size": 3},
                        {"name": "Innovation", "type": "pillar", "size": 3},
                        {"name": "Ethics & Governance", "type": "pillar", "size": 3}
                    ]
                },
                {
                    "name": "Priority Sectors",
                    "type": "category",
                    "children": [
                        {"name": "Agriculture", "type": "sector", "size": 2},
                        {"name": "Healthcare", "type": "sector", "size": 2},
                        {"name": "Education", "type": "sector", "size": 2},
                        {"name": "Financial Services", "type": "sector", "size": 2}
                    ]
                }
            ]
        }
        return jsonify(mind_map_data)
    return jsonify({'error': 'Country not found'}), 404

@app.route('/api/themes')
def api_themes():
    """API endpoint for all themes"""
    return jsonify(THEMES_DATA)

@app.route('/compare')
def compare():
    """Strategy comparison page"""
    return render_template('compare.html', countries=COUNTRIES_DATA)

@app.route('/analysis')
def analysis():
    """Cross-cutting analysis page"""
    return render_template('analysis.html', themes=THEMES_DATA)

@app.route('/search')
def search():
    """Search page"""
    return render_template('search.html')

@app.route('/network')
def network():
    """Network visualization page"""
    return render_template('network.html')

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
if __name__ == '__main__':
    app.run(debug=True)

# Export the Flask app for Vercel
# This is the key for Vercel to recognize the app
def handler(event, context):
    return app

# Make sure the app is available at module level
application = app
