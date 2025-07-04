# Student Guide: AI Course Development Environment

## Quick Start (5 minutes)

### 1. Prerequisites
- **Docker Desktop** installed on your computer
  - Windows/Mac: Download from [Docker Desktop](https://docs.docker.com/desktop/)
  - Linux: Follow [Docker Engine installation](https://docs.docker.com/engine/install/)

### 2. Setup (One-time)
1. Download the Docker files from your instructor:
   - `Dockerfile`
   - `docker-compose.yml`
   - `setup.sh`
   - `STUDENT_GUIDE.md` (this file)

2. Open terminal/command prompt in the folder with these files

3. Run the setup script:
   ```bash
   # On Windows (PowerShell):
   .\setup.sh
   
   # On Mac/Linux:
   chmod +x setup.sh
   ./setup.sh
   ```

4. Wait for the setup to complete (downloads course repository and builds environment)

### 3. Start Working

**Recommended method (works on all platforms):**
```bash
# Simple and reliable - works on Windows, Mac, and Linux
docker run -it --rm \
  -v ~/ai-course-work:/workspace/student_work \
  -v ~/ai-course-data:/workspace/data \
  -v ~/ai-course-output:/workspace/output \
  -v ~/ai-course-projects:/workspace/projects \
  mycourse-ai-course-dev
```

**Alternative methods:**
```bash
# Method 1: Use the provided start script
chmod +x start-dev.sh
./start-dev.sh

# Method 2: Docker Compose (may have issues on Windows)
docker-compose up ai-course-dev

# Method 3: Detached mode
docker-compose up -d ai-course-dev
docker-compose exec ai-course-dev /bin/bash

# Method 4: Start Jupyter Notebook
docker-compose up jupyter
```

**What happens when you run `docker-compose up ai-course-dev`:**

1. **Container starts** and shows "Setting up git configuration..."
2. **Welcome message appears** with available assignments and commands
3. **Interactive bash shell starts** - you'll see a prompt like: `student@ai-course:/workspace$`
4. **You're now inside the container** and can start working!

**Example of what you'll see:**
```
===============================================
Welcome to the AI Course Development Environment
===============================================

Course Repository: https://github.com/ftakelait/csp-scheduling-project/

Available assignments and projects:
1. CSP Scheduling Project: /workspace/assignments/csp-scheduling-project/
2. Your projects: /workspace/projects/
3. Your work: /workspace/student_work/
4. Tools: /workspace/tools/

Quick start commands:
- cd /workspace/assignments/csp-scheduling-project/
- python src/csp_scheduling_project.py
- python test_project.py
- python gui/scheduler_gui.py

Current directory: /workspace
===============================================

student@ai-course:/workspace$
```

### 4. Start Working on Assignments

Once you see the `student@ai-course:/workspace$` prompt, you're ready to work! Here are your first steps:

```bash
# Navigate to the CSP assignment
cd /workspace/assignments/csp-scheduling-project/

# List what's available
ls -la

# Run the main assignment
python src/csp_scheduling_project.py

# Or run tests
python test_project.py

# Or start the GUI
python gui/scheduler_gui.py
```

**Your work is automatically saved** in `~/ai-course-work/` on your computer!

## What's Included

The Docker environment automatically includes:
- **Course Repository**: https://github.com/ftakelait/csp-scheduling-project/
- **CSP Scheduling Project**: Complete assignment with GUI, tests, and grader
- **Python 3.11** with all necessary packages
- **Development Tools**: Jupyter, pytest, git, vim, nano
- **Persistent Storage**: Your work is saved in your home directory

## Your Work Directories

All your work is automatically saved in your home directory:
- `~/ai-course-work/` - Your assignment work
- `~/ai-course-projects/` - Your own projects
- `~/ai-course-data/` - Data files
- `~/ai-course-output/` - Generated files
- `~/ai-course-submissions/` - Assignment submissions
- `~/ai-course-grading/` - Grading results

## Working with Assignments

### CSP Scheduling Project
```bash
# Run the main assignment
docker-compose run --rm ai-course-dev run_assignment csp-scheduling-project

# Or start the development environment and work interactively
docker-compose up ai-course-dev
```

### Inside the Container
Once inside the container, you can:
```bash
# Navigate to the assignment
cd /workspace/assignments/csp-scheduling-project/

# Run the main program
python src/csp_scheduling_project.py

# Run tests
python test_project.py

# Start the GUI
python gui/scheduler_gui.py

# Run the grader on your work
python grader.py /workspace/student_work/my_solution.py
```

### Creating Your Own Projects
```bash
# Create a new project
docker-compose run --rm ai-course-dev create_project my_awesome_project

# Work on your project
cd ~/ai-course-projects/my_awesome_project/
```

## Jupyter Notebook

For interactive development:
```bash
# Start Jupyter
docker-compose up jupyter

# Open in browser: http://localhost:8889
```

## Useful Commands

### Container Management
```bash
# Start development environment
docker-compose up ai-course-dev

# Start Jupyter
docker-compose up jupyter

# Stop all containers
docker-compose down

# View running containers
docker-compose ps

# View logs
docker-compose logs
```

### Assignment Commands
```bash
# List all assignments
docker-compose run --rm ai-course-dev list_assignments

# Run specific assignment
docker-compose run --rm ai-course-dev run_assignment csp-scheduling-project

# Grade your submission
docker-compose run --rm ai-course-dev grade_assignment /workspace/student_work/my_file.py
```

### Development Commands
```bash
# Create new project
docker-compose run --rm ai-course-dev create_project project_name

# Start interactive shell
docker-compose run --rm ai-course-dev /bin/bash
```

## Troubleshooting

### Container Not Starting Properly
If you see "Setting up git configuration..." and then nothing happens:
```bash
# Stop the container
docker-compose down

# Rebuild and start
docker-compose build --no-cache
docker-compose up ai-course-dev
```

### No Interactive Prompt
If you see the welcome message but no `student@ai-course:/workspace$` prompt:
```bash
# Method 1: Use docker run (recommended for Windows)
docker run -it --rm \
  -v ~/ai-course-work:/workspace/student_work \
  -v ~/ai-course-data:/workspace/data \
  -v ~/ai-course-output:/workspace/output \
  -v ~/ai-course-projects:/workspace/projects \
  mycourse-ai-course-dev

# Method 2: Use detached mode
docker-compose up -d ai-course-dev
docker-compose exec ai-course-dev /bin/bash
```

### Docker Issues
```bash
# If containers won't start
docker-compose down
docker system prune -f
docker-compose up ai-course-dev

# If image is corrupted
docker-compose down
docker rmi ai-course-dev_ai-course-dev
docker-compose build
```

### Permission Issues (Linux/Mac)
```bash
# Fix file permissions
sudo chown -R $USER:$USER ~/ai-course-*
```

### Windows Issues
- Make sure Docker Desktop is running
- Use PowerShell or WSL for better compatibility
- If paths have spaces, use quotes: `"C:\Users\Your Name\ai-course-work"`

## Getting Help

1. **Check the logs**: `docker-compose logs`
2. **Restart containers**: `docker-compose down && docker-compose up ai-course-dev`
3. **Rebuild if needed**: `docker-compose build --no-cache`
4. **Ask your instructor** with the error message

## Course Repository

The environment automatically includes the course repository:
- **GitHub**: https://github.com/ftakelait/csp-scheduling-project/
- **Location in container**: `/workspace/assignments/csp-scheduling-project/`

## Next Steps

1. **Complete the CSP assignment** in `/workspace/assignments/csp-scheduling-project/`
2. **Create your own projects** using `create_project`
3. **Use Jupyter** for interactive development
4. **Submit your work** to the `~/ai-course-submissions/` directory

Happy coding! 🚀 