#!/usr/bin/env python3
"""
African AI Strategies Portal - Main Flask Application
Interactive web portal for exploring National AI Strategies across Africa
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DATA_PATH'] = 'data'

# Initialize demo data for Vercel deployment
def load_demo_data():
    """Load demo data for the application"""
    demo_data_path = Path('data/demo')
    
    # Sample countries data
    countries_data = [
        {"code": "KE", "name": "Kenya", "status": "published"},
        {"code": "NG", "name": "Nigeria", "status": "published"},
        {"code": "ZA", "name": "South Africa", "status": "published"},
        {"code": "EG", "name": "Egypt", "status": "published"},
        {"code": "MA", "name": "Morocco", "status": "draft"},
        {"code": "GH", "name": "Ghana", "status": "draft"},
        {"code": "RW", "name": "Rwanda", "status": "published"},
        {"code": "TN", "name": "Tunisia", "status": "under_development"}
    ]
    
    # Sample themes data
    themes_data = [
        {"name": "Skills Development", "frequency": 8, "countries": ["KE", "NG", "ZA", "EG", "MA", "GH", "RW", "TN"], "percentage": 100.0},
        {"name": "Innovation", "frequency": 7, "countries": ["KE", "NG", "ZA", "EG", "MA", "GH", "RW"], "percentage": 87.5},
        {"name": "Infrastructure", "frequency": 6, "countries": ["KE", "NG", "ZA", "EG", "RW", "TN"], "percentage": 75.0},
        {"name": "Agriculture", "frequency": 6, "countries": ["KE", "NG", "ZA", "MA", "GH", "RW"], "percentage": 75.0},
        {"name": "Healthcare", "frequency": 5, "countries": ["KE", "NG", "ZA", "EG", "RW"], "percentage": 62.5},
        {"name": "Education", "frequency": 5, "countries": ["KE", "NG", "ZA", "GH", "TN"], "percentage": 62.5},
        {"name": "Ethics", "frequency": 4, "countries": ["KE", "ZA", "EG", "MA"], "percentage": 50.0},
        {"name": "Financial Services", "frequency": 4, "countries": ["KE", "NG", "ZA", "RW"], "percentage": 50.0}
    ]
    
    return countries_data, themes_data

# Load demo data
COUNTRIES_DATA, THEMES_DATA = load_demo_data()

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
    # Sample Kenya data for demo
    if country_code == 'KE':
        country_data = {
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
        return render_template('country.html', country=country_data)
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
        # Return sample Kenya data
        return jsonify({"country_code": "KE", "country_name": "Kenya", "status": "published"})
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

@app.route('/api/comparison')
def api_comparison():
    """API endpoint for country comparison"""
    countries = request.args.getlist('countries')
    if len(countries) < 2:
        return jsonify({'error': 'At least 2 countries required for comparison'}), 400
    
    comparison = {
        "countries": countries,
        "similarities": {
            "Priority Sectors": ["Agriculture", "Healthcare", "Education"]
        },
        "differences": {
            country: {
                "budget": f"USD {100 + i*50} million",
                "governance": f"Ministry of {['ICT', 'Science', 'Digital'][i % 3]}"
            } for i, country in enumerate(countries)
        },
        "common_themes": ["Skills Development", "Innovation", "Infrastructure"],
        "collaboration_opportunities": [
            "Joint AI research initiative",
            "Shared AI talent development program",
            "Cross-border AI regulatory harmonization"
        ]
    }
    return jsonify(comparison)

@app.route('/compare')
def compare():
    """Strategy comparison page"""
    countries = COUNTRIES_DATA
    return render_template('compare.html', countries=countries)

@app.route('/analysis')
def analysis():
    """Cross-cutting analysis page"""
    themes = THEMES_DATA
    return render_template('analysis.html', themes=themes)

@app.route('/api/themes')
def api_themes():
    """API endpoint for all themes"""
    return jsonify(THEMES_DATA)

@app.route('/api/search')
def api_search():
    """API endpoint for search functionality"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'results': []})
    
    # Simple search simulation
    results = [
        {"country_code": "KE", "country_name": "Kenya", "relevance": 3},
        {"country_code": "NG", "country_name": "Nigeria", "relevance": 2}
    ]
    return jsonify({'results': results})

@app.route('/search')
def search():
    """Search page"""
    return render_template('search.html')

@app.route('/api/network-graph')
def api_network_graph():
    """API endpoint for network graph data"""
    graph_data = {
        "nodes": [
            {"id": "KE", "name": "Kenya", "type": "country", "group": 1, "size": 20, "color": "#FF6B35"},
            {"id": "NG", "name": "Nigeria", "type": "country", "group": 1, "size": 20, "color": "#004225"},
            {"id": "theme_skills", "name": "Skills Development", "type": "theme", "group": 2, "size": 15, "color": "#FF6B6B"}
        ],
        "links": [
            {"source": "KE", "target": "theme_skills", "value": 1, "type": "country_theme"},
            {"source": "NG", "target": "theme_skills", "value": 1, "type": "country_theme"}
        ],
        "metadata": {
            "total_countries": len(COUNTRIES_DATA),
            "total_themes": len(THEMES_DATA),
            "total_connections": 2
        }
    }
    return jsonify(graph_data)

@app.route('/network')
def network():
    """Network visualization page"""
    return render_template('network.html')

@app.route('/api/timeline')
def api_timeline():
    """API endpoint for timeline data"""
    timeline_data = {
        "events": [
            {
                "date": "2022-03-15",
                "country": "Kenya",
                "country_code": "KE",
                "event": "Strategy Published",
                "title": "Kenya National AI Strategy",
                "type": "publication",
                "color": "#FF6B35"
            },
            {
                "date": "2021-11-20",
                "country": "Nigeria",
                "country_code": "NG",
                "event": "Strategy Published",
                "title": "National AI Strategy for Nigeria",
                "type": "publication",
                "color": "#004225"
            }
        ],
        "metadata": {
            "total_events": 2,
            "date_range": {
                "start": "2021-11-20",
                "end": "2022-03-15"
            }
        }
    }
    return jsonify(timeline_data)

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

# For Vercel deployment
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
else:
    # This is for Vercel
    application = app
