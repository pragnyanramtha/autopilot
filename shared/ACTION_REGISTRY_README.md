# Action Registry

The Action Registry is a comprehensive system for managing and executing automation actions in the JSON Instruction Protocol. It provides a centralized registry of 68+ action handlers organized into 12 categories.

## Overview

The Action Registry consists of two main components:

1. **ActionRegistry**: Core registry class that manages action handlers, validates parameters, and executes actions
2. **ActionHandlers**: Collection of handler functions that implement the actual automation actions

## Features

- **68+ Actions**: Comprehensive library covering keyboard, mouse, window management, browser control, and more
- **Parameter Validation**: Automatic validation of required and optional parameters
- **Type Safety**: Clear parameter types and return values
- **Documentation Generation**: Auto-generate documentation for all actions
- **Category Organization**: Actions organized into logical categories
- **Extensible**: Easy to add new actions and categories

## Action Categories

### 1. KEYBOARD (6 actions)
- `press_key`: Press and release a single key
- `shortcut`: Press multiple keys simultaneously (Ctrl+T, Alt+F4, etc.)
- `type`: Type text of any length
- `type_with_delay`: Type text with slower speed
- `hold_key`: Press and hold a key
- `release_key`: Release a held key

### 2. MOUSE (7 actions)
- `mouse_move`: Move mouse with smooth curved path
- `mouse_click`: Click at current position
- `mouse_double_click`: Double-click convenience
- `mouse_right_click`: Right-click convenience
- `mouse_drag`: Drag to target position
- `mouse_scroll`: Scroll up/down/left/right
- `mouse_position`: Get current mouse position

### 3. WINDOW (7 actions)
- `open_app`: Open application by name
- `close_app`: Close application
- `switch_window`: Alt+Tab window switching
- `minimize_window`: Minimize current window
- `maximize_window`: Maximize current window
- `restore_window`: Restore minimized window
- `get_active_window`: Get active window title

### 4. BROWSER (10 actions)
- `open_url`: Open URL in default browser
- `browser_back`: Navigate back
- `browser_forward`: Navigate forward
- `browser_refresh`: Refresh page
- `browser_new_tab`: Open new tab
- `browser_close_tab`: Close current tab
- `browser_switch_tab`: Switch tabs
- `browser_address_bar`: Focus address bar
- `browser_bookmark`: Bookmark page
- `browser_find`: Open find dialog

### 5. CLIPBOARD (6 actions)
- `copy`: Copy selected content
- `paste`: Paste from clipboard
- `cut`: Cut selected content
- `get_clipboard`: Read clipboard content
- `set_clipboard`: Write to clipboard
- `paste_from_clipboard`: Fast paste for long text

### 6. FILE (6 actions)
- `open_file`: Open file with default app
- `save_file`: Save current file
- `save_as`: Save as dialog
- `open_file_dialog`: Open file dialog
- `create_folder`: Create new folder
- `delete_file`: Delete file

### 7. SCREEN (4 actions)
- `capture_screen`: Full screen screenshot
- `capture_region`: Capture specific region
- `capture_window`: Capture active window
- `save_screenshot`: Save screenshot to file

### 8. TIMING (4 actions)
- `delay`: Wait for milliseconds
- `wait_for_window`: Wait for window title
- `wait_for_image`: Wait for image on screen
- `wait_for_color`: Wait for color at coordinates

### 9. VISION (4 actions)
- `verify_screen`: AI vision verification
- `verify_element`: Verify element exists
- `find_element`: Locate element coordinates
- `verify_text`: OCR text verification

### 10. SYSTEM (7 actions)
- `lock_screen`: Lock screen (Win+L)
- `sleep_system`: Put system to sleep
- `shutdown_system`: Shutdown system
- `restart_system`: Restart system
- `volume_up`: Increase volume
- `volume_down`: Decrease volume
- `volume_mute`: Toggle mute

### 11. EDIT (6 actions)
- `select_all`: Select all text
- `undo`: Undo last action
- `redo`: Redo last action
- `find_replace`: Find and replace dialog
- `delete_line`: Delete current line
- `duplicate_line`: Duplicate current line

### 12. MACRO (1 action)
- `macro`: Execute predefined macro with variable substitution

## Usage

### Basic Usage

```python
from shared.action_registry import ActionRegistry
from shared.action_handlers import ActionHandlers

# Initialize registry
registry = ActionRegistry()
handlers = ActionHandlers(registry)
handlers.register_all()

# Execute an action
registry.execute("press_key", {"key": "enter"})
registry.execute("delay", {"ms": 1000})
registry.execute("mouse_move", {"x": 500, "y": 300})
```

### With Dependencies

```python
from automation_engine.input_controller import InputController
from automation_engine.mouse_controller import MouseController
from automation_engine.screen_capture import ScreenCapture

# Create dependencies
input_controller = InputController()
mouse_controller = MouseController()
screen_capture = ScreenCapture()

# Inject dependencies
registry.inject_dependencies(
    input_controller=input_controller,
    mouse_controller=mouse_controller,
    screen_capture=screen_capture
)

# Now actions will use the injected components
registry.execute("mouse_move", {"x": 500, "y": 300, "smooth": True})
```

### Parameter Validation

```python
# Get handler info
handler = registry.get_handler("press_key")

# Validate parameters
is_valid, error = handler.validate_params({"key": "enter"})
if not is_valid:
    print(f"Invalid parameters: {error}")

# Execute with validation
try:
    result = registry.execute("press_key", {"key": "enter"})
except ValueError as e:
    print(f"Execution failed: {e}")
```

### List Actions

```python
# List all actions
all_actions = registry.list_actions()
print(f"Total actions: {len(all_actions)}")

# List by category
from shared.action_registry import ActionCategory

keyboard_actions = registry.list_actions(ActionCategory.KEYBOARD)
print(f"Keyboard actions: {keyboard_actions}")
```

### Generate Documentation

```python
# Generate docs for all actions
docs = registry.generate_documentation()
print(docs)

# Generate docs for specific category
keyboard_docs = registry.generate_documentation(ActionCategory.KEYBOARD)
print(keyboard_docs)
```

### Get Action Library for AI

```python
# Get action library in AI-friendly format
library = registry.get_action_library_for_ai()

# This returns a dictionary like:
# {
#     "press_key": {
#         "category": "keyboard",
#         "description": "Press and release a SINGLE key",
#         "params": {
#             "required": ["key"],
#             "optional": {}
#         },
#         "examples": [...]
#     },
#     ...
# }
```

## Adding New Actions

To add a new action:

1. **Define the handler function** in `action_handlers.py`:

```python
def my_custom_action(param1: str, param2: int = 10):
    """My custom action implementation."""
    # Implementation here
    return result
```

2. **Register the action**:

```python
self.registry.register(
    name="my_custom_action",
    category=ActionCategory.KEYBOARD,  # Choose appropriate category
    description="Description of what this action does",
    handler=my_custom_action,
    required_params=["param1"],
    optional_params={"param2": 10},
    returns={"result": "str"},  # Optional
    examples=[
        '{"action": "my_custom_action", "params": {"param1": "value"}}'
    ]
)
```

## Architecture

```
ActionRegistry
├── _handlers: Dict[str, ActionHandler]
│   └── ActionHandler
│       ├── name: str
│       ├── category: ActionCategory
│       ├── description: str
│       ├── handler: Callable
│       ├── required_params: List[str]
│       ├── optional_params: Dict[str, Any]
│       ├── returns: Optional[Dict[str, str]]
│       └── examples: List[Any]
├── _categories: Dict[ActionCategory, List[str]]
└── Dependencies (injected)
    ├── input_controller
    ├── mouse_controller
    ├── screen_capture
    ├── visual_verifier
    └── macro_executor
```

## Error Handling

The registry provides comprehensive error handling:

- **Unknown Action**: Raises `ValueError` if action not found
- **Missing Parameters**: Raises `ValueError` if required params missing
- **Unknown Parameters**: Raises `ValueError` if unknown params provided
- **Execution Errors**: Wraps handler exceptions in `RuntimeError` with context

## Testing

Run the demo to see all actions:

```bash
python examples/action_registry_demo.py
```

Run tests:

```bash
python tests/test_action_registry.py
```

## Integration with Protocol Executor

The Action Registry is designed to be used by the Protocol Executor:

```python
# In protocol executor
registry = ActionRegistry()
handlers = ActionHandlers(registry)
handlers.register_all()

# Inject dependencies
registry.inject_dependencies(
    input_controller=input_controller,
    mouse_controller=mouse_controller,
    screen_capture=screen_capture,
    visual_verifier=visual_verifier,
    macro_executor=macro_executor
)

# Execute actions from protocol
for action in protocol["actions"]:
    action_name = action["action"]
    params = action.get("params", {})
    
    try:
        result = registry.execute(action_name, params)
        # Handle result
    except Exception as e:
        # Handle error
        pass
```

## Requirements

The Action Registry requires the following dependencies:

- `pyautogui`: For keyboard and mouse control
- `pyperclip`: For clipboard operations
- `mss`: For screen capture (via ScreenCapture)
- `PIL`: For image handling
- `numpy`: For mouse controller (smooth movements)

Optional dependencies:
- `pygetwindow`: For window management (fallback available)

## Performance

- Action lookup: O(1) - Direct dictionary access
- Parameter validation: O(n) where n is number of parameters
- Execution: Depends on action implementation

## Thread Safety

The Action Registry is **not thread-safe** by default. If using in a multi-threaded environment, wrap calls in locks:

```python
import threading

lock = threading.Lock()

with lock:
    registry.execute("press_key", {"key": "enter"})
```

## Future Enhancements

Planned improvements:

1. **Action Chaining**: Execute multiple actions in sequence
2. **Conditional Actions**: Support for if/else logic
3. **Action History**: Track executed actions for debugging
4. **Performance Metrics**: Measure action execution time
5. **Action Aliases**: Support multiple names for same action
6. **Custom Categories**: Allow users to define custom categories

## License

Part of the JSON Instruction Protocol implementation.
