"""
Test to verify the posting workflow bug fix.
Ensures that posting commands generate complete workflows.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_brain.gemini_client import GeminiClient


def test_posting_command_complexity():
    """Test that posting commands are detected as complex."""
    client = GeminiClient()
    
    # Test various posting commands
    posting_commands = [
        "post about today's weather on X",
        "tweet about AI trends",
        "post to Twitter about Python",
        "publish to X about machine learning",
        "share on Twitter my thoughts"
    ]
    
    print("Testing posting command complexity detection...")
    for command in posting_commands:
        complexity = client._detect_command_complexity(command)
        print(f"  '{command}' → {complexity}")
        assert complexity == 'complex', f"Expected 'complex' but got '{complexity}' for: {command}"
    
    print("✓ All posting commands correctly detected as complex\n")


def test_simple_commands_still_simple():
    """Test that simple commands are still detected as simple."""
    client = GeminiClient()
    
    simple_commands = [
        "click the button",
        "type hello world",
        "open chrome",
        "move mouse to center"
    ]
    
    print("Testing simple command detection...")
    for command in simple_commands:
        complexity = client._detect_command_complexity(command)
        print(f"  '{command}' → {complexity}")
        assert complexity == 'simple', f"Expected 'simple' but got '{complexity}' for: {command}"
    
    print("✓ All simple commands correctly detected as simple\n")


def test_protocol_prompt_includes_complete_workflow_requirements():
    """Test that the protocol generation prompt includes complete workflow requirements."""
    from ai_brain.action_registry import ActionRegistry
    from ai_brain.action_handlers import ActionHandlers
    
    client = GeminiClient()
    
    # Initialize action registry
    registry = ActionRegistry()
    handlers = ActionHandlers(registry)
    handlers.register_all()
    action_library = registry.get_action_library_for_ai()
    
    # Build prompt for a posting command
    user_input = "post about today's weather on X"
    prompt = client._build_protocol_prompt_template(user_input, action_library)
    
    print("Testing protocol generation prompt...")
    
    # Check for key requirements in prompt
    required_phrases = [
        "Complete Workflows",
        "post on X",
        "tweet about",
        "Do NOT stop at just searching",
        "ENTIRE task from start to finish",
        "Content in Protocol",
        "FULL content text",
        "Social Media Posts",
        "Navigate to x.com",
        "Type the COMPLETE post content",
        "Click Post button"
    ]
    
    missing = []
    for phrase in required_phrases:
        if phrase not in prompt:
            missing.append(phrase)
            print(f"  ✗ Missing: '{phrase}'")
        else:
            print(f"  ✓ Found: '{phrase}'")
    
    if missing:
        print(f"\n✗ Prompt missing {len(missing)} required phrases")
        assert False, f"Prompt missing required phrases: {missing}"
    else:
        print("\n✓ Prompt includes all complete workflow requirements\n")


if __name__ == "__main__":
    print("=" * 60)
    print("POSTING WORKFLOW BUG FIX VERIFICATION")
    print("=" * 60)
    print()
    
    try:
        test_posting_command_complexity()
        test_simple_commands_still_simple()
        test_protocol_prompt_includes_complete_workflow_requirements()
        
        print("=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        print("\nThe posting workflow bug fix is working correctly!")
        print("Posting commands will now generate complete end-to-end protocols.")
        
    except AssertionError as e:
        print("=" * 60)
        print("✗ TEST FAILED")
        print("=" * 60)
        print(f"\nError: {e}")
        sys.exit(1)
    except Exception as e:
        print("=" * 60)
        print("✗ TEST ERROR")
        print("=" * 60)
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
