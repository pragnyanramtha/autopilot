"""
Integration test demonstrating the complete flow:
AI Brain -> Communication Layer -> Automation Engine -> Status Report
"""

import time
import threading
from datetime import datetime

from ai_brain.main import AIBrainApp
from automation_engine.main import AutomationEngineApp
from shared.communication import MessageBroker


def test_full_integration():
    """
    Test the complete integration between AI Brain and Automation Engine.
    This demonstrates the full workflow from command to execution to status report.
    """
    print("=" * 70)
    print("FULL INTEGRATION TEST: AI Brain <-> Automation Engine")
    print("=" * 70)
    print()
    
    # Clean up any old messages
    broker = MessageBroker()
    broker.clear_messages()
    
    # Start Automation Engine in a separate thread (dry-run mode)
    print("Starting Automation Engine...")
    automation_app = AutomationEngineApp(dry_run=True)
    
    def run_automation_engine():
        automation_app.start()
    
    automation_thread = threading.Thread(target=run_automation_engine, daemon=True)
    automation_thread.start()
    
    # Give it time to start
    time.sleep(1)
    
    # Simulate sending a command from AI Brain (without actually starting AI Brain)
    print("\n" + "-" * 70)
    print("Simulating user command: 'Click at position 500, 300'")
    print("-" * 70)
    
    # Manually create and send a workflow (simulating what AI Brain would do)
    from shared.data_models import Workflow, WorkflowStep
    
    workflow = Workflow(
        id="integration-test-001",
        steps=[
            WorkflowStep(type="mouse_move", coordinates=(500, 300), delay_ms=100),
            WorkflowStep(type="click", coordinates=(500, 300), delay_ms=50),
        ],
        metadata={
            "command": "Click at position 500, 300",
            "source": "integration_test"
        }
    )
    
    print(f"\nAI Brain sending workflow: {workflow.id}")
    broker.send_workflow(workflow)
    
    # Wait for execution
    print("\nWaiting for Automation Engine to execute workflow...")
    time.sleep(3)
    
    # Check for status report
    print("\nChecking for status report from Automation Engine...")
    result = broker.receive_status(workflow.id, timeout=2)
    
    if result:
        print("\n" + "=" * 70)
        print("STATUS REPORT RECEIVED")
        print("=" * 70)
        print(f"Workflow ID: {result.workflow_id}")
        print(f"Status: {result.status}")
        print(f"Steps Completed: {result.steps_completed}")
        print(f"Duration: {result.duration_ms}ms")
        if result.error:
            print(f"Error: {result.error}")
        print("=" * 70)
        
        # Verify success
        assert result.status == "success", f"Expected success, got {result.status}"
        assert result.steps_completed == 2, f"Expected 2 steps, got {result.steps_completed}"
        
        print("\n✓ INTEGRATION TEST PASSED!")
        print("  - AI Brain successfully sent workflow")
        print("  - Automation Engine received and executed workflow")
        print("  - Status report successfully returned to AI Brain")
    else:
        print("\n✗ INTEGRATION TEST FAILED: No status report received")
        assert False, "No status report received"
    
    # Shutdown
    print("\nShutting down components...")
    automation_app.running = False
    time.sleep(1)
    
    print("\n" + "=" * 70)
    print("INTEGRATION TEST COMPLETE")
    print("=" * 70)


def test_error_propagation():
    """
    Test that errors are properly propagated from Automation Engine back to AI Brain.
    """
    print("\n" + "=" * 70)
    print("ERROR PROPAGATION TEST")
    print("=" * 70)
    print()
    
    broker = MessageBroker()
    broker.clear_messages()
    
    # Start Automation Engine
    print("Starting Automation Engine...")
    automation_app = AutomationEngineApp(dry_run=True)
    
    def run_automation_engine():
        automation_app.start()
    
    automation_thread = threading.Thread(target=run_automation_engine, daemon=True)
    automation_thread.start()
    time.sleep(1)
    
    # Send a workflow with an error
    from shared.data_models import Workflow, WorkflowStep
    
    workflow = Workflow(
        id="error-test-001",
        steps=[
            WorkflowStep(type="mouse_move", coordinates=(100, 100), delay_ms=50),
            WorkflowStep(type="invalid_action", delay_ms=50),  # This will fail
            WorkflowStep(type="click", coordinates=(100, 100), delay_ms=50),
        ],
        metadata={"test": "error_propagation"}
    )
    
    print(f"Sending workflow with invalid step: {workflow.id}")
    broker.send_workflow(workflow)
    
    # Wait for execution
    time.sleep(2)
    
    # Check for error status
    result = broker.receive_status(workflow.id, timeout=2)
    
    if result:
        print("\n" + "=" * 70)
        print("ERROR STATUS RECEIVED")
        print("=" * 70)
        print(f"Status: {result.status}")
        print(f"Steps Completed: {result.steps_completed}")
        print(f"Error: {result.error}")
        print("=" * 70)
        
        assert result.status == "failed", f"Expected failed status, got {result.status}"
        assert result.error is not None, "Expected error message"
        
        print("\n✓ ERROR PROPAGATION TEST PASSED!")
        print("  - Error was detected during execution")
        print("  - Error status was properly reported back")
    else:
        print("\n✗ ERROR PROPAGATION TEST FAILED: No status received")
        assert False, "No status received"
    
    # Shutdown
    automation_app.running = False
    time.sleep(1)
    
    print("\n" + "=" * 70)
    print("ERROR PROPAGATION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test_full_integration()
        test_error_propagation()
        
        print("\n" + "=" * 70)
        print("ALL INTEGRATION TESTS PASSED!")
        print("=" * 70)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        raise
