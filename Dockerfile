# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/workspace
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    vim \
    nano \
    tree \
    htop \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create workspace directory
WORKDIR /workspace

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional development tools
RUN pip install --no-cache-dir \
    ipython \
    jupyter \
    pytest \
    black \
    flake8 \
    mypy \
    pre-commit

# Create project structure
RUN mkdir -p /workspace/projects \
    && mkdir -p /workspace/assignments \
    && mkdir -p /workspace/tools \
    && mkdir -p /workspace/data \
    && mkdir -p /workspace/output

# Copy the current project to assignments folder
COPY . /workspace/assignments/csp-scheduling-project/

# Create a welcome script
RUN echo '#!/bin/bash\n\
echo "==============================================="\n\
echo "Welcome to the AI Course Development Environment"\n\
echo "==============================================="\n\
echo ""\n\
echo "Available projects and assignments:"\n\
echo "1. CSP Scheduling Project: /workspace/assignments/csp-scheduling-project/"\n\
echo "2. Other projects: /workspace/projects/"\n\
echo "3. Tools: /workspace/tools/"\n\
echo ""\n\
echo "Quick start commands:"\n\
echo "- cd /workspace/assignments/csp-scheduling-project/"\n\
echo "- python src/csp_scheduling_project.py"\n\
echo "- python test_project.py"\n\
echo "- python gui/scheduler_gui.py"\n\
echo ""\n\
echo "Development tools:"\n\
echo "- jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root"\n\
echo "- python -m http.server 8000"  # For serving files\n\
echo ""\n\
echo "Current directory: $(pwd)"\n\
echo "==============================================="\n\
' > /workspace/welcome.sh && chmod +x /workspace/welcome.sh

# Create a development script
RUN echo '#!/bin/bash\n\
# Development environment setup\n\
export PYTHONPATH=/workspace:$PYTHONPATH\n\
export PATH=/workspace/tools:$PATH\n\
\n\
# Set up git if not already configured\n\
if [ ! -f ~/.gitconfig ]; then\n\
    echo "Setting up git configuration..."\n\
    git config --global user.name "Student"\n\
    git config --global user.email "student@university.edu"\n\
fi\n\
\n\
# Start bash with custom prompt\n\
export PS1="\[\033[01;32m\]\u@ai-course\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ "\n\
exec bash\n\
' > /workspace/dev.sh && chmod +x /workspace/dev.sh

# Create a project template
RUN echo '#!/bin/bash\n\
# Project template creator\n\
if [ $# -eq 0 ]; then\n\
    echo "Usage: create_project <project_name>"\n\
    exit 1\n\
fi\n\
\n\
PROJECT_NAME=$1\n\
PROJECT_DIR="/workspace/projects/$PROJECT_NAME"\n\
\n\
if [ -d "$PROJECT_DIR" ]; then\n\
    echo "Project $PROJECT_NAME already exists!"\n\
    exit 1\n\
fi\n\
\n\
mkdir -p "$PROJECT_DIR"\n\
cd "$PROJECT_DIR"\n\
\n\
# Create basic project structure\n\
mkdir -p src tests data docs\n\
\n\
# Create README\n\
cat > README.md << EOF\n\
# $PROJECT_NAME\n\
\n\
## Description\n\
Add your project description here.\n\
\n\
## Setup\n\
\`\`\`bash\n\
pip install -r requirements.txt\n\
\`\`\`\n\
\n\
## Usage\n\
\`\`\`bash\n\
python src/main.py\n\
\`\`\`\n\
\n\
## Testing\n\
\`\`\`bash\n\
pytest tests/\n\
\`\`\`\n\
EOF\n\
\n\
# Create requirements.txt\n\
cat > requirements.txt << EOF\n\
# Add your project dependencies here\n\
pandas>=1.3.0\n\
numpy>=1.21.0\n\
matplotlib>=3.4.0\n\
EOF\n\
\n\
# Create main.py\n\
cat > src/main.py << EOF\n\
#!/usr/bin/env python3\n\
"""\n\
$PROJECT_NAME - Main Entry Point\n\
"""\n\
\n\
def main():\n\
    print("Hello from $PROJECT_NAME!")\n\
\n\
if __name__ == "__main__":\n\
    main()\n\
EOF\n\
\n\
# Create test file\n\
cat > tests/test_main.py << EOF\n\
#!/usr/bin/env python3\n\
"""\n\
Tests for $PROJECT_NAME\n\
"""\n\
\n\
import pytest\n\
import sys\n\
import os\n\
\n\
# Add src to path\n\
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))\n\
\n\
def test_import():\n\
    """Test that the module can be imported"""\n\
    import main\n\
    assert main is not None\n\
\n\
def test_main_function():\n\
    """Test the main function"""\n\
    import main\n\
    # Add your tests here\n\
    assert True\n\
EOF\n\
\n\
echo "Project $PROJECT_NAME created successfully!"\n\
echo "Location: $PROJECT_DIR"\n\
echo "Next steps:"\n\
echo "1. cd $PROJECT_DIR"\n\
echo "2. Edit src/main.py"\n\
echo "3. Add dependencies to requirements.txt"\n\
echo "4. Write tests in tests/"\n\
' > /workspace/tools/create_project && chmod +x /workspace/tools/create_project

# Create a grading script
RUN echo '#!/bin/bash\n\
# Grading script for assignments\n\
if [ $# -eq 0 ]; then\n\
    echo "Usage: grade_assignment <assignment_file.py>"\n\
    echo "Example: grade_assignment student_submission.py"\n\
    exit 1\n\
fi\n\
\n\
ASSIGNMENT_FILE=$1\n\
\n\
if [ ! -f "$ASSIGNMENT_FILE" ]; then\n\
    echo "Error: File $ASSIGNMENT_FILE not found!"\n\
    exit 1\n\
fi\n\
\n\
echo "Grading assignment: $ASSIGNMENT_FILE"\n\
cd /workspace/assignments/csp-scheduling-project/\n\
python grader.py "$ASSIGNMENT_FILE"\n\
' > /workspace/tools/grade_assignment && chmod +x /workspace/tools/grade_assignment

# Create a run assignment script
RUN echo '#!/bin/bash\n\
# Run assignment script\n\
if [ $# -eq 0 ]; then\n\
    echo "Usage: run_assignment <assignment_name>"\n\
    echo "Available assignments:"\n\
    echo "  csp-scheduling-project"\n\
    echo "Example: run_assignment csp-scheduling-project"\n\
    exit 1\n\
fi\n\
\n\
ASSIGNMENT_NAME=$1\n\
ASSIGNMENT_DIR="/workspace/assignments/$ASSIGNMENT_NAME"\n\
\n\
if [ ! -d "$ASSIGNMENT_DIR" ]; then\n\
    echo "Error: Assignment $ASSIGNMENT_NAME not found!"\n\
    echo "Available assignments:"\n\
    ls -1 /workspace/assignments/\n\
    exit 1\n\
fi\n\
\n\
cd "$ASSIGNMENT_DIR"\n\
echo "Running assignment: $ASSIGNMENT_NAME"\n\
echo "Directory: $ASSIGNMENT_DIR"\n\
echo ""\n\
\n\
case $ASSIGNMENT_NAME in\n\
    "csp-scheduling-project")\n\
        echo "CSP Scheduling Project Options:"\n\
        echo "1. Run main assignment: python src/csp_scheduling_project.py"\n\
        echo "2. Run tests: python test_project.py"\n\
        echo "3. Run GUI: python gui/scheduler_gui.py"\n\
        echo "4. Run grader: python grader.py <student_file>"\n\
        echo ""\n\
        echo "Choose an option (1-4) or press Enter to run main assignment:"\n\
        read -r choice\n\
        case $choice in\n\
            1|"")\n\
                python src/csp_scheduling_project.py\n\
                ;;\n\
            2)\n\
                python test_project.py\n\
                ;;\n\
            3)\n\
                python gui/scheduler_gui.py\n\
                ;;\n\
            4)\n\
                echo "Enter student file path:"\n\
                read -r student_file\n\
                python grader.py "$student_file"\n\
                ;;\n\
            *)\n\
                echo "Invalid choice. Running main assignment..."\n\
                python src/csp_scheduling_project.py\n\
                ;;\n\
        esac\n\
        ;;\n\
    *)\n\
        echo "Running default command for $ASSIGNMENT_NAME..."\n\
        if [ -f "main.py" ]; then\n\
            python main.py\n\
        elif [ -f "run.py" ]; then\n\
            python run.py\n\
        else\n\
            echo "No main.py or run.py found. Please specify how to run this assignment."\n\
        fi\n\
        ;;\nesac\n\
' > /workspace/tools/run_assignment && chmod +x /workspace/tools/run_assignment

# Set default command
CMD ["/workspace/welcome.sh"] 