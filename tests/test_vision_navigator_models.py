"""
Tests for vision navigator data models.
"""

import pytest
from ai_brain.vision_navigator import VisionNavigationResult, VisualNavigationAuditEntry


def test_vision_navigation_result_valid_click():
    """Test creating a valid click action result."""
    result = VisionNavigationResult(
        action='click',
        coordinates=(500, 300),
        confidence=0.85,
        reasoning='Found submit button at center of screen',
        requires_followup=True
    )
    
    assert result.action == 'click'
    assert result.coordinates == (500, 300)
    assert result.confidence == 0.85
    assert result.requires_followup is True
    assert result.text_to_type is None


def test_vision_navigation_result_valid_type():
    """Test creating a valid type action result."""
    result = VisionNavigationResult(
        action='type',
        coordinates=None,
        confidence=0.9,
        reasoning='Text input field is focused',
        requires_followup=True,
        text_to_type='Hello World'
    )
    
    assert result.action == 'type'
    assert result.text_to_type == 'Hello World'


def test_vision_navigation_result_valid_complete():
    """Test creating a valid complete action result."""
    result = VisionNavigationResult(
        action='complete',
        coordinates=None,
        confidence=1.0,
        reasoning='Workflow goal achieved',
        requires_followup=False
    )
    
    assert result.action == 'complete'
    assert result.coordinates is None


def test_vision_navigation_result_invalid_action():
    """Test that invalid action raises ValueError."""
    with pytest.raises(ValueError, match="Invalid action"):
        VisionNavigationResult(
            action='invalid_action',
            coordinates=(100, 100),
            confidence=0.5,
            reasoning='Test',
            requires_followup=False
        )


def test_vision_navigation_result_invalid_confidence():
    """Test that confidence out of range raises ValueError."""
    with pytest.raises(ValueError, match="Confidence must be between"):
        VisionNavigationResult(
            action='click',
            coordinates=(100, 100),
            confidence=1.5,
            reasoning='Test',
            requires_followup=False
        )


def test_vision_navigation_result_click_without_coordinates():
    """Test that click action without coordinates raises ValueError."""
    with pytest.raises(ValueError, match="requires coordinates"):
        VisionNavigationResult(
            action='click',
            coordinates=None,
            confidence=0.8,
            reasoning='Test',
            requires_followup=False
        )


def test_vision_navigation_result_type_without_text():
    """Test that type action without text raises ValueError."""
    with pytest.raises(ValueError, match="requires text_to_type"):
        VisionNavigationResult(
            action='type',
            coordinates=None,
            confidence=0.8,
            reasoning='Test',
            requires_followup=False
        )


def test_visual_navigation_audit_entry_create():
    """Test creating an audit entry with factory method."""
    entry = VisualNavigationAuditEntry.create(
        request_id='test-123',
        iteration=1,
        task_description='Click submit button',
        screenshot_path='logs/screenshot_001.png',
        mouse_position_before=(100, 200),
        action_taken='click',
        coordinates=(500, 300),
        confidence=0.85,
        reasoning='Found button',
        status='success'
    )
    
    assert entry.request_id == 'test-123'
    assert entry.iteration == 1
    assert entry.task_description == 'Click submit button'
    assert entry.mouse_position_before == (100, 200)
    assert entry.coordinates == (500, 300)
    assert entry.confidence == 0.85
    assert entry.status == 'success'
    assert entry.error is None
    assert entry.timestamp.endswith('Z')


def test_visual_navigation_audit_entry_with_error():
    """Test creating an audit entry with error status."""
    entry = VisualNavigationAuditEntry.create(
        request_id='test-456',
        iteration=2,
        task_description='Click button',
        screenshot_path='logs/screenshot_002.png',
        mouse_position_before=(150, 250),
        action_taken='click',
        coordinates=(600, 400),
        confidence=0.5,
        reasoning='Low confidence',
        status='error',
        error='Coordinates out of bounds'
    )
    
    assert entry.status == 'error'
    assert entry.error == 'Coordinates out of bounds'


def test_visual_navigation_audit_entry_to_dict():
    """Test converting audit entry to dictionary."""
    entry = VisualNavigationAuditEntry.create(
        request_id='test-789',
        iteration=3,
        task_description='Test task',
        screenshot_path='logs/screenshot_003.png',
        mouse_position_before=(200, 300),
        action_taken='double_click',
        coordinates=(700, 500),
        confidence=0.95,
        reasoning='High confidence',
        status='success'
    )
    
    entry_dict = entry.to_dict()
    
    assert entry_dict['request_id'] == 'test-789'
    assert entry_dict['iteration'] == 3
    assert entry_dict['mouse_position_before'] == [200, 300]
    assert entry_dict['coordinates'] == [700, 500]
    assert entry_dict['confidence'] == 0.95
    assert entry_dict['status'] == 'success'
    assert isinstance(entry_dict['timestamp'], str)


def test_visual_navigation_audit_entry_invalid_status():
    """Test that invalid status raises ValueError."""
    with pytest.raises(ValueError, match="Invalid status"):
        VisualNavigationAuditEntry(
            timestamp='2024-01-01T00:00:00Z',
            request_id='test',
            iteration=1,
            task_description='Test',
            screenshot_path='test.png',
            mouse_position_before=(0, 0),
            action_taken='click',
            coordinates=(100, 100),
            confidence=0.8,
            reasoning='Test',
            status='invalid_status'
        )


def test_visual_navigation_audit_entry_invalid_confidence():
    """Test that confidence out of range raises ValueError."""
    with pytest.raises(ValueError, match="Confidence must be between"):
        VisualNavigationAuditEntry(
            timestamp='2024-01-01T00:00:00Z',
            request_id='test',
            iteration=1,
            task_description='Test',
            screenshot_path='test.png',
            mouse_position_before=(0, 0),
            action_taken='click',
            coordinates=(100, 100),
            confidence=2.0,
            reasoning='Test',
            status='success'
        )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
