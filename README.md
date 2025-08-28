# Autopilot - AP AI Assistant for Linux & macOS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-blue.svg)](https://www.typescriptlang.org/)
[![AI Powered](https://img.shields.io/badge/AI-Gemini%20Powered-orange.svg)](https://ai.google.dev/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/pragnyanramtha/autopilot)

AP is an intelligent AI automation system that can perform complex tasks across your Linux and macOS systems using natural language commands. It uses advanced AI to understand your intent and execute the appropriate commands safely and efficiently.

## ✨ Features

- **🚀 Automatic Setup**: First-time initialization guides you through configuration
- **🤖 AI-Powered**: Uses Google Gemini for intelligent command understanding
- **🖥️ Cross-Platform**: Native support for Linux and macOS
- **📦 Smart Package Management**: Auto-detects and uses the right package manager
  - **Linux**: apt, pacman, yum, dnf, zypper, snap, flatpak
  - **macOS**: Homebrew, Homebrew Cask, Mac App Store (mas), MacPorts
- **🔧 Progressive Error Handling**: Automatically retries, analyzes errors, and suggests solutions
- **👤 Personalized**: Learns your preferences and system configuration
- **🛡️ Safe & Secure**: Conservative approach with user confirmation for risky operations
- **🎯 Context Aware**: Remembers your setup and preferences across sessions
- **📁 File Management**: Built-in file operations for reading, writing, and searching files

## 🚀 Quick Start

```bash
# 1. Clone and install
git clone https://github.com/pragnyanramtha/autopilot.git
cd autopilot
npm install && npm run build

# 2. First run - AP will guide you through setup automatically
ap

# 3. Start using AP!
ap check disk space
ap install git
ap help me set up a development environment
```

## 📦 Installation

### From Source

#### Linux
```bash
# Clone the repository
git clone https://github.com/pragnyanramtha/autopilot.git
cd autopilot

# Install dependencies
npm install

# Build the project
npm run build

# Install globally (optional)
npm install -g .
```

#### macOS
```bash
# Clone the repository
git clone https://github.com/pragnyanramtha/autopilot.git
cd autopilot

# Run macOS setup script (installs Homebrew, Node.js, etc.)
./scripts/setup-macos.sh

# Install dependencies
npm install

# Build the project
npm run build

# Install globally (optional)
npm install -g .
```

This will install the AP command:
- `ap` - AI-powered automation assistant

### 🤖 AI Setup (AUTOMATIC)

AP will automatically guide you through setting up your FREE Gemini API key on first run:

1. **Run AP for the first time**: `ap`
2. **Follow the interactive setup** - AP will guide you to get your API key
3. **Visit Google AI Studio**: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
4. **Copy your key** and paste it when prompted

**The Gemini API is FREE** with generous limits:
- ✅ 15 requests per minute
- ✅ 1 million tokens per minute  
- ✅ 1,500 requests per day

**Alternative link**: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

## Usage

### Usage

Use `ap` for any task - it intelligently analyzes and executes your commands:

```bash
# Install and open applications
ap install and open firefox

# System management
ap update system and install docker

# Development tasks
ap create a portfolio website from ~/resume.pdf

# File operations
ap create directory named projects and clone my repo

# System monitoring
ap check disk space and memory usage
```

## Examples

### First Time Usage
```bash
# First run - AP guides you through setup automatically
ap

# After setup, use AP for any task:
ap install and open firefox
ap check disk space and memory usage
ap help me set up a development environment
```

### Cross-Platform
```bash
# Install and open applications
ap install and open firefox
ap install visual studio code

# System management  
ap update system and install docker
ap check disk space and memory usage
```

### Configuration and Preferences
```bash
# Configure your preferences
ap preferences

# Check system status
ap status

# File management
ap file --read README.md
ap file --write notes.txt --content "My project notes"
ap file --list ~/projects
```

### Linux-Specific
```bash
# Package management
ap install git using apt
ap install discord via snap

# System administration
ap set up nginx and configure firewall
```

### macOS-Specific
```bash
# Homebrew packages
ap install git
ap install --cask visual studio code
ap install --cask firefox

# Mac App Store apps
ap install xcode from app store
ap install pages --mas

# System management
ap update homebrew and upgrade all packages
ap install development tools for ios
```

### Development Workflow
```bash
ap use ~/portfolio.pdf to create a beautiful website and deploy it
ap set up a react development environment
ap create a new node project with typescript
```

### Content Creation
```bash
ap download some dark aesthetic wallpapers and set one as my background
ap organize my downloads folder by file type
```

## How It Works

1. **AI Analysis**: AP uses advanced AI to understand your natural language command
2. **Intelligent Planning**: Breaks down complex tasks into safe, executable steps
3. **Smart Execution**: Automatically detects your Linux distribution and uses appropriate commands
4. **Error Recovery**: Intelligently handles failures with distribution-aware solutions
5. **Learning**: Continuously improves through AI-powered error analysis

## Configuration

AP creates a configuration file at `~/.env` on first run. You can customize:

- Browser settings and timeouts
- Terminal shell and command timeouts
- Security settings and blocked commands
- Learning and context retention settings
- Output formatting and verbosity

## Error Handling

Alvioli uses a progressive error handling approach:

1. **Immediate Retry**: Tries the same command again for transient issues
2. **Smart Retry**: Analyzes the error and tries alternative approaches
3. **Web Search**: Searches online for solutions to the specific error
4. **User Guidance**: Presents options when automatic resolution fails

## Security

- Commands requiring root access explain why before execution
- Configurable safe mode and command blocking
- No credential storage - uses existing browser sessions and SSH keys
- Respects system permissions and user boundaries

## Development

### Building

```bash
# Development build
make dev

# Production build
make build

# Run tests
make test

# Format code
make fmt
```

### Project Structure

```
autopilot/
├── cmd/                    # Application entry point
├── internal/
│   ├── cli/               # Command-line interface
│   ├── config/            # Configuration management
│   ├── types/             # Core interfaces and types
│   ├── parser/            # Command parsing logic
│   ├── planner/           # Task planning
│   ├── terminal/          # Terminal execution engine
│   ├── browser/           # Browser automation engine
│   ├── context/           # Context and memory management
│   └── coordinator/       # Execution coordination
├── pkg/                   # Public packages
└── tests/                 # Test files
```

## Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run `npm test` and `npm run lint`
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Pragnyan Ramtha** - [@pragnyanramtha](https://github.com/pragnyanramtha)

## Roadmap

- [x] Core command parsing and execution
- [x] Terminal engine with error handling
- [x] AI-powered command analysis
- [x] Progressive error handling with solutions
- [x] User profile and system detection
- [x] Multi-package manager support
- [ ] Browser automation integration
- [ ] Context memory and learning system
- [ ] Web search for error solutions
- [ ] Advanced task coordination
- [ ] Plugin system for extensibility
- [ ] GUI companion application

## Support

For issues, questions, or contributions, please visit:
- **Repository**: https://github.com/pragnyanramtha/autopilot
- **Issues**: https://github.com/pragnyanramtha/autopilot/issues
- **Discussions**: https://github.com/pragnyanramtha/autopilot/discussions