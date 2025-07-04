"""
Visualization Utilities for CSP Scheduling Project
Functions for creating charts and visualizations of scheduling solutions
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime
import os

def create_gantt_chart(solution: Dict[str, Any], tasks: List[Dict], 
                      resources: List[Dict]) -> plt.Figure:
    """
    Create a Gantt chart visualization of the schedule
    
    Args:
        solution: Dictionary containing task assignments
        tasks: List of task dictionaries
        resources: List of resource dictionaries
        
    Returns:
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Define colors for different resources
    colors = plt.cm.Set3(np.linspace(0, 1, len(resources)))
    resource_colors = {resource['id']: colors[i] for i, resource in enumerate(resources)}
    
    # Define day order
    day_order = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4}
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    # Create the Gantt chart
    y_pos = 0
    task_labels = []
    
    for task_id, assignment in solution.items():
        # Find task name
        task_name = assignment.get('task_name', task_id)
        resource_name = assignment.get('resource_name', 'Unknown')
        
        # Calculate position
        start_day = day_order.get(assignment.get('start_day', 'monday'), 0)
        start_hour = assignment.get('start_hour', 9)
        duration = assignment.get('duration', 1)
        
        # Convert to hours from start of week
        start_time = start_day * 8 + (start_hour - 9)  # Assuming 9-17 work hours
        end_time = start_time + duration
        
        # Create rectangle
        color = resource_colors.get(assignment.get('resource_id', 'R1'), 'gray')
        rect = patches.Rectangle((start_time, y_pos - 0.3), duration, 0.6, 
                               facecolor=color, edgecolor='black', alpha=0.7)
        ax.add_patch(rect)
        
        # Add text label
        ax.text(start_time + duration/2, y_pos, f'{task_name}\n({resource_name})', 
               ha='center', va='center', fontsize=8, fontweight='bold')
        
        task_labels.append(f'{task_name} ({resource_name})')
        y_pos += 1
    
    # Customize the chart
    ax.set_ylim(-0.5, len(solution) - 0.5)
    ax.set_xlim(0, 40)  # 5 days * 8 hours
    ax.set_xlabel('Time (Hours from Monday 9 AM)')
    ax.set_ylabel('Tasks')
    ax.set_title('Project Schedule Gantt Chart')
    
    # Set x-axis ticks
    ax.set_xticks([i * 8 for i in range(6)])
    ax.set_xticklabels(days)
    
    # Set y-axis ticks
    ax.set_yticks(range(len(solution)))
    ax.set_yticklabels(task_labels)
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def create_resource_utilization_chart(solution: Dict[str, Any], 
                                     resources: List[Dict]) -> plt.Figure:
    """
    Create a chart showing resource utilization
    
    Args:
        solution: Dictionary containing task assignments
        resources: List of resource dictionaries
        
    Returns:
        Matplotlib figure object
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Calculate utilization for each resource
    resource_hours = {}
    resource_tasks = {}
    
    for resource in resources:
        resource_id = resource['id']
        resource_hours[resource_id] = 0
        resource_tasks[resource_id] = []
    
    for task_id, assignment in solution.items():
        resource_id = assignment.get('resource_id')
        duration = assignment.get('duration', 0)
        
        if resource_id in resource_hours:
            resource_hours[resource_id] += duration
            resource_tasks[resource_id].append(assignment.get('task_name', task_id))
    
    # Create bar chart of total hours
    resource_names = [r['name'] for r in resources]
    hours = [resource_hours.get(r['id'], 0) for r in resources]
    
    bars = ax1.bar(resource_names, hours, color='skyblue', alpha=0.7)
    ax1.set_xlabel('Resources')
    ax1.set_ylabel('Total Hours')
    ax1.set_title('Resource Utilization (Total Hours)')
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, hour in zip(bars, hours):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{hour}h', ha='center', va='bottom')
    
    # Create pie chart of workload distribution
    non_zero_hours = [(name, hour) for name, hour in zip(resource_names, hours) if hour > 0]
    
    if non_zero_hours:
        names, hours_list = zip(*non_zero_hours)
        ax2.pie(hours_list, labels=names, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Workload Distribution')
    else:
        ax2.text(0.5, 0.5, 'No tasks assigned', ha='center', va='center', 
                transform=ax2.transAxes, fontsize=12)
        ax2.set_title('Workload Distribution')
    
    plt.tight_layout()
    return fig

def create_constraint_violation_chart(solution: Dict[str, Any], tasks: List[Dict],
                                    resources: List[Dict], constraints: Dict) -> plt.Figure:
    """
    Create a chart showing constraint violations
    
    Args:
        solution: Dictionary containing task assignments
        tasks: List of task dictionaries
        resources: List of resource dictionaries
        constraints: Dictionary of constraints
        
    Returns:
        Matplotlib figure object
    """
    from utils.constraint_utils import get_constraint_violations
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Count violations by type
    violation_counts = {}
    task_violations = {}
    
    for task_id, assignment in solution.items():
        violations = get_constraint_violations(assignment, task_id, resources, tasks, constraints)
        task_violations[task_id] = violations
        
        for violation in violations:
            violation_counts[violation] = violation_counts.get(violation, 0) + 1
    
    if violation_counts:
        # Create bar chart of violations
        violation_types = list(violation_counts.keys())
        counts = list(violation_counts.values())
        
        bars = ax.bar(violation_types, counts, color='red', alpha=0.7)
        ax.set_xlabel('Violation Type')
        ax.set_ylabel('Number of Violations')
        ax.set_title('Constraint Violations by Type')
        ax.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   str(count), ha='center', va='bottom')
    else:
        ax.text(0.5, 0.5, 'No constraint violations found!', ha='center', va='center',
               transform=ax.transAxes, fontsize=14, fontweight='bold', color='green')
        ax.set_title('Constraint Violations')
    
    plt.tight_layout()
    return fig

def create_performance_comparison_chart(performance_results: Dict[str, Any]) -> plt.Figure:
    """
    Create a chart comparing performance of different heuristics
    
    Args:
        performance_results: Dictionary containing performance metrics for different heuristics
        
    Returns:
        Matplotlib figure object
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    heuristics = list(performance_results.keys())
    
    # Extract metrics
    solve_times = [performance_results[h].get('solve_time', 0) for h in heuristics]
    nodes_explored = [performance_results[h].get('nodes_explored', 0) for h in heuristics]
    solution_quality = [performance_results[h].get('solution_quality', 0) for h in heuristics]
    tasks_scheduled = [performance_results[h].get('tasks_scheduled', 0) for h in heuristics]
    
    # Solve time comparison
    bars1 = ax1.bar(heuristics, solve_times, color='lightblue', alpha=0.7)
    ax1.set_title('Solve Time Comparison')
    ax1.set_ylabel('Time (seconds)')
    ax1.tick_params(axis='x', rotation=45)
    
    # Nodes explored comparison
    bars2 = ax2.bar(heuristics, nodes_explored, color='lightgreen', alpha=0.7)
    ax2.set_title('Nodes Explored Comparison')
    ax2.set_ylabel('Number of Nodes')
    ax2.tick_params(axis='x', rotation=45)
    
    # Solution quality comparison
    bars3 = ax3.bar(heuristics, solution_quality, color='lightcoral', alpha=0.7)
    ax3.set_title('Solution Quality Comparison')
    ax3.set_ylabel('Quality Score')
    ax3.tick_params(axis='x', rotation=45)
    
    # Tasks scheduled comparison
    bars4 = ax4.bar(heuristics, tasks_scheduled, color='lightyellow', alpha=0.7)
    ax4.set_title('Tasks Scheduled Comparison')
    ax4.set_ylabel('Number of Tasks')
    ax4.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bars, values in [(bars1, solve_times), (bars2, nodes_explored), 
                         (bars3, solution_quality), (bars4, tasks_scheduled)]:
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax = bar.axes
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{value:.2f}' if isinstance(value, float) else str(value),
                   ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    return fig

def save_all_visualizations(solution: Dict[str, Any], tasks: List[Dict], 
                          resources: List[Dict], constraints: Dict,
                          performance_results: Optional[Dict[str, Any]] = None,
                          output_dir: str = 'output') -> None:
    """
    Save all visualizations to files
    
    Args:
        solution: Dictionary containing task assignments
        tasks: List of task dictionaries
        resources: List of resource dictionaries
        constraints: Dictionary of constraints
        performance_results: Optional performance comparison results
        output_dir: Directory to save visualizations
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate and save Gantt chart
    gantt_fig = create_gantt_chart(solution, tasks, resources)
    gantt_fig.savefig(f'{output_dir}/gantt_chart.png', dpi=300, bbox_inches='tight')
    plt.close(gantt_fig)
    
    # Generate and save resource utilization chart
    util_fig = create_resource_utilization_chart(solution, resources)
    util_fig.savefig(f'{output_dir}/resource_utilization.png', dpi=300, bbox_inches='tight')
    plt.close(util_fig)
    
    # Generate and save constraint violation chart
    violation_fig = create_constraint_violation_chart(solution, tasks, resources, constraints)
    violation_fig.savefig(f'{output_dir}/constraint_violations.png', dpi=300, bbox_inches='tight')
    plt.close(violation_fig)
    
    # Generate and save performance comparison chart if available
    if performance_results:
        perf_fig = create_performance_comparison_chart(performance_results)
        perf_fig.savefig(f'{output_dir}/performance_comparison.png', dpi=300, bbox_inches='tight')
        plt.close(perf_fig)
    
    print(f"✓ All visualizations saved to {output_dir}/")
    print(f"  - gantt_chart.png")
    print(f"  - resource_utilization.png")
    print(f"  - constraint_violations.png")
    if performance_results:
        print(f"  - performance_comparison.png") 