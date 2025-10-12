# Variable Substitution Fix

## Issue
When protocols used vision-based actions with template variables like `{{verified_x}}` and `{{verified_y}}`, the execution failed with:
```
ERROR: Action 4 (mouse_move) failed: Error executing action 'mouse_move': [Errno 2] No such file or directory: '{{verified_x}}'
```

## Root Causes

### Cause #1: Missing Variables Not Detected
The variable substitution code was silently keeping the original `{{variable}}` string when a variable wasn't found in the context, leading to downstream errors when actions tried to use the unsubstituted string.

### Cause #2: Visual Verifier Not Initialized
The automation engine wasn't initializing the `VisualVerifier` component, so `verify_screen` actions were returning fallback responses without coordinates, meaning `verified_x` and `verified_y` were never set in the execution context.

## Solutions

### Solution #1: Fail Fast on Missing Variables
Updated `shared/protocol_executor.py` to raise a clear error when required variables are missing:

```python
def _substitute_variables_in_dict(self, data: Dict[str, Any], variables: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively substitute variables in a dictionary."""
    import re
    
    result = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            pattern = r'\{\{(\w+)\}\}'
            
            # Check if there are any variables to substitute
            matches = re.findall(pattern, value)
            if matches:
                # Check if all variables exist
                missing_vars = [var for var in matches if var not in variables]
                if missing_vars:
                    raise ValueError(
                        f"Missing required variables in context: {', '.join(missing_vars)}. "
                        f"Available variables: {', '.join(variables.keys()) if variables else 'none'}. "
                        f"Hint: Variables like 'verified_x' and 'verified_y' come from 'verify_screen' action results."
                    )
            
            def replace_var(match):
                var_name = match.group(1)
                return str(variables[var_name])
            
            result[key] = re.sub(pattern, replace_var, value)
            # ... rest of method
```

**Benefits:**
- Clear error messages when variables are missing
- Helpful hints about where variables come from
- Lists available variables for debugging

### Solution #2: Initialize Visual Verifier
Updated `automation_engine/main.py` to properly initialize all dependencies:

```python
def __init__(self, config_path: str = "config.json", dry_run: bool = False):
    """Initialize the Automation Engine application."""
    self.config = self._load_config(config_path)
    self.dry_run = dry_run
    
    # Initialize core components
    self.action_registry = ActionRegistry()
    
    # Initialize dependencies for action handlers
    from automation_engine.input_controller import InputController
    from automation_engine.mouse_controller import MouseController
    from shared.screen_capture import ScreenCapture
    from shared.visual_verifier import VisualVerifier
    
    input_controller = InputController()
    mouse_controller = MouseController()
    screen_capture = ScreenCapture()
    
    # Initialize visual verifier with Gemini API key
    import os
    api_key = os.getenv('GEMINI_API_KEY')
    visual_verifier = None
    if api_key:
        try:
            visual_verifier = VisualVerifier(
                api_key=api_key,
                screen_capture=screen_capture
            )
            print("✓ Visual verifier initialized")
        except Exception as e:
            print(f"⚠ Visual verifier initialization failed: {e}")
            print("  Vision-based actions will use fallback behavior")
    else:
        print("⚠ GEMINI_API_KEY not found - vision features disabled")
    
    # Inject dependencies into action registry
    self.action_registry.inject_dependencies(
        input_controller=input_controller,
        mouse_controller=mouse_controller,
        screen_capture=screen_capture,
        visual_verifier=visual_verifier
    )
    
    # Register all action handlers
    from shared.action_handlers import ActionHandlers
    action_handlers = ActionHandlers(self.action_registry)
    action_handlers.register_all()
    # ... rest of initialization
```

**Benefits:**
- Visual verification now works properly
- `verify_screen` returns actual coordinates from AI analysis
- Variables `verified_x` and `verified_y` are set correctly
- Graceful fallback if visual verifier can't be initialized

## How Variable Substitution Works

1. **Action with variables**: Protocol contains action like:
   ```json
   {"action": "mouse_move", "params": {"x": "{{verified_x}}", "y": "{{verified_y}}"}}
   ```

2. **verify_screen sets variables**: When `verify_screen` executes:
   - Captures screenshot
   - Sends to Gemini vision AI
   - AI analyzes and returns coordinates
   - Coordinates stored in context: `verified_x=500, verified_y=300`

3. **Substitution happens**: Before executing `mouse_move`:
   - Checks if `verified_x` and `verified_y` exist in context
   - If yes: substitutes → `{"x": "500", "y": "300"}`
   - If no: raises clear error with helpful message

4. **Action executes**: `mouse_move` receives actual coordinates

## What This Fixes
- ✅ Clear error messages when variables are missing
- ✅ Visual verifier properly initialized
- ✅ `verify_screen` returns actual AI-analyzed coordinates
- ✅ Template variables `{{verified_x}}` and `{{verified_y}}` work correctly
- ✅ Vision-based protocols can execute successfully

## Testing
1. Restart the automation engine to pick up changes
2. Try a vision-based command like "search for X"
3. The `verify_screen` action should now:
   - Capture screenshot
   - Analyze with Gemini vision
   - Return coordinates
   - Store them in context
4. Subsequent actions using `{{verified_x}}` should work

## Files Modified
- `shared/protocol_executor.py` - Better error handling for missing variables
- `automation_engine/main.py` - Initialize visual verifier and dependencies

## Related Documentation
- `docs/PROTOCOL_GENERATOR_FIX.md` - AI Brain fixes
- `docs/AUTOMATION_ENGINE_FIX.md` - Action registration fix
- `shared/VISUAL_VERIFICATION_README.md` - Visual verification system
