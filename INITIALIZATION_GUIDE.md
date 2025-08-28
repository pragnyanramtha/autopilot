# AP Initialization Guide

## Overview

AP now features an intelligent initialization system that automatically guides users through setup on their first run. This eliminates the need for manual configuration and provides a smooth onboarding experience.

## Features Implemented

### 1. First-Time Setup Flow

When a user runs `ap` for the first time, the system automatically:

1. **Detects first-time usage** - Checks if configuration exists
2. **Guides API key setup** - Interactive prompts to get Gemini API key
3. **Performs system detection** - Automatically detects OS, package managers, etc.
4. **Creates initial configuration** - Saves user preferences and system info

### 2. Subsequent Launch Behavior

On the second run, AP will:

1. **Check API key configuration** - Ensures API key is properly set
2. **Show preferences setup** - Optional configuration of user preferences
3. **Skip to normal operation** - If everything is configured

### 3. New Commands Added

#### `ap preferences` (or `ap prefs`)
- Configure user preferences interactively
- Set preferred package manager
- Configure automation level
- Set display preferences

#### `ap file` - File Management Operations
- `ap file --read <path>` - Read file content
- `ap file --write <path> --content "text"` - Write to file
- `ap file --append <path> --content "text"` - Append to file
- `ap file --list <directory>` - List directory contents
- `ap file --info <path>` - Get file information
- `ap file --search <pattern> --in <dir>` - Search for files

### 4. Configuration System

#### Configuration Location
- User config: `~/.ap/config.json`
- Environment variables: `.env` file in project root

#### Configuration Structure
```json
{
  "geminiApiKey": "your_api_key",
  "preferredPackageManager": "apt",
  "preferredShell": "/bin/bash",
  "systemInfo": { ... },
  "userPreferences": {
    "name": "user",
    "workingDirectory": "/home/user",
    "autoUpdate": false,
    "verboseOutput": false
  },
  "createdAt": "2024-01-01T00:00:00.000Z",
  "updatedAt": "2024-01-01T00:00:00.000Z"
}
```

## Usage Examples

### First Time Setup
```bash
# First run - automatic setup
ap

# Follow the prompts:
# 1. Get API key from https://aistudio.google.com/app/apikey
# 2. Enter API key when prompted
# 3. System detection runs automatically
# 4. Configuration is saved
```

### Subsequent Usage
```bash
# Normal usage after setup
ap install git
ap check disk space
ap help me set up development environment

# Configure preferences
ap preferences

# File operations
ap file --read README.md
ap file --write notes.txt --content "My notes"
ap file --list /home/user/projects
```

### Status and Information
```bash
# Check system status
ap status

# Check configuration
ap preferences

# System detection
ap detect
```

## File Management Capabilities

The new FileManager utility provides comprehensive file operations:

### Reading Files
```typescript
const result = FileManager.readFile('path/to/file.txt');
if (result.success) {
  console.log(result.data); // File content
}
```

### Writing Files
```typescript
const result = FileManager.writeFile('path/to/file.txt', 'content', { createDir: true });
```

### Directory Operations
```typescript
const result = FileManager.listDirectory('/path/to/directory');
const result = FileManager.createDirectory('/path/to/new/dir', { recursive: true });
```

### File Search
```typescript
const result = FileManager.searchFiles('/path/to/search', /\.js$/);
```

## System Detection

Enhanced system detection now includes:

- **Operating System**: Detailed OS information
- **Hardware**: CPU, memory, disk information
- **Package Managers**: Auto-detection of available package managers
- **Development Tools**: Detection of installed development tools
- **Network**: Connectivity and network information

## Error Handling

The initialization system includes comprehensive error handling:

- **API Key Validation**: Ensures API key format is correct
- **File System Errors**: Graceful handling of permission issues
- **Network Issues**: Fallback for system detection failures
- **User Cancellation**: Allows users to cancel setup at any point

## Migration from Previous Versions

If you have an existing AP installation:

1. **Backup existing configuration**: Copy your `.env` file
2. **Run AP**: The new system will detect existing configuration
3. **Update preferences**: Use `ap preferences` to update settings
4. **Verify setup**: Run `ap status` to confirm everything works

## Troubleshooting

### Common Issues

1. **API Key Not Working**
   - Verify key at https://aistudio.google.com/app/apikey
   - Check `.env` file format: `GEMINI_API_KEY=your_key_here`
   - Run `ap preferences` to reconfigure

2. **Permission Errors**
   - Ensure write permissions to home directory (`~/.ap/`)
   - Check file permissions on `.env` file

3. **System Detection Fails**
   - Run `ap detect --script` for alternative detection method
   - Check if bash is available and executable

### Getting Help

- Run `ap --help` for command overview
- Run `ap status` to check configuration
- Check logs in terminal output
- Visit: https://github.com/pragnyanramtha/autopilot/issues

## Development Notes

### Architecture Changes

1. **FirstTimeSetup Class**: Handles initialization flow
2. **FileManager Utility**: Provides file operations
3. **Enhanced CLI**: Integrated initialization checks
4. **Configuration Management**: Centralized config handling

### Key Files Modified

- `src/cli.ts` - Main CLI with initialization integration
- `src/setup/FirstTimeSetup.ts` - New initialization system
- `src/utils/FileManager.ts` - File management utilities
- `README.md` - Updated documentation

### Testing

The initialization system can be tested by:

1. Removing existing configuration: `rm -rf ~/.ap/`
2. Running AP: `npm run dev`
3. Following the setup prompts
4. Verifying configuration: `cat ~/.ap/config.json`

This provides a complete, user-friendly initialization experience that eliminates manual setup steps and provides immediate value to new users.