"""
Test retry logic for vision API calls.

This test verifies that the VisionNavigator properly implements
exponential backoff retry logic for API failures.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
from PIL import Image
import time


class TestVisionRetryLogic(unittest.TestCase):
    """Test cases for vision API retry logic."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock Gemini client
        self.mock_gemini_client = Mock()
        self.mock_gemini_client.use_ultra_fast = False
        self.mock_vision_model = Mock()
        self.mock_gemini_client.vision_model = self.mock_vision_model
        
        # Create test config
        self.config = {
            'visual_navigation': {
                'enabled': True,
                'vision_model': 'gemini-2.0-flash-exp',
                'vision_model_dev': 'gemini-2.0-flash-exp',
                'max_iterations': 10,
                'confidence_threshold': 0.6,
                'enable_audit_log': False
            }
        }
        
        # Create test screenshot
        self.screenshot = Image.new('RGB', (100, 100), color='white')
    
    def test_retry_logic_success_on_first_attempt(self):
        """Test that successful API call on first attempt doesn't retry."""
        from ai_brain.vision_navigator import VisionNavigator
        
        # Mock successful response
        mock_response = Mock()
        mock_response.text = '{"action": "click", "coordinates": {"x": 50, "y": 50}, "confidence": 0.9, "reasoning": "test", "requires_followup": false}'
        mock_response.candidates = [Mock()]
        mock_response.candidates[0].content.parts = ['test']
        self.mock_vision_model.generate_content.return_value = mock_response
        
        # Create navigator
        navigator = VisionNavigator(self.mock_gemini_client, self.config)
        
        # Call API
        result = navigator._call_vision_api_with_retry("test prompt", self.screenshot)
        
        # Verify only called once
        self.assertEqual(self.mock_vision_model.generate_content.call_count, 1)
        self.assertIsNotNone(result)
    
    def test_retry_logic_success_on_second_attempt(self):
        """Test that API call retries and succeeds on second attempt."""
        from ai_brain.vision_navigator import VisionNavigator
        
        # Mock first failure, then success
        mock_response = Mock()
        mock_response.text = '{"action": "click", "coordinates": {"x": 50, "y": 50}, "confidence": 0.9, "reasoning": "test", "requires_followup": false}'
        mock_response.candidates = [Mock()]
        mock_response.candidates[0].content.parts = ['test']
        
        self.mock_vision_model.generate_content.side_effect = [
            Exception("API Error"),
            mock_response
        ]
        
        # Create navigator
        navigator = VisionNavigator(self.mock_gemini_client, self.config)
        
        # Call API with patched sleep to speed up test
        with patch('time.sleep'):
            result = navigator._call_vision_api_with_retry("test prompt", self.screenshot)
        
        # Verify called twice
        self.assertEqual(self.mock_vision_model.generate_content.call_count, 2)
        self.assertIsNotNone(result)
    
    def test_retry_logic_exhausts_all_retries(self):
        """Test that API call fails after exhausting all retries."""
        from ai_brain.vision_navigator import VisionNavigator
        
        # Mock all failures
        self.mock_vision_model.generate_content.side_effect = Exception("API Error")
        
        # Create navigator
        navigator = VisionNavigator(self.mock_gemini_client, self.config)
        
        # Call API should raise exception after retries
        with patch('time.sleep'):
            with self.assertRaises(Exception) as context:
                navigator._call_vision_api_with_retry("test prompt", self.screenshot)
        
        # Verify called max_retries times (3)
        self.assertEqual(self.mock_vision_model.generate_content.call_count, 3)
        self.assertIn("API Error", str(context.exception))
    
    def test_retry_logic_exponential_backoff(self):
        """Test that retry delays follow exponential backoff pattern."""
        from ai_brain.vision_navigator import VisionNavigator
        
        # Mock all failures
        self.mock_vision_model.generate_content.side_effect = Exception("API Error")
        
        # Create navigator
        navigator = VisionNavigator(self.mock_gemini_client, self.config)
        
        # Track sleep calls
        sleep_times = []
        
        def mock_sleep(seconds):
            sleep_times.append(seconds)
        
        # Call API with patched sleep
        with patch('time.sleep', side_effect=mock_sleep):
            try:
                navigator._call_vision_api_with_retry("test prompt", self.screenshot)
            except Exception:
                pass
        
        # Verify exponential backoff: 1.0, 2.0 seconds
        # (3rd attempt doesn't sleep since it's the last one)
        self.assertEqual(len(sleep_times), 2)
        self.assertEqual(sleep_times[0], 1.0)  # 1.0 * 2^0
        self.assertEqual(sleep_times[1], 2.0)  # 1.0 * 2^1
    
    def test_analyze_screen_uses_retry_logic(self):
        """Test that analyze_screen_for_action uses retry logic."""
        from ai_brain.vision_navigator import VisionNavigator
        
        # Mock successful response
        mock_response = Mock()
        mock_response.text = '{"action": "click", "coordinates": {"x": 50, "y": 50}, "confidence": 0.9, "reasoning": "test", "requires_followup": false}'
        mock_response.candidates = [Mock()]
        mock_response.candidates[0].content.parts = ['test']
        self.mock_vision_model.generate_content.return_value = mock_response
        
        # Create navigator
        navigator = VisionNavigator(self.mock_gemini_client, self.config)
        
        # Call analyze_screen_for_action
        result = navigator.analyze_screen_for_action(
            screenshot=self.screenshot,
            current_mouse_pos=(10, 10),
            task_description="Click the button",
            screen_size=(1920, 1080)
        )
        
        # Verify result
        self.assertEqual(result.action, 'click')
        self.assertEqual(result.coordinates, (50, 50))
        self.assertEqual(result.confidence, 0.9)
    
    def test_analyze_screen_handles_retry_failure(self):
        """Test that analyze_screen_for_action handles retry failures gracefully."""
        from ai_brain.vision_navigator import VisionNavigator
        
        # Mock all failures
        self.mock_vision_model.generate_content.side_effect = Exception("API Error")
        
        # Create navigator
        navigator = VisionNavigator(self.mock_gemini_client, self.config)
        
        # Call analyze_screen_for_action with patched sleep
        with patch('time.sleep'):
            result = navigator.analyze_screen_for_action(
                screenshot=self.screenshot,
                current_mouse_pos=(10, 10),
                task_description="Click the button",
                screen_size=(1920, 1080)
            )
        
        # Verify returns error result instead of crashing
        self.assertEqual(result.action, 'no_action')
        self.assertEqual(result.confidence, 0.0)
        self.assertIn('Error', result.reasoning)


if __name__ == '__main__':
    unittest.main()
