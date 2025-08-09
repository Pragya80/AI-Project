#!/bin/bash

# LinkedIn AI Agent - Development Setup Script

echo "LinkedIn Personal Branding AI Agent - Development Setup"
echo "======================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null
then
    echo "Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "pip is not installed. Please install pip first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env with your actual API keys:"
    echo "nano .env"
    echo ""
fi

echo "Setting up backend development environment..."
echo "-------------------------------------------"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Setting up frontend development environment..."
echo "--------------------------------------------"

# Navigate to frontend directory
if [ ! -d "frontend" ]; then
    echo "Frontend directory not found!"
    exit 1
fi

cd frontend

# Install Node dependencies
echo "Installing Node dependencies..."
npm install

echo ""
echo "Development environment setup complete!"
echo "======================================"
echo ""
echo "To run the application in development mode:"
echo ""
echo "1. Start the backend:"
echo "   uvicorn app.main:app --reload"
echo ""
echo "2. In another terminal, start the frontend:"
echo "   cd frontend && npm start"
echo ""
echo "3. Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"