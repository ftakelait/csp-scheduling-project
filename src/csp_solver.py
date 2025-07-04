"""
CSP Solver Implementation
Core Constraint Satisfaction Problem solver for scheduling

Students need to implement the core CSP solving functionality.
"""

import time
import random
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict

class SchedulingCSP:
    """
    Constraint Satisfaction Problem solver for scheduling tasks to resources
    """
    
    def __init__(self, tasks: List[Dict], resources: List[Dict], 
                 time_slots: Dict, constraints: Dict):
        """
        Initialize the CSP solver
        
        Args:
            tasks: List of task dictionaries
            resources: List of resource dictionaries
            time_slots: Dictionary with time slot information
            constraints: Dictionary with hard and soft constraints
        """
        self.tasks = tasks
        self.resources = resources
        self.time_slots = time_slots
        self.constraints = constraints
        
        # CSP components to be initialized
        self.variables = []
        self.domains = {}
        self.constraint_graph = {}
        
        # Initialize the CSP
        self._initialize_csp()
    
    def _initialize_csp(self):
        """
        Initialize the CSP variables, domains, and constraints
        """
        # Create variables (one for each task)
        self.variables = [task['id'] for task in self.tasks]
        
        # Create domains (possible assignments for each task)
        self.domains = {}
        for task in self.tasks:
            task_id = task['id']
            domain = []
            
            # Generate possible assignments
            for resource in self.resources:
                for day in self.time_slots['days']:
                    for hour in self.time_slots['hours']:
                        # Check if assignment is valid
                        if self._is_valid_assignment(task, resource, day, hour):
                            assignment = {
                                'task_id': task_id,
                                'task_name': task['name'],
                                'resource_id': resource['id'],
                                'resource_name': resource['name'],
                                'start_day': day,
                                'start_hour': hour,
                                'end_hour': hour + task['duration'],
                                'duration': task['duration']
                            }
                            domain.append(assignment)
            
            self.domains[task_id] = domain
        
        # Create constraint graph
        self._build_constraint_graph()
    
    def _is_valid_assignment(self, task: Dict, resource: Dict, day: str, hour: int) -> bool:
        """
        Check if a task-resource-time assignment is valid
        
        Args:
            task: Task dictionary
            resource: Resource dictionary
            day: Day of the week
            hour: Starting hour
            
        Returns:
            True if assignment is valid, False otherwise
        """
        # Check if resource has required skills
        required_skills = task.get('required_skills', [])
        resource_skills = resource.get('skills', [])
        
        if required_skills and not all(skill in resource_skills for skill in required_skills):
            return False
        
        # Check if assignment fits within working hours
        end_hour = hour + task['duration']
        if end_hour > self.time_slots['working_hours_per_day']:
            return False
        
        # Check resource availability (simplified)
        max_hours = resource.get('max_hours_per_day', 8)
        if task['duration'] > max_hours:
            return False
        
        return True
    
    def _build_constraint_graph(self):
        """
        Build the constraint graph between variables
        """
        self.constraint_graph = defaultdict(list)
        
        # Add constraints based on task dependencies
        for task in self.tasks:
            task_id = task['id']
            dependencies = task.get('dependencies', [])
            
            for dep_id in dependencies:
                if dep_id in self.variables:
                    self.constraint_graph[task_id].append(dep_id)
                    self.constraint_graph[dep_id].append(task_id)
        
        # Add resource capacity constraints
        for resource in self.resources:
            resource_tasks = [task for task in self.tasks 
                            if any(skill in resource.get('skills', []) 
                                  for skill in task.get('required_skills', []))]
            
            for i, task1 in enumerate(resource_tasks):
                for task2 in resource_tasks[i+1:]:
                    if task1['id'] in self.variables and task2['id'] in self.variables:
                        self.constraint_graph[task1['id']].append(task2['id'])
                        self.constraint_graph[task2['id']].append(task1['id'])
    
    def solve(self, heuristic: str = 'mrv', use_arc_consistency: bool = True, 
              timeout: int = 60) -> Optional[Dict]:
        """
        Solve the CSP using backtracking search
        
        Args:
            heuristic: Variable ordering heuristic ('mrv', 'degree', 'combined')
            use_arc_consistency: Whether to use arc consistency preprocessing
            timeout: Maximum time to spend solving (seconds)
            
        Returns:
            Solution dictionary or None if no solution found
        """
        start_time = time.time()
        
        # Create a copy of domains for solving
        domains = {var: list(domain) for var, domain in self.domains.items()}
        
        # Apply arc consistency if requested
        if use_arc_consistency:
            domains = self._apply_arc_consistency(domains)
        
        # Initialize assignment
        assignment = {}
        
        # Solve using backtracking
        solution = self._backtrack(assignment, domains, heuristic, start_time, timeout)
        
        if solution:
            # Convert to the expected format
            result = {}
            for task_id, assignment in solution.items():
                result[task_id] = assignment
            return result
        
        return None
    
    def _apply_arc_consistency(self, domains: Dict) -> Dict:
        """
        Apply arc consistency to reduce domain sizes
        
        Args:
            domains: Current domains
            
        Returns:
            Reduced domains
        """
        # Simplified arc consistency implementation
        # In a full implementation, this would use AC-3 algorithm
        
        reduced_domains = domains.copy()
        
        # Remove assignments that violate hard constraints
        for var in self.variables:
            if var in reduced_domains:
                valid_assignments = []
                for assignment in reduced_domains[var]:
                    if self._check_constraints(assignment, var):
                        valid_assignments.append(assignment)
                reduced_domains[var] = valid_assignments
        
        return reduced_domains
    
    def _check_constraints(self, assignment: Dict, task_id: str) -> bool:
        """
        Check if an assignment satisfies all constraints
        
        Args:
            assignment: Task assignment
            task_id: ID of the task being assigned
            
        Returns:
            True if constraints are satisfied, False otherwise
        """
        # Check resource capacity constraints
        resource_id = assignment['resource_id']
        start_hour = assignment['start_hour']
        end_hour = assignment['end_hour']
        day = assignment['start_day']
        
        # Check if resource is available during this time
        # This is a simplified check - in practice, you'd check against other assignments
        
        # Check dependency constraints
        task = next(t for t in self.tasks if t['id'] == task_id)
        dependencies = task.get('dependencies', [])
        
        # For now, we'll assume dependencies are satisfied
        # In a full implementation, you'd check that dependent tasks are completed first
        
        return True
    
    def _backtrack(self, assignment: Dict, domains: Dict, heuristic: str,
                   start_time: float, timeout: int) -> Optional[Dict]:
        """
        Backtracking search implementation
        
        Args:
            assignment: Current partial assignment
            domains: Current domains
            heuristic: Variable ordering heuristic
            start_time: When solving started
            timeout: Maximum time to spend
            
        Returns:
            Complete assignment or None
        """
        # Check timeout
        if time.time() - start_time > timeout:
            return None
        
        # If all variables are assigned, we have a solution
        if len(assignment) == len(self.variables):
            return assignment
        
        # Select next variable using heuristic
        var = self._select_variable(assignment, domains, heuristic)
        if var is None:
            return None
        
        # Try each value in the variable's domain
        for value in domains[var]:
            # Check if this assignment is consistent
            if self._is_consistent(assignment, var, value):
                # Make the assignment
                assignment[var] = value
                
                # Recursively solve the rest
                result = self._backtrack(assignment, domains, heuristic, start_time, timeout)
                if result is not None:
                    return result
                
                # Backtrack
                del assignment[var]
        
        return None
    
    def _select_variable(self, assignment: Dict, domains: Dict, heuristic: str) -> Optional[str]:
        """
        Select the next variable to assign using the specified heuristic
        
        Args:
            assignment: Current partial assignment
            domains: Current domains
            heuristic: Heuristic to use
            
        Returns:
            Selected variable or None
        """
        unassigned = [var for var in self.variables if var not in assignment]
        
        if not unassigned:
            return None
        
        if heuristic == 'mrv':
            return self._mrv_heuristic(unassigned, domains)
        elif heuristic == 'degree':
            return self._degree_heuristic(unassigned, domains)
        elif heuristic == 'combined':
            return self._combined_heuristic(unassigned, domains)
        else:
            # Default to first unassigned variable
            return unassigned[0]
    
    def _mrv_heuristic(self, variables: List[str], domains: Dict) -> str:
        """
        Minimum Remaining Values heuristic
        """
        min_values = float('inf')
        selected_var = variables[0]
        
        for var in variables:
            if var in domains and len(domains[var]) < min_values:
                min_values = len(domains[var])
                selected_var = var
        
        return selected_var
    
    def _degree_heuristic(self, variables: List[str], domains: Dict) -> str:
        """
        Degree heuristic
        """
        max_degree = -1
        selected_var = variables[0]
        
        for var in variables:
            degree = len(self.constraint_graph.get(var, []))
            if degree > max_degree:
                max_degree = degree
                selected_var = var
        
        return selected_var
    
    def _combined_heuristic(self, variables: List[str], domains: Dict) -> str:
        """
        Combined heuristic (MRV + Degree tiebreaker)
        """
        # Find variables with minimum remaining values
        min_values = float('inf')
        mrv_vars = []
        
        for var in variables:
            if var in domains:
                num_values = len(domains[var])
                if num_values < min_values:
                    min_values = num_values
                    mrv_vars = [var]
                elif num_values == min_values:
                    mrv_vars.append(var)
        
        # If only one MRV variable, return it
        if len(mrv_vars) == 1:
            return mrv_vars[0]
        
        # Otherwise, use degree heuristic as tiebreaker
        max_degree = -1
        selected_var = mrv_vars[0]
        
        for var in mrv_vars:
            degree = len(self.constraint_graph.get(var, []))
            if degree > max_degree:
                max_degree = degree
                selected_var = var
        
        return selected_var
    
    def _is_consistent(self, assignment: Dict, var: str, value: Dict) -> bool:
        """
        Check if an assignment is consistent with current partial assignment
        
        Args:
            assignment: Current partial assignment
            var: Variable being assigned
            value: Value being assigned
            
        Returns:
            True if consistent, False otherwise
        """
        # Check resource conflicts
        resource_id = value['resource_id']
        start_hour = value['start_hour']
        end_hour = value['end_hour']
        day = value['start_day']
        
        for assigned_var, assigned_value in assignment.items():
            if (assigned_value['resource_id'] == resource_id and
                assigned_value['start_day'] == day):
                # Check for time overlap
                if not (end_hour <= assigned_value['start_hour'] or 
                       start_hour >= assigned_value['end_hour']):
                    return False
        
        return True 