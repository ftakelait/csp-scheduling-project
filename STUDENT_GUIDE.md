# 🎓 Student Guide - AI Course Development Environment

## 🚀 Quick Start (5 minutes)

### Step 1: Install Docker
- **Windows/Mac**: Download and install [Docker Desktop](https://docs.docker.com/desktop/)
- **Linux**: Install [Docker Engine](https://docs.docker.com/engine/install/) + [Docker Compose](https://docs.docker.com/compose/install/)

### Step 2: Download Course Files
```bash
git clone https://github.com/ftakelait/csp-scheduling-project.git
cd csp-scheduling-project
```

### Step 3: Setup Environment
```bash
# Make setup script executable (Linux/Mac only)
chmod +x setup-student.sh

# Run setup
./setup-student.sh
```

### Step 4: Start Working
```bash
# Start the development environment
docker-compose up ai-course-dev
```

## 🎯 What You'll See

After starting the environment, you'll see:

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
```

## 📝 Working on Assignments

### CSP Scheduling Project
```bash
# Navigate to the assignment
cd /workspace/assignments/csp-scheduling-project/

# Run the main assignment
python src/csp_scheduling_project.py

# Test your code
python test_project.py

# Run the GUI
python gui/scheduler_gui.py
```

### Your Work is Automatically Saved
- All your work is saved in `~/ai-course-work/` on your computer
- You can access it even when Docker is not running
- Your work persists between Docker sessions

## 🛠️ Useful Commands

```bash
# List all available assignments
list_assignments

# Run a specific assignment
run_assignment csp-scheduling-project

# Create a new project
create_project my-awesome-project

# Start Jupyter Notebook
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

## 📁 Your Files

Your work is saved in these folders on your computer:

- `~/ai-course-work/` - Your assignment work
- `~/ai-course-projects/` - Your own projects
- `~/ai-course-output/` - Generated files (charts, reports)
- `~/ai-course-data/` - Data files
- `~/ai-course-submissions/` - Assignment submissions
- `~/ai-course-grading/` - Grading results

## 🔧 Common Tasks

### Start Development Environment
```bash
docker-compose up ai-course-dev
```

### Stop Environment
```bash
# Press Ctrl+C in the terminal
# Or in another terminal:
docker-compose down
```

### Update Course Materials
```bash
# Get latest changes from GitHub
docker-compose build --no-cache
```

### Access Jupyter Notebook
```bash
# Start Jupyter service
docker-compose up jupyter

# Open in browser: http://localhost:8889
```

## 🐛 Troubleshooting

### "Docker not found"
- Install Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Make sure Docker is running

### "Permission denied"
```bash
chmod +x setup-student.sh
```

### "Port already in use"
- Close other applications using ports 8888, 8000, or 5000
- Or change ports in docker-compose.yml

### "Out of disk space"
```bash
docker system prune -a
```

## 📞 Getting Help

1. Check this guide first
2. Look at the troubleshooting section
3. Check the course repository: https://github.com/ftakelait/csp-scheduling-project/
4. Contact your instructor

## 🎉 You're Ready!

- ✅ Docker environment is set up
- ✅ Course materials are available
- ✅ Your work is automatically saved
- ✅ You can work on any OS (Windows, Mac, Linux)

**Happy coding! 🚀** 