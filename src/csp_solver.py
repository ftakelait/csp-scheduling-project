"""
CSP Solver for Scheduling Problems
Implements backtracking search with various heuristics and constraint propagation
"""

import time
from typing import Dict, List, Any, Set, Tuple, Optional, Callable
from collections import defaultdict
import random


class CSPVariable:
    """Represents a variable in the CSP"""
    
    def __init__(self, name: str, domain: List[Any]):
        self.name = name
        self.domain = domain.copy()
        self.assigned_value = None
        self.constraints = []
    
    def assign(self, value: Any) -> None:
        """Assign a value to this variable"""
        self.assigned_value = value
    
    def unassign(self) -> None:
        """Remove the assignment from this variable"""
        self.assigned_value = None
    
    def is_assigned(self) -> bool:
        """Check if this variable has been assigned"""
        return self.assigned_value is not None
    
    def get_remaining_values(self) -> List[Any]:
        """Get the remaining unassigned values in the domain"""
        if self.is_assigned():
            return []
        return self.domain.copy()


class CSPConstraint:
    """Represents a constraint in the CSP"""
    
    def __init__(self, variables: List[str], constraint_func: Callable):
        self.variables = variables
        self.constraint_func = constraint_func
    
    def check(self, assignment: Dict[str, Any]) -> bool:
        """Check if the constraint is satisfied given the current assignment"""
        # Only check if all variables in this constraint are assigned
        if not all(var in assignment for var in self.variables):
            return True
        
        # Extract values for the variables in this constraint
        values = [assignment[var] for var in self.variables]
        return self.constraint_func(*values)


class CSPSolver:
    """Main CSP solver class"""
    
    def __init__(self, variables: Dict[str, List[Any]], constraints: List[CSPConstraint]):
        self.variables = {name: CSPVariable(name, domain) for name, domain in variables.items()}
        self.constraints = constraints
        self.assignment = {}
        self.backtrack_count = 0
        self.start_time = None
        
        # Add constraints to variables
        for constraint in constraints:
            for var_name in constraint.variables:
                if var_name in self.variables:
                    self.variables[var_name].constraints.append(constraint)
    
    def solve(self, heuristic: str = "mrv", use_arc_consistency: bool = True, 
              timeout: int = 300) -> Optional[Dict[str, Any]]:
        """
        Solve the CSP using backtracking search
        
        Args:
            heuristic: Variable ordering heuristic ("mrv", "degree", "combined")
            use_arc_consistency: Whether to use arc consistency
            timeout: Maximum time to spend solving (seconds)
            
        Returns:
            Solution assignment or None if no solution found
        """
        self.start_time = time.time()
        self.backtrack_count = 0
        
        # Apply arc consistency if requested
        if use_arc_consistency:
            if not self.arc_consistency():
                return None
        
        # Start backtracking search
        solution = self.backtrack_search(heuristic, timeout)
        
        if solution:
            print(f"Solution found in {time.time() - self.start_time:.2f} seconds")
            print(f"Backtrack count: {self.backtrack_count}")
        else:
            print(f"No solution found after {time.time() - self.start_time:.2f} seconds")
            print(f"Backtrack count: {self.backtrack_count}")
        
        return solution
    
    def backtrack_search(self, heuristic: str, timeout: int) -> Optional[Dict[str, Any]]:
        """
        Recursive backtracking search
        
        Args:
            heuristic: Variable ordering heuristic
            timeout: Maximum time to spend solving
            
        Returns:
            Solution assignment or None
        """
        # Check timeout
        if time.time() - self.start_time > timeout:
            return None
        
        # Check if all variables are assigned
        if len(self.assignment) == len(self.variables):
            return self.assignment.copy()
        
        # Select next variable using heuristic
        var_name = self.select_variable(heuristic)
        if var_name is None:
            return None
        
        variable = self.variables[var_name]
        
        # Try each value in the variable's domain
        for value in variable.get_remaining_values():
            # Check if this assignment is consistent
            if self.is_consistent(var_name, value):
                # Make the assignment
                variable.assign(value)
                self.assignment[var_name] = value
                
                # Recursively try to assign the remaining variables
                result = self.backtrack_search(heuristic, timeout)
                if result is not None:
                    return result
                
                # Backtrack
                variable.unassign()
                del self.assignment[var_name]
                self.backtrack_count += 1
        
        return None
    
    def select_variable(self, heuristic: str) -> Optional[str]:
        """
        Select the next variable to assign using the specified heuristic
        
        Args:
            heuristic: Variable ordering heuristic
            
        Returns:
            Name of the selected variable or None if no unassigned variables
        """
        unassigned = [name for name, var in self.variables.items() if not var.is_assigned()]
        
        if not unassigned:
            return None
        
        if heuristic == "mrv":
            return self.select_mrv_variable(unassigned)
        elif heuristic == "degree":
            return self.select_degree_variable(unassigned)
        elif heuristic == "combined":
            return self.select_combined_variable(unassigned)
        else:
            return random.choice(unassigned)
    
    def select_mrv_variable(self, unassigned: List[str]) -> str:
        """
        Select variable with Minimum Remaining Values
        
        Args:
            unassigned: List of unassigned variable names
            
        Returns:
            Variable name with fewest remaining values
        """
        min_values = float('inf')
        selected_var = unassigned[0]
        
        for var_name in unassigned:
            variable = self.variables[var_name]
            remaining_values = len(variable.get_remaining_values())
            
            if remaining_values < min_values:
                min_values = remaining_values
                selected_var = var_name
        
        return selected_var
    
    def select_degree_variable(self, unassigned: List[str]) -> str:
        """
        Select variable with highest degree (most constraints on remaining variables)
        
        Args:
            unassigned: List of unassigned variable names
            
        Returns:
            Variable name with highest degree
        """
        max_degree = -1
        selected_var = unassigned[0]
        
        for var_name in unassigned:
            variable = self.variables[var_name]
            degree = 0
            
            # Count constraints that involve other unassigned variables
            for constraint in variable.constraints:
                for other_var in constraint.variables:
                    if other_var != var_name and other_var in unassigned:
                        degree += 1
            
            if degree > max_degree:
                max_degree = degree
                selected_var = var_name
        
        return selected_var
    
    def select_combined_variable(self, unassigned: List[str]) -> str:
        """
        Select variable using MRV, breaking ties with degree heuristic
        
        Args:
            unassigned: List of unassigned variable names
            
        Returns:
            Variable name selected by combined heuristic
        """
        # First, find variables with minimum remaining values
        min_values = float('inf')
        mrv_vars = []
        
        for var_name in unassigned:
            variable = self.variables[var_name]
            remaining_values = len(variable.get_remaining_values())
            
            if remaining_values < min_values:
                min_values = remaining_values
                mrv_vars = [var_name]
            elif remaining_values == min_values:
                mrv_vars.append(var_name)
        
        # If only one variable has minimum remaining values, return it
        if len(mrv_vars) == 1:
            return mrv_vars[0]
        
        # Otherwise, break ties using degree heuristic
        max_degree = -1
        selected_var = mrv_vars[0]
        
        for var_name in mrv_vars:
            variable = self.variables[var_name]
            degree = 0
            
            for constraint in variable.constraints:
                for other_var in constraint.variables:
                    if other_var != var_name and other_var in unassigned:
                        degree += 1
            
            if degree > max_degree:
                max_degree = degree
                selected_var = var_name
        
        return selected_var
    
    def is_consistent(self, var_name: str, value: Any) -> bool:
        """
        Check if assigning the given value to the variable is consistent
        
        Args:
            var_name: Name of the variable
            value: Value to assign
            
        Returns:
            True if assignment is consistent, False otherwise
        """
        # Create a temporary assignment including the new value
        temp_assignment = self.assignment.copy()
        temp_assignment[var_name] = value
        
        # Check all constraints
        for constraint in self.constraints:
            if not constraint.check(temp_assignment):
                return False
        
        return True
    
    def arc_consistency(self) -> bool:
        """
        Apply arc consistency to reduce domains
        
        Returns:
            True if arc consistency was successful, False if domain became empty
        """
        # Create a queue of all arcs (variable-constraint pairs)
        queue = []
        for var_name, variable in self.variables.items():
            for constraint in variable.constraints:
                for other_var in constraint.variables:
                    if other_var != var_name:
                        queue.append((var_name, other_var, constraint))
        
        # Process the queue
        while queue:
            var1, var2, constraint = queue.pop(0)
            
            if self.revise_domain(var1, var2, constraint):
                # If domain of var1 was revised, add all arcs involving var1 back to queue
                if len(self.variables[var1].domain) == 0:
                    return False
                
                for other_constraint in self.variables[var1].constraints:
                    for other_var in other_constraint.variables:
                        if other_var != var1 and other_var != var2:
                            queue.append((other_var, var1, other_constraint))
        
        return True
    
    def revise_domain(self, var1: str, var2: str, constraint: CSPConstraint) -> bool:
        """
        Revise the domain of var1 based on constraint with var2
        
        Args:
            var1: First variable
            var2: Second variable
            constraint: Constraint between the variables
            
        Returns:
            True if domain was revised, False otherwise
        """
        revised = False
        domain1 = self.variables[var1].domain.copy()
        
        for value1 in domain1:
            # Check if there's any value in var2's domain that satisfies the constraint
            has_support = False
            
            for value2 in self.variables[var2].domain:
                # Create temporary assignment
                temp_assignment = {var1: value1, var2: value2}
                
                # Check if constraint is satisfied
                if constraint.check(temp_assignment):
                    has_support = True
                    break
            
            # If no support found, remove value1 from domain
            if not has_support:
                self.variables[var1].domain.remove(value1)
                revised = True
        
        return revised
    
    def get_solution_quality(self, solution: Dict[str, Any]) -> float:
        """
        Calculate the quality score of a solution
        
        Args:
            solution: The solution assignment
            
        Returns:
            Quality score (higher is better)
        """
        if not solution:
            return 0.0
        
        # This is a placeholder - actual quality calculation would depend on the problem
        # For scheduling problems, you might consider:
        # - Number of constraint violations
        # - Resource utilization balance
        # - Task completion time
        # - Priority satisfaction
        
        return 1.0  # Placeholder score


class SchedulingCSP:
    """Specialized CSP for scheduling problems"""
    
    def __init__(self, tasks: List[Dict], resources: List[Dict], 
                 time_slots: Dict[str, Any], constraints: Dict[str, Any]):
        self.tasks = tasks
        self.resources = resources
        self.time_slots = time_slots
        self.constraints = constraints
        self.solver = None
        
    def create_csp(self) -> CSPSolver:
        """
        Create a CSP instance for the scheduling problem
        
        Returns:
            Configured CSP solver
        """
        # Create variables (one for each task)
        variables = {}
        for task in self.tasks:
            task_id = task['id']
            # Domain: all possible (resource, day, hour) combinations
            domain = self.create_domain_for_task(task)
            variables[task_id] = domain
        
        # Create constraints
        constraint_list = []
        
        # Add hard constraints
        constraint_list.extend(self.create_hard_constraints())
        
        # Add soft constraints (these will be handled in quality evaluation)
        
        self.solver = CSPSolver(variables, constraint_list)
        return self.solver
    
    def create_domain_for_task(self, task: Dict) -> List[Tuple[str, str, int]]:
        """
        Create the domain for a task (all possible assignments)
        
        Args:
            task: Task dictionary
            
        Returns:
            List of possible (resource_id, day, hour) assignments
        """
        domain = []
        days = self.time_slots['days']
        hours = self.time_slots['hours']
        duration = task['duration']
        
        # For each resource that has the required skills
        for resource in self.resources:
            if self.has_required_skills(resource, task):
                # For each day
                for day in days:
                    # For each possible start hour
                    for start_hour in hours:
                        # Check if the task can fit in the remaining hours
                        if start_hour + duration <= max(hours) + 1:
                            domain.append((resource['id'], day, start_hour))
        
        return domain
    
    def has_required_skills(self, resource: Dict, task: Dict) -> bool:
        """
        Check if a resource has the required skills for a task
        
        Args:
            resource: Resource dictionary
            task: Task dictionary
            
        Returns:
            True if resource has required skills
        """
        required_skills = set(task.get('required_skills', []))
        resource_skills = set(resource.get('skills', []))
        return required_skills.issubset(resource_skills)
    
    def create_hard_constraints(self) -> List[CSPConstraint]:
        """
        Create hard constraints for the scheduling problem
        
        Returns:
            List of hard constraints
        """
        constraints = []
        
        # No resource overlap constraint
        def no_overlap(task1_id, task2_id, assignment):
            if task1_id == task2_id:
                return True
            
            task1_assignment = assignment.get(task1_id)
            task2_assignment = assignment.get(task2_id)
            
            if not task1_assignment or not task2_assignment:
                return True
            
            resource1, day1, hour1 = task1_assignment
            resource2, day2, hour2 = task2_assignment
            
            # If different resources, no overlap
            if resource1 != resource2:
                return True
            
            # If different days, no overlap
            if day1 != day2:
                return True
            
            # Check for time overlap
            task1 = next(t for t in self.tasks if t['id'] == task1_id)
            task2 = next(t for t in self.tasks if t['id'] == task2_id)
            
            duration1 = task1['duration']
            duration2 = task2['duration']
            
            end1 = hour1 + duration1
            end2 = hour2 + duration2
            
            return not (hour1 < end2 and hour2 < end1)
        
        # Add no-overlap constraints for all pairs of tasks
        for i, task1 in enumerate(self.tasks):
            for j, task2 in enumerate(self.tasks):
                if i < j:  # Avoid duplicate constraints
                    constraint = CSPConstraint([task1['id'], task2['id']], no_overlap)
                    constraints.append(constraint)
        
        return constraints
    
    def solve(self, heuristic: str = "mrv", use_arc_consistency: bool = True, 
              timeout: int = 300) -> Optional[Dict[str, Any]]:
        """
        Solve the scheduling CSP
        
        Args:
            heuristic: Variable ordering heuristic
            use_arc_consistency: Whether to use arc consistency
            timeout: Maximum time to spend solving
            
        Returns:
            Schedule solution or None
        """
        if self.solver is None:
            self.create_csp()
        
        solution = self.solver.solve(heuristic, use_arc_consistency, timeout)
        
        if solution:
            return self.format_solution(solution)
        
        return None
    
    def format_solution(self, raw_solution: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the raw CSP solution into a readable schedule
        
        Args:
            raw_solution: Raw solution from CSP solver
            
        Returns:
            Formatted schedule
        """
        schedule = {}
        
        for task_id, assignment in raw_solution.items():
            resource_id, day, hour = assignment
            
            # Find task details
            task = next(t for t in self.tasks if t['id'] == task_id)
            
            schedule[task_id] = {
                'task_name': task['name'],
                'resource_id': resource_id,
                'resource_name': next(r['name'] for r in self.resources if r['id'] == resource_id),
                'start_day': day,
                'start_hour': hour,
                'duration': task['duration'],
                'end_day': day,  # Assuming tasks don't span multiple days
                'end_hour': hour + task['duration'],
                'priority': task.get('priority', 'medium')
            }
        
        return schedule 