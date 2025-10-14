"""
Test mouse curve movements - demonstrates smooth, human-like mouse control.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from shared.action_registry import ActionRegistry
from shared.action_handlers import ActionHandlers
from shared.protocol_executor import ProtocolExecutor
from shared.protocol_parser import JSONProtocolParser


def test_mouse_curves():
    """Test different mouse curve types."""
    
    print("\n" + "="*60)
    print("🖱️  MOUSE CURVE DEMONSTRATION")
    print("="*60)
    print("\nThis demo showcases:")
    print("  • Bezier curves (smooth S-curves)")
    print("  • Arc curves (circular paths)")
    print("  • Variable speeds (fast/slow)")
    print("  • Complex patterns (figure-8)")
    print("  • Straight lines (no smoothing)")
    print("\n" + "="*60 + "\n")
    
    # Ask for confirmation
    response = input("Watch your mouse move in beautiful curves? (yes/no): ").strip().lower()
    if response != 'yes':
        print("\n❌ Cancelled.")
        return False
    
    print("\n" + "="*60)
    print("Starting in 3 seconds...")
    print("Keep your hands off the mouse!")
    print("="*60 + "\n")
    
    import time
    time.sleep(3)
    
    # Initialize with REAL actions
    action_registry = ActionRegistry()
    
    # Initialize mouse controller for smooth curves
    from automation_engine.mouse_controller import MouseController, MouseConfig
    mouse_config = MouseConfig(
        curve_intensity=0.3,  # Moderate curves
        speed=1.0,
        add_noise=True,
        overshoot=True
    )
    mouse_controller = MouseController(mouse_config)
    
    # Initialize input controller
    from automation_engine.input_controller import InputController
    input_controller = InputController()
    
    # Inject dependencies
    action_registry.inject_dependencies(
        input_controller=input_controller,
        mouse_controller=mouse_controller
    )
    
    real_handlers = ActionHandlers(action_registry)
    real_handlers.register_all()
    
    print("✓ Real action handlers registered")
    
    # Load the mouse curves protocol
    parser = JSONProtocolParser()
    
    print("Loading protocol from: examples/protocols/mouse_curves_demo.json")
    import json
    with open('examples/protocols/mouse_curves_demo.json', 'r') as f:
        protocol_dict = json.load(f)
    protocol = parser.parse_dict(protocol_dict)
    
    print(f"\nProtocol loaded:")
    print(f"  Description: {protocol.metadata.description}")
    print(f"  Actions: {len(protocol.actions)}")
    print(f"  Demonstrations: 6 different curve types")
    print(f"\n" + "="*60 + "\n")
    
    # Execute the protocol
    executor = ProtocolExecutor(action_registry, dry_run=False)
    
    print("🖱️  Watch your mouse move!\n")
    print("The demo will show:")
    print("  1. Bezier curves (square pattern)")
    print("  2. Arc curves (square pattern)")
    print("  3. Fast speed movements")
    print("  4. Slow speed movements")
    print("  5. Figure-8 pattern")
    print("  6. Straight lines (no curves)")
    print("\n" + "="*60 + "\n")
    
    result = executor.execute_protocol(protocol)
    
    # Print results
    print(f"\n" + "="*60)
    print("EXECUTION RESULT")
    print("="*60)
    print(f"Status: {result.status}")
    print(f"Actions completed: {result.actions_completed}/{len(protocol.actions)}")
    print(f"Duration: {result.duration_ms}ms ({result.duration_ms/1000:.2f}s)")
    if result.error:
        print(f"Error: {result.error}")
    print("="*60 + "\n")
    
    if result.status == 'success':
        print("✅ All curve demonstrations completed!")
        print("\nYou should have seen:")
        print("  ✓ Smooth bezier curves")
        print("  ✓ Circular arc movements")
        print("  ✓ Fast and slow speeds")
        print("  ✓ Complex figure-8 pattern")
        print("  ✓ Direct straight lines")
        print("\nThe mouse controller creates human-like movements!")
    
    return result.status == 'success'


if __name__ == "__main__":
    print("\n" + "="*60)
    print("MOUSE CURVE DEMONSTRATION")
    print("="*60)
    print("\nThis demo shows the advanced mouse control features:")
    print("\n📊 Curve Types:")
    print("  • Bezier - Smooth S-shaped curves")
    print("  • Arc - Circular arc paths")
    print("\n⚡ Speed Control:")
    print("  • Fast (2.0x speed)")
    print("  • Normal (1.0x speed)")
    print("  • Slow (0.5x speed)")
    print("\n🎯 Features:")
    print("  • Human-like movements")
    print("  • Smooth acceleration/deceleration")
    print("  • Natural-looking paths")
    print("  • Avoids detection as bot")
    print("\n" + "="*60)
    
    try:
        success = test_mouse_curves()
        
        if success:
            print("\n✅ SUCCESS! Mouse curves work perfectly!")
            print("\nThe automation engine has:")
            print("  ✓ Smooth bezier curve support")
            print("  ✓ Circular arc path support")
            print("  ✓ Variable speed control")
            print("  ✓ Human-like movement patterns")
            print("  ✓ Natural acceleration curves")
        else:
            print("\n❌ Test was cancelled or failed.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("Demo complete!")
    print("="*60 + "\n")
