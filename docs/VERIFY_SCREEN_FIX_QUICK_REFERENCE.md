# Verify Screen Fix - Quick Reference

## The Problem
```
ERROR: Missing required variables in context: verified_x
```

When `verify_screen` fails (returns NOT SAFE), it doesn't provide `verified_x` and `verified_y` coordinates, causing subsequent `mouse_move` actions to fail.

## The Solution

**Use `visual_navigate` instead of `verify_screen` + `mouse_move` + `mouse_click`**

### ❌ DON'T DO THIS (Old Pattern)
```json
{
  "actions": [
    {"action": "verify_screen", "params": {"context": "Looking for button", "expected": "Button visible"}},
    {"action": "mouse_move", "params": {"x": "{{verified_x}}", "y": "{{verified_y}}"}},
    {"action": "mouse_click", "params": {"button": "left"}}
  ]
}
```

### ✅ DO THIS (Fixed Pattern)
```json
{
  "actions": [
    {"action": "visual_navigate", "params": {"task": "Click the blue Login button"}}
  ]
}
```

## When to Use Each Action

| Action | Use Case | Example |
|--------|----------|---------|
| `visual_navigate` | Find AND interact with UI elements | Click button, click input field |
| `verify_screen` | Check state WITHOUT interaction | Verify page loaded, confirm success |

## Key Changes Made

1. **Updated prompt templates** in `ai_brain/gemini_client.py`
2. **Changed examples** to use `visual_navigate`
3. **Added explicit warnings** against the old pattern

## Benefits

- ✅ No more variable substitution errors
- ✅ Automatic retry on element not found
- ✅ Graceful handling of page loading
- ✅ Simpler, more reliable protocols
- ✅ Better error messages

## Testing

Run the validation test:
```bash
python tests/test_verify_screen_fix.py
```

This will verify that new protocols use the correct pattern.
