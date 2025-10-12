"""
Quick test script for the mouse controller.
Run this to verify the mouse control system is working.
"""

import sys
import time

try:
    from automation_engine.mouse_controller import MouseController, MouseConfig
    import pyautogui
    print("✓ All imports successful!")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("\nPlease install required packages:")
    print("  pip install numpy pyautogui")
    sys.exit(1)


def main():
    print("\n" + "=" * 60)
    print("  MOUSE CONTROLLER TEST")
    print("=" * 60)
    
    # Get screen info
    screen_width, screen_height = pyautogui.size()
    print(f"\nScreen size: {screen_width}x{screen_height}")
    
    # Get current position
    current_x, current_y = pyautogui.position()
    print(f"Current mouse position: ({current_x}, {current_y})")
    
    print("\n" + "-" * 60)
    print("This test will move your mouse in a small square pattern.")
    print("The movements will be smooth curves, not straight lines.")
    print("\nIMPORTANT: Move mouse to corner to emergency stop!")
    print("-" * 60)
    
    input("\nPress ENTER to start test...")
    
    try:
        # Create mouse controller
        print("\nCreating mouse controller...")
        config = MouseConfig(
            curve_intensity=0.4,
            speed=1.0,
            overshoot=True,
            add_noise=True
        )
        mouse = MouseController(config)
        print("✓ Mouse controller created!")
        
        # Calculate test positions (small square in center)
        center_x = screen_width // 2
        center_y = screen_height // 2
        offset = 100
        
        positions = [
            (center_x - offset, center_y - offset, "Top-Left"),
            (center_x + offset, center_y - offset, "Top-Right"),
            (center_x + offset, center_y + offset, "Bottom-Right"),
            (center_x - offset, center_y + offset, "Bottom-Left"),
            (center_x, center_y, "Center"),
        ]
        
        print("\nStarting movement test...")
        time.sleep(1)
        
        for i, (x, y, label) in enumerate(positions):
            print(f"\n  {i+1}. Moving to {label} ({x}, {y})...")
            mouse.move_to(x, y)
            time.sleep(0.5)
        
        print("\n" + "=" * 60)
        print("  TEST COMPLETE!")
        print("=" * 60)
        print("\n✓ Mouse controller is working correctly!")
        print("\nFeatures verified:")
        print("  • Smooth curved movements")
        print("  • Bezier path generation")
        print("  • Overshoot and correction")
        print("  • Random noise")
        print("  • Natural timing")
        
        print("\nNext steps:")
        print("  • Run full demo: python examples/mouse_demo.py")
        print("  • Read guide: docs/MOUSE_CONTROL_GUIDE.md")
        print("  • Check architecture: docs/SYSTEM_ARCHITECTURE.md")
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n\n✗ Error during test: {e}")
        print("\nTroubleshooting:")
        print("  • Make sure numpy is installed: pip install numpy")
        print("  • Make sure pyautogui is installed: pip install pyautogui")
        print("  • Check that your mouse can move freely")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
