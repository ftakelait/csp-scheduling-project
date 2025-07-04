"""
CSP Scheduling Project - Main Assignment Script
University of North Dakota - CSCI 384 AI Course | Fall 2025

Title: Constraint Satisfaction Problem (CSP) Scheduling Solver
Total Points: 100 (+20 bonus points)

This is the main assignment script. You must complete each step where "YOUR CODE HERE" is indicated.
Use the provided helper modules (utils/ and src/csp_solver.py) to assist you.
The project implements a comprehensive CSP solver for real-world scheduling problems.

GRADING BREAKDOWN:
- Step 1: Data Loading and Validation (10 points)
- Step 2: CSP Formulation (15 points)  
- Step 3: Heuristic Implementation (15 points)
- Step 4: CSP Solving (20 points)
- Step 5: Solution Analysis (15 points)
- Step 6: Visualization (10 points)
- Step 7: Export Functionality (10 points)
- Conceptual Questions (15 points)
- Bonus Features (10 points)

TOTAL: 110 points
"""

import sys
import os
import time
import json
from typing import Dict, List, Any, Tuple, Optional

# Add the project root to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our utility modules
from utils.file_utils import load_schedule_data, validate_data_structure, export_schedule_to_json
from utils.constraint_utils import (
    check_resource_availability, check_task_dependencies, check_resource_skills,
    check_max_hours_per_day, check_preferred_resources, check_task_priority,
    check_balanced_workload, get_constraint_violations, calculate_schedule_score
)
from utils.visualization import (
    create_gantt_chart, create_resource_utilization_chart, 
    create_constraint_violation_chart, create_performance_comparison_chart,
    save_all_visualizations
)
from src.csp_solver import CSPSolver, CSPVariable, CSPConstraint, SchedulingCSP

# ---------------------------------------------------------------
# STEP 1 [10 pts]: DATA LOADING AND VALIDATION
# ---------------------------------------------------------------
# Load the scheduling problem data from the data directory.
# Validate that the data structure is correct before proceeding.

print("=" * 60)
print("STEP 1: DATA LOADING AND VALIDATION")
print("=" * 60)

# YOUR CODE HERE (5 points)
# Load the scheduling data using the provided utility function
# Store the result in a variable called 'data'

data = None  # Replace with your code

# YOUR CODE HERE (5 points)
# Validate that the data has the correct structure
# Check that it contains a 'schedule' key with required sub-keys:
# - 'tasks': list of task dictionaries
# - 'resources': list of resource dictionaries  
# - 'time_slots': dictionary with time slot information
# - 'constraints': dictionary with hard and soft constraints
# If validation fails, raise a ValueError with a descriptive message

is_valid = None  # Replace with your code

if not is_valid:
    print("❌ Data validation failed. Please check the data files.")
    sys.exit(1)
else:
    print("✅ Data validation successful!")

# Extract the main components from the loaded data
schedule_data = data['schedule']
constraints_data = data['constraints']

tasks = schedule_data['tasks']
resources = schedule_data['resources']
time_slots = schedule_data['time_slots']
constraints = schedule_data['constraints']

# Display basic information about the problem
print(f"📊 Problem Overview:")
print(f"   - Number of tasks: {len(tasks)}")
print(f"   - Number of resources: {len(resources)}")
print(f"   - Time slots: {len(time_slots['days'])} days, {len(time_slots['hours'])} hours per day")
print(f"   - Hard constraints: {len(constraints['hard_constraints'])}")
print(f"   - Soft constraints: {len(constraints['soft_constraints'])}")

# ---------------------------------------------------------------
# STEP 2 [15 pts]: CSP FORMULATION
# ---------------------------------------------------------------
# Formulate the scheduling problem as a CSP by defining variables, domains, and constraints.

print("\n" + "=" * 60)
print("STEP 2: CSP FORMULATION")
print("=" * 60)

# YOUR CODE HERE (15 points)
# Create a SchedulingCSP object using the loaded data
# The CSP should be initialized with:
# - tasks: schedule['tasks']
# - resources: schedule['resources'] 
# - time_slots: schedule['time_slots']
# - constraints: schedule['constraints']
# Store the result in a variable called 'scheduling_csp'

scheduling_csp = None  # Replace with your code

# Verify CSP creation
if scheduling_csp is not None:
    print(f"✓ CSP created successfully")
    print(f"  - Variables: {len(scheduling_csp.variables)}")
    print(f"  - Domains: {len(scheduling_csp.domains)}")
    print(f"  - Constraints: {len(scheduling_csp.constraints)}")
else:
    print("✗ CSP creation failed")

# ---------------------------------------------------------------
# STEP 3 [15 pts]: HEURISTIC IMPLEMENTATION
# ---------------------------------------------------------------
# Implement the MRV (Minimum Remaining Values) and Degree heuristics for variable ordering.

print("\n" + "=" * 60)
print("STEP 3: HEURISTIC IMPLEMENTATION")
print("=" * 60)

# YOUR CODE HERE (5 points)
# Implement the Minimum Remaining Values (MRV) heuristic
# This function should select the variable with the fewest legal values remaining
# Parameters: variables (list), domains (dict), constraints (list)
# Returns: selected variable (string)
def mrv_heuristic(variables, domains, constraints):
    """
    Minimum Remaining Values (MRV) heuristic
    Selects the variable with the fewest legal values remaining
    """
    # YOUR CODE HERE
    pass

# YOUR CODE HERE (5 points)
# Implement the Degree heuristic
# This function should select the variable with the highest degree (most constraints)
# Parameters: variables (list), domains (dict), constraints (list)
# Returns: selected variable (string)
def degree_heuristic(variables, domains, constraints):
    """
    Degree heuristic
    Selects the variable with the highest degree (most constraints)
    """
    # YOUR CODE HERE
    pass

# YOUR CODE HERE (5 points)
# Implement the Combined heuristic
# This function should use MRV first, then degree for tiebreaking
# Parameters: variables (list), domains (dict), constraints (list)
# Returns: selected variable (string)
def combined_heuristic(variables, domains, constraints):
    """
    Combined heuristic (MRV + Degree tiebreaker)
    Uses MRV first, then degree for tiebreaking
    """
    # YOUR CODE HERE
    pass

print("✓ Heuristics implemented:")
print("  - MRV heuristic: Minimum Remaining Values")
print("  - Degree heuristic: Highest degree variable")
print("  - Combined heuristic: MRV with degree tiebreaker")

# ---------------------------------------------------------------
# STEP 4 [20 pts]: CSP SOLVING
# ---------------------------------------------------------------
# Solve the CSP using different heuristics and compare their performance.

print("\n" + "=" * 60)
print("STEP 4: CSP SOLVING")
print("=" * 60)

# YOUR CODE HERE (20 points)
# Solve the CSP using different heuristics and compare results
# Test each heuristic: 'mrv', 'degree', 'combined'
# Store solutions in a dictionary called 'solutions'
# Use a timeout of 60 seconds for each solve attempt

solutions = {}  # Replace with your code

# Print solving results
for heuristic, solution in solutions.items():
    if solution:
        print(f"✓ {heuristic.upper()} heuristic: {len(solution)} tasks scheduled")
    else:
        print(f"✗ {heuristic.upper()} heuristic: No solution found")

# Select the best solution (you can choose based on your criteria)
best_solution = solutions.get('mrv', {})  # Replace with your selection logic
print(f"\n✓ Best solution selected: {len(best_solution)} tasks scheduled")

# ---------------------------------------------------------------
# STEP 5 [15 pts]: SOLUTION ANALYSIS
# ---------------------------------------------------------------
# Analyze the solutions found and validate them against the constraints.

print("\n" + "=" * 60)
print("STEP 5: SOLUTION ANALYSIS")
print("=" * 60)

# YOUR CODE HERE (5 points)
# Implement constraint violation analysis
# This function should check for constraint violations in the solution
# Parameters: solution (dict), tasks (list), resources (list)
# Returns: dictionary of violations by task_id

def analyze_constraint_violations(solution, tasks, resources):
    """Analyze constraint violations in the solution"""
    # YOUR CODE HERE
    pass

# YOUR CODE HERE (5 points)
# Implement solution validation
# This function should validate the complete solution
# Parameters: solution (dict), tasks (list), resources (list), constraints (dict)
# Returns: (is_valid: bool, message: str)

def validate_solution(solution, tasks, resources, constraints):
    """Validate the complete solution"""
    # YOUR CODE HERE
    pass

# YOUR CODE HERE (5 points)
# Implement performance metrics calculation
# This function should calculate various performance metrics
# Parameters: solution (dict), tasks (list), resources (list)
# Returns: dictionary with metrics (schedule_score, total_hours, avg_utilization, tasks_scheduled)

def calculate_performance_metrics(solution, tasks, resources):
    """Calculate performance metrics for the solution"""
    # YOUR CODE HERE
    pass

# Analyze the solution
if best_solution:
    violations = analyze_constraint_violations(best_solution, schedule['tasks'], schedule['resources'])
    is_valid, validation_msg = validate_solution(best_solution, schedule['tasks'], schedule['resources'], schedule['constraints'])
    metrics = calculate_performance_metrics(best_solution, schedule['tasks'], schedule['resources'])
    
    print(f"✓ Solution analysis completed:")
    print(f"  - Valid solution: {is_valid}")
    print(f"  - Validation message: {validation_msg}")
    print(f"  - Constraint violations: {len(violations)}")
    print(f"  - Schedule score: {metrics.get('schedule_score', 0):.3f}")
    print(f"  - Average utilization: {metrics.get('avg_utilization', 0):.1%}")
else:
    print("✗ No solution to analyze")

# ---------------------------------------------------------------
# STEP 6 [10 pts]: VISUALIZATION
# ---------------------------------------------------------------
# Create visualizations of the schedule and resource utilization.

print("\n" + "=" * 60)
print("STEP 6: VISUALIZATION")
print("=" * 60)

# YOUR CODE HERE (5 points)
# Implement Gantt chart creation
# This function should create a Gantt chart visualization of the schedule
# Parameters: solution (dict), tasks (list), resources (list)
# Returns: matplotlib figure object

def create_gantt_chart(solution, tasks, resources):
    """Create a Gantt chart visualization"""
    # YOUR CODE HERE
    pass

# YOUR CODE HERE (5 points)
# Implement resource utilization chart
# This function should create a chart showing resource utilization
# Parameters: solution (dict), resources (list)
# Returns: matplotlib figure object

def create_resource_utilization_chart(solution, resources):
    """Create a resource utilization chart"""
    # YOUR CODE HERE
    pass

# Create visualizations
if best_solution:
    gantt_fig = create_gantt_chart(best_solution, schedule['tasks'], schedule['resources'])
    util_fig = create_resource_utilization_chart(best_solution, schedule['resources'])
    
    # Save charts
    os.makedirs('output', exist_ok=True)
    gantt_fig.savefig('output/gantt_chart.png', dpi=300, bbox_inches='tight')
    util_fig.savefig('output/resource_utilization.png', dpi=300, bbox_inches='tight')
    
    print("✓ Visualizations created:")
    print("  - Gantt chart: output/gantt_chart.png")
    print("  - Resource utilization: output/resource_utilization.png")
else:
    print("✗ No solution to visualize")

# ---------------------------------------------------------------
# STEP 7 [15 pts]: EXPORT FUNCTIONALITY
# ---------------------------------------------------------------
# Export the solution to JSON and CSV formats.

# YOUR CODE HERE (5 points)
# Implement JSON export function
# This function should export the solution to JSON format
# Parameters: solution (dict), filename (str)
# Use the provided export_schedule_to_json utility function

def export_solution_json(solution, filename):
    """Export solution to JSON format"""
    # YOUR CODE HERE
    pass

# YOUR CODE HERE (5 points)
# Implement CSV export function
# This function should export the solution to CSV format
# Parameters: solution (dict), filename (str)
# Use the provided export_schedule_to_csv utility function

def export_solution_csv(solution, filename):
    """Export solution to CSV format"""
    # YOUR CODE HERE
    pass

# Export the solution
if best_solution:
    export_solution_json(best_solution, 'output/solution.json')
    export_solution_csv(best_solution, 'output/solution.csv')
    
    print("✓ Solution exported:")
    print("  - JSON format: output/solution.json")
    print("  - CSV format: output/solution.csv")
else:
    print("✗ No solution to export")

# ============================================================================
# CONCEPTUAL QUESTIONS (15 points)
# ============================================================================

print("\n" + "=" * 60)
print("CONCEPTUAL QUESTIONS")
print("=" * 60)

# YOUR CODE HERE (3 points each)
# Answer the following conceptual questions about CSP and scheduling

# Question 1: What is the main advantage of the MRV (Minimum Remaining Values) heuristic?
# A) It always finds the optimal solution
# B) It reduces the branching factor early in the search
# C) It guarantees polynomial time complexity
# D) It works best with arc consistency
q1_answer = None  # Replace with "A", "B", "C", or "D"

# Question 2: What does arc consistency accomplish in CSP solving?
# A) It removes values that cannot be part of any solution
# B) It guarantees finding a solution if one exists
# C) It reduces the number of variables in the problem
# D) It eliminates all constraint violations
q2_answer = None  # Replace with "A", "B", "C", or "D"

# Question 3: Which statement about Constraint Satisfaction Problems is TRUE?
# A) CSPs can only handle binary constraints
# B) CSPs always have unique solutions
# C) CSPs can handle both hard and soft constraints
# D) CSPs are only applicable to scheduling problems
q3_answer = None  # Replace with "A", "B", "C", or "D"

# Question 4: What is the worst-case time complexity of backtracking search?
# A) O(n) where n is the number of variables
# B) O(d^n) where d is domain size and n is number of variables
# C) O(n^2) where n is the number of variables
# D) O(n log n) where n is the number of variables
q4_answer = None  # Replace with "A", "B", "C", or "D"

# Question 5: Which heuristic is generally more effective for CSP solving?
# A) MRV is generally more effective than degree heuristic
# B) Degree heuristic is always better than MRV
# C) Heuristics have no impact on CSP solving
# D) The choice of heuristic doesn't matter
q5_answer = None  # Replace with "A", "B", "C", or "D"

# Provide explanations for your answers (these will be graded manually)
q1_explanation = """
YOUR EXPLANATION HERE (2 points)
Explain why you chose your answer for Question 1.
"""

q2_explanation = """
YOUR EXPLANATION HERE (2 points)
Explain why you chose your answer for Question 2.
"""

q3_explanation = """
YOUR EXPLANATION HERE (2 points)
Explain why you chose your answer for Question 3.
"""

q4_explanation = """
YOUR EXPLANATION HERE (1 point)
Explain why you chose your answer for Question 4.
"""

q5_explanation = """
YOUR EXPLANATION HERE (1 point)
Explain why you chose your answer for Question 5.
"""

print("✓ Conceptual questions answered:")
print(f"  - Q1 (MRV): {q1_answer}")
print(f"  - Q2 (Arc Consistency): {q2_answer}")
print(f"  - Q3 (CSP): {q3_answer}")
print(f"  - Q4 (Complexity): {q4_answer}")
print(f"  - Q5 (Heuristics): {q5_answer}")

# ============================================================================
# BONUS FEATURES (10 points)
# ============================================================================

print("\n" + "=" * 60)
print("BONUS FEATURES")
print("=" * 60)

# BONUS TASK 1: Implement arc consistency (3 points)
# YOUR CODE HERE
# Add arc consistency functionality to your CSP solver
# This should be implemented in the SchedulingCSP class or as a separate function

# BONUS TASK 2: Implement heuristic comparison (3 points)
# YOUR CODE HERE
# Create a function that compares the performance of different heuristics
# Parameters: scheduling_csp (SchedulingCSP), heuristics (list), timeout (int)
# Returns: dictionary with results for each heuristic

def compare_heuristics(scheduling_csp, heuristics, timeout=30):
    """Compare performance of different heuristics"""
    # YOUR CODE HERE
    pass

# BONUS TASK 3: Implement solution optimization (4 points)
# YOUR CODE HERE
# Create a function that optimizes the solution by improving resource utilization
# Parameters: solution (dict), tasks (list), resources (list), constraints (dict)
# Returns: optimized solution (dict)

def optimize_solution(solution, tasks, resources, constraints):
    """Optimize the solution by improving resource utilization"""
    # YOUR CODE HERE
    pass

# Test bonus features
if best_solution and scheduling_csp:
    heuristic_comparison = compare_heuristics(scheduling_csp, ['mrv', 'degree', 'combined'])
    optimized_solution = optimize_solution(best_solution, schedule['tasks'], schedule['resources'], schedule['constraints'])
    
    print("✓ Bonus features implemented:")
    print("  - Heuristic comparison analysis")
    print("  - Solution optimization")
    print("  - Performance metrics calculation")
else:
    print("✗ Bonus features require valid solution and CSP")

# ============================================================================
# GUI INTEGRATION
# ============================================================================

print("\n" + "=" * 60)
print("GUI INTEGRATION")
print("=" * 60)

# YOUR CODE HERE
# Implement a function to run the GUI application
# This should launch the PySide6-based GUI for interactive exploration

def run_gui():
    """Run the GUI application"""
    # YOUR CODE HERE
    pass

print("✓ GUI integration ready")
print("  - Run 'run_gui()' to launch the desktop application")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 60)
print("FINAL SUMMARY")
print("=" * 60)

if best_solution:
    print("✓ CSP Scheduling Project completed successfully!")
    print(f"  - Tasks processed: {len(schedule['tasks'])}")
    print(f"  - Resources available: {len(schedule['resources'])}")
    print(f"  - Solution found: {len(best_solution)} tasks scheduled")
    
    print("\nFiles generated:")
    print("  - output/gantt_chart.png")
    print("  - output/resource_utilization.png")
    print("  - output/solution.json")
    print("  - output/solution.csv")
    
    print("\nNext steps:")
    print("  1. Review the generated visualizations")
    print("  2. Analyze the exported solution files")
    print("  3. Run the GUI for interactive exploration")
    print("  4. Submit your completed assignment")
else:
    print("✗ Project incomplete - no solution found")
    print("  Please complete all required steps")

print("=" * 60) 