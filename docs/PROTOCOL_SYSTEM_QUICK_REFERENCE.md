# Protocol System Quick Reference

## Overview

The AI Automation Assistant now uses a JSON-based protocol system for all automation tasks. This guide provides quick reference for developers and users.

## System Components

### 1. AI Brain (`ai_brain/main.py`)
- Processes natural language commands
- Generates JSON protocols using `ProtocolGenerator`
- Sends protocols to Automation Engine

### 2. Automation Engine (`automation_engine/main.py`)
- Receives JSON protocols
- Executes protocols using `ProtocolExecutor`
- Reports results back to AI Brain

### 3. Protocol Generator (`ai_brain/protocol_generator.py`)
- Converts `CommandIntent` to JSON protocols
- Validates protocol structure
- Supports simple and complex protocols

### 4. Protocol Executor (`shared/protocol_executor.py`)
- Executes JSON protocols sequentially
- Handles macros and variable substitution
- Provides pause/resume/stop controls

### 5. Action Registry (`shared/action_registry.py`)
- Registers 80+ automation actions
- Maps action names to Python functions
- Provides action documentation

## Protocol Structure

```json
{
  "version": "1.0",
  "metadata": {
    "id": "unique-id",
    "description": "What this protocol does",
    "complexity": "simple|medium|complex",
    "uses_vision": false
  },
  "macros": {
    "macro_name": [
      {"action": "...", "params": {...}, "wait_after_ms": 100}
    ]
  },
  "actions": [
    {
      "action": "action_name",
      "params": {"key": "value"},
      "wait_after_ms": 100,
      "description": "Optional description"
    }
  ]
}
```

## Common Actions

### Keyboard Actions
```json
{"action": "press_key", "params": {"key": "enter"}}
{"action": "shortcut", "params": {"keys": ["ctrl", "t"]}}
{"action": "type", "params": {"text": "Hello World"}}
```

### Mouse Actions
```json
{"action": "mouse_move", "params": {"x": 500, "y": 300}}
{"action": "mouse_click", "params": {"button": "left"}}
{"action": "mouse_drag", "params": {"x": 600, "y": 400}}
```

### Window Management
```json
{"action": "open_app", "params": {"app_name": "chrome"}}
{"action": "switch_window", "params": {}}
{"action": "maximize_window", "params": {}}
```

### Browser Actions
```json
{"action": "open_url", "params": {"url": "https://example.com"}}
{"action": "browser_new_tab", "params": {}}
{"action": "browser_refresh", "params": {}}
```

### Visual Verification
```json
{
  "action": "verify_screen",
  "params": {
    "context": "Looking for login button",
    "expected": "Login button visible"
  }
}
```

## Usage Examples

### Simple Command
```python
# User: "Open Chrome"
# AI generates:
{
  "version": "1.0",
  "metadata": {"description": "Open Chrome"},
  "actions": [
    {"action": "open_app", "params": {"app_name": "chrome"}, "wait_after_ms": 2000}
  ]
}
```

### Complex Command with Macros
```python
# User: "Search for Python tutorials"
# AI generates:
{
  "version": "1.0",
  "metadata": {"description": "Search for Python tutorials"},
  "macros": {
    "search_in_browser": [
      {"action": "shortcut", "params": {"keys": ["ctrl", "l"]}, "wait_after_ms": 200},
      {"action": "type", "params": {"text": "{{query}}"}, "wait_after_ms": 100},
      {"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 3000}
    ]
  },
  "actions": [
    {"action": "open_app", "params": {"app_name": "chrome"}, "wait_after_ms": 2000},
    {"action": "macro", "params": {"name": "search_in_browser", "vars": {"query": "Python tutorials"}}}
  ]
}
```

## Running the System

### Start AI Brain
```bash
python -m ai_brain.main
```

### Start Automation Engine
```bash
python -m automation_engine.main
```

### Start Both (Unified Launcher)
```bash
python run.py
```

### Start with CLI
```bash
python scripts/cli.py
```

## API Reference

### ProtocolGenerator

```python
from ai_brain.protocol_generator import ProtocolGenerator

generator = ProtocolGenerator(gemini_client, config)

# Create protocol from intent
protocol = generator.create_protocol(intent, user_input)

# Validate protocol
validation = generator.validate_protocol(protocol)
if validation['valid']:
    # Protocol is ready to execute
    pass
```

### ProtocolExecutor

```python
from shared.protocol_executor import ProtocolExecutor
from shared.action_registry import ActionRegistry

registry = ActionRegistry()
executor = ProtocolExecutor(action_registry=registry, dry_run=False)

# Execute protocol
result = executor.execute_protocol(protocol)

# Check result
if result.status == 'success':
    print(f"Completed {result.actions_completed} actions")
```

### ActionRegistry

```python
from shared.action_registry import ActionRegistry

registry = ActionRegistry()

# List all actions
actions = registry.list_actions()

# Get action info
info = registry.get_action_info("mouse_move")

# Register custom action
def my_action(**params):
    print(f"Custom action: {params}")

registry.register_action("my_action", my_action, "Custom action description")
```

## Communication Flow

```
1. User enters command
   ↓
2. GeminiClient.process_command() → CommandIntent
   ↓
3. ProtocolGenerator.create_protocol() → JSON Protocol
   ↓
4. MessageBroker.send_protocol() → File system
   ↓
5. MessageBroker.receive_protocol() → Automation Engine
   ↓
6. ProtocolExecutor.execute_protocol() → Actions
   ↓
7. MessageBroker.send_protocol_status() → AI Brain
   ↓
8. Display result to user
```

## Configuration

### config.json
```json
{
  "gemini": {
    "model": "gemini-2.5-flash",
    "temperature": 0.7,
    "use_ultra_fast": false
  },
  "automation": {
    "safety_delay_ms": 100,
    "enable_safety_monitor": true
  },
  "protocol": {
    "validation_strict": true,
    "max_actions": 100,
    "max_macro_depth": 5
  }
}
```

### Environment Variables
```bash
GEMINI_API_KEY=your_api_key_here
USE_ULTRA_FAST_MODEL=false
```

## Troubleshooting

### Protocol Validation Errors
```python
validation = generator.validate_protocol(protocol)
if not validation['valid']:
    for issue in validation['issues']:
        print(f"Issue: {issue}")
```

### Execution Errors
```python
result = executor.execute_protocol(protocol)
if result.status == 'failed':
    print(f"Error: {result.error}")
    if result.error_details:
        print(f"Details: {result.error_details.to_dict()}")
```

### Communication Issues
```python
try:
    broker.send_protocol(protocol)
except CommunicationError as e:
    print(f"Communication error: {e}")
```

## Best Practices

1. **Always validate protocols** before sending to executor
2. **Use macros** for repeated action sequences
3. **Add descriptions** to actions for debugging
4. **Set appropriate wait times** between actions
5. **Use visual verification** for uncertain UI interactions
6. **Test in dry-run mode** before live execution
7. **Handle errors gracefully** with try-except blocks

## Resources

- **Full Documentation**: `docs/TASK12_SYSTEM_REPLACEMENT.md`
- **Protocol Models**: `shared/protocol_models.py`
- **Action Registry**: `shared/action_registry.py`
- **Examples**: `examples/protocols/`
- **Tests**: `tests/test_protocol_*.py`

## Support

For issues or questions:
1. Check verification script: `python verify_task12.py`
2. Review logs in console output
3. Check protocol validation results
4. Test with dry-run mode first

---

**Last Updated**: Task 12 Completion
**System Version**: Protocol System v1.0
