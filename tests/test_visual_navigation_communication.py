"""
Tests for visual navigation communication in MessageBroker.
"""
import pytest
import time
import uuid
from shared.communication import MessageBroker, CommunicationError


@pytest.fixture
def message_broker(tmp_path):
    """Create a MessageBroker with temporary directory."""
    broker = MessageBroker(base_dir=str(tmp_path / "messages"))
    yield broker
    broker.clear_messages()


def test_visual_navigation_request_response(message_broker):
    """Test sending and receiving visual navigation requests and responses."""
    # Create a request
    request_id = str(uuid.uuid4())
    request = {
        "request_id": request_id,
        "task_description": "Click the submit button",
        "workflow_goal": "Submit the form",
        "iteration": 1,
        "max_iterations": 10
    }
    
    # Send request
    message_broker.send_visual_navigation_request(request)
    
    # Receive request
    received_request = message_broker.receive_visual_navigation_request(timeout=1.0)
    assert received_request is not None
    assert received_request["request_id"] == request_id
    assert received_request["task_description"] == "Click the submit button"
    assert received_request["type"] == "visual_navigation_request"
    
    # Create a response
    response = {
        "request_id": request_id,
        "screenshot_base64": "fake_base64_data",
        "mouse_position": {"x": 100, "y": 200},
        "screen_size": {"width": 1920, "height": 1080}
    }
    
    # Send response
    message_broker.send_visual_navigation_response(response)
    
    # Receive response
    received_response = message_broker.receive_visual_navigation_response(request_id, timeout=1.0)
    assert received_response is not None
    assert received_response["request_id"] == request_id
    assert received_response["screenshot_base64"] == "fake_base64_data"
    assert received_response["mouse_position"]["x"] == 100
    assert received_response["type"] == "visual_navigation_response"


def test_visual_action_command_result(message_broker):
    """Test sending and receiving visual action commands and results."""
    # Create a command
    request_id = str(uuid.uuid4())
    command = {
        "request_id": request_id,
        "action": "click",
        "coordinates": {"x": 500, "y": 300},
        "text": None,
        "request_followup": True
    }
    
    # Send command
    message_broker.send_visual_action_command(command)
    
    # Receive command
    received_command = message_broker.receive_visual_action_command(timeout=1.0)
    assert received_command is not None
    assert received_command["request_id"] == request_id
    assert received_command["action"] == "click"
    assert received_command["coordinates"]["x"] == 500
    assert received_command["type"] == "visual_action_command"
    
    # Create a result
    result = {
        "request_id": request_id,
        "status": "success",
        "error": None,
        "screenshot_base64": "new_screenshot_data",
        "mouse_position": {"x": 500, "y": 300}
    }
    
    # Send result
    message_broker.send_visual_action_result(result)
    
    # Receive result
    received_result = message_broker.receive_visual_action_result(request_id, timeout=1.0)
    assert received_result is not None
    assert received_result["request_id"] == request_id
    assert received_result["status"] == "success"
    assert received_result["screenshot_base64"] == "new_screenshot_data"
    assert received_result["type"] == "visual_action_result"


def test_visual_navigation_timeout(message_broker):
    """Test timeout behavior for visual navigation messages."""
    # Try to receive request with no messages
    request = message_broker.receive_visual_navigation_request(timeout=0.2)
    assert request is None
    
    # Try to receive response with no messages
    response = message_broker.receive_visual_navigation_response("nonexistent_id", timeout=0.2)
    assert response is None
    
    # Try to receive command with no messages
    command = message_broker.receive_visual_action_command(timeout=0.2)
    assert command is None
    
    # Try to receive result with no messages
    result = message_broker.receive_visual_action_result("nonexistent_id", timeout=0.2)
    assert result is None


def test_visual_navigation_clear_messages(message_broker):
    """Test clearing visual navigation messages."""
    # Send some messages
    request_id = str(uuid.uuid4())
    message_broker.send_visual_navigation_request({
        "request_id": request_id,
        "task_description": "Test task"
    })
    message_broker.send_visual_action_command({
        "request_id": request_id,
        "action": "click",
        "coordinates": {"x": 100, "y": 100}
    })
    
    # Clear all messages
    message_broker.clear_messages()
    
    # Verify messages are cleared
    request = message_broker.receive_visual_navigation_request(timeout=0.1)
    assert request is None
    
    command = message_broker.receive_visual_action_command(timeout=0.1)
    assert command is None


def test_visual_navigation_message_structure(message_broker):
    """Test that message structures match the design specification."""
    request_id = str(uuid.uuid4())
    
    # Test request structure
    request = {
        "request_id": request_id,
        "task_description": "Click the submit button",
        "workflow_goal": "Submit the form",
        "iteration": 1,
        "max_iterations": 10
    }
    message_broker.send_visual_navigation_request(request)
    received = message_broker.receive_visual_navigation_request(timeout=1.0)
    
    assert "type" in received
    assert "request_id" in received
    assert "task_description" in received
    assert "workflow_goal" in received
    assert "iteration" in received
    assert "max_iterations" in received
    assert "timestamp" in received
    
    # Test response structure
    response = {
        "request_id": request_id,
        "screenshot_base64": "base64_data",
        "mouse_position": {"x": 100, "y": 200},
        "screen_size": {"width": 1920, "height": 1080}
    }
    message_broker.send_visual_navigation_response(response)
    received = message_broker.receive_visual_navigation_response(request_id, timeout=1.0)
    
    assert "type" in received
    assert "request_id" in received
    assert "screenshot_base64" in received
    assert "mouse_position" in received
    assert "screen_size" in received
    assert "timestamp" in received
    
    # Test command structure
    command = {
        "request_id": request_id,
        "action": "click",
        "coordinates": {"x": 500, "y": 300},
        "text": None,
        "request_followup": True
    }
    message_broker.send_visual_action_command(command)
    received = message_broker.receive_visual_action_command(timeout=1.0)
    
    assert "type" in received
    assert "request_id" in received
    assert "action" in received
    assert "coordinates" in received
    assert "request_followup" in received
    assert "timestamp" in received
    
    # Test result structure
    result = {
        "request_id": request_id,
        "status": "success",
        "error": None,
        "screenshot_base64": "new_data",
        "mouse_position": {"x": 500, "y": 300}
    }
    message_broker.send_visual_action_result(result)
    received = message_broker.receive_visual_action_result(request_id, timeout=1.0)
    
    assert "type" in received
    assert "request_id" in received
    assert "status" in received
    assert "mouse_position" in received
    assert "timestamp" in received


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
