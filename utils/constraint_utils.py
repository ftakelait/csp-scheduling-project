"""
Constraint Utilities for CSP Scheduling Project
Functions for checking various types of constraints in scheduling problems
"""

from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

def get_constraint_violations(assignment: Dict[str, Any], task_id: str, 
                            resources: List[Dict], tasks: List[Dict], 
                            solution: Dict[str, Any]) -> List[str]:
    """
    Check for constraint violations in a task assignment
    
    Args:
        assignment: Task assignment dictionary
        task_id: ID of the task being checked
        resources: List of resource dictionaries
        tasks: List of task dictionaries
        solution: Complete solution dictionary
        
    Returns:
        List of violation messages
    """
    violations = []
    
    # Find the task and resource
    task = next((t for t in tasks if t['id'] == task_id), None)
    resource = next((r for r in resources if r['id'] == assignment['resource_id']), None)
    
    if not task or not resource:
        violations.append(f"Invalid task or resource reference")
        return violations
    
    # Check resource skills
    required_skills = task.get('required_skills', [])
    resource_skills = resource.get('skills', [])
    
    if required_skills:
        missing_skills = [skill for skill in required_skills if skill not in resource_skills]
        if missing_skills:
            violations.append(f"Resource {resource['name']} missing skills: {missing_skills}")
    
    # Check resource capacity
    max_hours = resource.get('max_hours_per_day', 8)
    if assignment['duration'] > max_hours:
        violations.append(f"Task duration ({assignment['duration']}h) exceeds resource capacity ({max_hours}h)")
    
    # Check time conflicts with other assignments
    conflicts = check_time_conflicts(assignment, task_id, solution)
    violations.extend(conflicts)
    
    # Check dependency constraints
    dep_violations = check_dependency_constraints(assignment, task, solution)
    violations.extend(dep_violations)
    
    return violations

def check_time_conflicts(assignment: Dict[str, Any], task_id: str, 
                        solution: Dict[str, Any]) -> List[str]:
    """
    Check for time conflicts with other assignments
    
    Args:
        assignment: Task assignment
        task_id: ID of the task being checked
        solution: Complete solution
        
    Returns:
        List of conflict messages
    """
    conflicts = []
    
    resource_id = assignment['resource_id']
    start_hour = assignment['start_hour']
    end_hour = assignment['end_hour']
    day = assignment['start_day']
    
    for other_task_id, other_assignment in solution.items():
        if other_task_id == task_id:
            continue
        
        if (other_assignment['resource_id'] == resource_id and 
            other_assignment['start_day'] == day):
            
            # Check for overlap
            other_start = other_assignment['start_hour']
            other_end = other_assignment['end_hour']
            
            if not (end_hour <= other_start or start_hour >= other_end):
                conflicts.append(f"Time conflict with task {other_task_id}")
    
    return conflicts

def check_dependency_constraints(assignment: Dict[str, Any], task: Dict[str, Any], 
                                solution: Dict[str, Any]) -> List[str]:
    """
    Check dependency constraints
    
    Args:
        assignment: Task assignment
        task: Task dictionary
        solution: Complete solution
        
    Returns:
        List of dependency violation messages
    """
    violations = []
    
    dependencies = task.get('dependencies', [])
    
    for dep_id in dependencies:
        if dep_id not in solution:
            violations.append(f"Dependency {dep_id} not scheduled")
        else:
            # Check if dependency is completed before this task
            dep_assignment = solution[dep_id]
            
            # Simple check: dependency should be on an earlier day or same day but earlier time
            if dep_assignment['start_day'] > assignment['start_day']:
                violations.append(f"Dependency {dep_id} scheduled after dependent task")
            elif (dep_assignment['start_day'] == assignment['start_day'] and 
                  dep_assignment['end_hour'] > assignment['start_hour']):
                violations.append(f"Dependency {dep_id} overlaps with dependent task")
    
    return violations

def calculate_schedule_score(solution: Dict[str, Any], tasks: List[Dict], 
                           resources: List[Dict]) -> float:
    """
    Calculate a quality score for the schedule
    
    Args:
        solution: Complete solution dictionary
        tasks: List of task dictionaries
        resources: List of resource dictionaries
        
    Returns:
        Quality score between 0 and 1
    """
    if not solution:
        return 0.0
    
    # Calculate various metrics
    total_tasks = len(tasks)
    scheduled_tasks = len(solution)
    
    # Task completion rate
    completion_rate = scheduled_tasks / total_tasks if total_tasks > 0 else 0
    
    # Resource utilization
    resource_hours = {}
    for assignment in solution.values():
        resource_id = assignment['resource_id']
        duration = assignment['duration']
        resource_hours[resource_id] = resource_hours.get(resource_id, 0) + duration
    
    # Calculate average utilization
    total_hours = sum(resource_hours.values())
    max_possible_hours = len(resources) * 8 * 5  # 8 hours/day, 5 days
    utilization_rate = total_hours / max_possible_hours if max_possible_hours > 0 else 0
    
    # Constraint violation penalty
    violation_penalty = 0
    for task_id, assignment in solution.items():
        violations = get_constraint_violations(assignment, task_id, resources, tasks, solution)
        violation_penalty += len(violations) * 0.1  # 0.1 penalty per violation
    
    # Calculate final score
    score = (completion_rate * 0.4 + 
             utilization_rate * 0.4 + 
             max(0, 1 - violation_penalty) * 0.2)
    
    return min(1.0, max(0.0, score))

def check_resource_availability(resource_id: str, day: str, hour: int, 
                              resources: List[Dict]) -> bool:
    """
    Check if a resource is available at a specific time slot
    
    Args:
        resource_id: ID of the resource
        day: Day of the week
        hour: Hour of the day
        resources: List of resource dictionaries
        
    Returns:
        True if resource is available, False otherwise
    """
    for resource in resources:
        if resource['id'] == resource_id:
            availability = resource.get('availability', {})
            if day in availability and hour in availability[day]:
                return True
    return False

def get_resource_utilization(resource_id: str, solution: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate utilization metrics for a specific resource
    
    Args:
        resource_id: ID of the resource
        solution: Complete solution
        
    Returns:
        Dictionary with utilization metrics
    """
    total_hours = 0
    assignments = []
    
    for task_id, assignment in solution.items():
        if assignment['resource_id'] == resource_id:
            total_hours += assignment['duration']
            assignments.append({
                'task_id': task_id,
                'day': assignment['start_day'],
                'start_hour': assignment['start_hour'],
                'end_hour': assignment['end_hour'],
                'duration': assignment['duration']
            })
    
    return {
        'resource_id': resource_id,
        'total_hours': total_hours,
        'max_hours': 8 * 5,  # 8 hours/day, 5 days
        'utilization_rate': total_hours / (8 * 5),
        'assignments': assignments
    }

def validate_solution_completeness(solution: Dict[str, Any], tasks: List[Dict]) -> Dict[str, Any]:
    """
    Validate that all required tasks are scheduled
    
    Args:
        solution: Complete solution
        tasks: List of all tasks
        
    Returns:
        Dictionary with validation results
    """
    task_ids = {task['id'] for task in tasks}
    scheduled_ids = set(solution.keys())
    
    missing_tasks = task_ids - scheduled_ids
    extra_tasks = scheduled_ids - task_ids
    
    return {
        'complete': len(missing_tasks) == 0,
        'missing_tasks': list(missing_tasks),
        'extra_tasks': list(extra_tasks),
        'total_tasks': len(tasks),
        'scheduled_tasks': len(solution),
        'completion_rate': len(solution) / len(tasks) if len(tasks) > 0 else 0
    }

def check_task_dependencies(task_id: str, start_time: Dict, 
                           schedule: Dict, tasks: List[Dict]) -> bool:
    """
    Check if all dependencies of a task are completed before its start time
    
    Args:
        task_id: ID of the task
        start_time: Start time dictionary with 'day' and 'hour' keys
        schedule: Current schedule assignments
        tasks: List of task dictionaries
        
    Returns:
        True if dependencies are satisfied, False otherwise
    """
    # Find the task and its dependencies
    task = None
    for t in tasks:
        if t['id'] == task_id:
            task = t
            break
    
    if not task:
        return False
    
    dependencies = task.get('dependencies', [])
    
    # Check if all dependencies are completed
    for dep_id in dependencies:
        if dep_id not in schedule:
            return False
        
        dep_assignment = schedule[dep_id]
        dep_end_time = {
            'day': dep_assignment['start_day'],
            'hour': dep_assignment['end_hour']
        }
        
        # Check if dependency ends before this task starts
        if not _time_before(dep_end_time, start_time):
            return False
    
    return True

def check_resource_skills(resource_id: str, task_id: str, 
                         resources: List[Dict], tasks: List[Dict]) -> bool:
    """
    Check if a resource has the required skills for a task
    
    Args:
        resource_id: ID of the resource
        task_id: ID of the task
        resources: List of resource dictionaries
        tasks: List of task dictionaries
        
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
    
    required_skills = task.get('required_skills', [])
    resource_skills = resource.get('skills', [])
    
    return all(skill in resource_skills for skill in required_skills)

def check_max_hours_per_day(resource_id: str, day: str, schedule: Dict,
                           resources: List[Dict]) -> bool:
    """
    Check if a resource exceeds their maximum hours per day
    
    Args:
        resource_id: ID of the resource
        day: Day of the week
        schedule: Current schedule assignments
        resources: List of resource dictionaries
        
    Returns:
        True if within limits, False otherwise
    """
    # Find the resource's max hours
    max_hours = 8  # Default
    for resource in resources:
        if resource['id'] == resource_id:
            max_hours = resource.get('max_hours_per_day', 8)
            break
    
    # Calculate total hours for this resource on this day
    total_hours = 0
    for task_id, assignment in schedule.items():
        if (assignment.get('resource_id') == resource_id and 
            assignment.get('start_day') == day):
            total_hours += assignment.get('duration', 0)
    
    return total_hours <= max_hours

def check_preferred_resources(task_id: str, resource_id: str, 
                            tasks: List[Dict]) -> bool:
    """
    Check if a task is assigned to one of its preferred resources
    
    Args:
        task_id: ID of the task
        resource_id: ID of the resource
        tasks: List of task dictionaries
        
    Returns:
        True if resource is preferred, False otherwise
    """
    for task in tasks:
        if task['id'] == task_id:
            preferred_resources = task.get('preferred_resources', [])
            return resource_id in preferred_resources
    return False

def check_task_priority(task_id: str, start_time: Dict, schedule: Dict,
                       tasks: List[Dict]) -> float:
    """
    Check if higher priority tasks are scheduled earlier
    
    Args:
        task_id: ID of the task
        start_time: Start time dictionary
        schedule: Current schedule assignments
        tasks: List of task dictionaries
        
    Returns:
        Score based on priority scheduling (higher is better)
    """
    # Find the task's priority
    task_priority = 'medium'  # Default
    for task in tasks:
        if task['id'] == task_id:
            task_priority = task.get('priority', 'medium')
            break
    
    # Priority weights
    priority_weights = {'high': 3, 'medium': 2, 'low': 1}
    weight = priority_weights.get(task_priority, 1)
    
    # Calculate score based on start time (earlier is better)
    # This is a simplified scoring - in practice, you'd want more sophisticated logic
    day_order = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4}
    day_score = day_order.get(start_time.get('day', 'monday'), 0)
    hour_score = start_time.get('hour', 9)
    
    return weight * (5 - day_score) * (18 - hour_score)

def check_balanced_workload(schedule: Dict, resources: List[Dict]) -> float:
    """
    Calculate workload balance among all resources
    
    Args:
        schedule: Current schedule assignments
        resources: List of resource dictionaries
        
    Returns:
        Balance score (higher is better)
    """
    # Calculate workload for each resource
    workloads = defaultdict(int)
    for task_id, assignment in schedule.items():
        resource_id = assignment.get('resource_id')
        duration = assignment.get('duration', 0)
        workloads[resource_id] += duration
    
    if not workloads:
        return 0.0
    
    # Calculate variance in workloads
    values = list(workloads.values())
    mean_workload = sum(values) / len(values)
    variance = sum((x - mean_workload) ** 2 for x in values) / len(values)
    
    # Convert to a score (lower variance = higher score)
    max_possible_variance = 100  # Arbitrary maximum
    balance_score = max(0, 1 - (variance / max_possible_variance))
    
    return balance_score

def _time_before(time1: Dict, time2: Dict) -> bool:
    """
    Helper function to compare two times
    
    Args:
        time1: First time dictionary with 'day' and 'hour' keys
        time2: Second time dictionary with 'day' and 'hour' keys
        
    Returns:
        True if time1 is before time2, False otherwise
    """
    day_order = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4}
    
    day1 = day_order.get(time1.get('day', 'monday'), 0)
    day2 = day_order.get(time2.get('day', 'monday'), 0)
    
    if day1 < day2:
        return True
    elif day1 > day2:
        return False
    else:
        return time1.get('hour', 0) < time2.get('hour', 0) 