# 🐳 AI Course Development Environment

This Docker setup provides a consistent development environment for all students, regardless of their operating system. It includes all necessary tools, dependencies, and project templates.

## 🚀 Quick Start

### Prerequisites
- [Docker Desktop](https://docs.docker.com/desktop/) (Windows/Mac)
- [Docker Engine](https://docs.docker.com/engine/install/) + [Docker Compose](https://docs.docker.com/compose/install/) (Linux)

### Setup (One-time)
```bash
# Make setup script executable (Linux/Mac only)
chmod +x setup.sh

# Run setup script
./setup.sh
```

### Start Development Environment
```bash
# Start the main development environment
docker-compose up ai-course-dev

# Or start in background
docker-compose up -d ai-course-dev
```

## 📁 Directory Structure

```
csp-scheduling-project/
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Multi-service configuration
├── setup.sh                   # Setup script
├── requirements.txt           # Python dependencies
├── student_data/              # Student data files (persistent)
├── output/                    # Generated files (persistent)
├── student_projects/          # Student projects (persistent)
├── student_submissions/       # Assignment submissions (persistent)
├── grading_reports/           # Grading results (persistent)
└── [project files...]
```

## 🛠️ Available Services

### 1. Development Environment (`ai-course-dev`)
Main development container with all tools.

```bash
# Start development environment
docker-compose up ai-course-dev

# Access the container
docker-compose exec ai-course-dev bash
```

**Features:**
- Python 3.11 with all dependencies
- Development tools (git, vim, nano, tree, htop)
- Code quality tools (black, flake8, mypy)
- Jupyter Notebook support
- Custom bash prompt

### 2. Jupyter Notebook (`jupyter`)
Dedicated Jupyter service for notebook development.

```bash
# Start Jupyter service
docker-compose up jupyter

# Access at: http://localhost:8889
```

### 3. Grading Service (`grader`)
Dedicated container for grading assignments.

```bash
# Grade a student submission
docker-compose run --rm grader grade_assignment /workspace/student_submissions/student_file.py
```

## 🎯 Working with Assignments

### CSP Scheduling Project

```bash
# Run the main assignment
docker-compose run --rm ai-course-dev run_assignment csp-scheduling-project

# Or manually:
docker-compose run --rm ai-course-dev bash
cd /workspace/assignments/csp-scheduling-project/
python src/csp_scheduling_project.py
```

### Available Commands

```bash
# List available assignments
docker-compose run --rm ai-course-dev run_assignment

# Run specific assignment
docker-compose run --rm ai-course-dev run_assignment csp-scheduling-project

# Create new project
docker-compose run --rm ai-course-dev create_project my-new-project

# Grade assignment
docker-compose run --rm grader grade_assignment /workspace/student_submissions/student_file.py
```

## 📊 Ports and Access

| Service | Port | URL | Description |
|---------|------|-----|-------------|
| Jupyter | 8889 | http://localhost:8889 | Jupyter Notebook |
| HTTP Server | 8000 | http://localhost:8000 | File server |
| Web Apps | 5000 | http://localhost:5000 | Flask/Web applications |

## 🔧 Development Workflow

### 1. Start Environment
```bash
docker-compose up ai-course-dev
```

### 2. Work on Assignment
```bash
# Inside container or via run command
cd /workspace/assignments/csp-scheduling-project/
python src/csp_scheduling_project.py
```

### 3. Test Your Code
```bash
python test_project.py
```

### 4. Run GUI (if applicable)
```bash
python gui/scheduler_gui.py
```

### 5. Save Your Work
All changes in mounted volumes are automatically saved to your host machine.

## 📝 Creating New Projects

```bash
# Create a new project
docker-compose run --rm ai-course-dev create_project my-ai-project

# The project will be created in /workspace/projects/my-ai-project/
# and accessible from ./student_projects/my-ai-project/ on your host
```

## 🎓 For Instructors

### Grading Submissions

1. **Place student submissions** in `student_submissions/` directory
2. **Run the grader:**
   ```bash
   docker-compose run --rm grader grade_assignment /workspace/student_submissions/student_file.py
   ```
3. **Find results** in `grading_reports/` directory

### Adding New Assignments

1. **Create assignment directory** in the project
2. **Update docker-compose.yml** to mount the new assignment
3. **Update run_assignment script** in Dockerfile to handle the new assignment

### Batch Grading

```bash
# Grade multiple submissions
for file in student_submissions/*.py; do
    docker-compose run --rm grader grade_assignment "/workspace/student_submissions/$(basename $file)"
done
```

## 🐛 Troubleshooting

### Common Issues

**1. Port already in use**
```bash
# Check what's using the port
lsof -i :8888

# Use different ports in docker-compose.yml
```

**2. Permission denied**
```bash
# On Linux/Mac, fix permissions
chmod +x setup.sh
sudo chown -R $USER:$USER student_data output student_projects
```

**3. Docker daemon not running**
- Windows/Mac: Start Docker Desktop
- Linux: `sudo systemctl start docker`

**4. Out of disk space**
```bash
# Clean up Docker
docker system prune -a
```

### Useful Commands

```bash
# Check running containers
docker-compose ps

# View logs
docker-compose logs ai-course-dev

# Stop all services
docker-compose down

# Rebuild image
docker-compose build --no-cache

# Access running container
docker-compose exec ai-course-dev bash

# Copy files from container
docker cp ai-course-development:/workspace/output/ ./local_output/
```

## 🔄 Updating the Environment

### Update Dependencies
```bash
# Update requirements.txt
# Rebuild the image
docker-compose build --no-cache
```

### Update Assignment Files
```bash
# Files are mounted, so changes are immediate
# No rebuild needed for assignment content
```

## 📚 Learning Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Python in Docker](https://docs.docker.com/language/python/)

## 🤝 Contributing

To add new assignments or improve the environment:

1. Update `Dockerfile` with new tools/dependencies
2. Update `docker-compose.yml` with new services
3. Update `run_assignment` script for new assignments
4. Test the setup on different OS platforms
5. Update this README

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section
2. Look at Docker logs: `docker-compose logs`
3. Try rebuilding: `docker-compose build --no-cache`
4. Contact your instructor with error messages

---

**Happy coding! 🚀** 