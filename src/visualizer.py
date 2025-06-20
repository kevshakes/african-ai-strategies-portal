"""
Visualization engine for African AI Strategies Portal
Generates interactive charts, mind maps, and network graphs
"""

import json
from typing import Dict, List, Any, Tuple
from pathlib import Path
import logging
from collections import defaultdict, Counter
import random

logger = logging.getLogger(__name__)

class VisualizationEngine:
    """Generates various visualizations for AI strategy data"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.processed_dir = self.data_dir / "processed"
        
        # Color schemes for visualizations
        self.color_schemes = {
            "countries": {
                "KE": "#FF6B35", "NG": "#004225", "ZA": "#FFD23F",
                "EG": "#EE4266", "MA": "#540D6E", "TN": "#F15BB5",
                "GH": "#00BBF9", "RW": "#00F5FF", "ET": "#9B5DE5",
                "UG": "#F15BB5"
            },
            "themes": {
                "Skills Development": "#FF6B6B", "Innovation": "#4ECDC4",
                "Infrastructure": "#45B7D1", "Agriculture": "#96CEB4",
                "Healthcare": "#FFEAA7", "Education": "#DDA0DD",
                "Ethics": "#98D8C8", "Economic Growth": "#F7DC6F"
            },
            "sectors": [
                "#FF6B35", "#F7931E", "#FFD23F", "#06FFA5",
                "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"
            ]
        }
    
    def generate_mind_map(self, country_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mind map data for a country's AI strategy"""
        
        country_name = country_data.get('country_name', 'Unknown')
        
        # Central node
        mind_map = {
            "name": f"{country_name} AI Strategy",
            "type": "root",
            "children": []
        }
        
        # Strategic pillars as main branches
        if 'strategic_pillars' in country_data:
            for pillar in country_data['strategic_pillars']:
                pillar_node = {
                    "name": pillar.get('name', 'Strategic Pillar'),
                    "type": "pillar",
                    "description": pillar.get('description', ''),
                    "children": []
                }
                
                # Add key actions as sub-nodes
                if 'key_actions' in pillar:
                    for action in pillar['key_actions']:
                        pillar_node["children"].append({
                            "name": action,
                            "type": "action",
                            "size": 1
                        })
                
                mind_map["children"].append(pillar_node)
        
        # Priority sectors as another main branch
        if 'priority_sectors' in country_data:
            sectors_node = {
                "name": "Priority Sectors",
                "type": "category",
                "children": []
            }
            
            for sector in country_data['priority_sectors']:
                if isinstance(sector, dict):
                    sector_node = {
                        "name": sector.get('name', 'Sector'),
                        "type": "sector",
                        "description": sector.get('expected_impact', ''),
                        "children": []
                    }
                    
                    # Add AI applications
                    if 'ai_applications' in sector:
                        for app in sector['ai_applications']:
                            sector_node["children"].append({
                                "name": app,
                                "type": "application",
                                "size": 1
                            })
                    
                    sectors_node["children"].append(sector_node)
                else:
                    sectors_node["children"].append({
                        "name": str(sector),
                        "type": "sector",
                        "size": 2
                    })
            
            mind_map["children"].append(sectors_node)
        
        # Key initiatives as another branch
        if 'key_initiatives' in country_data:
            initiatives_node = {
                "name": "Key Initiatives",
                "type": "category",
                "children": []
            }
            
            for initiative in country_data['key_initiatives']:
                initiative_node = {
                    "name": initiative.get('name', 'Initiative'),
                    "type": "initiative",
                    "description": initiative.get('description', ''),
                    "budget": initiative.get('budget', 'Not specified'),
                    "size": 3
                }
                initiatives_node["children"].append(initiative_node)
            
            mind_map["children"].append(initiatives_node)
        
        # Add metadata for visualization
        mind_map["metadata"] = {
            "country_code": country_data.get('country_code', ''),
            "total_nodes": self._count_nodes(mind_map),
            "color_scheme": self.color_schemes["countries"].get(
                country_data.get('country_code', ''), "#333333"
            )
        }
        
        return mind_map
    
    def _count_nodes(self, node: Dict[str, Any]) -> int:
        """Recursively count nodes in mind map"""
        count = 1
        if 'children' in node:
            for child in node['children']:
                count += self._count_nodes(child)
        return count
    
    def generate_network_graph(self) -> Dict[str, Any]:
        """Generate network graph showing relationships between countries and themes"""
        
        # Load all strategies
        strategies = self._load_all_strategies()
        
        nodes = []
        links = []
        
        # Create country nodes
        for country_code, strategy in strategies.items():
            nodes.append({
                "id": country_code,
                "name": strategy.get('country_name', country_code),
                "type": "country",
                "group": 1,
                "size": 20,
                "color": self.color_schemes["countries"].get(country_code, "#333333")
            })
        
        # Extract themes and create theme nodes
        all_themes = set()
        country_themes = {}
        
        for country_code, strategy in strategies.items():
            themes = self._extract_themes(strategy)
            country_themes[country_code] = themes
            all_themes.update(themes)
        
        # Create theme nodes
        theme_counter = Counter()
        for themes in country_themes.values():
            theme_counter.update(themes)
        
        for theme in all_themes:
            nodes.append({
                "id": f"theme_{theme}",
                "name": theme,
                "type": "theme",
                "group": 2,
                "size": min(theme_counter[theme] * 5, 30),  # Size based on frequency
                "color": self.color_schemes["themes"].get(theme, "#888888")
            })
        
        # Create links between countries and themes
        for country_code, themes in country_themes.items():
            for theme in themes:
                links.append({
                    "source": country_code,
                    "target": f"theme_{theme}",
                    "value": 1,
                    "type": "country_theme"
                })
        
        # Create links between countries with similar themes
        countries = list(country_themes.keys())
        for i, country1 in enumerate(countries):
            for country2 in countries[i+1:]:
                common_themes = country_themes[country1].intersection(country_themes[country2])
                if len(common_themes) >= 2:  # At least 2 common themes
                    links.append({
                        "source": country1,
                        "target": country2,
                        "value": len(common_themes),
                        "type": "country_similarity",
                        "common_themes": list(common_themes)
                    })
        
        return {
            "nodes": nodes,
            "links": links,
            "metadata": {
                "total_countries": len(strategies),
                "total_themes": len(all_themes),
                "total_connections": len(links)
            }
        }
    
    def generate_timeline(self) -> Dict[str, Any]:
        """Generate timeline visualization of AI strategy development"""
        
        strategies = self._load_all_strategies()
        
        timeline_events = []
        
        for country_code, strategy in strategies.items():
            # Strategy publication
            if 'publication_date' in strategy:
                timeline_events.append({
                    "date": strategy['publication_date'],
                    "country": strategy.get('country_name', country_code),
                    "country_code": country_code,
                    "event": "Strategy Published",
                    "title": strategy.get('strategy_title', 'AI Strategy'),
                    "type": "publication",
                    "color": self.color_schemes["countries"].get(country_code, "#333333")
                })
            
            # Key milestones from implementation timeline
            if 'implementation_timeline' in strategy:
                timeline = strategy['implementation_timeline']
                for phase, details in timeline.items():
                    if isinstance(details, dict) and 'period' in details:
                        period = details['period']
                        start_year = period.split('-')[0]
                        timeline_events.append({
                            "date": f"{start_year}-01-01",
                            "country": strategy.get('country_name', country_code),
                            "country_code": country_code,
                            "event": f"{phase.title()} Phase",
                            "title": details.get('focus', 'Implementation Phase'),
                            "type": "milestone",
                            "color": self.color_schemes["countries"].get(country_code, "#333333")
                        })
        
        # Sort by date
        timeline_events.sort(key=lambda x: x['date'])
        
        return {
            "events": timeline_events,
            "metadata": {
                "total_events": len(timeline_events),
                "date_range": {
                    "start": timeline_events[0]['date'] if timeline_events else None,
                    "end": timeline_events[-1]['date'] if timeline_events else None
                }
            }
        }
    
    def generate_comparison_chart(self, countries: List[str], metric: str = "budget") -> Dict[str, Any]:
        """Generate comparison chart for specified countries and metric"""
        
        strategies = self._load_all_strategies()
        
        chart_data = []
        
        for country_code in countries:
            if country_code in strategies:
                strategy = strategies[country_code]
                
                if metric == "budget":
                    budget_str = strategy.get('funding_strategy', {}).get('total_budget', '0')
                    # Extract numeric value (simplified)
                    budget_value = self._extract_budget_value(budget_str)
                    chart_data.append({
                        "country": strategy.get('country_name', country_code),
                        "country_code": country_code,
                        "value": budget_value,
                        "label": budget_str,
                        "color": self.color_schemes["countries"].get(country_code, "#333333")
                    })
                
                elif metric == "sectors":
                    sectors_count = len(strategy.get('priority_sectors', []))
                    chart_data.append({
                        "country": strategy.get('country_name', country_code),
                        "country_code": country_code,
                        "value": sectors_count,
                        "label": f"{sectors_count} sectors",
                        "color": self.color_schemes["countries"].get(country_code, "#333333")
                    })
                
                elif metric == "initiatives":
                    initiatives_count = len(strategy.get('key_initiatives', []))
                    chart_data.append({
                        "country": strategy.get('country_name', country_code),
                        "country_code": country_code,
                        "value": initiatives_count,
                        "label": f"{initiatives_count} initiatives",
                        "color": self.color_schemes["countries"].get(country_code, "#333333")
                    })
        
        return {
            "data": chart_data,
            "metric": metric,
            "chart_type": "bar",
            "metadata": {
                "countries_compared": len(chart_data),
                "max_value": max([d["value"] for d in chart_data]) if chart_data else 0,
                "min_value": min([d["value"] for d in chart_data]) if chart_data else 0
            }
        }
    
    def generate_sector_analysis(self) -> Dict[str, Any]:
        """Generate sector-wise analysis across all countries"""
        
        strategies = self._load_all_strategies()
        
        sector_data = defaultdict(list)
        sector_counter = Counter()
        
        for country_code, strategy in strategies.items():
            if 'priority_sectors' in strategy:
                for sector in strategy['priority_sectors']:
                    sector_name = sector.get('name', str(sector)) if isinstance(sector, dict) else str(sector)
                    sector_counter[sector_name] += 1
                    sector_data[sector_name].append({
                        "country": strategy.get('country_name', country_code),
                        "country_code": country_code,
                        "applications": sector.get('ai_applications', []) if isinstance(sector, dict) else [],
                        "impact": sector.get('expected_impact', '') if isinstance(sector, dict) else ''
                    })
        
        # Create visualization data
        sectors_viz = []
        for i, (sector, count) in enumerate(sector_counter.most_common()):
            sectors_viz.append({
                "name": sector,
                "frequency": count,
                "percentage": (count / len(strategies)) * 100,
                "countries": sector_data[sector],
                "color": self.color_schemes["sectors"][i % len(self.color_schemes["sectors"])]
            })
        
        return {
            "sectors": sectors_viz,
            "metadata": {
                "total_sectors": len(sector_counter),
                "most_common": sector_counter.most_common(5),
                "countries_analyzed": len(strategies)
            }
        }
    
    def generate_theme_heatmap(self) -> Dict[str, Any]:
        """Generate heatmap showing theme distribution across countries"""
        
        strategies = self._load_all_strategies()
        
        # Extract themes for each country
        country_themes = {}
        all_themes = set()
        
        for country_code, strategy in strategies.items():
            themes = self._extract_themes(strategy)
            country_themes[country_code] = themes
            all_themes.update(themes)
        
        # Create heatmap matrix
        countries = list(strategies.keys())
        themes = sorted(list(all_themes))
        
        heatmap_data = []
        for i, country in enumerate(countries):
            for j, theme in enumerate(themes):
                value = 1 if theme in country_themes[country] else 0
                heatmap_data.append({
                    "country": strategies[country].get('country_name', country),
                    "country_code": country,
                    "theme": theme,
                    "value": value,
                    "x": j,
                    "y": i
                })
        
        return {
            "data": heatmap_data,
            "countries": [strategies[c].get('country_name', c) for c in countries],
            "themes": themes,
            "metadata": {
                "matrix_size": f"{len(countries)}x{len(themes)}",
                "total_cells": len(heatmap_data),
                "coverage_percentage": (sum([d["value"] for d in heatmap_data]) / len(heatmap_data)) * 100
            }
        }
    
    def _load_all_strategies(self) -> Dict[str, Dict[str, Any]]:
        """Load all processed strategy data"""
        strategies = {}
        
        if not self.processed_dir.exists():
            return strategies
        
        for strategy_file in self.processed_dir.glob("strategy_*.json"):
            try:
                country_code = strategy_file.stem.split("_")[1]
                with open(strategy_file, 'r') as f:
                    strategies[country_code] = json.load(f)
            except Exception as e:
                logger.error(f"Error loading strategy file {strategy_file}: {e}")
        
        return strategies
    
    def _extract_themes(self, strategy: Dict[str, Any]) -> set:
        """Extract themes from strategy data"""
        themes = set()
        
        # From explicit themes
        if 'themes' in strategy:
            themes.update(strategy['themes'])
        
        # From strategic pillars
        if 'strategic_pillars' in strategy:
            for pillar in strategy['strategic_pillars']:
                themes.add(pillar.get('name', ''))
        
        # From priority sectors
        if 'priority_sectors' in strategy:
            for sector in strategy['priority_sectors']:
                if isinstance(sector, dict):
                    themes.add(sector.get('name', ''))
                else:
                    themes.add(str(sector))
        
        # Remove empty themes
        themes.discard('')
        
        return themes
    
    def _extract_budget_value(self, budget_str: str) -> float:
        """Extract numeric budget value from string"""
        if not budget_str or budget_str == "Not specified":
            return 0
        
        # Simple extraction (would need more sophisticated parsing in real implementation)
        budget_str = budget_str.upper().replace('USD', '').replace('$', '').strip()
        
        try:
            if 'MILLION' in budget_str or 'M' in budget_str:
                number = float(''.join(filter(str.isdigit, budget_str.split('M')[0])))
                return number
            elif 'BILLION' in budget_str or 'B' in budget_str:
                number = float(''.join(filter(str.isdigit, budget_str.split('B')[0])))
                return number * 1000
            else:
                return float(''.join(filter(str.isdigit, budget_str)))
        except:
            return 0
    
    def generate_dashboard_summary(self) -> Dict[str, Any]:
        """Generate summary data for main dashboard"""
        
        strategies = self._load_all_strategies()
        
        # Basic statistics
        total_countries = len(strategies)
        published_count = sum(1 for s in strategies.values() if s.get('status') == 'published')
        draft_count = sum(1 for s in strategies.values() if s.get('status') == 'draft')
        
        # Theme analysis
        all_themes = set()
        for strategy in strategies.values():
            all_themes.update(self._extract_themes(strategy))
        
        # Sector analysis
        all_sectors = set()
        for strategy in strategies.values():
            if 'priority_sectors' in strategy:
                for sector in strategy['priority_sectors']:
                    sector_name = sector.get('name', str(sector)) if isinstance(sector, dict) else str(sector)
                    all_sectors.add(sector_name)
        
        # Recent updates
        recent_strategies = []
        for country_code, strategy in strategies.items():
            if 'publication_date' in strategy:
                recent_strategies.append({
                    "country": strategy.get('country_name', country_code),
                    "date": strategy['publication_date'],
                    "title": strategy.get('strategy_title', 'AI Strategy')
                })
        
        recent_strategies.sort(key=lambda x: x['date'], reverse=True)
        
        return {
            "statistics": {
                "total_countries": total_countries,
                "published_strategies": published_count,
                "draft_strategies": draft_count,
                "total_themes": len(all_themes),
                "total_sectors": len(all_sectors)
            },
            "top_themes": list(all_themes)[:8],
            "top_sectors": list(all_sectors)[:8],
            "recent_updates": recent_strategies[:5],
            "country_status": [
                {
                    "country": strategy.get('country_name', code),
                    "country_code": code,
                    "status": strategy.get('status', 'unknown'),
                    "color": self.color_schemes["countries"].get(code, "#333333")
                }
                for code, strategy in strategies.items()
            ]
        }
