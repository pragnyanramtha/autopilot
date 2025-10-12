# Voice Input Setup Guide

The AI Automation Assistant now supports voice input! Users can speak their commands instead of typing them.

## Features

- **Voice-to-Text**: Speak your automation commands naturally
- **Easy Toggle**: Switch between voice and text mode with simple commands
- **Microphone Test**: Test your microphone before using voice mode
- **Automatic Speech Recognition**: Uses Google's speech recognition service

## Installation

### 1. Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install PyAudio (Platform-Specific)

**Windows:**
```bash
pip install pyaudio
```

If you encounter issues, download the appropriate `.whl` file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install:
```bash
pip install PyAudio‑0.2.11‑cp310‑cp310‑win_amd64.whl
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

## Usage

### Starting the Application

```bash
python -m ai_brain.main
```

### Using Voice Mode

1. **Test Your Microphone** (recommended first step):
   ```
   test mic
   ```

2. **Enable Voice Mode**:
   ```
   voice
   ```
   or
   ```
   voice mode
   ```

3. **Speak Your Command**:
   - Wait for the "🎤 Listening..." prompt
   - Speak clearly into your microphone
   - The system will transcribe your speech and process the command

4. **Switch Back to Text Mode**:
   ```
   text
   ```
   or say "text mode" while in voice mode

### Example Voice Commands

Once in voice mode, you can say things like:
- "Click the submit button"
- "Type hello world"
- "Open Chrome"
- "Search for Python tutorials"
- "Move mouse to center"
- "Text mode" (to switch back to typing)

### Special Voice Commands

- **"voice" / "voice mode" / "enable voice"** - Enable voice input
- **"text" / "text mode" / "disable voice"** - Switch to text input
- **"test mic" / "test microphone"** - Test microphone availability
- **"status"** - Show system status including voice input status
- **"exit" / "quit"** - Exit the application

## How It Works

1. **Speech Capture**: Uses your system microphone to capture audio
2. **Speech-to-Text**: Sends audio to Google's Speech Recognition API
3. **Command Processing**: The transcribed text is processed the same way as typed commands
4. **Workflow Execution**: The AI Brain generates and executes the automation workflow

## Troubleshooting

### Voice Input Not Available

If voice input shows as unavailable:

1. **Check Microphone Connection**: Ensure your microphone is properly connected
2. **Install PyAudio**: Make sure PyAudio is installed correctly
3. **Check Permissions**: Grant microphone access to your terminal/Python
4. **Test Microphone**: Use the `test mic` command

### Recognition Issues

If the system can't understand your speech:

- **Speak Clearly**: Enunciate your words clearly
- **Reduce Background Noise**: Use voice mode in a quiet environment
- **Check Internet Connection**: Google Speech Recognition requires internet
- **Adjust Microphone Position**: Place microphone closer to your mouth

### "No speech detected (timeout)"

- The system waited but didn't hear any speech
- Try speaking sooner after the "Listening..." prompt
- Check if your microphone is working and not muted

### PyAudio Installation Errors

**Windows**: Download pre-built wheel files from unofficial sources
**macOS**: Install portaudio first using Homebrew
**Linux**: Install system packages for portaudio development files

## Technical Details

### Dependencies

- **SpeechRecognition**: Python library for speech recognition
- **PyAudio**: Python bindings for PortAudio (audio I/O)
- **Google Speech Recognition API**: Free speech-to-text service (requires internet)

### Files Modified

- `ai_brain/main.py` - Added voice mode toggle and command input routing
- `ai_brain/voice_input.py` - New module handling voice input
- `requirements.txt` - Added SpeechRecognition and PyAudio

### Privacy Note

Voice commands are sent to Google's Speech Recognition service for transcription. Only the audio of your commands is sent, not your screen content or automation actions.

## Advanced Usage

### Continuous Voice Mode

The system processes one command at a time. After each command:
1. The automation executes
2. System returns to voice input mode
3. Speak your next command

### Mixing Voice and Text

You can freely switch between voice and text modes:
- Use voice for complex commands
- Switch to text for quick single-word commands
- Use text mode for commands with special characters

## Support

If you encounter issues:

1. Run `status` to check component status
2. Run `test mic` to verify microphone
3. Check that all dependencies are installed
4. Ensure you have internet connection
5. Review error messages in the console

## Future Enhancements

Potential improvements:
- Offline speech recognition
- Multiple language support
- Custom wake word ("Hey Assistant")
- Voice feedback/confirmation
- Continuous listening mode
