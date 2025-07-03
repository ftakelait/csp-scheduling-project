"""
Constraint utilities for CSP Scheduling Project
Provides functions for checking and validating scheduling constraints
"""

from typing import Dict, List, Any, Set, Tuple, Optional
from collections import defaultdict


def check_resource_availability(resource_id: str, day: str, hour: int, 
                              resources: List[Dict], schedule: Dict[str, Any]) -> bool:
    """
    Check if a resource is available at a specific time slot
    
    Args:
        resource_id: ID of the resource to check
        day: Day of the week
        hour: Hour of the day
        resources: List of all resources
        schedule: Current schedule assignments
        
    Returns:
        True if resource is available, False otherwise
    """
    # Find the resource
    resource = None
    for r in resources:
        if r['id'] == resource_id:
            resource = r
            break
    
    if not resource:
        return False
    
    # Check if the time slot is in the resource's availability
    if day not in resource['availability'] or hour not in resource['availability'][day]:
        return False
    
    # Check if the resource is already assigned to another task at this time
    for task_id, assignment in schedule.items():
        if assignment.get('resource_id') == resource_id:
            assignment_day = assignment.get('start_day')
            assignment_hour = assignment.get('start_hour')
            assignment_duration = assignment.get('duration', 0)
            
            # Check if the time slots overlap
            if assignment_day == day:
                assignment_end_hour = assignment_hour + assignment_duration
                if hour >= assignment_hour and hour < assignment_end_hour:
                    return False
    
    return True


def check_task_dependencies(task_id: str, start_time: Tuple[str, int], 
                           schedule: Dict[str, Any], tasks: List[Dict]) -> bool:
    """
    Check if all dependencies of a task are completed before its start time
    
    Args:
        task_id: ID of the task to check
        start_time: Tuple of (day, hour) when the task starts
        schedule: Current schedule assignments
        tasks: List of all tasks
        
    Returns:
        True if dependencies are satisfied, False otherwise
    """
    # Find the task
    task = None
    for t in tasks:
        if t['id'] == task_id:
            task = t
            break
    
    if not task or not task.get('dependencies'):
        return True
    
    start_day, start_hour = start_time
    
    # Check each dependency
    for dep_id in task['dependencies']:
        if dep_id not in schedule:
            return False
        
        dep_assignment = schedule[dep_id]
        dep_day = dep_assignment.get('start_day')
        dep_hour = dep_assignment.get('start_hour')
        dep_duration = dep_assignment.get('duration', 0)
        
        # Calculate when the dependency ends
        dep_end_hour = dep_hour + dep_duration
        
        # If dependency ends on the same day, check if it's before the task starts
        if dep_day == start_day and dep_end_hour > start_hour:
            return False
        
        # If dependency is on a later day, it's not satisfied
        if dep_day > start_day:
            return False
    
    return True


def check_resource_skills(resource_id: str, task_id: str, 
                         resources: List[Dict], tasks: List[Dict]) -> bool:
    """
    Check if a resource has the required skills for a task
    
    Args:
        resource_id: ID of the resource
        task_id: ID of the task
        resources: List of all resources
        tasks: List of all tasks
        
    Returns:
        True if resource has required skills, False otherwise
    """
    # Find the resource and task
    resource = None
    task = None
    
    for r in resources:
        if r['id'] == resource_id:
            resource = r
            break
    
    for t in tasks:
        if t['id'] == task_id:
            task = t
            break
    
    if not resource or not task:
        return False
    
    # Check if resource has all required skills
    required_skills = set(task.get('required_skills', []))
    resource_skills = set(resource.get('skills', []))
    
    return required_skills.issubset(resource_skills)


def check_max_hours_per_day(resource_id: str, day: str, schedule: Dict[str, Any]) -> bool:
    """
    Check if a resource exceeds their maximum hours per day
    
    Args:
        resource_id: ID of the resource
        day: Day to check
        schedule: Current schedule assignments
        
    Returns:
        True if within limits, False otherwise
    """
    total_hours = 0
    
    for task_id, assignment in schedule.items():
        if assignment.get('resource_id') == resource_id and assignment.get('start_day') == day:
            total_hours += assignment.get('duration', 0)
    
    # Get the resource's max hours per day (default to 8)
    max_hours = 8  # This should be retrieved from the resource data
    
    return total_hours <= max_hours


def check_preferred_resources(task_id: str, resource_id: str, tasks: List[Dict]) -> bool:
    """
    Check if a task is assigned to one of its preferred resources
    
    Args:
        task_id: ID of the task
        resource_id: ID of the resource
        tasks: List of all tasks
        
    Returns:
        True if resource is preferred, False otherwise
    """
    # Find the task
    task = None
    for t in tasks:
        if t['id'] == task_id:
            task = t
            break
    
    if not task:
        return False
    
    preferred_resources = task.get('preferred_resources', [])
    return resource_id in preferred_resources


def check_task_priority(task_id: str, start_time: Tuple[str, int], 
                       schedule: Dict[str, Any], tasks: List[Dict]) -> float:
    """
    Calculate a score based on task priority scheduling
    
    Args:
        task_id: ID of the task
        start_time: Tuple of (day, hour) when the task starts
        schedule: Current schedule assignments
        tasks: List of all tasks
        
    Returns:
        Score (higher is better for priority scheduling)
    """
    # Find the task
    task = None
    for t in tasks:
        if t['id'] == task_id:
            task = t
            break
    
    if not task:
        return 0.0
    
    priority = task.get('priority', 'medium')
    priority_weights = {'high': 3.0, 'medium': 2.0, 'low': 1.0}
    weight = priority_weights.get(priority, 1.0)
    
    # Calculate time-based score (earlier is better)
    start_day, start_hour = start_time
    day_weights = {'monday': 5, 'tuesday': 4, 'wednesday': 3, 'thursday': 2, 'friday': 1}
    day_score = day_weights.get(start_day, 0)
    hour_score = 17 - start_hour  # Earlier hours get higher scores
    
    return weight * (day_score + hour_score)


def check_balanced_workload(schedule: Dict[str, Any], resources: List[Dict]) -> float:
    """
    Calculate workload balance among all resources
    
    Args:
        schedule: Current schedule assignments
        resources: List of all resources
        
    Returns:
        Balance score (higher is better)
    """
    if not schedule:
        return 0.0
    
    # Calculate total hours for each resource
    resource_hours = defaultdict(int)
    
    for task_id, assignment in schedule.items():
        resource_id = assignment.get('resource_id')
        duration = assignment.get('duration', 0)
        if resource_id:
            resource_hours[resource_id] += duration
    
    if not resource_hours:
        return 0.0
    
    # Calculate variance (lower variance = better balance)
    hours_list = list(resource_hours.values())
    mean_hours = sum(hours_list) / len(hours_list)
    
    variance = sum((h - mean_hours) ** 2 for h in hours_list) / len(hours_list)
    
    # Convert to a score (lower variance = higher score)
    max_possible_variance = max(hours_list) ** 2 if hours_list else 1
    balance_score = 1.0 - (variance / max_possible_variance)
    
    return max(0.0, balance_score)


def get_constraint_violations(assignment: Dict[str, Any], task_id: str, 
                            resources: List[Dict], tasks: List[Dict], 
                            schedule: Dict[str, Any]) -> List[str]:
    """
    Get list of constraint violations for a potential assignment
    
    Args:
        assignment: The assignment to check
        task_id: ID of the task being assigned
        resources: List of all resources
        tasks: List of all tasks
        schedule: Current schedule assignments
        
    Returns:
        List of constraint violation messages
    """
    violations = []
    
    resource_id = assignment.get('resource_id')
    start_day = assignment.get('start_day')
    start_hour = assignment.get('start_hour')
    duration = assignment.get('duration', 0)
    
    # Check resource availability
    for hour in range(start_hour, start_hour + duration):
        if not check_resource_availability(resource_id, start_day, hour, resources, schedule):
            violations.append(f"Resource {resource_id} not available at {start_day} {hour}:00")
    
    # Check task dependencies
    if not check_task_dependencies(task_id, (start_day, start_hour), schedule, tasks):
        violations.append(f"Task {task_id} dependencies not satisfied")
    
    # Check resource skills
    if not check_resource_skills(resource_id, task_id, resources, tasks):
        violations.append(f"Resource {resource_id} lacks required skills for task {task_id}")
    
    # Check max hours per day
    if not check_max_hours_per_day(resource_id, start_day, schedule):
        violations.append(f"Resource {resource_id} exceeds max hours per day on {start_day}")
    
    return violations


def calculate_schedule_score(schedule: Dict[str, Any], tasks: List[Dict], 
                           resources: List[Dict]) -> float:
    """
    Calculate overall score for a complete schedule
    
    Args:
        schedule: Complete schedule assignments
        tasks: List of all tasks
        resources: List of all resources
        
    Returns:
        Overall schedule score
    """
    if not schedule:
        return 0.0
    
    # Calculate various scores
    workload_balance = check_balanced_workload(schedule, resources)
    
    # Calculate priority scores
    priority_score = 0.0
    for task_id, assignment in schedule.items():
        start_time = (assignment.get('start_day'), assignment.get('start_hour'))
        priority_score += check_task_priority(task_id, start_time, schedule, tasks)
    
    # Calculate preferred resource score
    preferred_score = 0.0
    for task_id, assignment in schedule.items():
        resource_id = assignment.get('resource_id')
        if check_preferred_resources(task_id, resource_id, tasks):
            preferred_score += 1.0
    
    # Normalize scores
    max_priority_score = len(schedule) * 3.0  # Assuming max priority weight is 3.0
    max_preferred_score = len(schedule)
    
    normalized_priority = priority_score / max_priority_score if max_priority_score > 0 else 0
    normalized_preferred = preferred_score / max_preferred_score if max_preferred_score > 0 else 0
    
    # Combine scores (weights can be adjusted)
    total_score = (0.4 * workload_balance + 
                   0.4 * normalized_priority + 
                   0.2 * normalized_preferred)
    
    return total_score 