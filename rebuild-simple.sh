#!/bin/bash

# Simple rebuild script for the simplified CSP project
# This rebuilds with all the student-friendly changes

echo "==============================================="
echo "Rebuilding Simplified CSP Project (Difficulty: 5/10)"
echo "==============================================="
echo ""

# Stop all containers
echo "Stopping containers..."
docker-compose down

# Clean up Docker cache
echo "Cleaning up Docker cache..."
docker system prune -f

# Rebuild with no cache
echo "Rebuilding Docker image with simplifications..."
echo "Changes made:"
echo "  - Simplified data structure (no dependencies)"
echo "  - Reduced constraints (easier to solve)"
echo "  - Fixed visualization issues"
echo "  - Better error handling"
echo "  - Student-friendly difficulty level"
echo ""
docker-compose build --no-cache

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Rebuild successful!"
    echo ""
    echo "The project is now simplified and student-friendly:"
    echo "  - Difficulty: 5/10 (was 9/10)"
    echo "  - Easier to find solutions"
    echo "  - Working visualizations"
    echo "  - Better error handling"
    echo ""
    echo "To start the development environment:"
    echo "  docker run -it --rm \\"
    echo "    -v ~/ai-course-work:/workspace/student_work \\"
    echo "    -v ~/ai-course-data:/workspace/data \\"
    echo "    -v ~/ai-course-output:/workspace/output \\"
    echo "    -v ~/ai-course-projects:/workspace/projects \\"
    echo "    mycourse-ai-course-dev"
    echo ""
    echo "To test the solution:"
    echo "  cd /workspace/assignments/csp-scheduling-project/"
    echo "  python src/csp_scheduling_project_sol.py"
else
    echo "❌ Rebuild failed"
    exit 1
fi 