"""
Scheduler Module for CSP Scheduling Project
High-level scheduling problem management and solving
"""

import time
from typing import Dict, List, Any, Optional, Tuple
from .csp_solver import SchedulingCSP
from utils.constraint_utils import (
    get_constraint_violations, calculate_schedule_score, 
    validate_solution_completeness
)
from utils.file_utils import export_schedule_to_json, export_schedule_to_csv

class Scheduler:
    """
    High-level scheduler for managing CSP scheduling problems
    """
    
    def __init__(self, tasks: List[Dict], resources: List[Dict], 
                 time_slots: Dict, constraints: Dict):
        """
        Initialize the scheduler
        
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
        
        # Create CSP solver
        self.csp_solver = SchedulingCSP(tasks, resources, time_slots, constraints)
        
        # Solution storage
        self.solutions = {}
        self.current_solution = None
        self.performance_metrics = {}
    
    def solve(self, heuristic: str = 'mrv', use_arc_consistency: bool = True, 
              timeout: int = 60) -> Optional[Dict[str, Any]]:
        """
        Solve the scheduling problem
        
        Args:
            heuristic: Variable ordering heuristic
            use_arc_consistency: Whether to use arc consistency
            timeout: Maximum solving time in seconds
            
        Returns:
            Solution dictionary or None
        """
        start_time = time.time()
        
        solution = self.csp_solver.solve(
            heuristic=heuristic,
            use_arc_consistency=use_arc_consistency,
            timeout=timeout
        )
        
        solve_time = time.time() - start_time
        
        if solution:
            self.solutions[heuristic] = solution
            self.current_solution = solution
            
            # Calculate performance metrics
            self.performance_metrics[heuristic] = {
                'solve_time': solve_time,
                'tasks_scheduled': len(solution),
                'schedule_score': calculate_schedule_score(solution, self.tasks, self.resources)
            }
        
        return solution
    
    def solve_all_heuristics(self, heuristics: List[str] = None, 
                           timeout: int = 60) -> Dict[str, Dict[str, Any]]:
        """
        Solve using all available heuristics
        
        Args:
            heuristics: List of heuristics to try
            timeout: Maximum time per heuristic
            
        Returns:
            Dictionary of solutions by heuristic
        """
        if heuristics is None:
            heuristics = ['mrv', 'degree', 'combined']
        
        results = {}
        
        for heuristic in heuristics:
            print(f"Solving with {heuristic.upper()} heuristic...")
            solution = self.solve(heuristic=heuristic, timeout=timeout)
            
            if solution:
                results[heuristic] = solution
                print(f"  ✓ Solution found: {len(solution)} tasks scheduled")
            else:
                print(f"  ✗ No solution found")
        
        return results
    
    def get_best_solution(self, metric: str = 'schedule_score') -> Optional[Dict[str, Any]]:
        """
        Get the best solution based on a metric
        
        Args:
            metric: Metric to use for comparison ('schedule_score', 'solve_time', 'tasks_scheduled')
            
        Returns:
            Best solution or None
        """
        if not self.performance_metrics:
            return None
        
        best_heuristic = None
        best_value = None
        
        for heuristic, metrics in self.performance_metrics.items():
            value = metrics.get(metric, 0)
            
            if best_value is None:
                best_value = value
                best_heuristic = heuristic
            elif metric == 'solve_time':
                # For time, lower is better
                if value < best_value:
                    best_value = value
                    best_heuristic = heuristic
            else:
                # For other metrics, higher is better
                if value > best_value:
                    best_value = value
                    best_heuristic = heuristic
        
        return self.solutions.get(best_heuristic)
    
    def validate_solution(self, solution: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Validate a solution
        
        Args:
            solution: Solution to validate (uses current solution if None)
            
        Returns:
            Validation results
        """
        if solution is None:
            solution = self.current_solution
        
        if not solution:
            return {'valid': False, 'message': 'No solution to validate'}
        
        # Check completeness
        completeness = validate_solution_completeness(solution, self.tasks)
        
        # Check constraint violations
        violations = {}
        for task_id, assignment in solution.items():
            task_violations = get_constraint_violations(
                assignment, task_id, self.resources, self.tasks, solution
            )
            if task_violations:
                violations[task_id] = task_violations
        
        # Calculate overall validity
        is_valid = completeness['complete'] and len(violations) == 0
        
        return {
            'valid': is_valid,
            'complete': completeness,
            'violations': violations,
            'total_violations': sum(len(v) for v in violations.values()),
            'schedule_score': calculate_schedule_score(solution, self.tasks, self.resources)
        }
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Get a summary of performance across all heuristics
        
        Returns:
            Performance summary dictionary
        """
        if not self.performance_metrics:
            return {}
        
        summary = {
            'total_heuristics': len(self.performance_metrics),
            'successful_solves': len([m for m in self.performance_metrics.values() if m['tasks_scheduled'] > 0]),
            'best_schedule_score': max(m['schedule_score'] for m in self.performance_metrics.values()),
            'fastest_solve': min(m['solve_time'] for m in self.performance_metrics.values()),
            'most_tasks': max(m['tasks_scheduled'] for m in self.performance_metrics.values()),
            'heuristic_performance': self.performance_metrics
        }
        
        return summary
    
    def export_solution(self, solution: Dict[str, Any] = None, 
                       base_filename: str = 'solution') -> Dict[str, str]:
        """
        Export solution to multiple formats
        
        Args:
            solution: Solution to export (uses current solution if None)
            base_filename: Base filename for exports
            
        Returns:
            Dictionary of exported file paths
        """
        if solution is None:
            solution = self.current_solution
        
        if not solution:
            return {}
        
        exported_files = {}
        
        # Export to JSON
        json_filename = f"{base_filename}.json"
        export_schedule_to_json(solution, json_filename)
        exported_files['json'] = json_filename
        
        # Export to CSV
        csv_filename = f"{base_filename}.csv"
        export_schedule_to_csv(solution, csv_filename)
        exported_files['csv'] = csv_filename
        
        return exported_files
    
    def generate_report(self, solution: Dict[str, Any] = None) -> str:
        """
        Generate a text report for a solution
        
        Args:
            solution: Solution to report on (uses current solution if None)
            
        Returns:
            Formatted report string
        """
        if solution is None:
            solution = self.current_solution
        
        if not solution:
            return "No solution available for reporting."
        
        # Validate solution
        validation = self.validate_solution(solution)
        
        # Calculate metrics
        schedule_score = calculate_schedule_score(solution, self.tasks, self.resources)
        
        # Generate report
        report = []
        report.append("=" * 60)
        report.append("SCHEDULING SOLUTION REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Solution overview
        report.append("SOLUTION OVERVIEW:")
        report.append(f"  - Tasks scheduled: {len(solution)}")
        report.append(f"  - Total tasks available: {len(self.tasks)}")
        report.append(f"  - Completion rate: {len(solution)/len(self.tasks)*100:.1f}%")
        report.append(f"  - Schedule score: {schedule_score:.3f}")
        report.append("")
        
        # Validation results
        report.append("VALIDATION RESULTS:")
        report.append(f"  - Solution valid: {validation['valid']}")
        report.append(f"  - All tasks scheduled: {validation['complete']['complete']}")
        report.append(f"  - Constraint violations: {validation['total_violations']}")
        report.append("")
        
        # Task assignments
        report.append("TASK ASSIGNMENTS:")
        for task_id, assignment in solution.items():
            report.append(f"  {task_id}: {assignment['task_name']} -> {assignment['resource_name']}")
            report.append(f"    Time: {assignment['start_day']} {assignment['start_hour']}:00-{assignment['end_hour']}:00")
            report.append(f"    Duration: {assignment['duration']} hours")
            report.append("")
        
        # Resource utilization
        report.append("RESOURCE UTILIZATION:")
        resource_hours = {}
        for assignment in solution.values():
            resource_id = assignment['resource_id']
            duration = assignment['duration']
            resource_hours[resource_id] = resource_hours.get(resource_id, 0) + duration
        
        for resource in self.resources:
            hours = resource_hours.get(resource['id'], 0)
            max_hours = resource.get('max_hours_per_day', 8) * 5
            utilization = hours / max_hours * 100 if max_hours > 0 else 0
            report.append(f"  {resource['name']}: {hours}/{max_hours} hours ({utilization:.1f}%)")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def optimize_solution(self, solution: Dict[str, Any] = None, 
                         max_iterations: int = 100) -> Dict[str, Any]:
        """
        Optimize a solution by improving resource utilization
        
        Args:
            solution: Solution to optimize (uses current solution if None)
            max_iterations: Maximum optimization iterations
            
        Returns:
            Optimized solution
        """
        if solution is None:
            solution = self.current_solution
        
        if not solution:
            return {}
        
        # Simple optimization: try to balance resource utilization
        optimized = solution.copy()
        
        # Calculate current resource utilization
        resource_hours = {}
        for assignment in optimized.values():
            resource_id = assignment['resource_id']
            duration = assignment['duration']
            resource_hours[resource_id] = resource_hours.get(resource_id, 0) + duration
        
        # Find underutilized and overutilized resources
        avg_hours = sum(resource_hours.values()) / len(self.resources)
        
        print(f"Optimization: Average resource utilization = {avg_hours:.1f} hours")
        
        # For now, return the original solution
        # In a full implementation, you would implement more sophisticated optimization
        
        return optimized 