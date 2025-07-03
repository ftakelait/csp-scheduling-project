"""
Scheduler Module for CSP Scheduling Project
Provides high-level scheduling problem formulation and management
"""

import time
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import json

from src.csp_solver import SchedulingCSP, CSPSolver, CSPConstraint
from utils.constraint_utils import (
    check_resource_availability, check_task_dependencies, check_resource_skills,
    check_max_hours_per_day, check_preferred_resources, get_constraint_violations
)


class Scheduler:
    """High-level scheduler for managing scheduling problems"""
    
    def __init__(self, tasks: List[Dict], resources: List[Dict], 
                 time_slots: Dict[str, Any], constraints: Dict[str, Any]):
        self.tasks = tasks
        self.resources = resources
        self.time_slots = time_slots
        self.constraints = constraints
        self.scheduling_csp = None
        self.current_solution = None
        self.performance_history = []
        
    def create_csp_problem(self) -> SchedulingCSP:
        """
        Create a CSP problem from the scheduling data
        
        Returns:
            Configured SchedulingCSP instance
        """
        self.scheduling_csp = SchedulingCSP(self.tasks, self.resources, self.time_slots, self.constraints)
        return self.scheduling_csp
    
    def solve(self, heuristic: str = "mrv", use_arc_consistency: bool = True, 
              timeout: int = 300) -> Optional[Dict[str, Any]]:
        """
        Solve the scheduling problem
        
        Args:
            heuristic: Variable ordering heuristic
            use_arc_consistency: Whether to use arc consistency
            timeout: Maximum time to spend solving
            
        Returns:
            Schedule solution or None
        """
        if self.scheduling_csp is None:
            self.create_csp_problem()
        
        start_time = time.time()
        solution = self.scheduling_csp.solve(heuristic, use_arc_consistency, timeout)
        solve_time = time.time() - start_time
        
        # Record performance
        performance_record = {
            'heuristic': heuristic,
            'time': solve_time,
            'solution_found': solution is not None,
            'tasks_scheduled': len(solution) if solution else 0,
            'timestamp': time.time()
        }
        self.performance_history.append(performance_record)
        
        if solution:
            self.current_solution = solution
        
        return solution
    
    def solve_with_all_heuristics(self, timeout: int = 300) -> Dict[str, Any]:
        """
        Solve the problem with all available heuristics
        
        Args:
            timeout: Maximum time per heuristic
            
        Returns:
            Dictionary of results for each heuristic
        """
        heuristics = ["mrv", "degree", "combined"]
        results = {}
        
        for heuristic in heuristics:
            print(f"Solving with {heuristic.upper()} heuristic...")
            solution = self.solve(heuristic, timeout=timeout)
            results[heuristic] = {
                'solution': solution,
                'time': self.performance_history[-1]['time'],
                'success': solution is not None
            }
        
        return results
    
    def validate_solution(self, solution: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a solution against all constraints
        
        Args:
            solution: The solution to validate
            
        Returns:
            Validation results including violations
        """
        if not solution:
            return {'valid': False, 'violations': {}, 'message': 'No solution provided'}
        
        violations = {}
        total_violations = 0
        
        # Check each task assignment
        for task_id, assignment in solution.items():
            task_violations = get_constraint_violations(
                assignment, task_id, self.resources, self.tasks, solution
            )
            
            if task_violations:
                violations[task_id] = task_violations
                total_violations += len(task_violations)
        
        # Check resource utilization
        resource_hours = defaultdict(int)
        for assignment in solution.values():
            resource_id = assignment['resource_id']
            duration = assignment['duration']
            resource_hours[resource_id] += duration
        
        # Check for over-utilization
        for resource_id, total_hours in resource_hours.items():
            resource = next((r for r in self.resources if r['id'] == resource_id), None)
            if resource and total_hours > resource.get('max_hours_per_day', 8) * len(self.time_slots['days']):
                violations[f'resource_{resource_id}'] = [
                    f"Resource {resource_id} over-utilized: {total_hours} hours total"
                ]
                total_violations += 1
        
        return {
            'valid': total_violations == 0,
            'violations': violations,
            'total_violations': total_violations,
            'tasks_scheduled': len(solution),
            'resource_utilization': dict(resource_hours)
        }
    
    def get_solution_metrics(self, solution: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate various metrics for a solution
        
        Args:
            solution: The solution to analyze
            
        Returns:
            Dictionary of metrics
        """
        if not solution:
            return {}
        
        # Basic metrics
        metrics = {
            'total_tasks': len(solution),
            'total_duration': sum(assignment['duration'] for assignment in solution.values()),
            'unique_resources': len(set(assignment['resource_id'] for assignment in solution.values())),
            'schedule_span': self._calculate_schedule_span(solution)
        }
        
        # Resource utilization
        resource_hours = defaultdict(int)
        for assignment in solution.values():
            resource_id = assignment['resource_id']
            duration = assignment['duration']
            resource_hours[resource_id] += duration
        
        metrics['resource_utilization'] = dict(resource_hours)
        metrics['avg_resource_hours'] = sum(resource_hours.values()) / len(resource_hours) if resource_hours else 0
        metrics['max_resource_hours'] = max(resource_hours.values()) if resource_hours else 0
        metrics['min_resource_hours'] = min(resource_hours.values()) if resource_hours else 0
        
        # Priority distribution
        priority_counts = defaultdict(int)
        for assignment in solution.values():
            task_id = assignment.get('task_id', '')
            task = next((t for t in self.tasks if t['id'] == task_id), None)
            if task:
                priority = task.get('priority', 'medium')
                priority_counts[priority] += 1
        
        metrics['priority_distribution'] = dict(priority_counts)
        
        # Skill utilization
        skill_usage = defaultdict(int)
        for assignment in solution.values():
            task_id = assignment.get('task_id', '')
            task = next((t for t in self.tasks if t['id'] == task_id), None)
            if task:
                for skill in task.get('required_skills', []):
                    skill_usage[skill] += 1
        
        metrics['skill_usage'] = dict(skill_usage)
        
        return metrics
    
    def _calculate_schedule_span(self, solution: Dict[str, Any]) -> int:
        """Calculate the total span of the schedule in hours"""
        if not solution:
            return 0
        
        # Find earliest start and latest end
        earliest_start = float('inf')
        latest_end = 0
        
        for assignment in solution.values():
            start_hour = assignment['start_hour']
            end_hour = assignment['end_hour']
            
            earliest_start = min(earliest_start, start_hour)
            latest_end = max(latest_end, end_hour)
        
        return latest_end - earliest_start if earliest_start != float('inf') else 0
    
    def export_solution(self, solution: Dict[str, Any], filename: str, format: str = 'json') -> bool:
        """
        Export a solution to a file
        
        Args:
            solution: The solution to export
            filename: Output filename
            format: Export format ('json' or 'csv')
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            if format.lower() == 'json':
                with open(filename, 'w') as f:
                    json.dump(solution, f, indent=2)
            elif format.lower() == 'csv':
                import csv
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Task ID', 'Task Name', 'Resource ID', 'Resource Name', 
                                   'Start Day', 'Start Hour', 'Duration', 'End Hour', 'Priority'])
                    
                    for task_id, assignment in solution.items():
                        writer.writerow([
                            task_id,
                            assignment.get('task_name', ''),
                            assignment.get('resource_id', ''),
                            assignment.get('resource_name', ''),
                            assignment.get('start_day', ''),
                            assignment.get('start_hour', ''),
                            assignment.get('duration', ''),
                            assignment.get('end_hour', ''),
                            assignment.get('priority', '')
                        ])
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            return True
            
        except Exception as e:
            print(f"Export failed: {e}")
            return False
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Get a summary of solver performance
        
        Returns:
            Performance summary
        """
        if not self.performance_history:
            return {}
        
        # Calculate statistics
        successful_runs = [p for p in self.performance_history if p['solution_found']]
        failed_runs = [p for p in self.performance_history if not p['solution_found']]
        
        summary = {
            'total_runs': len(self.performance_history),
            'successful_runs': len(successful_runs),
            'failed_runs': len(failed_runs),
            'success_rate': len(successful_runs) / len(self.performance_history) if self.performance_history else 0,
            'average_time': sum(p['time'] for p in self.performance_history) / len(self.performance_history),
            'best_time': min(p['time'] for p in successful_runs) if successful_runs else None,
            'worst_time': max(p['time'] for p in successful_runs) if successful_runs else None
        }
        
        # Performance by heuristic
        heuristic_stats = defaultdict(list)
        for record in self.performance_history:
            heuristic_stats[record['heuristic']].append(record)
        
        summary['by_heuristic'] = {}
        for heuristic, records in heuristic_stats.items():
            successful = [r for r in records if r['solution_found']]
            summary['by_heuristic'][heuristic] = {
                'total_runs': len(records),
                'successful_runs': len(successful),
                'success_rate': len(successful) / len(records) if records else 0,
                'average_time': sum(r['time'] for r in records) / len(records),
                'best_time': min(r['time'] for r in successful) if successful else None
            }
        
        return summary
    
    def optimize_solution(self, solution: Dict[str, Any], max_iterations: int = 100) -> Dict[str, Any]:
        """
        Attempt to optimize an existing solution
        
        Args:
            solution: The solution to optimize
            max_iterations: Maximum optimization iterations
            
        Returns:
            Optimized solution
        """
        if not solution:
            return solution
        
        # This is a placeholder for optimization logic
        # In a real implementation, you might:
        # - Try to reduce schedule span
        # - Balance resource utilization
        # - Minimize constraint violations
        # - Optimize for preferred resources
        
        print("Optimization not yet implemented")
        return solution
    
    def create_report(self, solution: Dict[str, Any]) -> str:
        """
        Create a text report for a solution
        
        Args:
            solution: The solution to report on
            
        Returns:
            Formatted report string
        """
        if not solution:
            return "No solution available for reporting."
        
        # Validate solution
        validation = self.validate_solution(solution)
        metrics = self.get_solution_metrics(solution)
        
        report = f"""
CSP Scheduling Solution Report
{'=' * 50}

SOLUTION SUMMARY:
• Total tasks scheduled: {len(solution)}
• Total duration: {metrics.get('total_duration', 0)} hours
• Resources used: {metrics.get('unique_resources', 0)}
• Schedule span: {metrics.get('schedule_span', 0)} hours

VALIDATION RESULTS:
• Valid solution: {'Yes' if validation['valid'] else 'No'}
• Constraint violations: {validation['total_violations']}

RESOURCE UTILIZATION:
"""
        
        for resource_id, hours in metrics.get('resource_utilization', {}).items():
            resource_name = next((r['name'] for r in self.resources if r['id'] == resource_id), resource_id)
            report += f"• {resource_name}: {hours} hours\n"
        
        report += f"""
PRIORITY DISTRIBUTION:
"""
        for priority, count in metrics.get('priority_distribution', {}).items():
            report += f"• {priority.title()}: {count} tasks\n"
        
        if validation['violations']:
            report += f"""
CONSTRAINT VIOLATIONS:
"""
            for task_id, violations in validation['violations'].items():
                report += f"• {task_id}:\n"
                for violation in violations:
                    report += f"  - {violation}\n"
        
        report += f"""
PERFORMANCE SUMMARY:
"""
        perf_summary = self.get_performance_summary()
        if perf_summary:
            report += f"• Total solver runs: {perf_summary['total_runs']}\n"
            report += f"• Success rate: {perf_summary['success_rate']:.1%}\n"
            report += f"• Average solving time: {perf_summary['average_time']:.2f} seconds\n"
        
        return report


class SchedulingProblem:
    """Represents a complete scheduling problem"""
    
    def __init__(self, name: str = "Scheduling Problem"):
        self.name = name
        self.tasks = []
        self.resources = []
        self.time_slots = {
            'days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
            'hours': [9, 10, 11, 12, 13, 14, 15, 16, 17],
            'working_hours_per_day': 8
        }
        self.constraints = {
            'hard_constraints': [
                'no_resource_overlap',
                'task_dependencies',
                'resource_skills',
                'resource_availability',
                'max_hours_per_day'
            ],
            'soft_constraints': [
                'preferred_resources',
                'task_priority',
                'balanced_workload'
            ]
        }
        self.scheduler = None
    
    def add_task(self, task: Dict) -> None:
        """Add a task to the problem"""
        self.tasks.append(task)
    
    def add_resource(self, resource: Dict) -> None:
        """Add a resource to the problem"""
        self.resources.append(resource)
    
    def set_time_slots(self, time_slots: Dict[str, Any]) -> None:
        """Set the time slots configuration"""
        self.time_slots = time_slots
    
    def set_constraints(self, constraints: Dict[str, Any]) -> None:
        """Set the constraints configuration"""
        self.constraints = constraints
    
    def create_scheduler(self) -> Scheduler:
        """Create a scheduler for this problem"""
        self.scheduler = Scheduler(self.tasks, self.resources, self.time_slots, self.constraints)
        return self.scheduler
    
    def validate_problem(self) -> Dict[str, Any]:
        """Validate the problem definition"""
        issues = []
        
        # Check for required fields
        for i, task in enumerate(self.tasks):
            if 'id' not in task:
                issues.append(f"Task {i}: Missing 'id' field")
            if 'name' not in task:
                issues.append(f"Task {i}: Missing 'name' field")
            if 'duration' not in task:
                issues.append(f"Task {i}: Missing 'duration' field")
        
        for i, resource in enumerate(self.resources):
            if 'id' not in resource:
                issues.append(f"Resource {i}: Missing 'id' field")
            if 'name' not in resource:
                issues.append(f"Resource {i}: Missing 'name' field")
        
        # Check for duplicate IDs
        task_ids = [task.get('id') for task in self.tasks]
        resource_ids = [resource.get('id') for resource in self.resources]
        
        if len(task_ids) != len(set(task_ids)):
            issues.append("Duplicate task IDs found")
        
        if len(resource_ids) != len(set(resource_ids)):
            issues.append("Duplicate resource IDs found")
        
        # Check dependencies
        for task in self.tasks:
            for dep_id in task.get('dependencies', []):
                if dep_id not in task_ids:
                    issues.append(f"Task {task.get('id')}: Invalid dependency {dep_id}")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'task_count': len(self.tasks),
            'resource_count': len(self.resources)
        }
    
    def export_problem(self, filename: str) -> bool:
        """Export the problem to a JSON file"""
        try:
            problem_data = {
                'name': self.name,
                'tasks': self.tasks,
                'resources': self.resources,
                'time_slots': self.time_slots,
                'constraints': self.constraints
            }
            
            with open(filename, 'w') as f:
                json.dump(problem_data, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Export failed: {e}")
            return False
    
    @classmethod
    def from_file(cls, filename: str) -> 'SchedulingProblem':
        """Create a problem from a JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        problem = cls(data.get('name', 'Imported Problem'))
        problem.tasks = data.get('tasks', [])
        problem.resources = data.get('resources', [])
        problem.time_slots = data.get('time_slots', problem.time_slots)
        problem.constraints = data.get('constraints', problem.constraints)
        
        return problem 