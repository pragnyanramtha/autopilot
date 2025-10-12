# Action Library Reference

Complete reference for all available actions in the JSON Instruction Protocol.

## Table of Contents

- [Keyboard Actions](#keyboard-actions)
- [Mouse Actions](#mouse-actions)
- [Window Management Actions](#window-management-actions)
- [Browser Actions](#browser-actions)
- [Clipboard Actions](#clipboard-actions)
- [File System Actions](#file-system-actions)
- [Screen Capture Actions](#screen-capture-actions)
- [Timing and Control Actions](#timing-and-control-actions)
- [Visual Verification Actions](#visual-verification-actions)
- [System Control Actions](#system-control-actions)
- [Text Editing Actions](#text-editing-actions)
- [Macro Execution](#macro-execution)

---

## Keyboard Actions

### press_key

Press and release a SINGLE key.

**Parameters:**
- `key` (string, required): The key to press

**Examples:**

```json
{"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 100}
{"action": "press_key", "params": {"key": "escape"}, "wait_after_ms": 50}
{"action": "press_key", "params": {"key": "tab"}, "wait_after_ms": 100}
{"action": "press_key", "params": {"key": "space"}, "wait_after_ms": 50}
{"action": "press_key", "params": {"key": "backspace"}, "wait_after_ms": 50}
{"action": "press_key", "params": {"key": "delete"}, "wait_after_ms": 50}
```

**Common Keys:**
- `enter`, `escape`, `tab`, `space`, `backspace`, `delete`
- `up`, `down`, `left`, `right`
- `home`, `end`, `pageup`, `pagedown`
- `f1` through `f12`

---

### shortcut

Press MULTIPLE keys SIMULTANEOUSLY (keyboard shortcuts like Ctrl+T, Alt+F4).

**Parameters:**
- `keys` (array of strings, required): Keys to press simultaneously

**Examples:**

```json
// New tab
{"action": "shortcut", "params": {"keys": ["ctrl", "t"]}, "wait_after_ms": 1000}

// Copy
{"action": "shortcut", "params": {"keys": ["ctrl", "c"]}, "wait_after_ms": 100}

// Paste
{"action": "shortcut", "params": {"keys": ["ctrl", "v"]}, "wait_after_ms": 100}

// Close window
{"action": "shortcut", "params": {"keys": ["alt", "f4"]}, "wait_after_ms": 500}

// Task Manager
{"action": "shortcut", "params": {"keys": ["ctrl", "shift", "esc"]}, "wait_after_ms": 2000}

// Save
{"action": "shortcut", "params": {"keys": ["ctrl", "s"]}, "wait_after_ms": 500}

// Select All
{"action": "shortcut", "params": {"keys": ["ctrl", "a"]}, "wait_after_ms": 100}
```

**Important:** Always use `shortcut` for keyboard combinations, NOT multiple `press_key` actions.

---

### type

Type text of ANY length (words, sentences, paragraphs, full posts).

**Parameters:**
- `text` (string, required): Text to type
- `interval_ms` (integer, optional): Delay between keystrokes in milliseconds (default: 50)

**Examples:**

```json
// Short text
{"action": "type", "params": {"text": "hello world"}, "wait_after_ms": 100}

// URL
{"action": "type", "params": {"text": "github.com"}, "wait_after_ms": 100}

// Full tweet/post
{
  "action": "type",
  "params": {
    "text": "Winter is here! ❄️ The crisp air, cozy sweaters, and hot cocoa make this season magical. #Winter #CozyVibes"
  },
  "wait_after_ms": 1000
}

// Slower typing for sensitive fields
{
  "action": "type",
  "params": {
    "text": "password123",
    "interval_ms": 100
  },
  "wait_after_ms": 500
}
```

**Note:** For very long text (>500 characters), consider using `paste_from_clipboard` for faster execution.

---

### type_with_delay

Type text with slower speed (for sensitive fields or applications that need slower input).

**Parameters:**
- `text` (string, required): Text to type
- `delay_ms` (integer, required): Delay between keystrokes

**Example:**

```json
{
  "action": "type_with_delay",
  "params": {
    "text": "sensitive_data",
    "delay_ms": 150
  },
  "wait_after_ms": 500
}
```

---

### hold_key

Press and hold a key (must be released with `release_key`).

**Parameters:**
- `key` (string, required): Key to hold

**Example:**

```json
// Hold Shift while clicking
{"action": "hold_key", "params": {"key": "shift"}, "wait_after_ms": 100}
{"action": "mouse_click", "params": {"button": "left"}, "wait_after_ms": 100}
{"action": "release_key", "params": {"key": "shift"}, "wait_after_ms": 100}
```

---

### release_key

Release a held key.

**Parameters:**
- `key` (string, required): Key to release

**Example:**

```json
{"action": "release_key", "params": {"key": "shift"}, "wait_after_ms": 50}
```

---

## Mouse Actions

### mouse_move

Move mouse to coordinates (smooth curved path by default).

**Parameters:**
- `x` (integer, required): Target X coordinate
- `y` (integer, required): Target Y coordinate
- `smooth` (boolean, optional): Use smooth curved movement (default: true)
- `speed` (float, optional): Movement speed multiplier (default: 1.0)

**Examples:**

```json
// Smooth movement (default)
{"action": "mouse_move", "params": {"x": 500, "y": 300}, "wait_after_ms": 200}

// Fast straight movement
{
  "action": "mouse_move",
  "params": {"x": 800, "y": 400, "smooth": false},
  "wait_after_ms": 100
}

// Slower smooth movement
{
  "action": "mouse_move",
  "params": {"x": 1000, "y": 600, "smooth": true, "speed": 0.5},
  "wait_after_ms": 300
}
```

---

### mouse_click

Click mouse button at current position.

**Parameters:**
- `button` (string, optional): Button to click - "left", "right", or "middle" (default: "left")
- `clicks` (integer, optional): Number of clicks (default: 1)

**Examples:**

```json
// Left click
{"action": "mouse_click", "params": {}, "wait_after_ms": 200}

// Right click
{"action": "mouse_click", "params": {"button": "right"}, "wait_after_ms": 200}

// Double click
{"action": "mouse_click", "params": {"clicks": 2}, "wait_after_ms": 200}

// Middle click
{"action": "mouse_click", "params": {"button": "middle"}, "wait_after_ms": 200}
```

---

### mouse_double_click

Double-click at current position (convenience action).

**Parameters:**
- `button` (string, optional): Button to click (default: "left")

**Example:**

```json
{"action": "mouse_double_click", "params": {}, "wait_after_ms": 200}
```

---

### mouse_right_click

Right-click at current position (convenience action).

**Parameters:** None

**Example:**

```json
{"action": "mouse_right_click", "params": {}, "wait_after_ms": 200}
```

---

### mouse_drag

Drag mouse from current position to target coordinates.

**Parameters:**
- `x` (integer, required): Target X coordinate
- `y` (integer, required): Target Y coordinate
- `smooth` (boolean, optional): Use smooth curved movement (default: true)

**Example:**

```json
// Select text by dragging
{"action": "mouse_move", "params": {"x": 100, "y": 200}, "wait_after_ms": 100}
{"action": "mouse_drag", "params": {"x": 400, "y": 200}, "wait_after_ms": 200}
```

---

### mouse_scroll

Scroll mouse wheel.

**Parameters:**
- `direction` (string, required): "up", "down", "left", or "right"
- `amount` (integer, required): Scroll amount (positive integer)

**Examples:**

```json
// Scroll down
{"action": "mouse_scroll", "params": {"direction": "down", "amount": 3}, "wait_after_ms": 200}

// Scroll up
{"action": "mouse_scroll", "params": {"direction": "up", "amount": 5}, "wait_after_ms": 200}

// Horizontal scroll
{"action": "mouse_scroll", "params": {"direction": "right", "amount": 2}, "wait_after_ms": 200}
```

---

### mouse_position

Get current mouse position.

**Parameters:** None

**Returns:**
- `x` (integer): Current X coordinate
- `y` (integer): Current Y coordinate

**Example:**

```json
{"action": "mouse_position", "params": {}}
```

---

## Window Management Actions

### open_app

Open application by name.

**Parameters:**
- `app_name` (string, required): Application name

**Examples:**

```json
{"action": "open_app", "params": {"app_name": "chrome"}, "wait_after_ms": 2000}
{"action": "open_app", "params": {"app_name": "notepad"}, "wait_after_ms": 1000}
{"action": "open_app", "params": {"app_name": "calculator"}, "wait_after_ms": 1000}
{"action": "open_app", "params": {"app_name": "vscode"}, "wait_after_ms": 3000}
{"action": "open_app", "params": {"app_name": "excel"}, "wait_after_ms": 2000}
```

**Common App Names:**
- `chrome`, `firefox`, `edge`
- `notepad`, `wordpad`
- `calculator`
- `vscode`, `sublime`, `atom`
- `excel`, `word`, `powerpoint`

---

### close_app

Close application by name.

**Parameters:**
- `app_name` (string, required): Application name

**Example:**

```json
{"action": "close_app", "params": {"app_name": "notepad"}, "wait_after_ms": 500}
```

---

### switch_window

Switch to next/previous window (Alt+Tab).

**Parameters:**
- `direction` (string, optional): "next" or "previous" (default: "next")

**Examples:**

```json
// Switch to next window
{"action": "switch_window", "params": {}, "wait_after_ms": 500}

// Switch to previous window
{"action": "switch_window", "params": {"direction": "previous"}, "wait_after_ms": 500}
```

---

### minimize_window

Minimize current window.

**Parameters:** None

**Example:**

```json
{"action": "minimize_window", "params": {}, "wait_after_ms": 300}
```

---

### maximize_window

Maximize current window.

**Parameters:** None

**Example:**

```json
{"action": "maximize_window", "params": {}, "wait_after_ms": 300}
```

---

### restore_window

Restore minimized window.

**Parameters:** None

**Example:**

```json
{"action": "restore_window", "params": {}, "wait_after_ms": 300}
```

---

### get_active_window

Get title of active window.

**Parameters:** None

**Returns:**
- `title` (string): Window title

**Example:**

```json
{"action": "get_active_window", "params": {}}
```

---

## Browser Actions

### open_url

Open URL in default browser.

**Parameters:**
- `url` (string, required): URL to open

**Example:**

```json
{"action": "open_url", "params": {"url": "https://github.com"}, "wait_after_ms": 3000}
```

---

### browser_back

Navigate back (Alt+Left or Backspace).

**Parameters:** None

**Example:**

```json
{"action": "browser_back", "params": {}, "wait_after_ms": 1000}
```

---

### browser_forward

Navigate forward (Alt+Right).

**Parameters:** None

**Example:**

```json
{"action": "browser_forward", "params": {}, "wait_after_ms": 1000}
```

---

### browser_refresh

Refresh page (F5 or Ctrl+R).

**Parameters:** None

**Example:**

```json
{"action": "browser_refresh", "params": {}, "wait_after_ms": 2000}
```

---

### browser_new_tab

Open new tab (Ctrl+T).

**Parameters:** None

**Example:**

```json
{"action": "browser_new_tab", "params": {}, "wait_after_ms": 1000}
```

---

### browser_close_tab

Close current tab (Ctrl+W).

**Parameters:** None

**Example:**

```json
{"action": "browser_close_tab", "params": {}, "wait_after_ms": 500}
```

---

### browser_switch_tab

Switch to next/previous tab.

**Parameters:**
- `direction` (string, optional): "next" or "previous" (default: "next")

**Examples:**

```json
// Next tab
{"action": "browser_switch_tab", "params": {}, "wait_after_ms": 300}

// Previous tab
{"action": "browser_switch_tab", "params": {"direction": "previous"}, "wait_after_ms": 300}
```

---

### browser_address_bar

Focus address bar (Ctrl+L).

**Parameters:** None

**Example:**

```json
{"action": "browser_address_bar", "params": {}, "wait_after_ms": 200}
```

---

### browser_bookmark

Bookmark current page (Ctrl+D).

**Parameters:** None

**Example:**

```json
{"action": "browser_bookmark", "params": {}, "wait_after_ms": 500}
```

---

### browser_find

Open find dialog (Ctrl+F).

**Parameters:** None

**Example:**

```json
{"action": "browser_find", "params": {}, "wait_after_ms": 300}
```

---

## Clipboard Actions

### copy

Copy selected content (Ctrl+C).

**Parameters:** None

**Example:**

```json
{"action": "copy", "params": {}, "wait_after_ms": 100}
```

---

### paste

Paste from clipboard (Ctrl+V).

**Parameters:** None

**Example:**

```json
{"action": "paste", "params": {}, "wait_after_ms": 200}
```

---

### cut

Cut selected content (Ctrl+X).

**Parameters:** None

**Example:**

```json
{"action": "cut", "params": {}, "wait_after_ms": 100}
```

---

### get_clipboard

Read clipboard content.

**Parameters:** None

**Returns:**
- `text` (string): Clipboard content

**Example:**

```json
{"action": "get_clipboard", "params": {}}
```

---

### set_clipboard

Write text to clipboard.

**Parameters:**
- `text` (string, required): Text to write

**Example:**

```json
{"action": "set_clipboard", "params": {"text": "Hello, World!"}, "wait_after_ms": 100}
```

---

### paste_from_clipboard

Paste specific text via clipboard (fast for long text).

**Parameters:**
- `text` (string, required): Text to paste

**Example:**

```json
{
  "action": "paste_from_clipboard",
  "params": {
    "text": "Very long text content that would be slow to type character by character..."
  },
  "wait_after_ms": 200
}
```

**Note:** This is faster than `type` for long text (>500 characters).

---

## File System Actions

### open_file

Open file with default application.

**Parameters:**
- `path` (string, required): File path

**Example:**

```json
{"action": "open_file", "params": {"path": "C:\\Users\\Documents\\report.pdf"}, "wait_after_ms": 2000}
```

---

### save_file

Save current file (Ctrl+S).

**Parameters:** None

**Example:**

```json
{"action": "save_file", "params": {}, "wait_after_ms": 500}
```

---

### save_as

Save as dialog (Ctrl+Shift+S).

**Parameters:** None

**Example:**

```json
{"action": "save_as", "params": {}, "wait_after_ms": 1000}
```

---

### open_file_dialog

Open file dialog (Ctrl+O).

**Parameters:** None

**Example:**

```json
{"action": "open_file_dialog", "params": {}, "wait_after_ms": 1000}
```

---

### create_folder

Create new folder.

**Parameters:**
- `path` (string, required): Folder path

**Example:**

```json
{"action": "create_folder", "params": {"path": "C:\\Users\\Documents\\NewFolder"}, "wait_after_ms": 500}
```

---

### delete_file

Delete file (requires confirmation).

**Parameters:**
- `path` (string, required): File path

**Example:**

```json
{"action": "delete_file", "params": {"path": "C:\\Users\\Documents\\temp.txt"}, "wait_after_ms": 500}
```

---

## Screen Capture Actions

### capture_screen

Capture full screen screenshot.

**Parameters:** None

**Returns:**
- `image` (Image): Screenshot image

**Example:**

```json
{"action": "capture_screen", "params": {}}
```

---

### capture_region

Capture specific screen region.

**Parameters:**
- `x` (integer, required): Region X coordinate
- `y` (integer, required): Region Y coordinate
- `width` (integer, required): Region width
- `height` (integer, required): Region height

**Returns:**
- `image` (Image): Screenshot image

**Example:**

```json
{
  "action": "capture_region",
  "params": {"x": 100, "y": 100, "width": 800, "height": 600}
}
```

---

### capture_window

Capture active window.

**Parameters:** None

**Returns:**
- `image` (Image): Screenshot image

**Example:**

```json
{"action": "capture_window", "params": {}}
```

---

### save_screenshot

Save screenshot to file.

**Parameters:**
- `path` (string, required): File path to save

**Example:**

```json
{"action": "save_screenshot", "params": {"path": "C:\\Users\\Screenshots\\screen.png"}, "wait_after_ms": 500}
```

---

## Timing and Control Actions

### delay

Wait for specified milliseconds.

**Parameters:**
- `ms` (integer, required): Milliseconds to wait

**Examples:**

```json
{"action": "delay", "params": {"ms": 1000}}  // Wait 1 second
{"action": "delay", "params": {"ms": 500}}   // Wait 0.5 seconds
{"action": "delay", "params": {"ms": 2000}}  // Wait 2 seconds
```

---

### wait_for_window

Wait for window with specific title to appear.

**Parameters:**
- `title` (string, required): Window title to wait for
- `timeout_ms` (integer, optional): Timeout in milliseconds (default: 10000)

**Example:**

```json
{
  "action": "wait_for_window",
  "params": {"title": "Chrome", "timeout_ms": 5000},
  "wait_after_ms": 500
}
```

---

### wait_for_image

Wait for image to appear on screen.

**Parameters:**
- `image_path` (string, required): Path to reference image
- `timeout_ms` (integer, optional): Timeout in milliseconds (default: 10000)
- `confidence` (float, optional): Match confidence 0.0-1.0 (default: 0.8)

**Example:**

```json
{
  "action": "wait_for_image",
  "params": {
    "image_path": "C:\\Images\\button.png",
    "timeout_ms": 5000,
    "confidence": 0.9
  },
  "wait_after_ms": 500
}
```

---

### wait_for_color

Wait for specific color at coordinates.

**Parameters:**
- `x` (integer, required): X coordinate
- `y` (integer, required): Y coordinate
- `color` (string, required): Hex color code (e.g., "#FF0000")
- `timeout_ms` (integer, optional): Timeout in milliseconds (default: 10000)

**Example:**

```json
{
  "action": "wait_for_color",
  "params": {
    "x": 500,
    "y": 300,
    "color": "#00FF00",
    "timeout_ms": 5000
  },
  "wait_after_ms": 500
}
```

---

## Visual Verification Actions

### verify_screen

Pause and verify screen state with AI vision (use when uncertain).

**Parameters:**
- `context` (string, required): Description of what to verify
- `expected` (string, required): Expected state description
- `confidence_threshold` (float, optional): Confidence threshold 0.0-1.0 (default: 0.8)

**Examples:**

```json
// Verify Chrome opened
{
  "action": "verify_screen",
  "params": {
    "context": "Chrome should be open",
    "expected": "Chrome window with address bar visible"
  },
  "wait_after_ms": 500
}

// Verify login button location
{
  "action": "verify_screen",
  "params": {
    "context": "Looking for login button",
    "expected": "Login button visible and clickable",
    "confidence_threshold": 0.9
  },
  "wait_after_ms": 500
}

// Verify text input field
{
  "action": "verify_screen",
  "params": {
    "context": "Looking for text input field",
    "expected": "Text input field is focused and ready"
  },
  "wait_after_ms": 500
}
```

**Returns:**
- `safe_to_proceed` (boolean): Whether to continue
- `verified_x` (integer, optional): Updated X coordinate
- `verified_y` (integer, optional): Updated Y coordinate
- `message` (string): Verification message

---

### verify_element

Verify specific element exists on screen.

**Parameters:**
- `element_description` (string, required): Description of element

**Returns:**
- `exists` (boolean): Whether element exists
- `x` (integer): Element X coordinate
- `y` (integer): Element Y coordinate

**Example:**

```json
{
  "action": "verify_element",
  "params": {"element_description": "Submit button with blue background"}
}
```

---

### find_element

Locate element and return coordinates.

**Parameters:**
- `element_description` (string, required): Description of element

**Returns:**
- `x` (integer): Element X coordinate
- `y` (integer): Element Y coordinate
- `confidence` (float): Match confidence

**Example:**

```json
{
  "action": "find_element",
  "params": {"element_description": "Search icon in top right corner"}
}
```

---

### verify_text

Verify text exists on screen using OCR.

**Parameters:**
- `text` (string, required): Text to find

**Returns:**
- `exists` (boolean): Whether text exists
- `x` (integer): Text X coordinate
- `y` (integer): Text Y coordinate

**Example:**

```json
{
  "action": "verify_text",
  "params": {"text": "Welcome"}
}
```

---

## System Control Actions

### lock_screen

Lock screen (Win+L).

**Parameters:** None

**Example:**

```json
{"action": "lock_screen", "params": {}}
```

---

### sleep_system

Put system to sleep.

**Parameters:** None

**Example:**

```json
{"action": "sleep_system", "params": {}}
```

---

### shutdown_system

Shutdown system (requires confirmation).

**Parameters:** None

**Example:**

```json
{"action": "shutdown_system", "params": {}}
```

---

### restart_system

Restart system (requires confirmation).

**Parameters:** None

**Example:**

```json
{"action": "restart_system", "params": {}}
```

---

### volume_up

Increase system volume.

**Parameters:**
- `amount` (integer, optional): Volume increase 1-100 (default: 10)

**Example:**

```json
{"action": "volume_up", "params": {"amount": 20}, "wait_after_ms": 200}
```

---

### volume_down

Decrease system volume.

**Parameters:**
- `amount` (integer, optional): Volume decrease 1-100 (default: 10)

**Example:**

```json
{"action": "volume_down", "params": {"amount": 15}, "wait_after_ms": 200}
```

---

### volume_mute

Toggle volume mute.

**Parameters:** None

**Example:**

```json
{"action": "volume_mute", "params": {}, "wait_after_ms": 200}
```

---

## Text Editing Actions

### select_all

Select all text (Ctrl+A).

**Parameters:** None

**Example:**

```json
{"action": "select_all", "params": {}, "wait_after_ms": 100}
```

---

### undo

Undo last action (Ctrl+Z).

**Parameters:** None

**Example:**

```json
{"action": "undo", "params": {}, "wait_after_ms": 100}
```

---

### redo

Redo last undone action (Ctrl+Y).

**Parameters:** None

**Example:**

```json
{"action": "redo", "params": {}, "wait_after_ms": 100}
```

---

### find_replace

Open find and replace dialog (Ctrl+H).

**Parameters:** None

**Example:**

```json
{"action": "find_replace", "params": {}, "wait_after_ms": 500}
```

---

### delete_line

Delete current line.

**Parameters:** None

**Example:**

```json
{"action": "delete_line", "params": {}, "wait_after_ms": 100}
```

---

### duplicate_line

Duplicate current line.

**Parameters:** None

**Example:**

```json
{"action": "duplicate_line", "params": {}, "wait_after_ms": 100}
```

---

## Macro Execution

### macro

Execute predefined macro (reusable action sequence).

**Parameters:**
- `name` (string, required): Macro name
- `vars` (object, optional): Variables to substitute

**Example:**

```json
// Define macro in protocol
{
  "macros": {
    "search_in_browser": [
      {"action": "shortcut", "params": {"keys": ["ctrl", "l"]}, "wait_after_ms": 200},
      {"action": "type", "params": {"text": "{{query}}"}, "wait_after_ms": 100},
      {"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 5000}
    ]
  }
}

// Use macro
{
  "action": "macro",
  "params": {
    "name": "search_in_browser",
    "vars": {"query": "python tutorial"}
  }
}
```

---

## Summary

**Total Actions Available: 80+**

**Categories:**
- Keyboard: 6 actions
- Mouse: 7 actions
- Window Management: 7 actions
- Browser: 10 actions
- Clipboard: 6 actions
- File System: 6 actions
- Screen Capture: 4 actions
- Timing & Control: 4 actions
- Visual Verification: 4 actions
- System Control: 7 actions
- Text Editing: 6 actions
- Macro: 1 action

**Key Principles:**
1. Use `shortcut` for keyboard combinations (Ctrl+T, Alt+F4)
2. Use `press_key` for single keys (Enter, Escape)
3. Use `type` for any length text, including full posts
4. All mouse movements are smooth by default
5. Use `verify_screen` when uncertain about UI state
6. Use macros for reusable action sequences
7. Always include `wait_after_ms` for timing control
