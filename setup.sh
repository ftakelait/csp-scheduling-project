#!/bin/bash

# AI Course Development Environment Setup Script
# This script sets up the Docker environment for students

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

# Create necessary directories
echo "Creating directories..."
mkdir -p student_data
mkdir -p output
mkdir -p student_projects
mkdir -p student_submissions
mkdir -p grading_reports

echo "✅ Directories created:"
echo "  - student_data/ (for your data files)"
echo "  - output/ (for generated files)"
echo "  - student_projects/ (for your own projects)"
echo "  - student_submissions/ (for assignment submissions)"
echo "  - grading_reports/ (for grading results)"
echo ""

# Build the Docker image
echo "Building Docker image (this may take a few minutes)..."
docker-compose build

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
echo "To start the development environment:"
echo "  docker-compose up ai-course-dev"
echo ""
echo "To start Jupyter Notebook:"
echo "  docker-compose up jupyter"
echo ""
echo "To run a specific assignment:"
echo "  docker-compose run --rm ai-course-dev run_assignment csp-scheduling-project"
echo ""
echo "To grade a student submission:"
echo "  docker-compose run --rm grader grade_assignment /workspace/student_submissions/student_file.py"
echo ""
echo "Useful commands:"
echo "  - docker-compose ps (check running containers)"
echo "  - docker-compose down (stop all containers)"
echo "  - docker-compose logs (view logs)"
echo ""
echo "Happy coding! 🚀" 