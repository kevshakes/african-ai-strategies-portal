#!/bin/bash

# African AI Strategies Portal - Installation Script
echo "🌍 Installing African AI Strategies Portal..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✓ Python $python_version detected (>= 3.8 required)"
else
    echo "❌ Python 3.8+ required. Current version: $python_version"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/{raw,processed,analysis}
mkdir -p static/{css,js,images}
mkdir -p templates

# Initialize database
echo "🗄️ Initializing database..."
python3 -c "
from src.models import StrategyDatabase
db = StrategyDatabase()
print('✓ Database initialized successfully')
"

# Load initial data
echo "📊 Loading initial data..."
python3 -c "
from src.data_collector import DataCollector
collector = DataCollector()
collector.load_initial_data()
print('✓ Initial data loaded successfully')
"

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "To start the portal:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the application: python3 app.py"
echo "  3. Open browser to: http://localhost:5000"
echo ""
echo "📚 Documentation: See README.md for detailed usage instructions"
echo "🐛 Issues: Report at https://github.com/your-repo/issues"
