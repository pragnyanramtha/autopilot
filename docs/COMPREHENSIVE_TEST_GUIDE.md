# Comprehensive Automation Test Guide

## Overview

The comprehensive test (`examples/protocols/comprehensive_test.json`) exercises ALL automation features without making any API calls.

## What It Tests

### 1. **Keyboard Typing** ✅
- Types multiple lines of text
- Tests special characters and symbols
- Verifies text input works correctly

### 2. **Keyboard Shortcuts** ✅
- `Ctrl+A` - Select all
- `Ctrl+C` - Copy
- `Ctrl+T` - New tab
- `Ctrl+L` - Address bar
- `Ctrl+W` - Close tab
- `Ctrl+Shift+T` - Reopen closed tab
- `Alt+F4` - Close window
- Arrow keys and special keys

### 3. **Mouse Movement** ✅
- Smooth mouse movement
- Draws a square on screen
- Tests different speeds and paths
- Demonstrates precise control

### 4. **Mouse Clicks** ✅
- Single left click
- Double click
- Click at specific coordinates
- Tests click accuracy

### 5. **Browser Automation** ✅
- Opens Chrome
- Navigates to multiple URLs:
  - github.com
  - stackoverflow.com
  - python.org
- Opens new tabs
- Closes tabs
- Reopens closed tabs
- Closes browser

### 6. **Macros with Variables** ✅
- `open_new_tab` - Reusable tab opening
- `navigate_to_url` - URL navigation with variable substitution
- `close_tab` - Tab closing
- Tests variable substitution (`{{url}}`)

### 7. **Application Control** ✅
- Opens Notepad
- Opens Chrome
- Switches between applications
- Closes applications

## Test Sequence

```
1. Open Notepad
2. Type test header
3. Test keyboard typing
4. Test keyboard shortcuts (Ctrl+A, Ctrl+C)
5. Test mouse movement (draw square)
6. Open Chrome
7. Navigate to GitHub
8. Open new tab → Navigate to Stack Overflow
9. Open new tab → Navigate to Python.org
10. Reopen closed tab
11. Close all tabs
12. Close browser
13. Return to Notepad
14. Report all tests passed
```

## Running the Test

### Option 1: With Mock Actions (Safe, No Actual Automation)
```bash
python test_automation_engine_only.py
```
- Simulates all actions
- Shows what would happen
- Zero risk
- Zero API calls

### Option 2: With Real Actions (Actually Works!)
```bash
python test_automation_engine_real.py
```
- **⚠️ Actually moves mouse and types!**
- Opens real applications
- Performs real automation
- Zero API calls (uses pre-made protocol)

## What You'll See

### Console Output
```
============================================================
AUTOMATION ENGINE REAL TEST
============================================================

⚠️  WARNING: This uses REAL automation!

Do you want to continue? (yes/no): yes

Starting in 3 seconds...
Move your mouse to interrupt!
============================================================

✓ Real action handlers registered
Loading protocol from: examples/protocols/comprehensive_test.json

Protocol loaded:
  Description: Comprehensive automation test - exercises all features
  Actions: 70+
  Macros: 3
  Complexity: complex

🚀 Executing protocol with REAL actions...

[1/70] Executing: open_app
  Parameters: {'app_name': 'notepad'}
[2/70] Executing: type
  Parameters: {'text': '=== AUTOMATION ENGINE COMPREHENSIVE TEST ==='}
...
```

### On Your Screen
1. **Notepad opens** and text appears
2. **Mouse moves** in a square pattern
3. **Chrome opens** and navigates to websites
4. **Tabs open and close** automatically
5. **Back to Notepad** with test results

## Duration

- **Mock test:** ~30 seconds
- **Real test:** ~60-90 seconds (depends on browser load times)

## Safety Features

1. **Confirmation required** - Must type "yes" to proceed
2. **3-second countdown** - Time to cancel
3. **Mouse interrupt** - Move mouse to stop
4. **No destructive actions** - Only opens/closes apps
5. **No API calls** - Zero cost

## What It Proves

✅ **Protocol parsing** works  
✅ **Action execution** works  
✅ **Macro expansion** works  
✅ **Variable substitution** works  
✅ **Mouse control** works  
✅ **Keyboard control** works  
✅ **Application control** works  
✅ **Browser automation** works  
✅ **Timing and delays** work  
✅ **Error handling** works  

## Customization

Edit `examples/protocols/comprehensive_test.json` to:
- Add more tests
- Change URLs
- Modify timing
- Add your own macros
- Test different applications

## Troubleshooting

### Browser doesn't open
- Make sure Chrome is installed
- Change `"app_name": "chrome"` to `"msedge"` for Edge

### Mouse moves too fast
- Increase `duration_ms` in mouse_move actions
- Add longer `wait_after_ms` delays

### Actions happen too quickly
- Increase `wait_after_ms` values
- Add `wait` actions between steps

### Test interrupted
- Don't move your mouse during execution
- Close other applications
- Run in a clean environment

## Files

- `examples/protocols/comprehensive_test.json` - The test protocol
- `test_automation_engine_real.py` - Real automation runner
- `test_automation_engine_only.py` - Mock automation runner
- `docs/COMPREHENSIVE_TEST_GUIDE.md` - This guide

## Summary

This comprehensive test demonstrates that the automation engine can:
- Execute complex workflows
- Control mouse and keyboard
- Automate browser interactions
- Use macros and variables
- Handle timing and delays
- Provide detailed logging

**All without a single API call!** 🎉
