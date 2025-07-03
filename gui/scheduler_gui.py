"""
CSP Scheduling GUI Application
Desktop application for interactive CSP scheduling with real-time constraint checking
Built with PySide6 for modern UI
"""

import sys
import os
import json
import time
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add the project root to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QLabel, QPushButton, QComboBox, QSpinBox, QCheckBox,
    QProgressBar, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QGroupBox, QGridLayout, QSplitter, QMessageBox, QFileDialog,
    QFrame, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PySide6.QtGui import QFont, QPalette, QColor, QIcon

from utils.file_utils import load_schedule_data, export_schedule_to_json, export_schedule_to_csv
from utils.constraint_utils import get_constraint_violations, calculate_schedule_score
from utils.visualization import create_gantt_chart, create_resource_utilization_chart
from src.csp_solver import SchedulingCSP


class SolverThread(QThread):
    """Thread for running CSP solver to avoid blocking the GUI"""
    
    finished = pyqtSignal(dict, float, str)  # solution, time, heuristic
    error = pyqtSignal(str)  # error message
    
    def __init__(self, scheduling_csp, heuristic, use_arc_consistency, timeout):
        super().__init__()
        self.scheduling_csp = scheduling_csp
        self.heuristic = heuristic
        self.use_arc_consistency = use_arc_consistency
        self.timeout = timeout
    
    def run(self):
        """Run the solver in background thread"""
        try:
            start_time = time.time()
            solution = self.scheduling_csp.solve(
                heuristic=self.heuristic,
                use_arc_consistency=self.use_arc_consistency,
                timeout=self.timeout
            )
            solve_time = time.time() - start_time
            
            self.finished.emit(solution, solve_time, self.heuristic)
            
        except Exception as e:
            self.error.emit(str(e))


class SchedulerGUI(QMainWindow):
    """Main GUI application for CSP scheduling"""
    
    def __init__(self):
        super().__init__()
        
        # Data storage
        self.data = None
        self.tasks = []
        self.resources = []
        self.time_slots = {}
        self.constraints = {}
        self.current_solution = None
        self.scheduling_csp = None
        self.solver_thread = None
        
        # Performance tracking
        self.performance_results = {}
        
        # Setup UI
        self.setup_ui()
        self.load_initial_data()
        
    def setup_ui(self):
        """Setup the main UI"""
        self.setWindowTitle("CSP Scheduling Solver - Advanced AI Project")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #0078d4;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #c0c0c0;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QTableWidget {
                gridline-color: #e0e0e0;
                selection-background-color: #e3f2fd;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: 1px solid #c0c0c0;
                font-weight: bold;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_problem_tab()
        self.create_solver_tab()
        self.create_solution_tab()
        self.create_analysis_tab()
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready to solve")
        
    def create_problem_tab(self):
        """Create the problem definition tab"""
        problem_widget = QWidget()
        self.tab_widget.addTab(problem_widget, "Problem Definition")
        
        layout = QVBoxLayout(problem_widget)
        
        # Problem overview section
        overview_group = QGroupBox("Problem Overview")
        overview_layout = QVBoxLayout(overview_group)
        
        self.problem_info = QTextEdit()
        self.problem_info.setMaximumHeight(150)
        self.problem_info.setReadOnly(True)
        overview_layout.addWidget(self.problem_info)
        
        layout.addWidget(overview_group)
        
        # Tasks and Resources section
        splitter = QSplitter(Qt.Horizontal)
        
        # Tasks section
        tasks_group = QGroupBox("Tasks")
        tasks_layout = QVBoxLayout(tasks_group)
        
        self.tasks_table = QTableWidget()
        self.tasks_table.setColumnCount(6)
        self.tasks_table.setHorizontalHeaderLabels(['Task ID', 'Name', 'Duration', 'Priority', 'Skills', 'Dependencies'])
        header = self.tasks_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        tasks_layout.addWidget(self.tasks_table)
        
        splitter.addWidget(tasks_group)
        
        # Resources section
        resources_group = QGroupBox("Resources")
        resources_layout = QVBoxLayout(resources_group)
        
        self.resources_table = QTableWidget()
        self.resources_table.setColumnCount(4)
        self.resources_table.setHorizontalHeaderLabels(['Resource ID', 'Name', 'Skills', 'Max Hours/Day'])
        header = self.resources_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        resources_layout.addWidget(self.resources_table)
        
        splitter.addWidget(resources_group)
        
        layout.addWidget(splitter)
        
    def create_solver_tab(self):
        """Create the solver configuration tab"""
        solver_widget = QWidget()
        self.tab_widget.addTab(solver_widget, "CSP Solver")
        
        layout = QVBoxLayout(solver_widget)
        
        # Solver configuration section
        config_group = QGroupBox("Solver Configuration")
        config_layout = QGridLayout(config_group)
        
        # Heuristic selection
        config_layout.addWidget(QLabel("Variable Ordering Heuristic:"), 0, 0)
        self.heuristic_combo = QComboBox()
        self.heuristic_combo.addItems(["mrv", "degree", "combined"])
        config_layout.addWidget(self.heuristic_combo, 0, 1)
        
        # Arc consistency option
        self.arc_consistency_check = QCheckBox("Use Arc Consistency")
        self.arc_consistency_check.setChecked(True)
        config_layout.addWidget(self.arc_consistency_check, 1, 0, 1, 2)
        
        # Timeout setting
        config_layout.addWidget(QLabel("Timeout (seconds):"), 2, 0)
        self.timeout_spinbox = QSpinBox()
        self.timeout_spinbox.setRange(30, 3600)
        self.timeout_spinbox.setValue(300)
        config_layout.addWidget(self.timeout_spinbox, 2, 1)
        
        layout.addWidget(config_group)
        
        # Solve controls
        controls_layout = QHBoxLayout()
        
        self.solve_button = QPushButton("Solve CSP")
        self.solve_button.clicked.connect(self.solve_csp)
        controls_layout.addWidget(self.solve_button)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_solving)
        self.stop_button.setEnabled(False)
        controls_layout.addWidget(self.stop_button)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        controls_layout.addWidget(self.progress_bar)
        
        layout.addLayout(controls_layout)
        
        # Results section
        results_group = QGroupBox("Solver Results")
        results_layout = QVBoxLayout(results_group)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        results_layout.addWidget(self.results_text)
        
        layout.addWidget(results_group)
        
    def create_solution_tab(self):
        """Create the solution visualization tab"""
        solution_widget = QWidget()
        self.tab_widget.addTab(solution_widget, "Solution")
        
        layout = QVBoxLayout(solution_widget)
        
        # Solution controls
        controls_layout = QHBoxLayout()
        
        export_json_btn = QPushButton("Export Solution (JSON)")
        export_json_btn.clicked.connect(self.export_solution_json)
        controls_layout.addWidget(export_json_btn)
        
        export_csv_btn = QPushButton("Export Solution (CSV)")
        export_csv_btn.clicked.connect(self.export_solution_csv)
        controls_layout.addWidget(export_csv_btn)
        
        viz_btn = QPushButton("Generate Visualizations")
        viz_btn.clicked.connect(self.generate_visualizations)
        controls_layout.addWidget(viz_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Solution display
        solution_group = QGroupBox("Schedule Solution")
        solution_layout = QVBoxLayout(solution_group)
        
        self.solution_table = QTableWidget()
        self.solution_table.setColumnCount(6)
        self.solution_table.setHorizontalHeaderLabels(['Task', 'Resource', 'Day', 'Start Time', 'Duration (h)', 'End Time'])
        header = self.solution_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        solution_layout.addWidget(self.solution_table)
        
        layout.addWidget(solution_group)
        
        # Constraint violations section
        violations_group = QGroupBox("Constraint Violations")
        violations_layout = QVBoxLayout(violations_group)
        
        self.violations_text = QTextEdit()
        self.violations_text.setMaximumHeight(150)
        self.violations_text.setReadOnly(True)
        violations_layout.addWidget(self.violations_text)
        
        layout.addWidget(violations_group)
        
    def create_analysis_tab(self):
        """Create the analysis and performance tab"""
        analysis_widget = QWidget()
        self.tab_widget.addTab(analysis_widget, "Analysis")
        
        layout = QVBoxLayout(analysis_widget)
        
        # Performance comparison
        perf_group = QGroupBox("Performance Comparison")
        perf_layout = QVBoxLayout(perf_group)
        
        self.perf_table = QTableWidget()
        self.perf_table.setColumnCount(4)
        self.perf_table.setHorizontalHeaderLabels(['Heuristic', 'Time (s)', 'Tasks Scheduled', 'Quality Score'])
        header = self.perf_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        perf_layout.addWidget(self.perf_table)
        
        layout.addWidget(perf_group)
        
        # Analysis controls
        controls_layout = QHBoxLayout()
        
        run_all_btn = QPushButton("Run All Heuristics")
        run_all_btn.clicked.connect(self.run_all_heuristics)
        controls_layout.addWidget(run_all_btn)
        
        chart_btn = QPushButton("Generate Performance Chart")
        chart_btn.clicked.connect(self.generate_performance_chart)
        controls_layout.addWidget(chart_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Analysis results
        results_group = QGroupBox("Analysis Results")
        results_layout = QVBoxLayout(results_group)
        
        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        results_layout.addWidget(self.analysis_text)
        
        layout.addWidget(results_group)
        
    def load_initial_data(self):
        """Load the initial scheduling data"""
        try:
            self.data = load_schedule_data()
            self.tasks = self.data['schedule']['tasks']
            self.resources = self.data['schedule']['resources']
            self.time_slots = self.data['schedule']['time_slots']
            self.constraints = self.data['schedule']['constraints']
            
            self.update_problem_display()
            self.status_bar.showMessage("Data loaded successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")
            self.status_bar.showMessage("Failed to load data")
    
    def update_problem_display(self):
        """Update the problem overview display"""
        # Update problem info
        info_text = f"""Problem Overview:
• Tasks: {len(self.tasks)}
• Resources: {len(self.resources)}
• Time slots: {len(self.time_slots['days'])} days, {len(self.time_slots['hours'])} hours per day
• Hard constraints: {len(self.constraints['hard_constraints'])}
• Soft constraints: {len(self.constraints['soft_constraints'])}

Time Slots:
• Days: {', '.join(self.time_slots['days'])}
• Hours: {', '.join(map(str, self.time_slots['hours']))}
• Working hours per day: {self.time_slots['working_hours_per_day']}

Constraints:
• Hard: {', '.join(self.constraints['hard_constraints'])}
• Soft: {', '.join(self.constraints['soft_constraints'])}
"""
        self.problem_info.setPlainText(info_text)
        
        # Update tasks table
        self.tasks_table.setRowCount(len(self.tasks))
        for i, task in enumerate(self.tasks):
            self.tasks_table.setItem(i, 0, QTableWidgetItem(task['id']))
            self.tasks_table.setItem(i, 1, QTableWidgetItem(task['name']))
            self.tasks_table.setItem(i, 2, QTableWidgetItem(str(task['duration'])))
            self.tasks_table.setItem(i, 3, QTableWidgetItem(task.get('priority', 'medium')))
            self.tasks_table.setItem(i, 4, QTableWidgetItem(', '.join(task.get('required_skills', []))))
            self.tasks_table.setItem(i, 5, QTableWidgetItem(', '.join(task.get('dependencies', []))))
        
        # Update resources table
        self.resources_table.setRowCount(len(self.resources))
        for i, resource in enumerate(self.resources):
            self.resources_table.setItem(i, 0, QTableWidgetItem(resource['id']))
            self.resources_table.setItem(i, 1, QTableWidgetItem(resource['name']))
            self.resources_table.setItem(i, 2, QTableWidgetItem(', '.join(resource.get('skills', []))))
            self.resources_table.setItem(i, 3, QTableWidgetItem(str(resource.get('max_hours_per_day', 8))))
    
    def solve_csp(self):
        """Solve the CSP in a separate thread"""
        if self.scheduling_csp is None:
            self.scheduling_csp = SchedulingCSP(self.tasks, self.resources, self.time_slots, self.constraints)
        
        # Get solver parameters
        heuristic = self.heuristic_combo.currentText()
        use_arc_consistency = self.arc_consistency_check.isChecked()
        timeout = self.timeout_spinbox.value()
        
        # Create and start solver thread
        self.solver_thread = SolverThread(self.scheduling_csp, heuristic, use_arc_consistency, timeout)
        self.solver_thread.finished.connect(self.solving_complete)
        self.solver_thread.error.connect(self.solving_error)
        
        # Update UI
        self.solve_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.status_bar.showMessage("Solving CSP...")
        
        self.solver_thread.start()
    
    def solving_complete(self, solution, solve_time, heuristic):
        """Called when solving is complete"""
        self.progress_bar.setVisible(False)
        self.solve_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        if solution:
            self.current_solution = solution
            self.performance_results[heuristic] = [solve_time, len(solution)]
            
            self.status_bar.showMessage(f"Solution found in {solve_time:.2f}s")
            self.update_solution_display()
            self.update_performance_display()
            
            # Show results
            results_text = f"""Solver Results - {heuristic.upper()} Heuristic:
• Solution found: Yes
• Solving time: {solve_time:.2f} seconds
• Tasks scheduled: {len(solution)}
• Heuristic used: {heuristic}

Solution Summary:
"""
            for task_id, assignment in solution.items():
                results_text += f"• {task_id}: {assignment['task_name']} -> {assignment['resource_name']} "
                results_text += f"({assignment['start_day']} {assignment['start_hour']}:00)\n"
            
            self.results_text.setPlainText(results_text)
            
        else:
            self.status_bar.showMessage("No solution found")
            self.results_text.setPlainText(f"No solution found with {heuristic} heuristic")
    
    def solving_error(self, error_msg):
        """Called when solving encounters an error"""
        self.progress_bar.setVisible(False)
        self.solve_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_bar.showMessage("Error occurred")
        QMessageBox.critical(self, "Solver Error", f"Error during solving: {error_msg}")
    
    def stop_solving(self):
        """Stop the solving process"""
        if self.solver_thread and self.solver_thread.isRunning():
            self.solver_thread.terminate()
            self.solver_thread.wait()
        
        self.progress_bar.setVisible(False)
        self.solve_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_bar.showMessage("Solver stopped")
    
    def update_solution_display(self):
        """Update the solution display"""
        if not self.current_solution:
            return
        
        # Update solution table
        self.solution_table.setRowCount(len(self.current_solution))
        for i, (task_id, assignment) in enumerate(self.current_solution.items()):
            self.solution_table.setItem(i, 0, QTableWidgetItem(f"{task_id}: {assignment['task_name']}"))
            self.solution_table.setItem(i, 1, QTableWidgetItem(assignment['resource_name']))
            self.solution_table.setItem(i, 2, QTableWidgetItem(assignment['start_day']))
            self.solution_table.setItem(i, 3, QTableWidgetItem(f"{assignment['start_hour']}:00"))
            self.solution_table.setItem(i, 4, QTableWidgetItem(str(assignment['duration'])))
            self.solution_table.setItem(i, 5, QTableWidgetItem(f"{assignment['end_hour']}:00"))
        
        # Check for violations
        violations = {}
        for task_id, assignment in self.current_solution.items():
            task_violations = get_constraint_violations(assignment, task_id, self.resources, self.tasks, self.current_solution)
            if task_violations:
                violations[task_id] = task_violations
        
        # Display violations
        if violations:
            violations_text = "Constraint Violations Found:\n\n"
            for task_id, task_violations in violations.items():
                violations_text += f"{task_id}:\n"
                for violation in task_violations:
                    violations_text += f"  • {violation}\n"
                violations_text += "\n"
        else:
            violations_text = "No constraint violations found! ✅"
        
        self.violations_text.setPlainText(violations_text)
    
    def update_performance_display(self):
        """Update the performance display"""
        # Update performance table
        self.perf_table.setRowCount(len(self.performance_results))
        for i, (heuristic, (time_taken, tasks_scheduled)) in enumerate(self.performance_results.items()):
            quality_score = 0.0
            if self.current_solution:
                quality_score = calculate_schedule_score(self.current_solution, self.tasks, self.resources)
            
            self.perf_table.setItem(i, 0, QTableWidgetItem(heuristic.upper()))
            self.perf_table.setItem(i, 1, QTableWidgetItem(f"{time_taken:.2f}"))
            self.perf_table.setItem(i, 2, QTableWidgetItem(str(tasks_scheduled)))
            self.perf_table.setItem(i, 3, QTableWidgetItem(f"{quality_score:.3f}"))
    
    def export_solution_json(self):
        """Export solution to JSON file"""
        if not self.current_solution:
            QMessageBox.warning(self, "No Solution", "No solution to export")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Solution", "", "JSON files (*.json);;All files (*.*)"
        )
        
        if filename:
            try:
                export_schedule_to_json(self.current_solution, filename)
                QMessageBox.information(self, "Success", f"Solution exported to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")
    
    def export_solution_csv(self):
        """Export solution to CSV file"""
        if not self.current_solution:
            QMessageBox.warning(self, "No Solution", "No solution to export")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Solution", "", "CSV files (*.csv);;All files (*.*)"
        )
        
        if filename:
            try:
                export_schedule_to_csv(self.current_solution, filename)
                QMessageBox.information(self, "Success", f"Solution exported to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")
    
    def generate_visualizations(self):
        """Generate visualization charts"""
        if not self.current_solution:
            QMessageBox.warning(self, "No Solution", "No solution to visualize")
            return
        
        try:
            # Create output directory
            os.makedirs("output", exist_ok=True)
            
            # Generate charts
            import matplotlib.pyplot as plt
            
            # Gantt chart
            fig1 = create_gantt_chart(self.current_solution, self.tasks, self.resources)
            fig1.savefig("output/gantt_chart.png", dpi=300, bbox_inches='tight')
            plt.close(fig1)
            
            # Resource utilization
            fig2 = create_resource_utilization_chart(self.current_solution, self.resources)
            fig2.savefig("output/resource_utilization.png", dpi=300, bbox_inches='tight')
            plt.close(fig2)
            
            QMessageBox.information(self, "Success", "Visualizations generated in output/ directory")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate visualizations: {str(e)}")
    
    def run_all_heuristics(self):
        """Run all heuristics and compare performance"""
        heuristics = ["mrv", "degree", "combined"]
        
        self.analysis_text.setPlainText("Running all heuristics...\n\n")
        
        for heuristic in heuristics:
            self.analysis_text.append(f"Testing {heuristic.upper()} heuristic...")
            QApplication.processEvents()  # Update UI
            
            try:
                if self.scheduling_csp is None:
                    self.scheduling_csp = SchedulingCSP(self.tasks, self.resources, self.time_slots, self.constraints)
                
                start_time = time.time()
                solution = self.scheduling_csp.solve(heuristic=heuristic)
                solve_time = time.time() - start_time
                
                if solution:
                    quality_score = calculate_schedule_score(solution, self.tasks, self.resources)
                    self.performance_results[heuristic] = [solve_time, len(solution)]
                    
                    self.analysis_text.append(f"  ✓ Solution found in {solve_time:.2f}s, Quality: {quality_score:.3f}")
                else:
                    self.analysis_text.append(f"  ✗ No solution found")
                    
            except Exception as e:
                self.analysis_text.append(f"  ✗ Error: {str(e)}")
        
        self.update_performance_display()
        self.analysis_text.append("\nAll heuristics completed!")
    
    def generate_performance_chart(self):
        """Generate performance comparison chart"""
        if not self.performance_results:
            QMessageBox.warning(self, "No Data", "No performance data to chart")
            return
        
        try:
            os.makedirs("output", exist_ok=True)
            
            from utils.visualization import create_performance_comparison_chart
            import matplotlib.pyplot as plt
            
            fig = create_performance_comparison_chart(self.performance_results)
            fig.savefig("output/performance_comparison.png", dpi=300, bbox_inches='tight')
            plt.close(fig)
            
            QMessageBox.information(self, "Success", "Performance chart generated in output/ directory")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate chart: {str(e)}")


def main():
    """Main function to run the GUI application"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("CSP Scheduling Solver")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("CSCI 384 AI")
    
    # Create and show main window
    window = SchedulerGUI()
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 