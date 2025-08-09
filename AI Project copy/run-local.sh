#!/bin/bash

# LinkedIn AI Agent - Local Development Run Script

echo "LinkedIn Personal Branding AI Agent - Local Run"
echo "=============================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "pip is not installed. Please install pip first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null
then
    echo "Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env with your actual API keys:"
    echo "nano .env"
    echo ""
    echo "You need to add your Groq API key to the .env file for content generation to work."
    exit 0
fi

echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Starting backend server..."
# Start backend in background
uvicorn app.main:app --reload &
BACKEND_PID=$!

echo "Setting up frontend..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo "Starting frontend server..."
# Start frontend
npm start

# Kill backend process when frontend stops
kill $BACKEND_PID