# Quick Start Guide - Voice-Enabled AI Agent

## Prerequisites

✅ All dependencies are now installed!

## Setup Steps

### 1. Set Your Gemini API Key

You need a Google Gemini API key to use this application. Get one for free at:
https://makersuite.google.com/app/apikey

**Option A: Environment Variable (Recommended)**
```bash
# Windows Command Prompt
set GEMINI_API_KEY=your_api_key_here

# Windows PowerShell
$env:GEMINI_API_KEY="your_api_key_here"

# Linux/Mac
export GEMINI_API_KEY=your_api_key_here
```

**Option B: Config File**
Edit `config.json` in the project root and add your API key.

### 2. Run the Application

```bash
cd c:\Users\amaan\Downloads\taskX-main\taskX-main
python -m ai_brain.main
```

### 3. Test Voice Input

Once the application starts:

1. **Test your microphone first:**
   ```
   test mic
   ```

2. **Enable voice mode:**
   ```
   voice
   ```

3. **Speak your command** when you see "🎤 Listening..."
   - Example: "Click the submit button"
   - Example: "Type hello world"
   - Example: "Open Chrome"

4. **Switch back to text mode:**
   - Type: `text`
   - Or say: "text mode"

## Voice Mode Commands

### Enable Voice
- Type: `voice` or `voice mode` or `enable voice`

### Disable Voice
- Type: `text` or `text mode` or `disable voice`
- Say (in voice mode): "text mode"

### Test Microphone
- Type: `test mic` or `test microphone`

### Get Help
- Type or say: `help`

### Check Status
- Type or say: `status`

### Exit
- Type or say: `exit` or `quit`

## Usage Example Flow

```
# 1. Start the application
python -m ai_brain.main

# 2. Check status
> status

# 3. Test microphone
> test mic

# 4. Enable voice mode
> voice

# 5. Speak your automation commands
🎤 Listening...
(You say: "click the OK button")

# 6. Confirm the workflow
Send workflow to automation engine? (y/n) [y]: y

# 7. Continue with more voice commands or switch to text
(Say: "text mode")
```

## Automation Engine

**IMPORTANT:** The voice input works for the AI Brain component. To actually execute the automation workflows, you need to run the automation engine in a separate terminal:

```bash
# In a new terminal/command prompt
cd c:\Users\amaan\Downloads\taskX-main\taskX-main
python -m automation_engine.main
```

## Troubleshooting

### "Voice input is not available"
- Ensure your microphone is connected
- Check that PyAudio is installed: `pip list | grep -i pyaudio`
- Grant microphone permissions to your terminal/Python

### "No speech detected (timeout)"
- Speak sooner after seeing "Listening..."
- Check that your microphone is not muted
- Increase microphone volume in system settings

### "Could not understand audio"
- Speak more clearly
- Reduce background noise
- Check internet connection (Google Speech Recognition requires internet)

### Unicode/Encoding Errors (Windows)
- The application now automatically fixes Windows console encoding
- If issues persist, try running in Windows Terminal instead of CMD

## Tips for Best Results

1. **Microphone Quality**: Use a good quality microphone for better recognition
2. **Quiet Environment**: Minimize background noise
3. **Clear Speech**: Speak clearly and at a normal pace
4. **Internet Connection**: Ensure stable internet for speech recognition
5. **Test First**: Always run `test mic` before enabling voice mode

## Features Comparison

| Feature | Text Mode | Voice Mode |
|---------|-----------|------------|
| Input Method | Keyboard typing | Microphone speaking |
| Speed | Fast for short commands | Fast for complex commands |
| Accuracy | 100% (what you type) | Depends on speech clarity |
| Internet Required | Only for AI processing | Yes, for speech recognition |
| Best For | Precise input, special characters | Natural language, hands-free |

## Next Steps

1. ✅ Install dependencies (DONE)
2. 🔑 Get and set Gemini API key
3. 🎤 Test microphone
4. 🚀 Start using voice commands
5. 🤖 Run automation engine for workflow execution

Enjoy your voice-enabled AI automation assistant! 🎉
