# Protocol System Configuration Guide

This guide explains how to configure the JSON Instruction Protocol system using `config.json`.

## Overview

The protocol system configuration is located in `config.json` under the `"protocol"` section. It controls:

- **Validation**: How strictly protocols are validated
- **Visual Verification**: AI vision model settings and thresholds
- **Mouse Movement**: Default behavior for mouse movements
- **Action Library**: Which actions are enabled/disabled

## Configuration Structure

```json
{
  "protocol": {
    "validation": { ... },
    "visual_verification": { ... },
    "mouse_movement": { ... },
    "action_library": { ... }
  }
}
```

## Validation Configuration

Controls how protocols are validated before execution.

```json
"validation": {
  "strict_mode": false,
  "warning_level": "all"
}
```

### Settings

- **`strict_mode`** (boolean, default: `false`)
  - `true`: Treat warnings as errors, fail validation on any issue
  - `false`: Allow warnings, only fail on critical errors
  
- **`warning_level`** (string, default: `"all"`)
  - `"none"`: Don't show any warnings
  - `"errors_only"`: Only show critical errors
  - `"all"`: Show all warnings and errors

### Examples

**Strict validation for production:**
```json
"validation": {
  "strict_mode": true,
  "warning_level": "all"
}
```

**Relaxed validation for development:**
```json
"validation": {
  "strict_mode": false,
  "warning_level": "errors_only"
}
```

## Visual Verification Configuration

Controls AI vision-based verification behavior.

```json
"visual_verification": {
  "enabled": true,
  "timeout_seconds": 10,
  "confidence_threshold": 0.7,
  "primary_model": "gemini-2.0-flash-exp",
  "fallback_model": "gemini-1.5-flash"
}
```

### Settings

- **`enabled`** (boolean, default: `true`)
  - Enable/disable visual verification system
  
- **`timeout_seconds`** (integer, default: `10`)
  - Maximum time to wait for AI vision response
  - Recommended: 5-15 seconds
  
- **`confidence_threshold`** (float, default: `0.7`)
  - Minimum confidence level (0.0-1.0) to proceed
  - Higher = more strict, lower = more permissive
  - `0.9`: Very strict, only proceed if highly confident
  - `0.7`: Balanced (recommended)
  - `0.5`: Permissive, proceed with moderate confidence
  
- **`primary_model`** (string, default: `"gemini-2.0-flash-exp"`)
  - Primary AI vision model for verification
  - Options: `"gemini-2.0-flash-exp"`, `"gemini-2.5-flash"`, `"gemini-2.5-pro"`
  
- **`fallback_model`** (string, default: `"gemini-1.5-flash"`)
  - Backup model if primary fails
  - Automatically used if primary times out or errors

### Examples

**High confidence, fast timeout:**
```json
"visual_verification": {
  "enabled": true,
  "timeout_seconds": 5,
  "confidence_threshold": 0.9,
  "primary_model": "gemini-2.0-flash-exp",
  "fallback_model": "gemini-1.5-flash"
}
```

**Balanced settings (recommended):**
```json
"visual_verification": {
  "enabled": true,
  "timeout_seconds": 10,
  "confidence_threshold": 0.7,
  "primary_model": "gemini-2.0-flash-exp",
  "fallback_model": "gemini-1.5-flash"
}
```

**Disabled for testing:**
```json
"visual_verification": {
  "enabled": false,
  "timeout_seconds": 10,
  "confidence_threshold": 0.7,
  "primary_model": "gemini-2.0-flash-exp",
  "fallback_model": "gemini-1.5-flash"
}
```

## Mouse Movement Configuration

Controls default mouse movement behavior.

```json
"mouse_movement": {
  "smooth": true,
  "curve_type": "bezier",
  "curve_intensity": 0.3,
  "speed": 1.0,
  "overshoot": true,
  "overshoot_amount": 0.05,
  "add_noise": true,
  "noise_amount": 2.0,
  "min_duration": 0.3,
  "max_duration": 1.5
}
```

### Settings

- **`smooth`** (boolean, default: `true`)
  - `true`: Use smooth curved movements (human-like)
  - `false`: Use direct linear movements (faster but robotic)
  
- **`curve_type`** (string, default: `"bezier"`)
  - `"bezier"`: Smooth Bezier curves (recommended)
  - `"linear"`: Straight line movements
  
- **`curve_intensity`** (float, default: `0.3`)
  - How curved the path is (0.0-1.0)
  - `0.0`: Straight line
  - `0.3`: Gentle curve (recommended)
  - `1.0`: Very curved path
  
- **`speed`** (float, default: `1.0`)
  - Movement speed multiplier
  - `0.5`: Half speed (slower)
  - `1.0`: Normal speed
  - `2.0`: Double speed (faster)
  
- **`overshoot`** (boolean, default: `true`)
  - Slightly overshoot target then correct (human-like)
  
- **`overshoot_amount`** (float, default: `0.05`)
  - Percentage of distance to overshoot (0.0-1.0)
  - `0.05`: 5% overshoot (recommended)
  
- **`add_noise`** (boolean, default: `true`)
  - Add small random variations (human-like)
  
- **`noise_amount`** (float, default: `2.0`)
  - Pixels of random noise to add
  - `0.0`: No noise
  - `2.0`: Small variations (recommended)
  - `5.0`: Larger variations
  
- **`min_duration`** (float, default: `0.3`)
  - Minimum time for movement (seconds)
  
- **`max_duration`** (float, default: `1.5`)
  - Maximum time for movement (seconds)

### Examples

**Human-like movements (recommended):**
```json
"mouse_movement": {
  "smooth": true,
  "curve_type": "bezier",
  "curve_intensity": 0.3,
  "speed": 1.0,
  "overshoot": true,
  "overshoot_amount": 0.05,
  "add_noise": true,
  "noise_amount": 2.0,
  "min_duration": 0.3,
  "max_duration": 1.5
}
```

**Fast, direct movements:**
```json
"mouse_movement": {
  "smooth": false,
  "curve_type": "linear",
  "curve_intensity": 0.0,
  "speed": 2.0,
  "overshoot": false,
  "overshoot_amount": 0.0,
  "add_noise": false,
  "noise_amount": 0.0,
  "min_duration": 0.1,
  "max_duration": 0.5
}
```

**Very smooth, slow movements:**
```json
"mouse_movement": {
  "smooth": true,
  "curve_type": "bezier",
  "curve_intensity": 0.5,
  "speed": 0.5,
  "overshoot": true,
  "overshoot_amount": 0.1,
  "add_noise": true,
  "noise_amount": 3.0,
  "min_duration": 0.5,
  "max_duration": 2.0
}
```

## Action Library Configuration

Controls which actions are available for use.

```json
"action_library": {
  "enabled_categories": [
    "keyboard",
    "mouse",
    "window",
    "browser",
    "clipboard",
    "file",
    "screen",
    "timing",
    "vision",
    "system",
    "edit",
    "macro"
  ],
  "disabled_actions": []
}
```

### Settings

- **`enabled_categories`** (array of strings)
  - List of action categories to enable
  - Available categories:
    - `"keyboard"`: Keyboard input actions
    - `"mouse"`: Mouse movement and clicks
    - `"window"`: Window management
    - `"browser"`: Browser-specific actions
    - `"clipboard"`: Clipboard operations
    - `"file"`: File system operations
    - `"screen"`: Screen capture
    - `"timing"`: Delays and waits
    - `"vision"`: Visual verification
    - `"system"`: System control (shutdown, volume, etc.)
    - `"edit"`: Text editing shortcuts
    - `"macro"`: Macro execution
  
- **`disabled_actions`** (array of strings)
  - List of specific action names to disable
  - Takes precedence over enabled_categories
  - Example: `["shutdown_system", "delete_file"]`

### Examples

**All actions enabled (default):**
```json
"action_library": {
  "enabled_categories": [
    "keyboard", "mouse", "window", "browser", "clipboard",
    "file", "screen", "timing", "vision", "system", "edit", "macro"
  ],
  "disabled_actions": []
}
```

**Disable dangerous system actions:**
```json
"action_library": {
  "enabled_categories": [
    "keyboard", "mouse", "window", "browser", "clipboard",
    "file", "screen", "timing", "vision", "system", "edit", "macro"
  ],
  "disabled_actions": [
    "shutdown_system",
    "restart_system",
    "delete_file",
    "sleep_system"
  ]
}
```

**Only keyboard and mouse (minimal):**
```json
"action_library": {
  "enabled_categories": [
    "keyboard",
    "mouse",
    "timing"
  ],
  "disabled_actions": []
}
```

**Disable entire system category:**
```json
"action_library": {
  "enabled_categories": [
    "keyboard", "mouse", "window", "browser", "clipboard",
    "file", "screen", "timing", "vision", "edit", "macro"
  ],
  "disabled_actions": []
}
```

## Using Configuration in Code

### Python

```python
from shared.config_loader import get_config

# Load configuration
config = get_config()

# Access settings
timeout = config.visual_verification.timeout_seconds
confidence = config.visual_verification.confidence_threshold
smooth = config.mouse_movement.smooth
strict = config.validation.strict_mode

# Check if action is enabled
is_enabled = config.action_library.is_action_enabled("press_key", "keyboard")
```

### Example: Configure Visual Verifier

```python
from shared.config_loader import get_config
from shared.visual_verifier import VisualVerifier

config = get_config()

verifier = VisualVerifier(
    screen_capture=screen_capture,
    primary_model=config.visual_verification.primary_model,
    fallback_model=config.visual_verification.fallback_model,
    timeout_seconds=config.visual_verification.timeout_seconds
)

result = verifier.verify(
    context="Looking for login button",
    expected="Login button visible",
    confidence_threshold=config.visual_verification.confidence_threshold
)
```

### Example: Configure Mouse Controller

```python
from shared.config_loader import get_config
from automation_engine.mouse_controller import MouseController, MouseConfig

config = get_config()
mouse_cfg = config.mouse_movement

mouse_config = MouseConfig(
    curve_intensity=mouse_cfg.curve_intensity,
    speed=mouse_cfg.speed,
    overshoot=mouse_cfg.overshoot,
    overshoot_amount=mouse_cfg.overshoot_amount,
    add_noise=mouse_cfg.add_noise,
    noise_amount=mouse_cfg.noise_amount,
    min_duration=mouse_cfg.min_duration,
    max_duration=mouse_cfg.max_duration
)

mouse = MouseController(config=mouse_config)
mouse.move_to(500, 300, smooth=mouse_cfg.smooth)
```

## Reloading Configuration

Configuration is loaded once at startup (singleton pattern). To reload:

```python
from shared.config_loader import ConfigLoader

# Force reload from file
config = ConfigLoader.reload()
```

## Best Practices

1. **Development**: Use relaxed validation and lower confidence thresholds
2. **Production**: Use strict validation and higher confidence thresholds
3. **Testing**: Disable visual verification for faster tests
4. **Security**: Disable dangerous actions like `shutdown_system` in production
5. **Performance**: Adjust mouse speed and duration based on use case

## Troubleshooting

### Configuration not loading

- Check that `config.json` exists in the project root
- Verify JSON syntax is valid
- Check console for error messages

### Visual verification always fails

- Lower `confidence_threshold` (try 0.5)
- Increase `timeout_seconds` (try 15)
- Check API key is set in `.env`

### Mouse movements too slow/fast

- Adjust `speed` multiplier
- Adjust `min_duration` and `max_duration`
- Set `smooth: false` for instant movements

### Actions not working

- Check action is not in `disabled_actions`
- Check category is in `enabled_categories`
- Use `is_action_enabled()` to verify

## Related Documentation

- [Protocol Models](../shared/PROTOCOL_MODELS_README.md)
- [Protocol Parser](../shared/PROTOCOL_PARSER_README.md)
- [Visual Verification](../shared/VISUAL_VERIFICATION_README.md)
- [Mouse Control](MOUSE_CONTROL_GUIDE.md)
