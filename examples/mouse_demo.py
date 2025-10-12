"""
Mouse Controller Demo
Demonstrates the advanced mouse control system with smooth curved movements.
"""

import time
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from automation_engine.mouse_controller import MouseController, MouseConfig
import pyautogui


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def demo_basic_movement():
    """Demo 1: Basic smooth movement."""
    print_header("Demo 1: Basic Smooth Movement")
    
    mouse = MouseController()
    screen_width, screen_height = pyautogui.size()
    
    print("Moving mouse in a square pattern with smooth curves...")
    print("Watch how the mouse moves in smooth curves, not straight lines!")
    time.sleep(2)
    
    # Square pattern
    points = [
        (screen_width // 4, screen_height // 4),
        (3 * screen_width // 4, screen_height // 4),
        (3 * screen_width // 4, 3 * screen_height // 4),
        (screen_width // 4, 3 * screen_height // 4),
        (screen_width // 2, screen_height // 2),  # Center
    ]
    
    for i, (x, y) in enumerate(points):
        print(f"  Moving to point {i+1}: ({x}, {y})")
        mouse.move_to(x, y)
        time.sleep(0.5)
    
    print("✓ Basic movement complete!")


def demo_curve_types():
    """Demo 2: Different curve types."""
    print_header("Demo 2: Different Curve Types")
    
    mouse = MouseController()
    screen_width, screen_height = pyautogui.size()
    
    center_x = screen_width // 2
    center_y = screen_height // 2
    
    # Start at center
    mouse.move_to(center_x, center_y)
    time.sleep(1)
    
    curve_types = ['bezier', 'arc', 'wave']
    
    for curve_type in curve_types:
        print(f"\n  Testing {curve_type.upper()} curve...")
        
        # Move to corner
        target_x = screen_width - 200
        target_y = 200
        
        print(f"    Moving to ({target_x}, {target_y}) with {curve_type} curve")
        mouse.move_to(target_x, target_y, curve_type=curve_type)
        time.sleep(0.5)
        
        # Move back to center
        print(f"    Moving back to center with {curve_type} curve")
        mouse.move_to(center_x, center_y, curve_type=curve_type)
        time.sleep(0.5)
    
    print("\n✓ Curve types demo complete!")


def demo_speed_control():
    """Demo 3: Speed control."""
    print_header("Demo 3: Speed Control")
    
    screen_width, screen_height = pyautogui.size()
    start_x = screen_width // 4
    start_y = screen_height // 2
    end_x = 3 * screen_width // 4
    end_y = screen_height // 2
    
    speeds = [0.5, 1.0, 2.0]
    
    for speed in speeds:
        print(f"\n  Testing speed: {speed}x")
        
        config = MouseConfig(speed=speed)
        mouse = MouseController(config)
        
        # Move to start
        mouse.move_to(start_x, start_y, duration=0.3)
        time.sleep(0.3)
        
        # Move across screen
        print(f"    Moving across screen at {speed}x speed...")
        start_time = time.time()
        mouse.move_to(end_x, end_y)
        duration = time.time() - start_time
        print(f"    Took {duration:.2f} seconds")
        
        time.sleep(0.5)
    
    print("\n✓ Speed control demo complete!")


def demo_curve_intensity():
    """Demo 4: Curve intensity."""
    print_header("Demo 4: Curve Intensity")
    
    screen_width, screen_height = pyautogui.size()
    start_x = 200
    start_y = screen_height // 2
    end_x = screen_width - 200
    end_y = screen_height // 2
    
    intensities = [0.0, 0.3, 0.7, 1.0]
    
    for intensity in intensities:
        print(f"\n  Testing curve intensity: {intensity}")
        
        config = MouseConfig(curve_intensity=intensity)
        mouse = MouseController(config)
        
        # Move to start
        mouse.move_to(start_x, start_y, duration=0.3)
        time.sleep(0.3)
        
        # Move with curve
        print(f"    Moving with {intensity} curve intensity...")
        if intensity == 0.0:
            print("    (Should be nearly straight)")
        elif intensity == 1.0:
            print("    (Should be very curved)")
        
        mouse.move_to(end_x, end_y)
        time.sleep(0.5)
    
    print("\n✓ Curve intensity demo complete!")


def demo_overshoot():
    """Demo 5: Overshoot behavior."""
    print_header("Demo 5: Overshoot & Correction")
    
    screen_width, screen_height = pyautogui.size()
    center_x = screen_width // 2
    center_y = screen_height // 2
    
    print("\n  WITHOUT overshoot:")
    config_no_overshoot = MouseConfig(overshoot=False)
    mouse = MouseController(config_no_overshoot)
    
    mouse.move_to(center_x - 200, center_y)
    time.sleep(0.3)
    print("    Moving to center (no overshoot)...")
    mouse.move_to(center_x, center_y)
    time.sleep(1)
    
    print("\n  WITH overshoot:")
    config_overshoot = MouseConfig(overshoot=True, overshoot_amount=0.1)
    mouse = MouseController(config_overshoot)
    
    mouse.move_to(center_x - 200, center_y)
    time.sleep(0.3)
    print("    Moving to center (with overshoot)...")
    print("    Watch carefully - it will overshoot then correct!")
    mouse.move_to(center_x, center_y)
    time.sleep(1)
    
    print("\n✓ Overshoot demo complete!")


def demo_click_operations():
    """Demo 6: Click operations."""
    print_header("Demo 6: Click Operations")
    
    mouse = MouseController()
    screen_width, screen_height = pyautogui.size()
    
    print("\n  This demo will move and click at various positions.")
    print("  No actual clicks will be performed (safe demo mode).")
    time.sleep(2)
    
    # Define click targets
    targets = [
        (screen_width // 4, screen_height // 4, "Top-Left"),
        (3 * screen_width // 4, screen_height // 4, "Top-Right"),
        (screen_width // 2, screen_height // 2, "Center"),
        (screen_width // 4, 3 * screen_height // 4, "Bottom-Left"),
        (3 * screen_width // 4, 3 * screen_height // 4, "Bottom-Right"),
    ]
    
    for x, y, label in targets:
        print(f"\n  Moving to {label} ({x}, {y})...")
        mouse.move_to(x, y)
        print(f"    Would click here!")
        time.sleep(0.5)
    
    print("\n✓ Click operations demo complete!")


def demo_drag_operation():
    """Demo 7: Drag operation."""
    print_header("Demo 7: Drag Operation")
    
    mouse = MouseController()
    screen_width, screen_height = pyautogui.size()
    
    print("\n  Demonstrating drag operation...")
    print("  (No actual drag will be performed)")
    time.sleep(2)
    
    start_x = screen_width // 3
    start_y = screen_height // 2
    end_x = 2 * screen_width // 3
    end_y = screen_height // 2
    
    print(f"\n  Moving to start position ({start_x}, {start_y})...")
    mouse.move_to(start_x, start_y)
    time.sleep(0.5)
    
    print(f"  Would drag to ({end_x}, {end_y})...")
    print("  (Simulating drag movement)")
    mouse.move_to(end_x, end_y, duration=1.5)
    
    print("\n✓ Drag operation demo complete!")


def demo_human_like_behavior():
    """Demo 8: Human-like behavior."""
    print_header("Demo 8: Human-Like Behavior")
    
    print("\n  This demo shows all human-like features combined:")
    print("  • Smooth curves (not straight lines)")
    print("  • Random noise (micro-adjustments)")
    print("  • Overshoot and correction")
    print("  • Natural acceleration/deceleration")
    time.sleep(3)
    
    config = MouseConfig(
        curve_intensity=0.4,
        speed=0.8,
        overshoot=True,
        overshoot_amount=0.08,
        add_noise=True,
        noise_amount=3.0
    )
    
    mouse = MouseController(config)
    screen_width, screen_height = pyautogui.size()
    
    # Random movements
    import random
    
    print("\n  Performing random movements...")
    for i in range(5):
        x = random.randint(200, screen_width - 200)
        y = random.randint(200, screen_height - 200)
        
        print(f"    Movement {i+1}: ({x}, {y})")
        mouse.move_to(x, y)
        time.sleep(0.3)
    
    print("\n✓ Human-like behavior demo complete!")


def main():
    """Run all demos."""
    print("\n" + "=" * 60)
    print("  ADVANCED MOUSE CONTROLLER DEMO")
    print("  Smooth Curved Movements System")
    print("=" * 60)
    
    print("\nThis demo will showcase the advanced mouse control features.")
    print("\nIMPORTANT:")
    print("  • Your mouse will move automatically")
    print("  • Move your mouse to the corner to emergency stop")
    print("  • No actual clicks will be performed")
    print("  • Safe to run on any system")
    
    input("\nPress ENTER to start the demo...")
    
    try:
        # Run demos
        demo_basic_movement()
        time.sleep(2)
        
        demo_curve_types()
        time.sleep(2)
        
        demo_speed_control()
        time.sleep(2)
        
        demo_curve_intensity()
        time.sleep(2)
        
        demo_overshoot()
        time.sleep(2)
        
        demo_click_operations()
        time.sleep(2)
        
        demo_drag_operation()
        time.sleep(2)
        
        demo_human_like_behavior()
        
        # Final message
        print("\n" + "=" * 60)
        print("  DEMO COMPLETE!")
        print("=" * 60)
        print("\nAll mouse movement features demonstrated successfully!")
        print("\nKey Features:")
        print("  ✓ Smooth Bezier curves")
        print("  ✓ Multiple curve types (bezier, arc, wave)")
        print("  ✓ Speed control")
        print("  ✓ Curve intensity adjustment")
        print("  ✓ Overshoot and correction")
        print("  ✓ Random noise for realism")
        print("  ✓ Natural acceleration/deceleration")
        print("  ✓ Human-like behavior")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nError during demo: {e}")
    
    print("\nThank you for watching!")


if __name__ == "__main__":
    main()
