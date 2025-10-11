# Automation Engine

The Automation Engine is responsible for executing workflows received from the AI Brain. It continuously polls for incoming workflows, executes them using mouse/keyboard control, and reports execution status back.

## Features

- **Continuous Polling**: Monitors for incoming workflows from AI Brain
- **Workflow Execution**: Executes workflows step-by-step with proper timing
- **Status Reporting**: Reports execution results back to AI Brain
- **Error Handling**: Gracefully handles errors and user interrupts
- **Safety Controls**: Includes emergency stop and dry-run mode
- **Graceful Shutdown**: Handles Ctrl+C and system signals properly

## Usage

### Basic Usage

Start the automation engine in live mode:

```bash
python automation_engine/main.py
```

### Dry-Run Mode

Test workflows without performing actual actions:

```bash
python automation_engine/main.py --dry-run
```

### Custom Configuration

Use a custom configuration file:

```bash
python automation_engine/main.py --config path/to/config.json
```

## Command Line Options

- `--dry-run`: Run in simulation mode without performing actual mouse/keyboard actions
- `--config PATH`: Path to configuration file (default: config.json)

## How It Works

1. **Initialization**: Loads configuration and initializes executor and message broker
2. **Polling Loop**: Continuously checks for incoming workflows from AI Brain
3. **Execution**: When a workflow is received, executes it step-by-step
4. **Status Reporting**: After execution, sends status back to AI Brain
5. **Error Handling**: Catches and reports any errors during execution
6. **Shutdown**: Handles Ctrl+C gracefully, stopping any running workflows

## Architecture

```
AutomationEngineApp
├── AutomationExecutor (executes workflows)
│   ├── InputController (mouse/keyboard control)
│   └── ScreenCapture (screen capture)
└── MessageBroker (communication with AI Brain)
```

## Safety Features

- **Emergency Stop**: Press Ctrl+C to stop execution immediately
- **Mouse Movement Detection**: Automatically stops if user moves mouse significantly
- **Dangerous Action Detection**: Blocks potentially dangerous commands
- **Dry-Run Mode**: Test workflows safely without actual execution

## Communication Protocol

The engine communicates with AI Brain using file-based message passing:

- **Incoming**: Workflows are received from `shared/messages/workflows/`
- **Outgoing**: Status reports are sent to `shared/messages/status/`

## Requirements

See `requirements.txt` for dependencies:
- pyautogui (mouse/keyboard control)
- mss (screen capture)
- pillow (image processing)

## Testing

Run the test suite:

```bash
python test_automation_engine_main.py
```

## Example Output

```
============================================================
Automation Engine Started
============================================================
Mode: LIVE EXECUTION
Poll interval: 0.5s
Waiting for workflows from AI Brain...
Press Ctrl+C to stop
============================================================

============================================================
Received Workflow #1: workflow-12345
============================================================
Steps: 5
Metadata: {'task': 'open_browser'}

Executing step 1/5: mouse_move
Executing step 2/5: click
Executing step 3/5: type
Executing step 4/5: press_key
Executing step 5/5: wait
Workflow completed successfully!

============================================================
Workflow Execution Complete
============================================================
Status: success
Steps completed: 5/5
Duration: 1234ms
============================================================

Status reported back to AI Brain

Waiting for next workflow...
```

## Troubleshooting

### No workflows received
- Ensure AI Brain is running and sending workflows
- Check that `shared/messages/workflows/` directory exists
- Verify file permissions

### Execution errors
- Check that required dependencies are installed
- Verify screen resolution and coordinates
- Try running in `--dry-run` mode first

### Permission errors
- Some actions may require elevated privileges
- Run with appropriate permissions for your OS

## Related Components

- **AI Brain** (`ai_brain/main.py`): Generates workflows from user commands
- **Communication Layer** (`shared/communication.py`): Handles message passing
- **Executor** (`automation_engine/executor.py`): Core workflow execution logic
