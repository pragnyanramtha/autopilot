"""
Test safety and validation features for visual navigation.
Tests coordinate validation, loop detection, iteration limits, and critical action detection.
"""

import pytest
from unittest.mock import Mock, MagicMock
from ai_brain.vision_navigator import VisionNavigator, VisionNavigationResult


class TestCoordinateValidation:
    """Test coordinate validation (Task 8.1)"""
    
    def test_valid_coordinates_within_bounds(self):
        """Test that valid coordinates pass validation"""
        mock_client = Mock()
        mock_client.use_ultra_fast = False
        
        config = {
            'visual_navigation': {
                'vision_model': 'gemini-2.0-flash-exp',
                'max_iterations': 10,
                'confidence_threshold': 0.6
            }
        }
        
        navigator = VisionNavigator(mock_client, config)
        
        result = VisionNavigationResult(
            action='click',
            coordinates=(500, 300),
            confidence=0.9,
            reasoning='Click the button',
            requires_followup=False
        )
        
        screen_size = (1920, 1080)
        validated = navigator._validate_coordinates(result, screen_size)
        
        assert validated.action == 'click'
        assert validated.coordinates == (500, 300)
        assert validated.confidence == 0.9
    
    def test_slightly_out_of_bounds_clamped(self):
        """Test that slightly out of bounds coordinates are clamped"""
        mock_client = Mock()
        mock_client.use_ultra_fast = False
        
        config = {
            'visual_navigation': {
                'vision_model': 'gemini-2.0-flash-exp',
                'max_iterations': 10,
                'confidence_threshold': 0.6
            }
        }
        
        navigator = VisionNavigator(mock_client, config)
        
        result = VisionNavigationResult(
            action='click',
            coordinates=(1925, 300),  # 5 pixels out of bounds
            confidence=0.9,
            reasoning='Click the button',
            requires_followup=False
        )
        
        screen_size = (1920, 1080)
        validated = navigator._validate_coordinates(result, screen_size, margin=10)
        
        assert validated.action == 'click'
        assert validated.coordinates == (1920, 300)  # Clamped to max
        assert validated.confidence < 0.9  # Confidence reduced
    
    def test_severely_out_of_bounds_rejected(self):
        """Test that severely out of bounds coordinates are rejected"""
        mock_client = Mock()
        mock_client.use_ultra_fast = False
        
        config = {
            'visual_navigation': {
                'vision_model': 'gemini-2.0-flash-exp',
                'max_iterations': 10,
                'confidence_threshold': 0.6
            }
        }
        
        navigator = VisionNavigator(mock_client, config)
        
        result = VisionNavigationResult(
            action='click',
            coordinates=(2500, 300),  # Way out of bounds
            confidence=0.9,
            reasoning='Click the button',
            requires_followup=False
        )
        
        screen_size = (1920, 1080)
        validated = navigator._validate_coordinates(result, screen_size, margin=10)
        
        assert validated.action == 'no_action'
        assert validated.coordinates is None
        assert validated.confidence == 0.0


class TestLoopDetection:
    """Test loop detection (Task 8.2)"""
    
    def test_no_loop_with_different_coordinates(self):
        """Test that different coordinates don't trigger loop detection"""
        mock_client = Mock()
        mock_client.use_ultra_fast = False
        
        config = {
            'visual_navigation': {
                'vision_model': 'gemini-2.0-flash-exp',
                'max_iterations': 10,
                'confidence_threshold': 0.6,
                'loop_detection_threshold': 3
            }
        }
        
        navigator = VisionNavigator(mock_client, config)
        
        # Add different actions
        navigator.add_action_to_history('click', (100, 100))
        navigator.add_action_to_history('click', (200, 200))
        navigator.add_action_to_history('click', (300, 300))
        
        # Check for loop with new coordinates
        loop_detected, warning = navigator.detect_loop((400, 400))
        
        assert not loop_detected
        assert warning is None
    
    def test_loop_detected_with_repeated_coordinates(self):
        """Test that repeated coordinates trigger loop detection"""
        mock_client = Mock()
        mock_client.use_ultra_fast = False
        
        config = {
            'visual_navigation': {
                'vision_model': 'gemini-2.0-flash-exp',
                'max_iterations': 10,
                'confidence_threshold': 0.6,
                'loop_detection_threshold': 3
            }
        }
        
        navigator = VisionNavigator(mock_client, config)
        
        # Add same coordinates multiple times
        navigator.add_action_to_history('click', (100, 100))
        navigator.add_action_to_history('click', (102, 101))  # Within tolerance
        navigator.add_action_to_history('click', (99, 100))   # Within tolerance
        
        # Check for loop with similar coordinates
        loop_detected, warning = navigator.detect_loop((101, 99), tolerance=5)
        
        assert loop_detected
        assert warning is not None
        assert 'Loop detected' in warning
    
    def test_action_history_circular_buffer(self):
        """Test that action history maintains circular buffer size"""
        mock_client = Mock()
        mock_client.use_ultra_fast = False
        
        config = {
            'visual_navigation': {
                'vision_model': 'gemini-2.0-flash-exp',
                'max_iterations': 10,
                'confidence_threshold': 0.6,
                'loop_detection_buffer_size': 5
            }
        }
        
        navigator = VisionNavigator(mock_client, config)
        
        # Add more actions than buffer size
        for i in range(10):
            navigator.add_action_to_history('click', (i * 100, i * 100))
        
        # Buffer should only contain last 5 actions
        assert len(navigator.action_history) == 5
    
    def test_reset_action_history(self):
        """Test that action history can be reset"""
        mock_client = Mock()
        mock_client.use_ultra_fast = False
        
        config = {
            'visual_navigation': {
                'vision_model': 'gemini-2.0-flash-exp',
                'max_iterations': 10,
                'confidence_threshold': 0.6
            }
        }
        
        navigator = VisionNavigator(mock_client, config)
        
        # Add some actions
        navigator.add_action_to_history('click', (100, 100))
        navigator.add_action_to_history('click', (200, 200))
        
        assert len(navigator.action_history) == 2
        
        # Reset
        navigator.reset_action_history()
        
        assert len(navigator.action_history) == 0


class TestIterationLimitEnforcement:
    """Test iteration limit enforcement (Task 8.3)"""
    
    def test_iteration_within_limit(self):
        """Test that iterations within limit don't trigger warning"""
        mock_client = Mock()
        mock_client.use_ultra_fast = False
        
        config = {
            'visual_navigation': {
                'vision_model': 'gemini-2.0-flash-exp',
                'max_iterations': 10,
                'confidence_threshold': 0.6
            }
        }
        
        navigator = VisionNavigator(mock_client, config)
        
        limit_reached, warning = navigator.check_iteration_limit(5)
        
        assert not limit_reached
        assert warning is None
    
    def test_iteration_limit_reached(self):
        """Test that reaching iteration limit triggers warning"""
        mock_client = Mock()
        mock_client.use_ultra_fast = False
        
        config = {
            'visual_navigation': {
                'vision_model': 'gemini-2.0-flash-exp',
                'max_iterations': 10,
                'confidence_threshold': 0.6
            }
        }
        
        navigator = VisionNavigator(mock_client, config)
        
        limit_reached, warning = navigator.check_iteration_limit(10)
        
        assert limit_reached
        assert warning is not None
        assert 'Iteration limit reached' in warning
    
    def test_iteration_limit_exceeded(self):
        """Test that exceeding iteration limit triggers warning"""
        mock_client = Mock()
        mock_client.use_ultra_fast = False
        
        config = {
            'visual_navigation': {
                'vision_model': 'gemini-2.0-flash-exp',
                'max_iterations': 10,
                'confidence_threshold': 0.6
            }
        }
        
        navigator = VisionNavigator(mock_client, config)
        
        limit_reached, warning = navigator.check_iteration_limit(15)
        
        assert limit_reached
        assert warning is not None


class TestCriticalActionDetection:
    """Test critical action detection (Task 8.4)"""
    
    def test_non_critical_action(self):
        """Test that normal actions are not flagged as critical"""
        mock_client = Mock()
        mock_client.use_ultra_fast = False
        
        config = {
            'visual_navigation': {
                'vision_model': 'gemini-2.0-flash-exp',
                'max_iterations': 10,
                'confidence_threshold': 0.6,
                'critical_keywords': ['delete', 'format', 'shutdown']
            }
        }
        
        navigator = VisionNavigator(mock_client, config)
        
        is_critical, keywords = navigator.is_critical_action(
            'Click the submit button to save the form',
            'click'
        )
        
        assert not is_critical
        assert len(keywords) == 0
    
    def test_critical_action_with_delete_keyword(self):
        """Test that actions with 'delete' keyword are flagged as critical"""
        mock_client = Mock()
        mock_client.use_ultra_fast = False
        
        config = {
            'visual_navigation': {
                'vision_model': 'gemini-2.0-flash-exp',
                'max_iterations': 10,
                'confidence_threshold': 0.6,
                'critical_keywords': ['delete', 'format', 'shutdown']
            }
        }
        
        navigator = VisionNavigator(mock_client, config)
        
        is_critical, keywords = navigator.is_critical_action(
            'Click the delete button to remove the file',
            'click'
        )
        
        assert is_critical
        assert 'delete' in keywords
    
    def test_critical_action_with_multiple_keywords(self):
        """Test that actions with multiple critical keywords are detected"""
        mock_client = Mock()
        mock_client.use_ultra_fast = False
        
        config = {
            'visual_navigation': {
                'vision_model': 'gemini-2.0-flash-exp',
                'max_iterations': 10,
                'confidence_threshold': 0.6,
                'critical_keywords': ['delete', 'format', 'shutdown', 'remove']
            }
        }
        
        navigator = VisionNavigator(mock_client, config)
        
        is_critical, keywords = navigator.is_critical_action(
            'Delete and remove all files from the system',
            'click'
        )
        
        assert is_critical
        assert 'delete' in keywords
        assert 'remove' in keywords
    
    def test_critical_action_case_insensitive(self):
        """Test that critical keyword detection is case-insensitive"""
        mock_client = Mock()
        mock_client.use_ultra_fast = False
        
        config = {
            'visual_navigation': {
                'vision_model': 'gemini-2.0-flash-exp',
                'max_iterations': 10,
                'confidence_threshold': 0.6,
                'critical_keywords': ['delete', 'format', 'shutdown']
            }
        }
        
        navigator = VisionNavigator(mock_client, config)
        
        is_critical, keywords = navigator.is_critical_action(
            'Click the DELETE button to remove the file',
            'click'
        )
        
        assert is_critical
        assert 'delete' in keywords


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
