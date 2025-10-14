"""
Tests for VisualNavigationHandler.
Verifies screen capture, state reporting, and action execution.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from PIL import Image
import base64
import io

from automation_engine.visual_navigation_handler import VisualNavigationHandler


class TestVisualNavigationHandler:
    """Test suite for VisualNavigationHandler."""
    
    @pytest.fixture
    def mock_screen_capture(self):
        """Create mock ScreenCapture."""
        mock = Mock()
        # Create a simple test image
        test_image = Image.new('RGB', (100, 100), color='red')
        mock.capture_screen.return_value = test_image
        mock.get_screen_size.return_value = (1920, 1080)
        return mock
    
    @pytest.fixture
    def mock_mouse_controller(self):
        """Create mock MouseController."""
        mock = Mock()
        mock.get_position.return_value = (500, 300)
        return mock
    
    @pytest.fixture
    def mock_message_broker(self):
        """Create mock MessageBroker."""
        return Mock()
    
    @pytest.fixture
    def handler(self, mock_screen_capture, mock_mouse_controller, mock_message_broker):
        """Create VisualNavigationHandler instance."""
        return VisualNavigationHandler(
            mock_screen_capture,
            mock_mouse_controller,
            mock_message_broker
        )
    
    def test_initialization(self, handler, mock_screen_capture, mock_mouse_controller, mock_message_broker):
        """Test handler initialization stores references correctly."""
        assert handler.screen_capture == mock_screen_capture
        assert handler.mouse_controller == mock_mouse_controller
        assert handler.message_broker == mock_message_broker
    
    def test_capture_current_state(self, handler, mock_screen_capture, mock_mouse_controller):
        """Test capturing current screen state."""
        state = handler.capture_current_state()
        
        # Verify all required fields are present
        assert "screenshot_base64" in state
        assert "mouse_position" in state
        assert "screen_size" in state
        
        # Verify mouse position
        assert state["mouse_position"]["x"] == 500
        assert state["mouse_position"]["y"] == 300
        
        # Verify screen size
        assert state["screen_size"]["width"] == 1920
        assert state["screen_size"]["height"] == 1080
        
        # Verify screenshot is base64 encoded
        assert isinstance(state["screenshot_base64"], str)
        assert len(state["screenshot_base64"]) > 0
        
        # Verify methods were called
        mock_screen_capture.capture_screen.assert_called_once()
        mock_mouse_controller.get_position.assert_called_once()
        mock_screen_capture.get_screen_size.assert_called_once()
    
    def test_handle_visual_navigation_request(self, handler, mock_message_broker):
        """Test handling visual navigation request."""
        request = {
            "request_id": "test-123",
            "task_description": "Click the button",
            "workflow_goal": "Submit form"
        }
        
        handler.handle_visual_navigation_request(request)
        
        # Verify response was sent
        mock_message_broker.send_visual_navigation_response.assert_called_once()
        
        # Verify response structure
        response = mock_message_broker.send_visual_navigation_response.call_args[0][0]
        assert response["request_id"] == "test-123"
        assert "screenshot_base64" in response
        assert "mouse_position" in response
        assert "screen_size" in response
    
    def test_execute_visual_action_click(self, handler, mock_mouse_controller):
        """Test executing click action."""
        command = {
            "request_id": "test-456",
            "action": "click",
            "coordinates": {"x": 800, "y": 600},
            "request_followup": False
        }
        
        result = handler.execute_visual_action(command)
        
        # Verify result
        assert result["request_id"] == "test-456"
        assert result["status"] == "success"
        assert result["error"] is None
        
        # Verify click was executed
        mock_mouse_controller.click.assert_called_once_with(800, 600, button='left')
    
    def test_execute_visual_action_double_click(self, handler, mock_mouse_controller):
        """Test executing double-click action."""
        command = {
            "request_id": "test-789",
            "action": "double_click",
            "coordinates": {"x": 400, "y": 300},
            "request_followup": False
        }
        
        result = handler.execute_visual_action(command)
        
        # Verify result
        assert result["status"] == "success"
        
        # Verify double-click was executed
        mock_mouse_controller.click.assert_called_once_with(400, 300, button='left', clicks=2)
    
    def test_execute_visual_action_right_click(self, handler, mock_mouse_controller):
        """Test executing right-click action."""
        command = {
            "request_id": "test-101",
            "action": "right_click",
            "coordinates": {"x": 600, "y": 400},
            "request_followup": False
        }
        
        result = handler.execute_visual_action(command)
        
        # Verify result
        assert result["status"] == "success"
        
        # Verify right-click was executed
        mock_mouse_controller.click.assert_called_once_with(600, 400, button='right')
    
    def test_execute_visual_action_with_followup(self, handler, mock_screen_capture):
        """Test executing action with followup screenshot."""
        command = {
            "request_id": "test-202",
            "action": "click",
            "coordinates": {"x": 500, "y": 500},
            "request_followup": True
        }
        
        result = handler.execute_visual_action(command)
        
        # Verify result includes screenshot
        assert result["status"] == "success"
        assert result["screenshot_base64"] is not None
        assert isinstance(result["screenshot_base64"], str)
        
        # Verify screenshot was captured twice (once in initial state, once for followup)
        assert mock_screen_capture.capture_screen.call_count >= 1
    
    def test_execute_visual_action_invalid_coordinates(self, handler):
        """Test executing action with out-of-bounds coordinates."""
        command = {
            "request_id": "test-303",
            "action": "click",
            "coordinates": {"x": 5000, "y": 5000},  # Out of bounds
            "request_followup": False
        }
        
        result = handler.execute_visual_action(command)
        
        # Verify error result
        assert result["status"] == "error"
        assert "out of screen bounds" in result["error"]
    
    def test_execute_visual_action_unknown_action(self, handler):
        """Test executing unknown action type."""
        command = {
            "request_id": "test-404",
            "action": "unknown_action",
            "coordinates": {"x": 500, "y": 500},
            "request_followup": False
        }
        
        result = handler.execute_visual_action(command)
        
        # Verify error result
        assert result["status"] == "error"
        assert "Unknown action type" in result["error"]
    
    def test_encode_screenshot(self, handler):
        """Test screenshot encoding to base64."""
        # Create test image
        test_image = Image.new('RGB', (100, 100), color='blue')
        
        # Encode
        encoded = handler._encode_screenshot(test_image)
        
        # Verify it's a valid base64 string
        assert isinstance(encoded, str)
        assert len(encoded) > 0
        
        # Verify it can be decoded back
        decoded_bytes = base64.b64decode(encoded)
        decoded_image = Image.open(io.BytesIO(decoded_bytes))
        assert decoded_image.size == (100, 100)
    
    def test_validate_coordinates_valid(self, handler):
        """Test coordinate validation with valid coordinates."""
        assert handler._validate_coordinates(100, 100, 1920, 1080) is True
        assert handler._validate_coordinates(1000, 500, 1920, 1080) is True
    
    def test_validate_coordinates_invalid(self, handler):
        """Test coordinate validation with invalid coordinates."""
        # Out of bounds
        assert handler._validate_coordinates(2000, 100, 1920, 1080) is False
        assert handler._validate_coordinates(100, 2000, 1920, 1080) is False
        
        # Too close to edges (within margin)
        assert handler._validate_coordinates(2, 100, 1920, 1080) is False
        assert handler._validate_coordinates(100, 2, 1920, 1080) is False
        assert handler._validate_coordinates(1918, 100, 1920, 1080) is False
        assert handler._validate_coordinates(100, 1078, 1920, 1080) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
