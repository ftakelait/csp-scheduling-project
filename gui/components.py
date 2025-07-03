"""
Reusable GUI Components for CSP Scheduling Application
Modern PySide6-based components for better user experience
"""

import sys
import os
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime

# Add the project root to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, 
    QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit, QComboBox,
    QSpinBox, QCheckBox, QGroupBox, QFrame, QScrollArea, QSizePolicy,
    QProgressBar, QSlider, QSplitter, QMessageBox, QFileDialog,
    QLineEdit, QTextBrowser, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PySide6.QtGui import QFont, QPalette, QColor, QPixmap, QPainter, QBrush

from utils.constraint_utils import get_constraint_violations, calculate_schedule_score
from utils.visualization import create_gantt_chart, create_resource_utilization_chart


class ScheduleGridWidget(QWidget):
    """Interactive schedule grid display widget"""
    
    task_selected = pyqtSignal(str)  # Emits task_id when a task is selected
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.schedule_data = {}
        self.tasks = []
        self.resources = []
        self.time_slots = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the schedule grid UI"""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Schedule Grid"))
        header_layout.addStretch()
        
        # Zoom controls
        zoom_label = QLabel("Zoom:")
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(50, 200)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.update_zoom)
        
        header_layout.addWidget(zoom_label)
        header_layout.addWidget(self.zoom_slider)
        layout.addLayout(header_layout)
        
        # Schedule table
        self.schedule_table = QTableWidget()
        self.schedule_table.setAlternatingRowColors(True)
        self.schedule_table.itemClicked.connect(self.on_cell_clicked)
        layout.addWidget(self.schedule_table)
        
        # Status bar
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
    def update_schedule(self, schedule_data, tasks, resources, time_slots):
        """Update the schedule display with new data"""
        self.schedule_data = schedule_data
        self.tasks = tasks
        self.resources = resources
        self.time_slots = time_slots
        
        self.populate_table()
        
    def populate_table(self):
        """Populate the schedule table"""
        if not self.schedule_data:
            return
            
        # Setup table structure
        days = self.time_slots.get('days', [])
        hours = self.time_slots.get('hours', [])
        
        # Set table dimensions
        self.schedule_table.setRowCount(len(self.resources))
        self.schedule_table.setColumnCount(len(days) * len(hours))
        
        # Set headers
        headers = []
        for day in days:
            for hour in hours:
                headers.append(f"{day} {hour}:00")
        self.schedule_table.setHorizontalHeaderLabels(headers)
        
        # Set row labels (resources)
        resource_labels = [f"{r['id']}: {r['name']}" for r in self.resources]
        self.schedule_table.setVerticalHeaderLabels(resource_labels)
        
        # Populate cells
        for resource_idx, resource in enumerate(self.resources):
            for day_idx, day in enumerate(days):
                for hour_idx, hour in enumerate(hours):
                    col_idx = day_idx * len(hours) + hour_idx
                    
                    # Find task assigned to this resource at this time
                    task_info = self.find_task_at_time(resource['id'], day, hour)
                    
                    if task_info:
                        item = QTableWidgetItem(task_info)
                        item.setBackground(QColor(200, 255, 200))  # Light green
                        item.setToolTip(f"Task: {task_info}")
                    else:
                        item = QTableWidgetItem("")
                        item.setBackground(QColor(240, 240, 240))  # Light gray
                    
                    self.schedule_table.setItem(resource_idx, col_idx, item)
        
        # Resize columns
        header = self.schedule_table.horizontalHeader()
        for i in range(self.schedule_table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.Fixed)
            header.resizeSection(i, 80)
            
    def find_task_at_time(self, resource_id, day, hour):
        """Find task assigned to resource at specific time"""
        for task_id, assignment in self.schedule_data.items():
            if (assignment['resource_id'] == resource_id and 
                assignment['start_day'] == day and 
                assignment['start_hour'] <= hour < assignment['end_hour']):
                return f"{task_id}: {assignment['task_name']}"
        return None
        
    def on_cell_clicked(self, item):
        """Handle cell click events"""
        if item.text():
            # Extract task ID from cell text
            task_id = item.text().split(':')[0]
            self.task_selected.emit(task_id)
            self.status_label.setText(f"Selected task: {task_id}")
            
    def update_zoom(self, value):
        """Update zoom level"""
        header = self.schedule_table.horizontalHeader()
        new_width = int(80 * value / 100)
        for i in range(self.schedule_table.columnCount()):
            header.resizeSection(i, new_width)


class ConstraintViolationPanel(QWidget):
    """Panel for displaying constraint violations"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the constraint violation panel UI"""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Constraint Violations"))
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_violations)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Violations list
        self.violations_list = QListWidget()
        layout.addWidget(self.violations_list)
        
        # Summary
        self.summary_label = QLabel("No violations found")
        layout.addWidget(self.summary_label)
        
    def update_violations(self, schedule_data, tasks, resources):
        """Update the violations display"""
        self.schedule_data = schedule_data
        self.tasks = tasks
        self.resources = resources
        
        self.refresh_violations()
        
    def refresh_violations(self):
        """Refresh the violations list"""
        self.violations_list.clear()
        
        if not self.schedule_data:
            self.summary_label.setText("No schedule data")
            return
            
        all_violations = []
        
        # Check violations for each task
        for task_id, assignment in self.schedule_data.items():
            violations = get_constraint_violations(
                assignment, task_id, self.resources, self.tasks, self.schedule_data
            )
            if violations:
                all_violations.extend([(task_id, v) for v in violations])
        
        # Display violations
        if all_violations:
            for task_id, violation in all_violations:
                item = QListWidgetItem(f"{task_id}: {violation}")
                item.setBackground(QColor(255, 200, 200))  # Light red
                self.violations_list.addItem(item)
            
            self.summary_label.setText(f"Found {len(all_violations)} violations")
        else:
            self.summary_label.setText("No violations found! ✅")


class PerformanceChartWidget(QWidget):
    """Widget for displaying performance charts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.performance_data = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the performance chart widget UI"""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Performance Analysis"))
        
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["Time Comparison", "Quality Comparison", "Tasks Scheduled"])
        self.chart_type_combo.currentTextChanged.connect(self.update_chart)
        header_layout.addWidget(self.chart_type_combo)
        
        self.generate_btn = QPushButton("Generate Chart")
        self.generate_btn.clicked.connect(self.generate_chart)
        header_layout.addWidget(self.generate_btn)
        
        layout.addLayout(header_layout)
        
        # Chart display area
        self.chart_display = QTextBrowser()
        self.chart_display.setMaximumHeight(300)
        layout.addWidget(self.chart_display)
        
    def update_performance_data(self, performance_data):
        """Update performance data"""
        self.performance_data = performance_data
        self.update_chart()
        
    def update_chart(self):
        """Update the chart display"""
        if not self.performance_data:
            self.chart_display.setPlainText("No performance data available")
            return
            
        chart_type = self.chart_type_combo.currentText()
        
        if chart_type == "Time Comparison":
            self.display_time_chart()
        elif chart_type == "Quality Comparison":
            self.display_quality_chart()
        elif chart_type == "Tasks Scheduled":
            self.display_tasks_chart()
            
    def display_time_chart(self):
        """Display time comparison chart"""
        chart_text = "Time Comparison (seconds):\n\n"
        
        for heuristic, (time_taken, tasks_scheduled) in self.performance_data.items():
            chart_text += f"{heuristic.upper()}: {time_taken:.2f}s\n"
            chart_text += "█" * int(time_taken * 10) + "\n\n"
            
        self.chart_display.setPlainText(chart_text)
        
    def display_quality_chart(self):
        """Display quality comparison chart"""
        chart_text = "Quality Score Comparison:\n\n"
        
        for heuristic, (time_taken, tasks_scheduled) in self.performance_data.items():
            # Calculate quality score (placeholder)
            quality_score = tasks_scheduled / 10.0  # Simple metric
            chart_text += f"{heuristic.upper()}: {quality_score:.3f}\n"
            chart_text += "█" * int(quality_score * 20) + "\n\n"
            
        self.chart_display.setPlainText(chart_text)
        
    def display_tasks_chart(self):
        """Display tasks scheduled comparison chart"""
        chart_text = "Tasks Scheduled Comparison:\n\n"
        
        for heuristic, (time_taken, tasks_scheduled) in self.performance_data.items():
            chart_text += f"{heuristic.upper()}: {tasks_scheduled} tasks\n"
            chart_text += "█" * tasks_scheduled + "\n\n"
            
        self.chart_display.setPlainText(chart_text)
        
    def generate_chart(self):
        """Generate and save performance chart"""
        if not self.performance_data:
            QMessageBox.warning(self, "No Data", "No performance data to chart")
            return
            
        try:
            os.makedirs("output", exist_ok=True)
            
            from utils.visualization import create_performance_comparison_chart
            import matplotlib.pyplot as plt
            
            fig = create_performance_comparison_chart(self.performance_data)
            fig.savefig("output/performance_comparison.png", dpi=300, bbox_inches='tight')
            plt.close(fig)
            
            QMessageBox.information(self, "Success", "Performance chart generated in output/ directory")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate chart: {str(e)}")


class TaskEditorWidget(QWidget):
    """Widget for editing task properties"""
    
    task_updated = pyqtSignal(str, dict)  # Emits task_id and updated data
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_task = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the task editor UI"""
        layout = QVBoxLayout(self)
        
        # Header
        layout.addWidget(QLabel("Task Editor"))
        
        # Task selection
        selection_layout = QHBoxLayout()
        selection_layout.addWidget(QLabel("Select Task:"))
        self.task_combo = QComboBox()
        self.task_combo.currentTextChanged.connect(self.on_task_selected)
        selection_layout.addWidget(self.task_combo)
        layout.addLayout(selection_layout)
        
        # Task properties
        self.properties_group = QGroupBox("Task Properties")
        properties_layout = QGridLayout(self.properties_group)
        
        # Name
        properties_layout.addWidget(QLabel("Name:"), 0, 0)
        self.name_edit = QLineEdit()
        properties_layout.addWidget(self.name_edit, 0, 1)
        
        # Duration
        properties_layout.addWidget(QLabel("Duration (hours):"), 1, 0)
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setRange(1, 24)
        properties_layout.addWidget(self.duration_spinbox, 1, 1)
        
        # Priority
        properties_layout.addWidget(QLabel("Priority:"), 2, 0)
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["low", "medium", "high"])
        properties_layout.addWidget(self.priority_combo, 2, 1)
        
        # Skills
        properties_layout.addWidget(QLabel("Required Skills:"), 3, 0)
        self.skills_edit = QLineEdit()
        self.skills_edit.setPlaceholderText("skill1, skill2, skill3")
        properties_layout.addWidget(self.skills_edit, 3, 1)
        
        # Dependencies
        properties_layout.addWidget(QLabel("Dependencies:"), 4, 0)
        self.dependencies_edit = QLineEdit()
        self.dependencies_edit.setPlaceholderText("task1, task2")
        properties_layout.addWidget(self.dependencies_edit, 4, 1)
        
        layout.addWidget(self.properties_group)
        
        # Update button
        self.update_btn = QPushButton("Update Task")
        self.update_btn.clicked.connect(self.update_task)
        layout.addWidget(self.update_btn)
        
        layout.addStretch()
        
    def set_tasks(self, tasks):
        """Set the list of tasks for editing"""
        self.tasks = tasks
        self.task_combo.clear()
        self.task_combo.addItems([task['id'] for task in tasks])
        
    def on_task_selected(self, task_id):
        """Handle task selection"""
        if not task_id:
            return
            
        # Find the selected task
        self.current_task = next((task for task in self.tasks if task['id'] == task_id), None)
        
        if self.current_task:
            self.name_edit.setText(self.current_task.get('name', ''))
            self.duration_spinbox.setValue(self.current_task.get('duration', 1))
            self.priority_combo.setCurrentText(self.current_task.get('priority', 'medium'))
            self.skills_edit.setText(', '.join(self.current_task.get('required_skills', [])))
            self.dependencies_edit.setText(', '.join(self.current_task.get('dependencies', [])))
            
    def update_task(self):
        """Update the current task"""
        if not self.current_task:
            return
            
        # Collect updated data
        updated_data = {
            'name': self.name_edit.text(),
            'duration': self.duration_spinbox.value(),
            'priority': self.priority_combo.currentText(),
            'required_skills': [s.strip() for s in self.skills_edit.text().split(',') if s.strip()],
            'dependencies': [d.strip() for d in self.dependencies_edit.text().split(',') if d.strip()]
        }
        
        # Emit signal
        self.task_updated.emit(self.current_task['id'], updated_data)
        
        QMessageBox.information(self, "Success", f"Task {self.current_task['id']} updated successfully")


class ResourceEditorWidget(QWidget):
    """Widget for editing resource properties"""
    
    resource_updated = pyqtSignal(str, dict)  # Emits resource_id and updated data
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_resource = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the resource editor UI"""
        layout = QVBoxLayout(self)
        
        # Header
        layout.addWidget(QLabel("Resource Editor"))
        
        # Resource selection
        selection_layout = QHBoxLayout()
        selection_layout.addWidget(QLabel("Select Resource:"))
        self.resource_combo = QComboBox()
        self.resource_combo.currentTextChanged.connect(self.on_resource_selected)
        selection_layout.addWidget(self.resource_combo)
        layout.addLayout(selection_layout)
        
        # Resource properties
        self.properties_group = QGroupBox("Resource Properties")
        properties_layout = QGridLayout(self.properties_group)
        
        # Name
        properties_layout.addWidget(QLabel("Name:"), 0, 0)
        self.name_edit = QLineEdit()
        properties_layout.addWidget(self.name_edit, 0, 1)
        
        # Skills
        properties_layout.addWidget(QLabel("Skills:"), 1, 0)
        self.skills_edit = QLineEdit()
        self.skills_edit.setPlaceholderText("skill1, skill2, skill3")
        properties_layout.addWidget(self.skills_edit, 1, 1)
        
        # Max hours per day
        properties_layout.addWidget(QLabel("Max Hours/Day:"), 2, 0)
        self.max_hours_spinbox = QSpinBox()
        self.max_hours_spinbox.setRange(1, 24)
        self.max_hours_spinbox.setValue(8)
        properties_layout.addWidget(self.max_hours_spinbox, 2, 1)
        
        # Availability
        properties_layout.addWidget(QLabel("Available Days:"), 3, 0)
        self.availability_edit = QLineEdit()
        self.availability_edit.setPlaceholderText("Monday, Tuesday, Wednesday")
        properties_layout.addWidget(self.availability_edit, 3, 1)
        
        layout.addWidget(self.properties_group)
        
        # Update button
        self.update_btn = QPushButton("Update Resource")
        self.update_btn.clicked.connect(self.update_resource)
        layout.addWidget(self.update_btn)
        
        layout.addStretch()
        
    def set_resources(self, resources):
        """Set the list of resources for editing"""
        self.resources = resources
        self.resource_combo.clear()
        self.resource_combo.addItems([resource['id'] for resource in resources])
        
    def on_resource_selected(self, resource_id):
        """Handle resource selection"""
        if not resource_id:
            return
            
        # Find the selected resource
        self.current_resource = next((r for r in self.resources if r['id'] == resource_id), None)
        
        if self.current_resource:
            self.name_edit.setText(self.current_resource.get('name', ''))
            self.skills_edit.setText(', '.join(self.current_resource.get('skills', [])))
            self.max_hours_spinbox.setValue(self.current_resource.get('max_hours_per_day', 8))
            self.availability_edit.setText(', '.join(self.current_resource.get('available_days', [])))
            
    def update_resource(self):
        """Update the current resource"""
        if not self.current_resource:
            return
            
        # Collect updated data
        updated_data = {
            'name': self.name_edit.text(),
            'skills': [s.strip() for s in self.skills_edit.text().split(',') if s.strip()],
            'max_hours_per_day': self.max_hours_spinbox.value(),
            'available_days': [d.strip() for d in self.availability_edit.text().split(',') if d.strip()]
        }
        
        # Emit signal
        self.resource_updated.emit(self.current_resource['id'], updated_data)
        
        QMessageBox.information(self, "Success", f"Resource {self.current_resource['id']} updated successfully") 