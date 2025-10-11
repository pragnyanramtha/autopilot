# AI Automation Assistant

**Control your computer with natural language and voice commands.**

Powered by Google Gemini AI, this assistant understands what you want to do and executes it automatically.

---

## 🚀 Quick Start

### 1. Setup (First Time)
```cmd
setup_venv.bat
```

### 2. Configure API Key
Create a `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```
Get your key: https://makersuite.google.com/app/apikey

### 3. Run
```cmd
run.bat
```

That's it! 🎉

---

## 💬 Usage

### Text Commands
Just type naturally:
```
search for Python tutorials and open first result
write an article about AI and post to X
click the submit button
```

### Voice Commands (Optional)
Press `V` then speak:
```
🎤 "Search for AI trends"
🎤 "Post to Twitter"
```

---

## 📖 Documentation

### Getting Started
- **[Launcher Guide](docs/LAUNCHER_GUIDE.md)** - All ways to start the app
- **[Quick Start Guide](docs/QUICK_START_COMPLEX_COMMANDS.md)** - Command examples

### Features
- **[Complex Workflows](docs/COMPLEX_WORKFLOW_ENHANCEMENT.md)** - Multi-step automation
- **[Direct Search & Input](docs/DIRECT_SEARCH_AND_INPUT_GUIDE.md)** - Search and voice features
- **[Latest Enhancements](docs/LATEST_ENHANCEMENTS.md)** - What's new

### Technical
- **[Architecture](docs/ARCHITECTURE_ENHANCEMENT.md)** - How it works
- **[Bug Fixes](docs/BUGS_FIXED.md)** - Recent fixes
- **[Implementation Details](docs/IMPLEMENTATION_VERIFICATION.md)** - Technical specs

---

## ✨ Features

### 🎯 Smart Command Understanding
- Natural language processing
- Detects simple vs complex tasks
- Automatic workflow generation

### 🌐 Web Automation
- **15+ websites supported** (X, Facebook, LinkedIn, Gmail, GitHub, etc.)
- Smart navigation with keyboard shortcuts
- Tab-based navigation fallback

### 🎤 Voice Input (Optional)
- Press `V` to speak commands
- Works alongside text input
- Install: `pip install SpeechRecognition pyaudio`

### 🔍 Search Features
- Opens Chrome and searches
- Can open first result automatically
- Example: "search for Python and open first result"

### ✍️ Content Generation
- AI-powered article writing
- Social media posts
- Customizable length and style

### 🔒 Security
- API key in `.env` file (not in code)
- Dry-run mode for testing
- Emergency stop (Ctrl+C)

---

## 📋 Requirements

- **Python 3.10+**
- **Windows** (Linux/Mac support coming)
- **Gemini API Key** (free from Google)

---

## 🎮 Commands

### Simple Actions
```
click the OK button
type hello world
press enter
open Chrome
```

### Web Automation
```
search for AI trends
go to twitter.com
navigate to github.com
```

### Complex Workflows
```
search for Python tutorials and open first result
write an article about AI and post to X
research machine learning and create a summary
```

### Special Commands
```
help     - Show help
voice    - Toggle voice input
exit     - Quit
```

---

## 🛠️ Configuration

Edit `config.json` to customize:

```json
{
  "social_media": {
    "posting_strategy": "tab_navigation",
    "supported_platforms": ["X/Twitter", "Facebook", "LinkedIn", ...]
  }
}
```

**Strategies:**
- `keyboard_shortcut` - Fast (uses N key for Twitter)
- `tab_navigation` - Reliable (presses Tab to navigate)
- `smart` - With verification (uses screen capture)

---

## 📁 Project Structure

```
ai-automation-assistant/
├── run.py                  # 🚀 Main launcher (use this!)
├── run.bat                 # Windows launcher
├── .env                    # API key (create this)
├── config.json             # Configuration
├── requirements.txt        # Dependencies
│
├── ai_brain/              # AI command processing
├── automation_engine/     # Mouse/keyboard control
├── shared/                # Shared utilities
│
├── docs/                  # 📖 Documentation
└── venv/                  # Virtual environment
```

---

## 🐛 Troubleshooting

### "Virtual environment not found"
```cmd
setup_venv.bat
```

### ".env file not found"
Create `.env` with:
```
GEMINI_API_KEY=your_key_here
```

### "Module not found"
```cmd
venv\Scripts\activate.bat
pip install -r requirements.txt
```

### Voice not working
```cmd
pip install SpeechRecognition pyaudio
```

---

## 🎯 Examples

### Example 1: Quick Search
```
> search for Python tutorials

✓ Opens Chrome
✓ Searches "Python tutorials"
✓ Shows results
```

### Example 2: Search and Open
```
> search for best restaurants and open first result

✓ Opens Chrome
✓ Searches "best restaurants"
✓ Presses Tab+Tab+Enter
✓ Opens first result
```

### Example 3: Social Media Post
```
> write an article about AI and post to X

✓ Researches AI topics
✓ Generates article
✓ Opens Chrome
✓ Goes to X.com
✓ Posts content
```

---

## 🤝 Contributing

Contributions welcome! The codebase is clean and well-documented.

---

## 📄 License

MIT License - See LICENSE file

---

## 🙏 Acknowledgments

- **Google Gemini AI** - Natural language processing
- **PyAutoGUI** - Automation
- **Rich** - Beautiful terminal UI

---

## 📞 Support

- **Documentation**: See `docs/` folder
- **Issues**: Check error messages (they're helpful!)
- **Quick Check**: Run `run.bat` and choose option 6

---

**Made with ❤️ for automation enthusiasts**

🚀 **Start now:** `run.bat`
