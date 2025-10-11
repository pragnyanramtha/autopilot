# AI Automation Assistant

An intelligent automation system that understands natural language commands and executes them by controlling your mouse and keyboard. Powered by Google's Gemini AI.

## Overview

The AI Automation Assistant bridges the gap between natural language and system-level automation. Simply tell it what you want to do in plain English, and it will understand, plan, and execute the task for you.

### Key Features

- **Natural Language Processing**: Give commands in plain English
- **Screen Vision**: AI can see and understand your screen
- **Intelligent Workflow Generation**: Automatically creates step-by-step execution plans
- **Safe Execution**: Dry-run mode, confirmations, and emergency stop
- **Real-time Feedback**: See execution progress and results
- **Easy Control**: Unified CLI for managing all components

## Architecture

The system consists of three main components:

1. **AI Brain** - Processes natural language commands using Gemini AI and generates workflows
2. **Automation Engine** - Executes workflows by controlling mouse and keyboard
3. **Communication Layer** - Coordinates between components using file-based messaging

```
┌─────────────┐         ┌──────────────────┐         ┌────────────────────┐
│   User      │────────▶│    AI Brain      │────────▶│ Automation Engine  │
│  Commands   │         │  (Gemini SDK)    │         │  (Mouse/Keyboard)  │
└─────────────┘         └──────────────────┘         └────────────────────┘
                               │                              │
                               │                              │
                               ▼                              ▼
                        ┌──────────────┐            ┌─────────────────┐
                        │   Workflow   │            │  Screen Capture │
                        │  Generator   │            │   & Analysis    │
                        └──────────────┘            └─────────────────┘
```

## Requirements

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: 3.10 or higher
- **RAM**: 4GB minimum
- **Internet**: Required for Gemini API access
- **Screen Resolution**: 1920x1080 or higher recommended

### Python Dependencies

```
google-generativeai>=0.3.0
pyautogui>=0.9.54
mss>=9.0.1
Pillow>=10.0.0
rich>=13.0.0
```

## Installation

### 1. Clone or Download the Repository

```bash
git clone <repository-url>
cd ai-automation-assistant
```

### 2. Set Up Python Virtual Environment

**Windows:**
```cmd
setup_venv.bat
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Gemini API Key

You need a Gemini API key from Google AI Studio.

**Option A: Environment Variable (Recommended)**
```bash
# Windows (Command Prompt)
set GEMINI_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:GEMINI_API_KEY="your_api_key_here"

# macOS/Linux
export GEMINI_API_KEY=your_api_key_here
```

**Option B: Configuration File**

Edit `config.json` and replace `YOUR_GEMINI_API_KEY_HERE` with your actual API key:

```json
{
  "gemini": {
    "api_key": "your_actual_api_key_here",
    "model": "gemini-2.5-flash",
    "temperature": 0.7
  }
}
```

### 4. Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and use it in step 3 above

## Usage

### Quick Start with CLI

The easiest way to use the system is through the unified CLI:

```bash
python cli.py
```

This will show you a menu with options to:
- Start/stop AI Brain
- Start/stop Automation Engine
- View system status
- Get help

### Starting Components Individually

**Start AI Brain:**
```bash
python -m ai_brain.main
```

**Start Automation Engine:**
```bash
python -m automation_engine.main
```

**Start Automation Engine in Dry-Run Mode (Safe Testing):**
```bash
python -m automation_engine.main --dry-run
```

### Example Commands

Once the AI Brain is running, you can give it natural language commands:

#### Basic Mouse Actions
```
Click the submit button
Click at coordinates 500, 300
Double click the file icon
Right click the desktop
Move mouse to center of screen
```

#### Keyboard Actions
```
Type hello world
Type my email address
Press enter
Press ctrl+c
```

#### Application Control
```
Open Chrome
Launch Notepad
Open File Explorer
```

#### Complex Tasks
```
Search for Python tutorials
Fill out the form with my information
Navigate to the settings page
```

### Workflow Execution

1. **Give Command**: Type your command in natural language
2. **AI Analysis**: The AI Brain analyzes your command and current screen
3. **Workflow Generation**: A step-by-step workflow is created
4. **Review**: You'll see the planned steps and can review them
5. **Confirmation**: Confirm to execute or cancel
6. **Execution**: The Automation Engine executes each step
7. **Results**: See the execution status and any errors

## Configuration

### config.json

```json
{
  "gemini": {
    "api_key": "YOUR_GEMINI_API_KEY_HERE",
    "model": "gemini-2.5-flash",
    "temperature": 0.7
  },
  "automation": {
    "safety_delay_ms": 100,
    "screenshot_quality": 85,
    "enable_safety_monitor": true,
    "interrupt_on_mouse_move": true
  },
  "communication": {
    "method": "file",
    "workflow_file": "shared/workflow_queue.json",
    "status_file": "shared/status_queue.json"
  }
}
```

### Configuration Options

#### Gemini Settings
- `api_key`: Your Gemini API key
- `model`: Gemini model to use (default: gemini-2.5-flash)
- `temperature`: AI creativity level (0.0-1.0, default: 0.7)

#### Automation Settings
- `safety_delay_ms`: Delay between actions for safety (default: 100ms)
- `screenshot_quality`: JPEG quality for screen captures (1-100, default: 85)
- `enable_safety_monitor`: Enable safety checks (default: true)
- `interrupt_on_mouse_move`: Stop if user moves mouse (default: true)

#### Communication Settings
- `method`: Communication method (default: "file")
- `workflow_file`: Path to workflow queue file
- `status_file`: Path to status queue file

## Safety Features

### Dry-Run Mode

Test workflows without actually executing them:

```bash
python -m automation_engine.main --dry-run
```

### Confirmation Required

By default, you must confirm before any workflow is executed. Review the steps and approve or cancel.

### Emergency Stop

Press `Ctrl+C` at any time to stop execution immediately.

### User Interrupt Detection

If you move your mouse during execution, the system can automatically pause or stop (configurable).

### Action Validation

Dangerous actions require explicit confirmation before execution.

## Project Structure

```
ai-automation-assistant/
├── ai_brain/                 # AI Brain component
│   ├── main.py              # AI Brain main application
│   ├── gemini_client.py     # Gemini API client
│   └── workflow_generator.py # Workflow generation logic
├── automation_engine/        # Automation Engine component
│   ├── main.py              # Automation Engine main application
│   ├── executor.py          # Workflow executor
│   ├── screen_capture.py    # Screen capture utilities
│   └── input_controller.py  # Mouse/keyboard control
├── shared/                   # Shared components
│   ├── communication.py     # Inter-component communication
│   └── data_models.py       # Data models and structures
├── cli.py                    # Unified CLI interface
├── config.json              # Configuration file
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Troubleshooting

### AI Brain Won't Start

**Problem**: "Error: Gemini API key not configured!"

**Solution**: 
- Set the `GEMINI_API_KEY` environment variable
- Or edit `config.json` with your API key
- Verify your API key is valid at [Google AI Studio](https://makersuite.google.com/)

### Automation Engine Won't Start

**Problem**: Import errors or missing dependencies

**Solution**:
```bash
pip install -r requirements.txt
```

### Commands Not Executing

**Problem**: Workflows are generated but not executed

**Solution**:
- Make sure both AI Brain and Automation Engine are running
- Check that communication files are being created in `shared/` directory
- Verify file permissions for the `shared/` directory

### Low Confidence Warnings

**Problem**: "Warning: Low confidence"

**Solution**:
- Be more specific in your commands
- Provide more context about what you want to do
- Check that your screen is visible and clear

### Screen Capture Issues

**Problem**: AI can't find elements on screen

**Solution**:
- Ensure the target application is visible and not minimized
- Check screen resolution and scaling settings
- Try describing the element more specifically

## Testing

### Run All Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest test_communication.py

# Run with verbose output
python -m pytest -v
```

### Test Files

- `test_communication.py` - Communication layer tests
- `test_executor.py` - Automation executor tests
- `test_ai_brain_main.py` - AI Brain integration tests
- `test_automation_engine_main.py` - Automation Engine integration tests
- `test_integration_full_flow.py` - End-to-end integration tests

### Manual Testing

1. Start in dry-run mode:
```bash
python -m automation_engine.main --dry-run
```

2. Give simple commands to test parsing:
```
Click at 100, 200
Type hello
```

3. Verify workflows are generated correctly

## Development

### Adding New Actions

1. Update `gemini_client.py` to recognize the new action
2. Add workflow step generation in `workflow_generator.py`
3. Implement execution logic in `executor.py`
4. Add tests for the new action

### Extending the AI

The system uses Gemini's vision and language capabilities. You can:
- Adjust the temperature for more/less creative responses
- Modify prompts in `gemini_client.py`
- Add context management for multi-turn conversations

### Custom Communication Methods

The current implementation uses file-based communication. You can implement other methods:
- ZeroMQ for faster IPC
- HTTP REST API
- WebSockets for real-time updates

## Security Considerations

### API Key Security

- Never commit your API key to version control
- Use environment variables for production
- Rotate keys regularly

### Action Validation

- Review workflows before execution
- Use dry-run mode for testing
- Be cautious with system-level commands

### Data Privacy

- Screen captures are sent to Gemini API
- Don't use with sensitive information visible
- Clear conversation history when needed

## Performance

### Typical Latency

- Command parsing: 1-3 seconds
- Workflow generation: 2-5 seconds
- Execution: Depends on workflow complexity

### Optimization Tips

- Use lower screenshot quality for faster processing
- Reduce safety delays for faster execution (less safe)
- Cache common workflows

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

[Add your license information here]

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation
- Review test files for examples

## Acknowledgments

- Built with [Google Gemini AI](https://deepmind.google/technologies/gemini/)
- Uses [PyAutoGUI](https://pyautogui.readthedocs.io/) for automation
- CLI powered by [Rich](https://rich.readthedocs.io/)

## Changelog

### Version 1.0.0 (Current)

- Initial release
- Natural language command processing
- Screen vision and analysis
- Workflow generation and execution
- Safety features and dry-run mode
- Unified CLI interface
- File-based communication
- Comprehensive testing suite
