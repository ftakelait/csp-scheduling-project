#!/bin/bash

# Simple script to start the development environment
# This bypasses Docker Compose interactive issues

echo "Starting AI Course Development Environment..."
echo ""

# Stop any existing containers
docker-compose down

# Build the image if needed
docker-compose build

# Start the container in detached mode
docker-compose up -d ai-course-dev

echo ""
echo "Container started in background."
echo "Attaching to container..."
echo ""

# Attach to the running container
docker-compose exec ai-course-dev /bin/bash

echo ""
echo "Container stopped." 