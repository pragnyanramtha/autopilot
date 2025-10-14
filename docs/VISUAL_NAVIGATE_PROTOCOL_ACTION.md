# Visual Navigate Protocol Action

## Overview

The `visual_navigate` action enables AI-powered visual navigation within protocol workflows. Instead of requiring hardcoded coordinates, this action uses AI vision models to analyze the screen, identify target elements, and determine optimal click coordinates dynamically.

## Features

- **AI Vision Analysis**: Uses Gemini vision models to understand screen context
- **Adaptive Targeting**: Finds elements even when UI changes or varies across resolutions
- **Iterative Workflow**: Can perform multiple actions to complete complex tasks
- **Fallback Support**: Optional fallback coordinates if visual navigation fails
- **Safety Features**: Confidence thresholds and critical action detection

## Action Parameters

### Required Parameters

- **`task`** (string): Description of what to do
  - Example: `"Click the login button"`
  - Example: `"Find and click the submit button"`

### Optional Parameters

- **`goal`** (string): Overall workflow goal (defaults to task)
  - Example: `"Navigate to the login page"`
  - Helps AI understand context for multi-step workflows

- **`max_iterations`** (integer): Maximum number of AI analysis iterations (default: 10)
  - Each iteration involves: analyze screen → execute action → verify
  - Prevents infinite loops

- **`timeout`** (integer): Maximum time in seconds to wait for completion (default: 60)
  - Includes time for all iterations and AI processing

- **`fallback_coordinates`** (array): Coordinates to use if visual navigation fails
  - Format: `[x, y]`
  - Example: `[960, 540]` (center of 1920x1080 screen)
  - If provided, will execute standard click at these coordinates on failure

## Usage Examples

### Basic Visual Navigation

```json
{
  "action": "visual_navigate",
  "params": {
    "task": "Click the login button"
  },
  "wait_after_ms": 1000,
  "description": "Use AI vision to find and click login button"
}
```

### With Fallback Coordinates

```json
{
  "action": "visual_navigate",
  "params": {
    "task": "Click the submit button",
    "goal": "Submit the form",
    "max_iterations": 5,
    "fallback_coordinates": [500, 300]
  },
  "wait_after_ms": 1000,
  "description": "Find submit button, fall back to known location if needed"
}
```

### Complex Multi-Step Workflow

```json
{
  "action": "visual_navigate",
  "params": {
    "task": "Navigate to settings and enable dark mode",
    "goal": "Enable dark mode in application settings",
    "max_iterations": 10,
    "timeout": 45
  },
  "wait_after_ms": 2000,
  "description": "Multi-step navigation to enable dark mode"
}
```

## How It Works

### Workflow Sequence

1. **Request Initiated**: Protocol executor sends visual navigation request
2. **Screenshot Capture**: Automation engine captures current screen state
3. **AI Analysis**: Vision model analyzes screenshot and determines action
4. **Action Execution**: Automation engine executes the determined action
5. **Verification**: AI verifies result and determines if more actions needed
6. **Iteration**: Steps 2-5 repeat until goal achieved or limit reached
7. **Result Returned**: Final status sent back to protocol executor

### AI Decision Making

The AI vision model considers:
- Current screen content and layout
- Mouse position
- Task description and goal
- Previous actions taken
- UI element visibility and accessibility

The AI can return:
- **click**: Single click at coordinates
- **double_click**: Double click at coordinates
- **right_click**: Right click at coordinates
- **type**: Type text (with coordinates for focus)
- **complete**: Workflow goal achieved
- **no_action**: No action needed

### Fallback Behavior

Fallback coordinates are used when:
- Visual navigation times out
- Visual navigation fails (AI cannot find target)
- An error occurs during visual navigation

When fallback is triggered:
1. Standard `click` action executed at fallback coordinates
2. Fallback usage logged
3. Result status set to `fallback_success`

## Configuration

Visual navigation behavior is configured in `config.json`:

```json
{
  "visual_navigation": {
    "enabled": true,
    "vision_model": "gemini-2.0-flash-exp",
    "max_iterations": 10,
    "confidence_threshold": 0.6,
    "require_confirmation_for_critical": true,
    "critical_keywords": ["delete", "format", "shutdown", "remove", "erase"]
  }
}
```

## Return Values

### Success

```json
{
  "status": "success",
  "actions_taken": [
    {
      "iteration": 1,
      "action": "click",
      "coordinates": [500, 300],
      "confidence": 0.85,
      "reasoning": "Found login button at center of screen"
    }
  ],
  "iterations": 1,
  "final_coordinates": [500, 300]
}
```

### Fallback Success

```json
{
  "status": "fallback_success",
  "action": "click",
  "coordinates": {"x": 500, "y": 300},
  "result": {...}
}
```

### Timeout

```json
{
  "status": "timeout",
  "error": "Visual navigation timed out after 60s",
  "request_id": "..."
}
```

### Failure (No Fallback)

```json
{
  "status": "failed",
  "error": "Could not find target element",
  "actions_taken": [...]
}
```

## Best Practices

### 1. Provide Clear Task Descriptions

✅ Good:
```json
"task": "Click the blue 'Submit' button at the bottom of the form"
```

❌ Bad:
```json
"task": "Click it"
```

### 2. Use Fallback Coordinates for Critical Actions

```json
{
  "action": "visual_navigate",
  "params": {
    "task": "Click the save button",
    "fallback_coordinates": [800, 600]
  }
}
```

### 3. Set Appropriate Iteration Limits

- Simple tasks (single click): `max_iterations: 3-5`
- Complex workflows (multiple steps): `max_iterations: 10-15`

### 4. Combine with Standard Actions

```json
{
  "actions": [
    {
      "action": "visual_navigate",
      "params": {
        "task": "Click the username field"
      }
    },
    {
      "action": "type",
      "params": {
        "text": "username"
      }
    }
  ]
}
```

### 5. Use Descriptive Goals for Context

```json
{
  "task": "Click the next button",
  "goal": "Navigate through the multi-step registration wizard"
}
```

## Limitations

1. **Performance**: Each iteration takes 2-4 seconds due to AI processing
2. **Accuracy**: Depends on screen clarity and element visibility
3. **Cost**: Uses vision-capable AI models (may incur API costs)
4. **Dynamic Content**: May struggle with rapidly changing UIs
5. **Requires Automation Engine**: Must be running and connected

## Troubleshooting

### Visual Navigation Times Out

- Increase `timeout` parameter
- Reduce `max_iterations` if task is simpler than expected
- Check if automation engine is running
- Verify AI Brain is connected

### Low Confidence Actions

- Improve task description clarity
- Ensure target element is visible on screen
- Check screen resolution and scaling
- Consider using fallback coordinates

### Fallback Always Used

- Task description may be too vague
- Target element may not be visible
- Screen may be in unexpected state
- Check AI Brain logs for analysis details

## Integration with Existing Actions

Visual navigation works seamlessly with other protocol actions:

```json
{
  "actions": [
    {
      "action": "open_browser",
      "params": {"url": "https://example.com"}
    },
    {
      "action": "visual_navigate",
      "params": {"task": "Click the login button"}
    },
    {
      "action": "type",
      "params": {"text": "username"}
    },
    {
      "action": "key",
      "params": {"key": "tab"}
    },
    {
      "action": "type",
      "params": {"text": "password"}
    },
    {
      "action": "visual_navigate",
      "params": {"task": "Click the submit button"}
    }
  ]
}
```

## See Also

- [Visual Navigation System Design](VISUAL_NAVIGATION_HANDLER_IMPLEMENTATION.md)
- [Vision Navigator Implementation](VISION_NAVIGATOR_IMPLEMENTATION.md)
- [Protocol System Documentation](PROTOCOL_SYSTEM_QUICK_REFERENCE.md)
- [Example Protocols](../examples/protocols/)
