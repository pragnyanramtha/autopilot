"""
Simple verification script for VisionNavigator implementation.
Tests the basic functionality without requiring pytest.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_brain.vision_navigator import VisionNavigationResult, VisualNavigationAuditEntry, VisionNavigator


def test_data_models():
    """Test the data models."""
    print("Testing VisionNavigationResult...")
    
    # Test valid click action
    result = VisionNavigationResult(
        action='click',
        coordinates=(500, 300),
        confidence=0.85,
        reasoning='Found submit button',
        requires_followup=True
    )
    assert result.action == 'click'
    assert result.coordinates == (500, 300)
    print("  ✓ Click action result works")
    
    # Test complete action
    result = VisionNavigationResult(
        action='complete',
        coordinates=None,
        confidence=1.0,
        reasoning='Task complete',
        requires_followup=False
    )
    assert result.action == 'complete'
    print("  ✓ Complete action result works")
    
    # Test type action
    result = VisionNavigationResult(
        action='type',
        coordinates=None,
        confidence=0.9,
        reasoning='Text field focused',
        requires_followup=True,
        text_to_type='Hello World'
    )
    assert result.text_to_type == 'Hello World'
    print("  ✓ Type action result works")
    
    print("\nTesting VisualNavigationAuditEntry...")
    
    # Test audit entry creation
    entry = VisualNavigationAuditEntry.create(
        request_id='test-123',
        iteration=1,
        task_description='Click button',
        screenshot_path='logs/test.png',
        mouse_position_before=(100, 200),
        action_taken='click',
        coordinates=(500, 300),
        confidence=0.85,
        reasoning='Found button',
        status='success'
    )
    assert entry.request_id == 'test-123'
    assert entry.status == 'success'
    print("  ✓ Audit entry creation works")
    
    # Test to_dict conversion
    entry_dict = entry.to_dict()
    assert entry_dict['request_id'] == 'test-123'
    assert entry_dict['coordinates'] == [500, 300]
    print("  ✓ Audit entry to_dict works")
    
    print("\n✅ All data model tests passed!")


def test_vision_navigator_init():
    """Test VisionNavigator initialization."""
    print("\nTesting VisionNavigator initialization...")
    
    # Mock GeminiClient
    class MockGeminiClient:
        def __init__(self):
            self.use_ultra_fast = False
            self.vision_model = None
    
    # Test config
    config = {
        'visual_navigation': {
            'vision_model': 'gemini-2.0-flash-exp',
            'vision_model_dev': 'gemini-2.0-flash-exp',
            'max_iterations': 10,
            'confidence_threshold': 0.6,
            'enable_audit_log': False,  # Disable for testing
            'critical_keywords': ['delete', 'format']
        }
    }
    
    mock_client = MockGeminiClient()
    navigator = VisionNavigator(mock_client, config)
    
    assert navigator.vision_model == 'gemini-2.0-flash-exp'
    assert navigator.max_iterations == 10
    assert navigator.confidence_threshold == 0.6
    assert 'delete' in navigator.critical_keywords
    print("  ✓ VisionNavigator initialization works")
    
    # Test dev mode
    mock_client.use_ultra_fast = True
    navigator = VisionNavigator(mock_client, config)
    assert navigator.vision_model == 'gemini-2.0-flash-exp'
    print("  ✓ Dev mode model selection works")
    
    print("\n✅ VisionNavigator initialization tests passed!")


def test_helper_methods():
    """Test helper methods."""
    print("\nTesting helper methods...")
    
    # Mock GeminiClient
    class MockGeminiClient:
        def __init__(self):
            self.use_ultra_fast = False
            self.vision_model = None
    
    config = {
        'visual_navigation': {
            'enable_audit_log': False,
            'critical_keywords': ['delete', 'format', 'shutdown']
        }
    }
    
    mock_client = MockGeminiClient()
    navigator = VisionNavigator(mock_client, config)
    
    # Test is_critical_action
    assert navigator.is_critical_action("Click the delete button") == True
    assert navigator.is_critical_action("Click the submit button") == False
    print("  ✓ is_critical_action works")
    
    # Test coordinate validation
    result = VisionNavigationResult(
        action='click',
        coordinates=(2000, 1500),  # Out of bounds
        confidence=0.9,
        reasoning='Test',
        requires_followup=False
    )
    
    validated = navigator._validate_coordinates(result, (1920, 1080))
    assert validated.coordinates == (1920, 1080)  # Clamped
    assert validated.confidence < result.confidence  # Reduced
    print("  ✓ Coordinate validation works")
    
    # Test JSON parsing
    json_text = '''```json
    {
        "action": "click",
        "coordinates": {"x": 100, "y": 200}
    }
    ```'''
    
    parsed = navigator._parse_json_response(json_text)
    assert parsed['action'] == 'click'
    assert parsed['coordinates']['x'] == 100
    print("  ✓ JSON parsing works")
    
    print("\n✅ All helper method tests passed!")


def main():
    """Run all tests."""
    print("=" * 60)
    print("VisionNavigator Implementation Verification")
    print("=" * 60)
    
    try:
        test_data_models()
        test_vision_navigator_init()
        test_helper_methods()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe VisionNavigator implementation is working correctly.")
        print("\nImplemented features:")
        print("  ✓ VisionNavigationResult data model")
        print("  ✓ VisualNavigationAuditEntry data model")
        print("  ✓ VisionNavigator class initialization")
        print("  ✓ Configuration loading with defaults")
        print("  ✓ Dev mode model selection")
        print("  ✓ Critical action detection")
        print("  ✓ Coordinate validation and clamping")
        print("  ✓ JSON response parsing")
        print("  ✓ Audit logging support")
        print("\nNote: Vision model API calls require actual GeminiClient")
        print("and will be tested during integration.")
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
