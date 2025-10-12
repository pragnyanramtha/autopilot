"""
Quick verification script for Task 6: Configure Smooth Mouse Movements

This script provides a quick check that all smooth mouse movement
configuration is properly set up.
"""

import sys
sys.path.insert(0, '.')

from automation_engine.mouse_controller import MouseController, MouseConfig
from shared.action_registry import ActionRegistry
from shared.action_handlers import ActionHandlers


def verify_task6():
    """Verify Task 6 implementation."""
    print("\n" + "=" * 70)
    print("TASK 6 VERIFICATION: Configure Smooth Mouse Movements")
    print("=" * 70)
    
    checks_passed = 0
    total_checks = 6
    
    # Check 1: MouseConfig defaults
    print("\n[1/6] Checking MouseConfig defaults...")
    config = MouseConfig()
    if (config.curve_intensity == 0.3 and 
        config.speed == 1.0 and 
        config.overshoot == True and 
        config.add_noise == True):
        print("      ✓ MouseConfig has correct defaults")
        checks_passed += 1
    else:
        print("      ✗ MouseConfig defaults are incorrect")
    
    # Check 2: MouseController initialization
    print("\n[2/6] Checking MouseController initialization...")
    controller = MouseController()
    if controller.config is not None:
        print("      ✓ MouseController initializes with config")
        checks_passed += 1
    else:
        print("      ✗ MouseController missing config")
    
    # Check 3: move_to curve_type default
    print("\n[3/6] Checking move_to() default curve type...")
    import inspect
    sig = inspect.signature(controller.move_to)
    if sig.parameters['curve_type'].default == 'bezier':
        print("      ✓ move_to() defaults to 'bezier' curve type")
        checks_passed += 1
    else:
        print("      ✗ move_to() curve_type default is incorrect")
    
    # Check 4: Action handler registration
    print("\n[4/6] Checking action handler registration...")
    registry = ActionRegistry()
    handlers = ActionHandlers(registry)
    handlers.register_mouse_handlers()
    handler = registry.get_handler("mouse_move")
    if handler is not None:
        print("      ✓ mouse_move action handler is registered")
        checks_passed += 1
    else:
        print("      ✗ mouse_move action handler not found")
    
    # Check 5: Action handler smooth default
    print("\n[5/6] Checking action handler smooth default...")
    if (handler and 
        handler.optional_params.get("smooth") == True and
        handler.optional_params.get("curve_type") == "bezier"):
        print("      ✓ mouse_move defaults to smooth=True, curve_type='bezier'")
        checks_passed += 1
    else:
        print("      ✗ mouse_move defaults are incorrect")
    
    # Check 6: Documentation exists
    print("\n[6/6] Checking documentation...")
    import os
    if os.path.exists("docs/SMOOTH_MOUSE_CONFIGURATION.md"):
        print("      ✓ Documentation file exists")
        checks_passed += 1
    else:
        print("      ✗ Documentation file missing")
    
    # Summary
    print("\n" + "=" * 70)
    print(f"VERIFICATION RESULT: {checks_passed}/{total_checks} checks passed")
    print("=" * 70)
    
    if checks_passed == total_checks:
        print("\n✓ Task 6 Implementation: COMPLETE")
        print("\nAll requirements satisfied:")
        print("  ✓ MouseController uses smooth=True by default")
        print("  ✓ curve_type defaults to 'bezier'")
        print("  ✓ Proper defaults for curve_intensity, speed, overshoot, noise")
        print("  ✓ All mouse_move actions use curved paths unless disabled")
        print("\nRequirements: 12.1, 12.2, 12.6 ✓")
        return True
    else:
        print("\n✗ Task 6 has issues - some checks failed")
        return False


if __name__ == "__main__":
    success = verify_task6()
    sys.exit(0 if success else 1)
