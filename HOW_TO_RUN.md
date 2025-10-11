# How to Run the Voice-Enabled AI Automation Assistant

## ✅ Voice Input is Now Ready!

Your system successfully recognized "search for Elon Musk" via voice! The only issue is that the automation engine needs to be running to execute the workflows.

## Quick Start (Easiest Method)

### Option 1: Use the Startup Script (Recommended)

1. **Set your Gemini API Key** (one time setup):
   ```powershell
   $env:GEMINI_API_KEY="your_api_key_here"
   ```

2. **Run the startup script**:
   ```bash
   cd c:\Users\amaan\Downloads\taskX-main\taskX-main
   start_with_voice.bat
   ```

This script will:
- Start the Automation Engine in a separate window
- Start the AI Brain with voice input
- You can now use voice commands and see them execute!

### Option 2: Manual Start (Two Terminals)

**Terminal 1 - Automation Engine:**
```bash
cd c:\Users\amaan\Downloads\taskX-main\taskX-main
python -m automation_engine.main
```

**Terminal 2 - AI Brain with Voice:**
```bash
cd c:\Users\amaan\Downloads\taskX-main\taskX-main
python -m ai_brain.main
```

## Using Voice Commands

Once both components are running:

1. **Test Microphone**:
   ```
   test mic
   ```

2. **Enable Voice Mode**:
   ```
   voice
   ```

3. **Speak Your Commands**:
   - Wait for "🎤 Listening..." prompt
   - Speak clearly: "click the submit button"
   - Or: "type hello world"
   - Or: "search for Python tutorials"

4. **Switch Back to Text**:
   - Type: `text`
   - Or say: "text mode"

## What Happened in Your Test?

✅ **What Worked:**
- Voice input recognized perfectly: "search for Elon Musk"
- AI Brain parsed the command correctly (98% confidence)
- Workflow was generated with 6 steps
- Workflow was sent successfully

❌ **What Didn't Work:**
- The Automation Engine wasn't running
- So the workflow couldn't be executed
- Message: "No result received (timeout or automation engine not running)"

## The Fix

**You need BOTH components running:**

1. **AI Brain** = Takes your voice/text input, generates workflows
2. **Automation Engine** = Executes the workflows on your computer

Think of it like this:
- **AI Brain** = The "brain" that understands what you want
- **Automation Engine** = The "hands" that actually do it

## Architecture Diagram

```
You (Voice) --> AI Brain --> Workflow File --> Automation Engine --> Execute
     ↑            ↓                                    ↓
  Microphone   Gemini AI                          Your Computer
                                                  (mouse, keyboard)
```

## Next Steps

1. **Set your Gemini API Key** (required):
   - Get it from: https://makersuite.google.com/app/apikey
   - Set it: `$env:GEMINI_API_KEY="your_key_here"`

2. **Run the startup script**:
   ```bash
   start_with_voice.bat
   ```

3. **Try your voice command again**:
   - Type `voice` to enable voice mode
   - Say "search for Elon Musk"
   - Watch it execute! ✨

## Communication Between Components

The two components communicate via JSON files in:
```
taskX-main/shared/messages/
├── workflows/  (AI Brain → Automation Engine)
└── status/     (Automation Engine → AI Brain)
```

- When you give a voice command, AI Brain creates a workflow file
- Automation Engine picks it up and executes it
- Then sends back status through a status file
- AI Brain displays the result

## Troubleshooting

### "No result received (timeout...)"
✅ **Solution**: Start the Automation Engine in a separate terminal

### "Voice input is not available"
- Check microphone is connected
- Install PyAudio: `pip install pyaudio`

### "Error: Gemini API key not configured"
- Set the environment variable: `$env:GEMINI_API_KEY="your_key"`

### Both components running but no execution
- Check the `shared/messages/workflows/` folder exists
- Try restarting both components

## Tips for Best Experience

1. **Always start Automation Engine first** (wait 2-3 seconds)
2. **Then start AI Brain**
3. **Test microphone** before using voice mode
4. **Speak clearly** and wait for "Listening..." prompt
5. **Confirm workflows** before they execute
6. **Keep both terminal windows open**

## Example Session

```
# Terminal 1 (Automation Engine)
$ python -m automation_engine.main
==================================================
Automation Engine Started
==================================================
Waiting for workflows from AI Brain...

# Terminal 2 (AI Brain)
$ python -m ai_brain.main
Welcome to AI Automation Assistant!

> test mic
✓ Microphone is available

> voice
🎤 Voice mode enabled!

🎤 VOICE MODE
🎤 Listening... (speak now)

[You say: "search for Python tutorials"]

✓ Recognized: search for Python tutorials
→ Analyzing command with Gemini...
→ Generating workflow...
Send workflow to automation engine? [y/n] (y): y
✓ Workflow sent
→ Waiting for execution result...
✓ Execution SUCCESS
```

Enjoy your voice-controlled automation! 🎤🤖
