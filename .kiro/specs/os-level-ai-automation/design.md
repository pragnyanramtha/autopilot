# Design Document

## Overview

Alvioli (alias: ali) is a hybrid CLI/GUI AI automation system for Linux that intelligently executes complex multi-step tasks. It uses a command-based interface where users specify the execution mode (terminal or browser) and provide natural language instructions. The system prioritizes terminal solutions but seamlessly switches to browser automation when needed, with intelligent error handling and authentication management.

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Alvioli Core Engine                      │
├─────────────────────────────────────────────────────────────┤
│  Command Parser  │  Task Planner  │  Execution Coordinator │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐   ┌────────▼────────┐   ┌───────▼────────┐
│ Terminal Engine │   │ Browser Engine  │   │ Context Manager│
├────────────────┤   ├─────────────────┤   ├────────────────┤
│ • Command Exec │   │ • Puppeteer     │   │ • Memory Store │
│ • Error Handler│   │ • Element Detect│   │ • Session Data │
│ • Retry Logic  │   │ • Auth Monitor  │   │ • Learning DB  │
└────────────────┘   └─────────────────┘   └────────────────┘
```

### Command Interface Design

The system uses a hybrid approach with multiple command interfaces:

- `alido <anything>` - Main general-purpose command (auto-mode selection)
- `ali ter "task description"` - Terminal-first execution
- `ali brw "task description"` - Browser-first execution  
- `ali do "task description"` - Auto-mode selection

**Examples:**
- `alido install and open upscayl`
- `alido search for good wallpapers with a dark aesthetic`

Note: Everything after `alido` is treated as a single command regardless of quotes or special characters.

## Components and Interfaces

### 1. Command Parser

**Purpose**: Parse user input and determine execution strategy

```typescript
interface CommandInput {
  mode: 'terminal' | 'browser' | 'auto';
  task: string;
  context?: string;
  isAlidoCommand?: boolean; // True for general-purpose alido commands
}

interface ParsedCommand {
  executionMode: ExecutionMode;
  steps: TaskStep[];
  requiredTools: string[];
  estimatedComplexity: number;
}
```

**Key Functions**:
- Natural language processing for task breakdown
- Mode detection and validation (auto-detect for `alido` commands)
- Context extraction from previous sessions
- Raw command parsing (everything after `alido` treated as single command)

### 2. Task Planner

**Purpose**: Break down high-level tasks into executable steps

```typescript
interface TaskStep {
  id: string;
  type: 'terminal' | 'browser' | 'file' | 'wait';
  command?: string;
  selector?: string;
  expectedOutput?: string;
  fallbackSteps?: TaskStep[];
  requiresAuth?: boolean;
}

interface ExecutionPlan {
  steps: TaskStep[];
  dependencies: string[];
  riskLevel: 'low' | 'medium' | 'high';
  requiresRoot: boolean;
}
```

### 3. Terminal Engine

**Purpose**: Execute Linux commands with intelligent error handling

```typescript
interface TerminalEngine {
  executeCommand(command: string): Promise<CommandResult>;
  handleError(error: CommandError): Promise<RetryStrategy>;
  searchSolution(error: string): Promise<Solution[]>;
  requestRootAccess(reason: string): Promise<boolean>;
}

interface CommandResult {
  exitCode: number;
  stdout: string;
  stderr: string;
  duration: number;
}
```

**Error Handling Strategy**:
1. **First Failure**: Immediate retry with same command
2. **Second Failure**: Analyze error and try alternative approach
3. **Third Failure**: Search Google/Stack Overflow for solutions
4. **Final Fallback**: Present options to user

### 4. Browser Engine

**Purpose**: Control visible browser for web-based tasks

```typescript
interface BrowserEngine {
  launchBrowser(): Promise<Browser>;
  navigateToUrl(url: string): Promise<void>;
  waitForAuth(): Promise<void>;
  extractContent(selector: string): Promise<string>;
  detectLoginScreen(): Promise<boolean>;
}
```

**Authentication Handling**:
- Monitor for login screens and password prompts
- Pause execution when authentication is required
- Resume automatically after user completes login
- Support auto-login detection (Google SSO, saved passwords)

### 5. Context Manager

**Purpose**: Maintain memory and learning across sessions

```typescript
interface ContextManager {
  storeInformation(key: string, value: any, context: string): void;
  retrieveRelevant(task: string): Promise<ContextData[]>;
  updateLearning(command: string, success: boolean): void;
  getSessionHistory(): SessionData[];
}
```

## Data Models

### Task Execution Model

```typescript
interface TaskExecution {
  id: string;
  originalCommand: string;
  mode: ExecutionMode;
  steps: ExecutedStep[];
  status: 'running' | 'completed' | 'failed' | 'waiting_auth';
  startTime: Date;
  endTime?: Date;
  context: Record<string, any>;
}

interface ExecutedStep {
  step: TaskStep;
  result?: CommandResult;
  error?: string;
  retryCount: number;
  duration: number;
}
```

### Learning Database Schema

```sql
-- Command success/failure tracking
CREATE TABLE command_history (
  id INTEGER PRIMARY KEY,
  command TEXT,
  context TEXT,
  success BOOLEAN,
  error_message TEXT,
  solution TEXT,
  timestamp DATETIME
);

-- User preferences and patterns
CREATE TABLE user_patterns (
  id INTEGER PRIMARY KEY,
  pattern_type TEXT,
  pattern_data JSON,
  frequency INTEGER,
  last_used DATETIME
);

-- Stored information from tasks
CREATE TABLE context_memory (
  id INTEGER PRIMARY KEY,
  key TEXT,
  value TEXT,
  context TEXT,
  relevance_score REAL,
  created_at DATETIME,
  expires_at DATETIME
);
```

## Error Handling

### Progressive Error Resolution

1. **Immediate Retry**: Same command, handle transient issues
2. **Smart Retry**: Modify command based on error analysis
3. **Alternative Approach**: Use different tools/methods
4. **Web Search**: Query solutions from online resources
5. **User Intervention**: Present options and ask for guidance

### Root Access Management

When commands require sudo:
1. Explain why root access is needed
2. List specific packages/operations
3. Execute command (system will prompt for password)
4. Continue with task after successful authentication

## Testing Strategy

### Unit Testing
- Command parsing accuracy
- Task planning logic
- Error handling scenarios
- Context storage/retrieval

### Integration Testing
- Terminal command execution
- Browser automation flows
- Authentication handling
- Cross-component communication

### End-to-End Testing
- Complete task scenarios (Gmail summary, portfolio creation)
- Error recovery workflows
- Multi-step task coordination
- User interaction flows

### Security Testing
- Command injection prevention
- Safe file operations
- Authentication flow security
- Root access validation

## Implementation Phases

### Phase 1: Core Infrastructure
- Command parser with `alido` and `ali` command support
- Terminal engine with simple command execution
- Basic error handling and retry logic
- Auto-mode detection for general-purpose commands

### Phase 2: Browser Integration
- Browser automation setup
- Authentication detection and waiting
- Content extraction capabilities

### Phase 3: Intelligence Layer
- Task planning and breakdown
- Context management and memory
- Learning from success/failure patterns

### Phase 4: Advanced Features
- Web search for error solutions
- Complex multi-step task coordination
- Performance optimization and caching