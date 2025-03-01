#!/bin/bash
# Quick setup script for Materials Research Aggregator

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install the package and dependencies
echo "Installing dependencies..."
pip install -e .

# Check for Materials Project API key
if [ -z "$MATERIALS_PROJECT_API_KEY" ]; then
    echo ""
    echo "IMPORTANT: You need to set your Materials Project API key."
    echo "Get your key from https://materialsproject.org/dashboard"
    echo ""
    echo "Then set it with:"
    echo "export MATERIALS_PROJECT_API_KEY='your_api_key'"
    echo ""
fi

# Run a simple test
echo "Testing installation..."
python -c "from materials_aggregator import MaterialsResearchAggregator; print('Installation successful!')"

echo ""
echo "✓ Setup complete! Use the tool with: materials_aggregator"
echo "Example: materials_aggregator search Li,O --limit 5"
echo ""