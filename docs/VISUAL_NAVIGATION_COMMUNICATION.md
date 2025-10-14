# Visual Navigation Communication Implementation

## Overview

This document describes the implementation of visual navigation communication methods in the MessageBroker class. These methods enable the AI Brain and Automation Engine to communicate for AI-driven visual navigation tasks.

## Implementation Summary

### Task 3: Extend MessageBroker for Visual Navigation Communication

**Status**: ✅ Completed

All subtasks have been successfully implemented:
- ✅ 3.1 Add visual navigation message types
- ✅ 3.2 Implement visual navigation request/response methods
- ✅ 3.3 Implement visual action command/result methods

## Message Types

### 1. Visual Navigation Request
**Direction**: AI Brain → Automation Engine

```json
{
  "type": "visual_navigation_request",
  "request_id": "unique_id",
  "task_description": "Click the submit button",
  "workflow_goal": "Submit the form",
  "iteration": 1,
  "max_iterations": 10,
  "timestamp": "ISO timestamp"
}
```

### 2. Visual Navigation Response
**Direction**: Automation Engine → AI Brain

```json
{
  "type": "visual_navigation_response",
  "request_id": "unique_id",
  "screenshot_base64": "base64_encoded_image",
  "mouse_position": {"x": 100, "y": 200},
  "screen_size": {"width": 1920, "height": 1080},
  "timestamp": "ISO timestamp"
}
```

### 3. Visual Action Command
**Direction**: AI Brain → Automation Engine

```json
{
  "type": "visual_action_command",
  "request_id": "unique_id",
  "action": "click",
  "coordinates": {"x": 500, "y": 300},
  "text": null,
  "request_followup": true,
  "timestamp": "ISO timestamp"
}
```

### 4. Visual Action Result
**Direction**: Automation Engine → AI Brain

```json
{
  "type": "visual_action_result",
  "request_id": "unique_id",
  "status": "success",
  "error": null,
  "screenshot_base64": "...",
  "mouse_position": {"x": 500, "y": 300},
  "timestamp": "ISO timestamp"
}
```

## API Methods

### Request/Response Methods

#### `send_visual_navigation_request(request: dict) -> None`
Sends a visual navigation request to the automation engine.

#### `receive_visual_navigation_request(timeout: float = 0) -> Optional[dict]`
Receives a visual navigation request from the AI brain.

#### `send_visual_navigation_response(response: dict) -> None`
Sends a visual navigation response with screenshot to the AI brain.

#### `receive_visual_navigation_response(request_id: str, timeout: float = 5.0) -> Optional[dict]`
Receives a visual navigation response for a specific request.

### Command/Result Methods

#### `send_visual_action_command(command: dict) -> None`
Sends a visual action command to the automation engine.

#### `receive_visual_action_command(timeout: float = 0) -> Optional[dict]`
Receives a visual action command from the AI brain.

#### `send_visual_action_result(result: dict) -> None`
Sends a visual action result back to the AI brain.

#### `receive_visual_action_result(request_id: str, timeout: float = 5.0) -> Optional[dict]`
Receives a visual action result for a specific request.

## File Storage

All visual navigation messages are stored in:
```
shared/messages/visual_navigation/
├── request_{request_id}.json
├── response_{request_id}.json
├── command_{request_id}.json
└── result_{request_id}.json
```

## Usage Example

### AI Brain Side (Sending Request)

```python
from shared.communication import MessageBroker
import uuid

broker = MessageBroker()

# Send visual navigation request
request_id = str(uuid.uuid4())
broker.send_visual_navigation_request({
    "request_id": request_id,
    "task_description": "Click the login button",
    "workflow_goal": "Navigate to login page",
    "iteration": 1,
    "max_iterations": 10
})

# Wait for response with screenshot
response = broker.receive_visual_navigation_response(request_id, timeout=5.0)
if response:
    screenshot = response["screenshot_base64"]
    mouse_pos = response["mouse_position"]
    # Analyze screenshot and determine action...
```

### Automation Engine Side (Handling Request)

```python
from shared.communication import MessageBroker

broker = MessageBroker()

# Check for visual navigation requests
request = broker.receive_visual_navigation_request(timeout=0.1)
if request:
    # Capture screenshot and mouse position
    screenshot_base64 = capture_and_encode_screenshot()
    mouse_pos = get_mouse_position()
    
    # Send response
    broker.send_visual_navigation_response({
        "request_id": request["request_id"],
        "screenshot_base64": screenshot_base64,
        "mouse_position": {"x": mouse_pos[0], "y": mouse_pos[1]},
        "screen_size": {"width": 1920, "height": 1080}
    })
```

### AI Brain Side (Sending Action Command)

```python
# After analyzing screenshot, send action command
broker.send_visual_action_command({
    "request_id": request_id,
    "action": "click",
    "coordinates": {"x": 500, "y": 300},
    "text": None,
    "request_followup": True  # Request new screenshot after action
})

# Wait for action result
result = broker.receive_visual_action_result(request_id, timeout=5.0)
if result and result["status"] == "success":
    if result.get("screenshot_base64"):
        # Verify action succeeded by analyzing new screenshot
        pass
```

### Automation Engine Side (Executing Action)

```python
# Check for visual action commands
command = broker.receive_visual_action_command(timeout=0.1)
if command:
    # Execute the action
    success = execute_mouse_action(
        command["action"],
        command["coordinates"]["x"],
        command["coordinates"]["y"]
    )
    
    # Capture new screenshot if requested
    new_screenshot = None
    if command.get("request_followup"):
        new_screenshot = capture_and_encode_screenshot()
    
    # Send result
    broker.send_visual_action_result({
        "request_id": command["request_id"],
        "status": "success" if success else "error",
        "error": None,
        "screenshot_base64": new_screenshot,
        "mouse_position": command["coordinates"]
    })
```

## Testing

Comprehensive tests have been implemented in `tests/test_visual_navigation_communication.py`:

- ✅ Request/response message flow
- ✅ Command/result message flow
- ✅ Timeout behavior
- ✅ Message clearing
- ✅ Message structure validation

All tests pass successfully.

## Requirements Satisfied

This implementation satisfies the following requirements from the design document:

- **Requirement 5.1**: ✅ Defined "visual_navigation_request" message type
- **Requirement 5.2**: ✅ AI Brain can send messages with task_description, screenshot, and mouse_position
- **Requirement 5.3**: ✅ Automation Engine responds with status, action_taken, and optional new screenshot
- **Requirement 5.4**: ✅ Error details included in response messages
- **Requirement 5.5**: ✅ "request_followup" flag supported for requesting new screenshots

## Next Steps

The following tasks depend on this implementation:

1. **Task 4**: Create VisualNavigationHandler for automation engine
2. **Task 5**: Integrate visual navigation into AI Brain main loop
3. **Task 6**: Integrate visual navigation into Automation Engine main loop

These tasks can now proceed using the communication methods implemented here.

## Files Modified

- `shared/communication.py` - Added visual navigation methods and directory
- `tests/test_visual_navigation_communication.py` - Comprehensive test suite

## Notes

- All messages are stored as JSON files in `shared/messages/visual_navigation/`
- Messages are automatically deleted after being read
- Request IDs are used to match requests with their responses/results
- Default timeout for responses and results is 5.0 seconds
- The `clear_messages()` method now also clears visual navigation messages
