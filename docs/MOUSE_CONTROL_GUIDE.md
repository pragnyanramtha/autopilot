# Mouse Control System Guide

## Overview

The Advanced Mouse Controller provides smooth, human-like mouse movements using curved paths instead of straight lines. This makes automation look more natural and less robotic.

## Quick Start

### Basic Usage

```python
from automation_engine.mouse_controller import MouseController

# Create controller with default settings
mouse = MouseController()

# Move to position with smooth curve
mouse.move_to(500, 300)

# Click at position
mouse.click(500, 300)

# Drag from current position to target
mouse.drag_to(800, 400)

# Scroll at position
mouse.scroll(5, x=500, y=300)  # Scroll up 5 units
```

### Custom Configuration

```python
from automation_engine.mouse_controller import MouseController, MouseConfig

# Create custom configuration
config = MouseConfig(
    curve_intensity=0.5,    # More curved movements
    speed=1.5,              # 50% faster
    overshoot=True,         # Enable overshoot
    add_noise=True          # Add random variations
)

mouse = MouseController(config)
mouse.move_to(500, 300)
```

## Movement Types

### 1. Bezier Curves (Default)

Smooth curved paths using cubic Bezier curves. Best for natural-looking movements.

```python
mouse.move_to(500, 300, curve_type='bezier')
```

**Characteristics:**
- Smooth S-shaped curves
- Natural acceleration/deceleration
- Most human-like appearance

**Use Cases:**
- General mouse movements
- Clicking buttons
- Navigating interfaces

### 2. Arc Paths

Follows a circular arc between points. Good for sweeping motions.

```python
mouse.move_to(500, 300, curve_type='arc')
```

**Characteristics:**
- Circular arc path
- Consistent curvature
- Predictable trajectory

**Use Cases:**
- Sweeping gestures
- Circular selections
- Arc-like movements

### 3. Wave Patterns

Adds sinusoidal wave to the path. Creates oscillating movement.

```python
mouse.move_to(500, 300, curve_type='wave')
```

**Characteristics:**
- Oscillating path
- Wave-like motion
- Unique visual effect

**Use Cases:**
- Special effects
- Attention-grabbing movements
- Creative animations

## Configuration Options

### MouseConfig Parameters

```python
MouseConfig(
    # Movement Settings
    curve_intensity=0.3,      # 0.0 = straight, 1.0 = very curved
    speed=1.0,                # Speed multiplier (higher = faster)
    overshoot=True,           # Overshoot target then correct
    overshoot_amount=0.05,    # Overshoot distance (5% of movement)
    
    # Randomization (Human-like behavior)
    add_noise=True,           # Add random micro-adjustments
    noise_amount=2.0,         # Noise magnitude in pixels
    
    # Timing
    min_duration=0.3,         # Minimum movement time (seconds)
    max_duration=1.5,         # Maximum movement time (seconds)
    
    # Click Settings
    click_delay_min=0.05,     # Min delay before click
    click_delay_max=0.15,     # Max delay before click
    
    # Safety
    boundary_margin=5         # Pixels from screen edge
)
```

### Curve Intensity Examples

```python
# Straight line (robotic)
config = MouseConfig(curve_intensity=0.0)

# Slight curve (subtle)
config = MouseConfig(curve_intensity=0.2)

# Medium curve (natural) - DEFAULT
config = MouseConfig(curve_intensity=0.3)

# Strong curve (obvious)
config = MouseConfig(curve_intensity=0.7)

# Very curved (exaggerated)
config = MouseConfig(curve_intensity=1.0)
```

### Speed Examples

```python
# Slow motion (0.5x speed)
config = MouseConfig(speed=0.5)

# Normal speed (1.0x) - DEFAULT
config = MouseConfig(speed=1.0)

# Fast (2x speed)
config = MouseConfig(speed=2.0)

# Very fast (3x speed)
config = MouseConfig(speed=3.0)
```

## Advanced Features

### Overshoot & Correction

Mimics human behavior by slightly overshooting the target, then correcting.

```python
config = MouseConfig(
    overshoot=True,
    overshoot_amount=0.08  # 8% overshoot
)
mouse = MouseController(config)
mouse.move_to(500, 300)
# Will overshoot to ~540, 324, then correct to 500, 300
```

**When to Use:**
- Long-distance movements
- Clicking small targets
- Simulating human aiming

**When to Disable:**
- Precise positioning required
- Short movements
- Rapid successive clicks

### Random Noise

Adds small random variations to the path for imperfection.

```python
config = MouseConfig(
    add_noise=True,
    noise_amount=3.0  # 3 pixels of variation
)
mouse = MouseController(config)
mouse.move_to(500, 300)
```

**Benefits:**
- More human-like
- Prevents perfect paths
- Harder to detect as automation

**Considerations:**
- May reduce precision
- Can look jittery if too high
- Disable for pixel-perfect tasks

### Duration Control

Control how long movements take:

```python
# Auto-calculated based on distance (default)
mouse.move_to(500, 300)

# Fixed duration (0.5 seconds)
mouse.move_to(500, 300, duration=0.5)

# Very slow (2 seconds)
mouse.move_to(500, 300, duration=2.0)

# Very fast (0.2 seconds)
mouse.move_to(500, 300, duration=0.2)
```

## Click Operations

### Basic Click

```python
# Click at current position
mouse.click()

# Click at specific position (moves first)
mouse.click(500, 300)

# Right-click
mouse.click(500, 300, button='right')

# Double-click
mouse.click(500, 300, clicks=2)

# Middle-click
mouse.click(500, 300, button='middle')
```

### Click Without Moving

```python
# Move to position first
mouse.move_to(500, 300)

# Click without additional movement
mouse.click(button='left', move_first=False)
```

### Click with Custom Delay

The controller automatically adds a random delay before clicking (0.05-0.15 seconds by default). Customize this:

```python
config = MouseConfig(
    click_delay_min=0.1,   # Minimum 100ms delay
    click_delay_max=0.3    # Maximum 300ms delay
)
mouse = MouseController(config)
mouse.click(500, 300)
```

## Drag Operations

### Basic Drag

```python
# Drag from current position to target
mouse.drag_to(800, 400)

# Drag with specific button
mouse.drag_to(800, 400, button='left')

# Drag with custom duration
mouse.drag_to(800, 400, duration=1.5)
```

### Drag Workflow

```python
# 1. Move to start position
mouse.move_to(100, 100)

# 2. Drag to end position
mouse.drag_to(500, 500)

# The drag will follow a smooth curved path
```

## Scroll Operations

```python
# Scroll up 5 units at current position
mouse.scroll(5)

# Scroll down 3 units at current position
mouse.scroll(-3)

# Scroll at specific position
mouse.scroll(5, x=500, y=300)
```

## Utility Methods

### Get Current Position

```python
x, y = mouse.get_position()
print(f"Mouse is at ({x}, {y})")
```

### Get Screen Size

```python
width, height = pyautogui.size()
print(f"Screen is {width}x{height}")
```

## Practical Examples

### Example 1: Click Button

```python
from automation_engine.mouse_controller import MouseController

mouse = MouseController()

# Move to button and click
button_x, button_y = 500, 300
mouse.click(button_x, button_y)
```

### Example 2: Fill Form

```python
mouse = MouseController()

# Click first field
mouse.click(300, 200)
time.sleep(0.2)

# Type text (using keyboard controller)
# ...

# Click second field
mouse.click(300, 250)
time.sleep(0.2)

# Type text
# ...

# Click submit button
mouse.click(400, 350)
```

### Example 3: Drag and Drop

```python
mouse = MouseController()

# Move to item
mouse.move_to(200, 200)
time.sleep(0.2)

# Drag to target location
mouse.drag_to(600, 400)
```

### Example 4: Scroll Through Page

```python
mouse = MouseController()

# Move to page center
mouse.move_to(800, 400)

# Scroll down in increments
for _ in range(5):
    mouse.scroll(-3)  # Scroll down
    time.sleep(0.5)
```

### Example 5: Natural Navigation

```python
from automation_engine.mouse_controller import MouseController, MouseConfig

# Configure for very natural movement
config = MouseConfig(
    curve_intensity=0.4,
    speed=0.8,
    overshoot=True,
    overshoot_amount=0.1,
    add_noise=True,
    noise_amount=3.0
)

mouse = MouseController(config)

# Navigate through menu items
menu_items = [
    (100, 50),   # File
    (200, 50),   # Edit
    (300, 50),   # View
    (400, 50),   # Help
]

for x, y in menu_items:
    mouse.move_to(x, y)
    time.sleep(0.3)
```

## Integration with Automation System

### Using in Workflows

The mouse controller is automatically integrated into the automation system:

```python
from automation_engine.input_controller import InputController

# Input controller uses smooth mouse by default
controller = InputController(use_smooth_mouse=True)

# All mouse operations use smooth movements
controller.move_mouse(500, 300)
controller.click(500, 300)
```

### Disable Smooth Mouse

If you need direct movements (no curves):

```python
controller = InputController(use_smooth_mouse=False)

# Uses PyAutoGUI directly (straight lines)
controller.move_mouse(500, 300)
```

## Performance Considerations

### Path Generation

- **Calculation Time**: ~5ms per movement
- **Memory Usage**: ~10KB per path
- **Frame Rate**: 60 FPS path generation

### Optimization Tips

1. **Reduce Points for Short Movements**
   - Automatically handled by duration calculation
   - Shorter movements = fewer points

2. **Disable Features for Speed**
   ```python
   config = MouseConfig(
       overshoot=False,      # Skip overshoot
       add_noise=False,      # Skip noise
       curve_intensity=0.1   # Minimal curve
   )
   ```

3. **Use Direct Mode for Rapid Clicks**
   ```python
   controller = InputController(use_smooth_mouse=False)
   ```

## Troubleshooting

### Movement Too Slow

```python
# Increase speed
config = MouseConfig(speed=2.0)

# Or reduce min_duration
config = MouseConfig(min_duration=0.1)
```

### Movement Too Fast

```python
# Decrease speed
config = MouseConfig(speed=0.5)

# Or increase min_duration
config = MouseConfig(min_duration=0.5)
```

### Too Much Curve

```python
# Reduce curve intensity
config = MouseConfig(curve_intensity=0.1)

# Or use straight lines
config = MouseConfig(curve_intensity=0.0)
```

### Not Enough Curve

```python
# Increase curve intensity
config = MouseConfig(curve_intensity=0.7)
```

### Jittery Movement

```python
# Reduce noise
config = MouseConfig(noise_amount=1.0)

# Or disable noise
config = MouseConfig(add_noise=False)
```

### Missing Target

```python
# Disable overshoot
config = MouseConfig(overshoot=False)

# Increase click delay
config = MouseConfig(
    click_delay_min=0.2,
    click_delay_max=0.3
)
```

## Safety Features

### Boundary Protection

All coordinates are automatically clamped to screen boundaries:

```python
# Even if you specify off-screen coordinates
mouse.move_to(10000, 10000)
# Will move to (screen_width - 5, screen_height - 5)
```

### Fail-Safe

PyAutoGUI's fail-safe is enabled by default:

- Move mouse to upper-left corner to emergency stop
- Raises `pyautogui.FailSafeException`
- Immediately halts all operations

### Coordinate Validation

All coordinates are validated before movement:

- Negative values clamped to margin
- Values beyond screen clamped to screen - margin
- Invalid coordinates raise exceptions

## Best Practices

### 1. Choose Appropriate Curve Type

- **Bezier**: General use, most natural
- **Arc**: Sweeping motions, circular paths
- **Wave**: Special effects only

### 2. Adjust Speed Based on Context

- **Slow (0.5x)**: Precise operations, demonstrations
- **Normal (1.0x)**: General automation
- **Fast (2.0x)**: Rapid navigation, testing

### 3. Use Overshoot Selectively

- **Enable**: Long movements, human simulation
- **Disable**: Precise positioning, rapid clicks

### 4. Configure Noise Appropriately

- **High (3-5px)**: Very human-like, less precise
- **Medium (2-3px)**: Balanced (default)
- **Low (1px)**: Subtle variation
- **None (0px)**: Perfect paths

### 5. Test Before Production

Always test your configuration:

```python
# Run the demo script
python examples/mouse_demo.py

# Or test your specific configuration
config = MouseConfig(...)
mouse = MouseController(config)
# Test movements...
```

## Running the Demo

To see all features in action:

```bash
# Windows
python examples\mouse_demo.py

# Linux/Mac
python examples/mouse_demo.py
```

The demo showcases:
- Basic movements
- Different curve types
- Speed variations
- Curve intensity levels
- Overshoot behavior
- Click operations
- Drag operations
- Human-like behavior

## Further Reading

- [System Architecture](SYSTEM_ARCHITECTURE.md) - Complete system overview
- [API Reference](API_REFERENCE.md) - Detailed API documentation
- [Examples](../examples/) - More code examples
