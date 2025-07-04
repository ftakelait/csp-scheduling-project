"""
Constraint Utilities for CSP Scheduling Project
Functions for checking constraints and calculating schedule metrics
"""

from typing import Dict, List, Any, Optional, Tuple

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

def check_resource_availability(resource_id: str, day: str, start_hour: int, 
                              end_hour: int, solution: Dict[str, Any]) -> bool:
    """
    Check if a resource is available during a specific time period
    
    Args:
        resource_id: ID of the resource
        day: Day of the week
        start_hour: Starting hour
        end_hour: Ending hour
        solution: Current solution
        
    Returns:
        True if resource is available, False otherwise
    """
    for assignment in solution.values():
        if (assignment['resource_id'] == resource_id and 
            assignment['start_day'] == day):
            
            # Check for overlap
            if not (end_hour <= assignment['start_hour'] or 
                   start_hour >= assignment['end_hour']):
                return False
    
    return True

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