"""
File utilities for CSP Scheduling Project
Provides functions for loading and saving scheduling data
"""

import json
import os
from typing import Dict, List, Any, Optional
import pandas as pd


def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Load data from a JSON file
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dictionary containing the loaded data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in {file_path}: {e}")


def save_json_file(data: Dict[str, Any], file_path: str) -> None:
    """
    Save data to a JSON file
    
    Args:
        data: Dictionary to save
        file_path: Path where to save the file
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def load_schedule_data(data_dir: str = "data") -> Dict[str, Any]:
    """
    Load scheduling problem data from the data directory
    
    Args:
        data_dir: Directory containing the data files
        
    Returns:
        Dictionary containing tasks, resources, and constraints
    """
    schedule_file = os.path.join(data_dir, "sample_schedule.json")
    constraints_file = os.path.join(data_dir, "constraints.json")
    
    schedule_data = load_json_file(schedule_file)
    constraints_data = load_json_file(constraints_file)
    
    return {
        "schedule": schedule_data,
        "constraints": constraints_data
    }


def export_schedule_to_csv(schedule: Dict[str, Any], output_path: str) -> None:
    """
    Export a schedule to CSV format for easy viewing
    
    Args:
        schedule: The schedule dictionary
        output_path: Path where to save the CSV file
    """
    # Convert schedule to DataFrame format
    rows = []
    for task_id, assignment in schedule.items():
        if isinstance(assignment, dict):
            rows.append({
                'task_id': task_id,
                'resource_id': assignment.get('resource_id', ''),
                'start_day': assignment.get('start_day', ''),
                'start_hour': assignment.get('start_hour', ''),
                'duration': assignment.get('duration', ''),
                'end_day': assignment.get('end_day', ''),
                'end_hour': assignment.get('end_hour', '')
            })
    
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)


def export_schedule_to_json(schedule: Dict[str, Any], output_path: str) -> None:
    """
    Export a schedule to JSON format
    
    Args:
        schedule: The schedule dictionary
        output_path: Path where to save the JSON file
    """
    save_json_file(schedule, output_path)


def validate_data_structure(data: Dict[str, Any]) -> bool:
    """
    Validate that the loaded data has the correct structure
    
    Args:
        data: The data dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_keys = ['tasks', 'resources', 'time_slots', 'constraints']
    
    if 'schedule' in data:
        schedule_data = data['schedule']
    else:
        schedule_data = data
    
    for key in required_keys:
        if key not in schedule_data:
            print(f"Missing required key: {key}")
            return False
    
    # Validate tasks structure
    for task in schedule_data['tasks']:
        required_task_keys = ['id', 'name', 'duration', 'priority', 'required_skills']
        for key in required_task_keys:
            if key not in task:
                print(f"Task missing required key: {key}")
                return False
    
    # Validate resources structure
    for resource in schedule_data['resources']:
        required_resource_keys = ['id', 'name', 'skills', 'availability', 'max_hours_per_day']
        for key in required_resource_keys:
            if key not in resource:
                print(f"Resource missing required key: {key}")
                return False
    
    return True


def get_available_data_files(data_dir: str = "data") -> List[str]:
    """
    Get list of available data files in the data directory
    
    Args:
        data_dir: Directory to search for data files
        
    Returns:
        List of available data file names
    """
    if not os.path.exists(data_dir):
        return []
    
    files = []
    for file in os.listdir(data_dir):
        if file.endswith(('.json', '.csv')):
            files.append(file)
    
    return sorted(files)


def create_sample_data() -> Dict[str, Any]:
    """
    Create a minimal sample dataset for testing
    
    Returns:
        Dictionary containing sample scheduling data
    """
    return {
        "tasks": [
            {
                "id": "T1",
                "name": "Sample Task 1",
                "duration": 2,
                "priority": "high",
                "required_skills": ["skill1"],
                "dependencies": [],
                "preferred_resources": ["R1"]
            }
        ],
        "resources": [
            {
                "id": "R1",
                "name": "Sample Resource 1",
                "skills": ["skill1"],
                "availability": {
                    "monday": [9, 10, 11, 12, 13, 14, 15, 16, 17],
                    "tuesday": [9, 10, 11, 12, 13, 14, 15, 16, 17]
                },
                "max_hours_per_day": 8
            }
        ],
        "time_slots": {
            "days": ["monday", "tuesday"],
            "hours": [9, 10, 11, 12, 13, 14, 15, 16, 17],
            "working_hours_per_day": 8
        },
        "constraints": {
            "hard_constraints": ["no_resource_overlap", "resource_skills"],
            "soft_constraints": ["preferred_resources"]
        }
    } 