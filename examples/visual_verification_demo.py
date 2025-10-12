"""
Visual Verification Demo

This example demonstrates how to use visual verification in a protocol.
It shows how the AI can pause execution, verify screen state, and adapt
based on what it sees.
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


def create_visual_verification_protocol() -> ProtocolSchema:
    """
    Create a protocol that demonstrates visual verification.
    
    This protocol:
    1. Opens Notepad
    2. Verifies Notepad is open
    3. Uses verified coordinates to interact with the window
    4. Types some text
    """
    return ProtocolSchema(
        version="1.0",
        metadata=Metadata(
            description="Visual verification demo with Notepad",
            complexity="medium",
            uses_vision=True,
            estimated_duration_seconds=15
        ),
        macros={},
        actions=[
            ActionStep(
                action="open_app",
                params={"app_name": "notepad"},
                wait_after_ms=2000,
                description="Open Notepad application"
            ),
            ActionStep(
                action="verify_screen",
                params={
                    "context": "Looking for Notepad window with text area",
                    "expected": "Notepad window is open with empty text area visible",
                    "confidence_threshold": 0.7
                },
                wait_after_ms=500,
                description="Verify Notepad opened successfully"
            ),
            ActionStep(
                action="type",
                params={
                    "text": "Hello from Visual Verification!\n\nThis text was typed after AI verified the screen state.",
                    "interval_ms": 30
                },
                wait_after_ms=1000,
                description="Type demo text"
            ),
            ActionStep(
                action="verify_screen",
                params={
                    "context": "Looking at Notepad with typed text",
                    "expected": "Text is visible in Notepad",
                    "confidence_threshold": 0.6
                },
                wait_after_ms=500,
                description="Verify text was typed successfully"
            ),
            ActionStep(
                action="delay",
                params={"ms": 2000},
                description="Wait to see the result"
            )
        ]
    )


def create_adaptive_mouse_protocol() -> ProtocolSchema:
    """
    Create a protocol that uses visual verification to find and click elements.
    
    This demonstrates adaptive execution where the AI:
    1. Verifies an element exists
    2. Gets coordinates from the verification
    3. Uses those coordinates to move the mouse
    """
    return ProtocolSchema(
        version="1.0",
        metadata=Metadata(
            description="Adaptive mouse movement with visual verification",
            complexity="medium",
            uses_vision=True,
            estimated_duration_seconds=10
        ),
        macros={},
        actions=[
            ActionStep(
                action="verify_screen",
                params={
                    "context": "Looking for any clickable button or icon on screen",
                    "expected": "At least one clickable element is visible",
                    "confidence_threshold": 0.6
                },
                wait_after_ms=500,
                description="Find a clickable element"
            ),
            ActionStep(
                action="mouse_move",
                params={
                    "x": "{{verified_x}}",
                    "y": "{{verified_y}}",
                    "smooth": True
                },
                wait_after_ms=1000,
                description="Move mouse to verified coordinates"
            ),
            ActionStep(
                action="delay",
                params={"ms": 2000},
                description="Wait to see the mouse position"
            )
        ]
    )


def run_demo(dry_run: bool = False):
    """
    Run the visual verification demo.
    
    Args:
        dry_run: If True, simulate execution without performing actions
    """
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("✗ GEMINI_API_KEY not found in .env file")
        print("  Visual verification requires a Gemini API key")
        return False
    
    print("="*60)
    print("VISUAL VERIFICATION DEMO")
    print("="*60)
    print()
    
    # Initialize components
    print("Initializing components...")
    input_controller = InputController()
    mouse_controller = MouseController()
    screen_capture = ScreenCapture()
    
    # Initialize visual verifier
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
    
    print(f"✓ Action handlers registered")
    print()
    
    # Create protocol executor
    executor = ProtocolExecutor(action_registry, dry_run=dry_run)
    
    # Demo 1: Basic visual verification
    print("="*60)
    print("DEMO 1: Basic Visual Verification with Notepad")
    print("="*60)
    print()
    
    protocol1 = create_visual_verification_protocol()
    result1 = executor.execute_protocol(protocol1)
    
    print()
    print("Result:")
    print(f"  Status: {result1.status}")
    print(f"  Actions completed: {result1.actions_completed}/{result1.total_actions}")
    print(f"  Duration: {result1.duration_ms}ms")
    
    if result1.error:
        print(f"  Error: {result1.error}")
    
    if result1.context:
        print(f"\nExecution Context:")
        variables = result1.context.get('variables', {})
        if variables:
            print(f"  Variables:")
            for key, value in variables.items():
                print(f"    {key}: {value}")
    
    # Demo 2: Adaptive mouse movement
    print()
    print("="*60)
    print("DEMO 2: Adaptive Mouse Movement")
    print("="*60)
    print()
    
    input("Press Enter to continue with adaptive mouse demo...")
    
    protocol2 = create_adaptive_mouse_protocol()
    result2 = executor.execute_protocol(protocol2)
    
    print()
    print("Result:")
    print(f"  Status: {result2.status}")
    print(f"  Actions completed: {result2.actions_completed}/{result2.total_actions}")
    print(f"  Duration: {result2.duration_ms}ms")
    
    if result2.context:
        print(f"\nExecution Context:")
        variables = result2.context.get('variables', {})
        if variables:
            print(f"  Variables:")
            for key, value in variables.items():
                print(f"    {key}: {value}")
    
    # Print visual verifier statistics
    print()
    print("="*60)
    print("VISUAL VERIFIER STATISTICS")
    print("="*60)
    stats = visual_verifier.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print()
    print("="*60)
    print("DEMO COMPLETED")
    print("="*60)
    
    return result1.status == 'success' and result2.status == 'success'


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Visual Verification Demo")
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate execution without performing actions'
    )
    
    args = parser.parse_args()
    
    try:
        success = run_demo(dry_run=args.dry_run)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
