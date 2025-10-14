# Verify Screen Variable Substitution Fix

## Problem

The automation was failing with this error:
```
Missing required variables in context: verified_x. 
Available variables: suggested_actions, last_verification_safe, last_verification_confidence, last_verification_analysis. 
Hint: Variables like 'verified_x' and 'verified_y' come from 'verify_screen' action results.
```

### Root Cause

The AI was generating protocols with this pattern:
```json
{
  "actions": [
    {"action": "verify_screen", "params": {...}},
    {"action": "mouse_move", "params": {"x": "{{verified_x}}", "y": "{{verified_y}}"}},
    {"action": "mouse_click", ...}
  ]
}
```

**The issue:** When `verify_screen` determines the screen state is NOT SAFE (e.g., page still loading, element not visible, window blocking), it only sets these variables:
- `last_verification_safe` (False)
- `last_verification_confidence`
- `last_verification_analysis`
- `suggested_actions`

It does NOT set `verified_x` and `verified_y` because it didn't successfully find the target element.

The subsequent `mouse_move` action tries to use `{{verified_x}}` and `{{verified_y}}`, which don't exist → ERROR.

## Solution

Updated the protocol generation prompts in `ai_brain/gemini_client.py` to instruct the AI to use `visual_navigate` instead of the `verify_screen` + `mouse_move` + `mouse_click` pattern.

### Before (Problematic Pattern)
```json
{
  "actions": [
    {"action": "verify_screen", "params": {"context": "Looking for button", "expected": "Button visible"}},
    {"action": "mouse_move", "params": {"x": "{{verified_x}}", "y": "{{verified_y}}"}},
    {"action": "mouse_click", "params": {"button": "left"}}
  ]
}
```

### After (Fixed Pattern)
```json
{
  "actions": [
    {"action": "visual_navigate", "params": {"target_description": "the blue Login button", "action_type": "click"}}
  ]
}
```

## Why This Works

The `visual_navigate` action:
1. Handles verification internally
2. Automatically retries if the element isn't found
3. Gracefully handles failures without exposing variable substitution issues
4. Combines find + click into a single atomic operation
5. Provides better error messages

## Changes Made

### 1. Updated Main Prompt Template
- Changed Example 3 (Twitter post) to use `visual_navigate`
- Changed Example 4 to demonstrate `visual_navigate` usage
- Updated rule #3 to emphasize using `visual_navigate` for UI interactions

### 2. Updated Simpler Prompt Template
- Changed the example format to use `visual_navigate` instead of `verify_screen` + `mouse_move` + `mouse_click`

### 3. Updated Critical Requirements
- Modified social media posting instructions to use `visual_navigate`
- Added explicit warning against using `verify_screen` + `mouse_move` pattern

## When to Use Each Action

### Use `visual_navigate`
- When you need to find AND click/interact with a UI element
- For buttons, links, input fields, etc.
- Example: "Click the Post button", "Click the compose area"

### Use `verify_screen`
- When you only need to CHECK if something is visible (no interaction)
- For validation/confirmation without clicking
- Example: "Verify the page loaded", "Check if login was successful"
- **NEVER** follow with `mouse_move` using `{{verified_x}}` and `{{verified_y}}`

## Testing

After this fix, the AI should generate protocols that:
1. Use `visual_navigate` for all UI interactions
2. Only use `verify_screen` for state validation (without subsequent mouse actions)
3. Handle page loading and UI state issues gracefully
4. Complete workflows successfully even when elements take time to appear

## Example: Twitter Posting (Fixed)

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
    {"action": "visual_navigate", "params": {"target_description": "the 'What's happening?' post compose input field", "action_type": "click"}, "wait_after_ms": 500},
    {"action": "type", "params": {"text": "Why do CSS developers prefer dark mode? Because light attracts bugs! 🐛💡 #CSS #WebDev #DeveloperHumor"}, "wait_after_ms": 1000},
    {"action": "visual_navigate", "params": {"target_description": "the blue 'Post' button to publish the tweet", "action_type": "click"}, "wait_after_ms": 2000}
  ]
}
```

This protocol will:
- Wait for the page to load
- Find the compose area even if it takes time to appear
- Handle any UI state issues gracefully
- Complete the posting workflow successfully
