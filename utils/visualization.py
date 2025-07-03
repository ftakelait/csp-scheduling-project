"""
Visualization utilities for CSP Scheduling Project
Provides functions for plotting schedules and performance metrics
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
import seaborn as sns


def create_gantt_chart(schedule: Dict[str, Any], tasks: List[Dict], 
                      resources: List[Dict], figsize: Tuple[int, int] = (12, 8)) -> plt.Figure:
    """
    Create a Gantt chart visualization of the schedule
    
    Args:
        schedule: Schedule assignments
        tasks: List of all tasks
        resources: List of all resources
        figsize: Figure size (width, height)
        
    Returns:
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Define colors for different priorities
    priority_colors = {'high': '#ff6b6b', 'medium': '#4ecdc4', 'low': '#45b7d1'}
    
    # Create resource mapping
    resource_names = {r['id']: r['name'] for r in resources}
    resource_ids = list(resource_names.keys())
    
    # Create day mapping
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    day_positions = {day: i for i, day in enumerate(days)}
    
    # Plot each task
    for task_id, assignment in schedule.items():
        # Find task details
        task = None
        for t in tasks:
            if t['id'] == task_id:
                task = t
                break
        
        if not task:
            continue
        
        resource_id = assignment.get('resource_id')
        start_day = assignment.get('start_day')
        start_hour = assignment.get('start_hour')
        duration = assignment.get('duration', 0)
        
        if resource_id not in resource_ids or start_day not in day_positions:
            continue
        
        # Calculate positions
        resource_idx = resource_ids.index(resource_id)
        day_idx = day_positions[start_day]
        
        # Create rectangle
        rect = Rectangle((start_hour, resource_idx - 0.4), duration, 0.8,
                        facecolor=priority_colors.get(task.get('priority', 'medium'), '#cccccc'),
                        edgecolor='black', linewidth=1)
        ax.add_patch(rect)
        
        # Add task label
        ax.text(start_hour + duration/2, resource_idx, task['name'], 
                ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Customize the plot
    ax.set_xlim(9, 18)
    ax.set_ylim(-0.5, len(resource_ids) - 0.5)
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Resources')
    ax.set_title('Project Schedule Gantt Chart')
    
    # Set y-axis labels
    ax.set_yticks(range(len(resource_ids)))
    ax.set_yticklabels([resource_names[rid] for rid in resource_ids])
    
    # Set x-axis labels
    ax.set_xticks(range(9, 19))
    ax.set_xticklabels([f'{h}:00' for h in range(9, 19)])
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    # Add legend
    legend_elements = [patches.Patch(color=color, label=priority.title()) 
                      for priority, color in priority_colors.items()]
    ax.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    return fig


def create_resource_utilization_chart(schedule: Dict[str, Any], resources: List[Dict], 
                                     figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
    """
    Create a resource utilization chart
    
    Args:
        schedule: Schedule assignments
        resources: List of all resources
        figsize: Figure size (width, height)
        
    Returns:
        Matplotlib figure object
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Calculate utilization for each resource
    resource_hours = {}
    resource_names = {}
    
    for resource in resources:
        resource_id = resource['id']
        resource_names[resource_id] = resource['name']
        resource_hours[resource_id] = 0
    
    # Count hours from schedule
    for task_id, assignment in schedule.items():
        resource_id = assignment.get('resource_id')
        duration = assignment.get('duration', 0)
        if resource_id in resource_hours:
            resource_hours[resource_id] += duration
    
    # Create bar chart
    resource_ids = list(resource_hours.keys())
    hours = list(resource_hours.values())
    names = [resource_names[rid] for rid in resource_ids]
    
    bars = ax1.bar(names, hours, color='skyblue', edgecolor='navy')
    ax1.set_xlabel('Resources')
    ax1.set_ylabel('Total Hours')
    ax1.set_title('Resource Utilization')
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, hour in zip(bars, hours):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{hour}h', ha='center', va='bottom')
    
    # Create pie chart
    total_hours = sum(hours)
    if total_hours > 0:
        percentages = [h/total_hours * 100 for h in hours]
        ax2.pie(percentages, labels=names, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Resource Workload Distribution')
    
    plt.tight_layout()
    return fig


def create_constraint_violation_chart(violations: Dict[str, List[str]], 
                                    figsize: Tuple[int, int] = (8, 6)) -> plt.Figure:
    """
    Create a chart showing constraint violations
    
    Args:
        violations: Dictionary mapping task IDs to violation lists
        figsize: Figure size (width, height)
        
    Returns:
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Count violations by type
    violation_counts = {}
    for task_id, violation_list in violations.items():
        for violation in violation_list:
            # Extract violation type from message
            if 'not available' in violation:
                violation_type = 'Resource Availability'
            elif 'dependencies' in violation:
                violation_type = 'Task Dependencies'
            elif 'skills' in violation:
                violation_type = 'Resource Skills'
            elif 'max hours' in violation:
                violation_type = 'Max Hours Per Day'
            else:
                violation_type = 'Other'
            
            violation_counts[violation_type] = violation_counts.get(violation_type, 0) + 1
    
    if violation_counts:
        violation_types = list(violation_counts.keys())
        counts = list(violation_counts.values())
        
        bars = ax.bar(violation_types, counts, color='lightcoral', edgecolor='darkred')
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
        ax.text(0.5, 0.5, 'No Violations Found', ha='center', va='center', 
                transform=ax.transAxes, fontsize=14, fontweight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
    
    plt.tight_layout()
    return fig


def create_performance_comparison_chart(performance_data: Dict[str, List[float]], 
                                       figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
    """
    Create a performance comparison chart for different algorithms
    
    Args:
        performance_data: Dictionary mapping algorithm names to performance metrics
        figsize: Figure size (width, height)
        
    Returns:
        Matplotlib figure object
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    algorithms = list(performance_data.keys())
    
    # Time performance
    times = [data[0] if len(data) > 0 else 0 for data in performance_data.values()]
    bars1 = ax1.bar(algorithms, times, color='lightgreen', edgecolor='darkgreen')
    ax1.set_xlabel('Algorithm')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('Execution Time Comparison')
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, time in zip(bars1, times):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{time:.2f}s', ha='center', va='bottom')
    
    # Solution quality
    qualities = [data[1] if len(data) > 1 else 0 for data in performance_data.values()]
    bars2 = ax2.bar(algorithms, qualities, color='lightblue', edgecolor='darkblue')
    ax2.set_xlabel('Algorithm')
    ax2.set_ylabel('Solution Quality Score')
    ax2.set_title('Solution Quality Comparison')
    ax2.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, quality in zip(bars2, qualities):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{quality:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    return fig


def create_schedule_timeline(schedule: Dict[str, Any], tasks: List[Dict], 
                           figsize: Tuple[int, int] = (12, 6)) -> plt.Figure:
    """
    Create a timeline visualization of the schedule
    
    Args:
        schedule: Schedule assignments
        tasks: List of all tasks
        figsize: Figure size (width, height)
        
    Returns:
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Define colors for different priorities
    priority_colors = {'high': '#ff6b6b', 'medium': '#4ecdc4', 'low': '#45b7d1'}
    
    # Create day mapping
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    
    # Plot each task
    y_pos = 0
    for task_id, assignment in schedule.items():
        # Find task details
        task = None
        for t in tasks:
            if t['id'] == task_id:
                task = t
                break
        
        if not task:
            continue
        
        start_day = assignment.get('start_day')
        start_hour = assignment.get('start_hour')
        duration = assignment.get('duration', 0)
        
        if start_day not in days:
            continue
        
        # Calculate positions
        day_idx = days.index(start_day)
        x_start = day_idx * 24 + start_hour
        x_end = x_start + duration
        
        # Create rectangle
        rect = Rectangle((x_start, y_pos - 0.3), duration, 0.6,
                        facecolor=priority_colors.get(task.get('priority', 'medium'), '#cccccc'),
                        edgecolor='black', linewidth=1)
        ax.add_patch(rect)
        
        # Add task label
        ax.text(x_start + duration/2, y_pos, f"{task['name']}\n({task_id})", 
                ha='center', va='center', fontsize=8, fontweight='bold')
        
        y_pos += 1
    
    # Customize the plot
    ax.set_xlim(0, len(days) * 24)
    ax.set_ylim(-0.5, y_pos - 0.5)
    ax.set_xlabel('Time (Hours)')
    ax.set_ylabel('Tasks')
    ax.set_title('Project Timeline')
    
    # Set x-axis labels
    ax.set_xticks([i * 24 + 12 for i in range(len(days))])
    ax.set_xticklabels([day.title() for day in days])
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    # Add legend
    legend_elements = [patches.Patch(color=color, label=priority.title()) 
                      for priority, color in priority_colors.items()]
    ax.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    return fig


def save_all_visualizations(schedule: Dict[str, Any], tasks: List[Dict], 
                           resources: List[Dict], output_dir: str = "output") -> None:
    """
    Create and save all visualization charts
    
    Args:
        schedule: Schedule assignments
        tasks: List of all tasks
        resources: List of all resources
        output_dir: Directory to save the charts
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Create Gantt chart
    fig1 = create_gantt_chart(schedule, tasks, resources)
    fig1.savefig(os.path.join(output_dir, 'gantt_chart.png'), dpi=300, bbox_inches='tight')
    plt.close(fig1)
    
    # Create resource utilization chart
    fig2 = create_resource_utilization_chart(schedule, resources)
    fig2.savefig(os.path.join(output_dir, 'resource_utilization.png'), dpi=300, bbox_inches='tight')
    plt.close(fig2)
    
    # Create timeline
    fig3 = create_schedule_timeline(schedule, tasks)
    fig3.savefig(os.path.join(output_dir, 'timeline.png'), dpi=300, bbox_inches='tight')
    plt.close(fig3)
    
    print(f"Visualizations saved to {output_dir}/") 