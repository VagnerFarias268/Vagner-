#!/bin/bash
# Quick start script for Mac/Linux (without venv)

echo ""
echo "========================================"
echo "  Starting Vagner Sales Agent"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and configure it"
    exit 1
fi

echo "Starting server..."
echo "Server will be available at: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Press CTRL+C to stop"
echo ""

# Start with uvicorn
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

