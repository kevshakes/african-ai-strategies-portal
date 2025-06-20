"""
Data models and database management for African AI Strategies Portal
"""

import json
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class AIStrategy:
    """Data model for a country's AI strategy"""
    country_code: str
    country_name: str
    strategy_title: str
    publication_date: str
    status: str  # 'published', 'draft', 'under_development'
    
    # Core strategy components
    vision: str
    objectives: List[str]
    priority_sectors: List[str]
    key_initiatives: List[Dict[str, Any]]
    
    # Implementation details
    governance_structure: Dict[str, Any]
    funding_mechanisms: List[str]
    timeline: Dict[str, str]
    
    # Analysis metadata
    themes: List[str]
    cross_cutting_issues: List[str]
    international_cooperation: List[str]
    
    # Document metadata
    document_url: Optional[str] = None
    document_pages: Optional[int] = None
    last_updated: Optional[str] = None

@dataclass
class Theme:
    """Data model for cross-cutting themes"""
    theme_id: str
    name: str
    description: str
    countries: List[str]
    frequency: int
    related_themes: List[str]

@dataclass
class Initiative:
    """Data model for specific AI initiatives"""
    initiative_id: str
    name: str
    description: str
    country_code: str
    sector: str
    status: str
    budget: Optional[str] = None
    timeline: Optional[Dict[str, str]] = None
    partners: Optional[List[str]] = None

class StrategyDatabase:
    """Database management for AI strategies data"""
    
    def __init__(self, db_path: str = "data/strategies.db"):
        self.db_path = db_path
        self.data_dir = Path("data")
        self.processed_dir = self.data_dir / "processed"
        self.analysis_dir = self.data_dir / "analysis"
        
        # Ensure directories exist
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.analysis_dir.mkdir(parents=True, exist_ok=True)
        
        self._init_database()
        self._load_sample_data()
    
    def _init_database(self):
        """Initialize SQLite database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS strategies (
                    country_code TEXT PRIMARY KEY,
                    country_name TEXT NOT NULL,
                    strategy_title TEXT NOT NULL,
                    publication_date TEXT,
                    status TEXT,
                    data_json TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS themes (
                    theme_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    data_json TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS initiatives (
                    initiative_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    country_code TEXT,
                    sector TEXT,
                    status TEXT,
                    data_json TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (country_code) REFERENCES strategies (country_code)
                )
            ''')
    
    def _load_sample_data(self):
        """Load sample data for demonstration"""
        sample_strategies = [
            {
                "country_code": "KE",
                "country_name": "Kenya",
                "strategy_title": "Kenya National Artificial Intelligence Strategy 2022-2027",
                "publication_date": "2022-03-15",
                "status": "published",
                "vision": "To be a globally competitive AI-driven economy that harnesses artificial intelligence for sustainable development",
                "objectives": [
                    "Develop AI capabilities and infrastructure",
                    "Build AI talent and skills",
                    "Foster AI innovation and entrepreneurship",
                    "Ensure ethical and responsible AI development",
                    "Strengthen AI governance frameworks"
                ],
                "priority_sectors": [
                    "Agriculture", "Healthcare", "Education", "Financial Services", 
                    "Manufacturing", "Transport", "Energy", "Security"
                ],
                "key_initiatives": [
                    {
                        "name": "AI Innovation Hub",
                        "description": "Establish centers of excellence for AI research and development",
                        "budget": "USD 50M",
                        "timeline": {"start": "2022", "end": "2025"}
                    },
                    {
                        "name": "Digital Skills Program",
                        "description": "Train 100,000 Kenyans in AI and digital skills",
                        "budget": "USD 30M",
                        "timeline": {"start": "2022", "end": "2027"}
                    }
                ],
                "governance_structure": {
                    "lead_agency": "Ministry of ICT, Innovation and Youth Affairs",
                    "coordinating_body": "National AI Steering Committee",
                    "implementation_agencies": ["KENET", "ICTA", "Universities"]
                },
                "funding_mechanisms": ["Government Budget", "Development Partners", "Private Sector"],
                "timeline": {"phase1": "2022-2024", "phase2": "2025-2027"},
                "themes": ["Digital Economy", "Innovation", "Skills Development", "Ethics"],
                "cross_cutting_issues": ["Gender Inclusion", "Youth Empowerment", "Rural Development"],
                "international_cooperation": ["African Union", "UN", "World Bank"],
                "document_url": "https://www.ict.go.ke/ai-strategy",
                "document_pages": 85
            },
            {
                "country_code": "NG",
                "country_name": "Nigeria",
                "strategy_title": "National Artificial Intelligence Strategy for Nigeria",
                "publication_date": "2021-11-20",
                "status": "published",
                "vision": "To position Nigeria as a leading AI nation in Africa and globally competitive in the AI value chain",
                "objectives": [
                    "Build AI research and development capacity",
                    "Develop AI talent pipeline",
                    "Create enabling environment for AI adoption",
                    "Establish AI governance and ethics framework",
                    "Promote AI for social good"
                ],
                "priority_sectors": [
                    "Agriculture", "Health", "Education", "Financial Services",
                    "Oil and Gas", "Manufacturing", "Transportation", "Government Services"
                ],
                "key_initiatives": [
                    {
                        "name": "National AI Research Institute",
                        "description": "Establish premier AI research facility",
                        "budget": "USD 100M",
                        "timeline": {"start": "2022", "end": "2026"}
                    },
                    {
                        "name": "AI for Agriculture Program",
                        "description": "Deploy AI solutions for smallholder farmers",
                        "budget": "USD 25M",
                        "timeline": {"start": "2022", "end": "2025"}
                    }
                ],
                "governance_structure": {
                    "lead_agency": "Federal Ministry of Communications and Digital Economy",
                    "coordinating_body": "National AI Advisory Council",
                    "implementation_agencies": ["NITDA", "NCC", "Universities"]
                },
                "funding_mechanisms": ["Federal Budget", "State Governments", "International Partners"],
                "timeline": {"short_term": "2022-2024", "medium_term": "2025-2027", "long_term": "2028-2030"},
                "themes": ["Research Excellence", "Talent Development", "Digital Transformation", "Governance"],
                "cross_cutting_issues": ["Financial Inclusion", "Healthcare Access", "Agricultural Productivity"],
                "international_cooperation": ["African Union", "ECOWAS", "World Bank", "UN"],
                "document_url": "https://nitda.gov.ng/ai-strategy",
                "document_pages": 120
            },
            {
                "country_code": "ZA",
                "country_name": "South Africa",
                "strategy_title": "South Africa's National Artificial Intelligence Strategy",
                "publication_date": "2021-04-15",
                "status": "published",
                "vision": "To leverage AI for inclusive economic growth, social development, and improved quality of life for all South Africans",
                "objectives": [
                    "Develop AI capabilities and infrastructure",
                    "Build human capital for AI",
                    "Promote AI adoption across sectors",
                    "Ensure responsible AI development",
                    "Foster international AI cooperation"
                ],
                "priority_sectors": [
                    "Mining", "Agriculture", "Healthcare", "Education",
                    "Financial Services", "Manufacturing", "Energy", "Tourism"
                ],
                "key_initiatives": [
                    {
                        "name": "AI Institute of South Africa",
                        "description": "National center for AI research and innovation",
                        "budget": "USD 75M",
                        "timeline": {"start": "2021", "end": "2025"}
                    },
                    {
                        "name": "AI Skills Development Program",
                        "description": "Train 50,000 professionals in AI technologies",
                        "budget": "USD 40M",
                        "timeline": {"start": "2022", "end": "2026"}
                    }
                ],
                "governance_structure": {
                    "lead_agency": "Department of Science and Innovation",
                    "coordinating_body": "National AI Council",
                    "implementation_agencies": ["CSIR", "Universities", "SITA"]
                },
                "funding_mechanisms": ["National Treasury", "Provincial Governments", "Private Sector"],
                "timeline": {"phase1": "2021-2023", "phase2": "2024-2026", "phase3": "2027-2030"},
                "themes": ["Innovation", "Skills Development", "Responsible AI", "Economic Growth"],
                "cross_cutting_issues": ["Inequality Reduction", "Job Creation", "Rural Development"],
                "international_cooperation": ["BRICS", "African Union", "G20", "UN"],
                "document_url": "https://www.dst.gov.za/ai-strategy",
                "document_pages": 95
            }
        ]
        
        # Check if data already exists
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM strategies")
            count = cursor.fetchone()[0]
            
            if count == 0:  # Only load if database is empty
                for strategy_data in sample_strategies:
                    strategy = AIStrategy(**strategy_data)
                    self.save_strategy(strategy)
    
    def save_strategy(self, strategy: AIStrategy):
        """Save or update a strategy in the database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO strategies 
                (country_code, country_name, strategy_title, publication_date, status, data_json, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                strategy.country_code,
                strategy.country_name,
                strategy.strategy_title,
                strategy.publication_date,
                strategy.status,
                json.dumps(asdict(strategy)),
                datetime.now().isoformat()
            ))
    
    def get_country_strategy(self, country_code: str) -> Optional[Dict[str, Any]]:
        """Get strategy data for a specific country"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT data_json FROM strategies WHERE country_code = ?",
                (country_code,)
            )
            result = cursor.fetchone()
            
            if result:
                return json.loads(result[0])
            return None
    
    def get_all_countries(self) -> List[Dict[str, str]]:
        """Get list of all countries with AI strategies"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT country_code, country_name, status FROM strategies ORDER BY country_name"
            )
            return [
                {"code": row[0], "name": row[1], "status": row[2]}
                for row in cursor.fetchall()
            ]
    
    def count_strategies(self) -> int:
        """Get total number of strategies"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM strategies")
            return cursor.fetchone()[0]
    
    def search_strategies(self, query: str) -> List[Dict[str, Any]]:
        """Search strategies by text query"""
        results = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT country_code, country_name, data_json FROM strategies"
            )
            
            for row in cursor.fetchall():
                strategy_data = json.loads(row[2])
                # Simple text search in strategy content
                search_text = json.dumps(strategy_data).lower()
                if query.lower() in search_text:
                    results.append({
                        "country_code": row[0],
                        "country_name": row[1],
                        "relevance": search_text.count(query.lower())
                    })
        
        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results
    
    def get_strategies_by_theme(self, theme: str) -> List[str]:
        """Get countries that have a specific theme"""
        countries = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT country_code, data_json FROM strategies")
            
            for row in cursor.fetchall():
                strategy_data = json.loads(row[1])
                if theme in strategy_data.get('themes', []):
                    countries.append(row[0])
        
        return countries
