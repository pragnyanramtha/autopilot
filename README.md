# Autopilot - Kira AI Assistant for Linux

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-blue.svg)](https://www.typescriptlang.org/)
[![AI Powered](https://img.shields.io/badge/AI-Gemini%20Powered-orange.svg)](https://ai.google.dev/)

Kira is an intelligent AI automation system that can perform complex tasks across your Linux system using natural language commands. It uses advanced AI to understand your intent and execute the appropriate commands safely and efficiently.

## ✨ Features

- **🤖 AI-Powered**: Uses Google Gemini for intelligent command understanding
- **🐧 Linux Native**: Built specifically for Linux with multi-distro support
- **📦 Smart Package Management**: Auto-detects and uses the right package manager (apt, pacman, yum, etc.)
- **🔧 Progressive Error Handling**: Automatically retries, analyzes errors, and suggests solutions
- **👤 Personalized**: Learns your preferences and system configuration
- **🛡️ Safe & Secure**: Conservative approach with user confirmation for risky operations
- **🎯 Context Aware**: Remembers your setup and preferences across sessions

## 🚀 Quick Start

```bash
# 1. Clone and install
git clone https://github.com/pragnyanramtha/autopilot.git
cd autopilot
npm install && npm run build

# 2. Initialize Kira (first-time setup)
kira init

# 3. Start using Kira!
kira check disk space
kira install git
kira help me set up a development environment
```

## 📦 Installation

### From Source

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

This will install the Kira command:
- `kira` - AI-powered automation assistant

### 🤖 AI Setup (Optional but Recommended)

For enhanced AI capabilities, get a free Gemini API key:

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a free API key
3. Add it to your `.env` file:
   ```bash
   echo "GEMINI_API_KEY=your_api_key_here" >> .env
   ```

Without an API key, Kira will use built-in command parsing (still very capable!).

## Usage

### Usage

Use `kira` for any task - it intelligently analyzes and executes your commands:

```bash
# Install and open applications
kira install and open firefox

# System management
kira update system and install docker

# Development tasks
kira create a portfolio website from ~/resume.pdf

# File operations
kira create directory named projects and clone my repo

# System monitoring
kira check disk space and memory usage
```

## Examples

### Email Management
```bash
kira read my gmail and summarize important emails
```

### Development Workflow
```bash
kira use ~/portfolio.pdf to create a beautiful website and deploy it
```

### System Administration
```bash
kira install docker, set up a nginx container, and configure it for my website
```

### Content Creation
```bash
kira download some dark aesthetic wallpapers and set one as my background
```

## How It Works

1. **AI Analysis**: Kira uses advanced AI to understand your natural language command
2. **Intelligent Planning**: Breaks down complex tasks into safe, executable steps
3. **Smart Execution**: Automatically detects your Linux distribution and uses appropriate commands
4. **Error Recovery**: Intelligently handles failures with distribution-aware solutions
5. **Learning**: Continuously improves through AI-powered error analysis

## Configuration

Kira creates a configuration file at `~/.env` on first run. You can customize:

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
alvioli/
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

**Pragnya Ramtha** - [@pragnyanramtha](https://github.com/pragnyanramtha)

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