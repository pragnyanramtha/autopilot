# Task 16: Mock Actions for Testing Without API Calls

## Problem

Testing automation protocols is expensive because:
- Every `visual_navigate` action = 1-3 Gemini API calls
- Every `verify_screen` action = 1 Gemini API call
- Testing a protocol 10 times = 20-40 API calls
- API calls cost money and have rate limits

## Solution

Created a complete mock action system that simulates all automation actions without:
- Making any API calls
- Actually moving the mouse or clicking
- Typing on the keyboard
- Capturing screenshots

## What Was Created

### 1. Mock Action Handlers (`shared/mock_action_handlers.py`)

A complete implementation of mock versions of all actions:

**Mouse Actions:**
- `mouse_move` - Simulates movement with timing
- `mouse_click` - Simulates clicks

**Keyboard Actions:**
- `type` - Simulates typing with realistic timing
- `press_key` - Simulates key presses
- `shortcut` - Simulates keyboard shortcuts

**Application Actions:**
- `open_app` - Simulates app launch (1s delay)
- `open_url` - Simulates URL opening (0.5s delay)

**Visual Actions:**
- `visual_navigate` - Simulates visual navigation
  - Returns mock coordinates
  - Simulates 1-3 iterations
  - Always succeeds
- `verify_screen` - Simulates screen verification
  - 80% success rate (random)
  - Returns mock coordinates on success
  - Returns suggested actions on failure

**Utility Actions:**
- `wait` - Actual wait (not mocked)

### 2. Test Suite (`tests/test_with_mock_actions.py`)

Comprehensive test suite with three scenarios:

1. **Basic Protocol Execution** - Simulates Twitter posting
2. **Verify Screen Mock** - Tests random success/failure
3. **Complex Workflow with Macros** - Tests macro expansion and variables

### 3. Example Protocol (`examples/protocols/mock_testing_example.json`)

A complete example protocol that can be tested with mock actions, demonstrating:
- Application launching
- URL navigation with macros
- Visual navigation
- Screen verification
- Variable substitution

### 4. Documentation (`docs/MOCK_ACTIONS_TESTING.md`)

Complete guide covering:
- Why use mock actions
- Quick start guide
- Available mock actions
- Mock behavior details
- Execution logging
- Best practices
- Switching between mock and real

### 5. Quick Start Script (`run_mock_tests.bat`)

Simple batch file to run the test suite.

## Features

### Execution Logging

Mock handlers maintain a detailed log:
```python
log = mock_handlers.get_execution_log()
# Returns list of all executed actions with params and results
```

### Execution Summary

```python
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

### Realistic Behavior

Mock actions simulate realistic behavior:
- **Timing:** Actions take realistic time (app launch = 1s, typing = 50ms per char)
- **Coordinates:** Returns random but valid coordinates
- **Success/Failure:** `verify_screen` randomly fails 20% of the time
- **Iterations:** `visual_navigate` simulates 1-3 iterations

### Console Output

Mock actions print what they're doing:
```
[MOCK] Opening application: chrome
[MOCK] Pressing shortcut: ctrl+l
[MOCK] Typing: 'x.com'
[MOCK] Pressing key: enter
[MOCK] Visual navigate: Click the compose field
  Goal: Click the compose field
  Iteration 1/2: Analyzing screen...
  Iteration 2/2: Analyzing screen...
  ✓ Found target at (847, 523)
  ✓ Clicked successfully
```

## Usage

### Quick Test

```bash
python tests/test_with_mock_actions.py
```

or

```bash
run_mock_tests.bat
```

### In Your Code

```python
from shared.action_registry import ActionRegistry
from shared.mock_action_handlers import MockActionHandlers
from shared.protocol_executor import ProtocolExecutor

# Initialize with mock actions
action_registry = ActionRegistry()
mock_handlers = MockActionHandlers(action_registry)
mock_handlers.register_all_mock_actions()

# Execute protocol (no API calls!)
executor = ProtocolExecutor(action_registry)
result = executor.execute_protocol(your_protocol)

# View what happened
mock_handlers.print_summary()
```

### Switching Between Mock and Real

```python
# Mock mode (no API calls)
from shared.mock_action_handlers import MockActionHandlers
mock_handlers = MockActionHandlers(action_registry)
mock_handlers.register_all_mock_actions()

# Real mode (API calls, actual automation)
from shared.action_handlers import ActionHandlers
real_handlers = ActionHandlers(action_registry)
real_handlers.register_all()
```

## Benefits

### 💰 Save Money
- Zero API calls
- Test as much as you want
- No rate limits

### 🚀 Fast Iteration
- Instant feedback
- No waiting for API responses
- Test protocol structure quickly

### 🛡️ Safe Testing
- No accidental mouse movements
- No accidental clicks or typing
- Can run in the background

### 🧪 Perfect for Development
- Test protocol syntax
- Validate parameter passing
- Debug execution flow
- Test macro expansion

### 📊 Detailed Logging
- See exactly what actions were executed
- View parameters and results
- Debug issues easily

## What Mock Actions Test

### ✅ They DO Test:
- Protocol structure and syntax
- Parameter passing and substitution
- Macro expansion
- Execution flow and error handling
- Action sequencing
- Variable substitution

### ❌ They DON'T Test:
- Actual visual recognition accuracy
- Real timing and coordination issues
- Actual UI element detection
- Real-world edge cases

## Example Output

```
============================================================
TESTING WITH MOCK ACTIONS (No API calls)
============================================================

Protocol: Test protocol with mock actions
Actions: 7
Uses vision: True

============================================================

Executing protocol with mock actions...

[1/7] Executing: open_app
  [MOCK] Opening application: chrome
[2/7] Executing: shortcut
  [MOCK] Pressing shortcut: ctrl+l
[3/7] Executing: type
  [MOCK] Typing: 'x.com'
[4/7] Executing: press_key
  [MOCK] Pressing key: enter
[5/7] Executing: visual_navigate
  [MOCK] Visual navigate: Click the 'What's happening?' post compose input field
    Goal: Click the 'What's happening?' post compose input field
    Iteration 1/2: Analyzing screen...
    Iteration 2/2: Analyzing screen...
    ✓ Found target at (847, 523)
    ✓ Clicked successfully
[6/7] Executing: type
  [MOCK] Typing: 'This is a test post! 🚀 #Testing #Automation'
[7/7] Executing: visual_navigate
  [MOCK] Visual navigate: Click the blue 'Post' button to publish the tweet
    Goal: Click the blue 'Post' button to publish the tweet
    Iteration 1/1: Analyzing screen...
    ✓ Found target at (1234, 678)
    ✓ Clicked successfully

============================================================
EXECUTION RESULT
============================================================
Status: success
Actions completed: 7/7
Duration: 8523ms
============================================================

============================================================
MOCK EXECUTION SUMMARY
============================================================
Total actions executed: 7

Actions by type:
  open_app: 1
  press_key: 1
  shortcut: 1
  type: 2
  visual_navigate: 2
============================================================
```

## Files Created

1. `shared/mock_action_handlers.py` - Mock action implementations (350 lines)
2. `tests/test_with_mock_actions.py` - Test suite (300 lines)
3. `examples/protocols/mock_testing_example.json` - Example protocol
4. `docs/MOCK_ACTIONS_TESTING.md` - Complete documentation
5. `run_mock_tests.bat` - Quick start script
6. `docs/TASK16_MOCK_ACTIONS_SUMMARY.md` - This summary

## Use Cases

### 1. Protocol Development
Test protocol structure without API calls:
```python
# Generate protocol (uses API once)
protocol = generator.create_protocol(intent, user_input)

# Test execution multiple times (no API calls)
for i in range(10):
    result = executor.execute_protocol(protocol)
    assert result.status == 'success'
```

### 2. Regression Testing
```python
# Load test protocols
protocols = load_test_protocols()

# Test all without API calls
for protocol in protocols:
    result = executor.execute_protocol(protocol)
    assert result.status == 'success'
```

### 3. Debugging
```python
# Execute with mock
result = executor.execute_protocol(protocol)

# Check execution log
log = mock_handlers.get_execution_log()
for entry in log:
    print(f"{entry['action']}: {entry['result']}")
```

### 4. CI/CD Testing
```bash
# In your CI pipeline
python tests/test_with_mock_actions.py
# No API keys needed, no rate limits, fast execution
```

## Impact

This mock action system enables:
- ✅ Unlimited testing without API costs
- ✅ Fast development iteration
- ✅ Safe testing without side effects
- ✅ Detailed execution logging
- ✅ Easy debugging
- ✅ CI/CD integration

Perfect for development and testing before deploying to production with real actions!
