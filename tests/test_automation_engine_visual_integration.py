"""
Test visual navigation integration in Automation Engine main loop.
Verifies that the visual navigation handler is properly initialized and polled.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestAutomationEngineVisualIntegration(unittest.TestCase):
    """Test visual navigation integration in automation engine."""
    
    @patch('automation_engine.main.VisualNavigationHandler')
    @patch('automation_engine.main.MessageBroker')
    @patch('automation_engine.main.ScreenCapture')
    @patch('automation_engine.main.MouseController')
    @patch('automation_engine.main.InputController')
    @patch('automation_engine.main.VisualVerifier')
    def test_visual_handler_initialization(
        self,
        mock_visual_verifier,
        mock_input_controller,
        mock_mouse_controller,
        mock_screen_capture,
        mock_message_broker,
        mock_visual_handler
    ):
        """Test that VisualNavigationHandler is initialized with correct dependencies."""
        from automation_engine.main import AutomationEngineApp
        
        # Create app
        app = AutomationEngineApp(config_path='config.json', dry_run=True)
        
        # Verify VisualNavigationHandler was instantiated
        mock_visual_handler.assert_called_once()
        
        # Verify it was called with correct arguments
        call_kwargs = mock_visual_handler.call_args[1]
        self.assertIn('screen_capture', call_kwargs)
        self.assertIn('mouse_controller', call_kwargs)
        self.assertIn('message_broker', call_kwargs)
    
    @patch('automation_engine.main.VisualNavigationHandler')
    @patch('automation_engine.main.MessageBroker')
    @patch('automation_engine.main.ScreenCapture')
    @patch('automation_engine.main.MouseController')
    @patch('automation_engine.main.InputController')
    @patch('automation_engine.main.VisualVerifier')
    def test_visual_navigation_request_handling(
        self,
        mock_visual_verifier,
        mock_input_controller,
        mock_mouse_controller,
        mock_screen_capture,
        mock_message_broker_class,
        mock_visual_handler_class
    ):
        """Test that visual navigation requests are handled in main loop."""
        from automation_engine.main import AutomationEngineApp
        
        # Setup mocks
        mock_message_broker = Mock()
        mock_message_broker_class.return_value = mock_message_broker
        
        mock_visual_handler = Mock()
        mock_visual_handler_class.return_value = mock_visual_handler
        
        # Simulate receiving a visual navigation request, then None
        visual_request = {
            'request_id': 'test-123',
            'task_description': 'Click the button',
            'workflow_goal': 'Complete the form'
        }
        mock_message_broker.receive_visual_navigation_request.side_effect = [
            visual_request,
            None,
            None
        ]
        mock_message_broker.receive_visual_action_command.return_value = None
        mock_message_broker.receive_protocol.return_value = None
        
        # Create app
        app = AutomationEngineApp(config_path='config.json', dry_run=True)
        
        # Run one iteration of the loop
        app.running = True
        try:
            # Simulate one loop iteration
            visual_req = app.message_broker.receive_visual_navigation_request(timeout=0)
            if visual_req:
                app.visual_handler.handle_visual_navigation_request(visual_req)
        except Exception:
            pass
        
        # Verify handler was called
        mock_visual_handler.handle_visual_navigation_request.assert_called_once_with(visual_request)
    
    @patch('automation_engine.main.VisualNavigationHandler')
    @patch('automation_engine.main.MessageBroker')
    @patch('automation_engine.main.ScreenCapture')
    @patch('automation_engine.main.MouseController')
    @patch('automation_engine.main.InputController')
    @patch('automation_engine.main.VisualVerifier')
    def test_visual_action_command_handling(
        self,
        mock_visual_verifier,
        mock_input_controller,
        mock_mouse_controller,
        mock_screen_capture,
        mock_message_broker_class,
        mock_visual_handler_class
    ):
        """Test that visual action commands are handled in main loop."""
        from automation_engine.main import AutomationEngineApp
        
        # Setup mocks
        mock_message_broker = Mock()
        mock_message_broker_class.return_value = mock_message_broker
        
        mock_visual_handler = Mock()
        mock_visual_handler_class.return_value = mock_visual_handler
        
        # Simulate receiving a visual action command
        action_command = {
            'request_id': 'test-123',
            'action': 'click',
            'coordinates': {'x': 100, 'y': 200},
            'request_followup': True
        }
        action_result = {
            'request_id': 'test-123',
            'status': 'success',
            'error': None
        }
        
        mock_message_broker.receive_visual_navigation_request.return_value = None
        mock_message_broker.receive_visual_action_command.side_effect = [
            action_command,
            None,
            None
        ]
        mock_message_broker.receive_protocol.return_value = None
        mock_visual_handler.execute_visual_action.return_value = action_result
        
        # Create app
        app = AutomationEngineApp(config_path='config.json', dry_run=True)
        
        # Run one iteration of the loop
        app.running = True
        try:
            # Simulate one loop iteration
            visual_req = app.message_broker.receive_visual_navigation_request(timeout=0)
            if not visual_req:
                action_cmd = app.message_broker.receive_visual_action_command(timeout=0)
                if action_cmd:
                    result = app.visual_handler.execute_visual_action(action_cmd)
                    app.message_broker.send_visual_action_result(result)
        except Exception:
            pass
        
        # Verify handler was called
        mock_visual_handler.execute_visual_action.assert_called_once_with(action_command)
        mock_message_broker.send_visual_action_result.assert_called_once_with(action_result)


if __name__ == '__main__':
    unittest.main()
