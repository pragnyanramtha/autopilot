# AI Brain - Main Application

The AI Brain is the command center of the AI Automation Assistant. It processes natural language commands, generates workflows, and coordinates with the automation engine.

## Features

- Natural language command processing using Gemini AI
- Workflow generation and validation
- Interactive command-line interface with rich formatting
- Real-time execution status monitoring
- Bidirectional communication with automation engine

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Gemini API key:
```bash
# Windows (PowerShell)
$env:GEMINI_API_KEY="your-api-key-here"

# Windows (CMD)
set GEMINI_API_KEY=your-api-key-here

# Linux/Mac
export GEMINI_API_KEY="your-api-key-here"
```

Alternatively, update the `config.json` file with your API key.

## Running

```bash
python ai_brain/main.py
```

## Usage

Once started, you can give natural language commands:

### Example Commands

- `Click the submit button` - Click on a UI element
- `Type hello world` - Type text
- `Open Chrome` - Launch an application
- `Search for Python tutorials` - Perform a web search
- `Move mouse to center` - Move the mouse cursor

### Special Commands

- `help` - Show help message
- `status` - Show system status
- `clear` - Clear the screen
- `exit` or `quit` - Exit the application

## How It Works

1. **Command Input**: You enter a natural language command
2. **Intent Parsing**: Gemini AI analyzes the command and extracts the intent
3. **Workflow Generation**: The system creates a step-by-step workflow
4. **Validation**: The workflow is validated for safety and correctness
5. **Confirmation**: You review and confirm the workflow
6. **Execution**: The workflow is sent to the automation engine
7. **Status Monitoring**: Execution results are displayed in real-time

## Requirements Satisfied

This implementation satisfies the following requirements:

- **1.1**: Processes user commands using Gemini SDK
- **1.3**: Handles ambiguous commands with confidence checking
- **1.4**: Provides helpful error messages and examples
- **6.6**: Maintains conversation context for multi-turn interactions

## Architecture

```
User Input
    ↓
GeminiClient (NLP Processing)
    ↓
WorkflowGenerator (Workflow Creation)
    ↓
MessageBroker (Communication)
    ↓
Automation Engine
    ↓
Execution Result
    ↓
Display to User
```

## Configuration

Edit `config.json` to customize:

- Gemini model and temperature
- Safety settings
- Communication method
- Automation parameters

## Testing

Run the test suite:

```bash
python test_ai_brain_main.py
```

## Troubleshooting

### "Gemini API key not configured"
- Set the `GEMINI_API_KEY` environment variable
- Or update `config.json` with your API key

### "No result received (timeout)"
- Make sure the automation engine is running
- Check that the communication layer is working
- Verify the `shared/messages` directory exists

### Low confidence warnings
- Try being more specific in your commands
- Use the help command to see examples
- Check that your command matches supported actions
