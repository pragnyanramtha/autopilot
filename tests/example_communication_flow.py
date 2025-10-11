"""
Example demonstrating the complete communication flow between AI Brain and Automation Engine.
Shows how workflows are sent and status is reported back.
"""
import uuid
import time
from shared.communication import MessageBroker
from shared.data_models import Workflow, WorkflowStep, ExecutionResult


def run_complete_flow():
    """Run a complete communication flow demonstration."""
    print("=" * 60)
    print("Communication Flow Example")
    print("=" * 60)
    print("\nThis example demonstrates bidirectional communication:")
    print("1. AI Brain sends workflow to Automation Engine")
    print("2. Automation Engine executes workflow")
    print("3. Automation Engine reports status back to AI Brain")
    print("\n" + "=" * 60)
    
    # Clean up any existing messages
    broker = MessageBroker()
    broker.clear_messages()
    
    # Step 1: AI Brain creates and sends workflow
    print("\n=== STEP 1: AI BRAIN SENDS WORKFLOW ===")
    workflow_id = str(uuid.uuid4())
    workflow = Workflow(
        id=workflow_id,
        steps=[
            WorkflowStep(type="mouse_move", coordinates=(500, 300), delay_ms=200),
            WorkflowStep(type="click", coordinates=(500, 300), data="left", delay_ms=100),
            WorkflowStep(type="type", data="automation test", delay_ms=50),
        ],
        metadata={"description": "Example automation workflow"}
    )
    
    print(f"AI Brain: Sending workflow {workflow_id}")
    broker.send_workflow(workflow)
    print("✓ Workflow sent")
    
    # Step 2: Automation Engine receives and executes
    print("\n=== STEP 2: AUTOMATION ENGINE EXECUTES ===")
    received_workflow = broker.receive_workflow(timeout=1.0)
    
    if received_workflow:
        print(f"Automation Engine: Received workflow {received_workflow.id}")
        print(f"  - Steps: {len(received_workflow.steps)}")
        
        # Simulate execution
        print("Executing workflow...")
        start_time = time.time()
        for i, step in enumerate(received_workflow.steps, 1):
            print(f"  Step {i}: {step.type}")
            time.sleep(0.1)  # Simulate work
        
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Send status back
        result = ExecutionResult(
            workflow_id=received_workflow.id,
            status="success",
            steps_completed=len(received_workflow.steps),
            error=None,
            duration_ms=duration_ms
        )
        broker.send_status(result)
        print(f"✓ Execution complete in {duration_ms}ms")
        print("✓ Status sent back to AI Brain")
    
    # Step 3: AI Brain receives status
    print("\n=== STEP 3: AI BRAIN RECEIVES STATUS ===")
    status = broker.receive_status(workflow_id, timeout=1.0)
    
    if status:
        print(f"AI Brain: Received status for workflow {status.workflow_id}")
        print(f"  - Status: {status.status}")
        print(f"  - Steps completed: {status.steps_completed}/{len(workflow.steps)}")
        print(f"  - Duration: {status.duration_ms}ms")
        if status.error:
            print(f"  - Error: {status.error}")
        print("✓ Communication flow complete!")
    
    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    run_complete_flow()
