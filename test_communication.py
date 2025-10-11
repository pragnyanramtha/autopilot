"""
Test script for the communication module.
Verifies workflow and status message passing.
"""
import uuid
from datetime import datetime
from shared.communication import MessageBroker, CommunicationError
from shared.data_models import Workflow, WorkflowStep, ExecutionResult


def test_workflow_communication():
    """Test sending and receiving workflows."""
    print("Testing workflow communication...")
    
    # Create a message broker
    broker = MessageBroker("shared/messages_test")
    broker.clear_messages()
    
    # Create a test workflow
    workflow_id = str(uuid.uuid4())
    workflow = Workflow(
        id=workflow_id,
        steps=[
            WorkflowStep(
                type="mouse_move",
                coordinates=(100, 200),
                delay_ms=500
            ),
            WorkflowStep(
                type="click",
                coordinates=(100, 200),
                data="left",
                delay_ms=100
            ),
            WorkflowStep(
                type="type",
                data="Hello World",
                delay_ms=50
            )
        ],
        metadata={"description": "Test workflow"}
    )
    
    # Send workflow
    try:
        broker.send_workflow(workflow)
        print(f"✓ Sent workflow {workflow_id}")
    except CommunicationError as e:
        print(f"✗ Failed to send workflow: {e}")
        return False
    
    # Receive workflow
    try:
        received_workflow = broker.receive_workflow(timeout=1.0)
        if received_workflow:
            print(f"✓ Received workflow {received_workflow.id}")
            
            # Verify data integrity
            assert received_workflow.id == workflow_id
            assert len(received_workflow.steps) == 3
            assert received_workflow.steps[0].type == "mouse_move"
            assert received_workflow.steps[0].coordinates == (100, 200)
            assert received_workflow.steps[1].type == "click"
            assert received_workflow.steps[2].type == "type"
            assert received_workflow.steps[2].data == "Hello World"
            assert received_workflow.metadata["description"] == "Test workflow"
            
            print("✓ Workflow data integrity verified")
        else:
            print("✗ No workflow received")
            return False
    except CommunicationError as e:
        print(f"✗ Failed to receive workflow: {e}")
        return False
    
    # Clean up
    broker.clear_messages()
    return True


def test_status_communication():
    """Test sending and receiving execution status."""
    print("\nTesting status communication...")
    
    # Create a message broker
    broker = MessageBroker("shared/messages_test")
    broker.clear_messages()
    
    # Create a test execution result
    workflow_id = str(uuid.uuid4())
    result = ExecutionResult(
        workflow_id=workflow_id,
        status="success",
        steps_completed=3,
        error=None,
        duration_ms=1500
    )
    
    # Send status
    try:
        broker.send_status(result)
        print(f"✓ Sent status for workflow {workflow_id}")
    except CommunicationError as e:
        print(f"✗ Failed to send status: {e}")
        return False
    
    # Receive status
    try:
        received_status = broker.receive_status(workflow_id, timeout=1.0)
        if received_status:
            print(f"✓ Received status for workflow {received_status.workflow_id}")
            
            # Verify data integrity
            assert received_status.workflow_id == workflow_id
            assert received_status.status == "success"
            assert received_status.steps_completed == 3
            assert received_status.error is None
            assert received_status.duration_ms == 1500
            
            print("✓ Status data integrity verified")
        else:
            print("✗ No status received")
            return False
    except CommunicationError as e:
        print(f"✗ Failed to receive status: {e}")
        return False
    
    # Clean up
    broker.clear_messages()
    return True


def test_error_status():
    """Test sending and receiving error status."""
    print("\nTesting error status communication...")
    
    broker = MessageBroker("shared/messages_test")
    broker.clear_messages()
    
    workflow_id = str(uuid.uuid4())
    result = ExecutionResult(
        workflow_id=workflow_id,
        status="failed",
        steps_completed=2,
        error="Element not found on screen",
        duration_ms=800
    )
    
    broker.send_status(result)
    received_status = broker.receive_status(workflow_id, timeout=1.0)
    
    if received_status:
        assert received_status.status == "failed"
        assert received_status.error == "Element not found on screen"
        print("✓ Error status communication verified")
        broker.clear_messages()
        return True
    else:
        print("✗ Failed to receive error status")
        return False


def test_no_message_timeout():
    """Test timeout behavior when no messages are available."""
    print("\nTesting timeout behavior...")
    
    broker = MessageBroker("shared/messages_test")
    broker.clear_messages()
    
    # Try to receive workflow with no messages
    workflow = broker.receive_workflow(timeout=0.5)
    if workflow is None:
        print("✓ Timeout behavior works correctly (no workflow)")
    else:
        print("✗ Expected None but received workflow")
        return False
    
    # Try to receive status with no messages
    status = broker.receive_status("nonexistent-id", timeout=0.5)
    if status is None:
        print("✓ Timeout behavior works correctly (no status)")
    else:
        print("✗ Expected None but received status")
        return False
    
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Communication Module Test Suite")
    print("=" * 60)
    
    tests = [
        test_workflow_communication,
        test_status_communication,
        test_error_status,
        test_no_message_timeout
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("\n✓ All tests passed!")
    else:
        print(f"\n✗ {failed} test(s) failed")
