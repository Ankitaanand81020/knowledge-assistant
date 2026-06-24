#!/bin/bash
# Quick setup script for Knowledge Assistant

set -e

echo "🚀 Knowledge Assistant - Setup Script"
echo "======================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3.11+ not found. Please install from python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION found"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 18+ not found. Please install from nodejs.org"
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✅ Node.js $NODE_VERSION found"

# Check Ollama
echo ""
echo "Checking for Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama not found in PATH"
    echo "   Download from: https://ollama.ai"
    echo "   After installing, run: ollama pull qwen2.5:1.5b"
else
    echo "✅ Ollama found"
fi

# Backend setup
echo ""
echo "📦 Setting up backend..."
cd backend

# Create venv
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

# Generate synthetic data
echo "🎲 Generating synthetic documents..."
python tools/synth_data.py

# Reindex
echo "🔄 Building vector index..."
python tools/reindex.py

cd ..

# Frontend setup
echo ""
echo "📦 Setting up frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    npm install
fi

# Create .env.local if not exists
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    cp .env.example .env.local
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Start Ollama: ollama serve"
echo "2. Run the app: make run"
echo "3. Visit http://localhost:3000"
echo ""
echo "For more info, see README.md"
