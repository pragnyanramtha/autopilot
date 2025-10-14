# Visual Navigate Action - Quick Reference

## Basic Usage

```json
{
  "action": "visual_navigate",
  "params": {
    "task": "Click the login button"
  }
}
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `task` | string | ✅ Yes | - | What to do (e.g., "Click the submit button") |
| `goal` | string | No | Same as task | Overall workflow goal for context |
| `max_iterations` | integer | No | 10 | Maximum AI analysis iterations |
| `timeout` | integer | No | 60 | Maximum time in seconds |
| `fallback_coordinates` | array | No | None | [x, y] coordinates to use if visual navigation fails |

## Common Patterns

### Simple Click
```json
{
  "action": "visual_navigate",
  "params": {
    "task": "Click the submit button"
  },
  "wait_after_ms": 1000
}
```

### With Fallback
```json
{
  "action": "visual_navigate",
  "params": {
    "task": "Click the save button",
    "fallback_coordinates": [800, 600]
  },
  "wait_after_ms": 1000
}
```

### Multi-Step Workflow
```json
{
  "action": "visual_navigate",
  "params": {
    "task": "Navigate to settings and enable dark mode",
    "goal": "Enable dark mode",
    "max_iterations": 10
  },
  "wait_after_ms": 2000
}
```

### Form Field Focus
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
        "text": "myusername"
      }
    }
  ]
}
```

## Return Values

### Success
```json
{
  "status": "success",
  "actions_taken": [...],
  "iterations": 1
}
```

### Fallback Used
```json
{
  "status": "fallback_success",
  "action": "click",
  "coordinates": {"x": 500, "y": 300}
}
```

### Timeout
```json
{
  "status": "timeout",
  "error": "Visual navigation timed out after 60s"
}
```

### Failed
```json
{
  "status": "failed",
  "error": "Could not find target element"
}
```

## Tips

✅ **DO**:
- Provide clear, specific task descriptions
- Use fallback coordinates for critical actions
- Set appropriate iteration limits (3-5 for simple, 10-15 for complex)
- Combine with standard actions for complete workflows

❌ **DON'T**:
- Use vague task descriptions ("click it")
- Set very high iteration limits (wastes time)
- Rely solely on visual navigation without fallbacks for critical actions
- Expect instant results (each iteration takes 2-4 seconds)

## Requirements

- Automation engine must be running
- AI Brain must be connected
- Visual navigation must be enabled in config
- Vision-capable AI model must be configured

## See Also

- [Full Documentation](VISUAL_NAVIGATE_PROTOCOL_ACTION.md)
- [Example Protocol](../examples/protocols/visual_navigation_example.json)
- [Protocol System Reference](PROTOCOL_SYSTEM_QUICK_REFERENCE.md)
