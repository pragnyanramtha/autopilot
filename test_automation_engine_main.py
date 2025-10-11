"""
Test script for automation_engine/main.py
Tests the main application loop, workflow polling, and error handling.
"""

import time
import threading
from datetime import datetime

from automation_engine.main import AutomationEngineApp
from shared.communication import MessageBroker
from shared.data_models import Workflow, WorkflowStep


def test_basic_workflow_execution():
    """Test that the engine can receive and execute a basic workflow."""
    print("Test 1: Basic workflow execution")
    print("-" * 60)
    
    # Create message broker and send a test workflow
    broker = MessageBroker()
    broker.clear_messages()  # Clean up any old messages
    
    # Create a simple test workflow
    workflow = Workflow(
        id="test-workflow-001",
        steps=[
            WorkflowStep(type="wait", delay_ms=100),
            WorkflowStep(type="mouse_move", coordinates=(100, 100), delay_ms=50),
            WorkflowStep(type="click", coordinates=(100, 100), delay_ms=50),
        ],
        metadata={"test": "basic_execution"}
    )
    
    print(f"Sending test workflow: {workflow.id}")
    broker.send_workflow(workflow)
    
    # Create and start the automation engine in dry-run mode
    app = AutomationEngineApp(dry_run=True)
    
    # Run the engine in a separate thread for a short time
    def run_engine():
        app.start()
    
    engine_thread = threading.Thread(target=run_engine, daemon=True)
    engine_thread.start()
    
    # Wait for execution
    time.sleep(2)
    
    # Stop the engine
    app.running = False
    time.sleep(0.5)
    
    # Check for status report
    result = broker.receive_status(workflow.id, timeout=1)
    
    if result:
        print(f"\n✓ Workflow executed successfully!")
        print(f"  Status: {result.status}")
        print(f"  Steps completed: {result.steps_completed}")
        print(f"  Duration: {result.duration_ms}ms")
        assert result.status == "success", f"Expected success, got {result.status}"
        assert result.steps_completed == 3, f"Expected 3 steps, got {result.steps_completed}"
    else:
        print("\n✗ No status received")
        assert False, "No execution result received"
    
    print("\nTest 1: PASSED\n")


def test_multiple_workflows():
    """Test that the engine can handle multiple workflows in sequence."""
    print("Test 2: Multiple workflows")
    print("-" * 60)
    
    broker = MessageBroker()
    broker.clear_messages()
    
    # Send multiple workflows
    workflows = []
    for i in range(3):
        workflow = Workflow(
            id=f"test-workflow-{i:03d}",
            steps=[
                WorkflowStep(type="wait", delay_ms=50),
                WorkflowStep(type="mouse_move", coordinates=(i*10, i*10), delay_ms=50),
            ],
            metadata={"test": "multiple_workflows", "index": i}
        )
        workflows.append(workflow)
        broker.send_workflow(workflow)
        print(f"Sent workflow: {workflow.id}")
    
    # Start the engine
    app = AutomationEngineApp(dry_run=True)
    
    def run_engine():
        app.start()
    
    engine_thread = threading.Thread(target=run_engine, daemon=True)
    engine_thread.start()
    
    # Wait for all executions
    time.sleep(3)
    
    # Stop the engine
    app.running = False
    time.sleep(0.5)
    
    # Check all status reports
    success_count = 0
    for workflow in workflows:
        result = broker.receive_status(workflow.id, timeout=0.5)
        if result and result.status == "success":
            success_count += 1
            print(f"✓ {workflow.id}: {result.status}")
    
    print(f"\n✓ {success_count}/{len(workflows)} workflows executed successfully")
    assert success_count == len(workflows), f"Expected {len(workflows)} successes, got {success_count}"
    
    print("\nTest 2: PASSED\n")


def test_error_handling():
    """Test that the engine handles errors gracefully."""
    print("Test 3: Error handling")
    print("-" * 60)
    
    broker = MessageBroker()
    broker.clear_messages()
    
    # Create a workflow with an invalid step
    workflow = Workflow(
        id="test-workflow-error",
        steps=[
            WorkflowStep(type="wait", delay_ms=50),
            WorkflowStep(type="invalid_type", delay_ms=50),  # This should fail
            WorkflowStep(type="wait", delay_ms=50),
        ],
        metadata={"test": "error_handling"}
    )
    
    print(f"Sending workflow with invalid step: {workflow.id}")
    broker.send_workflow(workflow)
    
    # Start the engine
    app = AutomationEngineApp(dry_run=True)
    
    def run_engine():
        app.start()
    
    engine_thread = threading.Thread(target=run_engine, daemon=True)
    engine_thread.start()
    
    # Wait for execution
    time.sleep(2)
    
    # Stop the engine
    app.running = False
    time.sleep(0.5)
    
    # Check status report
    result = broker.receive_status(workflow.id, timeout=1)
    
    if result:
        print(f"\n✓ Error handled gracefully")
        print(f"  Status: {result.status}")
        print(f"  Steps completed: {result.steps_completed}")
        print(f"  Error: {result.error}")
        assert result.status == "failed", f"Expected failed status, got {result.status}"
        assert result.error is not None, "Expected error message"
        assert "invalid_type" in result.error.lower() or "unknown" in result.error.lower()
    else:
        print("\n✗ No status received")
        assert False, "No execution result received"
    
    print("\nTest 3: PASSED\n")


def test_graceful_shutdown():
    """Test that the engine shuts down gracefully."""
    print("Test 4: Graceful shutdown")
    print("-" * 60)
    
    broker = MessageBroker()
    broker.clear_messages()
    
    # Start the engine
    app = AutomationEngineApp(dry_run=True)
    
    def run_engine():
        app.start()
    
    engine_thread = threading.Thread(target=run_engine, daemon=True)
    engine_thread.start()
    
    print("Engine started, waiting 1 second...")
    time.sleep(1)
    
    # Trigger shutdown
    print("Triggering shutdown...")
    app.running = False
    
    # Wait for shutdown
    time.sleep(1)
    
    print("✓ Engine shut down gracefully")
    print("\nTest 4: PASSED\n")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("AUTOMATION ENGINE MAIN APPLICATION TESTS")
    print("=" * 60 + "\n")
    
    try:
        test_basic_workflow_execution()
        test_multiple_workflows()
        test_error_handling()
        test_graceful_shutdown()
        
        print("=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
