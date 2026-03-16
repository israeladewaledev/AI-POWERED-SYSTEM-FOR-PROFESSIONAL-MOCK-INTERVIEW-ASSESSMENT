#!/bin/bash

# VocalAce Local STT Service Setup
echo "🚀 Setting up Local Speech-to-Text Service..."

# Navigate to service directory
cd stt-service

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies (faster-whisper, fastapi)..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo "🏃 To start the service, run: source stt-service/venv/bin/activate && python stt-service/main.py"
