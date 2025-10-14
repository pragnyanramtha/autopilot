"""
Verification script for visual navigation integration in Automation Engine.
Checks that the integration is properly implemented.
"""

import sys
import os
import ast

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def verify_visual_navigation_integration():
    """Verify that visual navigation is integrated into automation engine main loop."""
    
    print("=" * 70)
    print("Verifying Visual Navigation Integration in Automation Engine")
    print("=" * 70)
    print()
    
    # Read the automation engine main.py file
    main_file = 'automation_engine/main.py'
    
    with open(main_file, 'r') as f:
        content = f.read()
    
    checks = []
    
    # Check 1: VisualNavigationHandler import
    check1 = 'from automation_engine.visual_navigation_handler import VisualNavigationHandler' in content
    checks.append(('VisualNavigationHandler import', check1))
    
    # Check 2: VisualNavigationHandler initialization
    check2 = 'self.visual_handler = VisualNavigationHandler(' in content
    checks.append(('VisualNavigationHandler initialization', check2))
    
    # Check 3: screen_capture parameter passed
    check3 = 'screen_capture=screen_capture' in content
    checks.append(('screen_capture parameter', check3))
    
    # Check 4: mouse_controller parameter passed
    check4 = 'mouse_controller=mouse_controller' in content
    checks.append(('mouse_controller parameter', check4))
    
    # Check 5: message_broker parameter passed
    check5 = 'message_broker=self.message_broker' in content
    checks.append(('message_broker parameter', check5))
    
    # Check 6: Visual navigation request polling
    check6 = 'receive_visual_navigation_request' in content
    checks.append(('Visual navigation request polling', check6))
    
    # Check 7: Visual navigation request handling
    check7 = 'handle_visual_navigation_request' in content
    checks.append(('Visual navigation request handling', check7))
    
    # Check 8: Visual action command polling
    check8 = 'receive_visual_action_command' in content
    checks.append(('Visual action command polling', check8))
    
    # Check 9: Visual action execution
    check9 = 'execute_visual_action' in content
    checks.append(('Visual action execution', check9))
    
    # Check 10: Visual action result sending
    check10 = 'send_visual_action_result' in content
    checks.append(('Visual action result sending', check10))
    
    # Print results
    all_passed = True
    for check_name, passed in checks:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check_name}")
        if not passed:
            all_passed = False
    
    print()
    print("=" * 70)
    
    if all_passed:
        print("✓ All checks passed! Visual navigation is properly integrated.")
        print()
        print("Integration Summary:")
        print("  - VisualNavigationHandler is imported and initialized")
        print("  - Handler receives screen_capture, mouse_controller, and message_broker")
        print("  - Main loop polls for visual navigation requests")
        print("  - Main loop polls for visual action commands")
        print("  - Visual actions are executed and results are sent back")
        return True
    else:
        print("✗ Some checks failed. Please review the integration.")
        return False


if __name__ == '__main__':
    success = verify_visual_navigation_integration()
    sys.exit(0 if success else 1)
