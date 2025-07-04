# Instructor Guide: Sharing Docker Environment with Students

## Overview

This setup allows you to share only the Docker files with students, who can then run the complete course environment from anywhere without needing the full project repository.

## What Students Need

Share these 5 files with your students:
- `Dockerfile` - Builds the complete environment
- `docker-compose.yml` - Orchestrates the services
- `setup.sh` - One-time setup script
- `start-simple.sh` - Simple startup script (recommended)
- `STUDENT_GUIDE.md` - Complete instructions for students

## How It Works

1. **Standalone Setup**: Students only need the Docker files, not the full project
2. **Automatic Repository**: The Dockerfile clones your GitHub repository during build
3. **Persistent Storage**: Student work is saved in their home directories
4. **Cross-Platform**: Works on Windows, Mac, and Linux

## Repository Configuration

The Dockerfile automatically clones from:
```dockerfile
RUN git clone https://github.com/ftakelait/csp-scheduling-project.git /workspace/course-repo
```

**To change the repository URL:**
1. Update the URL in `Dockerfile` (line with `git clone`)
2. Update the URL in `STUDENT_GUIDE.md`
3. Share the updated files with students

## Student Workflow

1. Students download the 4 Docker files
2. Run `./setup.sh` (one-time setup)
3. Use `docker-compose up ai-course-dev` to start working
4. All work is saved in `~/ai-course-work/` on their computer

## Advantages

### For Students
- ✅ No need to clone repositories
- ✅ No need to install Python packages
- ✅ Works on any OS
- ✅ Consistent environment
- ✅ Persistent work storage

### For Instructors
- ✅ Easy to distribute (just 4 files)
- ✅ Centralized updates via GitHub
- ✅ No environment setup issues
- ✅ Easy grading with grader container

## Updating Course Materials

### Method 1: GitHub Updates (Recommended)
1. Update your GitHub repository
2. Students rebuild: `docker-compose build --no-cache`
3. New materials are automatically available

### Method 2: New Docker Files
1. Update the Dockerfile with new assignments
2. Share new Docker files with students
3. Students run `./setup.sh` again

## Grading Student Submissions

Students can submit work in `~/ai-course-submissions/`:

```bash
# Grade a submission
docker-compose run --rm grader grade_assignment /workspace/student_submissions/student_file.py

# View grading reports
ls ~/ai-course-grading/
```

## File Structure in Container

```
/workspace/
├── course-repo/                    # Your GitHub repository
├── assignments/
│   └── csp-scheduling-project/     # Current assignment
├── projects/                       # Student projects
├── student_work/                   # Student assignment work
├── data/                          # Data files
├── output/                        # Generated files
└── tools/                         # Helper scripts
```

## Student Directories (on their computer)

```
~/ai-course-work/          # Assignment work
~/ai-course-projects/      # Student projects
~/ai-course-data/          # Data files
~/ai-course-output/        # Generated files
~/ai-course-submissions/   # Assignment submissions
~/ai-course-grading/       # Grading results
```

## Adding New Assignments

### Option 1: Add to GitHub Repository
1. Add new assignment to your GitHub repository
2. Students rebuild: `docker-compose build --no-cache`
3. New assignment appears in `/workspace/assignments/`

### Option 2: Modify Dockerfile
1. Add new assignment files to Dockerfile
2. Update `run_assignment` script in Dockerfile
3. Share updated Docker files with students

## Troubleshooting

### Common Student Issues
- **Docker not installed**: Direct to Docker Desktop installation
- **Permission errors**: Check file permissions on setup.sh
- **Port conflicts**: Change ports in docker-compose.yml
- **Build failures**: Check internet connection and GitHub access

### Instructor Commands
```bash
# Test the setup locally
./setup.sh
docker-compose up ai-course-dev

# Update course materials
git push origin main  # Updates GitHub repository

# Grade submissions
docker-compose run --rm grader /bin/bash
```

## Security Considerations

- Students have full access to the container
- No sensitive data should be in the Docker image
- Consider using private repositories for sensitive materials
- Students can access the internet from within containers

## Performance Tips

- Students should have at least 4GB RAM for Docker
- SSD storage recommended for faster builds
- Consider using Docker volumes for large datasets
- Students can use `docker system prune` to free space

## Support

### For Students
- Direct them to `STUDENT_GUIDE.md`
- Check `docker-compose logs` for errors
- Ensure Docker Desktop is running

### For Instructors
- Monitor GitHub repository for issues
- Update Docker files as needed
- Provide alternative setup if Docker fails

## Example Distribution

Create a zip file with:
```
docker-setup/
├── Dockerfile
├── docker-compose.yml
├── setup.sh
└── STUDENT_GUIDE.md
```

Students extract and run `./setup.sh` - that's it!

## Next Steps

1. **Test the setup** on a clean machine
2. **Share the 4 files** with your students
3. **Monitor student progress** through submissions
4. **Update materials** via GitHub as needed

The setup is designed to be as simple as possible for students while giving you full control over the course environment. 