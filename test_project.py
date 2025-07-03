"""
Test script for CSP Scheduling Project
Tests all major components and functionality
"""

import sys
import os
import json
import time

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from utils.file_utils import load_schedule_data, export_schedule_to_json, export_schedule_to_csv
        print("✓ File utilities imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import file utilities: {e}")
        return False
    
    try:
        from utils.constraint_utils import get_constraint_violations, calculate_schedule_score
        print("✓ Constraint utilities imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import constraint utilities: {e}")
        return False
    
    try:
        from utils.visualization import create_gantt_chart, create_resource_utilization_chart
        print("✓ Visualization utilities imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import visualization utilities: {e}")
        return False
    
    try:
        from src.csp_solver import SchedulingCSP
        print("✓ CSP solver imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import CSP solver: {e}")
        return False
    
    try:
        from src.scheduler import Scheduler
        print("✓ Scheduler imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import scheduler: {e}")
        return False
    
    try:
        from PySide6.QtWidgets import QApplication
        print("✓ PySide6 imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import PySide6: {e}")
        return False
    
    return True

def test_data_loading():
    """Test data loading functionality"""
    print("\nTesting data loading...")
    
    try:
        from utils.file_utils import load_schedule_data
        
        data = load_schedule_data()
        
        # Check required keys
        required_keys = ['schedule']
        for key in required_keys:
            if key not in data:
                print(f"✗ Missing required key: {key}")
                return False
        
        schedule = data['schedule']
        required_schedule_keys = ['tasks', 'resources', 'time_slots', 'constraints']
        for key in required_schedule_keys:
            if key not in schedule:
                print(f"✗ Missing required schedule key: {key}")
                return False
        
        print(f"✓ Data loaded successfully")
        print(f"  - Tasks: {len(schedule['tasks'])}")
        print(f"  - Resources: {len(schedule['resources'])}")
        print(f"  - Time slots: {len(schedule['time_slots']['days'])} days")
        print(f"  - Constraints: {len(schedule['constraints']['hard_constraints'])} hard, {len(schedule['constraints']['soft_constraints'])} soft")
        
        return True
        
    except Exception as e:
        print(f"✗ Data loading failed: {e}")
        return False

def test_csp_creation():
    """Test CSP creation and basic functionality"""
    print("\nTesting CSP creation...")
    
    try:
        from utils.file_utils import load_schedule_data
        from src.csp_solver import SchedulingCSP
        
        data = load_schedule_data()
        schedule = data['schedule']
        
        csp = SchedulingCSP(
            schedule['tasks'],
            schedule['resources'],
            schedule['time_slots'],
            schedule['constraints']
        )
        
        print("✓ CSP created successfully")
        print(f"  - Variables: {len(csp.variables)}")
        print(f"  - Domains: {len(csp.domains)}")
        print(f"  - Constraints: {len(csp.constraints)}")
        
        return True
        
    except Exception as e:
        print(f"✗ CSP creation failed: {e}")
        return False

def test_constraint_checking():
    """Test constraint checking functionality"""
    print("\nTesting constraint checking...")
    
    try:
        from utils.file_utils import load_schedule_data
        from utils.constraint_utils import get_constraint_violations
        
        data = load_schedule_data()
        schedule = data['schedule']
        
        # Create a sample assignment
        sample_assignment = {
            'resource_id': 'R1',
            'start_day': 'Monday',
            'start_hour': 9,
            'end_hour': 12,
            'task_name': 'Sample Task'
        }
        
        violations = get_constraint_violations(
            sample_assignment,
            'T1',
            schedule['resources'],
            schedule['tasks'],
            {}
        )
        
        print("✓ Constraint checking works")
        print(f"  - Sample violations found: {len(violations)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Constraint checking failed: {e}")
        return False

def test_visualization():
    """Test visualization functionality"""
    print("\nTesting visualization...")
    
    try:
        from utils.visualization import create_gantt_chart, create_resource_utilization_chart
        
        # Create sample data
        sample_solution = {
            'T1': {
                'task_name': 'Task 1',
                'resource_name': 'Resource 1',
                'start_day': 'Monday',
                'start_hour': 9,
                'end_hour': 12,
                'duration': 3
            }
        }
        
        sample_tasks = [{'id': 'T1', 'name': 'Task 1', 'duration': 3}]
        sample_resources = [{'id': 'R1', 'name': 'Resource 1'}]
        
        # Test chart creation (without saving)
        fig1 = create_gantt_chart(sample_solution, sample_tasks, sample_resources)
        fig2 = create_resource_utilization_chart(sample_solution, sample_resources)
        
        print("✓ Visualization functions work")
        print("  - Gantt chart created")
        print("  - Resource utilization chart created")
        
        return True
        
    except Exception as e:
        print(f"✗ Visualization failed: {e}")
        return False

def test_gui_components():
    """Test GUI component imports"""
    print("\nTesting GUI components...")
    
    try:
        from gui.components import (
            ScheduleGridWidget, 
            ConstraintViolationPanel, 
            PerformanceChartWidget,
            TaskEditorWidget,
            ResourceEditorWidget
        )
        print("✓ GUI components imported successfully")
        
        # Test component creation (without showing)
        app = None
        try:
            from PySide6.QtWidgets import QApplication
            app = QApplication.instance()
            if app is None:
                app = QApplication([])
        except:
            pass
        
        if app:
            grid_widget = ScheduleGridWidget()
            violation_panel = ConstraintViolationPanel()
            perf_widget = PerformanceChartWidget()
            task_editor = TaskEditorWidget()
            resource_editor = ResourceEditorWidget()
            
            print("✓ GUI components created successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ GUI component test failed: {e}")
        return False

def test_export_functionality():
    """Test export functionality"""
    print("\nTesting export functionality...")
    
    try:
        from utils.file_utils import export_schedule_to_json, export_schedule_to_csv
        
        # Create sample data
        sample_solution = {
            'T1': {
                'task_name': 'Task 1',
                'resource_name': 'Resource 1',
                'start_day': 'Monday',
                'start_hour': 9,
                'end_hour': 12,
                'duration': 3
            }
        }
        
        # Test JSON export
        export_schedule_to_json(sample_solution, 'test_export.json')
        if os.path.exists('test_export.json'):
            print("✓ JSON export works")
            os.remove('test_export.json')
        
        # Test CSV export
        export_schedule_to_csv(sample_solution, 'test_export.csv')
        if os.path.exists('test_export.csv'):
            print("✓ CSV export works")
            os.remove('test_export.csv')
        
        return True
        
    except Exception as e:
        print(f"✗ Export functionality failed: {e}")
        return False

def main():
    """Run all tests"""
    print("CSP Scheduling Project - Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_data_loading,
        test_csp_creation,
        test_constraint_checking,
        test_visualization,
        test_gui_components,
        test_export_functionality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The project is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 