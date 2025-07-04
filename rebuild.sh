#!/bin/bash

# Rebuild script for AI Course Development Environment
# Use this when you need to get the latest updates

echo "==============================================="
echo "Rebuilding AI Course Development Environment"
echo "==============================================="
echo ""

# Stop all containers
echo "Stopping containers..."
docker-compose down

# Clean up Docker cache
echo "Cleaning up Docker cache..."
docker system prune -f

# Rebuild with no cache
echo "Rebuilding Docker image (this may take a few minutes)..."
echo "Using --no-cache to ensure latest version..."
docker-compose build --no-cache

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Rebuild successful!"
    echo ""
    echo "To start the development environment:"
    echo "  docker run -it --rm \\"
    echo "    -v ~/ai-course-work:/workspace/student_work \\"
    echo "    -v ~/ai-course-data:/workspace/data \\"
    echo "    -v ~/ai-course-output:/workspace/output \\"
    echo "    -v ~/ai-course-projects:/workspace/projects \\"
    echo "    mycourse-ai-course-dev"
    echo ""
    echo "Or use the simple command:"
    echo "  ./start-simple.sh"
else
    echo "❌ Rebuild failed"
    exit 1
fi 