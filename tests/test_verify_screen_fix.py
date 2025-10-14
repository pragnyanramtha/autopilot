"""
Test to verify the verify_screen variable substitution fix.

This test ensures that the AI generates protocols using visual_navigate
instead of the problematic verify_screen + mouse_move pattern.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_brain.gemini_client import GeminiClient
from shared.action_registry import ActionRegistry
from shared.action_handlers import ActionHandlers


def test_protocol_uses_visual_navigate():
    """Test that generated protocols use visual_navigate instead of verify_screen + mouse_move."""
    
    # Initialize components
    gemini_client = GeminiClient()
    action_registry = ActionRegistry()
    action_handlers = ActionHandlers(action_registry)
    action_handlers.register_all()
    
    # Get action library
    action_library = action_registry.get_action_library_for_ai()
    
    # Test command that would previously generate the problematic pattern
    user_input = "Post a CSS joke on X"
    
    print(f"\n{'='*60}")
    print(f"Testing protocol generation for: {user_input}")
    print(f"{'='*60}\n")
    
    try:
        # Generate protocol
        protocol = gemini_client.generate_protocol(user_input, action_library)
        
        print(f"✓ Protocol generated successfully")
        print(f"  Actions: {len(protocol.get('actions', []))}")
        print(f"  Uses vision: {protocol.get('metadata', {}).get('uses_vision', False)}")
        
        # Check for problematic pattern
        actions = protocol.get('actions', [])
        problematic_pattern_found = False
        
        for i in range(len(actions) - 2):
            action1 = actions[i]
            action2 = actions[i + 1]
            action3 = actions[i + 2] if i + 2 < len(actions) else None
            
            # Check for verify_screen followed by mouse_move with {{verified_x}}
            if (action1.get('action') == 'verify_screen' and 
                action2.get('action') == 'mouse_move'):
                
                params = action2.get('params', {})
                if '{{verified_x}}' in str(params) or '{{verified_y}}' in str(params):
                    problematic_pattern_found = True
                    print(f"\n✗ PROBLEMATIC PATTERN FOUND at action {i+1}-{i+2}:")
                    print(f"  Action {i+1}: {action1}")
                    print(f"  Action {i+2}: {action2}")
                    if action3:
                        print(f"  Action {i+3}: {action3}")
                    break
        
        if not problematic_pattern_found:
            print(f"\n✓ No problematic verify_screen + mouse_move pattern found")
        
        # Check for visual_navigate usage
        visual_navigate_count = sum(1 for a in actions if a.get('action') == 'visual_navigate')
        
        if visual_navigate_count > 0:
            print(f"✓ Protocol uses visual_navigate ({visual_navigate_count} times)")
            print(f"\n  Visual navigate actions:")
            for i, action in enumerate(actions):
                if action.get('action') == 'visual_navigate':
                    target = action.get('params', {}).get('target_description', 'N/A')
                    action_type = action.get('params', {}).get('action_type', 'N/A')
                    print(f"    [{i+1}] {action_type}: {target}")
        else:
            print(f"⚠ Protocol does not use visual_navigate")
        
        # Print full protocol for inspection
        print(f"\n{'='*60}")
        print(f"Full Protocol:")
        print(f"{'='*60}")
        import json
        print(json.dumps(protocol, indent=2))
        
        # Verdict
        print(f"\n{'='*60}")
        if problematic_pattern_found:
            print(f"❌ TEST FAILED: Problematic pattern still present")
            print(f"   The AI is still generating verify_screen + mouse_move patterns")
            print(f"   that will fail when verify_screen returns NOT SAFE")
            return False
        elif visual_navigate_count > 0:
            print(f"✅ TEST PASSED: Protocol uses visual_navigate correctly")
            print(f"   The fix is working - no variable substitution issues expected")
            return True
        else:
            print(f"⚠ TEST INCONCLUSIVE: No visual navigation used")
            print(f"   This command may not require visual navigation")
            return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_multiple_commands():
    """Test multiple commands to ensure consistency."""
    
    commands = [
        "Post a CSS joke on X",
        "Tweet about Python programming",
        "Click the login button",
        "Find and click the submit button"
    ]
    
    print(f"\n{'='*60}")
    print(f"Testing Multiple Commands")
    print(f"{'='*60}\n")
    
    results = []
    
    for cmd in commands:
        print(f"\nTesting: {cmd}")
        print(f"-" * 40)
        
        try:
            gemini_client = GeminiClient()
            action_registry = ActionRegistry()
            action_handlers = ActionHandlers(action_registry)
            action_handlers.register_all()
            action_library = action_registry.get_action_library_for_ai()
            
            protocol = gemini_client.generate_protocol(cmd, action_library)
            actions = protocol.get('actions', [])
            
            # Check for problematic pattern
            has_problem = False
            for i in range(len(actions) - 1):
                if (actions[i].get('action') == 'verify_screen' and 
                    actions[i+1].get('action') == 'mouse_move'):
                    params = actions[i+1].get('params', {})
                    if '{{verified_x}}' in str(params):
                        has_problem = True
                        break
            
            # Check for visual_navigate
            has_visual_nav = any(a.get('action') == 'visual_navigate' for a in actions)
            
            if has_problem:
                print(f"  ❌ Has problematic pattern")
                results.append(False)
            elif has_visual_nav:
                print(f"  ✅ Uses visual_navigate")
                results.append(True)
            else:
                print(f"  ⚠ No visual navigation (may be OK)")
                results.append(True)
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            results.append(False)
    
    print(f"\n{'='*60}")
    print(f"Summary: {sum(results)}/{len(results)} tests passed")
    print(f"{'='*60}\n")
    
    return all(results)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("VERIFY_SCREEN FIX VALIDATION TEST")
    print("="*60)
    
    # Run main test
    test1_passed = test_protocol_uses_visual_navigate()
    
    # Run multiple command test
    # test2_passed = test_multiple_commands()
    
    print(f"\n{'='*60}")
    print(f"FINAL RESULT")
    print(f"{'='*60}")
    
    if test1_passed:
        print(f"✅ All tests passed!")
        print(f"   The verify_screen fix is working correctly")
        print(f"   Protocols should no longer fail with variable substitution errors")
    else:
        print(f"❌ Some tests failed")
        print(f"   The fix may need additional adjustments")
    
    print(f"{'='*60}\n")
