# Visual Navigation Communication - Quick Reference

## Quick Start

```python
from shared.communication import MessageBroker
import uuid

broker = MessageBroker()
request_id = str(uuid.uuid4())
```

## Message Flow

```
AI Brain                    Automation Engine
   |                               |
   |--visual_navigation_request--->|
   |                               | (captures screenshot)
   |<--visual_navigation_response--|
   | (analyzes screenshot)         |
   |--visual_action_command------->|
   |                               | (executes action)
   |<--visual_action_result--------|
   |                               |
```

## Methods

### Send/Receive Requests
```python
# AI Brain sends request
broker.send_visual_navigation_request({
    "request_id": request_id,
    "task_description": "Click submit button",
    "workflow_goal": "Submit form",
    "iteration": 1,
    "max_iterations": 10
})

# Automation Engine receives request
request = broker.receive_visual_navigation_request(timeout=0.1)
```

### Send/Receive Responses
```python
# Automation Engine sends response
broker.send_visual_navigation_response({
    "request_id": request_id,
    "screenshot_base64": "...",
    "mouse_position": {"x": 100, "y": 200},
    "screen_size": {"width": 1920, "height": 1080}
})

# AI Brain receives response
response = broker.receive_visual_navigation_response(request_id, timeout=5.0)
```

### Send/Receive Commands
```python
# AI Brain sends command
broker.send_visual_action_command({
    "request_id": request_id,
    "action": "click",  # or 'double_click', 'right_click', 'type'
    "coordinates": {"x": 500, "y": 300},
    "text": None,
    "request_followup": True
})

# Automation Engine receives command
command = broker.receive_visual_action_command(timeout=0.1)
```

### Send/Receive Results
```python
# Automation Engine sends result
broker.send_visual_action_result({
    "request_id": request_id,
    "status": "success",  # or 'error'
    "error": None,
    "screenshot_base64": "...",  # if request_followup was True
    "mouse_position": {"x": 500, "y": 300}
})

# AI Brain receives result
result = broker.receive_visual_action_result(request_id, timeout=5.0)
```

## Action Types

- `"click"` - Single left click
- `"double_click"` - Double left click
- `"right_click"` - Right click
- `"type"` - Type text (use `text` field)

## Timeouts

- **Request/Command receive**: Default 0 (no wait), use 0.1 for polling
- **Response/Result receive**: Default 5.0 seconds

## Error Handling

```python
try:
    broker.send_visual_navigation_request(request)
except CommunicationError as e:
    print(f"Communication failed: {e}")

# Check for None on receive
response = broker.receive_visual_navigation_response(request_id, timeout=5.0)
if response is None:
    print("Timeout waiting for response")
```

## Message Storage

Files stored in: `shared/messages/visual_navigation/`
- `request_{request_id}.json`
- `response_{request_id}.json`
- `command_{request_id}.json`
- `result_{request_id}.json`

Files are automatically deleted after being read.

## Complete Example

```python
from shared.communication import MessageBroker
import uuid

broker = MessageBroker()
request_id = str(uuid.uuid4())

# 1. AI Brain: Send request
broker.send_visual_navigation_request({
    "request_id": request_id,
    "task_description": "Click login button",
    "workflow_goal": "Login",
    "iteration": 1,
    "max_iterations": 10
})

# 2. Automation Engine: Receive and respond
request = broker.receive_visual_navigation_request(timeout=0.1)
if request:
    broker.send_visual_navigation_response({
        "request_id": request["request_id"],
        "screenshot_base64": "base64_screenshot_data",
        "mouse_position": {"x": 100, "y": 200},
        "screen_size": {"width": 1920, "height": 1080}
    })

# 3. AI Brain: Receive response and send command
response = broker.receive_visual_navigation_response(request_id, timeout=5.0)
if response:
    broker.send_visual_action_command({
        "request_id": request_id,
        "action": "click",
        "coordinates": {"x": 500, "y": 300},
        "request_followup": True
    })

# 4. Automation Engine: Execute and send result
command = broker.receive_visual_action_command(timeout=0.1)
if command:
    # Execute action...
    broker.send_visual_action_result({
        "request_id": command["request_id"],
        "status": "success",
        "error": None,
        "screenshot_base64": "new_screenshot_data",
        "mouse_position": {"x": 500, "y": 300}
    })

# 5. AI Brain: Verify result
result = broker.receive_visual_action_result(request_id, timeout=5.0)
if result and result["status"] == "success":
    print("Action completed successfully!")
```

## Testing

Run tests:
```bash
python -m pytest tests/test_visual_navigation_communication.py -v
```

All 5 tests should pass.
