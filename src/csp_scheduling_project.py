"""
CSP Scheduling Project - Main Assignment Script
University of North Dakota – CSCI 384 AI Course | Spring 2025

Title: Constraint Satisfaction Problem (CSP) Scheduling Solver
Total Points: 100 (+20 bonus points)
Difficulty Level: 9/10 ⭐⭐⭐⭐⭐⭐⭐⭐⭐

This is the main assignment script. You must complete each step where "YOUR CODE HERE" is indicated.
Use the provided helper modules (utils/ and src/csp_solver.py) to assist you.
The project implements a comprehensive CSP solver for real-world scheduling problems.
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
# STEP 1 [10 pts]: Load and Validate Data
# ---------------------------------------------------------------
# Load the scheduling problem data from the data directory.
# Validate that the data structure is correct before proceeding.

print("=" * 60)
print("STEP 1: Loading and Validating Data")
print("=" * 60)

# YOUR CODE HERE:
# Load the scheduling data using the provided utility function
# Hint: Use load_schedule_data() from utils.file_utils

data = load_schedule_data()

# YOUR CODE HERE:
# Validate the data structure using the provided utility function
# Hint: Use validate_data_structure() from utils.file_utils

is_valid = validate_data_structure(data)

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
# STEP 2 [10 pts]: Create CSP Problem Formulation
# ---------------------------------------------------------------
# Formulate the scheduling problem as a CSP by defining variables, domains, and constraints.

print("\n" + "=" * 60)
print("STEP 2: CSP Problem Formulation")
print("=" * 60)

# YOUR CODE HERE:
# Create a SchedulingCSP instance with the loaded data
# Hint: Use the SchedulingCSP class from src.csp_solver

scheduling_csp = SchedulingCSP(tasks, resources, time_slots, constraints)

# YOUR CODE HERE:
# Create the CSP solver instance
# Hint: Use the create_csp() method of the SchedulingCSP instance

csp_solver = scheduling_csp.create_csp()

print("✅ CSP problem formulation completed!")
print(f"   - Variables (tasks): {len(csp_solver.variables)}")
print(f"   - Constraints: {len(csp_solver.constraints)}")

# ---------------------------------------------------------------
# STEP 3 [15 pts]: Implement Variable Ordering Heuristics
# ---------------------------------------------------------------
# Implement the MRV (Minimum Remaining Values) and Degree heuristics for variable ordering.

print("\n" + "=" * 60)
print("STEP 3: Variable Ordering Heuristics")
print("=" * 60)

# YOUR CODE HERE:
# Test the MRV heuristic by selecting variables in order
# Hint: Use the select_mrv_variable method of the CSP solver

print("Testing MRV (Minimum Remaining Values) heuristic:")
mrv_order = []
for i in range(min(5, len(tasks))):  # Test with first 5 variables
    # YOUR CODE HERE:
    # Select the next variable using MRV heuristic
    # Hint: Use select_mrv_variable() method
    
    next_var = csp_solver.select_mrv_variable(list(csp_solver.variables.keys()))
    
    if next_var:
        mrv_order.append(next_var)
        print(f"   {i+1}. {next_var}")

# YOUR CODE HERE:
# Test the Degree heuristic by selecting variables in order
# Hint: Use the select_degree_variable method of the CSP solver

print("\nTesting Degree heuristic:")
degree_order = []
for i in range(min(5, len(tasks))):  # Test with first 5 variables
    # YOUR CODE HERE:
    # Select the next variable using Degree heuristic
    # Hint: Use select_degree_variable() method
    
    next_var = csp_solver.select_degree_variable(list(csp_solver.variables.keys()))
    
    if next_var:
        degree_order.append(next_var)
        print(f"   {i+1}. {next_var}")

print("✅ Variable ordering heuristics implemented!")

# ---------------------------------------------------------------
# STEP 4 [20 pts]: Solve CSP with Different Heuristics
# ---------------------------------------------------------------
# Solve the CSP using different heuristics and compare their performance.

print("\n" + "=" * 60)
print("STEP 4: Solving CSP with Different Heuristics")
print("=" * 60)

# Performance tracking
performance_results = {}

# YOUR CODE HERE:
# Solve the CSP using MRV heuristic
# Hint: Use the solve() method of the SchedulingCSP instance

print("Solving with MRV heuristic...")
start_time = time.time()
# YOUR CODE HERE:
solution_mrv = scheduling_csp.solve(heuristic="mrv")
mrv_time = time.time() - start_time

if solution_mrv:
    print(f"✅ MRV solution found in {mrv_time:.2f} seconds")
    performance_results['MRV'] = [mrv_time, len(solution_mrv)]
else:
    print("❌ MRV heuristic failed to find solution")
    performance_results['MRV'] = [mrv_time, 0]

# YOUR CODE HERE:
# Solve the CSP using Degree heuristic
# Hint: Use the solve() method with 'degree' parameter

print("\nSolving with Degree heuristic...")
start_time = time.time()
# YOUR CODE HERE:
solution_degree = scheduling_csp.solve(heuristic="degree")
degree_time = time.time() - start_time

if solution_degree:
    print(f"✅ Degree solution found in {degree_time:.2f} seconds")
    performance_results['Degree'] = [degree_time, len(solution_degree)]
else:
    print("❌ Degree heuristic failed to find solution")
    performance_results['Degree'] = [degree_time, 0]

# YOUR CODE HERE:
# Solve the CSP using Combined heuristic (MRV + Degree)
# Hint: Use the solve() method with 'combined' parameter

print("\nSolving with Combined heuristic...")
start_time = time.time()
# YOUR CODE HERE:
solution_combined = scheduling_csp.solve(heuristic="combined")
combined_time = time.time() - start_time

if solution_combined:
    print(f"✅ Combined solution found in {combined_time:.2f} seconds")
    performance_results['Combined'] = [combined_time, len(solution_combined)]
else:
    print("❌ Combined heuristic failed to find solution")
    performance_results['Combined'] = [combined_time, 0]

# ---------------------------------------------------------------
# STEP 5 [15 pts]: Solution Analysis and Validation
# ---------------------------------------------------------------
# Analyze the solutions found and validate them against the constraints.

print("\n" + "=" * 60)
print("STEP 5: Solution Analysis and Validation")
print("=" * 60)

# Select the best solution (first one found)
best_solution = solution_mrv or solution_degree or solution_combined

if best_solution:
    print("📋 Best Solution Found:")
    for task_id, assignment in best_solution.items():
        print(f"   {task_id}: {assignment['task_name']} -> {assignment['resource_name']} "
              f"({assignment['start_day']} {assignment['start_hour']}:00, {assignment['duration']}h)")
    
    # YOUR CODE HERE:
    # Calculate the overall schedule score
    # Hint: Use calculate_schedule_score() from utils.constraint_utils
    
    schedule_score = calculate_schedule_score(best_solution, tasks, resources)
    print(f"\n📊 Schedule Quality Score: {schedule_score:.3f}")
    
    # YOUR CODE HERE:
    # Check for constraint violations in the solution
    # Hint: Use get_constraint_violations() for each task assignment
    
    violations = {}
    for task_id, assignment in best_solution.items():
        # YOUR CODE HERE:
        # Get violations for this task assignment
        # Hint: Use get_constraint_violations() function
        
        task_violations = get_constraint_violations(assignment, task_id, resources, tasks, best_solution)
        
        if task_violations:
            violations[task_id] = task_violations
    
    if violations:
        print(f"\n⚠️  Constraint Violations Found: {len(violations)}")
        for task_id, task_violations in violations.items():
            print(f"   {task_id}: {len(task_violations)} violations")
    else:
        print("\n✅ No constraint violations found!")
    
    # YOUR CODE HERE:
    # Calculate resource utilization
    # Hint: Count total hours for each resource
    
    resource_hours = {}
    for assignment in best_solution.values():
        resource_id = assignment['resource_id']
        duration = assignment['duration']
        # YOUR CODE HERE:
        # Add duration to the resource's total hours
        
        resource_hours[resource_id] = resource_hours.get(resource_id, 0) + duration
    
    print(f"\n📈 Resource Utilization:")
    for resource_id, hours in resource_hours.items():
        resource_name = next(r['name'] for r in resources if r['id'] == resource_id)
        print(f"   {resource_name}: {hours} hours")
    
else:
    print("❌ No solution found with any heuristic")

# ---------------------------------------------------------------
# STEP 6 [15 pts]: Visualization and Export
# ---------------------------------------------------------------
# Create visualizations of the solution and export the results.

print("\n" + "=" * 60)
print("STEP 6: Visualization and Export")
print("=" * 60)

if best_solution:
    # YOUR CODE HERE:
    # Create and save all visualizations
    # Hint: Use save_all_visualizations() from utils.visualization
    
    save_all_visualizations(best_solution, tasks, resources)
    
    print("✅ Visualizations created and saved to output/ directory")
    
    # YOUR CODE HERE:
    # Export the solution to JSON format
    # Hint: Use export_schedule_to_json() from utils.file_utils
    
    export_schedule_to_json(best_solution, "output/solution.json")
    
    print("✅ Solution exported to output/solution.json")
    
    # YOUR CODE HERE:
    # Create performance comparison chart
    # Hint: Use create_performance_comparison_chart() from utils.visualization
    
    import matplotlib.pyplot as plt
    fig = create_performance_comparison_chart(performance_results)
    fig.savefig("output/performance_comparison.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    print("✅ Performance comparison chart created")
    
else:
    print("❌ No solution to visualize or export")

# ---------------------------------------------------------------
# STEP 7 [15 pts]: Answer Conceptual Questions
# ---------------------------------------------------------------
# Answer questions about CSP theory and the implemented algorithms.

print("\n" + "=" * 60)
print("STEP 7: Conceptual Questions")
print("=" * 60)

# Q1 [5 pts]: Explain the difference between MRV and Degree heuristics
print("Q1: Explain the difference between MRV and Degree heuristics")
print("Your answer should include:")
print("- How MRV selects variables (fewest remaining values)")
print("- How Degree selects variables (most constraints on remaining variables)")
print("- When each heuristic is most effective")
print("- The trade-offs between them")

q1_answer = """
YOUR ANSWER HERE:

"""

# Q2 [5 pts]: What is arc consistency and why is it useful in CSP solving?
print("\nQ2: What is arc consistency and why is it useful in CSP solving?")
print("Your answer should include:")
print("- Definition of arc consistency")
print("- How it reduces search space")
print("- When it's most beneficial")
print("- Potential computational costs")

q2_answer = """
YOUR ANSWER HERE:

"""

# Q3 [5 pts]: Compare the performance of the three heuristics you implemented
print("\nQ3: Compare the performance of the three heuristics you implemented")
print("Your answer should include:")
print("- Execution time comparison")
print("- Solution quality comparison")
print("- When to use each heuristic")
print("- Recommendations for real-world problems")

q3_answer = """
YOUR ANSWER HERE:

"""

# ---------------------------------------------------------------
# BONUS SECTION: Advanced Analysis [20 bonus points]
# ---------------------------------------------------------------
# Advanced analysis and optimization techniques.

print("\n" + "=" * 60)
print("BONUS SECTION: Advanced Analysis")
print("=" * 60)

# BONUS Task 1 [10 pts]: Implement constraint relaxation
print("BONUS Task 1: Constraint Relaxation")
print("Implement a mechanism to relax soft constraints when no solution is found")

# YOUR CODE HERE:
# Implement constraint relaxation logic
# This could involve:
# - Temporarily removing soft constraints
# - Adjusting constraint weights
# - Finding the best partial solution

def relax_constraints():
    """
    Implement constraint relaxation to find a solution when hard constraints fail
    """
    # YOUR CODE HERE:
    # Implement constraint relaxation
    
    pass

# BONUS Task 2 [10 pts]: Performance optimization
print("\nBONUS Task 2: Performance Optimization")
print("Implement additional optimizations to improve solver performance")

# YOUR CODE HERE:
# Implement performance optimizations such as:
# - Forward checking
# - Dynamic variable ordering
# - Constraint propagation improvements
# - Parallel search strategies

def optimize_performance():
    """
    Implement performance optimizations for the CSP solver
    """
    # YOUR CODE HERE:
    # Implement performance optimizations
    
    pass

# ---------------------------------------------------------------
# FINAL OUTPUT AND SUMMARY
# ---------------------------------------------------------------

print("\n" + "=" * 60)
print("FINAL SUMMARY")
print("=" * 60)

print("🎯 CSP Scheduling Project Summary:")
print(f"   - Tasks processed: {len(tasks)}")
print(f"   - Resources available: {len(resources)}")
print(f"   - Solution found: {'Yes' if best_solution else 'No'}")

if best_solution:
    print(f"   - Solution quality: {schedule_score:.3f}")
    print(f"   - Constraint violations: {len(violations) if 'violations' in locals() else 0}")
    print(f"   - Best heuristic: {min(performance_results.items(), key=lambda x: x[1][0])[0]}")

print("\n📁 Files generated:")
print("   - output/gantt_chart.png")
print("   - output/resource_utilization.png")
print("   - output/timeline.png")
print("   - output/solution.json")
print("   - output/performance_comparison.png")

print("\n✅ Assignment completed successfully!")
print("📝 Remember to submit your completed script and report.") 