# Alvioli - AI-Powered OS Automation for Linux

Alvioli is a terminal-first AI automation system that can perform complex multi-step tasks across your Linux system using natural language commands. It intelligently combines terminal operations with browser automation to accomplish sophisticated workflows.

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

This will install three commands:
- `alvioli` - Main application
- `alido` - General-purpose automation (recommended)
- `ali` - Mode-specific automation

## Usage

### General Purpose Commands (Recommended)

Use `alido` for most tasks - it automatically determines the best execution approach:

```bash
# Install and open applications
alido install and open upscayl

# Search and download content
alido search for good wallpapers with a dark aesthetic

# Development tasks
alido create a portfolio website from ~/resume.pdf

# System management
alido update system and install docker
```

### Mode-Specific Commands

Use `ali` with subcommands when you want to force a specific execution mode:

```bash
# Terminal-first execution
ali ter "set up development environment"

# Browser-first execution  
ali brw "generate mail summary"

# Auto-mode selection
ali do "install chrome and create a github repo named ai-server"
```

## Examples

### Email Management
```bash
alido read my gmail and summarize important emails
```

### Development Workflow
```bash
alido use ~/portfolio.pdf to create a beautiful website and deploy it
```

### System Administration
```bash
alido install docker, set up a nginx container, and configure it for my website
```

### Content Creation
```bash
alido download some dark aesthetic wallpapers and set one as my background
```

## How It Works

1. **Command Parsing**: Alvioli analyzes your natural language command
2. **Task Planning**: Breaks down the task into executable steps
3. **Intelligent Execution**: Uses terminal commands primarily, browser automation when needed
4. **Error Recovery**: Automatically handles failures with progressive retry strategies
5. **Learning**: Stores successful patterns and solutions for future use

## Configuration

Alvioli creates a configuration file at `~/.alvioli/config.json` on first run. You can customize:

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