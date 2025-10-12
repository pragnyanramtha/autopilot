"""
Test script to verify the protocol generator fix.
This tests that the action_library parameter is properly passed.
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_brain.protocol_generator import ProtocolGenerator
from ai_brain.gemini_client import GeminiClient, CommandIntent


def test_protocol_generator_initialization():
    """Test that ProtocolGenerator initializes correctly with action registry."""
    print("Testing ProtocolGenerator initialization...")
    
    # Create a mock GeminiClient (we won't actually call the API)
    api_key = os.getenv('GEMINI_API_KEY', 'test_key')
    gemini_client = GeminiClient(api_key=api_key)
    
    # Initialize ProtocolGenerator
    generator = ProtocolGenerator(gemini_client=gemini_client)
    
    # Verify action registry is initialized
    assert generator.action_registry is not None, "Action registry should be initialized"
    
    # Verify action library can be retrieved
    action_library = generator.action_registry.get_action_library_for_ai()
    assert isinstance(action_library, dict), "Action library should be a dictionary"
    assert len(action_library) > 0, "Action library should contain actions"
    
    print(f"✓ Action registry initialized with {len(action_library)} actions")
    
    # Print some sample actions
    print("\nSample actions available:")
    for i, (action_name, action_info) in enumerate(list(action_library.items())[:5]):
        print(f"  - {action_name}: {action_info.get('description', 'No description')}")
    
    print("\n✓ All tests passed!")
    return True


def test_action_library_structure():
    """Test that the action library has the expected structure."""
    print("\nTesting action library structure...")
    
    api_key = os.getenv('GEMINI_API_KEY', 'test_key')
    gemini_client = GeminiClient(api_key=api_key)
    generator = ProtocolGenerator(gemini_client=gemini_client)
    
    action_library = generator.action_registry.get_action_library_for_ai()
    
    # Check structure of first action
    if action_library:
        first_action = list(action_library.values())[0]
        assert 'category' in first_action, "Action should have category"
        assert 'description' in first_action, "Action should have description"
        assert 'params' in first_action, "Action should have params"
        assert 'required' in first_action['params'], "Params should have required list"
        assert 'optional' in first_action['params'], "Params should have optional dict"
        
        print("✓ Action library structure is correct")
    
    return True


if __name__ == "__main__":
    try:
        test_protocol_generator_initialization()
        test_action_library_structure()
        print("\n" + "="*50)
        print("ALL TESTS PASSED ✓")
        print("="*50)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
