# Protocol Executor

The Protocol Executor is the execution engine for the JSON Instruction Protocol. It handles sequential action execution, macro expansion, variable substitution, timing control, and comprehensive error handling.

## Overview

The `ProtocolExecutor` class executes `ProtocolSchema` objects by:
1. Processing actions sequentially
2. Expanding and executing macros with variable substitution
3. Managing execution context and state
4. Providing pause/resume/stop controls
5. Handling errors with structured error information

## Key Components

### ExecutionContext

Maintains state during protocol execution:
- **Variables**: Store and retrieve variables for use across actions
- **Action Results**: Track results from each executed action
- **Current Position**: Track which action is currently executing

```python
context = ExecutionContext(protocol_id="my_protocol")
context.set_variable("x", 100)
context.add_result("press_key", None)
value = context.get_variable("x")  # Returns 100
```

### ExecutionError

Structured error information for debugging and recovery:
- **Action Index**: Which action failed (0-based)
- **Action Name**: Name of the failed action
- **Error Type**: Exception type (ValueError, RuntimeError, etc.)
- **Error Message**: Detailed error message
- **Timestamp**: When the error occurred
- **Parameters**: Parameters that were passed to the action

### ExecutionResult

Result of protocol execution:
- **Status**: 'success', 'failed', 'stopped', or 'paused'
- **Actions Completed**: Number of actions successfully executed
- **Total Actions**: Total number of actions in protocol
- **Duration**: Execution time in milliseconds
- **Error**: Human-readable error message (if failed)
- **Error Details**: Structured error information (if failed)
- **Context**: Full execution context for debugging

## Usage

### Basic Execution

```python
from shared.protocol_executor import ProtocolExecutor
from shared.action_registry import ActionRegistry
from shared.protocol_models import ProtocolSchema

# Create action registry and register handlers
registry = ActionRegistry()
# ... register action handlers ...

# Create executor
executor = ProtocolExecutor(registry, dry_run=False)

# Execute protocol
result = executor.execute_protocol(protocol)

if result.status == 'success':
    print(f"Protocol completed in {result.duration_ms}ms")
else:
    print(f"Protocol failed: {result.error}")
    if result.error_details:
        print(f"Failed at action {result.error_details.action_index}: {result.error_details.action_name}")
```

### Dry Run Mode

Test protocols without executing actions:

```python
executor = ProtocolExecutor(registry, dry_run=True)
result = executor.execute_protocol(protocol)
# Actions are logged but not executed
```

### Pause/Resume/Stop Controls

```python
import threading

# Start execution in background thread
def run():
    result = executor.execute_protocol(protocol)

thread = threading.Thread(target=run)
thread.start()

# Pause execution
executor.pause_execution()

# Check status
status = executor.get_execution_status()
print(f"Running: {status['is_running']}, Paused: {status['is_paused']}")

# Resume execution
executor.resume_execution()

# Emergency stop
executor.stop_execution()

thread.join()
```

### Error Handling

The executor provides comprehensive error information:

```python
result = executor.execute_protocol(protocol)

if result.status == 'failed':
    # Basic error message
    print(f"Error: {result.error}")
    
    # Structured error details
    if result.error_details:
        error = result.error_details
        print(f"Action: {error.action_name} (index {error.action_index})")
        print(f"Type: {error.error_type}")
        print(f"Message: {error.error_message}")
        print(f"Parameters: {error.params}")
        print(f"Timestamp: {error.timestamp}")
    
    # Execution context (for recovery)
    if result.context:
        print(f"Actions completed: {len(result.context['action_results'])}")
        print(f"Variables: {result.context['variables']}")
        
        # Could potentially resume from error point
        next_action = error.action_index + 1
        print(f"Could resume from action {next_action}")
```

## Macro Execution

The executor supports macro expansion with variable substitution:

### Simple Macro

```python
protocol = ProtocolSchema(
    version="1.0",
    metadata=Metadata(description="Macro example"),
    macros={
        "copy_paste": MacroDefinition(
            name="copy_paste",
            actions=[
                ActionStep(action="shortcut", params={"keys": ["ctrl", "c"]}, wait_after_ms=100),
                ActionStep(action="shortcut", params={"keys": ["ctrl", "v"]}, wait_after_ms=100)
            ]
        )
    },
    actions=[
        ActionStep(action="macro", params={"name": "copy_paste"})
    ]
)
```

### Macro with Variables

```python
protocol = ProtocolSchema(
    version="1.0",
    metadata=Metadata(description="Variable substitution"),
    macros={
        "search": MacroDefinition(
            name="search",
            actions=[
                ActionStep(action="shortcut", params={"keys": ["ctrl", "l"]}, wait_after_ms=200),
                ActionStep(action="type", params={"text": "{{query}}"}, wait_after_ms=100),
                ActionStep(action="press_key", params={"key": "enter"}, wait_after_ms=1000)
            ]
        )
    },
    actions=[
        ActionStep(action="macro", params={"name": "search", "vars": {"query": "elon musk"}}),
        ActionStep(action="macro", params={"name": "search", "vars": {"query": "jeff bezos"}})
    ]
)
```

### Nested Macros

Macros can call other macros:

```python
protocol = ProtocolSchema(
    version="1.0",
    metadata=Metadata(description="Nested macros"),
    macros={
        "type_text": MacroDefinition(
            name="type_text",
            actions=[
                ActionStep(action="type", params={"text": "{{text}}"})
            ]
        ),
        "type_and_submit": MacroDefinition(
            name="type_and_submit",
            actions=[
                ActionStep(action="macro", params={"name": "type_text", "vars": {"text": "{{content}}"}}),
                ActionStep(action="press_key", params={"key": "enter"})
            ]
        )
    },
    actions=[
        ActionStep(action="macro", params={"name": "type_and_submit", "vars": {"content": "Hello World"}})
    ]
)
```

## Variable Substitution

Variables use `{{variable_name}}` syntax and are substituted at execution time:

### In String Parameters

```python
ActionStep(action="type", params={"text": "Hello {{name}}"})
# With vars={"name": "Alice"} becomes: "Hello Alice"
```

### In Nested Structures

```python
ActionStep(
    action="custom_action",
    params={
        "message": "{{msg}}",
        "options": {
            "speed": "{{speed}}"
        }
    }
)
# Variables are substituted recursively
```

### Context Variables

Variables can also come from the execution context:

```python
# Set variable in context
executor._current_context.set_variable("verified_x", 500)
executor._current_context.set_variable("verified_y", 300)

# Use in action
ActionStep(action="mouse_move", params={"x": "{{verified_x}}", "y": "{{verified_y}}"})
```

## Timing Control

Each action can specify `wait_after_ms` for timing:

```python
ActionStep(
    action="press_key",
    params={"key": "enter"},
    wait_after_ms=1000  # Wait 1 second after pressing enter
)
```

The executor respects these delays to ensure proper timing between actions.

## Execution Status

Get real-time execution status:

```python
status = executor.get_execution_status()

print(f"Running: {status['is_running']}")
print(f"Paused: {status['is_paused']}")
print(f"Dry Run: {status['dry_run']}")

if status['is_running']:
    print(f"Protocol: {status['protocol_id']}")
    print(f"Progress: {status['current_action']}/{status['total_actions']}")
```

## Context Retrieval

Access execution context during or after execution:

```python
# During execution (from another thread)
context = executor.get_context()
if context:
    print(f"Current action: {context['current_action_index']}")
    print(f"Variables: {context['variables']}")
    print(f"Results: {len(context['action_results'])}")

# After execution (from result)
result = executor.execute_protocol(protocol)
if result.context:
    for action_result in result.context['action_results']:
        print(f"Action: {action_result['action']}")
        print(f"Result: {action_result['result']}")
        if action_result['error']:
            print(f"Error: {action_result['error']}")
```

## Error Recovery

The executor provides enough information to potentially resume execution:

```python
result = executor.execute_protocol(protocol)

if result.status == 'failed' and result.error_details:
    # Know exactly where it failed
    failed_index = result.error_details.action_index
    
    # Could create a new protocol starting from next action
    remaining_actions = protocol.actions[failed_index + 1:]
    
    # Create recovery protocol
    recovery_protocol = ProtocolSchema(
        version=protocol.version,
        metadata=Metadata(description="Recovery protocol"),
        macros=protocol.macros,  # Keep same macros
        actions=remaining_actions
    )
    
    # Execute recovery protocol
    recovery_result = executor.execute_protocol(recovery_protocol)
```

## Thread Safety

The executor uses locks to ensure thread-safe operation:
- Only one protocol can execute at a time
- Pause/resume/stop operations are thread-safe
- Status queries are thread-safe

## Best Practices

1. **Use Dry Run First**: Test protocols in dry run mode before actual execution
2. **Handle Errors**: Always check `result.status` and handle failures
3. **Use Macros**: Create reusable macros for common action sequences
4. **Set Appropriate Timing**: Use `wait_after_ms` to ensure actions complete
5. **Monitor Status**: Use `get_execution_status()` for long-running protocols
6. **Preserve Context**: Save `result.context` for debugging and recovery

## Requirements Satisfied

- **4.1**: Sequential action execution ✓
- **4.2**: Execution context management ✓
- **4.3**: Timing control with wait_after_ms ✓
- **4.4**: Pause/resume/stop controls ✓
- **4.5**: Error handling with structured responses ✓
- **6.4**: Context preservation on error ✓
- **7.1**: Macro execution with variable substitution ✓
- **10.1**: Context and state management ✓
- **10.2**: Result storage and retrieval ✓

## Testing

Comprehensive tests are available:
- `tests/test_protocol_executor_simple.py` - Basic functionality
- `tests/test_protocol_executor_macros.py` - Macro execution
- `tests/test_protocol_executor_errors.py` - Error handling

Run tests:
```bash
python tests/test_protocol_executor_simple.py
python tests/test_protocol_executor_macros.py
python tests/test_protocol_executor_errors.py
```

## Example: Complete Protocol Execution

```python
from shared.protocol_executor import ProtocolExecutor
from shared.action_registry import ActionRegistry
from shared.protocol_models import ProtocolSchema, ActionStep, Metadata, MacroDefinition

# Setup
registry = ActionRegistry()
# ... register handlers ...

executor = ProtocolExecutor(registry, dry_run=False)

# Create protocol
protocol = ProtocolSchema(
    version="1.0",
    metadata=Metadata(
        description="Search example",
        complexity="simple"
    ),
    macros={
        "search": MacroDefinition(
            name="search",
            actions=[
                ActionStep(action="shortcut", params={"keys": ["ctrl", "l"]}, wait_after_ms=200),
                ActionStep(action="type", params={"text": "{{query}}"}, wait_after_ms=100),
                ActionStep(action="press_key", params={"key": "enter"}, wait_after_ms=2000)
            ]
        )
    },
    actions=[
        ActionStep(action="open_app", params={"app_name": "chrome"}, wait_after_ms=2000),
        ActionStep(action="macro", params={"name": "search", "vars": {"query": "python programming"}})
    ]
)

# Execute
result = executor.execute_protocol(protocol)

# Handle result
if result.status == 'success':
    print(f"✓ Protocol completed successfully in {result.duration_ms}ms")
    print(f"  Actions executed: {result.actions_completed}/{result.total_actions}")
else:
    print(f"✗ Protocol failed: {result.error}")
    if result.error_details:
        print(f"  Failed at: {result.error_details.action_name} (index {result.error_details.action_index})")
        print(f"  Error type: {result.error_details.error_type}")
```
