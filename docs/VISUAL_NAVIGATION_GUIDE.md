# Visual Navigation System - User Guide

## Overview

The Visual Navigation System enables the AI Brain to make intelligent, context-aware decisions about mouse movements and clicks by analyzing real-time screenshots. Instead of relying solely on predefined coordinates, the system uses vision-capable AI models (Gemini with vision) to understand the screen context and determine optimal interaction points.

This creates an adaptive automation system that can:
- Handle dynamic UIs that change layout or position
- Adapt to different screen resolutions
- Recover from unexpected interface changes
- Navigate complex multi-step workflows with visual verification

## How It Works

The system operates in an iterative feedback loop:

1. **Capture** - Take a screenshot of the current screen and mouse position
2. **Analyze** - AI vision model analyzes the screen and determines where to click
3. **Execute** - Automation engine moves mouse and performs the action
4. **Verify** - Capture new screenshot to verify the action succeeded
5. **Continue or Complete** - AI decides if more actions are needed or workflow is done

## Configuration

### Basic Configuration

Add the following section to your `config.json`:

```json
{
  "visual_navigation": {
    "enabled": true,
    "vision_model": "gemini-2.0-flash-exp",
    "vision_model_dev": "gemini-2.0-flash-exp",
    "max_iterations": 10,
    "iteration_timeout_seconds": 30,
    "confidence_threshold": 0.6,
    "require_confirmation_for_critical": true,
    "critical_keywords": ["delete", "format", "shutdown", "remove", "erase"],
    "loop_detection_threshold": 3,
    "screenshot_quality": 85,
    "enable_audit_log": true,
    "audit_log_path": "logs/visual_navigation_audit.json"
  }
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable/disable visual navigation system |
| `vision_model` | string | `"gemini-2.0-flash-exp"` | Vision-capable model for production |
| `vision_model_dev` | string | `"gemini-2.0-flash-exp"` | Vision-capable model for dev mode |
| `max_iterations` | integer | `10` | Maximum consecutive actions before requiring approval |
| `iteration_timeout_seconds` | integer | `30` | Timeout per iteration in seconds |
| `confidence_threshold` | float | `0.6` | Minimum confidence (0.0-1.0) to execute action |
| `require_confirmation_for_critical` | boolean | `true` | Require user confirmation for critical actions |
| `critical_keywords` | array | See above | Keywords that trigger confirmation prompts |
| `loop_detection_threshold` | integer | `3` | Number of repeated clicks before halting |
| `screenshot_quality` | integer | `85` | JPEG quality for screenshot compression (1-100) |
| `enable_audit_log` | boolean | `true` | Enable audit logging of all actions |
| `audit_log_path` | string | `"logs/visual_navigation_audit.json"` | Path to audit log file |

### Model Selection

The system requires a vision-capable AI model. Supported models:
- `gemini-2.0-flash-exp` (recommended for speed)
- `gemini-1.5-pro` (for complex scenarios)
- `gemini-1.5-flash` (balanced option)

**Dev Mode**: When running in dev mode, the system uses `vision_model_dev` instead of `vision_model`, allowing you to use faster/cheaper models during development.

## Usage

### Method 1: Protocol-Based Visual Navigation

Create a protocol file with the `visual_navigate` action:

```json
{
  "name": "Login Workflow",
  "description": "Use AI vision to navigate login page",
  "actions": [
    {
      "action": "visual_navigate",
      "description": "Navigate to login page and click login button",
      "parameters": {
        "task": "Click the login button",
        "goal": "Navigate to login page",
        "max_iterations": 5,
        "fallback_coordinates": [500, 300]
      }
    }
  ]
}
```

**Parameters**:
- `task` (required): Description of what to click or interact with
- `goal` (optional): Overall workflow goal for context
- `max_iterations` (optional): Override default max iterations
- `fallback_coordinates` (optional): Coordinates to use if visual navigation fails

### Method 2: Voice Command

Simply speak a command that requires visual navigation:

```
"Click the submit button"
"Navigate to settings and enable dark mode"
"Find and click the download link"
```

The AI Brain will automatically detect when visual navigation is needed and initiate the workflow.

### Method 3: Programmatic Usage

```python
from ai_brain.vision_navigator import VisionNavigator
from ai_brain.gemini_client import GeminiClient

# Initialize
gemini_client = GeminiClient(config)
navigator = VisionNavigator(gemini_client, config)

# Analyze screen
result = navigator.analyze_screen_for_action(
    screenshot=screenshot_image,
    current_mouse_pos=(100, 200),
    task_description="Click the submit button",
    screen_size=(1920, 1080)
)

# Execute action based on result
if result.action == 'click':
    mouse_controller.move_to(result.coordinates)
    mouse_controller.click()
```

## Examples

### Example 1: Simple Button Click

**Protocol**:
```json
{
  "action": "visual_navigate",
  "description": "Click submit button",
  "parameters": {
    "task": "Click the submit button on the form"
  }
}
```

**What happens**:
1. AI captures screenshot
2. AI identifies submit button location
3. Mouse moves to button
4. Click is performed
5. New screenshot verifies button was clicked

### Example 2: Multi-Step Navigation

**Protocol**:
```json
{
  "action": "visual_navigate",
  "description": "Navigate to settings",
  "parameters": {
    "task": "Open settings menu and enable dark mode",
    "goal": "Enable dark mode in settings",
    "max_iterations": 8
  }
}
```

**What happens**:
1. AI finds and clicks settings icon
2. Verifies settings menu opened
3. AI finds dark mode toggle
4. Clicks toggle
5. Verifies dark mode is enabled
6. Workflow completes

### Example 3: With Fallback Coordinates

**Protocol**:
```json
{
  "action": "visual_navigate",
  "description": "Click login with fallback",
  "parameters": {
    "task": "Click the login button",
    "fallback_coordinates": [960, 540]
  }
}
```

**What happens**:
- AI attempts visual navigation first
- If vision fails (API error, low confidence, etc.), uses fallback coordinates
- Ensures workflow continues even if vision is unavailable

## Safety Features

### 1. Critical Action Confirmation

The system detects potentially dangerous actions and requires user confirmation:

**Critical Keywords**:
- delete, remove, erase
- format, wipe
- shutdown, restart, reboot
- uninstall, destroy

**Example**:
```
AI: "I need to click the 'Delete All' button. This is a critical action. Confirm? (y/n)"
User: "y"
AI: "Proceeding with action..."
```

### 2. Loop Detection

If the AI clicks the same coordinates 3+ times, the system halts execution:

```
Warning: Loop detected - clicked (500, 300) 3 times. Halting execution.
```

This prevents infinite loops when the AI can't complete a task.

### 3. Iteration Limits

Maximum consecutive actions is limited (default: 10):

```
Warning: Max iterations (10) reached. Workflow incomplete.
```

User approval is required to continue beyond the limit.

### 4. Coordinate Validation

All coordinates are validated before execution:
- Must be within screen bounds
- Slightly out-of-bounds coordinates are clamped
- Severely invalid coordinates are rejected

### 5. Audit Logging

When enabled, all actions are logged with:
- Timestamp
- Screenshot (saved to disk)
- Mouse position before/after
- Action taken and coordinates
- AI's confidence and reasoning
- Success/failure status

**Audit Log Location**: `logs/visual_navigation_audit.json`

## Limitations

### Current Limitations

1. **Single Monitor Only**
   - Currently supports primary monitor only
   - Multi-monitor support planned for future release

2. **Performance**
   - Each action takes 2-4 seconds (API latency)
   - Multi-step workflows can take 10-20 seconds
   - Faster models reduce latency but may have lower accuracy

3. **Complex UIs**
   - May struggle with very cluttered interfaces
   - Overlapping elements can cause confusion
   - Small UI elements (<20px) may be hard to detect

4. **Dynamic Content**
   - Animations and loading states can cause issues
   - Rapidly changing content may confuse the AI
   - Use `wait` actions before visual navigation for dynamic pages

5. **Text Input**
   - Currently limited to mouse actions (click, double-click, right-click)
   - Keyboard input support is basic
   - Complex text entry may require protocol-based typing

### Best Practices

1. **Be Specific**: Provide clear, specific task descriptions
   - Good: "Click the blue 'Submit' button in the bottom right"
   - Bad: "Click something"

2. **Use Fallbacks**: Always provide fallback coordinates for critical workflows
   ```json
   {
     "task": "Click login",
     "fallback_coordinates": [960, 540]
   }
   ```

3. **Set Appropriate Limits**: Adjust `max_iterations` based on workflow complexity
   - Simple tasks: 3-5 iterations
   - Complex navigation: 8-12 iterations

4. **Wait for Stability**: Use `wait` actions before visual navigation
   ```json
   [
     {"action": "wait", "parameters": {"seconds": 2}},
     {"action": "visual_navigate", "parameters": {"task": "Click button"}}
   ]
   ```

5. **Monitor Audit Logs**: Review logs regularly to identify issues
   - Check for low confidence actions
   - Look for repeated failures
   - Identify UI elements that cause problems

## Troubleshooting

### Issue: "Vision model API failure"

**Symptoms**: Error message about API failure, retries exhausted

**Solutions**:
1. Check internet connection
2. Verify API key is valid in `.env` file
3. Check Gemini API status: https://status.cloud.google.com/
4. Reduce `screenshot_quality` to decrease payload size
5. Try a different vision model in config

### Issue: "Low confidence - action skipped"

**Symptoms**: AI reports low confidence, doesn't execute action

**Solutions**:
1. Make task description more specific
2. Ensure UI element is clearly visible (not obscured)
3. Lower `confidence_threshold` in config (carefully!)
4. Use fallback coordinates for critical actions
5. Simplify the UI or zoom in on target element

### Issue: "Loop detected - halting execution"

**Symptoms**: Same coordinates clicked multiple times, execution stops

**Solutions**:
1. Check if UI element is actually clickable
2. Verify element doesn't require double-click or right-click
3. Add `wait` action to allow UI to respond
4. Use protocol-based action instead of visual navigation
5. Increase `loop_detection_threshold` (not recommended)

### Issue: "Max iterations reached"

**Symptoms**: Workflow stops after 10 actions, incomplete

**Solutions**:
1. Increase `max_iterations` in config or protocol
2. Break workflow into smaller sub-tasks
3. Use protocol-based actions for known steps
4. Simplify the workflow goal
5. Check audit log to see where it's getting stuck

### Issue: "Coordinates out of bounds"

**Symptoms**: Error about invalid coordinates, action rejected

**Solutions**:
1. Ensure correct screen resolution in config
2. Check for multi-monitor issues (use primary monitor)
3. Verify screenshot capture is working correctly
4. Try restarting automation engine
5. Use fallback coordinates

### Issue: "Screenshot capture failed"

**Symptoms**: Error capturing screenshot, visual navigation aborts

**Solutions**:
1. Check screen capture permissions (Windows: allow screen recording)
2. Restart automation engine
3. Verify no other apps are blocking screen capture
4. Check disk space for temporary files
5. Try reducing `screenshot_quality`

### Issue: "Critical action requires confirmation but no response"

**Symptoms**: Workflow pauses waiting for confirmation

**Solutions**:
1. Check console for confirmation prompt
2. Respond with 'y' or 'n' in terminal
3. Disable `require_confirmation_for_critical` if running unattended
4. Remove critical keywords from task description if false positive
5. Use protocol-based actions for critical operations

### Issue: "Visual navigation slower than expected"

**Symptoms**: Each action takes >5 seconds

**Solutions**:
1. Use faster vision model: `gemini-2.0-flash-exp`
2. Reduce `screenshot_quality` to 70-80
3. Disable audit logging if not needed
4. Check network latency to Gemini API
5. Use protocol-based actions for known coordinates

## Advanced Usage

### Custom Vision Prompts

For advanced users, you can customize vision prompts by modifying `ai_brain/vision_navigator.py`:

```python
def analyze_screen_for_action(self, screenshot, current_mouse_pos, task_description, screen_size):
    prompt = f"""
    Custom prompt here...
    Task: {task_description}
    Current mouse: {current_mouse_pos}
    """
    # ... rest of method
```

### Integrating with Custom Workflows

```python
# In your custom workflow
from ai_brain.vision_navigator import VisionNavigator

def my_custom_workflow():
    navigator = VisionNavigator(gemini_client, config)
    
    # Step 1: Visual navigation
    result = navigator.analyze_screen_for_action(...)
    
    # Step 2: Custom logic
    if result.confidence > 0.8:
        execute_action(result)
    else:
        use_fallback_method()
    
    # Step 3: Verification
    success = navigator.verify_action_result(before_img, after_img, "Button clicked")
```

### Audit Log Analysis

```python
import json

# Load audit log
with open('logs/visual_navigation_audit.json', 'r') as f:
    audit_data = json.load(f)

# Analyze confidence scores
confidences = [entry['confidence'] for entry in audit_data]
avg_confidence = sum(confidences) / len(confidences)
print(f"Average confidence: {avg_confidence:.2f}")

# Find low-confidence actions
low_conf = [e for e in audit_data if e['confidence'] < 0.7]
print(f"Low confidence actions: {len(low_conf)}")
```

## Performance Optimization

### Tips for Faster Execution

1. **Use Fast Model**: `gemini-2.0-flash-exp` is 2-3x faster than pro models
2. **Reduce Screenshot Quality**: 70-80 quality is usually sufficient
3. **Disable Audit Logging**: Saves disk I/O time
4. **Minimize Iterations**: Set lower `max_iterations` for simple tasks
5. **Cache Results**: For repeated workflows, cache vision analysis

### Expected Performance

| Scenario | Latency | Notes |
|----------|---------|-------|
| Single click | 2-4s | Includes capture, analysis, execution |
| Multi-step (3-5 actions) | 8-15s | With verification between steps |
| Complex workflow (8-10 actions) | 20-30s | May require user confirmation |

## Security and Privacy

### Data Handling

- **Screenshots**: Sent to Gemini API for analysis
- **Audit Logs**: Stored locally, may contain sensitive information
- **API Keys**: Stored in `.env` file, never logged

### Privacy Recommendations

1. **Disable Audit Logging**: If handling sensitive data
2. **Clear Logs Regularly**: Delete old audit logs
3. **Review Screenshots**: Check what's being sent to API
4. **Use Local Models**: Consider local vision models for sensitive environments (future feature)

### Security Best Practices

1. **Enable Critical Action Confirmation**: Always require confirmation for dangerous actions
2. **Set Conservative Limits**: Use low `max_iterations` to prevent runaway automation
3. **Monitor Audit Logs**: Review for unexpected behavior
4. **Use Fallbacks Carefully**: Fallback coordinates bypass visual verification
5. **Test in Safe Environment**: Always test new workflows in non-production environment

## FAQ

**Q: Can I use visual navigation without an internet connection?**
A: No, currently requires Gemini API which needs internet. Local model support is planned.

**Q: Does visual navigation work with multiple monitors?**
A: Currently only supports primary monitor. Multi-monitor support is planned.

**Q: How much does visual navigation cost?**
A: Depends on Gemini API pricing. Each action uses ~1 vision API call. Check Google Cloud pricing.

**Q: Can I use visual navigation for gaming?**
A: Not recommended. Gaming requires real-time responses (<100ms), visual navigation has 2-4s latency.

**Q: What happens if the UI changes during execution?**
A: The AI adapts to changes between iterations. Each action captures a fresh screenshot.

**Q: Can I disable visual navigation for specific protocols?**
A: Yes, simply don't use `visual_navigate` action. Use standard protocol actions instead.

**Q: How do I debug visual navigation issues?**
A: Enable audit logging and review `logs/visual_navigation_audit.json` for detailed action history.

**Q: Can visual navigation handle dropdown menus?**
A: Yes, but may require multiple iterations. First click opens dropdown, second click selects item.

**Q: What's the difference between visual navigation and protocol-based automation?**
A: Protocol uses fixed coordinates, visual navigation uses AI to find elements dynamically.

**Q: Can I combine visual navigation with protocol actions?**
A: Yes! Mix `visual_navigate` with standard actions like `click`, `type`, `wait` in the same protocol.

## Support and Resources

### Documentation
- [System Architecture](SYSTEM_ARCHITECTURE.md)
- [Protocol System Guide](PROTOCOL_SYSTEM_QUICK_REFERENCE.md)
- [Vision Navigator Implementation](VISION_NAVIGATOR_IMPLEMENTATION.md)
- [Safety Validation](SAFETY_VALIDATION_QUICK_REFERENCE.md)

### Examples
- [Visual Navigation Example Protocol](../examples/protocols/visual_navigation_example.json)
- [Complex Workflow Example](../examples/protocols/complex_macro_workflow.json)

### Testing
- Run tests: `pytest tests/test_visual_navigate_protocol.py`
- Verify installation: `python tests/verify_vision_navigator.py`

### Getting Help
- Check audit logs: `logs/visual_navigation_audit.json`
- Review error messages in console
- Enable debug logging in config
- Consult troubleshooting section above

## Changelog

### Version 1.0 (Current)
- Initial release
- Basic visual navigation with click actions
- Safety features (critical action confirmation, loop detection)
- Audit logging
- Protocol integration
- Fallback coordinate support

### Planned Features
- Multi-monitor support
- Enhanced text input capabilities
- Local vision model support
- Element highlighting and visual feedback
- Voice guidance during execution
- Learning and adaptation from past actions
- Advanced verification with OCR
- Confidence improvement with multi-model consensus

---

**Last Updated**: 2025-10-14
**Version**: 1.0
