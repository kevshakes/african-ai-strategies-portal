# Data Directory Structure

This directory contains the data files for the African AI Strategies Portal.

## Directory Structure

```
data/
├── raw/           # Original strategy documents (PDFs, Word docs)
├── processed/     # Cleaned and structured JSON data
├── analysis/      # Analysis results and insights
└── demo/          # Sample data for demonstration
```

## Data Sources

The portal aggregates data from:
- Official government AI strategy documents
- Policy papers and white papers
- International organization reports (AU, UN, World Bank)
- Academic research and analysis

## Data Format

All processed data follows a standardized JSON schema for consistency:

### Country Strategy Schema
```json
{
  "country_code": "KE",
  "country_name": "Kenya",
  "strategy_title": "Kenya National Artificial Intelligence Strategy 2022-2027",
  "publication_date": "2022-03-15",
  "status": "published",
  "vision": "Strategy vision statement",
  "objectives": ["List of objectives"],
  "priority_sectors": ["Agriculture", "Healthcare", "Education"],
  "key_initiatives": [
    {
      "name": "Initiative name",
      "description": "Description",
      "budget": "USD 50M",
      "timeline": {"start": "2022", "end": "2025"}
    }
  ],
  "governance_structure": {},
  "funding_mechanisms": [],
  "themes": ["Skills Development", "Innovation"],
  "cross_cutting_issues": [],
  "international_cooperation": []
}
```

## Usage

The data is automatically loaded by the application. To add new countries:

1. Place raw documents in `raw/` directory
2. Run the data collector: `python src/data_collector.py`
3. Processed data will be saved to `processed/` directory
4. Analysis results will be generated in `analysis/` directory

## Data Privacy and Ethics

- All data used is from publicly available sources
- No personal or sensitive information is stored
- Data is used solely for research and policy analysis purposes
- Attribution is provided for all data sources
