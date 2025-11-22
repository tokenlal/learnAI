#!/bin/bash

# Script to run RAG POC with Rancher Desktop
# This sets up the PATH for Rancher Desktop's Docker CLI

# Add Rancher Desktop binaries to PATH
export PATH="/Applications/Rancher Desktop.app/Contents/Resources/resources/darwin/bin:$PATH"

echo "🐳 Using Rancher Desktop Docker..."
echo "Docker version: $(docker --version)"
echo "Docker Compose version: $(docker compose version)"
echo ""

# Check if Rancher Desktop is running
if ! docker info &> /dev/null; then
    echo "❌ Docker engine not accessible. Please ensure Rancher Desktop is running."
    exit 1
fi

echo "✅ Docker engine is running"
echo ""

# Run the docker-compose command based on the argument
case "$1" in
    "up")
        echo "🚀 Starting services..."
        docker compose up -d
        ;;
    "down")
        echo "🛑 Stopping services..."
        docker compose down
        ;;
    "logs")
        echo "📝 Showing logs..."
        docker compose logs -f
        ;;
    "ps")
        echo "📋 Container status..."
        docker compose ps
        ;;
    "restart")
        echo "🔄 Restarting services..."
        docker compose restart
        ;;
    *)
        echo "Usage: $0 {up|down|logs|ps|restart}"
        echo ""
        echo "Commands:"
        echo "  up      - Start all services in detached mode"
        echo "  down    - Stop and remove all services"
        echo "  logs    - Show and follow service logs"
        echo "  ps      - Show running containers"
        echo "  restart - Restart all services"
        ;;
esac