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

# Import our custom modules
from src.data_collector import DataCollector
from src.analyzer import CrossCuttingAnalyzer
from src.visualizer import VisualizationEngine
from src.models import StrategyDatabase

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['DATA_PATH'] = 'data'

# Initialize components
db = StrategyDatabase()
collector = DataCollector()
analyzer = CrossCuttingAnalyzer()
visualizer = VisualizationEngine()

@app.route('/')
def index():
    """Main dashboard page"""
    countries = db.get_all_countries()
    stats = {
        'total_countries': len(countries),
        'total_strategies': db.count_strategies(),
        'last_updated': datetime.now().strftime('%Y-%m-%d')
    }
    return render_template('index.html', countries=countries, stats=stats)

@app.route('/country/<country_code>')
def country_detail(country_code):
    """Individual country strategy page"""
    country_data = db.get_country_strategy(country_code)
    if not country_data:
        return render_template('404.html'), 404
    
    # Generate mind map data
    mind_map_data = visualizer.generate_mind_map(country_data)
    
    return render_template('country.html', 
                         country=country_data, 
                         mind_map=mind_map_data)

@app.route('/api/countries')
def api_countries():
    """API endpoint for countries list"""
    countries = db.get_all_countries()
    return jsonify(countries)

@app.route('/api/country/<country_code>/strategy')
def api_country_strategy(country_code):
    """API endpoint for country strategy data"""
    strategy = db.get_country_strategy(country_code)
    return jsonify(strategy) if strategy else jsonify({'error': 'Country not found'}), 404

@app.route('/api/cross-cutting')
def api_cross_cutting():
    """API endpoint for cross-cutting analysis"""
    countries = request.args.getlist('countries')
    if not countries:
        countries = [c['code'] for c in db.get_all_countries()]
    
    analysis = analyzer.analyze_cross_cutting_themes(countries)
    return jsonify(analysis)

@app.route('/api/mind-map/<country_code>')
def api_mind_map(country_code):
    """API endpoint for mind map data"""
    country_data = db.get_country_strategy(country_code)
    if not country_data:
        return jsonify({'error': 'Country not found'}), 404
    
    mind_map_data = visualizer.generate_mind_map(country_data)
    return jsonify(mind_map_data)

@app.route('/api/comparison')
def api_comparison():
    """API endpoint for country comparison"""
    countries = request.args.getlist('countries')
    if len(countries) < 2:
        return jsonify({'error': 'At least 2 countries required for comparison'}), 400
    
    comparison = analyzer.compare_strategies(countries)
    return jsonify(comparison)

@app.route('/compare')
def compare():
    """Strategy comparison page"""
    countries = db.get_all_countries()
    return render_template('compare.html', countries=countries)

@app.route('/analysis')
def analysis():
    """Cross-cutting analysis page"""
    themes = analyzer.get_all_themes()
    return render_template('analysis.html', themes=themes)

@app.route('/api/themes')
def api_themes():
    """API endpoint for all themes"""
    themes = analyzer.get_all_themes()
    return jsonify(themes)

@app.route('/api/search')
def api_search():
    """API endpoint for search functionality"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'results': []})
    
    results = db.search_strategies(query)
    return jsonify({'results': results})

@app.route('/search')
def search():
    """Search page"""
    return render_template('search.html')

@app.route('/api/network-graph')
def api_network_graph():
    """API endpoint for network graph data"""
    graph_data = visualizer.generate_network_graph()
    return jsonify(graph_data)

@app.route('/network')
def network():
    """Network visualization page"""
    return render_template('network.html')

@app.route('/api/timeline')
def api_timeline():
    """API endpoint for timeline data"""
    timeline_data = visualizer.generate_timeline()
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

if __name__ == '__main__':
    # Initialize database and load initial data
    print("Initializing African AI Strategies Portal...")
    
    # Create data directories if they don't exist
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('data/analysis', exist_ok=True)
    
    # Load initial data
    try:
        collector.load_initial_data()
        print("✓ Initial data loaded successfully")
    except Exception as e:
        print(f"⚠ Warning: Could not load initial data - {e}")
    
    print("🌍 Starting African AI Strategies Portal...")
    print("📊 Access the portal at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
