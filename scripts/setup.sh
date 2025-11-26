#!/bin/bash

# Sentinel Setup Script
# Quick setup for local development

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "🛠️  Sentinel - Local Development Setup"
echo "======================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
cd "$PROJECT_ROOT"

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "📦 Upgrading pip..."
python -m pip install --upgrade pip --quiet

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    echo "✅ Dependencies installed"
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Install development dependencies
echo ""
echo "📦 Installing development dependencies..."
pip install pytest pytest-cov pytest-mock black flake8 mypy isort --quiet
echo "✅ Development dependencies installed"

# Create .env file if it doesn't exist
echo ""
echo "⚙️  Setting up configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ .env file created from template"
    echo "ℹ️  Edit .env file to add your AWS configuration"
else
    echo "ℹ️  .env file already exists"
fi

# Run tests
echo ""
echo "🧪 Running tests..."
pytest tests/ -v

if [ $? -eq 0 ]; then
    echo "✅ All tests passed"
else
    echo "⚠️  Some tests failed"
fi

# Summary
echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Edit .env file with your AWS credentials"
echo ""
echo "3. Run the dashboard:"
echo "   streamlit run src/dashboard/app.py"
echo ""
echo "4. Run tests:"
echo "   pytest"
echo ""
echo "Happy coding! 🚀"
