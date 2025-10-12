# Protocol Configuration Quick Reference

Quick reference for configuring the JSON Instruction Protocol system.

## Quick Access in Code

```python
from shared.config_loader import get_config

config = get_config()

# Validation
strict = config.validation.strict_mode
warnings = config.validation.warning_level

# Visual Verification
timeout = config.visual_verification.timeout_seconds
confidence = config.visual_verification.confidence_threshold
primary = config.visual_verification.primary_model

# Mouse Movement
smooth = config.mouse_movement.smooth
curve = config.mouse_movement.curve_intensity
speed = config.mouse_movement.speed

# Action Library
is_enabled = config.action_library.is_action_enabled("press_key", "keyboard")
```

## Common Configuration Scenarios

### Development Mode (Fast, Permissive)

```json
{
  "protocol": {
    "validation": {
      "strict_mode": false,
      "warning_level": "errors_only"
    },
    "visual_verification": {
      "enabled": false,
      "timeout_seconds": 5,
      "confidence_threshold": 0.5
    },
    "mouse_movement": {
      "smooth": false,
      "speed": 2.0,
      "min_duration": 0.1,
      "max_duration": 0.5
    }
  }
}
```

### Production Mode (Strict, Reliable)

```json
{
  "protocol": {
    "validation": {
      "strict_mode": true,
      "warning_level": "all"
    },
    "visual_verification": {
      "enabled": true,
      "timeout_seconds": 15,
      "confidence_threshold": 0.9
    },
    "mouse_movement": {
      "smooth": true,
      "speed": 1.0,
      "overshoot": true,
      "add_noise": true
    }
  }
}
```

### Testing Mode (Minimal, Fast)

```json
{
  "protocol": {
    "validation": {
      "strict_mode": false,
      "warning_level": "none"
    },
    "visual_verification": {
      "enabled": false
    },
    "mouse_movement": {
      "smooth": false,
      "speed": 3.0
    },
    "action_library": {
      "disabled_actions": ["shutdown_system", "restart_system", "delete_file"]
    }
  }
}
```

## Configuration Defaults

| Setting | Default | Range/Options |
|---------|---------|---------------|
| **Validation** | | |
| strict_mode | `false` | `true`/`false` |
| warning_level | `"all"` | `"none"`, `"errors_only"`, `"all"` |
| **Visual Verification** | | |
| enabled | `true` | `true`/`false` |
| timeout_seconds | `10` | 1-60 |
| confidence_threshold | `0.7` | 0.0-1.0 |
| primary_model | `"gemini-2.0-flash-exp"` | Any Gemini model |
| fallback_model | `"gemini-1.5-flash"` | Any Gemini model |
| **Mouse Movement** | | |
| smooth | `true` | `true`/`false` |
| curve_type | `"bezier"` | `"bezier"`, `"linear"` |
| curve_intensity | `0.3` | 0.0-1.0 |
| speed | `1.0` | 0.1-5.0 |
| overshoot | `true` | `true`/`false` |
| overshoot_amount | `0.05` | 0.0-1.0 |
| add_noise | `true` | `true`/`false` |
| noise_amount | `2.0` | 0.0-10.0 |
| min_duration | `0.3` | 0.1-2.0 |
| max_duration | `1.5` | 0.5-5.0 |

## Action Categories

| Category | Actions |
|----------|---------|
| `keyboard` | press_key, shortcut, type, type_with_delay, hold_key, release_key |
| `mouse` | mouse_move, mouse_click, mouse_double_click, mouse_right_click, mouse_drag, mouse_scroll, mouse_position |
| `window` | open_app, close_app, switch_window, minimize_window, maximize_window, restore_window, get_active_window |
| `browser` | open_url, browser_back, browser_forward, browser_refresh, browser_new_tab, browser_close_tab, browser_switch_tab, browser_address_bar, browser_bookmark, browser_find |
| `clipboard` | copy, paste, cut, get_clipboard, set_clipboard, paste_from_clipboard |
| `file` | open_file, save_file, save_as, open_file_dialog, create_folder, delete_file |
| `screen` | capture_screen, capture_region, capture_window, save_screenshot |
| `timing` | delay, wait_for_window, wait_for_image, wait_for_color |
| `vision` | verify_screen, verify_element, find_element, verify_text |
| `system` | lock_screen, sleep_system, shutdown_system, restart_system, volume_up, volume_down, volume_mute |
| `edit` | select_all, undo, redo, find_replace, delete_line, duplicate_line |
| `macro` | macro |

## Disabling Dangerous Actions

```json
{
  "protocol": {
    "action_library": {
      "disabled_actions": [
        "shutdown_system",
        "restart_system",
        "delete_file",
        "sleep_system"
      ]
    }
  }
}
```

## Reload Configuration

```python
from shared.config_loader import ConfigLoader

# Force reload from file
config = ConfigLoader.reload()
```

## Full Documentation

See [PROTOCOL_CONFIGURATION.md](PROTOCOL_CONFIGURATION.md) for complete documentation.
