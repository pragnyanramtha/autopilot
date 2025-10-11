# Launcher Scripts Guide

## Quick Start

**Just double-click:** `quick_start.bat`

This is the easiest way to start! It will:
- Check if everything is set up correctly
- Show you a menu to choose what to start
- Handle venv activation automatically
- Provide helpful error messages

## Available Launchers

### 1. `quick_start.bat` ⭐ RECOMMENDED
**Interactive menu with system checks**

Features:
- ✓ Checks venv, .env, and API key
- ✓ Menu to start AI Brain, Automation Engine, or both
- ✓ Run tests
- ✓ Check system status
- ✓ Safe and user-friendly

**Usage:** Just double-click the file!

---

### 2. `start_ai_brain.bat`
**Start AI Brain only**

What it does:
- Checks venv exists
- Checks .env file exists
- Checks API key is set
- Activates venv
- Starts AI Brain

**Usage:** Double-click or run from command line
```cmd
start_ai_brain.bat
```

---

### 3. `start_automation_engine.bat`
**Start Automation Engine only**

What it does:
- Checks venv exists
- Asks if you want DRY-RUN mode (safe testing)
- Activates venv
- Starts Automation Engine

**Usage:** Double-click or run from command line
```cmd
start_automation_engine.bat
```

**Options:**
- DRY-RUN mode: Simulates actions (safe for testing)
- LIVE mode: Actually controls your computer

---

### 4. `start_both.bat`
**Start both components in separate windows**

What it does:
- Checks venv and .env
- Opens Automation Engine in one window
- Opens AI Brain in another window
- Both run simultaneously

**Usage:** Double-click or run from command line
```cmd
start_both.bat
```

**Note:** You'll see two command windows - one for each component.

---

## Troubleshooting

### "Virtual environment not found"
**Solution:** Run `setup_venv.bat` first to create the virtual environment.

### ".env file not found"
**Solution:** Create a `.env` file in the project root with:
```
GEMINI_API_KEY=your_api_key_here
```

Get your API key from: https://makersuite.google.com/app/apikey

### "GEMINI_API_KEY not found in .env"
**Solution:** Open `.env` file and add:
```
GEMINI_API_KEY=your_actual_api_key
```

### "Missing dependencies"
**Solution:** Activate venv and install requirements:
```cmd
venv\Scripts\activate.bat
pip install -r requirements.txt
```

### Python version error
**Solution:** Requires Python 3.10 or higher. Check version:
```cmd
python --version
```

---

## What Each Component Does

### AI Brain
- Accepts natural language commands
- Analyzes commands with Gemini AI
- Generates workflows
- Sends workflows to Automation Engine
- Shows results

**Example commands:**
- "Click the submit button"
- "Search for trending topics and post to X"
- "Write an article about AI"

### Automation Engine
- Receives workflows from AI Brain
- Controls mouse and keyboard
- Executes workflows step-by-step
- Reports results back to AI Brain

**Safety features:**
- DRY-RUN mode for testing
- Emergency stop (Ctrl+C)
- User interrupt detection

---

## Tips

### First Time Setup
1. Run `setup_venv.bat` to create virtual environment
2. Create `.env` file with your API key
3. Run `quick_start.bat` and choose option 6 to check status
4. If all checks pass, choose option 4 to start both components

### Daily Use
1. Double-click `quick_start.bat`
2. Choose option 4 (Start BOTH)
3. Give commands in the AI Brain window
4. Watch automation happen in real-time

### Testing
1. Use `quick_start.bat` → option 2 (DRY-RUN mode)
2. Or run `start_automation_engine.bat` and choose DRY-RUN
3. Test commands without actually controlling your computer

### Stopping
- Press `Ctrl+C` in any window to stop that component
- Or just close the window
- To stop both: close both windows

---

## Advanced Usage

### Run from Command Line
```cmd
# Activate venv
venv\Scripts\activate.bat

# Start AI Brain
python -m ai_brain.main

# Start Automation Engine (in another terminal)
python -m automation_engine.main

# Start Automation Engine in DRY-RUN mode
python -m automation_engine.main --dry-run
```

### Run Tests
```cmd
venv\Scripts\activate.bat
python test_complex_workflows.py
```

### Check Status
Use `quick_start.bat` → option 6, or:
```cmd
venv\Scripts\activate.bat
python -c "import sys; print(f'Python: {sys.version}')"
python -c "import google.generativeai; print('Gemini: OK')"
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(f'API Key: {os.getenv(\"GEMINI_API_KEY\")[:20]}...')"
```

---

## Quick Reference

| Want to... | Use this |
|------------|----------|
| Start everything easily | `quick_start.bat` |
| Just use AI Brain | `start_ai_brain.bat` |
| Just test automation | `start_automation_engine.bat` (choose DRY-RUN) |
| Run full system | `start_both.bat` |
| Check if setup is correct | `quick_start.bat` → option 6 |
| Run tests | `quick_start.bat` → option 5 |

---

## Need Help?

1. Run `quick_start.bat` → option 6 to check system status
2. Check error messages - they usually tell you what's wrong
3. Make sure you have:
   - Python 3.10+
   - Virtual environment created (`setup_venv.bat`)
   - `.env` file with API key
   - All dependencies installed (`pip install -r requirements.txt`)

---

**Happy Automating! 🚀**
