# Task 15: Visual Navigate Parameter Fix

## Issues Found

### Issue 1: Misleading Dev Mode Message

**Problem:** The log showed:
```
Using ultra-fast models (no pro in dev mode)
...
Switched to complex model: gemini-2.5-pro
```

This was confusing - it said "no pro in dev mode" but then appeared to switch to the pro model.

**Root Cause:** The print statement was outside the `if self.use_ultra_fast` check, so it printed "Switched to complex model: gemini-2.5-pro" even though the actual model being used was `gemini-2.5-flash` (the fast model, not pro).

**Fix:** Updated the print statement to be inside the mode check and clarify that dev mode doesn't use pro:
```python
if self.use_ultra_fast:
    if complexity == 'complex':
        print(f"  ⚡⚡ DEV MODE - Complex task: Using {target_model} (no pro in dev mode)")
    else:
        print(f"  ⚡⚡⚡ DEV MODE - Simple task: Using {target_model}")
```

### Issue 2: visual_navigate Parameter Mismatch

**Problem:** The automation failed with:
```
ERROR: Action 3 (visual_navigate) failed: visual_navigate action requires 'task' parameter
Error details: {'params': {'target_description': "the 'What is happening?!' compose post input field", 'action_type': 'click'}}
```

**Root Cause:** The AI was generating protocols with `target_description` and `action_type` parameters because that's what the examples showed. However, the actual `visual_navigate` action handler expects a `task` parameter.

**The Mismatch:**
- **AI was generating:** `{"action": "visual_navigate", "params": {"target_description": "...", "action_type": "click"}}`
- **Action handler expects:** `{"action": "visual_navigate", "params": {"task": "Click the ..."}}`

## Solution

Updated all `visual_navigate` examples in `ai_brain/gemini_client.py` to use the correct `task` parameter.

### Changes Made

#### 1. Example 3 (Twitter Posting)

**Before:**
```json
{"action": "visual_navigate", "params": {"target_description": "the 'What's happening?' post compose input field", "action_type": "click"}}
```

**After:**
```json
{"action": "visual_navigate", "params": {"task": "Click the 'What's happening?' post compose input field"}}
```

#### 2. Example 4 (Visual Navigation)

**Before:**
```json
{"action": "visual_navigate", "params": {"target_description": "the blue Login button", "action_type": "click"}}
```

**After:**
```json
{"action": "visual_navigate", "params": {"task": "Click the blue Login button"}}
```

#### 3. Rule #3 (Visual Navigation)

**Before:**
```
Example: {"action": "visual_navigate", "params": {"target_description": "the blue Login button", "action_type": "click"}}
```

**After:**
```
Example: {"action": "visual_navigate", "params": {"task": "Click the blue Login button"}}
The "task" parameter should describe what to do (e.g., "Click the submit button", "Find and click the search icon")
```

#### 4. Simpler Prompt Template

**Before:**
```json
{"action": "visual_navigate", "params": {"target_description": "the 'What's happening?' post compose input field", "action_type": "click"}}
```

**After:**
```json
{"action": "visual_navigate", "params": {"task": "Click the 'What's happening?' post compose input field"}}
```

#### 5. Social Media Instructions

**Before:**
```
Use visual_navigate to find and click compose area
```

**After:**
```
Use visual_navigate with task="Click the compose area" to find and click compose area
IMPORTANT: visual_navigate requires a "task" parameter describing what to do
```

## visual_navigate Action Parameters

The `visual_navigate` action accepts these parameters:

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `task` | ✅ Yes | Description of what to do | "Click the submit button" |
| `goal` | ❌ No | Optional goal (defaults to task) | "Submit the form" |
| `max_iterations` | ❌ No | Max attempts (default: 10) | 5 |
| `fallback_coordinates` | ❌ No | Fallback if vision fails | {"x": 500, "y": 300} |
| `timeout` | ❌ No | Timeout in seconds (default: 60) | 30 |

### Correct Usage Examples

```json
// Simple click
{"action": "visual_navigate", "params": {"task": "Click the login button"}}

// With goal
{"action": "visual_navigate", "params": {"task": "Click the submit button", "goal": "Submit the registration form"}}

// With fallback
{"action": "visual_navigate", "params": {"task": "Click the search icon", "fallback_coordinates": {"x": 100, "y": 50}}}

// With max iterations
{"action": "visual_navigate", "params": {"task": "Find and click the next button", "max_iterations": 5}}
```

### Incorrect Usage (Will Fail)

```json
// ❌ Wrong: Using target_description and action_type
{"action": "visual_navigate", "params": {"target_description": "the button", "action_type": "click"}}

// ❌ Wrong: Missing task parameter
{"action": "visual_navigate", "params": {"goal": "Click button"}}

// ❌ Wrong: Using description instead of task
{"action": "visual_navigate", "params": {"description": "Click the button"}}
```

## Testing

After this fix, the AI should generate protocols with the correct `task` parameter:

```json
{
  "version": "1.0",
  "metadata": {
    "description": "Post a CSS joke on X",
    "complexity": "medium",
    "uses_vision": true
  },
  "actions": [
    {"action": "open_app", "params": {"app_name": "chrome"}, "wait_after_ms": 2000},
    {"action": "shortcut", "params": {"keys": ["ctrl", "l"]}, "wait_after_ms": 200},
    {"action": "type", "params": {"text": "x.com"}, "wait_after_ms": 100},
    {"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 3000},
    {"action": "visual_navigate", "params": {"task": "Click the 'What's happening?' post compose input field"}, "wait_after_ms": 500},
    {"action": "type", "params": {"text": "Why do CSS developers prefer dark mode? Because light attracts bugs! 🐛💡 #CSS #WebDev"}, "wait_after_ms": 1000},
    {"action": "visual_navigate", "params": {"task": "Click the blue 'Post' button to publish the tweet"}, "wait_after_ms": 2000}
  ]
}
```

## Impact

This fix ensures:
- ✅ AI generates protocols with correct parameter names
- ✅ visual_navigate actions execute successfully
- ✅ No more "requires 'task' parameter" errors
- ✅ Consistent parameter naming across all examples
- ✅ Clear documentation of what parameters are required

## Files Modified

- `ai_brain/gemini_client.py` - Updated all visual_navigate examples and instructions

## Related Documentation

- `docs/VISUAL_NAVIGATE_QUICK_REFERENCE.md` - Visual navigate action reference
- `docs/VISUAL_NAVIGATE_PROTOCOL_ACTION.md` - Protocol action documentation
- `docs/TASK14_VERIFY_SCREEN_FIX_SUMMARY.md` - Previous fix that introduced visual_navigate usage
