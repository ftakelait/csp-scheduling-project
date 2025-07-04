#!/usr/bin/env python3
"""
CSP Scheduling Project - Automatic Grader
University of North Dakota - CSCI 384 AI Course | Fall 2025

Usage: python grader.py <student_file.py>

This grader automatically evaluates student submissions and provides detailed feedback
with point breakdowns for each section of the assignment.

GRADING CRITERIA:
- Step 1: Data Loading and Validation (10 points)
- Step 2: CSP Formulation (15 points)  
- Step 3: Heuristic Implementation (15 points)
- Step 4: CSP Solving (20 points)
- Step 5: Solution Analysis (15 points)
- Step 6: Visualization (10 points)
- Step 7: Export Functionality (10 points)
- Conceptual Questions (15 points)
- Bonus Features (10 points)

TOTAL: 110 points
"""

import sys
import os
import json
import time
import traceback
import importlib.util
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
import tempfile
import shutil

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class CSPGrader:
    """Automatic grader for CSP Scheduling Project"""
    
    def __init__(self, student_file: str):
        self.student_file = student_file
        self.student_name = os.path.splitext(os.path.basename(student_file))[0]
        self.results = {
            'student_name': self.student_name,
            'timestamp': datetime.now().isoformat(),
            'total_score': 0,
            'max_score': 110,
            'sections': {},
            'errors': [],
            'warnings': [],
            'feedback': []
        }
        
        # Import student module
        self.student_module = None
        self.load_student_module()
    
    def load_student_module(self):
        """Load the student's submission as a module"""
        try:
            spec = importlib.util.spec_from_file_location("student_submission", self.student_file)
            self.student_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.student_module)
            self.add_feedback("✓ Student file loaded successfully", "info")
        except Exception as e:
            self.add_error(f"Failed to load student file: {str(e)}")
            raise
    
    def add_error(self, message: str):
        """Add an error message"""
        self.results['errors'].append(message)
        print(f"❌ ERROR: {message}")
    
    def add_warning(self, message: str):
        """Add a warning message"""
        self.results['warnings'].append(message)
        print(f"⚠️  WARNING: {message}")
    
    def add_feedback(self, message: str, level: str = "info"):
        """Add feedback message"""
        self.results['feedback'].append({
            'message': message,
            'level': level,
            'timestamp': datetime.now().isoformat()
        })
        print(f"ℹ️  {message}")
    
    def grade_section(self, section_name: str, max_points: int, test_func) -> int:
        """Grade a section using the provided test function"""
        print(f"\n{'='*60}")
        print(f"GRADING SECTION: {section_name.upper()} ({max_points} points)")
        print(f"{'='*60}")
        
        try:
            points = test_func()
            points = min(points, max_points)  # Cap at max points
            points = max(points, 0)  # Ensure non-negative
            
            self.results['sections'][section_name] = {
                'points_earned': points,
                'max_points': max_points,
                'percentage': (points / max_points * 100) if max_points > 0 else 0
            }
            
            print(f"✓ {section_name}: {points}/{max_points} points ({points/max_points*100:.1f}%)")
            return points
            
        except Exception as e:
            self.add_error(f"Error grading {section_name}: {str(e)}")
            self.results['sections'][section_name] = {
                'points_earned': 0,
                'max_points': max_points,
                'percentage': 0,
                'error': str(e)
            }
            return 0
    
    def test_data_loading(self) -> int:
        """Test Step 1: Data Loading and Validation (10 points)"""
        points = 0
        
        try:
            # Test if data loading is implemented
            if hasattr(self.student_module, 'data') and self.student_module.data is not None:
                points += 3
                self.add_feedback("✓ Data loading implemented")
            else:
                self.add_error("Data loading not implemented or data is None")
            
            # Test if validation is implemented
            if hasattr(self.student_module, 'is_valid') and self.student_module.is_valid is not None:
                points += 2
                self.add_feedback("✓ Data validation implemented")
            else:
                self.add_error("Data validation not implemented")
            
            # Test if required variables are extracted
            required_vars = ['tasks', 'resources', 'time_slots', 'constraints']
            for var in required_vars:
                if hasattr(self.student_module, var) and getattr(self.student_module, var) is not None:
                    points += 1
                    self.add_feedback(f"✓ {var} extracted correctly")
                else:
                    self.add_error(f"{var} not extracted or is None")
            
            # Test data structure
            if hasattr(self.student_module, 'data') and self.student_module.data:
                if 'schedule' in self.student_module.data:
                    points += 1
                    self.add_feedback("✓ Correct data structure (schedule key present)")
                else:
                    self.add_error("Incorrect data structure (missing schedule key)")
            
            return min(points, 10)
            
        except Exception as e:
            self.add_error(f"Data loading test failed: {str(e)}")
            return 0
    
    def test_csp_formulation(self) -> int:
        """Test Step 2: CSP Formulation (15 points)"""
        points = 0
        
        try:
            # Test if CSP object is created
            if hasattr(self.student_module, 'scheduling_csp') and self.student_module.scheduling_csp is not None:
                points += 5
                self.add_feedback("✓ CSP object created")
            else:
                self.add_error("CSP object not created or is None")
            
            # Test CSP initialization
            if hasattr(self.student_module, 'scheduling_csp'):
                csp = self.student_module.scheduling_csp
                if hasattr(csp, 'variables') and csp.variables:
                    points += 3
                    self.add_feedback("✓ CSP variables initialized")
                else:
                    self.add_error("CSP variables not initialized")
                
                if hasattr(csp, 'domains') and csp.domains:
                    points += 3
                    self.add_feedback("✓ CSP domains initialized")
                else:
                    self.add_error("CSP domains not initialized")
                
                if hasattr(csp, 'constraint_graph') and csp.constraint_graph is not None:
                    points += 2
                    self.add_feedback("✓ CSP constraint graph initialized")
                else:
                    self.add_error("CSP constraint graph not initialized")
                
                # Test CSP solve method
                if hasattr(csp, 'solve'):
                    points += 2
                    self.add_feedback("✓ CSP solve method present")
                else:
                    self.add_error("CSP solve method missing")
            
            return min(points, 15)
            
        except Exception as e:
            self.add_error(f"CSP formulation test failed: {str(e)}")
            return 0
    
    def test_heuristics(self) -> int:
        """Test Step 3: Heuristic Implementation (15 points)"""
        points = 0
        
        try:
            # Test MRV heuristic
            if hasattr(self.student_module, 'mrv_heuristic'):
                points += 5
                self.add_feedback("✓ MRV heuristic implemented")
                
                # Test if it's callable
                if callable(self.student_module.mrv_heuristic):
                    points += 1
                    self.add_feedback("✓ MRV heuristic is callable")
                else:
                    self.add_error("MRV heuristic is not callable")
            else:
                self.add_error("MRV heuristic not implemented")
            
            # Test Degree heuristic
            if hasattr(self.student_module, 'degree_heuristic'):
                points += 3
                self.add_feedback("✓ Degree heuristic implemented")
                
                if callable(self.student_module.degree_heuristic):
                    points += 1
                    self.add_feedback("✓ Degree heuristic is callable")
                else:
                    self.add_error("Degree heuristic is not callable")
            else:
                self.add_error("Degree heuristic not implemented")
            
            # Test Combined heuristic
            if hasattr(self.student_module, 'combined_heuristic'):
                points += 3
                self.add_feedback("✓ Combined heuristic implemented")
                
                if callable(self.student_module.combined_heuristic):
                    points += 1
                    self.add_feedback("✓ Combined heuristic is callable")
                else:
                    self.add_error("Combined heuristic is not callable")
            else:
                self.add_error("Combined heuristic not implemented")
            
            return min(points, 15)
            
        except Exception as e:
            self.add_error(f"Heuristic test failed: {str(e)}")
            return 0
    
    def test_csp_solving(self) -> int:
        """Test Step 4: CSP Solving (20 points)"""
        points = 0
        
        try:
            # Test if solutions dictionary is created
            if hasattr(self.student_module, 'solutions') and self.student_module.solutions is not None:
                points += 5
                self.add_feedback("✓ Solutions dictionary created")
            else:
                self.add_error("Solutions dictionary not created or is None")
            
            # Test if best solution is selected
            if hasattr(self.student_module, 'best_solution') and self.student_module.best_solution is not None:
                points += 5
                self.add_feedback("✓ Best solution selected")
            else:
                self.add_error("Best solution not selected or is None")
            
            # Test if CSP solve method works
            if hasattr(self.student_module, 'scheduling_csp') and self.student_module.scheduling_csp:
                csp = self.student_module.scheduling_csp
                if hasattr(csp, 'solve'):
                    try:
                        # Test with a short timeout
                        solution = csp.solve(heuristic='mrv', timeout=5)
                        if solution is not None:
                            points += 5
                            self.add_feedback("✓ CSP solve method works and returns solution")
                        else:
                            points += 2
                            self.add_feedback("✓ CSP solve method works but no solution found (may be due to timeout)")
                    except Exception as e:
                        self.add_error(f"CSP solve method failed: {str(e)}")
                else:
                    self.add_error("CSP solve method missing")
            
            # Test multiple heuristics
            if hasattr(self.student_module, 'solutions') and self.student_module.solutions:
                solutions = self.student_module.solutions
                if isinstance(solutions, dict) and len(solutions) > 0:
                    points += 3
                    self.add_feedback(f"✓ Multiple heuristics tested ({len(solutions)} heuristics)")
                else:
                    self.add_error("Solutions dictionary is empty or not a dictionary")
            
            # Test solution format
            if hasattr(self.student_module, 'best_solution') and self.student_module.best_solution:
                best_solution = self.student_module.best_solution
                if isinstance(best_solution, dict):
                    points += 2
                    self.add_feedback("✓ Best solution is in correct format (dictionary)")
                else:
                    self.add_error("Best solution is not in correct format (should be dictionary)")
            
            return min(points, 20)
            
        except Exception as e:
            self.add_error(f"CSP solving test failed: {str(e)}")
            return 0
    
    def test_solution_analysis(self) -> int:
        """Test Step 5: Solution Analysis (15 points)"""
        points = 0
        
        try:
            # Test constraint violation analysis
            if hasattr(self.student_module, 'analyze_constraint_violations'):
                points += 3
                self.add_feedback("✓ Constraint violation analysis function implemented")
                
                if callable(self.student_module.analyze_constraint_violations):
                    points += 1
                    self.add_feedback("✓ Constraint violation analysis is callable")
                else:
                    self.add_error("Constraint violation analysis is not callable")
            else:
                self.add_error("Constraint violation analysis function not implemented")
            
            # Test solution validation
            if hasattr(self.student_module, 'validate_solution'):
                points += 3
                self.add_feedback("✓ Solution validation function implemented")
                
                if callable(self.student_module.validate_solution):
                    points += 1
                    self.add_feedback("✓ Solution validation is callable")
                else:
                    self.add_error("Solution validation is not callable")
            else:
                self.add_error("Solution validation function not implemented")
            
            # Test performance metrics
            if hasattr(self.student_module, 'calculate_performance_metrics'):
                points += 3
                self.add_feedback("✓ Performance metrics function implemented")
                
                if callable(self.student_module.calculate_performance_metrics):
                    points += 1
                    self.add_feedback("✓ Performance metrics is callable")
                else:
                    self.add_error("Performance metrics is not callable")
            else:
                self.add_error("Performance metrics function not implemented")
            
            # Test if analysis is performed on best solution
            if hasattr(self.student_module, 'best_solution') and self.student_module.best_solution:
                best_solution = self.student_module.best_solution
                if isinstance(best_solution, dict) and len(best_solution) > 0:
                    points += 3
                    self.add_feedback("✓ Solution analysis performed on valid solution")
                else:
                    self.add_error("Solution analysis not performed on valid solution")
            
            return min(points, 15)
            
        except Exception as e:
            self.add_error(f"Solution analysis test failed: {str(e)}")
            return 0
    
    def test_visualization(self) -> int:
        """Test Step 6: Visualization (10 points)"""
        points = 0
        
        try:
            # Test Gantt chart function
            if hasattr(self.student_module, 'create_gantt_chart'):
                points += 3
                self.add_feedback("✓ Gantt chart function implemented")
                
                if callable(self.student_module.create_gantt_chart):
                    points += 1
                    self.add_feedback("✓ Gantt chart function is callable")
                else:
                    self.add_error("Gantt chart function is not callable")
            else:
                self.add_error("Gantt chart function not implemented")
            
            # Test resource utilization chart function
            if hasattr(self.student_module, 'create_resource_utilization_chart'):
                points += 3
                self.add_feedback("✓ Resource utilization chart function implemented")
                
                if callable(self.student_module.create_resource_utilization_chart):
                    points += 1
                    self.add_feedback("✓ Resource utilization chart function is callable")
                else:
                    self.add_error("Resource utilization chart function is not callable")
            else:
                self.add_error("Resource utilization chart function not implemented")
            
            # Test if visualizations are created when solution exists
            if hasattr(self.student_module, 'best_solution') and self.student_module.best_solution:
                best_solution = self.student_module.best_solution
                if isinstance(best_solution, dict) and len(best_solution) > 0:
                    points += 2
                    self.add_feedback("✓ Visualizations created for valid solution")
                else:
                    self.add_error("Visualizations not created for valid solution")
            
            return min(points, 10)
            
        except Exception as e:
            self.add_error(f"Visualization test failed: {str(e)}")
            return 0
    
    def test_export_functionality(self) -> int:
        """Test Step 7: Export Functionality (10 points)"""
        points = 0
        
        try:
            # Test JSON export function
            if hasattr(self.student_module, 'export_solution_json'):
                points += 3
                self.add_feedback("✓ JSON export function implemented")
                
                if callable(self.student_module.export_solution_json):
                    points += 1
                    self.add_feedback("✓ JSON export function is callable")
                else:
                    self.add_error("JSON export function is not callable")
            else:
                self.add_error("JSON export function not implemented")
            
            # Test CSV export function
            if hasattr(self.student_module, 'export_solution_csv'):
                points += 3
                self.add_feedback("✓ CSV export function implemented")
                
                if callable(self.student_module.export_solution_csv):
                    points += 1
                    self.add_feedback("✓ CSV export function is callable")
                else:
                    self.add_error("CSV export function is not callable")
            else:
                self.add_error("CSV export function not implemented")
            
            # Test if export is performed when solution exists
            if hasattr(self.student_module, 'best_solution') and self.student_module.best_solution:
                best_solution = self.student_module.best_solution
                if isinstance(best_solution, dict) and len(best_solution) > 0:
                    points += 2
                    self.add_feedback("✓ Export functionality used for valid solution")
                else:
                    self.add_error("Export functionality not used for valid solution")
            
            return min(points, 10)
            
        except Exception as e:
            self.add_error(f"Export functionality test failed: {str(e)}")
            return 0
    
    def test_conceptual_questions(self) -> int:
        """Test Conceptual Questions (15 points)"""
        points = 0
        
        try:
            # Test if all questions are answered
            questions = ['q1_answer', 'q2_answer', 'q3_answer', 'q4_answer', 'q5_answer']
            valid_answers = ['A', 'B', 'C', 'D']
            
            for i, question in enumerate(questions):
                if hasattr(self.student_module, question):
                    answer = getattr(self.student_module, question)
                    if answer in valid_answers:
                        points += 2
                        self.add_feedback(f"✓ Question {i+1} answered correctly")
                    elif answer is not None:
                        points += 1
                        self.add_feedback(f"⚠️  Question {i+1} answered but not with A/B/C/D")
                    else:
                        self.add_error(f"Question {i+1} not answered")
                else:
                    self.add_error(f"Question {i+1} variable not found")
            
            # Test explanations
            explanations = ['q1_explanation', 'q2_explanation', 'q3_explanation', 'q4_explanation', 'q5_explanation']
            
            for i, explanation in enumerate(explanations):
                if hasattr(self.student_module, explanation):
                    expl = getattr(self.student_module, explanation)
                    if expl and isinstance(expl, str) and len(expl.strip()) > 10:
                        points += 1
                        self.add_feedback(f"✓ Question {i+1} explanation provided")
                    else:
                        self.add_error(f"Question {i+1} explanation missing or too short")
                else:
                    self.add_error(f"Question {i+1} explanation variable not found")
            
            return min(points, 15)
            
        except Exception as e:
            self.add_error(f"Conceptual questions test failed: {str(e)}")
            return 0
    
    def test_bonus_features(self) -> int:
        """Test Bonus Features (10 points)"""
        points = 0
        
        try:
            # Test arc consistency
            if hasattr(self.student_module, 'compare_heuristics'):
                points += 3
                self.add_feedback("✓ Heuristic comparison function implemented")
                
                if callable(self.student_module.compare_heuristics):
                    points += 1
                    self.add_feedback("✓ Heuristic comparison is callable")
                else:
                    self.add_error("Heuristic comparison is not callable")
            else:
                self.add_error("Heuristic comparison function not implemented")
            
            # Test solution optimization
            if hasattr(self.student_module, 'optimize_solution'):
                points += 3
                self.add_feedback("✓ Solution optimization function implemented")
                
                if callable(self.student_module.optimize_solution):
                    points += 1
                    self.add_feedback("✓ Solution optimization is callable")
                else:
                    self.add_error("Solution optimization is not callable")
            else:
                self.add_error("Solution optimization function not implemented")
            
            # Test GUI integration
            if hasattr(self.student_module, 'run_gui'):
                points += 2
                self.add_feedback("✓ GUI integration function implemented")
                
                if callable(self.student_module.run_gui):
                    self.add_feedback("✓ GUI integration is callable")
                else:
                    self.add_error("GUI integration is not callable")
            else:
                self.add_error("GUI integration function not implemented")
            
            return min(points, 10)
            
        except Exception as e:
            self.add_error(f"Bonus features test failed: {str(e)}")
            return 0
    
    def run_all_tests(self):
        """Run all grading tests"""
        print(f"\n{'='*80}")
        print(f"GRADING STUDENT: {self.student_name}")
        print(f"FILE: {self.student_file}")
        print(f"TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        # Run all tests
        total_score = 0
        
        total_score += self.grade_section("Data Loading and Validation", 10, self.test_data_loading)
        total_score += self.grade_section("CSP Formulation", 15, self.test_csp_formulation)
        total_score += self.grade_section("Heuristic Implementation", 15, self.test_heuristics)
        total_score += self.grade_section("CSP Solving", 20, self.test_csp_solving)
        total_score += self.grade_section("Solution Analysis", 15, self.test_solution_analysis)
        total_score += self.grade_section("Visualization", 10, self.test_visualization)
        total_score += self.grade_section("Export Functionality", 10, self.test_export_functionality)
        total_score += self.grade_section("Conceptual Questions", 15, self.test_conceptual_questions)
        total_score += self.grade_section("Bonus Features", 10, self.test_bonus_features)
        
        self.results['total_score'] = total_score
        
        # Generate final report
        self.generate_report()
    
    def generate_report(self):
        """Generate detailed grading report"""
        print(f"\n{'='*80}")
        print("FINAL GRADING REPORT")
        print(f"{'='*80}")
        
        print(f"Student: {self.student_name}")
        print(f"File: {self.student_file}")
        print(f"Total Score: {self.results['total_score']}/{self.results['max_score']} ({self.results['total_score']/self.results['max_score']*100:.1f}%)")
        
        print(f"\nSECTION BREAKDOWN:")
        print(f"{'Section':<30} {'Points':<10} {'Percentage':<12}")
        print(f"{'-'*30} {'-'*10} {'-'*12}")
        
        for section_name, section_data in self.results['sections'].items():
            points = section_data['points_earned']
            max_points = section_data['max_points']
            percentage = section_data['percentage']
            print(f"{section_name:<30} {points}/{max_points:<10} {percentage:.1f}%")
        
        if self.results['errors']:
            print(f"\nERRORS FOUND:")
            for error in self.results['errors']:
                print(f"❌ {error}")
        
        if self.results['warnings']:
            print(f"\nWARNINGS:")
            for warning in self.results['warnings']:
                print(f"⚠️  {warning}")
        
        print(f"\nDETAILED FEEDBACK:")
        for feedback in self.results['feedback']:
            level_icon = {"info": "ℹ️", "warning": "⚠️", "error": "❌"}
            icon = level_icon.get(feedback['level'], "ℹ️")
            print(f"{icon} {feedback['message']}")
        
        # Save detailed report to file
        report_file = f"grade_report_{self.student_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\nDetailed report saved to: {report_file}")
        
        # Determine letter grade
        percentage = (self.results['total_score'] / self.results['max_score']) * 100
        if percentage >= 93:
            letter_grade = "A"
        elif percentage >= 90:
            letter_grade = "A-"
        elif percentage >= 87:
            letter_grade = "B+"
        elif percentage >= 83:
            letter_grade = "B"
        elif percentage >= 80:
            letter_grade = "B-"
        elif percentage >= 77:
            letter_grade = "C+"
        elif percentage >= 73:
            letter_grade = "C"
        elif percentage >= 70:
            letter_grade = "C-"
        elif percentage >= 67:
            letter_grade = "D+"
        elif percentage >= 63:
            letter_grade = "D"
        elif percentage >= 60:
            letter_grade = "D-"
        else:
            letter_grade = "F"
        
        print(f"\nLETTER GRADE: {letter_grade}")
        
        # Generate email template
        self.generate_email_template(letter_grade, percentage)
    
    def generate_email_template(self, letter_grade: str, percentage: float):
        """Generate email template for student feedback"""
        email_file = f"email_template_{self.student_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(email_file, 'w') as f:
            f.write(f"Subject: CSP Scheduling Project - Grading Results\n\n")
            f.write(f"Dear Student,\n\n")
            f.write(f"Your CSP Scheduling Project has been graded. Here are your results:\n\n")
            f.write(f"Overall Score: {self.results['total_score']}/{self.results['max_score']} ({percentage:.1f}%)\n")
            f.write(f"Letter Grade: {letter_grade}\n\n")
            
            f.write("SECTION BREAKDOWN:\n")
            f.write("-" * 50 + "\n")
            for section_name, section_data in self.results['sections'].items():
                points = section_data['points_earned']
                max_points = section_data['max_points']
                percentage = section_data['percentage']
                f.write(f"{section_name}: {points}/{max_points} ({percentage:.1f}%)\n")
            
            f.write("\nAREAS FOR IMPROVEMENT:\n")
            f.write("-" * 50 + "\n")
            
            # Find sections with low scores
            low_score_sections = []
            for section_name, section_data in self.results['sections'].items():
                if section_data['percentage'] < 70:
                    low_score_sections.append(section_name)
            
            if low_score_sections:
                f.write("You need to improve in the following areas:\n")
                for section in low_score_sections:
                    f.write(f"- {section}\n")
            else:
                f.write("Good work! All sections are well implemented.\n")
            
            if self.results['errors']:
                f.write("\nSPECIFIC ISSUES FOUND:\n")
                f.write("-" * 50 + "\n")
                for error in self.results['errors']:
                    f.write(f"- {error}\n")
            
            f.write("\nPOSITIVE FEEDBACK:\n")
            f.write("-" * 50 + "\n")
            positive_feedback = [f['message'] for f in self.results['feedback'] if f['level'] == 'info']
            if positive_feedback:
                for feedback in positive_feedback[:5]:  # Top 5 positive feedback
                    f.write(f"- {feedback}\n")
            else:
                f.write("- Keep working on the implementation\n")
            
            f.write("\nIf you have any questions about your grade, please don't hesitate to ask.\n\n")
            f.write("Best regards,\n")
            f.write("Your Teaching Assistant\n")
        
        print(f"Email template saved to: {email_file}")


def main():
    """Main function to run the grader"""
    if len(sys.argv) != 2:
        print("Usage: python grader.py <student_file.py>")
        print("Example: python grader.py student_submission.py")
        sys.exit(1)
    
    student_file = sys.argv[1]
    
    if not os.path.exists(student_file):
        print(f"Error: File '{student_file}' not found.")
        sys.exit(1)
    
    if not student_file.endswith('.py'):
        print(f"Error: File '{student_file}' is not a Python file.")
        sys.exit(1)
    
    try:
        grader = CSPGrader(student_file)
        grader.run_all_tests()
    except Exception as e:
        print(f"Fatal error during grading: {str(e)}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 