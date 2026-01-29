#!/bin/bash

# Brute Force Detection API - Startup Script (usando venv de cbproy)

echo "🚀 Starting Brute Force Detection API..."
echo ""

# Check if we're in the correct directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the api/ directory."
    exit 1
fi

# Path to shared venv
VENV_PATH="/home/megalodon/dev/cbproy/venv"

# Check if shared venv exists
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Error: Shared venv not found at $VENV_PATH"
    exit 1
fi

# Activate virtual environment
echo "🔧 Using shared virtual environment at $VENV_PATH"
source "$VENV_PATH/bin/activate"

# Verify dependencies are installed
echo "📦 Checking dependencies..."
python -c "import fastapi, uvicorn, pydantic, joblib, sklearn, pandas, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: Some dependencies are missing in the shared venv."
    exit 1
fi

# Check if model exists
if [ ! -f "../modeling/outputs/models/random_forest_20260117_021309.pkl" ]; then
    echo "❌ Error: Model file not found at ../modeling/outputs/models/random_forest_20260117_021309.pkl"
    echo "   Please run the modeling notebook first to train the model."
    exit 1
fi

echo "✅ All dependencies available"
echo ""
echo "🌐 Starting API server..."
echo "   URL: http://localhost:8002"
echo "   Docs: http://localhost:8002/docs"
echo ""
echo "   Press Ctrl+C to stop"
echo ""

# Start API
python app.py
