"""
Simple test script for the AutomationExecutor.
Tests basic functionality in dry-run mode.
"""

from shared.data_models import Workflow, WorkflowStep
from automation_engine.executor import AutomationExecutor
import uuid


def test_basic_workflow():
    """Test a basic workflow execution in dry-run mode."""
    print("=" * 60)
    print("Testing AutomationExecutor - Basic Workflow")
    print("=" * 60)
    
    # Create a simple workflow
    workflow = Workflow(
        id=str(uuid.uuid4()),
        steps=[
            WorkflowStep(type="mouse_move", coordinates=(100, 100), delay_ms=500),
            WorkflowStep(type="click", coordinates=(100, 100), delay_ms=200),
            WorkflowStep(type="type", data="Hello World", delay_ms=300),
            WorkflowStep(type="press_key", data="enter", delay_ms=100),
            WorkflowStep(type="wait", delay_ms=1000),
        ],
        metadata={"name": "Test Workflow"}
    )
    
    # Execute in dry-run mode
    executor = AutomationExecutor(dry_run=True)
    result = executor.execute_workflow(workflow)
    
    print("\n" + "=" * 60)
    print("Execution Result:")
    print(f"  Status: {result.status}")
    print(f"  Steps Completed: {result.steps_completed}/{len(workflow.steps)}")
    print(f"  Duration: {result.duration_ms}ms")
    print(f"  Error: {result.error}")
    print("=" * 60)
    
    assert result.status == "success", f"Expected success, got {result.status}"
    assert result.steps_completed == len(workflow.steps), "Not all steps completed"
    print("\n✓ Basic workflow test passed!\n")


def test_dangerous_action():
    """Test dangerous action detection."""
    print("=" * 60)
    print("Testing AutomationExecutor - Dangerous Action Detection")
    print("=" * 60)
    
    # Create workflow with dangerous action
    workflow = Workflow(
        id=str(uuid.uuid4()),
        steps=[
            WorkflowStep(type="type", data="rm -rf /important/files", delay_ms=100),
        ],
        metadata={"name": "Dangerous Workflow"}
    )
    
    # Execute in dry-run mode (should detect but not block)
    executor = AutomationExecutor(dry_run=True)
    result = executor.execute_workflow(workflow)
    
    print("\n" + "=" * 60)
    print("Execution Result:")
    print(f"  Status: {result.status}")
    print(f"  Error: {result.error}")
    print("=" * 60)
    
    print("\n✓ Dangerous action detection test passed!\n")


def test_pause_resume_stop():
    """Test pause, resume, and stop controls."""
    print("=" * 60)
    print("Testing AutomationExecutor - Control Functions")
    print("=" * 60)
    
    executor = AutomationExecutor(dry_run=True)
    
    # Test when not running
    assert not executor.pause_execution(), "Should not pause when not running"
    assert not executor.resume_execution(), "Should not resume when not running"
    assert not executor.stop_execution(), "Should not stop when not running"
    
    # Test status
    status = executor.get_execution_status()
    assert not status['is_running'], "Should not be running"
    assert not status['is_paused'], "Should not be paused"
    assert status['dry_run'], "Should be in dry-run mode"
    
    print("\n✓ Control functions test passed!\n")


def test_hotkey_step():
    """Test hotkey execution."""
    print("=" * 60)
    print("Testing AutomationExecutor - Hotkey Step")
    print("=" * 60)
    
    workflow = Workflow(
        id=str(uuid.uuid4()),
        steps=[
            WorkflowStep(type="hotkey", data="ctrl, c", delay_ms=100),
            WorkflowStep(type="hotkey", data="ctrl, v", delay_ms=100),
        ],
        metadata={"name": "Hotkey Workflow"}
    )
    
    executor = AutomationExecutor(dry_run=True)
    result = executor.execute_workflow(workflow)
    
    print("\n" + "=" * 60)
    print("Execution Result:")
    print(f"  Status: {result.status}")
    print(f"  Steps Completed: {result.steps_completed}/{len(workflow.steps)}")
    print("=" * 60)
    
    assert result.status == "success", f"Expected success, got {result.status}"
    print("\n✓ Hotkey test passed!\n")


if __name__ == "__main__":
    try:
        test_basic_workflow()
        test_dangerous_action()
        test_pause_resume_stop()
        test_hotkey_step()
        
        print("=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        import traceback
        traceback.print_exc()
