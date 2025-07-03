# 🎯 CSP Scheduling Problem Solver

**Programming Project Assignment: CSCI 384 AI - Advanced Level**

This project implements a **Constraint Satisfaction Problem (CSP)** solver for complex scheduling scenarios, featuring a desktop GUI application and advanced algorithmic implementations. Students will build a comprehensive scheduling system that can handle multiple constraints, resources, and optimization goals.

**Difficulty Level: 9/10** ⭐⭐⭐⭐⭐⭐⭐⭐⭐

---

## 🎓 What You'll Practice

- **Constraint Satisfaction Problem (CSP)** formulation and solving
- **Backtracking algorithms** with various heuristics (MRV, Degree, LCV)
- **Arc consistency** and constraint propagation
- **Desktop GUI development** using PySide6
- **Advanced data structures** and algorithmic optimization
- **Real-world problem modeling** and constraint representation
- **Performance analysis** and algorithm comparison

---

## 📁 Project Structure

| Folder / File                    | Description                                           |
| -------------------------------- | ----------------------------------------------------- |
| `data/`                         | Sample scheduling datasets and test cases             |
| `data/sample_schedule.json`     | Sample scheduling problem with constraints            |
| `data/constraints.json`         | Constraint definitions and rules                      |
| `src/csp_scheduling_project.py` | Main assignment script to complete                    |
| `src/csp_solver.py`             | Core CSP solver implementation                        |
| `src/scheduler.py`              | Scheduling problem formulation                        |
| `utils/`                        | Helper modules and utilities                          |
| `utils/constraint_utils.py`     | Constraint validation and checking functions          |
| `utils/visualization.py`        | Data visualization and plotting utilities             |
| `utils/file_utils.py`           | File I/O and data loading functions                   |
| `gui/`                          | Desktop application components                        |
| `gui/scheduler_gui.py`          | Main GUI application (complete this)                  |
| `gui/components.py`             | Reusable GUI components                               |
| `report/`                       | Documentation and report templates                    |
| `report/report_template.docx`   | Report template to complete and submit               |

---

## 🚀 Getting Started

1. **Navigate** to the project directory in your Docker environment
2. **Open** `src/csp_scheduling_project.py` and complete the marked sections
3. **Implement** the GUI components in `gui/scheduler_gui.py`
4. **Run** the main script: `python src/csp_scheduling_project.py`
5. **Test** the GUI application: `python gui/scheduler_gui.py`

---

## 📦 Dependencies

Install required packages:

```bash
pip install pandas numpy matplotlib PySide6 pillow
```

---

## 🎯 Assignment Overview

### **Part 1: Core CSP Implementation (40 points)**
- Implement backtracking search with heuristics
- Add arc consistency and constraint propagation
- Build constraint satisfaction framework

### **Part 2: Scheduling Problem Formulation (30 points)**
- Model real-world scheduling constraints
- Implement resource allocation logic
- Create flexible constraint definitions

### **Part 3: Desktop GUI Application (20 points)**
- Build interactive scheduling interface
- Implement real-time constraint checking
- Create visualization components

### **Part 4: Analysis & Questions (10 points)**
- Algorithm performance analysis
- Constraint satisfaction theory questions
- Optimization strategy evaluation

---

## ✅ Submission Requirements

### **File Naming Convention:**
- **Python Script:** `CSP-Scheduling-YourName1_YourName2_YourName3.py`
- **GUI Application:** `CSP-GUI-YourName1_YourName2_YourName3.py`
- **Report:** `CSP-Report-YourName1_YourName2_YourName3.pdf`

### **What to Submit:**
1. **Completed Python scripts** with all sections implemented
2. **Working GUI application** with full functionality
3. **Written report** with analysis and answers to questions
4. **Performance analysis** and algorithm comparison

### **Submission Format:**
- Zip all files as: `CSP-Scheduling-YourName1_YourName2_YourName3.zip`
- Include only your completed files (not data or utility files)

---

## 🎨 GUI Features to Implement

- **Interactive constraint definition**
- **Real-time schedule visualization**
- **Constraint violation highlighting**
- **Solution export functionality**
- **Performance metrics display**

---

## 🔧 Advanced Features (Bonus Points)

- **Multiple heuristic implementations**
- **Performance comparison tools**
- **Constraint relaxation options**
- **Solution optimization algorithms**
- **Export to various formats**

---

## 📚 Learning Resources

- **CSP Theory:** Russell & Norvig, "Artificial Intelligence: A Modern Approach"
- **Backtracking:** Chapter 6 - Constraint Satisfaction Problems
- **GUI Development:** PySide6 documentation
- **Algorithm Analysis:** Big-O notation and performance metrics

---

## ⚠️ Important Notes

- **Start early** - This is a complex project requiring significant time
- **Test incrementally** - Build and test each component separately
- **Document your code** - Clear comments and explanations required
- **Optimize performance** - Consider algorithm efficiency in your implementation
- **Handle edge cases** - Robust error handling expected

---

## 🎯 Success Criteria

- **Complete CSP solver** with all required algorithms
- **Functional GUI application** with intuitive interface
- **Correct constraint handling** for all test cases
- **Performance analysis** with meaningful insights
- **Clean, well-documented code** following best practices

**Good luck with your CSP scheduling project! 🚀**
