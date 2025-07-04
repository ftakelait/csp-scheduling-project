"""
File Utilities for CSP Scheduling Project
Functions for loading, validating, and exporting scheduling data
"""

import json
import csv
import os
from typing import Dict, List, Any, Optional

def load_schedule_data(file_path: str = "data/sample_schedule.json") -> Dict[str, Any]:
    """
    Load scheduling data from JSON file
    
    Args:
        file_path: Path to the JSON file containing scheduling data
        
    Returns:
        Dictionary containing the scheduling data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Schedule data file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return data

def validate_data_structure(data: Dict[str, Any]) -> bool:
    """
    Validate that the data has the correct structure
    
    Args:
        data: Dictionary containing scheduling data
        
    Returns:
        True if data structure is valid, False otherwise
    """
    # Check top-level structure
    if 'schedule' not in data:
        return False
    
    schedule = data['schedule']
    
    # Check required keys
    required_keys = ['tasks', 'resources', 'time_slots', 'constraints']
    for key in required_keys:
        if key not in schedule:
            return False
    
    # Check that tasks is a list
    if not isinstance(schedule['tasks'], list):
        return False
    
    # Check that resources is a list
    if not isinstance(schedule['resources'], list):
        return False
    
    # Check that time_slots is a dictionary
    if not isinstance(schedule['time_slots'], dict):
        return False
    
    # Check that constraints is a dictionary
    if not isinstance(schedule['constraints'], dict):
        return False
    
    # Check time_slots structure
    time_slots = schedule['time_slots']
    if 'days' not in time_slots or 'hours' not in time_slots:
        return False
    
    # Check constraints structure
    constraints = schedule['constraints']
    if 'hard_constraints' not in constraints or 'soft_constraints' not in constraints:
        return False
    
    return True

def export_schedule_to_json(solution: Dict[str, Any], filename: str) -> None:
    """
    Export solution to JSON format
    
    Args:
        solution: Dictionary containing the solution
        filename: Output filename
        
    Raises:
        IOError: If there's an error writing the file
    """
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(solution, file, indent=2, ensure_ascii=False)

def export_schedule_to_csv(solution: Dict[str, Any], filename: str) -> None:
    """
    Export solution to CSV format
    
    Args:
        solution: Dictionary containing the solution
        filename: Output filename
        
    Raises:
        IOError: If there's an error writing the file
    """
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Define CSV headers
    headers = ['task_id', 'task_name', 'resource_id', 'resource_name', 
              'start_day', 'start_hour', 'end_hour', 'duration']
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        
        for task_id, assignment in solution.items():
            row = {
                'task_id': task_id,
                'task_name': assignment.get('task_name', ''),
                'resource_id': assignment.get('resource_id', ''),
                'resource_name': assignment.get('resource_name', ''),
                'start_day': assignment.get('start_day', ''),
                'start_hour': assignment.get('start_hour', ''),
                'end_hour': assignment.get('end_hour', ''),
                'duration': assignment.get('duration', '')
            }
            writer.writerow(row)

def load_constraints(file_path: str = "data/constraints.json") -> Dict[str, Any]:
    """
    Load constraint definitions from JSON file
    
    Args:
        file_path: Path to the constraints file
        
    Returns:
        Dictionary containing constraint definitions
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Constraints file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        constraints = json.load(file)
    
    return constraints

def save_performance_metrics(metrics: Dict[str, Any], filename: str) -> None:
    """
    Save performance metrics to JSON file
    
    Args:
        metrics: Dictionary containing performance metrics
        filename: Output filename
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(metrics, file, indent=2, ensure_ascii=False)

def load_performance_metrics(filename: str) -> Dict[str, Any]:
    """
    Load performance metrics from JSON file
    
    Args:
        filename: Input filename
        
    Returns:
        Dictionary containing performance metrics
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Performance metrics file not found: {filename}")
    
    with open(filename, 'r', encoding='utf-8') as file:
        metrics = json.load(file)
    
    return metrics 