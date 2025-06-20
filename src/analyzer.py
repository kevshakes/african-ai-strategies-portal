"""
Cross-cutting analysis engine for African AI Strategies Portal
"""

import json
from collections import Counter, defaultdict
from typing import Dict, List, Any, Set, Tuple
from pathlib import Path
import numpy as np
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ThemeAnalysis:
    """Analysis results for a specific theme"""
    theme_name: str
    countries: List[str]
    frequency: int
    percentage: float
    related_themes: List[str]
    key_initiatives: List[Dict[str, Any]]
    common_approaches: List[str]

@dataclass
class ComparisonResult:
    """Results of comparing strategies between countries"""
    countries: List[str]
    similarities: Dict[str, List[str]]
    differences: Dict[str, Dict[str, Any]]
    common_themes: List[str]
    unique_approaches: Dict[str, List[str]]
    collaboration_opportunities: List[str]

class CrossCuttingAnalyzer:
    """Analyzes cross-cutting themes and patterns across AI strategies"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.processed_dir = self.data_dir / "processed"
        self.analysis_dir = self.data_dir / "analysis"
        
        # Ensure analysis directory exists
        self.analysis_dir.mkdir(parents=True, exist_ok=True)
        
        # Load strategy data
        self.strategies = self._load_all_strategies()
        
        # Define theme categories for analysis
        self.theme_categories = {
            "Strategic Focus": [
                "Digital Transformation", "Innovation", "Economic Growth", 
                "Social Development", "Competitiveness", "Sustainability"
            ],
            "Implementation": [
                "Skills Development", "Infrastructure", "Research & Development",
                "Public-Private Partnership", "International Cooperation", "Funding"
            ],
            "Governance": [
                "Ethics", "Regulation", "Data Governance", "Privacy",
                "Transparency", "Accountability", "Standards"
            ],
            "Sectoral Applications": [
                "Agriculture", "Healthcare", "Education", "Financial Services",
                "Manufacturing", "Energy", "Transportation", "Government Services"
            ],
            "Social Impact": [
                "Job Creation", "Inclusion", "Gender Equality", "Youth Empowerment",
                "Rural Development", "Poverty Reduction", "Digital Divide"
            ]
        }
    
    def _load_all_strategies(self) -> Dict[str, Dict[str, Any]]:
        """Load all processed strategy data"""
        strategies = {}
        
        if not self.processed_dir.exists():
            logger.warning("Processed data directory not found")
            return strategies
        
        for strategy_file in self.processed_dir.glob("strategy_*.json"):
            try:
                country_code = strategy_file.stem.split("_")[1]
                with open(strategy_file, 'r') as f:
                    strategies[country_code] = json.load(f)
            except Exception as e:
                logger.error(f"Error loading strategy file {strategy_file}: {e}")
        
        return strategies
    
    def analyze_cross_cutting_themes(self, countries: List[str] = None) -> Dict[str, Any]:
        """Analyze themes that appear across multiple countries"""
        if countries is None:
            countries = list(self.strategies.keys())
        
        # Extract themes from each country
        country_themes = {}
        all_themes = set()
        
        for country in countries:
            if country in self.strategies:
                strategy = self.strategies[country]
                themes = self._extract_themes_from_strategy(strategy)
                country_themes[country] = themes
                all_themes.update(themes)
        
        # Analyze theme frequency and co-occurrence
        theme_analysis = {}
        for theme in all_themes:
            countries_with_theme = [c for c, themes in country_themes.items() if theme in themes]
            
            theme_analysis[theme] = ThemeAnalysis(
                theme_name=theme,
                countries=countries_with_theme,
                frequency=len(countries_with_theme),
                percentage=(len(countries_with_theme) / len(countries)) * 100,
                related_themes=self._find_related_themes(theme, country_themes),
                key_initiatives=self._extract_theme_initiatives(theme, countries_with_theme),
                common_approaches=self._identify_common_approaches(theme, countries_with_theme)
            )
        
        # Group by categories
        categorized_themes = self._categorize_themes(theme_analysis)
        
        # Generate insights
        insights = self._generate_cross_cutting_insights(theme_analysis, country_themes)
        
        analysis_result = {
            "analysis_date": "2024-06-19",
            "countries_analyzed": countries,
            "total_themes": len(all_themes),
            "theme_analysis": {theme: {
                "countries": analysis.countries,
                "frequency": analysis.frequency,
                "percentage": round(analysis.percentage, 1),
                "related_themes": analysis.related_themes[:5],  # Top 5
                "key_initiatives": analysis.key_initiatives[:3],  # Top 3
                "common_approaches": analysis.common_approaches
            } for theme, analysis in theme_analysis.items()},
            "categorized_themes": categorized_themes,
            "insights": insights,
            "collaboration_opportunities": self._identify_collaboration_opportunities(country_themes)
        }
        
        # Save analysis results
        with open(self.analysis_dir / "cross_cutting_analysis.json", "w") as f:
            json.dump(analysis_result, f, indent=2)
        
        return analysis_result
    
    def _extract_themes_from_strategy(self, strategy: Dict[str, Any]) -> Set[str]:
        """Extract themes from a strategy document"""
        themes = set()
        
        # Extract from explicit themes field
        if 'themes' in strategy:
            themes.update(strategy['themes'])
        
        # Extract from strategic pillars
        if 'strategic_pillars' in strategy:
            for pillar in strategy['strategic_pillars']:
                themes.add(pillar.get('name', ''))
        
        # Extract from priority sectors
        if 'priority_sectors' in strategy:
            if isinstance(strategy['priority_sectors'], list):
                for sector in strategy['priority_sectors']:
                    if isinstance(sector, dict):
                        themes.add(sector.get('name', ''))
                    else:
                        themes.add(str(sector))
        
        # Extract from objectives
        if 'objectives' in strategy:
            for obj in strategy['objectives']:
                # Simple keyword extraction
                if 'skill' in obj.lower() or 'talent' in obj.lower():
                    themes.add('Skills Development')
                if 'infrastructure' in obj.lower():
                    themes.add('Infrastructure')
                if 'innovation' in obj.lower():
                    themes.add('Innovation')
                if 'ethics' in obj.lower() or 'responsible' in obj.lower():
                    themes.add('Ethics')
        
        # Remove empty themes
        themes.discard('')
        
        return themes
    
    def _find_related_themes(self, target_theme: str, country_themes: Dict[str, Set[str]]) -> List[str]:
        """Find themes that frequently co-occur with the target theme"""
        co_occurrence = Counter()
        
        for country, themes in country_themes.items():
            if target_theme in themes:
                for theme in themes:
                    if theme != target_theme:
                        co_occurrence[theme] += 1
        
        return [theme for theme, count in co_occurrence.most_common(10)]
    
    def _extract_theme_initiatives(self, theme: str, countries: List[str]) -> List[Dict[str, Any]]:
        """Extract key initiatives related to a specific theme"""
        initiatives = []
        
        for country in countries:
            if country in self.strategies:
                strategy = self.strategies[country]
                if 'key_initiatives' in strategy:
                    for initiative in strategy['key_initiatives']:
                        # Simple matching based on keywords
                        if self._initiative_matches_theme(initiative, theme):
                            initiatives.append({
                                "country": country,
                                "name": initiative.get('name', ''),
                                "description": initiative.get('description', ''),
                                "budget": initiative.get('budget', 'Not specified')
                            })
        
        return initiatives[:10]  # Return top 10
    
    def _initiative_matches_theme(self, initiative: Dict[str, Any], theme: str) -> bool:
        """Check if an initiative matches a theme"""
        text = f"{initiative.get('name', '')} {initiative.get('description', '')}".lower()
        theme_keywords = {
            'Skills Development': ['skill', 'training', 'education', 'capacity'],
            'Innovation': ['innovation', 'research', 'development', 'startup'],
            'Infrastructure': ['infrastructure', 'connectivity', 'broadband', 'network'],
            'Agriculture': ['agriculture', 'farming', 'crop', 'livestock'],
            'Healthcare': ['health', 'medical', 'hospital', 'diagnosis'],
            'Ethics': ['ethics', 'responsible', 'governance', 'transparency']
        }
        
        keywords = theme_keywords.get(theme, [theme.lower()])
        return any(keyword in text for keyword in keywords)
    
    def _identify_common_approaches(self, theme: str, countries: List[str]) -> List[str]:
        """Identify common approaches for implementing a theme"""
        approaches = []
        
        # This would analyze implementation strategies
        # For now, return sample approaches based on theme
        approach_mapping = {
            'Skills Development': [
                'University partnerships', 'Online training platforms', 
                'Certification programs', 'Industry collaboration'
            ],
            'Innovation': [
                'Innovation hubs', 'Startup incubators', 
                'Research grants', 'Public-private partnerships'
            ],
            'Infrastructure': [
                'Broadband expansion', 'Data centers', 
                'Cloud platforms', 'Digital infrastructure investment'
            ],
            'Ethics': [
                'Ethics committees', 'Regulatory frameworks', 
                'Guidelines development', 'Stakeholder consultation'
            ]
        }
        
        return approach_mapping.get(theme, ['Policy development', 'Stakeholder engagement'])
    
    def _categorize_themes(self, theme_analysis: Dict[str, ThemeAnalysis]) -> Dict[str, List[str]]:
        """Categorize themes into predefined categories"""
        categorized = {category: [] for category in self.theme_categories.keys()}
        uncategorized = []
        
        for theme_name in theme_analysis.keys():
            categorized_flag = False
            for category, category_themes in self.theme_categories.items():
                if any(cat_theme.lower() in theme_name.lower() or 
                      theme_name.lower() in cat_theme.lower() 
                      for cat_theme in category_themes):
                    categorized[category].append(theme_name)
                    categorized_flag = True
                    break
            
            if not categorized_flag:
                uncategorized.append(theme_name)
        
        if uncategorized:
            categorized['Other'] = uncategorized
        
        return categorized
    
    def _generate_cross_cutting_insights(self, theme_analysis: Dict[str, ThemeAnalysis], 
                                       country_themes: Dict[str, Set[str]]) -> List[str]:
        """Generate insights from cross-cutting analysis"""
        insights = []
        
        # Most common themes
        most_common = sorted(theme_analysis.items(), 
                           key=lambda x: x[1].frequency, reverse=True)[:5]
        insights.append(f"Most common themes: {', '.join([t[0] for t in most_common])}")
        
        # Universal themes (present in all countries)
        universal_themes = [theme for theme, analysis in theme_analysis.items() 
                          if analysis.frequency == len(country_themes)]
        if universal_themes:
            insights.append(f"Universal themes across all countries: {', '.join(universal_themes)}")
        
        # Unique themes per country
        for country, themes in country_themes.items():
            unique_themes = [theme for theme in themes 
                           if theme_analysis[theme].frequency == 1]
            if unique_themes:
                insights.append(f"{country} unique focus areas: {', '.join(unique_themes)}")
        
        return insights
    
    def _identify_collaboration_opportunities(self, country_themes: Dict[str, Set[str]]) -> List[Dict[str, Any]]:
        """Identify potential collaboration opportunities"""
        opportunities = []
        
        # Find countries with similar themes
        theme_countries = defaultdict(list)
        for country, themes in country_themes.items():
            for theme in themes:
                theme_countries[theme].append(country)
        
        # Identify high-potential collaboration areas
        for theme, countries in theme_countries.items():
            if len(countries) >= 2:  # At least 2 countries share this theme
                opportunities.append({
                    "theme": theme,
                    "countries": countries,
                    "collaboration_type": self._suggest_collaboration_type(theme),
                    "potential_impact": "High" if len(countries) >= 3 else "Medium"
                })
        
        return sorted(opportunities, key=lambda x: len(x["countries"]), reverse=True)[:10]
    
    def _suggest_collaboration_type(self, theme: str) -> str:
        """Suggest type of collaboration based on theme"""
        collaboration_types = {
            'Skills Development': 'Joint training programs and certification',
            'Innovation': 'Shared research initiatives and innovation hubs',
            'Infrastructure': 'Regional infrastructure development',
            'Agriculture': 'Knowledge sharing and technology transfer',
            'Healthcare': 'Telemedicine and health data sharing',
            'Ethics': 'Common regulatory frameworks and standards'
        }
        
        return collaboration_types.get(theme, 'Policy coordination and best practice sharing')
    
    def compare_strategies(self, countries: List[str]) -> ComparisonResult:
        """Compare AI strategies between specified countries"""
        if len(countries) < 2:
            raise ValueError("At least 2 countries required for comparison")
        
        # Extract data for comparison
        comparison_data = {}
        for country in countries:
            if country in self.strategies:
                comparison_data[country] = self.strategies[country]
        
        # Find similarities and differences
        similarities = self._find_similarities(comparison_data)
        differences = self._find_differences(comparison_data)
        common_themes = self._find_common_themes(comparison_data)
        unique_approaches = self._find_unique_approaches(comparison_data)
        collaboration_opportunities = self._suggest_bilateral_collaboration(comparison_data)
        
        result = ComparisonResult(
            countries=countries,
            similarities=similarities,
            differences=differences,
            common_themes=common_themes,
            unique_approaches=unique_approaches,
            collaboration_opportunities=collaboration_opportunities
        )
        
        return result
    
    def _find_similarities(self, comparison_data: Dict[str, Dict[str, Any]]) -> Dict[str, List[str]]:
        """Find similarities between strategies"""
        similarities = defaultdict(list)
        
        # Compare priority sectors
        all_sectors = set()
        country_sectors = {}
        for country, strategy in comparison_data.items():
            sectors = set()
            if 'priority_sectors' in strategy:
                for sector in strategy['priority_sectors']:
                    if isinstance(sector, dict):
                        sectors.add(sector.get('name', ''))
                    else:
                        sectors.add(str(sector))
            country_sectors[country] = sectors
            all_sectors.update(sectors)
        
        common_sectors = all_sectors
        for sectors in country_sectors.values():
            common_sectors = common_sectors.intersection(sectors)
        
        if common_sectors:
            similarities['Priority Sectors'] = list(common_sectors)
        
        return dict(similarities)
    
    def _find_differences(self, comparison_data: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Find key differences between strategies"""
        differences = {}
        
        for country, strategy in comparison_data.items():
            differences[country] = {
                'budget': strategy.get('funding_strategy', {}).get('total_budget', 'Not specified'),
                'timeline': strategy.get('implementation_timeline', {}),
                'governance': strategy.get('governance_structure', {}).get('steering_committee', {}).get('chair', 'Not specified')
            }
        
        return differences
    
    def _find_common_themes(self, comparison_data: Dict[str, Dict[str, Any]]) -> List[str]:
        """Find themes common to all compared countries"""
        all_themes = []
        for country, strategy in comparison_data.items():
            themes = self._extract_themes_from_strategy(strategy)
            all_themes.append(themes)
        
        if all_themes:
            common_themes = all_themes[0]
            for themes in all_themes[1:]:
                common_themes = common_themes.intersection(themes)
            return list(common_themes)
        
        return []
    
    def _find_unique_approaches(self, comparison_data: Dict[str, Dict[str, Any]]) -> Dict[str, List[str]]:
        """Find unique approaches for each country"""
        unique_approaches = {}
        
        for country, strategy in comparison_data.items():
            approaches = []
            
            # Extract unique initiatives
            if 'key_initiatives' in strategy:
                for initiative in strategy['key_initiatives'][:3]:  # Top 3
                    approaches.append(initiative.get('name', ''))
            
            unique_approaches[country] = approaches
        
        return unique_approaches
    
    def _suggest_bilateral_collaboration(self, comparison_data: Dict[str, Dict[str, Any]]) -> List[str]:
        """Suggest collaboration opportunities between countries"""
        suggestions = []
        
        countries = list(comparison_data.keys())
        if len(countries) >= 2:
            suggestions.append(f"Joint AI research initiative between {' and '.join(countries)}")
            suggestions.append(f"Shared AI talent development program")
            suggestions.append(f"Cross-border AI regulatory harmonization")
        
        return suggestions
    
    def get_all_themes(self) -> List[Dict[str, Any]]:
        """Get all identified themes with metadata"""
        if not hasattr(self, '_all_themes_cache'):
            analysis = self.analyze_cross_cutting_themes()
            self._all_themes_cache = [
                {
                    "name": theme,
                    "frequency": data["frequency"],
                    "countries": data["countries"],
                    "percentage": data["percentage"]
                }
                for theme, data in analysis["theme_analysis"].items()
            ]
        
        return self._all_themes_cache
