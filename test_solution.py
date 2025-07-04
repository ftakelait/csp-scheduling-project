#!/usr/bin/env python3
"""
Test script to check if the solution imports work correctly
"""

import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

try:
    print("1. Testing utility imports...")
    from utils.file_utils import load_schedule_data, validate_data_structure
    print("   ✓ File utils imported successfully")
    
    from utils.constraint_utils import check_resource_availability, check_task_dependencies
    print("   ✓ Constraint utils imported successfully")
    
    from utils.visualization import create_gantt_chart, create_resource_utilization_chart
    print("   ✓ Visualization imported successfully")
    
    print("2. Testing CSP solver import...")
    from src.csp_solver import SchedulingCSP
    print("   ✓ CSP solver imported successfully")
    
    print("3. Testing data loading...")
    data = load_schedule_data("data/sample_schedule.json")
    print("   ✓ Data loaded successfully")
    
    print("4. Testing CSP creation...")
    schedule_data = data['schedule']
    csp = SchedulingCSP(
        tasks=schedule_data['tasks'],
        resources=schedule_data['resources'],
        time_slots=schedule_data['time_slots'],
        constraints=schedule_data['constraints']
    )
    print("   ✓ CSP created successfully")
    
    print("5. Testing CSP solve...")
    solution = csp.solve()
    print(f"   ✓ CSP solve completed, solution found: {solution is not None}")
    
    print("\n✅ All tests passed! The solution should work correctly.")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc() 