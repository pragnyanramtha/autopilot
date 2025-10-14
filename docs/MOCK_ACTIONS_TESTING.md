# Mock Actions for Testing Without API Calls

## Overview

Mock actions allow you to test your automation protocols without:
- ❌ Making API calls to Gemini (saves money!)
- ❌ Actually moving the mouse or clicking
- ❌ Typing on the keyboard
- ❌ Capturing screenshots

Instead, they:
- ✅ Simulate realistic behavior and timing
- ✅ Log all actions for debugging
- ✅ Return mock results (coordinates, success/failure)
- ✅ Test protocol generation and execution flow

## Why Use Mock Actions?

### Save API Credits
Testing with real actions means:
- Every `visual_navigate` = 1-3 Gemini API calls
- Every `verify_screen` = 1 Gemini API call
- Testing a protocol 10 times = 20-40 API calls

With mock actions:
- **Zero API calls**
- Test as much as you want
- Perfect for development and debugging

### Safe Testing
- No accidental mouse movements
- No accidental clicks or typing
- No interference with your work
- Can run in the background

### Fast Iteration
- No waiting for API responses
- Instant feedback
- Test protocol structure and flow
- Validate parameter passing

## Quick Start

### 1. Run the Test Suite

```bash
python tests/test_with_mock_actions.py
```

This will run three test scenarios:
1. Basic protocol execution (Twitter posting simulation)
2. Verify screen mock (random success/failure)
3. Complex workflow with macros

### 2. Use Mock Actions in Your Code

```python
from shared.action_registry import ActionRegistry
from shared.mock_action_handlers import MockActionHandlers
from shared.protocol_executor import ProtocolExecutor

# Initialize
action_registry = ActionRegistry()
mock_handlers = MockActionHandlers(action_registry)

# Register mock actions instead of real ones
mock_handlers.register_all_mock_actions()

# Execute your protocol
executor = ProtocolExecutor(action_registry)
result = executor.execute_protocol(your_protocol)

# View execution log
mock_handlers.print_summary()
```

### 3. Test a Protocol File

```python
from shared.protocol_parser import JSONProtocolParser

# Load protocol
parser = JSONProtocolParser()
protocol = parser.parse_file('examples/protocols/mock_testing_example.json')

# Execute with mock actions
executor = ProtocolExecutor(action_registry)
result = executor.execute_protocol(protocol)
```

## Available Mock Actions

All standard actions are available as mocks:

### Mouse Actions
- `mouse_move` - Simulates movement with timing
- `mouse_click` - Simulates clicks

### Keyboard Actions
- `type` - Simulates typing with realistic timing
- `press_key` - Simulates key press
- `shortcut` - Simulates keyboard shortcuts

### Application Actions
- `open_app` - Simulates app launch (1s delay)
- `open_url` - Simulates URL opening (0.5s delay)

### Visual Actions
- `visual_navigate` - Simulates visual navigation with iterations
  - Returns mock coordinates
  - Simulates 1-3 iterations
  - Always succeeds
- `verify_screen` - Simulates screen verification
  - 80% success rate (random)
  - Returns mock coordinates on success
  - Returns suggested actions on failure

### Utility Actions
- `wait` - Actual wait (not mocked)

## Mock Behavior

### visual_navigate Mock

```python
# Input
{"action": "visual_navigate", "params": {"task": "Click the submit button"}}

# Output (console)
[MOCK] Visual navigate: Click the submit button
  Goal: Click the submit button
  Iteration 1/2: Analyzing screen...
  Iteration 2/2: Analyzing screen...
  ✓ Found target at (847, 523)
  ✓ Clicked successfully

# Returns
{
  'task': 'Click the submit button',
  'iterations': 2,
  'coordinates': {'x': 847, 'y': 523},
  'success': True
}
```

### verify_screen Mock

```python
# Input
{"action": "verify_screen", "params": {"context": "Looking for button", "expected": "Button visible"}}

# Output (console) - Success case
[MOCK] Verifying screen
  Context: Looking for button
  Expected: Button visible
  ✓ SAFE (confidence: 0.87)

# Returns (success)
{
  'safe_to_proceed': True,
  'confidence': 0.87,
  'analysis': 'Mock: Button visible is visible and ready',
  'verified_x': 1234,
  'verified_y': 567
}

# Output (console) - Failure case
[MOCK] Verifying screen
  Context: Looking for button
  Expected: Button visible
  ✗ NOT SAFE (confidence: 0.45)

# Returns (failure)
{
  'safe_to_proceed': False,
  'confidence': 0.45,
  'analysis': 'Mock: Button visible is not visible or not ready',
  'suggested_actions': ['Wait for page to load', 'Refresh the page']
}
```

## Execution Log

Mock handlers maintain an execution log:

```python
# Get log
log = mock_handlers.get_execution_log()

# Each entry contains
{
  'action': 'visual_navigate',
  'params': {'task': 'Click button'},
  'result': {'success': True, 'coordinates': {'x': 100, 'y': 200}},
  'timestamp': 1234567890.123
}

# Print summary
mock_handlers.print_summary()
```

Output:
```
============================================================
MOCK EXECUTION SUMMARY
============================================================
Total actions executed: 7

Actions by type:
  mouse_click: 2
  open_app: 1
  press_key: 1
  type: 2
  visual_navigate: 1
============================================================
```

## Example Test Protocol

See `examples/protocols/mock_testing_example.json` for a complete example.

```json
{
  "version": "1.0",
  "metadata": {
    "description": "Example protocol for testing with mock actions",
    "complexity": "medium",
    "uses_vision": true
  },
  "actions": [
    {"action": "open_app", "params": {"app_name": "chrome"}, "wait_after_ms": 2000},
    {"action": "visual_navigate", "params": {"task": "Click the search field"}, "wait_after_ms": 500},
    {"action": "type", "params": {"text": "test query"}, "wait_after_ms": 500},
    {"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 2000}
  ]
}
```

## Testing Protocol Generation

You can also test protocol generation without executing:

```python
from ai_brain.gemini_client import GeminiClient
from ai_brain.protocol_generator import ProtocolGenerator

# This will still make API calls to generate the protocol
# But you can then test it with mock actions
client = GeminiClient()
generator = ProtocolGenerator(client)

# Generate protocol (uses API)
protocol = generator.create_protocol(intent, "post on twitter")

# Test execution with mock actions (no API)
executor = ProtocolExecutor(action_registry)  # with mock handlers
result = executor.execute_protocol(protocol)
```

## Best Practices

### 1. Test Protocol Structure First
Use mock actions to validate:
- Protocol syntax is correct
- Actions are in the right order
- Parameters are passed correctly
- Macros work as expected

### 2. Then Test with Real Actions
Once the protocol structure is validated:
- Switch to real action handlers
- Test with actual automation
- Verify real-world behavior

### 3. Use Mock for Regression Testing
- Create test protocols
- Run with mock actions in CI/CD
- Catch protocol generation issues early

### 4. Debug with Execution Log
```python
# Execute protocol
result = executor.execute_protocol(protocol)

# Check what happened
log = mock_handlers.get_execution_log()
for entry in log:
    print(f"{entry['action']}: {entry['params']}")
```

## Switching Between Mock and Real

```python
# Mock mode (no API calls, no automation)
from shared.mock_action_handlers import MockActionHandlers
mock_handlers = MockActionHandlers(action_registry)
mock_handlers.register_all_mock_actions()

# Real mode (API calls, actual automation)
from shared.action_handlers import ActionHandlers
real_handlers = ActionHandlers(action_registry)
real_handlers.register_all()
```

## Limitations

Mock actions don't test:
- ❌ Actual visual recognition accuracy
- ❌ Real timing and coordination issues
- ❌ Actual UI element detection
- ❌ Real-world edge cases

They DO test:
- ✅ Protocol structure and syntax
- ✅ Parameter passing and substitution
- ✅ Macro expansion
- ✅ Execution flow and error handling
- ✅ Action sequencing

## Files

- `shared/mock_action_handlers.py` - Mock action implementations
- `tests/test_with_mock_actions.py` - Test suite
- `examples/protocols/mock_testing_example.json` - Example protocol
- `docs/MOCK_ACTIONS_TESTING.md` - This documentation

## Summary

Mock actions are perfect for:
- 💰 Saving API credits during development
- 🚀 Fast iteration on protocol structure
- 🧪 Testing without side effects
- 📊 Debugging execution flow
- ✅ Validating protocol syntax

Use them during development, then switch to real actions for final testing!
