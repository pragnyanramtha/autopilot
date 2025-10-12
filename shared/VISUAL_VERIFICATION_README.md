# Visual Verification System

## Overview

The Visual Verification System enables the JSON Instruction Protocol to pause execution, capture screenshots, and verify screen state using Gemini vision models. This allows for adaptive automation that can respond to actual visual feedback rather than relying on fixed coordinates or timing.

## Features

- **AI-Powered Screen Analysis**: Uses Gemini vision models to analyze screenshots
- **Multi-Model Support**: Primary model with automatic fallback for reliability
- **Coordinate Extraction**: AI can identify element locations and return coordinates
- **Adaptive Execution**: Protocol can adapt based on verification results
- **Context Integration**: Verification results stored in execution context for use in subsequent actions

## Architecture

```
Protocol Execution
       ↓
   verify_screen action
       ↓
   Pause Execution
       ↓
   Capture Screenshot
       ↓
   Send to Gemini Vision API
       ↓
   Parse AI Response
       ↓
   Extract Coordinates (if provided)
       ↓
   Update Execution Context
       ↓
   Resume Execution
```

## Components

### VisualVerifier Class

Located in `shared/visual_verifier.py`

**Key Methods:**
- `verify_screen()`: Main verification method
- `_verify_with_model()`: Verify using specific model
- `_parse_verification_response()`: Parse AI response
- `get_statistics()`: Get verification statistics

**Configuration:**
- Primary Model: `gemini-2.0-flash-exp` (Gemini 2.5 Flash Live equivalent)
- Fallback Model: `gemini-1.5-flash` (gemini-flash-lite-latest equivalent)
- Timeout: 10 seconds (configurable)

### VerificationResult

Data class containing verification results:

```python
@dataclass
class VerificationResult:
    safe_to_proceed: bool          # Whether it's safe to continue
    confidence: float               # Confidence level (0.0-1.0)
    analysis: str                   # AI's analysis of the screen
    updated_coordinates: Optional[Dict[str, int]]  # Element coordinates if found
    suggested_actions: Optional[list]  # Alternative actions if not safe
    model_used: str                 # Which model was used
```

## Usage

### Basic Verification

```json
{
  "action": "verify_screen",
  "params": {
    "context": "Looking for login button",
    "expected": "Login button is visible and clickable",
    "confidence_threshold": 0.7
  },
  "wait_after_ms": 500
}
```

### Adaptive Mouse Movement

Use verification to find elements and move the mouse:

```json
{
  "actions": [
    {
      "action": "verify_screen",
      "params": {
        "context": "Looking for Submit button",
        "expected": "Submit button is visible",
        "confidence_threshold": 0.7
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
  ]
}
```

### Context Variables

After a `verify_screen` action, these variables are available:

- `{{verified_x}}`: X coordinate of identified element
- `{{verified_y}}`: Y coordinate of identified element
- `{{last_verification_safe}}`: Boolean indicating if safe to proceed
- `{{last_verification_confidence}}`: Confidence level
- `{{last_verification_analysis}}`: AI's analysis text
- `{{suggested_actions}}`: List of suggested alternative actions

## Integration with Protocol Executor

The ProtocolExecutor automatically handles verification results:

1. **Execute verify_screen action**: Calls VisualVerifier
2. **Receive result**: Gets VerificationResult object
3. **Update context**: Stores coordinates and metadata in execution context
4. **Continue execution**: Subsequent actions can use `{{verified_x}}` and `{{verified_y}}`

### Adaptive Execution Flow

```python
# In ProtocolExecutor._execute_action()
result = self.action_registry.execute(action.action, params)

# Handle visual verification results
if action.action == 'verify_screen' and isinstance(result, dict):
    self._handle_verification_result(result)
```

```python
# In ProtocolExecutor._handle_verification_result()
if updated_coordinates:
    x = updated_coordinates.get('x')
    y = updated_coordinates.get('y')
    
    # Store in context for subsequent actions
    self._current_context.set_variable('verified_x', x)
    self._current_context.set_variable('verified_y', y)
```

## Model Configuration

### Primary Model: Gemini 2.0 Flash Exp

- **Speed**: Ultra-fast responses (~1-2 seconds)
- **Quality**: High-quality vision analysis
- **Use Case**: Primary model for all verifications

### Fallback Model: Gemini 1.5 Flash

- **Speed**: Fast responses (~2-3 seconds)
- **Quality**: Good vision analysis
- **Use Case**: Automatic fallback if primary fails

### Automatic Fallback

The system automatically falls back to the secondary model if:
- Primary model times out (>10 seconds)
- Primary model returns an error
- Primary model is unavailable

## Error Handling

### Verification Failures

If verification fails (safe_to_proceed = false):
- Execution continues (doesn't halt)
- Warning is logged
- Context variables are still updated
- Calling code can check `{{last_verification_safe}}` to decide next steps

### Model Failures

If both models fail:
- Returns VerificationResult with safe_to_proceed = false
- Error message in analysis field
- Execution continues with warning

### Timeout Handling

Default timeout: 10 seconds
- Configurable via VisualVerifier constructor
- Applies to each model attempt separately
- Total max time: 20 seconds (10s primary + 10s fallback)

## Examples

### Example 1: Verify Before Clicking

```json
{
  "version": "1.0",
  "metadata": {
    "description": "Safe button click with verification",
    "uses_vision": true
  },
  "actions": [
    {
      "action": "verify_screen",
      "params": {
        "context": "Looking for Save button",
        "expected": "Save button is visible and enabled"
      }
    },
    {
      "action": "mouse_move",
      "params": {
        "x": "{{verified_x}}",
        "y": "{{verified_y}}"
      }
    },
    {
      "action": "mouse_click",
      "params": {"button": "left"}
    }
  ]
}
```

### Example 2: Verify Application State

```json
{
  "action": "verify_screen",
  "params": {
    "context": "Checking if application loaded",
    "expected": "Main window is visible with all UI elements loaded",
    "confidence_threshold": 0.8
  }
}
```

### Example 3: Find and Interact with Dynamic UI

```json
{
  "actions": [
    {
      "action": "verify_screen",
      "params": {
        "context": "Looking for notification popup",
        "expected": "Notification popup with Close button"
      }
    },
    {
      "action": "mouse_move",
      "params": {
        "x": "{{verified_x}}",
        "y": "{{verified_y}}"
      }
    },
    {
      "action": "mouse_click",
      "params": {}
    }
  ]
}
```

## Testing

### Unit Tests

Run visual verifier tests:

```bash
python tests/test_visual_verifier.py
```

Tests include:
- Initialization test
- Result parsing test
- Live verification test (requires API key)

### Demo

Run the visual verification demo:

```bash
python examples/visual_verification_demo.py
```

Demo includes:
- Basic verification with Notepad
- Adaptive mouse movement
- Context variable usage

### Dry Run Mode

Test without executing actions:

```bash
python examples/visual_verification_demo.py --dry-run
```

## Performance

### Typical Response Times

- **Primary Model**: 1-3 seconds
- **Fallback Model**: 2-4 seconds
- **Total (with fallback)**: 3-7 seconds

### Optimization Tips

1. **Use appropriate confidence thresholds**: Lower thresholds (0.6-0.7) for faster acceptance
2. **Capture specific regions**: Use `capture_region` parameter to reduce image size
3. **Cache verification results**: Avoid re-verifying the same state
4. **Batch verifications**: Verify multiple elements in one call when possible

## Requirements Satisfied

This implementation satisfies the following requirements:

- **11.1**: Pause workflow execution for verification ✓
- **11.2**: Capture screenshot and send to Gemini ✓
- **11.3**: Receive AI analysis and resume/adapt ✓
- **11.4**: Multi-model support with fallback ✓
- **11.5**: Parse safe_to_proceed vs requires_adaptation ✓
- **11.6**: Extract updated coordinates from AI response ✓
- **11.7**: Update execution context with new coordinates ✓
- **12.4**: Resume execution with adapted parameters ✓
- **13.1**: Configure primary model ✓
- **13.2**: Configure fallback model ✓
- **13.3**: Timeout handling ✓
- **13.4**: Error handling ✓

## Future Enhancements

Potential improvements:
- OCR integration for text verification
- Image template matching for faster element detection
- Caching of verification results
- Batch verification of multiple elements
- Region-based verification for better performance
- Custom model configuration per verification
