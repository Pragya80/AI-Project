#!/bin/bash

# LinkedIn AI Agent - Setup and Run Script

echo "LinkedIn Personal Branding AI Agent"
echo "===================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null
then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env with your actual API keys and then run this script again."
    echo "You can edit the file with: nano .env"
    exit 0
fi

echo "Starting LinkedIn AI Agent..."

# Build and start services
echo "Building and starting services..."
docker-compose up --build

echo "Application is now running!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"