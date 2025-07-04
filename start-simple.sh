#!/bin/bash

# Simple script to start the development environment
# Uses docker run which works reliably on all platforms

echo "Starting AI Course Development Environment..."
echo ""

# Check if image exists
if ! docker images | grep -q "mycourse-ai-course-dev"; then
    echo "Building Docker image..."
    docker-compose build
fi

echo "Starting interactive container..."
echo ""

# Start the container with volume mounts
docker run -it --rm \
  -v ~/ai-course-work:/workspace/student_work \
  -v ~/ai-course-data:/workspace/data \
  -v ~/ai-course-output:/workspace/output \
  -v ~/ai-course-projects:/workspace/projects \
  mycourse-ai-course-dev

echo ""
echo "Container stopped." 