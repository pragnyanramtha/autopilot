"""
Test AI Brain visual navigation integration.

This test verifies that the AI Brain correctly integrates visual navigation
functionality including command detection, workflow orchestration, and
critical action confirmation.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch, call
from ai_brain.main import AIBrainApp
from ai_brain.gemini_client import CommandIntent
from ai_brain.vision_navigator import VisionNavigationResult
from PIL import Image
import io
import base64


class TestAIBrainVisualNavigation(unittest.TestCase):
    """Test AI Brain visual navigation integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = AIBrainApp()
        self.app.config = {
            'visual_navigation': {
                'enabled': True,
                'vision_model': 'gemini-2.0-flash-exp',
                'max_iterations': 10,
                'confidence_threshold': 0.6,
                'require_confirmation_for_critical': True,
                'critical_keywords': ['delete', 'format', 'shutdown']
            }
        }
        
        # Mock components
        self.app.gemini_client = Mock()
        self.app.message_broker = Mock()
        self.app.vision_navigator = Mock()
        self.app.console = Mock()
    
    def test_requires_visual_navigation_with_keywords(self):
        """Test that visual navigation is triggered by keywords."""
        intent = CommandIntent(
            action='click',
            target='submit button',
            parameters={},
            confidence=0.9
        )
        
        # Should require visual navigation with "click the" keyword
        result = self.app._requires_visual_navigation(intent, "click the submit button")
        self.assertTrue(result)
    
    def test_requires_visual_navigation_without_coordinates(self):
        """Test that visual navigation is used when no coordinates provided."""
        intent = CommandIntent(
            action='click',
            target='button',
            parameters={},
            confidence=0.9
        )
        
        # Should require visual navigation for button without coordinates
        result = self.app._requires_visual_navigation(intent, "click button")
        self.assertTrue(result)
    
    def test_no_visual_navigation_with_coordinates(self):
        """Test that visual navigation is not used when coordinates are provided."""
        intent = CommandIntent(
            action='click',
            target='screen',
            parameters={'x': 100, 'y': 200},
            confidence=0.9
        )
        
        # Should not require visual navigation with explicit coordinates
        result = self.app._requires_visual_navigation(intent, "click at 100, 200")
        self.assertFalse(result)
    
    def test_no_visual_navigation_when_disabled(self):
        """Test that visual navigation is not used when disabled."""
        self.app.vision_navigator = None
        
        intent = CommandIntent(
            action='click',
            target='button',
            parameters={},
            confidence=0.9
        )
        
        # Should not require visual navigation when disabled
        result = self.app._requires_visual_navigation(intent, "click the button")
        self.assertFalse(result)
    
    def test_is_critical_action_detects_keywords(self):
        """Test that critical actions are detected by keywords."""
        result = VisionNavigationResult(
            action='click',
            coordinates=(100, 200),
            confidence=0.9,
            reasoning='Click the delete button to remove the file',
            requires_followup=False
        )
        
        # Should detect "delete" as critical keyword
        is_critical = self.app._is_critical_action(result)
        self.assertTrue(is_critical)
    
    def test_is_critical_action_safe_action(self):
        """Test that safe actions are not flagged as critical."""
        result = VisionNavigationResult(
            action='click',
            coordinates=(100, 200),
            confidence=0.9,
            reasoning='Click the submit button to save the form',
            requires_followup=False
        )
        
        # Should not detect as critical
        is_critical = self.app._is_critical_action(result)
        self.assertFalse(is_critical)
    
    def test_is_critical_action_when_disabled(self):
        """Test that critical action detection can be disabled."""
        self.app.config['visual_navigation']['require_confirmation_for_critical'] = False
        
        result = VisionNavigationResult(
            action='click',
            coordinates=(100, 200),
            confidence=0.9,
            reasoning='Click the delete button',
            requires_followup=False
        )
        
        # Should not flag as critical when disabled
        is_critical = self.app._is_critical_action(result)
        self.assertFalse(is_critical)
    
    @patch('ai_brain.main.Prompt.ask')
    def test_handle_visual_navigation_workflow(self, mock_prompt):
        """Test the complete visual navigation workflow."""
        # Mock prompt to always confirm
        mock_prompt.return_value = 'y'
        
        # Create test screenshot
        img = Image.new('RGB', (100, 100), color='white')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
        
        # Mock message broker responses
        self.app.message_broker.receive_visual_navigation_response.return_value = {
            'screenshot_base64': img_base64,
            'mouse_position': {'x': 50, 'y': 50},
            'screen_size': {'width': 1920, 'height': 1080}
        }
        
        self.app.message_broker.receive_visual_action_result.return_value = {
            'status': 'success',
            'screenshot_base64': img_base64,
            'mouse_position': {'x': 100, 'y': 200}
        }
        
        # Mock vision navigator to return complete action
        self.app.vision_navigator.analyze_screen_for_action.return_value = VisionNavigationResult(
            action='complete',
            coordinates=None,
            confidence=0.95,
            reasoning='Task completed successfully',
            requires_followup=False
        )
        
        # Create test intent
        intent = CommandIntent(
            action='click',
            target='submit button',
            parameters={},
            confidence=0.9
        )
        
        # Execute visual navigation
        self.app._handle_visual_navigation(intent, "click the submit button")
        
        # Verify message broker was called
        self.app.message_broker.send_visual_navigation_request.assert_called_once()
        self.app.message_broker.receive_visual_navigation_response.assert_called_once()
        
        # Verify vision navigator was called
        self.app.vision_navigator.analyze_screen_for_action.assert_called_once()
    
    @patch('ai_brain.main.Prompt.ask')
    def test_handle_visual_navigation_with_action_execution(self, mock_prompt):
        """Test visual navigation with action execution."""
        # Mock prompt to always confirm
        mock_prompt.return_value = 'y'
        
        # Create test screenshot
        img = Image.new('RGB', (100, 100), color='white')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
        
        # Mock message broker responses
        self.app.message_broker.receive_visual_navigation_response.return_value = {
            'screenshot_base64': img_base64,
            'mouse_position': {'x': 50, 'y': 50},
            'screen_size': {'width': 1920, 'height': 1080}
        }
        
        self.app.message_broker.receive_visual_action_result.return_value = {
            'status': 'success',
            'screenshot_base64': img_base64,
            'mouse_position': {'x': 100, 'y': 200}
        }
        
        # Mock vision navigator to return click action then complete
        self.app.vision_navigator.analyze_screen_for_action.side_effect = [
            VisionNavigationResult(
                action='click',
                coordinates=(100, 200),
                confidence=0.85,
                reasoning='Click the submit button',
                requires_followup=True
            ),
            VisionNavigationResult(
                action='complete',
                coordinates=None,
                confidence=0.95,
                reasoning='Task completed',
                requires_followup=False
            )
        ]
        
        # Create test intent
        intent = CommandIntent(
            action='click',
            target='submit button',
            parameters={},
            confidence=0.9
        )
        
        # Execute visual navigation
        self.app._handle_visual_navigation(intent, "click the submit button")
        
        # Verify action command was sent
        self.app.message_broker.send_visual_action_command.assert_called_once()
        
        # Verify action result was received
        self.app.message_broker.receive_visual_action_result.assert_called_once()
        
        # Verify vision navigator was called twice (initial + followup)
        self.assertEqual(self.app.vision_navigator.analyze_screen_for_action.call_count, 2)
    
    @patch('ai_brain.main.Prompt.ask')
    def test_handle_visual_navigation_critical_action_cancelled(self, mock_prompt):
        """Test that critical actions can be cancelled by user."""
        # Mock prompt to deny critical action
        mock_prompt.return_value = 'n'
        
        # Create test screenshot
        img = Image.new('RGB', (100, 100), color='white')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
        
        # Mock message broker responses
        self.app.message_broker.receive_visual_navigation_response.return_value = {
            'screenshot_base64': img_base64,
            'mouse_position': {'x': 50, 'y': 50},
            'screen_size': {'width': 1920, 'height': 1080}
        }
        
        # Mock vision navigator to return critical action
        self.app.vision_navigator.analyze_screen_for_action.return_value = VisionNavigationResult(
            action='click',
            coordinates=(100, 200),
            confidence=0.85,
            reasoning='Click the delete button to remove all files',
            requires_followup=False
        )
        
        # Create test intent
        intent = CommandIntent(
            action='click',
            target='delete button',
            parameters={},
            confidence=0.9
        )
        
        # Execute visual navigation
        self.app._handle_visual_navigation(intent, "click the delete button")
        
        # Verify action command was NOT sent (cancelled by user)
        self.app.message_broker.send_visual_action_command.assert_not_called()
    
    def test_handle_visual_navigation_max_iterations(self):
        """Test that visual navigation respects max iterations limit."""
        # Create test screenshot
        img = Image.new('RGB', (100, 100), color='white')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
        
        # Mock message broker responses
        self.app.message_broker.receive_visual_navigation_response.return_value = {
            'screenshot_base64': img_base64,
            'mouse_position': {'x': 50, 'y': 50},
            'screen_size': {'width': 1920, 'height': 1080}
        }
        
        self.app.message_broker.receive_visual_action_result.return_value = {
            'status': 'success',
            'screenshot_base64': img_base64,
            'mouse_position': {'x': 100, 'y': 200}
        }
        
        # Mock vision navigator to always return click action (never complete)
        self.app.vision_navigator.analyze_screen_for_action.return_value = VisionNavigationResult(
            action='click',
            coordinates=(100, 200),
            confidence=0.85,
            reasoning='Click button',
            requires_followup=True
        )
        
        # Set low max iterations
        self.app.config['visual_navigation']['max_iterations'] = 3
        
        # Create test intent
        intent = CommandIntent(
            action='click',
            target='button',
            parameters={},
            confidence=0.9
        )
        
        # Execute visual navigation
        self.app._handle_visual_navigation(intent, "click button")
        
        # Verify vision navigator was called max_iterations times
        self.assertEqual(
            self.app.vision_navigator.analyze_screen_for_action.call_count,
            3
        )


if __name__ == '__main__':
    unittest.main()
