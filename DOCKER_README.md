# 🐳 AI Course Development Environment

This Docker setup provides a consistent development environment for all students, regardless of their operating system. The course repository is automatically cloned inside the container, so students can run it from anywhere on their system.

## 🚀 Quick Start for Students

### Prerequisites
- [Docker Desktop](https://docs.docker.com/desktop/) (Windows/Mac)
- [Docker Engine](https://docs.docker.com/engine/install/) + [Docker Compose](https://docs.docker.com/compose/install/) (Linux)

### Setup (One-time)
```bash
# 1. Download the course files from GitHub
git clone https://github.com/ftakelait/csp-scheduling-project.git
cd csp-scheduling-project

# 2. Make setup script executable (Linux/Mac only)
chmod +x setup-student.sh

# 3. Run setup script
./setup-student.sh
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
Student's Home Directory:
├── ai-course-work/           # Your assignment work (persistent)
├── ai-course-data/           # Data files (persistent)
├── ai-course-output/         # Generated files (persistent)
├── ai-course-projects/       # Your projects (persistent)
├── ai-course-submissions/    # Assignment submissions (persistent)
└── ai-course-grading/        # Grading results (persistent)

Inside Docker Container:
├── /workspace/
│   ├── course-repo/          # Cloned from GitHub
│   ├── assignments/          # All course assignments
│   │   └── csp-scheduling-project/
│   ├── student_work/         # Your work (mounted from ~/ai-course-work)
│   ├── projects/             # Your projects (mounted from ~/ai-course-projects)
│   ├── data/                 # Data files (mounted from ~/ai-course-data)
│   ├── output/               # Generated files (mounted from ~/ai-course-output)
│   └── tools/                # Development tools
```

## 🛠️ Available Services

### 1. Development Environment (`ai-course-dev`)
Main development container with all tools and course repository.

```bash
# Start development environment
docker-compose up ai-course-dev

# Access the container
docker-compose exec ai-course-dev bash
```

**Features:**
- Python 3.11 with all dependencies
- Course repository automatically cloned
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
# List all available assignments
docker-compose run --rm ai-course-dev list_assignments

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
All changes in mounted volumes are automatically saved to your host machine in the `~/ai-course-work/` directory.

## 📝 Creating New Projects

```bash
# Create a new project
docker-compose run --rm ai-course-dev create_project my-ai-project

# The project will be created in /workspace/projects/my-ai-project/
# and accessible from ~/ai-course-projects/my-ai-project/ on your host
```

## 🎓 For Instructors

### Grading Submissions

1. **Place student submissions** in `~/ai-course-submissions/` directory
2. **Run the grader:**
   ```bash
   docker-compose run --rm grader grade_assignment /workspace/student_submissions/student_file.py
   ```
3. **Find results** in `~/ai-course-grading/` directory

### Adding New Assignments

1. **Add new assignments** to the GitHub repository: https://github.com/ftakelait/csp-scheduling-project/
2. **Students will automatically get updates** when they rebuild the Docker image
3. **Update run_assignment script** in Dockerfile to handle new assignments

### Batch Grading

```bash
# Grade multiple submissions
for file in ~/ai-course-submissions/*.py; do
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
chmod +x setup-student.sh
sudo chown -R $USER:$USER ~/ai-course-*
```

**3. Docker daemon not running**
- Windows/Mac: Start Docker Desktop
- Linux: `sudo systemctl start docker`

**4. Out of disk space**
```bash
# Clean up Docker
docker system prune -a
```

**5. Course repository not found**
```bash
# Rebuild the image to re-clone the repository
docker-compose build --no-cache
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
docker cp ai-course-development:/workspace/output/ ~/ai-course-output/
```

## 🔄 Updating the Environment

### Update Course Repository
```bash
# Rebuild the image to get latest changes from GitHub
docker-compose build --no-cache
```

### Update Dependencies
```bash
# Update requirements.txt in the GitHub repository
# Students will get updates when they rebuild
docker-compose build --no-cache
```

## 📚 Learning Resources

- [Course Repository](https://github.com/ftakelait/csp-scheduling-project/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Python in Docker](https://docs.docker.com/language/python/)

## 🤝 Contributing

To add new assignments or improve the environment:

1. **Update the GitHub repository**: https://github.com/ftakelait/csp-scheduling-project/
2. **Update Dockerfile** with new tools/dependencies
3. **Update docker-compose.yml** with new services
4. **Update run_assignment script** for new assignments
5. **Test the setup** on different OS platforms
6. **Update this README**

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section
2. Look at Docker logs: `docker-compose logs`
3. Try rebuilding: `docker-compose build --no-cache`
4. Check the course repository for updates
5. Contact your instructor with error messages

---

**Happy coding! 🚀** 