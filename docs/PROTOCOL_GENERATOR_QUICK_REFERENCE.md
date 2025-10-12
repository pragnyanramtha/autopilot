# Protocol Generator Quick Reference

## Basic Usage

### Import

```python
from ai_brain.protocol_generator import ProtocolGenerator
from ai_brain.gemini_client import GeminiClient, CommandIntent
```

### Initialize

```python
# Create GeminiClient
gemini_client = GeminiClient(api_key="your-api-key")

# Create ProtocolGenerator
generator = ProtocolGenerator(
    gemini_client=gemini_client,
    config={'optional': 'config'}
)
```

### Generate Protocol

```python
# From CommandIntent
intent = CommandIntent(
    action='search_web',
    target='Python tutorials',
    parameters={},
    confidence=0.95
)

protocol = generator.create_protocol(intent, "search for Python tutorials")
```

### Validate Protocol

```python
result = generator.validate_protocol(protocol)

if result['valid']:
    print("Protocol is valid!")
else:
    print("Issues:", result['issues'])
```

## Protocol Structure

```json
{
  "version": "1.0",
  "metadata": {
    "id": "unique-id",
    "description": "Search for Python tutorials"
  },
  "macros": {
    "search_in_browser": [
      {"action": "shortcut", "params": {"keys": ["ctrl", "l"]}, "wait_after_ms": 200},
      {"action": "type", "params": {"text": "{{query}}"}, "wait_after_ms": 100},
      {"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 5000}
    ]
  },
  "actions": [
    {"action": "open_app", "params": {"app_name": "chrome"}, "wait_after_ms": 2000},
    {"action": "macro", "params": {"name": "search_in_browser", "vars": {"query": "Python tutorials"}}}
  ]
}
```

## Common Patterns

### Simple Action

```python
protocol = {
    "version": "1.0",
    "actions": [
        {"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 100}
    ]
}
```

### With Macros

```python
protocol = {
    "version": "1.0",
    "macros": {
        "new_tab": [
            {"action": "shortcut", "params": {"keys": ["ctrl", "t"]}, "wait_after_ms": 1000}
        ]
    },
    "actions": [
        {"action": "macro", "params": {"name": "new_tab"}}
    ]
}
```

### With Visual Verification

```python
protocol = {
    "version": "1.0",
    "actions": [
        {
            "action": "verify_screen",
            "params": {
                "context": "Looking for submit button",
                "expected": "Submit button visible"
            },
            "wait_after_ms": 500
        },
        {
            "action": "mouse_move",
            "params": {"x": "{{verified_x}}", "y": "{{verified_y}}"},
            "wait_after_ms": 200
        }
    ]
}
```

## Sending Protocols

### Using MessageBroker

```python
from shared.communication import MessageBroker

broker = MessageBroker()
broker.send_protocol(protocol)
```

### Direct Execution

```python
from shared.protocol_executor import ProtocolExecutor

executor = ProtocolExecutor()
result = executor.execute(protocol)
```

## Error Handling

```python
try:
    protocol = generator.create_protocol(intent, user_input)
    
    validation = generator.validate_protocol(protocol)
    if not validation['valid']:
        print("Validation failed:")
        for issue in validation['issues']:
            print(f"  - {issue}")
        return
    
    # Send protocol
    broker.send_protocol(protocol)
    
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Comparison: Workflow vs Protocol

### Old Way (Workflow)

```python
from ai_brain.workflow_generator import WorkflowGenerator

generator = WorkflowGenerator(gemini_client, config)
workflow = generator.create_workflow(intent)
broker.send_workflow(workflow)
```

### New Way (Protocol)

```python
from ai_brain.protocol_generator import ProtocolGenerator

generator = ProtocolGenerator(gemini_client, config)
protocol = generator.create_protocol(intent, user_input)
broker.send_protocol(protocol)
```

## Available Actions

The protocol supports 80+ actions including:

### Keyboard
- `press_key` - Single key press
- `shortcut` - Multiple keys simultaneously
- `type` - Type text of any length

### Mouse
- `mouse_move` - Move to coordinates
- `mouse_click` - Click at position
- `mouse_drag` - Drag to position

### Browser
- `open_url` - Open URL
- `browser_back` - Navigate back
- `browser_new_tab` - Open new tab

### Visual
- `verify_screen` - AI vision verification
- `verify_element` - Check element exists
- `find_element` - Locate element

### System
- `open_app` - Open application
- `delay` - Wait milliseconds
- `macro` - Execute macro

See `docs/PROTOCOL_GENERATION_IMPLEMENTATION.md` for complete action library.

## Tips

1. **Always validate** protocols before sending
2. **Use macros** for repeated action sequences
3. **Add metadata** for debugging and tracking
4. **Use visual verification** when uncertain about UI state
5. **Keep actions simple** - one action per step
6. **Use wait_after_ms** to ensure actions complete

## Troubleshooting

### "GeminiClient is required"
```python
# Make sure to pass GeminiClient
generator = ProtocolGenerator(gemini_client=client)
```

### Validation fails
```python
# Check the issues
result = generator.validate_protocol(protocol)
print(result['issues'])
```

### Protocol not executing
```python
# Verify protocol structure
print(json.dumps(protocol, indent=2))

# Check actions array exists
assert 'actions' in protocol
```

## See Also

- `docs/PROTOCOL_GENERATION_IMPLEMENTATION.md` - Complete action library
- `docs/PROTOCOL_EXECUTOR_README.md` - Execution details
- `shared/protocol_models.py` - Protocol data models
- `shared/protocol_parser.py` - Validation logic
