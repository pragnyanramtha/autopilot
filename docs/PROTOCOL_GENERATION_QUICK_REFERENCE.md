# Protocol Generation Quick Reference

## Quick Start

```python
from ai_brain.gemini_client import GeminiClient
from shared.action_registry import ActionRegistry

# 1. Initialize
client = GeminiClient()
registry = ActionRegistry()
# ... register actions ...

# 2. Get action library
action_library = registry.get_action_library_for_ai()

# 3. Generate protocol
protocol = client.generate_protocol(
    "your natural language command here",
    action_library
)

# 4. Execute (with ProtocolExecutor)
from shared.protocol_executor import ProtocolExecutor
executor = ProtocolExecutor(registry)
result = executor.execute_protocol(protocol)
```

## Method Signature

```python
def generate_protocol(
    self,
    user_input: str,
    action_library: dict
) -> dict
```

**Parameters:**
- `user_input`: Natural language command from user
- `action_library`: Dictionary of available actions (from `registry.get_action_library_for_ai()`)

**Returns:**
- Dictionary containing the generated protocol

**Raises:**
- `ValueError`: If protocol generation or validation fails

## Protocol Structure

Generated protocols follow this structure:

```json
{
  "version": "1.0",
  "metadata": {
    "description": "What this protocol does",
    "complexity": "simple|medium|complex",
    "uses_vision": true|false
  },
  "macros": {
    "macro_name": [
      {"action": "...", "params": {...}, "wait_after_ms": 200}
    ]
  },
  "actions": [
    {"action": "...", "params": {...}, "wait_after_ms": 200}
  ]
}
```

## Key Features

### 1. Automatic Complexity Detection
The method automatically detects command complexity and selects the appropriate AI model:
- **Simple**: Single actions (click, type, open app)
- **Complex**: Multi-step workflows (research + write + post)

### 2. Response Caching
Identical commands are cached to avoid redundant API calls:
```python
# First call - hits API
protocol1 = client.generate_protocol("search for python", action_library)

# Second call - returns cached result
protocol2 = client.generate_protocol("search for python", action_library)
```

### 3. Validation
All generated protocols are validated before being returned:
- Required fields present (version, actions)
- Actions list not empty
- Each action has required 'action' field
- Proper structure for metadata and macros

### 4. Error Handling
Comprehensive error handling with descriptive messages:
```python
try:
    protocol = client.generate_protocol(command, action_library)
except ValueError as e:
    print(f"Protocol generation failed: {e}")
```

## Examples

### Simple Command
```python
protocol = client.generate_protocol(
    "open chrome and search for python",
    action_library
)
```

**Generated Protocol:**
```json
{
  "version": "1.0",
  "metadata": {
    "description": "Open Chrome and search for Python",
    "complexity": "simple"
  },
  "actions": [
    {"action": "open_app", "params": {"app_name": "chrome"}, "wait_after_ms": 2000},
    {"action": "shortcut", "params": {"keys": ["ctrl", "l"]}, "wait_after_ms": 200},
    {"action": "type", "params": {"text": "python"}, "wait_after_ms": 100},
    {"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 3000}
  ]
}
```

### Command with Macros
```python
protocol = client.generate_protocol(
    "search for elon musk and jeff bezos",
    action_library
)
```

**Generated Protocol:**
```json
{
  "version": "1.0",
  "macros": {
    "search_in_browser": [
      {"action": "shortcut", "params": {"keys": ["ctrl", "l"]}, "wait_after_ms": 200},
      {"action": "type", "params": {"text": "{{query}}"}, "wait_after_ms": 100},
      {"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 3000}
    ]
  },
  "actions": [
    {"action": "open_app", "params": {"app_name": "chrome"}, "wait_after_ms": 2000},
    {"action": "macro", "params": {"name": "search_in_browser", "vars": {"query": "elon musk"}}},
    {"action": "shortcut", "params": {"keys": ["ctrl", "t"]}, "wait_after_ms": 1000},
    {"action": "macro", "params": {"name": "search_in_browser", "vars": {"query": "jeff bezos"}}}
  ]
}
```

### Command with Visual Verification
```python
protocol = client.generate_protocol(
    "post about winter on twitter",
    action_library
)
```

**Generated Protocol:**
```json
{
  "version": "1.0",
  "metadata": {
    "uses_vision": true
  },
  "actions": [
    {"action": "open_app", "params": {"app_name": "chrome"}, "wait_after_ms": 2000},
    {"action": "shortcut", "params": {"keys": ["ctrl", "l"]}, "wait_after_ms": 200},
    {"action": "type", "params": {"text": "x.com"}, "wait_after_ms": 100},
    {"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 3000},
    {"action": "verify_screen", "params": {"context": "Looking for post input", "expected": "Post compose area visible"}, "wait_after_ms": 500},
    {"action": "mouse_move", "params": {"x": "{{verified_x}}", "y": "{{verified_y}}"}, "wait_after_ms": 200},
    {"action": "mouse_click", "params": {"button": "left"}, "wait_after_ms": 500},
    {"action": "type", "params": {"text": "Winter is here! ❄️ Complete post content..."}, "wait_after_ms": 1000}
  ]
}
```

## Performance Tips

1. **Reuse Action Library**: Get the action library once and reuse it:
   ```python
   action_library = registry.get_action_library_for_ai()
   
   # Reuse for multiple commands
   protocol1 = client.generate_protocol(cmd1, action_library)
   protocol2 = client.generate_protocol(cmd2, action_library)
   ```

2. **Enable Ultra-Fast Mode**: For development, use ultra-fast model:
   ```python
   client = GeminiClient(use_ultra_fast=True)
   # or set environment variable
   # USE_ULTRA_FAST_MODEL=true
   ```

3. **Cache Clearing**: Clear cache if needed:
   ```python
   client.clear_cache()
   ```

4. **Performance Stats**: Monitor performance:
   ```python
   stats = client.get_performance_stats()
   print(f"Avg response time: {stats['avg_response_time']:.2f}s")
   ```

## Troubleshooting

### Issue: "Failed to generate protocol"
**Cause**: AI response couldn't be parsed or validated
**Solution**: Check API key, network connection, and command clarity

### Issue: "Protocol missing 'version' field"
**Cause**: AI generated invalid protocol structure
**Solution**: Simplify command or try again (AI responses can vary)

### Issue: Slow generation
**Cause**: Using complex model for simple commands
**Solution**: Enable ultra-fast mode or simplify command

### Issue: Cache not working
**Cause**: Action library hash changes between calls
**Solution**: Reuse the same action library object

## Integration with Existing Code

### Replace Workflow Generation
```python
# OLD
from ai_brain.workflow_generator import WorkflowGenerator
generator = WorkflowGenerator(client)
workflow = generator.generate_workflow(command)

# NEW
action_library = registry.get_action_library_for_ai()
protocol = client.generate_protocol(command, action_library)
```

### With Protocol Executor
```python
# Generate and execute in one flow
protocol = client.generate_protocol(command, action_library)
result = executor.execute_protocol(protocol)
```

## API Reference

### Main Method
- `generate_protocol(user_input, action_library)` - Generate protocol from command

### Helper Methods (Internal)
- `_build_protocol_prompt_template(user_input, action_library)` - Build AI prompt
- `_format_action_library(action_library)` - Format actions for prompt
- `_parse_protocol_response(response_text)` - Parse AI response
- `_validate_protocol_structure(protocol)` - Validate protocol structure

### Inherited Methods
- `_switch_model(complexity)` - Switch AI model based on complexity
- `_get_cached_response(cache_key)` - Get cached response
- `_cache_response(cache_key, response)` - Cache response
- `_detect_command_complexity(user_input)` - Detect command complexity

## See Also

- [Protocol Generation Implementation](PROTOCOL_GENERATION_IMPLEMENTATION.md) - Detailed implementation docs
- [Protocol Executor README](../shared/PROTOCOL_EXECUTOR_README.md) - Protocol execution
- [Action Registry README](../shared/ACTION_REGISTRY_README.md) - Action library
- [Protocol Models README](../shared/PROTOCOL_MODELS_README.md) - Protocol data models
