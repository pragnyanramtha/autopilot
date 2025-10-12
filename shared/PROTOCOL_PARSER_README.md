# JSON Protocol Parser and Validator

## Overview

The `JSONProtocolParser` class provides comprehensive validation for the JSON Instruction Protocol. It validates schema structure, action parameters, macro definitions, circular dependencies, variable substitution, timing consistency, and coordinate bounds.

## Features

### 1. Schema Validation
- Validates JSON structure against protocol schema
- Checks for required fields (version, metadata, actions)
- Validates metadata fields (description, complexity, uses_vision)

### 2. Action Validation
- Validates action names against `VALID_ACTIONS` set (80+ actions)
- Checks required parameters for each action type
- Validates parameter types (lists, integers, strings, etc.)
- Detects unknown parameters (warnings)

### 3. Macro Validation
- Checks macro existence before usage
- Validates macro definitions
- Detects circular dependencies (simple and complex)
- Validates variable substitution syntax (`{{var}}`)
- Checks for missing and unused variables

### 4. Timing Validation
- Calculates total wait time from actions
- Compares against estimated duration
- Warns if timing differs significantly (>20% variance)

### 5. Coordinate Validation
- Validates screen coordinates are within bounds
- Checks x, y coordinates for mouse actions
- Validates region bounds for capture actions
- Configurable screen dimensions

## Usage

### Basic Usage

```python
from shared.protocol_parser import JSONProtocolParser, validate_protocol_json

# Simple validation
result = validate_protocol_json(json_string)

if result.is_valid:
    print("✓ Protocol is valid!")
else:
    for error in result.errors:
        print(f"ERROR: {error}")

for warning in result.warnings:
    print(f"WARNING: {warning}")
```

### Advanced Usage

```python
from shared.protocol_parser import JSONProtocolParser

# Create parser with custom screen dimensions
parser = JSONProtocolParser(screen_width=2560, screen_height=1440)

# Parse JSON
protocol = parser.parse(json_string)

# Validate
result = parser.validate_protocol(protocol)
```

### Parse from Dictionary

```python
protocol_dict = {
    "version": "1.0",
    "metadata": {"description": "Test"},
    "actions": [...]
}

protocol = parser.parse_dict(protocol_dict)
result = parser.validate_protocol(protocol)
```

## Validation Result

The `ValidationResult` object contains:

```python
@dataclass
class ValidationResult:
    is_valid: bool          # True if no errors
    errors: List[str]       # List of error messages
    warnings: List[str]     # List of warning messages
```

## Supported Actions

The parser validates 80+ actions across categories:

- **Keyboard**: press_key, shortcut, type, type_with_delay, hold_key, release_key
- **Mouse**: mouse_move, mouse_click, mouse_drag, mouse_scroll, etc.
- **Window**: open_app, close_app, switch_window, minimize_window, etc.
- **Browser**: open_url, browser_back, browser_new_tab, browser_address_bar, etc.
- **Clipboard**: copy, paste, cut, get_clipboard, set_clipboard
- **File System**: open_file, save_file, create_folder, delete_file
- **Screen Capture**: capture_screen, capture_region, capture_window
- **Timing**: delay, wait_for_window, wait_for_image, wait_for_color
- **Visual Verification**: verify_screen, verify_element, find_element, verify_text
- **System**: lock_screen, volume_up, volume_down, shutdown_system
- **Text Editing**: select_all, undo, redo, find_replace
- **Macros**: macro (execute predefined macro)

## Action Parameter Specifications

Each action has defined required and optional parameters:

```python
ACTION_PARAMS = {
    "press_key": {"required": ["key"], "optional": []},
    "shortcut": {"required": ["keys"], "optional": []},
    "type": {"required": ["text"], "optional": ["interval_ms"]},
    "mouse_move": {"required": ["x", "y"], "optional": ["smooth", "speed"]},
    "open_app": {"required": ["app_name"], "optional": []},
    "macro": {"required": ["name"], "optional": ["vars"]},
    # ... 80+ actions total
}
```

## Validation Examples

### Valid Protocol

```json
{
  "version": "1.0",
  "metadata": {
    "description": "Search workflow",
    "complexity": "simple"
  },
  "macros": {
    "search": [
      {"action": "shortcut", "params": {"keys": ["ctrl", "l"]}, "wait_after_ms": 200},
      {"action": "type", "params": {"text": "{{query}}"}, "wait_after_ms": 100}
    ]
  },
  "actions": [
    {"action": "open_app", "params": {"app_name": "chrome"}, "wait_after_ms": 2000},
    {"action": "macro", "params": {"name": "search", "vars": {"query": "test"}}}
  ]
}
```

### Invalid Action Name

```json
{
  "actions": [
    {"action": "invalid_action", "params": {}}
  ]
}
```

**Error**: `Invalid action 'invalid_action'. Must be one of the registered actions.`

### Missing Required Parameter

```json
{
  "actions": [
    {"action": "open_app", "params": {}}
  ]
}
```

**Error**: `Action 0: Missing required parameter 'app_name' for action 'open_app'`

### Circular Dependency

```json
{
  "macros": {
    "macro_a": [
      {"action": "macro", "params": {"name": "macro_b"}}
    ],
    "macro_b": [
      {"action": "macro", "params": {"name": "macro_a"}}
    ]
  }
}
```

**Error**: `Circular dependency detected: macro_a -> macro_b`

### Missing Variable

```json
{
  "macros": {
    "search": [
      {"action": "type", "params": {"text": "{{query}}"}}
    ]
  },
  "actions": [
    {"action": "macro", "params": {"name": "search", "vars": {}}}
  ]
}
```

**Warning**: `Macro 'search': Missing variables {'query'}`

### Coordinate Out of Bounds

```json
{
  "actions": [
    {"action": "mouse_move", "params": {"x": 5000, "y": 5000}}
  ]
}
```

**Warning**: `Action 0: x coordinate 5000 is outside screen bounds (0-1920)`

### Timing Inconsistency

```json
{
  "metadata": {
    "estimated_duration_seconds": 10
  },
  "actions": [
    {"action": "delay", "params": {"ms": 1000}}
  ]
}
```

**Warning**: `Timing inconsistency: Total wait time (1000ms) differs significantly from estimated duration (10000ms)`

## Testing

Run the test suite:

```bash
python tests/test_protocol_parser.py
```

Tests cover:
- Valid protocol parsing
- Invalid action detection
- Missing required parameters
- Macro existence checking
- Simple circular dependencies
- Complex circular dependencies (A -> B -> C -> A)
- Variable substitution validation
- Coordinate bounds validation
- Timing consistency validation
- Parameter type validation

## Integration

The parser integrates with:

1. **Protocol Models** (`shared/protocol_models.py`): Uses `ProtocolSchema`, `ActionStep`, `MacroDefinition`
2. **AI Brain**: Will validate AI-generated protocols before execution
3. **Automation Engine**: Will validate protocols before execution
4. **Communication Layer**: Will validate protocols during transmission

## Error Handling

The parser uses two levels of feedback:

1. **Errors**: Critical issues that prevent execution
   - Invalid JSON syntax
   - Missing required fields
   - Invalid action names
   - Missing required parameters
   - Circular dependencies
   - Undefined macros

2. **Warnings**: Non-critical issues that may indicate problems
   - Timing inconsistencies
   - Coordinates out of bounds
   - Unknown parameters
   - Missing/unused variables
   - Parameter type mismatches

## Performance

- Fast validation: < 10ms for typical protocols
- Efficient circular dependency detection using DFS
- Minimal memory overhead
- Suitable for real-time validation

## Future Enhancements

Potential improvements:
- JSON Schema validation using jsonschema library
- More detailed parameter type checking
- Custom validation rules per action
- Validation caching for repeated protocols
- Performance profiling and optimization
