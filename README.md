# Autopilot - Kira AI Assistant for Linux

Kira is an intelligent AI automation system that can perform complex tasks across your Linux system using natural language commands. It uses advanced AI to understand your intent and execute the appropriate commands safely and efficiently.

## Features

- **Natural Language Commands**: Tell Alvioli what you want in plain English
- **Terminal-First Approach**: Prioritizes command-line solutions for efficiency
- **Intelligent Error Handling**: Automatically retries, searches for solutions, and learns from failures
- **Browser Automation**: Seamlessly handles web-based tasks when needed
- **Context Memory**: Remembers information across sessions to improve efficiency
- **Progressive Learning**: Gets better at solving problems over time

## Installation

### From Source

```bash
# Clone the repository
git clone <repository-url>
cd alvioli

# Build and install
make install
```

This will install the Kira command:
- `kira` - AI-powered automation assistant

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

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run `make test` and `make lint`
6. Submit a pull request

## License

[License information to be added]

## Roadmap

- [ ] Core command parsing and execution
- [ ] Terminal engine with error handling
- [ ] Browser automation integration
- [ ] Context memory and learning system
- [ ] Web search for error solutions
- [ ] Advanced task coordination
- [ ] Plugin system for extensibility
- [ ] GUI companion application

## Support

For issues, questions, or contributions, please visit the project repository or create an issue.