# Advanced Mouse Control System

## 🎯 Overview

This AI Automation Assistant now includes an **Advanced Mouse Control System** that moves the mouse in **smooth, curved paths** instead of straight lines, making automation look natural and human-like.

## ✨ Key Features

### 🌊 Smooth Curved Movements
- **Bezier Curves**: Natural S-shaped paths
- **Arc Paths**: Circular sweeping motions  
- **Wave Patterns**: Oscillating movements
- No more robotic straight lines!

### 🎭 Human-Like Behavior
- **Overshoot & Correction**: Slightly overshoots target, then corrects (like humans do)
- **Random Noise**: Micro-adjustments during movement
- **Natural Timing**: Smooth acceleration and deceleration
- **Variable Speed**: Adjusts based on distance

### ⚙️ Highly Configurable
- Curve intensity (0.0 = straight, 1.0 = very curved)
- Movement speed (0.5x to 3.0x)
- Overshoot amount
- Noise level
- Click delays
- And more!

### 🛡️ Safety Features
- Automatic boundary protection
- Emergency stop (move to corner)
- Coordinate validation
- Fail-safe mechanisms

## 🚀 Quick Start

### 1. Test the System

```bash
# Quick test (moves mouse in small square)
python test_mouse.py

# Full demo (showcases all features)
python examples/mouse_demo.py
```

### 2. Basic Usage

```python
from automation_engine.mouse_controller import MouseController

# Create controller
mouse = MouseController()

# Move with smooth curve
mouse.move_to(500, 300)

# Click at position
mouse.click(500, 300)

# Drag smoothly
mouse.drag_to(800, 400)
```

### 3. Custom Configuration

```python
from automation_engine.mouse_controller import MouseController, MouseConfig

# Configure behavior
config = MouseConfig(
    curve_intensity=0.5,    # More curved
    speed=1.5,              # 50% faster
    overshoot=True,         # Enable overshoot
    add_noise=True          # Add randomness
)

mouse = MouseController(config)
mouse.move_to(500, 300)
```

## 📊 Movement Comparison

### Before (Straight Lines)
```
Start ──────────────────────> End
      (Robotic, obvious)
```

### After (Smooth Curves)
```
Start ╭─────────╮
      │         │
      │         ╰────> End
      (Natural, human-like)
```

## 🎨 Curve Types

### Bezier (Default)
Best for general use. Creates smooth S-shaped curves.

```python
mouse.move_to(500, 300, curve_type='bezier')
```

### Arc
Good for sweeping motions. Follows circular arc.

```python
mouse.move_to(500, 300, curve_type='arc')
```

### Wave
Creates oscillating path. Good for special effects.

```python
mouse.move_to(500, 300, curve_type='wave')
```

## ⚡ Configuration Examples

### Very Natural (Recommended)
```python
config = MouseConfig(
    curve_intensity=0.4,
    speed=0.8,
    overshoot=True,
    overshoot_amount=0.08,
    add_noise=True,
    noise_amount=3.0
)
```

### Fast & Efficient
```python
config = MouseConfig(
    curve_intensity=0.2,
    speed=2.0,
    overshoot=False,
    add_noise=False
)
```

### Precise & Accurate
```python
config = MouseConfig(
    curve_intensity=0.1,
    speed=0.5,
    overshoot=False,
    add_noise=False,
    min_duration=0.5
)
```

### Exaggerated (Demo/Testing)
```python
config = MouseConfig(
    curve_intensity=1.0,
    speed=0.5,
    overshoot=True,
    overshoot_amount=0.15,
    add_noise=True,
    noise_amount=5.0
)
```

## 📖 Documentation

- **[Mouse Control Guide](docs/MOUSE_CONTROL_GUIDE.md)** - Complete usage guide
- **[System Architecture](docs/SYSTEM_ARCHITECTURE.md)** - Technical architecture
- **[Examples](examples/mouse_demo.py)** - Demo script with all features

## 🔧 Integration

### With Automation System

The mouse controller is automatically integrated:

```python
from automation_engine.input_controller import InputController

# Smooth mouse enabled by default
controller = InputController(use_smooth_mouse=True)

# All movements are now smooth
controller.move_mouse(500, 300)
controller.click(500, 300)
```

### With AI Commands

Works seamlessly with AI commands:

```
You: "Click the submit button at 500, 300"
AI: *Moves mouse smoothly in curved path and clicks*
```

### In Workflows

Automatically used in all workflows:

```python
workflow = {
    "steps": [
        {"type": "mouse_move", "coordinates": [500, 300]},
        {"type": "click", "coordinates": [500, 300]}
    ]
}
# Executes with smooth movements
```

## 🎯 Use Cases

### Web Automation
- Navigate websites naturally
- Click buttons and links
- Fill forms smoothly
- Scroll pages

### UI Testing
- Test applications with realistic input
- Simulate real user behavior
- Record and replay interactions

### Gaming
- Natural mouse movements
- Smooth camera control
- Realistic aiming

### Demonstrations
- Professional-looking demos
- Smooth screen recordings
- Training videos

## 🛠️ Technical Details

### Path Generation
- **Algorithm**: Cubic Bezier curves
- **Frame Rate**: 60 FPS
- **Points**: 18-90 per movement
- **Calculation**: ~5ms overhead

### Easing Function
- **Type**: Cubic ease-in-out
- **Effect**: Natural acceleration/deceleration
- **Formula**: `f(t) = t < 0.5 ? 4t³ : 1 - (-2t + 2)³ / 2`

### Performance
- **CPU Usage**: 1-3% during movement
- **Memory**: ~10KB per path
- **Latency**: Negligible (<5ms)

## 🔒 Safety

### Boundary Protection
All coordinates automatically clamped to screen:
```python
mouse.move_to(99999, 99999)  # Safe!
# Moves to (screen_width - 5, screen_height - 5)
```

### Emergency Stop
Move mouse to upper-left corner to stop immediately.

### Validation
All inputs validated before execution:
- Coordinate ranges
- Duration limits
- Parameter types

## 📦 Dependencies

```
numpy>=1.20.0      # Mathematical operations
pyautogui>=0.9.50  # Low-level mouse control
```

Install with:
```bash
pip install numpy pyautogui
```

## 🎓 Examples

### Example 1: Simple Click
```python
mouse = MouseController()
mouse.click(500, 300)
```

### Example 2: Form Filling
```python
mouse = MouseController()

# Click first field
mouse.click(300, 200)
time.sleep(0.2)

# Click second field  
mouse.click(300, 250)
time.sleep(0.2)

# Click submit
mouse.click(400, 350)
```

### Example 3: Drag and Drop
```python
mouse = MouseController()

# Move to item
mouse.move_to(200, 200)
time.sleep(0.2)

# Drag to target
mouse.drag_to(600, 400)
```

### Example 4: Menu Navigation
```python
config = MouseConfig(curve_intensity=0.4)
mouse = MouseController(config)

menu_items = [(100, 50), (200, 50), (300, 50)]

for x, y in menu_items:
    mouse.move_to(x, y)
    time.sleep(0.3)
```

## 🐛 Troubleshooting

### Movement Too Slow
```python
config = MouseConfig(speed=2.0)  # 2x faster
```

### Movement Too Fast
```python
config = MouseConfig(speed=0.5)  # 2x slower
```

### Too Curved
```python
config = MouseConfig(curve_intensity=0.1)  # Less curve
```

### Not Curved Enough
```python
config = MouseConfig(curve_intensity=0.7)  # More curve
```

### Jittery Movement
```python
config = MouseConfig(add_noise=False)  # Disable noise
```

### Missing Target
```python
config = MouseConfig(overshoot=False)  # Disable overshoot
```

## 📝 Configuration Reference

```python
MouseConfig(
    # Movement
    curve_intensity=0.3,      # 0.0-1.0, curve amount
    speed=1.0,                # Speed multiplier
    overshoot=True,           # Overshoot target
    overshoot_amount=0.05,    # Overshoot distance
    
    # Randomization
    add_noise=True,           # Random variations
    noise_amount=2.0,         # Noise magnitude (pixels)
    
    # Timing
    min_duration=0.3,         # Min time (seconds)
    max_duration=1.5,         # Max time (seconds)
    
    # Clicks
    click_delay_min=0.05,     # Min click delay
    click_delay_max=0.15,     # Max click delay
    
    # Safety
    boundary_margin=5         # Edge margin (pixels)
)
```

## 🎬 Demo Video

Run the demo to see it in action:
```bash
python examples/mouse_demo.py
```

The demo shows:
- ✓ Basic movements
- ✓ Different curve types
- ✓ Speed variations
- ✓ Curve intensity levels
- ✓ Overshoot behavior
- ✓ Click operations
- ✓ Drag operations
- ✓ Human-like behavior

## 🤝 Contributing

Want to improve the mouse control system?

1. Test new curve algorithms
2. Optimize performance
3. Add new features
4. Improve documentation
5. Report bugs

## 📄 License

Part of the AI Automation Assistant project.

## 🙏 Credits

- **Bezier Curves**: Based on De Casteljau's algorithm
- **Easing Functions**: Robert Penner's easing equations
- **PyAutoGUI**: Al Sweigart
- **NumPy**: NumPy Developers

## 🔗 Related

- [Main README](README.md)
- [Quick Start Guide](QUICK_START.md)
- [System Architecture](docs/SYSTEM_ARCHITECTURE.md)
- [Developer Mode](dev.bat)

---

**Made with ❤️ for natural, human-like automation**
