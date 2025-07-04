#!/bin/bash

# AI Course Development Environment Setup Script
# Students can run this from anywhere to set up the Docker environment

echo "==============================================="
echo "AI Course Development Environment Setup"
echo "==============================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "Please install Docker first:"
    echo "  - Windows/Mac: https://docs.docker.com/desktop/"
    echo "  - Linux: https://docs.docker.com/engine/install/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed!"
    echo "Please install Docker Compose first:"
    echo "  - Windows/Mac: Usually comes with Docker Desktop"
    echo "  - Linux: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Create necessary directories in student's home
echo "Creating directories in your home folder..."
mkdir -p ~/ai-course-work
mkdir -p ~/ai-course-data
mkdir -p ~/ai-course-output
mkdir -p ~/ai-course-projects
mkdir -p ~/ai-course-submissions
mkdir -p ~/ai-course-grading

echo "✅ Directories created in your home folder:"
echo "  - ~/ai-course-work/ (for your assignment work)"
echo "  - ~/ai-course-data/ (for data files)"
echo "  - ~/ai-course-output/ (for generated files)"
echo "  - ~/ai-course-projects/ (for your own projects)"
echo "  - ~/ai-course-submissions/ (for submitting assignments)"
echo "  - ~/ai-course-grading/ (for grading results)"
echo ""

# Check if Dockerfile and docker-compose.yml exist in current directory
if [ ! -f "Dockerfile" ] || [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Dockerfile and docker-compose.yml not found!"
    echo ""
    echo "Please make sure you have these files in your current directory:"
    echo "  - Dockerfile"
    echo "  - docker-compose.yml"
    echo ""
    echo "If you don't have them, download them from your instructor."
    exit 1
fi

# Clean up any existing containers and images
echo "Cleaning up existing containers and images..."
docker-compose down
docker system prune -f

# Build the Docker image
echo "Building Docker image (this may take a few minutes)..."
echo "The image will clone the course repository: https://github.com/ftakelait/csp-scheduling-project/"
echo "Using --no-cache to ensure latest version..."
docker-compose build --no-cache

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
else
    echo "❌ Failed to build Docker image"
    exit 1
fi

echo ""
echo "==============================================="
echo "Setup Complete! 🎉"
echo "==============================================="
echo ""
echo "The Docker environment is ready with the course repository!"
echo ""
echo "To start the development environment (recommended):"
echo "  docker run -it --rm \\"
echo "    -v ~/ai-course-work:/workspace/student_work \\"
echo "    -v ~/ai-course-data:/workspace/data \\"
echo "    -v ~/ai-course-output:/workspace/output \\"
echo "    -v ~/ai-course-projects:/workspace/projects \\"
echo "    mycourse-ai-course-dev"
echo ""
echo "Alternative methods:"
echo "  docker-compose up ai-course-dev"
echo "  docker-compose up jupyter"
echo ""
echo "To run the CSP assignment:"
echo "  docker run --rm mycourse-ai-course-dev run_assignment csp-scheduling-project"
echo ""
echo "Your work will be saved in:"
echo "  ~/ai-course-work/ (assignment work)"
echo "  ~/ai-course-projects/ (your projects)"
echo "  ~/ai-course-output/ (generated files)"
echo ""
echo "Course Repository: https://github.com/ftakelait/csp-scheduling-project/"
echo ""
echo "Happy coding! 🚀" 