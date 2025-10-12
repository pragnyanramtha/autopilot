# Smooth Mouse Movement Configuration

**Task 6: Configure Smooth Mouse Movements**

This document describes the smooth mouse movement configuration implemented for the JSON Instruction Protocol.

## Overview

All mouse movements in the system now use smooth, curved paths by default, providing natural, human-like motion. This eliminates robotic straight-line movements and makes automation less detectable.

## Configuration Details

### 1. Default Curve Type: Bezier

The `move_to()` method defaults to using **Bezier curves**, which provide the most natural-looking mouse movements:

```python
def move_to(self, x: int, y: int, duration: Optional[float] = None, 
            curve_type: Literal['bezier', 'arc', 'wave'] = 'bezier'):
    # Uses bezier by default
```

**Available curve types:**
- `bezier` (default): Smooth cubic Bezier curves with control points
- `arc`: Circular arc paths
- `wave`: Wave-like motion perpendicular to movement direction

### 2. MouseConfig Default Values

The `MouseConfig` dataclass defines all default parameters for smooth movements:

```python
@dataclass
class MouseConfig:
    # Movement settings
    curve_intensity: float = 0.3      # 0.0 = straight, 1.0 = very curved
    speed: float = 1.0                # Movement speed multiplier
    overshoot: bool = True            # Slightly overshoot then correct
    overshoot_amount: float = 0.05    # 5% of distance
    
    # Randomization for human-like behavior
    add_noise: bool = True            # Add small random variations
    noise_amount: float = 2.0         # Pixels of random noise
    
    # Timing
    min_duration: float = 0.3         # Minimum time (seconds)
    max_duration: float = 1.5         # Maximum time (seconds)
    
    # Click settings
    click_delay_min: float = 0.05     # Min delay before click
    click_delay_max: float = 0.15     # Max delay before click
    
    # Safety
    boundary_margin: int = 5          # Pixels from screen edge
```

### 3. Action Handler Configuration

The `mouse_move` action handler is configured to use smooth movements by default:

```python
def mouse_move(x: int, y: int, smooth: bool = True, speed: float = 1.0, 
               curve_type: str = "bezier", duration: float = None):
    """Move mouse to coordinates (smooth curved path by default)."""
    if self.registry.mouse_controller and smooth:
        self.registry.mouse_controller.move_to(x, y, duration=duration, 
                                               curve_type=curve_type)
```

**Default parameters:**
- `smooth`: `True` (enables curved paths)
- `curve_type`: `"bezier"` (uses Bezier curves)
- `speed`: `1.0` (normal speed)
- `duration`: `None` (auto-calculated based on distance)

## Usage in JSON Protocol

### Basic Usage (Uses All Defaults)

```json
{
  "action": "mouse_move",
  "params": {
    "x": 500,
    "y": 300
  }
}
```

This will:
- Use smooth Bezier curve path
- Auto-calculate duration based on distance
- Apply overshoot and noise for natural motion
- Use normal speed (1.0x)

### Custom Curve Type

```json
{
  "action": "mouse_move",
  "params": {
    "x": 500,
    "y": 300,
    "curve_type": "arc"
  }
}
```

### Disable Smooth Movement (Straight Line)

```json
{
  "action": "mouse_move",
  "params": {
    "x": 500,
    "y": 300,
    "smooth": false
  }
}
```

### Custom Speed

```json
{
  "action": "mouse_move",
  "params": {
    "x": 500,
    "y": 300,
    "speed": 2.0
  }
}
```

## Human-Like Features

### 1. Curved Paths

Instead of moving in a straight line, the mouse follows a smooth curve:

```
Start (100, 100)
    \
     \___
         \___
             \___  Control points create curve
                 \___
                     \
                      End (500, 300)
```

### 2. Overshoot and Correction

The mouse slightly overshoots the target, then corrects back (natural human behavior):

```
                    Overshoot
                        ↓
Start → → → → → → → Target → ← Correction
```

### 3. Micro-Adjustments (Noise)

Small random variations (±2 pixels) are added along the path to simulate natural hand tremor:

```
Intended path:  ————————————————
Actual path:    ～～～～～～～～～～
```

### 4. Easing Function

Movement uses cubic easing (acceleration/deceleration):

```
Speed
  ↑
  |     ___---~~~
  |  __/
  | /
  |/
  +————————————————→ Time
  Start         End
```

## Benefits

1. **Natural Appearance**: Movements look human-like, not robotic
2. **Less Detectable**: Harder to distinguish from real user input
3. **Configurable**: Can adjust curve intensity, speed, and behavior
4. **Consistent**: All mouse movements use the same smooth system
5. **Safe**: Respects screen boundaries with margin

## Requirements Satisfied

- ✅ **12.1**: Mouse movements use smooth curved paths by default
- ✅ **12.2**: Bezier curves are the default curve type  
- ✅ **12.6**: Proper default configuration for curve_intensity, speed, overshoot, and noise

## Testing

Run the test suite to verify configuration:

```bash
python tests/test_mouse_smooth_config.py
```

This verifies:
- MouseConfig default values
- MouseController initialization
- move_to() default curve type
- Action handler smooth defaults
- Complete configuration summary

## Implementation Files

- `automation_engine/mouse_controller.py`: MouseController and MouseConfig
- `shared/action_handlers.py`: mouse_move action handler
- `tests/test_mouse_smooth_config.py`: Configuration tests
- `docs/SMOOTH_MOUSE_CONFIGURATION.md`: This documentation

## Future Enhancements

Possible future improvements:
- Adaptive curve intensity based on distance
- Learning from user's actual mouse patterns
- Different profiles (fast, slow, cautious, etc.)
- Screen region-specific behavior
- Integration with visual verification for adaptive targeting
