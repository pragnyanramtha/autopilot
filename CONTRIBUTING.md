# Contributing to Autopilot (AP)

Thank you for your interest in contributing to AP! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Linux or macOS system (for testing)
- Git
- **macOS only**: Xcode Command Line Tools (`xcode-select --install`)

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/autopilot.git
   cd autopilot
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Set up Development Environment**
   ```bash
   # macOS: Run setup script (optional but recommended)
   ./scripts/setup-macos.sh
   
   # Copy environment template
   cp .env.example .env
   
   # Add your Gemini API key (REQUIRED)
   # Get it from: https://aistudio.google.com/app/apikey
   echo "GEMINI_API_KEY=your_api_key_here" >> .env
   ```

4. **Build and Test**
   ```bash
   npm run build
   npm test
   npm run dev ap init  # Test the application
   ```

## 🛠️ Development Workflow

### Project Structure

```
autopilot/
├── src/
│   ├── ai/              # AI service (Gemini integration)
│   ├── cli/             # Command-line interface
│   ├── parser/          # Command parsing logic
│   ├── terminal/        # Terminal execution engine
│   ├── profile/         # User profile management
│   ├── setup/           # Initialization wizards
│   └── types/           # TypeScript interfaces
├── scripts/             # System detection scripts
├── tests/               # Test files
└── docs/                # Documentation
```

### Making Changes

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   npm run build
   npm test
   npm run lint
   
   # Test manually
   npm run dev ap your-test-command
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add amazing new feature"
   ```

   Use conventional commit messages:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `refactor:` for code refactoring
   - `test:` for adding tests

## 🎯 Areas for Contribution

### High Priority
- **Browser Automation**: Implement web interaction capabilities
- **Plugin System**: Create extensible architecture for custom commands
- **Error Recovery**: Enhance AI-powered error analysis and solutions
- **Testing**: Add comprehensive test coverage

### Medium Priority
- **Package Manager Support**: Add support for more Linux distributions and improve macOS integration
- **Performance**: Optimize command execution and AI response times
- **Documentation**: Improve user guides and API documentation
- **Internationalization**: Add support for multiple languages
- **macOS Features**: Enhanced App Store integration, system preferences automation

### Low Priority
- **GUI Interface**: Desktop application companion
- **Cloud Integration**: Remote execution capabilities
- **Advanced AI**: Fine-tuning and custom models

## 🧪 Testing

### Running Tests
```bash
# Run all tests
npm test

# Run specific test file
npm test -- --grep "CommandParser"

# Run with coverage
npm run test:coverage
```

### Writing Tests
- Place test files in the `tests/` directory
- Use descriptive test names
- Test both success and failure scenarios
- Mock external dependencies (AI API calls, system commands)

### Manual Testing
```bash
# Test basic functionality
npm run dev ap check disk space
npm run dev ap install git

# Test initialization
rm -rf ~/.ap && npm run dev init

# Test error handling
npm run dev ap nonexistent-command
```

## 📝 Code Style

### TypeScript Guidelines
- Use strict TypeScript configuration
- Prefer interfaces over types for object shapes
- Use meaningful variable and function names
- Add JSDoc comments for public APIs

### Formatting
- Use Prettier for code formatting
- Follow ESLint rules
- Use 2 spaces for indentation
- Maximum line length: 100 characters

### AI Integration
- Always handle AI API failures gracefully
- Provide fallback behavior when AI is unavailable
- Use timeouts to prevent hanging requests
- Log AI interactions for debugging

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - OS and distribution
   - Node.js version
   - AP version
   - Terminal and shell

2. **Steps to Reproduce**
   - Exact commands used
   - Expected behavior
   - Actual behavior

3. **Additional Context**
   - Error messages
   - Log files
   - Screenshots (if applicable)
   - Package manager availability (`brew --version`, `apt --version`, etc.)

## 💡 Feature Requests

For feature requests, please:

1. Check existing issues first
2. Describe the use case clearly
3. Explain why it would be valuable
4. Consider implementation complexity
5. Provide examples of usage

## 🔒 Security

If you discover a security vulnerability:

1. **DO NOT** create a public issue
2. Email the maintainer directly
3. Provide detailed information about the vulnerability
4. Allow time for the issue to be addressed before disclosure

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## 🤝 Community

- Be respectful and inclusive
- Help others learn and grow
- Share knowledge and best practices
- Celebrate successes together

## 📞 Getting Help

- **Issues**: https://github.com/pragnyanramtha/autopilot/issues
- **Discussions**: https://github.com/pragnyanramtha/autopilot/discussions
- **Email**: pragnyanramtha@gmail.com

Thank you for contributing to AP! 🚀