"""
Data collection and processing for African AI Strategies Portal
"""

import json
import requests
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCollector:
    """Collects and processes AI strategy data from various sources"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        
        # Create directories
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Known AI strategy sources
        self.strategy_sources = {
            "KE": {
                "name": "Kenya",
                "urls": [
                    "https://www.ict.go.ke/wp-content/uploads/2022/03/Kenya-AI-Strategy.pdf",
                    "https://www.ict.go.ke/ai-strategy-summary"
                ],
                "status": "published"
            },
            "NG": {
                "name": "Nigeria", 
                "urls": [
                    "https://nitda.gov.ng/wp-content/uploads/2021/11/National-AI-Strategy.pdf"
                ],
                "status": "published"
            },
            "ZA": {
                "name": "South Africa",
                "urls": [
                    "https://www.dst.gov.za/images/2021/AI_Strategy_eng.pdf"
                ],
                "status": "published"
            },
            "EG": {
                "name": "Egypt",
                "urls": [
                    "https://mcit.gov.eg/en/Digital_Egypt/Artificial_Intelligence_Strategy"
                ],
                "status": "published"
            },
            "MA": {
                "name": "Morocco",
                "urls": [
                    "https://www.maroc.ma/en/content/morocco-artificial-intelligence-strategy"
                ],
                "status": "draft"
            },
            "TN": {
                "name": "Tunisia",
                "urls": [
                    "https://www.tunisie.gov.tn/en/actualites/tunisia-ai-strategy"
                ],
                "status": "under_development"
            },
            "GH": {
                "name": "Ghana",
                "urls": [
                    "https://www.moc.gov.gh/ai-strategy"
                ],
                "status": "draft"
            },
            "RW": {
                "name": "Rwanda",
                "urls": [
                    "https://www.minict.gov.rw/ai-strategy"
                ],
                "status": "published"
            },
            "ET": {
                "name": "Ethiopia",
                "urls": [
                    "https://www.ethioict.gov.et/ai-strategy"
                ],
                "status": "under_development"
            },
            "UG": {
                "name": "Uganda",
                "urls": [
                    "https://www.ict.go.ug/ai-strategy"
                ],
                "status": "draft"
            }
        }
    
    def load_initial_data(self):
        """Load initial sample data for demonstration"""
        logger.info("Loading initial sample data...")
        
        # Create sample data files
        sample_data = {
            "countries_overview": {
                "total_countries": len(self.strategy_sources),
                "published_strategies": len([s for s in self.strategy_sources.values() if s["status"] == "published"]),
                "draft_strategies": len([s for s in self.strategy_sources.values() if s["status"] == "draft"]),
                "under_development": len([s for s in self.strategy_sources.values() if s["status"] == "under_development"]),
                "last_updated": datetime.now().isoformat()
            },
            "strategy_sources": self.strategy_sources
        }
        
        # Save overview data
        with open(self.processed_dir / "countries_overview.json", "w") as f:
            json.dump(sample_data, f, indent=2)
        
        # Create detailed sample strategies
        self._create_sample_strategies()
        
        logger.info("✓ Initial data loaded successfully")
    
    def _create_sample_strategies(self):
        """Create detailed sample strategy data"""
        
        # Enhanced Kenya strategy data
        kenya_strategy = {
            "country_code": "KE",
            "country_name": "Kenya",
            "strategy_title": "Kenya National Artificial Intelligence Strategy 2022-2027",
            "publication_date": "2022-03-15",
            "status": "published",
            "executive_summary": "Kenya's AI strategy aims to position the country as a leader in AI adoption and innovation in Africa, focusing on economic transformation and social development.",
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
                },
                {
                    "name": "AI Adoption and Innovation",
                    "description": "Promote AI adoption across priority sectors",
                    "key_actions": [
                        "Support AI startups and SMEs",
                        "Facilitate public-private partnerships",
                        "Create AI sandbox environments",
                        "Develop sector-specific AI solutions"
                    ]
                },
                {
                    "name": "Ethics and Governance",
                    "description": "Ensure responsible and ethical AI development",
                    "key_actions": [
                        "Develop AI ethics guidelines",
                        "Establish AI governance structures",
                        "Create AI regulatory frameworks",
                        "Promote transparency and accountability"
                    ]
                }
            ],
            "priority_sectors": [
                {
                    "name": "Agriculture",
                    "ai_applications": ["Precision farming", "Crop monitoring", "Market intelligence", "Supply chain optimization"],
                    "expected_impact": "Increase agricultural productivity by 30%"
                },
                {
                    "name": "Healthcare",
                    "ai_applications": ["Medical diagnosis", "Drug discovery", "Telemedicine", "Health records management"],
                    "expected_impact": "Improve healthcare access and quality"
                },
                {
                    "name": "Education",
                    "ai_applications": ["Personalized learning", "Automated assessment", "Educational content creation", "Student analytics"],
                    "expected_impact": "Enhance learning outcomes and accessibility"
                },
                {
                    "name": "Financial Services",
                    "ai_applications": ["Credit scoring", "Fraud detection", "Robo-advisory", "Mobile payments"],
                    "expected_impact": "Increase financial inclusion to 85%"
                }
            ],
            "key_initiatives": [
                {
                    "name": "Kenya AI Innovation Hub",
                    "description": "Establish world-class AI research and innovation center",
                    "budget": "USD 50 million",
                    "timeline": {"start": "2022", "end": "2025"},
                    "partners": ["Universities", "Private sector", "International organizations"],
                    "expected_outcomes": ["100 AI startups incubated", "500 AI researchers trained", "50 AI solutions developed"]
                },
                {
                    "name": "Digital Skills for All Program",
                    "description": "Train 100,000 Kenyans in AI and digital skills",
                    "budget": "USD 30 million",
                    "timeline": {"start": "2022", "end": "2027"},
                    "partners": ["Technical institutions", "Private sector", "Development partners"],
                    "expected_outcomes": ["100,000 people trained", "50,000 jobs created", "1,000 AI specialists certified"]
                },
                {
                    "name": "AI for Agriculture Platform",
                    "description": "Deploy AI solutions for smallholder farmers",
                    "budget": "USD 20 million",
                    "timeline": {"start": "2023", "end": "2026"},
                    "partners": ["Agricultural organizations", "Tech companies", "Farmer cooperatives"],
                    "expected_outcomes": ["1 million farmers reached", "25% increase in yields", "30% reduction in post-harvest losses"]
                }
            ],
            "governance_structure": {
                "steering_committee": {
                    "name": "National AI Steering Committee",
                    "chair": "Cabinet Secretary, Ministry of ICT",
                    "members": ["Government agencies", "Private sector", "Academia", "Civil society"],
                    "mandate": "Provide strategic oversight and policy direction"
                },
                "implementation_unit": {
                    "name": "AI Implementation Unit",
                    "host": "ICT Authority",
                    "mandate": "Coordinate strategy implementation and monitoring"
                },
                "advisory_council": {
                    "name": "AI Advisory Council",
                    "composition": "AI experts, industry leaders, researchers",
                    "mandate": "Provide technical advice and guidance"
                }
            },
            "funding_strategy": {
                "total_budget": "USD 200 million over 5 years",
                "funding_sources": [
                    {"source": "Government budget", "percentage": 40, "amount": "USD 80M"},
                    {"source": "Development partners", "percentage": 35, "amount": "USD 70M"},
                    {"source": "Private sector", "percentage": 25, "amount": "USD 50M"}
                ],
                "funding_mechanisms": ["Direct budget allocation", "Tax incentives", "Innovation funds", "PPP arrangements"]
            },
            "implementation_timeline": {
                "phase1": {
                    "period": "2022-2024",
                    "focus": "Foundation building",
                    "key_milestones": ["Establish governance structures", "Launch key initiatives", "Build basic infrastructure"]
                },
                "phase2": {
                    "period": "2025-2027",
                    "focus": "Scale and expansion",
                    "key_milestones": ["Scale successful initiatives", "Expand to all sectors", "Achieve key targets"]
                }
            },
            "monitoring_evaluation": {
                "kpis": [
                    {"indicator": "AI readiness index ranking", "baseline": "65th globally", "target": "Top 50 globally"},
                    {"indicator": "AI startups", "baseline": "50", "target": "500"},
                    {"indicator": "AI professionals", "baseline": "1,000", "target": "10,000"},
                    {"indicator": "AI adoption rate", "baseline": "15%", "target": "60%"}
                ],
                "reporting": "Annual progress reports to Parliament",
                "evaluation": "Mid-term and final evaluations by independent experts"
            },
            "international_cooperation": [
                {"organization": "African Union", "focus": "Continental AI coordination"},
                {"organization": "UN", "focus": "AI for SDGs"},
                {"organization": "World Bank", "focus": "Funding and technical assistance"},
                {"organization": "Partnership on AI", "focus": "Best practices and standards"}
            ],
            "challenges_risks": [
                {"challenge": "Limited AI skills", "mitigation": "Massive skills development programs"},
                {"challenge": "Infrastructure gaps", "mitigation": "Accelerated digital infrastructure development"},
                {"challenge": "Regulatory uncertainty", "mitigation": "Develop clear AI governance frameworks"},
                {"challenge": "Ethical concerns", "mitigation": "Strong ethics and accountability mechanisms"}
            ]
        }
        
        # Save Kenya strategy
        with open(self.processed_dir / "strategy_KE.json", "w") as f:
            json.dump(kenya_strategy, f, indent=2)
        
        # Create similar detailed data for other countries (abbreviated for space)
        other_strategies = {
            "NG": {
                "country_name": "Nigeria",
                "strategy_title": "National Artificial Intelligence Strategy for Nigeria",
                "focus_areas": ["Research Excellence", "Talent Pipeline", "Industry Adoption", "Governance"],
                "budget": "USD 300 million"
            },
            "ZA": {
                "country_name": "South Africa", 
                "strategy_title": "South Africa's National Artificial Intelligence Strategy",
                "focus_areas": ["Innovation", "Skills", "Responsible AI", "Economic Growth"],
                "budget": "USD 250 million"
            }
        }
        
        for code, data in other_strategies.items():
            with open(self.processed_dir / f"strategy_{code}.json", "w") as f:
                json.dump(data, f, indent=2)
    
    def collect_strategy_document(self, country_code: str, url: str) -> Optional[Dict[str, Any]]:
        """Collect and process a strategy document from URL"""
        try:
            logger.info(f"Collecting strategy document for {country_code} from {url}")
            
            # In a real implementation, this would:
            # 1. Download the PDF/document
            # 2. Extract text using OCR/PDF parsing
            # 3. Process and structure the content
            # 4. Extract key information using NLP
            
            # For now, return placeholder data
            return {
                "country_code": country_code,
                "source_url": url,
                "collected_at": datetime.now().isoformat(),
                "status": "collected",
                "content_length": 0,
                "processing_status": "pending"
            }
            
        except Exception as e:
            logger.error(f"Error collecting document for {country_code}: {e}")
            return None
    
    def process_raw_document(self, country_code: str, raw_content: str) -> Dict[str, Any]:
        """Process raw document content and extract structured data"""
        # This would use NLP techniques to extract:
        # - Vision and mission statements
        # - Key objectives and goals
        # - Priority sectors and applications
        # - Implementation timelines
        # - Budget and funding information
        # - Governance structures
        
        # Placeholder implementation
        processed_data = {
            "country_code": country_code,
            "processed_at": datetime.now().isoformat(),
            "extraction_method": "automated_nlp",
            "confidence_score": 0.85,
            "extracted_sections": {
                "vision": "Extracted vision statement...",
                "objectives": ["Objective 1", "Objective 2"],
                "sectors": ["Agriculture", "Healthcare", "Education"],
                "timeline": {"start": "2022", "end": "2027"}
            }
        }
        
        return processed_data
    
    def update_strategy_data(self, country_code: str) -> bool:
        """Update strategy data for a specific country"""
        try:
            if country_code not in self.strategy_sources:
                logger.error(f"Unknown country code: {country_code}")
                return False
            
            country_info = self.strategy_sources[country_code]
            logger.info(f"Updating strategy data for {country_info['name']}")
            
            # Collect from all available sources
            for url in country_info["urls"]:
                document_data = self.collect_strategy_document(country_code, url)
                if document_data:
                    # Save raw data
                    raw_file = self.raw_dir / f"{country_code}_raw.json"
                    with open(raw_file, "w") as f:
                        json.dump(document_data, f, indent=2)
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating strategy data for {country_code}: {e}")
            return False
    
    def get_collection_status(self) -> Dict[str, Any]:
        """Get status of data collection for all countries"""
        status = {
            "total_countries": len(self.strategy_sources),
            "collection_status": {},
            "last_updated": datetime.now().isoformat()
        }
        
        for code, info in self.strategy_sources.items():
            raw_file = self.raw_dir / f"{code}_raw.json"
            processed_file = self.processed_dir / f"strategy_{code}.json"
            
            status["collection_status"][code] = {
                "country_name": info["name"],
                "strategy_status": info["status"],
                "raw_data_available": raw_file.exists(),
                "processed_data_available": processed_file.exists(),
                "urls_count": len(info["urls"])
            }
        
        return status
