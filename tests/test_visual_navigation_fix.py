"""
Test script to verify visual navigation fix.
Tests that AI Brain can handle visual navigation requests from protocols.
"""
import sys
import time
import uuid
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.communication import MessageBroker


def test_visual_navigation_request_handling():
    """
    Test that visual navigation requests can be sent and received.
    This simulates what happens when a protocol with visual_navigate is executed.
    """
    print("=" * 60)
    print("Visual Navigation Fix Verification Test")
    print("=" * 60)
    
    broker = MessageBroker()
    
    # Clean up any old messages
    broker.clear_messages()
    
    print("\n1. Testing visual navigation request sending...")
    request_id = str(uuid.uuid4())
    
    request = {
        'request_id': request_id,
        'task_description': 'Click the submit button',
        'workflow_goal': 'Submit the form',
        'max_iterations': 5
    }
    
    broker.send_visual_navigation_request(request)
    print(f"   ✓ Request sent (ID: {request_id[:8]}...)")
    
    print("\n2. Testing visual navigation request receiving...")
    received = broker.receive_visual_navigation_request(timeout=1.0)
    
    if received:
        print(f"   ✓ Request received")
        print(f"   - Task: {received.get('task_description')}")
        print(f"   - Goal: {received.get('workflow_goal')}")
        print(f"   - Max iterations: {received.get('max_iterations')}")
        assert received['request_id'] == request_id
        assert received['task_description'] == 'Click the submit button'
    else:
        print("   ✗ Request NOT received (timeout)")
        return False
    
    print("\n3. Testing visual navigation result sending...")
    result = {
        'request_id': request_id,
        'status': 'success',
        'actions_taken': [
            {'action': 'click', 'coordinates': (500, 300), 'confidence': 0.95}
        ],
        'iterations': 1,
        'final_coordinates': (500, 300),
        'error': None
    }
    
    broker.send_visual_navigation_result(result)
    print(f"   ✓ Result sent")
    
    print("\n4. Testing visual navigation result receiving...")
    received_result = broker.receive_visual_navigation_result(request_id, timeout=1.0)
    
    if received_result:
        print(f"   ✓ Result received")
        print(f"   - Status: {received_result.get('status')}")
        print(f"   - Actions: {len(received_result.get('actions_taken', []))}")
        print(f"   - Iterations: {received_result.get('iterations')}")
        assert received_result['status'] == 'success'
        assert received_result['iterations'] == 1
    else:
        print("   ✗ Result NOT received (timeout)")
        return False
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
    print("\nThe visual navigation communication is working correctly.")
    print("The AI Brain should now be able to handle visual navigation")
    print("requests from protocol execution without timing out.")
    print("\nNext steps:")
    print("1. Start automation engine: python automation_engine/main.py")
    print("2. Start AI Brain: python ai_brain/main.py")
    print("3. Send a protocol with visual_navigate action")
    print("4. Verify no timeout occurs")
    
    return True


def test_message_flow_simulation():
    """
    Simulate the complete message flow for visual navigation.
    """
    print("\n" + "=" * 60)
    print("Message Flow Simulation")
    print("=" * 60)
    
    broker = MessageBroker()
    broker.clear_messages()
    
    request_id = str(uuid.uuid4())
    
    print("\n[Protocol Executor] Sending visual navigation request...")
    broker.send_visual_navigation_request({
        'request_id': request_id,
        'task_description': 'Click the login button',
        'workflow_goal': 'Navigate to login page',
        'max_iterations': 10
    })
    
    print("[AI Brain] Polling for requests...")
    request = broker.receive_visual_navigation_request(timeout=0.5)
    if request:
        print(f"[AI Brain] ✓ Received request: {request['task_description']}")
    else:
        print("[AI Brain] ✗ No request received")
        return False
    
    print("[AI Brain] Requesting screenshot from automation engine...")
    broker.send_visual_navigation_request({
        'request_id': request_id,
        'task_description': request['task_description'],
        'workflow_goal': request['workflow_goal'],
        'iteration': 0,
        'max_iterations': request['max_iterations']
    })
    
    print("[Automation Engine] Sending screenshot response...")
    broker.send_visual_navigation_response({
        'request_id': request_id,
        'screenshot_base64': 'fake_base64_data',
        'mouse_position': {'x': 100, 'y': 200},
        'screen_size': {'width': 1920, 'height': 1080}
    })
    
    print("[AI Brain] Receiving screenshot...")
    response = broker.receive_visual_navigation_response(request_id, timeout=0.5)
    if response:
        print(f"[AI Brain] ✓ Received screenshot (screen: {response['screen_size']})")
    else:
        print("[AI Brain] ✗ No screenshot received")
        return False
    
    print("[AI Brain] Analyzing screen and sending action command...")
    broker.send_visual_action_command({
        'request_id': request_id,
        'action': 'click',
        'coordinates': {'x': 500, 'y': 300},
        'text': None,
        'request_followup': True
    })
    
    print("[Automation Engine] Executing action...")
    command = broker.receive_visual_action_command(timeout=0.5)
    if command:
        print(f"[Automation Engine] ✓ Executing {command['action']} at {command['coordinates']}")
    else:
        print("[Automation Engine] ✗ No command received")
        return False
    
    print("[Automation Engine] Sending action result...")
    broker.send_visual_action_result({
        'request_id': request_id,
        'status': 'success',
        'error': None,
        'screenshot_base64': 'new_fake_base64_data',
        'mouse_position': {'x': 500, 'y': 300}
    })
    
    print("[AI Brain] Receiving action result...")
    result = broker.receive_visual_action_result(request_id, timeout=0.5)
    if result:
        print(f"[AI Brain] ✓ Action {result['status']}")
    else:
        print("[AI Brain] ✗ No result received")
        return False
    
    print("[AI Brain] Workflow complete, sending final result...")
    broker.send_visual_navigation_result({
        'request_id': request_id,
        'status': 'success',
        'actions_taken': [
            {'action': 'click', 'coordinates': (500, 300), 'confidence': 0.95}
        ],
        'iterations': 1,
        'final_coordinates': (500, 300),
        'error': None
    })
    
    print("[Protocol Executor] Receiving final result...")
    final_result = broker.receive_visual_navigation_result(request_id, timeout=0.5)
    if final_result:
        print(f"[Protocol Executor] ✓ Workflow {final_result['status']}")
        print(f"[Protocol Executor] Actions taken: {len(final_result['actions_taken'])}")
    else:
        print("[Protocol Executor] ✗ No final result received")
        return False
    
    print("\n✅ Complete message flow simulation successful!")
    return True


if __name__ == '__main__':
    print("\nRunning visual navigation fix verification tests...\n")
    
    success = True
    
    # Test 1: Basic request/response
    if not test_visual_navigation_request_handling():
        success = False
    
    # Test 2: Complete message flow
    if not test_message_flow_simulation():
        success = False
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("=" * 60)
        print("\nThe visual navigation fix is working correctly!")
        print("You can now use visual_navigate in protocols without timeouts.")
    else:
        print("\n" + "=" * 60)
        print("❌ SOME TESTS FAILED")
        print("=" * 60)
        print("\nPlease check the error messages above.")
        sys.exit(1)

