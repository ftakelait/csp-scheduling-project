#!/bin/bash

# Script to start interactive development environment
# This works around Windows Docker interactive issues

echo "Starting AI Course Development Environment..."
echo ""

# Stop any existing containers
docker-compose down

# Build the image
echo "Building Docker image..."
docker-compose build --no-cache

# Start container in detached mode
echo "Starting container in background..."
docker-compose up -d ai-course-dev

# Wait a moment for container to be ready
sleep 3

# Check if container is running
if docker-compose ps | grep -q "Up"; then
    echo "Container is running. Attaching..."
    echo ""
    
    # Try to attach with interactive bash
    docker-compose exec -it ai-course-dev /bin/bash
    
    echo ""
    echo "Container stopped."
else
    echo "Error: Container failed to start"
    docker-compose logs ai-course-dev
fi 