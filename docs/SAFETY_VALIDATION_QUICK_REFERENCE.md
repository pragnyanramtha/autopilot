# Safety and Validation Quick Reference

## Overview

Quick reference for safety and validation features in the AI Visual Navigation system.

## Features Summary

| Feature | Purpose | Default Config |
|---------|---------|----------------|
| Coordinate Validation | Ensure clicks are within screen bounds | margin: 10px |
| Loop Detection | Prevent infinite loops from repeated clicks | threshold: 3 clicks |
| Iteration Limit | Stop runaway workflows | max: 10 iterations |
| Critical Action Detection | Require confirmation for dangerous actions | enabled: true |

## Configuration

```json
{
  "visual_navigation": {
    "max_iterations": 10,
    "loop_detection_threshold": 3,
    "loop_detection_buffer_size": 10,
    "require_confirmation_for_critical": true,
    "critical_keywords": ["delete", "format", "shutdown", "remove", "erase"]
  }
}
```

## API Reference

### Coordinate Validation

```python
# Automatically applied in analyze_screen_for_action()
result = navigator.analyze_screen_for_action(screenshot, pos, task, screen_size)

# Result will have:
# - Clamped coordinates if slightly out of bounds
# - no_action if severely out of bounds
```

### Loop Detection

```python
# Reset at workflow start
navigator.reset_action_history()

# Check for loops
loop_detected, warning = navigator.detect_loop(coordinates, tolerance=5)

# Add to history after execution
navigator.add_action_to_history(action, coordinates)
```

### Iteration Limit

```python
# Check limit
limit_reached, warning = navigator.check_iteration_limit(iteration)
```

### Critical Action Detection

```python
# Check if critical
is_critical, keywords = navigator.is_critical_action(reasoning, action)
```

## Safety Behaviors

### Coordinate Validation
- **Within bounds**: ✅ Proceed normally
- **Slightly out (≤10px)**: ⚠️ Clamp and reduce confidence
- **Severely out (>10px)**: ❌ Reject with no_action

### Loop Detection
- **Different coords**: ✅ Proceed normally
- **3+ similar clicks**: ❌ Halt with warning

### Iteration Limit
- **< max_iterations**: ✅ Continue
- **≥ max_iterations**: ❌ Stop with timeout

### Critical Actions
- **Normal action**: ✅ Execute
- **Critical keyword**: ⚠️ Require user confirmation

## Error Messages

### Coordinate Validation
```
⚠ Coordinates (2500, 300) severely out of bounds (overflow: 580px)
✗ Action rejected - coordinates invalid
```

### Loop Detection
```
⚠ Loop detected: Coordinates (100, 100) clicked 3 times (threshold: 3)
```

### Iteration Limit
```
⚠ Workflow Timeout
Maximum iterations (10) reached
Partial results: 8 actions completed
```

### Critical Action
```
⚠ CRITICAL ACTION DETECTED ⚠
Matched keywords: delete, remove
The AI wants to: Click the delete button to remove all files
```

## Testing

Run safety validation tests:
```bash
python -m pytest tests/test_safety_validation.py -v
```

## Common Issues

### False Loop Detection
**Problem**: Loop detected but coordinates are actually different
**Solution**: Increase `tolerance` parameter or `loop_detection_threshold`

### Premature Timeout
**Problem**: Workflow stops before completion
**Solution**: Increase `max_iterations` in config

### Missing Critical Actions
**Problem**: Dangerous actions not flagged
**Solution**: Add keywords to `critical_keywords` list

### Coordinate Clamping Too Aggressive
**Problem**: Valid coordinates being clamped
**Solution**: Increase `margin` parameter in validation

## Best Practices

1. **Always reset action history** at workflow start
2. **Check for loops** before executing actions
3. **Add actions to history** after successful execution
4. **Configure critical keywords** based on your use case
5. **Set appropriate iteration limits** for task complexity
6. **Test with edge cases** (screen edges, repeated actions)

## Related Documentation

- [Safety Validation Implementation](SAFETY_VALIDATION_IMPLEMENTATION.md)
- [Vision Navigator Implementation](VISION_NAVIGATOR_IMPLEMENTATION.md)
- [Visual Navigation Communication](VISUAL_NAVIGATION_COMMUNICATION.md)
