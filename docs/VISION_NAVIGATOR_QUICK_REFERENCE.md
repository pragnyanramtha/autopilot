# VisionNavigator Quick Reference

## Overview

The `VisionNavigator` class enables AI-driven visual navigation by analyzing screenshots and determining optimal mouse actions.

## Quick Start

```python
from ai_brain.gemini_client import GeminiClient
from ai_brain.vision_navigator import VisionNavigator

# Initialize
client = GeminiClient()
config = {'visual_navigation': {'vision_model': 'gemini-2.0-flash-exp'}}
navigator = VisionNavigator(client, config)

# Analyze screen
result = navigator.analyze_screen_for_action(
    screenshot=screenshot,
    current_mouse_pos=(100, 200),
    task_description="Click submit button",
    screen_size=(1920, 1080)
)
```

## Key Methods

### analyze_screen_for_action()
Analyzes screenshot and determines next action.

**Returns**: `VisionNavigationResult` with:
- `action`: 'click', 'double_click', 'right_click', 'type', 'no_action', 'complete'
- `coordinates`: (x, y) tuple or None
- `confidence`: 0.0 to 1.0
- `reasoning`: AI's explanation
- `requires_followup`: bool

### verify_action_result()
Compares before/after screenshots to verify success.

**Returns**: `bool` (True if action succeeded)

### should_continue()
Determines if workflow should continue.

**Returns**: `(should_continue: bool, next_task: str)`

## Configuration

```json
{
  "visual_navigation": {
    "vision_model": "gemini-2.0-flash-exp",
    "vision_model_dev": "gemini-2.0-flash-exp",
    "max_iterations": 10,
    "confidence_threshold": 0.6,
    "enable_audit_log": true,
    "audit_log_path": "logs/visual_navigation_audit.json",
    "critical_keywords": ["delete", "format", "shutdown"]
  }
}
```

## Action Types

- **click**: Single left click
- **double_click**: Double left click
- **right_click**: Right click
- **type**: Type text (requires `text_to_type`)
- **no_action**: Cannot determine action
- **complete**: Task is complete

## Safety Features

✅ Coordinate validation (clamps to screen bounds)
✅ Critical action detection (keywords)
✅ Confidence thresholds
✅ Audit logging
✅ Error handling with safe defaults

## Helper Methods

- `is_critical_action(reasoning)`: Check for critical keywords
- `save_audit_entry(entry)`: Save to audit log
- `_validate_coordinates(result, screen_size)`: Validate/clamp coords
- `_parse_json_response(text)`: Parse JSON from response

## Testing

Run verification: `python tests/verify_vision_navigator.py`

## Integration Status

✅ Task 2.1: Class initialization
✅ Task 2.2: Screen analysis method
✅ Task 2.3: Action verification method
✅ Task 2.4: Workflow continuation logic
✅ Task 2.5: Error handling and validation

## Next Tasks

- [ ] Task 3: MessageBroker integration
- [ ] Task 4: VisualNavigationHandler
- [ ] Task 5: AI Brain integration
- [ ] Task 6: Automation Engine integration
