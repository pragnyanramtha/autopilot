# JSON Instruction Protocol System Documentation

Complete system documentation for the JSON Instruction Protocol automation framework.

## Table of Contents

1. [Protocol Schema](#protocol-schema)
2. [Troubleshooting Guide](#troubleshooting-guide)
3. [Visual Verification Usage](#visual-verification-usage)
4. [Macro Creation and Usage](#macro-creation-and-usage)
5. [Performance Optimization Tips](#performance-optimization-tips)

---

## Protocol Schema

### Overview

The JSON Instruction Protocol uses a hybrid schema that combines simplicity with power. It's designed to be easy for AI to generate and easy for humans to read and modify.

### Complete Schema Structure

```json
{
  "version": "1.0",
  "metadata": {
    "description": "Human-readable description of what this protocol does",
    "complexity": "simple|medium|complex",
    "uses_vision": false,
    "estimated_duration_seconds": 30,
    "author": "optional",
    "created_at": "optional ISO timestamp",
    "tags": ["optional", "array", "of", "tags"]
  },
  "macros": {
    "macro_name": [
      {
        "action": "action_name",
        "params": {},
        "wait_after_ms": 0,
        "description": "optional action description"
      }
    ]
  },
  "actions": [
    {
      "action": "action_name",
      "params": {},
      "wait_after_ms": 0,
      "description": "optional action description"
    }
  ]
}
```

### Field Descriptions

#### Root Level

- **version** (string, required): Protocol version, currently "1.0"
- **metadata** (object, required): Protocol metadata
- **macros** (object, optional): Reusable action sequences
- **actions** (array, required): Main action sequence to execute

#### Metadata Object

- **description** (string, required): Clear description of protocol purpose
- **complexity** (string, required): "simple", "medium", or "complex"
- **uses_vision** (boolean, required): Whether protocol uses visual verification
- **estimated_duration_seconds** (integer, optional): Expected execution time
- **author** (string, optional): Protocol creator
- **created_at** (string, optional): ISO 8601 timestamp
- **tags** (array, optional): Categorization tags

#### Macros Object

Key-value pairs where:
- **Key**: Macro name (string)
- **Value**: Array of action objects

Macros support variable substitution using `{{variable_name}}` syntax.

#### Actions Array

Array of action objects, each containing:
- **action** (string, required): Action name from action library
- **params** (object, required): Action parameters (can be empty {})
- **wait_after_ms** (integer, optional): Milliseconds to wait after action (default: 0)
- **description** (string, optional): Human-readable action description

### Action Object Structure

```json
{
  "action": "type",
  "params": {
    "text": "Hello, World!",
    "interval_ms": 50
  },
  "wait_after_ms": 200,
  "description": "Type greeting message"
}
```

### Variable Substitution

Variables use double curly brace syntax: `{{variable_name}}`

**In Macros:**
```json
"macros": {
  "search_query": [
    {"action": "type", "params": {"text": "{{query}}"}, "wait_after_ms": 100}
  ]
}
```

**Using Macros with Variables:**
```json
{
  "action": "macro",
  "params": {
    "name": "search_query",
    "vars": {"query": "python tutorial"}
  }
}
```

**From Visual Verification:**
```json
{
  "action": "verify_screen",
  "params": {"context": "Find button", "expected": "Button visible"}
},
{
  "action": "mouse_move",
  "params": {"x": "{{verified_x}}", "y": "{{verified_y}}"}
}
```

### Schema Validation Rules

1. **Version must be "1.0"**
2. **Metadata must include description, complexity, and uses_vision**
3. **Actions array cannot be empty**
4. **Each action must have valid action name from action library**
5. **Action params must match expected parameter types**
6. **Macro names must be unique**
7. **Macro references must exist in macros object**
8. **No circular macro dependencies**
9. **wait_after_ms must be non-negative integer**
10. **Variable references must be defined when macro is called**


---

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Protocol Validation Errors

**Problem:** Protocol fails validation with schema errors

**Symptoms:**
```
ValidationError: Invalid protocol schema
- Missing required field: metadata.description
- Invalid action name: typo_action
```

**Solutions:**
- Verify all required fields are present (version, metadata, actions)
- Check action names against action library
- Ensure metadata includes description, complexity, uses_vision
- Validate JSON syntax (no trailing commas, proper quotes)

**Example Fix:**
```json
// ❌ WRONG
{
  "version": "1.0",
  "actions": []
}

// ✅ CORRECT
{
  "version": "1.0",
  "metadata": {
    "description": "My workflow",
    "complexity": "simple",
    "uses_vision": false
  },
  "actions": [
    {"action": "delay", "params": {"ms": 1000}}
  ]
}
```

---

#### 2. Macro Not Found

**Problem:** Protocol references undefined macro

**Symptoms:**
```
MacroError: Macro 'search_query' not found
```

**Solutions:**
- Verify macro is defined in macros object
- Check macro name spelling (case-sensitive)
- Ensure macros object exists if using macro action

**Example Fix:**
```json
// ❌ WRONG - macro not defined
{
  "actions": [
    {"action": "macro", "params": {"name": "search_query"}}
  ]
}

// ✅ CORRECT
{
  "macros": {
    "search_query": [
      {"action": "type", "params": {"text": "{{query}}"}}
    ]
  },
  "actions": [
    {"action": "macro", "params": {"name": "search_query", "vars": {"query": "test"}}}
  ]
}
```

---

#### 3. Circular Macro Dependencies

**Problem:** Macros reference each other in a loop

**Symptoms:**
```
MacroError: Circular dependency detected: macro_a -> macro_b -> macro_a
```

**Solutions:**
- Review macro definitions for circular references
- Restructure macros to avoid loops
- Consider combining macros or using direct actions

**Example Fix:**
```json
// ❌ WRONG - circular dependency
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

// ✅ CORRECT - no circular dependency
{
  "macros": {
    "macro_a": [
      {"action": "press_key", "params": {"key": "enter"}}
    ],
    "macro_b": [
      {"action": "macro", "params": {"name": "macro_a"}},
      {"action": "delay", "params": {"ms": 500}}
    ]
  }
}
```

---

#### 4. Missing Variable Substitution

**Problem:** Macro variable not provided when called

**Symptoms:**
```
VariableError: Variable 'query' not provided for macro 'search_query'
```

**Solutions:**
- Provide all required variables in vars parameter
- Check variable name spelling (case-sensitive)
- Ensure vars is an object with key-value pairs

**Example Fix:**
```json
// ❌ WRONG - missing variable
{
  "action": "macro",
  "params": {"name": "search_query"}
}

// ✅ CORRECT
{
  "action": "macro",
  "params": {
    "name": "search_query",
    "vars": {"query": "python tutorial"}
  }
}
```


---

#### 5. Action Execution Failures

**Problem:** Action fails during execution

**Symptoms:**
```
ExecutionError: Action 'mouse_click' failed: No mouse button pressed
ActionError: Action 'open_app' failed: Application 'chrme' not found
```

**Solutions:**
- Verify action parameters are correct
- Check application names for typos
- Ensure required applications are installed
- Add longer wait times before actions
- Use visual verification for uncertain UI states

**Example Fix:**
```json
// ❌ WRONG - typo in app name
{"action": "open_app", "params": {"app_name": "chrme"}}

// ✅ CORRECT
{"action": "open_app", "params": {"app_name": "chrome"}, "wait_after_ms": 2000}
```

---

#### 6. Visual Verification Timeout

**Problem:** Visual verification takes too long or fails

**Symptoms:**
```
VisionError: Visual verification timed out after 10000ms
VisionError: Gemini API unavailable, fallback failed
```

**Solutions:**
- Increase wait_after_ms before verification
- Lower confidence_threshold (default 0.8)
- Provide more specific context and expected descriptions
- Check internet connection for API access
- Verify Gemini API key is configured

**Example Fix:**
```json
// ❌ WRONG - vague description
{
  "action": "verify_screen",
  "params": {
    "context": "Find button",
    "expected": "Button exists"
  }
}

// ✅ CORRECT - specific description
{
  "action": "verify_screen",
  "params": {
    "context": "Looking for blue 'Submit' button in bottom right corner",
    "expected": "Submit button visible with blue background and white text",
    "confidence_threshold": 0.75
  },
  "wait_after_ms": 1000
}
```

---

#### 7. Timing Issues

**Problem:** Actions execute too fast or UI doesn't respond in time

**Symptoms:**
- Actions execute before UI is ready
- Mouse clicks miss targets
- Text typed into wrong fields

**Solutions:**
- Increase wait_after_ms values
- Add delay actions between critical steps
- Use wait_for_window for application launches
- Use visual verification to confirm UI state

**Example Fix:**
```json
// ❌ WRONG - no wait times
{"action": "open_app", "params": {"app_name": "chrome"}},
{"action": "type", "params": {"text": "github.com"}}

// ✅ CORRECT - appropriate waits
{"action": "open_app", "params": {"app_name": "chrome"}, "wait_after_ms": 2000},
{"action": "shortcut", "params": {"keys": ["ctrl", "l"]}, "wait_after_ms": 200},
{"action": "type", "params": {"text": "github.com"}, "wait_after_ms": 100}
```

---

#### 8. Mouse Movement Issues

**Problem:** Mouse doesn't move to correct coordinates

**Symptoms:**
- Mouse moves to wrong location
- Clicks miss targets
- Coordinates seem off

**Solutions:**
- Use visual verification to get accurate coordinates
- Check screen resolution and scaling settings
- Use smooth movements for better accuracy
- Verify coordinates are within screen bounds

**Example Fix:**
```json
// ❌ WRONG - hardcoded coordinates may be wrong
{"action": "mouse_move", "params": {"x": 500, "y": 300}},
{"action": "mouse_click", "params": {}}

// ✅ CORRECT - use visual verification
{"action": "verify_screen", "params": {"context": "Find button", "expected": "Button visible"}},
{"action": "mouse_move", "params": {"x": "{{verified_x}}", "y": "{{verified_y}}", "smooth": true}},
{"action": "mouse_click", "params": {}, "wait_after_ms": 500}
```

---

#### 9. Keyboard Shortcut Not Working

**Problem:** Keyboard shortcut doesn't execute correctly

**Symptoms:**
- Keys pressed sequentially instead of simultaneously
- Shortcut has no effect
- Wrong keys pressed

**Solutions:**
- Use shortcut action, not multiple press_key actions
- Verify key names are correct
- Check if application has focus
- Add wait time after shortcut

**Example Fix:**
```json
// ❌ WRONG - sequential key presses
{"action": "press_key", "params": {"key": "ctrl"}},
{"action": "press_key", "params": {"key": "t"}}

// ✅ CORRECT - simultaneous key press
{"action": "shortcut", "params": {"keys": ["ctrl", "t"]}, "wait_after_ms": 1000}
```


---

#### 10. Long Text Typing Slow

**Problem:** Typing long text takes too long

**Symptoms:**
- Protocol execution is very slow
- Typing character by character is inefficient

**Solutions:**
- Use paste_from_clipboard for text >500 characters
- Reduce interval_ms in type action
- Consider breaking into smaller chunks

**Example Fix:**
```json
// ❌ SLOW - typing 1000 characters
{"action": "type", "params": {"text": "Very long text content..."}}

// ✅ FAST - paste via clipboard
{"action": "paste_from_clipboard", "params": {"text": "Very long text content..."}}
```

---

### Debugging Tips

1. **Enable Dry Run Mode**: Test protocol without executing actions
   ```python
   executor = ProtocolExecutor(dry_run=True)
   ```

2. **Add Descriptions**: Document each action for easier debugging
   ```json
   {"action": "mouse_click", "params": {}, "description": "Click submit button"}
   ```

3. **Use Incremental Testing**: Build protocol step by step, test each addition

4. **Check Logs**: Review execution logs for detailed error information

5. **Validate Before Execution**: Always validate protocol before running
   ```python
   parser = JSONProtocolParser()
   result = parser.validate(protocol_json)
   ```

6. **Use Visual Verification Liberally**: When uncertain, verify with AI vision

7. **Test on Consistent Environment**: Same screen resolution, same applications

---

## Visual Verification Usage

### Overview

Visual verification uses AI vision models (Gemini 2.5 Flash Live API) to analyze screenshots and guide automation. It enables adaptive execution where the protocol can adjust based on actual UI state.

### When to Use Visual Verification

**Use visual verification when:**
- UI element locations are unknown or variable
- Need to confirm action success before proceeding
- Working with dynamic or responsive interfaces
- Element positions change based on content
- Uncertain about current UI state

**Don't use visual verification when:**
- Element locations are fixed and known
- Simple keyboard-only workflows
- Performance is critical (verification adds latency)
- Working offline (requires API access)

### Basic Visual Verification

```json
{
  "action": "verify_screen",
  "params": {
    "context": "What you're looking for",
    "expected": "What you expect to see"
  },
  "wait_after_ms": 500
}
```

**Parameters:**
- **context** (required): Description of what to verify or find
- **expected** (required): Expected state or element description
- **confidence_threshold** (optional): 0.0-1.0, default 0.8

**Returns:**
- **safe_to_proceed** (boolean): Whether to continue execution
- **verified_x** (integer, optional): X coordinate of found element
- **verified_y** (integer, optional): Y coordinate of found element
- **message** (string): Verification result message

### Adaptive Mouse Movement

Use verified coordinates for accurate mouse movements:

```json
{
  "action": "verify_screen",
  "params": {
    "context": "Looking for Submit button",
    "expected": "Blue Submit button visible in bottom right"
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
  "params": {"button": "left"},
  "wait_after_ms": 1000
}
```

### Confidence Thresholds

Adjust confidence based on verification importance:

- **0.6-0.7**: Low confidence, permissive matching
- **0.8**: Default, balanced accuracy
- **0.85-0.9**: High confidence, strict matching
- **0.95+**: Very high confidence, exact matching

```json
{
  "action": "verify_screen",
  "params": {
    "context": "Critical security dialog",
    "expected": "Security warning with red border",
    "confidence_threshold": 0.95
  }
}
```

### Writing Good Verification Descriptions

**Context - What to look for:**
- Be specific about location: "top right corner", "bottom of page"
- Mention visual characteristics: "blue button", "red text"
- Include surrounding context: "below the username field"

**Expected - What you expect:**
- Describe visual appearance: "button with white text on blue background"
- Mention state: "button is enabled and clickable"
- Include text content: "button labeled 'Submit'"

**Examples:**

```json
// ❌ VAGUE
{
  "context": "Find button",
  "expected": "Button exists"
}

// ✅ SPECIFIC
{
  "context": "Looking for login button in top right corner of navigation bar",
  "expected": "Blue rectangular button with white text 'Log In', approximately 100x40 pixels"
}
```


### Multi-Step Verification Workflow

Use multiple verification points for complex workflows:

```json
{
  "actions": [
    {
      "action": "open_app",
      "params": {"app_name": "chrome"},
      "wait_after_ms": 2000
    },
    {
      "action": "verify_screen",
      "params": {
        "context": "Verify Chrome opened successfully",
        "expected": "Chrome window with address bar visible"
      },
      "wait_after_ms": 500,
      "description": "Checkpoint 1: Chrome launched"
    },
    {
      "action": "shortcut",
      "params": {"keys": ["ctrl", "l"]},
      "wait_after_ms": 200
    },
    {
      "action": "type",
      "params": {"text": "github.com"},
      "wait_after_ms": 100
    },
    {
      "action": "press_key",
      "params": {"key": "enter"},
      "wait_after_ms": 3000
    },
    {
      "action": "verify_screen",
      "params": {
        "context": "Verify GitHub homepage loaded",
        "expected": "GitHub logo and navigation bar visible"
      },
      "wait_after_ms": 500,
      "description": "Checkpoint 2: GitHub loaded"
    },
    {
      "action": "verify_screen",
      "params": {
        "context": "Looking for Sign in button in top right",
        "expected": "Sign in button with dark background"
      },
      "wait_after_ms": 500,
      "description": "Checkpoint 3: Find Sign in button"
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
      "params": {"button": "left"},
      "wait_after_ms": 2000
    }
  ]
}
```

### Fallback Behavior

The system automatically handles API failures:

1. **Primary**: Gemini 2.5 Flash Live API (fast, accurate)
2. **Fallback**: gemini-flash-lite-latest (backup)
3. **Timeout**: 10 seconds per verification
4. **Error Handling**: Logs failure, returns error message

### Visual Verification Best Practices

1. **Verify Before Critical Actions**: Always verify before clicks or form submissions
2. **Use Specific Descriptions**: More detail = better accuracy
3. **Set Appropriate Confidence**: Higher for critical actions, lower for exploratory
4. **Add Wait Times**: Give UI time to stabilize before verification
5. **Test Verification Separately**: Validate descriptions work before full protocol
6. **Consider Performance**: Each verification adds ~1-3 seconds
7. **Provide Context**: Include surrounding UI elements in descriptions

---

## Macro Creation and Usage

### Overview

Macros are reusable action sequences that can be called multiple times with different parameters. They reduce duplication and make protocols more maintainable.

### Basic Macro Definition

```json
{
  "macros": {
    "macro_name": [
      {"action": "action1", "params": {}, "wait_after_ms": 0},
      {"action": "action2", "params": {}, "wait_after_ms": 0}
    ]
  }
}
```

### Using Macros

```json
{
  "action": "macro",
  "params": {"name": "macro_name"}
}
```

### Macros with Variables

**Define macro with variables:**
```json
{
  "macros": {
    "search_in_browser": [
      {
        "action": "shortcut",
        "params": {"keys": ["ctrl", "l"]},
        "wait_after_ms": 200
      },
      {
        "action": "type",
        "params": {"text": "{{query}}"},
        "wait_after_ms": 100
      },
      {
        "action": "press_key",
        "params": {"key": "enter"},
        "wait_after_ms": 3000
      }
    ]
  }
}
```

**Call macro with variables:**
```json
{
  "action": "macro",
  "params": {
    "name": "search_in_browser",
    "vars": {"query": "python tutorial"}
  }
}
```

### Multiple Variables

```json
{
  "macros": {
    "create_document": [
      {
        "action": "type",
        "params": {"text": "{{title}}"},
        "wait_after_ms": 100
      },
      {
        "action": "press_key",
        "params": {"key": "enter"},
        "wait_after_ms": 100
      },
      {
        "action": "type",
        "params": {"text": "{{content}}"},
        "wait_after_ms": 500
      },
      {
        "action": "shortcut",
        "params": {"keys": ["ctrl", "s"]},
        "wait_after_ms": 500
      },
      {
        "action": "type",
        "params": {"text": "{{filename}}"},
        "wait_after_ms": 100
      },
      {
        "action": "press_key",
        "params": {"key": "enter"},
        "wait_after_ms": 1000
      }
    ]
  }
}
```

**Usage:**
```json
{
  "action": "macro",
  "params": {
    "name": "create_document",
    "vars": {
      "title": "Meeting Notes",
      "content": "Discussion about project timeline...",
      "filename": "meeting_notes.txt"
    }
  }
}
```


### Nested Macros

Macros can call other macros:

```json
{
  "macros": {
    "focus_address_bar": [
      {
        "action": "shortcut",
        "params": {"keys": ["ctrl", "l"]},
        "wait_after_ms": 200
      }
    ],
    "navigate_to_url": [
      {
        "action": "macro",
        "params": {"name": "focus_address_bar"}
      },
      {
        "action": "type",
        "params": {"text": "{{url}}"},
        "wait_after_ms": 100
      },
      {
        "action": "press_key",
        "params": {"key": "enter"},
        "wait_after_ms": 3000
      }
    ]
  },
  "actions": [
    {
      "action": "macro",
      "params": {
        "name": "navigate_to_url",
        "vars": {"url": "github.com"}
      }
    }
  ]
}
```

### Macro Best Practices

1. **Name Descriptively**: Use clear, action-oriented names
   - ✅ `search_in_browser`, `save_and_close`, `fill_login_form`
   - ❌ `macro1`, `do_stuff`, `helper`

2. **Keep Macros Focused**: Each macro should do one logical task
   - ✅ `open_new_tab` (focused)
   - ❌ `open_tab_search_and_bookmark` (too broad)

3. **Use Variables for Flexibility**: Parameterize values that change
   ```json
   // ✅ GOOD - flexible
   {"text": "{{search_term}}"}
   
   // ❌ BAD - hardcoded
   {"text": "python tutorial"}
   ```

4. **Document Variables**: Use clear variable names
   - ✅ `{{username}}`, `{{file_path}}`, `{{button_text}}`
   - ❌ `{{x}}`, `{{val}}`, `{{temp}}`

5. **Avoid Deep Nesting**: Limit macro nesting to 2-3 levels
   ```
   ✅ GOOD: macro_a → macro_b → actions
   ❌ BAD: macro_a → macro_b → macro_c → macro_d → actions
   ```

6. **Test Macros Independently**: Verify each macro works before combining

7. **Reuse Common Patterns**: Create macros for repeated sequences
   - Opening applications
   - Navigating to URLs
   - Saving files
   - Switching windows

### Common Macro Patterns

**New Browser Tab:**
```json
"new_tab": [
  {"action": "shortcut", "params": {"keys": ["ctrl", "t"]}, "wait_after_ms": 1000}
]
```

**Focus Address Bar:**
```json
"focus_address_bar": [
  {"action": "shortcut", "params": {"keys": ["ctrl", "l"]}, "wait_after_ms": 200}
]
```

**Save File:**
```json
"save_file": [
  {"action": "shortcut", "params": {"keys": ["ctrl", "s"]}, "wait_after_ms": 500}
]
```

**Select All and Copy:**
```json
"select_all_and_copy": [
  {"action": "shortcut", "params": {"keys": ["ctrl", "a"]}, "wait_after_ms": 100},
  {"action": "shortcut", "params": {"keys": ["ctrl", "c"]}, "wait_after_ms": 100}
]
```

**Switch to Next Window:**
```json
"switch_window": [
  {"action": "shortcut", "params": {"keys": ["alt", "tab"]}, "wait_after_ms": 500}
]
```

**Close Current Tab:**
```json
"close_tab": [
  {"action": "shortcut", "params": {"keys": ["ctrl", "w"]}, "wait_after_ms": 300}
]
```

---

## Performance Optimization Tips

### 1. Minimize Wait Times

**Problem**: Excessive wait times slow execution

**Solution**: Use minimum necessary wait times

```json
// ❌ SLOW - unnecessary long waits
{"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 5000}

// ✅ FAST - appropriate wait
{"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 500}
```

**Guidelines:**
- Key presses: 50-100ms
- Shortcuts: 100-200ms
- Mouse movements: 100-200ms
- Mouse clicks: 200-500ms
- Application launches: 1000-3000ms
- Page loads: 2000-5000ms

### 2. Use Clipboard for Long Text

**Problem**: Typing long text character-by-character is slow

**Solution**: Use `paste_from_clipboard` for text >500 characters

```json
// ❌ SLOW - typing 1000 characters at 50ms each = 50 seconds
{
  "action": "type",
  "params": {"text": "Very long text content..."}
}

// ✅ FAST - paste in ~200ms
{
  "action": "paste_from_clipboard",
  "params": {"text": "Very long text content..."},
  "wait_after_ms": 200
}
```

### 3. Reduce Visual Verification Calls

**Problem**: Each verification adds 1-3 seconds

**Solution**: Only verify when necessary

```json
// ❌ SLOW - unnecessary verification
{"action": "verify_screen", "params": {...}},
{"action": "press_key", "params": {"key": "enter"}},
{"action": "verify_screen", "params": {...}},
{"action": "delay", "params": {"ms": 1000}},
{"action": "verify_screen", "params": {...}}

// ✅ FAST - verify only critical points
{"action": "verify_screen", "params": {...}},
{"action": "press_key", "params": {"key": "enter"}},
{"action": "delay", "params": {"ms": 1000}}
```

**When to verify:**
- Before clicking unknown UI elements
- After critical actions (login, submit)
- When UI state is uncertain

**When NOT to verify:**
- Between every action
- For fixed keyboard shortcuts
- For known, stable UI elements


### 4. Use Shortcuts Instead of Mouse

**Problem**: Mouse movements are slower than keyboard shortcuts

**Solution**: Prefer keyboard shortcuts when available

```json
// ❌ SLOW - mouse navigation
{"action": "mouse_move", "params": {"x": 100, "y": 50}, "wait_after_ms": 200},
{"action": "mouse_click", "params": {}, "wait_after_ms": 200},
{"action": "mouse_move", "params": {"x": 150, "y": 80}, "wait_after_ms": 200},
{"action": "mouse_click", "params": {}, "wait_after_ms": 200}

// ✅ FAST - keyboard shortcuts
{"action": "shortcut", "params": {"keys": ["ctrl", "t"]}, "wait_after_ms": 500},
{"action": "shortcut", "params": {"keys": ["ctrl", "l"]}, "wait_after_ms": 200}
```

**Common Shortcuts:**
- New tab: `Ctrl+T` (not mouse click)
- Address bar: `Ctrl+L` (not mouse click)
- Save: `Ctrl+S` (not File → Save)
- Copy: `Ctrl+C` (not right-click → Copy)
- Close: `Ctrl+W` or `Alt+F4` (not mouse click X)

### 5. Batch Similar Actions

**Problem**: Switching between action types adds overhead

**Solution**: Group similar actions together

```json
// ❌ INEFFICIENT - alternating action types
{"action": "type", "params": {"text": "hello"}},
{"action": "mouse_move", "params": {"x": 100, "y": 100}},
{"action": "type", "params": {"text": "world"}},
{"action": "mouse_move", "params": {"x": 200, "y": 200}}

// ✅ EFFICIENT - grouped actions
{"action": "type", "params": {"text": "hello"}},
{"action": "type", "params": {"text": "world"}},
{"action": "mouse_move", "params": {"x": 100, "y": 100}},
{"action": "mouse_move", "params": {"x": 200, "y": 200}}
```

### 6. Optimize Mouse Movement Speed

**Problem**: Default mouse speed may be too slow

**Solution**: Increase speed parameter for non-critical movements

```json
// ❌ SLOW - default speed
{"action": "mouse_move", "params": {"x": 1000, "y": 800}, "wait_after_ms": 500}

// ✅ FAST - increased speed
{
  "action": "mouse_move",
  "params": {"x": 1000, "y": 800, "speed": 2.0},
  "wait_after_ms": 200
}
```

**Speed Guidelines:**
- 0.5: Very slow, precise movements
- 1.0: Default, natural speed
- 1.5-2.0: Fast, for non-critical movements
- 3.0+: Very fast, may look unnatural

### 7. Use Macros to Reduce Duplication

**Problem**: Repeated action sequences increase protocol size and execution time

**Solution**: Extract repeated patterns into macros

```json
// ❌ SLOW - repeated sequences
{"action": "shortcut", "params": {"keys": ["ctrl", "l"]}},
{"action": "type", "params": {"text": "site1.com"}},
{"action": "press_key", "params": {"key": "enter"}},
{"action": "delay", "params": {"ms": 3000}},
{"action": "shortcut", "params": {"keys": ["ctrl", "t"]}},
{"action": "shortcut", "params": {"keys": ["ctrl", "l"]}},
{"action": "type", "params": {"text": "site2.com"}},
{"action": "press_key", "params": {"key": "enter"}},
{"action": "delay", "params": {"ms": 3000}}

// ✅ FAST - using macros
{
  "macros": {
    "navigate": [
      {"action": "shortcut", "params": {"keys": ["ctrl", "l"]}, "wait_after_ms": 200},
      {"action": "type", "params": {"text": "{{url}}"}, "wait_after_ms": 100},
      {"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 3000}
    ]
  },
  "actions": [
    {"action": "macro", "params": {"name": "navigate", "vars": {"url": "site1.com"}}},
    {"action": "shortcut", "params": {"keys": ["ctrl", "t"]}, "wait_after_ms": 500},
    {"action": "macro", "params": {"name": "navigate", "vars": {"url": "site2.com"}}}
  ]
}
```

### 8. Disable Smooth Mouse When Not Needed

**Problem**: Smooth mouse movements add overhead

**Solution**: Use straight movements for non-visible actions

```json
// ❌ SLOWER - smooth movement when not needed
{
  "action": "mouse_move",
  "params": {"x": 500, "y": 300, "smooth": true},
  "wait_after_ms": 200
}

// ✅ FASTER - straight movement
{
  "action": "mouse_move",
  "params": {"x": 500, "y": 300, "smooth": false},
  "wait_after_ms": 100
}
```

**When to use smooth:**
- User-visible actions
- Recording demonstrations
- Natural-looking automation

**When to use straight:**
- Background automation
- Performance-critical workflows
- Non-visible movements

### 9. Parallel Execution Considerations

**Problem**: Sequential execution can be slow

**Solution**: Structure protocols to minimize dependencies

```json
// ❌ SLOW - unnecessary sequential dependencies
{"action": "open_app", "params": {"app_name": "chrome"}, "wait_after_ms": 3000},
{"action": "delay", "params": {"ms": 2000}},
{"action": "verify_screen", "params": {...}, "wait_after_ms": 1000}

// ✅ FAST - optimized timing
{"action": "open_app", "params": {"app_name": "chrome"}, "wait_after_ms": 2000},
{"action": "verify_screen", "params": {...}, "wait_after_ms": 500}
```

### 10. Profile and Measure

**Problem**: Don't know which actions are slow

**Solution**: Use execution logging to identify bottlenecks

```python
# Enable detailed logging
executor = ProtocolExecutor(log_level="DEBUG")
result = executor.execute(protocol)

# Review timing for each action
for action_result in result['actions']:
    print(f"{action_result['action']}: {action_result['duration_ms']}ms")
```

**Optimization Workflow:**
1. Run protocol with logging enabled
2. Identify slowest actions
3. Optimize those specific actions
4. Re-test and measure improvement
5. Repeat until performance is acceptable

### Performance Checklist

- [ ] Wait times are minimal but sufficient
- [ ] Long text uses clipboard paste
- [ ] Visual verification only where needed
- [ ] Keyboard shortcuts used instead of mouse when possible
- [ ] Similar actions are batched together
- [ ] Mouse speed optimized for use case
- [ ] Repeated sequences extracted to macros
- [ ] Smooth mouse disabled for non-visible actions
- [ ] No unnecessary delays or verification
- [ ] Protocol profiled and bottlenecks identified

---

## Summary

This documentation covers:

1. **Protocol Schema**: Complete structure and validation rules
2. **Troubleshooting**: Common issues and solutions
3. **Visual Verification**: When and how to use AI vision
4. **Macros**: Creating reusable action sequences
5. **Performance**: Optimization techniques for faster execution

For more information, see:
- [Action Library Reference](ACTION_LIBRARY_REFERENCE.md)
- [Protocol Examples](../examples/protocols/README.md)
- [Protocol Parser Documentation](../shared/PROTOCOL_PARSER_README.md)
- [Protocol Executor Documentation](../shared/PROTOCOL_EXECUTOR_README.md)
- [Visual Verification Documentation](../shared/VISUAL_VERIFICATION_README.md)

