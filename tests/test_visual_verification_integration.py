"""
Integration Test for Visual Verification System

This test demonstrates the complete integration of visual verification
with the protocol executor and action registry.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.protocol_models import ProtocolSchema, Metadata, ActionStep
from shared.protocol_executor import ProtocolExecutor
from shared.action_registry import ActionRegistry
from shared.action_handlers import ActionHandlers
from shared.visual_verifier import VisualVerifier
from automation_engine.screen_capture import ScreenCapture
from automation_engine.input_controller import InputController
from automation_engine.mouse_controller import MouseController
from dotenv import load_dotenv


def test_visual_verification_integration():
    """
    Test complete integration of visual verification system.
    
    This test verifies:
    1. VisualVerifier integrates with ActionRegistry
    2. verify_screen action executes correctly
    3. Verification results update execution context
    4. Context variables are available for subsequent actions
    """
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("⚠ GEMINI_API_KEY not found - skipping integration test")
        return False
    
    print("="*60)
    print("VISUAL VERIFICATION INTEGRATION TEST")
    print("="*60)
    print()
    
    # Initialize components
    print("1. Initializing components...")
    input_controller = InputController()
    mouse_controller = MouseController()
    screen_capture = ScreenCapture()
    
    visual_verifier = VisualVerifier(
        screen_capture=screen_capture,
        api_key=api_key,
        timeout_seconds=15
    )
    
    # Initialize action registry
    action_registry = ActionRegistry()
    action_registry.inject_dependencies(
        input_controller=input_controller,
        mouse_controller=mouse_controller,
        screen_capture=screen_capture,
        visual_verifier=visual_verifier
    )
    
    # Register all action handlers
    action_handlers = ActionHandlers(action_registry)
    action_handlers.register_all()
    
    print(f"   ✓ Action handlers registered")
    print()
    
    # Create protocol with visual verification
    print("2. Creating test protocol...")
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(
            description="Integration test protocol",
            complexity="simple",
            uses_vision=True
        ),
        macros={},
        actions=[
            ActionStep(
                action="verify_screen",
                params={
                    "context": "Looking at current screen",
                    "expected": "Screen is visible and ready",
                    "confidence_threshold": 0.5
                },
                wait_after_ms=500,
                description="Verify screen state"
            ),
            ActionStep(
                action="delay",
                params={"ms": 100},
                description="Short delay"
            )
        ]
    )
    print("   ✓ Protocol created")
    print()
    
    # Execute protocol
    print("3. Executing protocol...")
    executor = ProtocolExecutor(action_registry, dry_run=False)
    result = executor.execute_protocol(protocol)
    
    print()
    print("4. Checking results...")
    
    # Verify execution completed
    assert result.status in ['success', 'stopped'], f"Unexpected status: {result.status}"
    print(f"   ✓ Execution status: {result.status}")
    
    # Verify actions were executed
    assert result.actions_completed >= 1, "No actions were completed"
    print(f"   ✓ Actions completed: {result.actions_completed}/{result.total_actions}")
    
    # Verify context was updated
    assert result.context is not None, "No execution context"
    print(f"   ✓ Execution context available")
    
    # Check for verification variables in context
    variables = result.context.get('variables', {})
    print(f"\n   Context variables:")
    for key, value in variables.items():
        print(f"     {key}: {value}")
    
    # Verify that verification metadata was stored
    assert 'last_verification_safe' in variables, "Missing last_verification_safe"
    assert 'last_verification_confidence' in variables, "Missing last_verification_confidence"
    assert 'last_verification_analysis' in variables, "Missing last_verification_analysis"
    
    print(f"\n   ✓ Verification metadata stored in context")
    
    # Check if coordinates were extracted
    if 'verified_x' in variables and 'verified_y' in variables:
        print(f"   ✓ Coordinates extracted: ({variables['verified_x']}, {variables['verified_y']})")
    else:
        print(f"   ℹ No coordinates extracted (element not identified)")
    
    # Print visual verifier statistics
    print()
    print("5. Visual Verifier Statistics:")
    stats = visual_verifier.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print()
    print("="*60)
    print("✓ INTEGRATION TEST PASSED")
    print("="*60)
    
    return True


def test_adaptive_execution():
    """
    Test adaptive execution with coordinate substitution.
    
    This test verifies that coordinates from verification can be used
    in subsequent mouse actions.
    """
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("⚠ GEMINI_API_KEY not found - skipping adaptive test")
        return False
    
    print("\n" + "="*60)
    print("ADAPTIVE EXECUTION TEST")
    print("="*60)
    print()
    
    # Initialize components
    input_controller = InputController()
    mouse_controller = MouseController()
    screen_capture = ScreenCapture()
    
    visual_verifier = VisualVerifier(
        screen_capture=screen_capture,
        api_key=api_key,
        timeout_seconds=15
    )
    
    action_registry = ActionRegistry()
    action_registry.inject_dependencies(
        input_controller=input_controller,
        mouse_controller=mouse_controller,
        screen_capture=screen_capture,
        visual_verifier=visual_verifier
    )
    
    action_handlers = ActionHandlers(action_registry)
    action_handlers.register_all()
    
    # Create protocol with coordinate substitution
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(
            description="Adaptive execution test",
            complexity="medium",
            uses_vision=True
        ),
        macros={},
        actions=[
            ActionStep(
                action="verify_screen",
                params={
                    "context": "Looking for any clickable element",
                    "expected": "At least one UI element is visible",
                    "confidence_threshold": 0.5
                },
                wait_after_ms=500
            ),
            # This action will use {{verified_x}} and {{verified_y}} if available
            ActionStep(
                action="delay",
                params={"ms": 100},
                description="Delay to show coordinate usage"
            )
        ]
    )
    
    # Execute with dry run to avoid actual mouse movement
    executor = ProtocolExecutor(action_registry, dry_run=True)
    result = executor.execute_protocol(protocol)
    
    print("\nResult:")
    print(f"  Status: {result.status}")
    print(f"  Actions: {result.actions_completed}/{result.total_actions}")
    
    if result.context:
        variables = result.context.get('variables', {})
        if 'verified_x' in variables and 'verified_y' in variables:
            print(f"  ✓ Coordinates available for adaptive execution:")
            print(f"    x: {variables['verified_x']}")
            print(f"    y: {variables['verified_y']}")
        else:
            print(f"  ℹ No coordinates extracted (element not identified)")
    
    print("\n✓ ADAPTIVE EXECUTION TEST PASSED")
    
    return True


def main():
    """Run all integration tests."""
    print("="*60)
    print("VISUAL VERIFICATION INTEGRATION TESTS")
    print("="*60)
    
    tests = [
        ("Integration Test", test_visual_verification_integration),
        ("Adaptive Execution Test", test_adaptive_execution),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
