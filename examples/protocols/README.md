# Protocol Examples

This directory contains example JSON protocols demonstrating various features of the JSON Instruction Protocol system.

## Examples Overview

### 1. Simple Search (`simple_search.json`)

**Complexity:** Simple  
**Uses Vision:** No  
**Duration:** ~15 seconds

Demonstrates basic protocol features:
- Opening an application
- Using macros for reusable action sequences
- Variable substitution in macros (`{{query}}`)
- Sequential browser searches

**What it does:**
1. Opens Chrome browser
2. Searches for "Elon Musk"
3. Opens a new tab
4. Searches for "Jeff Bezos"

**Key Features:**
- `search_in_browser` macro with variable substitution
- `new_tab` macro for reusability
- Simple sequential execution

---

### 2. Twitter/X Post (`twitter_post.json`)

**Complexity:** Medium  
**Uses Vision:** Yes  
**Duration:** ~30 seconds

Demonstrates content generation and visual verification:
- Full content generation in `type` action
- Visual verification for UI element location
- Adaptive mouse movements using verified coordinates
- Multi-step workflow with verification checkpoints

**What it does:**
1. Opens Chrome and navigates to x.com
2. Uses AI vision to locate the compose area
3. Types a complete post with emojis and hashtags
4. Uses AI vision to locate the Post button
5. Publishes the post
6. Verifies successful publication

**Key Features:**
- `verify_screen` action for adaptive UI navigation
- `{{verified_x}}` and `{{verified_y}}` coordinate substitution
- Complete content generation (280 character post)
- Smooth mouse movements to verified coordinates

---

### 3. Visual Verification Workflow (`visual_verification_workflow.json`)

**Complexity:** Medium  
**Uses Vision:** Yes  
**Duration:** ~25 seconds

Demonstrates comprehensive visual verification usage:
- Multiple verification checkpoints
- Adaptive navigation based on AI vision
- Confidence thresholds for verification
- Form filling with visual guidance

**What it does:**
1. Opens Chrome and verifies it launched
2. Navigates to GitHub
3. Uses AI vision to find and click Sign in button
4. Verifies login page loaded
5. Uses AI vision to locate and fill username field
6. Uses AI vision to locate and fill password field
7. Uses AI vision to find and click Sign in button

**Key Features:**
- Multiple `verify_screen` actions throughout workflow
- Different confidence thresholds (0.8, 0.85, 0.9)
- Adaptive mouse movements based on verified coordinates
- Context-aware verification descriptions

---

### 4. Complex Macro Workflow (`complex_macro_workflow.json`)

**Complexity:** Complex  
**Uses Vision:** No  
**Duration:** ~45 seconds

Demonstrates advanced macro composition:
- Nested macros (macros calling other macros)
- Multiple variable substitutions
- Multi-window management
- Complex text editing and file operations

**What it does:**
1. Opens three Notepad instances
2. Creates and saves "Meeting Notes" document
3. Creates and saves "Project Tasks" document
4. Creates a third document combining both
5. Switches between windows to copy content
6. Saves combined summary
7. Opens File Explorer to view created files

**Key Features:**
- 8 reusable macros: `open_notepad`, `save_file_as`, `create_text_document`, `switch_to_next_window`, `select_all_and_copy`, `open_file_explorer`, `navigate_to_documents`
- Nested macro calls (`create_text_document` calls `save_file_as`)
- Multiple variable substitutions (`{{content}}`, `{{filename}}`)
- Window switching and clipboard operations
- Long-form content in `type` actions

---

### 5. File Management Workflow (`file_management_workflow.json`)

**Complexity:** Medium  
**Uses Vision:** No  
**Duration:** ~25 seconds

Demonstrates file system operations:
- Creating folders
- Opening and editing files
- Saving files with specific paths
- Using macros for common file operations

**What it does:**
1. Creates a new folder in Documents
2. Opens Notepad
3. Types document content
4. Saves file to the new folder
5. Edits the content
6. Saves and closes using a macro
7. Reopens the file to verify changes

**Key Features:**
- `create_folder` action for directory creation
- `save_and_close` macro for common file operations
- File path specification in save dialog
- `select_all` for text replacement
- `open_file` to reopen saved files

---

### 6. Multi-Window Workflow (`multi_window_workflow.json`)

**Complexity:** Complex  
**Uses Vision:** Yes  
**Duration:** ~40 seconds

Demonstrates working with multiple applications simultaneously:
- Window switching between applications
- Copying data from browser to text editor
- Visual verification across window switches
- Complex multi-step workflows

**What it does:**
1. Opens Chrome and navigates to GitHub trending
2. Uses AI vision to find first trending repository
3. Copies repository name
4. Opens Notepad in parallel
5. Pastes first repository name
6. Switches back to Chrome
7. Finds and copies second repository
8. Switches to Notepad and pastes
9. Closes both applications

**Key Features:**
- `switch_window` action for Alt+Tab navigation
- Multiple `verify_screen` actions across window switches
- Clipboard operations between applications
- `copy_from_browser` and `paste_to_notepad` macros
- Coordinate verification in different windows

---

## Protocol Features Demonstrated

### Actions Used Across Examples

| Action | Simple Search | Twitter Post | Visual Verification | Complex Macro | File Management | Multi-Window |
|--------|--------------|--------------|---------------------|---------------|-----------------|--------------|
| `open_app` | ✓ | ✓ | ✓ | - | ✓ | ✓ |
| `press_key` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `shortcut` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `type` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `mouse_move` | - | ✓ | ✓ | - | - | ✓ |
| `mouse_click` | - | ✓ | ✓ | - | - | ✓ |
| `verify_screen` | - | ✓ | ✓ | - | - | ✓ |
| `macro` | ✓ | - | ✓ | ✓ | ✓ | ✓ |
| `delay` | - | - | - | ✓ | ✓ | - |
| `create_folder` | - | - | - | - | ✓ | - |
| `open_file` | - | - | - | - | ✓ | - |
| `select_all` | - | - | - | - | ✓ | ✓ |
| `switch_window` | - | - | - | - | - | ✓ |
| `copy` | - | - | - | - | - | ✓ |
| `paste` | - | - | - | - | - | ✓ |

### Macro Features

- **Simple macros:** `new_tab`, `focus_address_bar`
- **Parameterized macros:** `search_in_browser` with `{{query}}`
- **Nested macros:** `create_text_document` calls `save_file_as`
- **Multi-variable macros:** `create_text_document` with `{{content}}` and `{{filename}}`

### Visual Verification Features

- **Context descriptions:** Clear descriptions of what to look for
- **Expected outcomes:** Specific expectations for verification
- **Confidence thresholds:** 0.8 (low), 0.85 (medium), 0.9 (high)
- **Coordinate substitution:** `{{verified_x}}` and `{{verified_y}}`
- **Adaptive execution:** Mouse movements adjust based on AI vision

---

## Usage

### Running Examples with Protocol Executor

```python
from shared.protocol_executor import ProtocolExecutor
from shared.protocol_parser import JSONProtocolParser
import json

# Load protocol
with open('examples/protocols/simple_search.json', 'r') as f:
    protocol_json = json.load(f)

# Parse and validate
parser = JSONProtocolParser()
protocol = parser.parse(protocol_json)

# Execute
executor = ProtocolExecutor()
result = executor.execute(protocol)
print(result)
```

### Testing Visual Verification

```python
from shared.visual_verifier import VisualVerifier
from shared.protocol_executor import ProtocolExecutor
import json

# Load protocol with visual verification
with open('examples/protocols/twitter_post.json', 'r') as f:
    protocol_json = json.load(f)

# Execute with visual verification enabled
executor = ProtocolExecutor(enable_vision=True)
result = executor.execute(protocol_json)
```

### Validating Protocols

```python
from shared.protocol_parser import JSONProtocolParser
import json

# Load and validate
with open('examples/protocols/complex_macro_workflow.json', 'r') as f:
    protocol_json = json.load(f)

parser = JSONProtocolParser()
validation_result = parser.validate(protocol_json)

if validation_result['valid']:
    print("Protocol is valid!")
else:
    print(f"Validation errors: {validation_result['errors']}")
```

---

## Creating Your Own Protocols

### Basic Structure

```json
{
  "version": "1.0",
  "metadata": {
    "description": "Your workflow description",
    "complexity": "simple|medium|complex",
    "uses_vision": false,
    "estimated_duration_seconds": 10
  },
  "macros": {
    "macro_name": [
      {"action": "...", "params": {...}, "wait_after_ms": 0}
    ]
  },
  "actions": [
    {"action": "...", "params": {...}, "wait_after_ms": 0}
  ]
}
```

### Best Practices

1. **Use macros for repeated patterns** - If you do the same sequence more than once, make it a macro
2. **Add descriptive metadata** - Help others understand what your protocol does
3. **Use visual verification when uncertain** - Better to verify than to fail
4. **Set appropriate wait times** - Give UI time to respond between actions
5. **Use smooth mouse movements** - Set `"smooth": true` for natural movement
6. **Add descriptions to actions** - Document what each action does
7. **Test incrementally** - Build complex workflows step by step

### Common Patterns

**Opening and navigating to a website:**
```json
{
  "action": "open_app",
  "params": {"app_name": "chrome"},
  "wait_after_ms": 2000
},
{
  "action": "shortcut",
  "params": {"keys": ["ctrl", "l"]},
  "wait_after_ms": 200
},
{
  "action": "type",
  "params": {"text": "example.com"},
  "wait_after_ms": 100
},
{
  "action": "press_key",
  "params": {"key": "enter"},
  "wait_after_ms": 3000
}
```

**Visual verification and adaptive clicking:**
```json
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
  "params": {
    "x": "{{verified_x}}",
    "y": "{{verified_y}}",
    "smooth": true
  },
  "wait_after_ms": 200
},
{
  "action": "mouse_click",
  "params": {"button": "left", "clicks": 1},
  "wait_after_ms": 1000
}
```

**Reusable macro with variables:**
```json
"macros": {
  "fill_form_field": [
    {
      "action": "press_key",
      "params": {"key": "tab"},
      "wait_after_ms": 200
    },
    {
      "action": "type",
      "params": {"text": "{{field_value}}"},
      "wait_after_ms": 300
    }
  ]
}
```

---

## Requirements Mapping

These examples satisfy the following requirements from the spec:

- **Requirement 1.1:** JSON protocol structure with metadata and actions
- **Requirement 11.1:** Visual verification with AI vision models
- **Requirement 7.1:** Macro composition and variable substitution
- **Requirement 2.1-2.6:** Comprehensive action usage (keyboard, mouse, window management)
- **Requirement 12.1-12.2:** Smooth mouse movements with visual feedback

---

## See Also

- [Protocol Models Documentation](../../shared/PROTOCOL_MODELS_README.md)
- [Protocol Parser Documentation](../../shared/PROTOCOL_PARSER_README.md)
- [Protocol Executor Documentation](../../shared/PROTOCOL_EXECUTOR_README.md)
- [Visual Verification Documentation](../../shared/VISUAL_VERIFICATION_README.md)
- [Action Registry Documentation](../../shared/ACTION_REGISTRY_README.md)
