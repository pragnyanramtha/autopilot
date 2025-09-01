# Design Document

## Overview

The autopilot system transforms the existing CLI tool into a comprehensive automation platform that provides seamless first-launch setup, direct natural language prompting, and advanced automation capabilities including browser control, mouse/keyboard automation, and intelligent task coordination. The system leverages Gemini 2.5 Pro for natural language processing and integrates with native browser instances through debugging protocols and MCP servers.

## Architecture

### Core Architecture Principles

1. **Modular Design**: Each automation capability is implemented as a separate service with well-defined interfaces
2. **MCP Integration**: Extensibility through Model Context Protocol servers for browser automation and tool integration
3. **Native Integration**: Works with existing user applications rather than replacing them
4. **Security First**: All automation actions require explicit user consent and respect system boundaries
5. **Progressive Enhancement**: Graceful degradation when advanced features are unavailable

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                        Autopilot System                         │
├─────────────────────────────────────────────────────────────────┤
│  CLI Interface          │  GUI Companion App                    │
│  - Direct Prompting     │  - Chat Interface                     │
│  - Command Processing   │  - Visual Feedback                    │
│  - Status Display       │  - History Management                 │
├─────────────────────────────────────────────────────────────────┤
│                    Core Orchestration Layer                     │
│  - Task Coordinator     │  - Context Manager                    │
│  - Security Manager     │  - Plugin Registry                    │
├─────────────────────────────────────────────────────────────────┤
│  Automation Services                                            │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │ Browser Control │ │ System Control  │ │ Web Search      │   │
│  │ - Native Debug  │ │ - Mouse/Keyboard│ │ - Error Lookup  │   │
│  │ - Element Detect│ │ - Screenshot    │ │ - Solution Rank │   │
│  │ - MCP Bridge    │ │ - App Control   │ │ - Auto Research │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  Foundation Layer                                               │
│  - Gemini 2.5 Pro API  │  - OS Detection  │  - Memory System  │
│  - MCP Server Manager   │  - Config Store  │  - Plugin Loader  │
└─────────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. First Launch Setup Service

**Purpose**: Handles automatic OS detection and API configuration on first launch.

**Key Interfaces**:
```typescript
interface FirstLaunchSetup {
  detectOperatingSystem(): Promise<OSInfo>;
  setupGeminiAPI(): Promise<APIConfig>;
  validateAPIKey(key: string): Promise<boolean>;
  saveConfiguration(config: SystemConfig): Promise<void>;
}

interface OSInfo {
  platform: 'windows' | 'macos' | 'linux';
  version: string;
  architecture: string;
  capabilities: SystemCapabilities;
}
```

**Implementation Strategy**:
- Replace existing init wizard with streamlined first-launch flow
- Automatic OS detection using Node.js platform APIs and system commands
- Interactive API key setup with real-time validation
- Persistent configuration storage in user directory

### 2. Direct Prompting Engine

**Purpose**: Processes natural language commands using Gemini 2.5 Pro and routes to appropriate automation services.

**Key Interfaces**:
```typescript
interface PromptingEngine {
  processCommand(input: string): Promise<ExecutionPlan>;
  executeTask(plan: ExecutionPlan): Promise<ExecutionResult>;
  getContextualHelp(error: string): Promise<string[]>;
}

interface ExecutionPlan {
  intent: TaskIntent;
  steps: AutomationStep[];
  requiredServices: string[];
  riskLevel: 'low' | 'medium' | 'high';
  requiresConfirmation: boolean;
}
```

**Implementation Strategy**:
- Integration with existing CommandParser and TaskPlanner
- Enhanced prompt engineering for Gemini 2.5 Pro model
- Context-aware command interpretation
- Multi-step task decomposition

### 3. Browser Automation Service

**Purpose**: Controls native browser instances through debugging protocol and browser extensions.

**Key Interfaces**:
```typescript
interface BrowserAutomation {
  connectToNativeBrowser(): Promise<BrowserConnection>;
  detectPageElements(): Promise<PageElement[]>;
  interactWithElement(selector: string, action: ElementAction): Promise<void>;
  extractPageContent(): Promise<PageContent>;
}

interface BrowserConnection {
  isConnected: boolean;
  browserType: 'chrome' | 'firefox' | 'safari' | 'edge';
  debugPort: number;
  extensionId?: string;
}

interface PageElement {
  id: string;
  type: 'button' | 'input' | 'link' | 'text' | 'form';
  selector: string;
  text: string;
  isInteractive: boolean;
  boundingBox: ElementBounds;
}
```

**Implementation Strategy**:
- Chrome DevTools Protocol for Chromium-based browsers
- Firefox Remote Debugging Protocol for Firefox
- Browser extension fallback for enhanced compatibility
- MCP server integration for element detection using open-source tools
- Accessibility API integration for robust element identification

### 4. System Control Service

**Purpose**: Provides mouse, keyboard, and application control capabilities.

**Key Interfaces**:
```typescript
interface SystemControl {
  moveMouse(x: number, y: number): Promise<void>;
  clickMouse(button: 'left' | 'right' | 'middle'): Promise<void>;
  typeText(text: string): Promise<void>;
  sendKeyCombo(keys: string[]): Promise<void>;
  takeScreenshot(): Promise<Buffer>;
  getActiveWindow(): Promise<WindowInfo>;
}

interface WindowInfo {
  title: string;
  processName: string;
  bounds: WindowBounds;
  isActive: boolean;
}
```

**Implementation Strategy**:
- Cross-platform native modules for mouse/keyboard control
- Screen capture capabilities for visual feedback
- Window management integration
- Permission handling for system access
- Security boundaries and user consent mechanisms

### 5. Context Memory System

**Purpose**: Maintains conversation history, learns from interactions, and provides contextual assistance.

**Key Interfaces**:
```typescript
interface ContextMemory {
  storeInteraction(interaction: UserInteraction): Promise<void>;
  retrieveContext(query: string): Promise<ContextData>;
  learnFromExecution(task: string, result: ExecutionResult): Promise<void>;
  suggestOptimizations(taskPattern: string): Promise<Suggestion[]>;
}

interface UserInteraction {
  timestamp: Date;
  command: string;
  intent: TaskIntent;
  result: ExecutionResult;
  userFeedback?: string;
}
```

**Implementation Strategy**:
- SQLite database for local storage
- Vector embeddings for semantic search
- Pattern recognition for task optimization
- Privacy-focused local storage only

### 6. Web Search Service

**Purpose**: Automatically researches error solutions and provides intelligent problem resolution.

**Key Interfaces**:
```typescript
interface WebSearchService {
  searchErrorSolution(error: string): Promise<SearchResult[]>;
  rankSolutions(results: SearchResult[]): Promise<RankedSolution[]>;
  extractSolutionSteps(solution: RankedSolution): Promise<ActionStep[]>;
}

interface RankedSolution {
  source: string;
  relevanceScore: number;
  steps: string[];
  riskLevel: 'low' | 'medium' | 'high';
  applicability: number;
}
```

**Implementation Strategy**:
- Integration with search APIs (DuckDuckGo, Bing)
- Web scraping for solution extraction
- ML-based relevance scoring
- Solution validation and safety checks

### 7. MCP Server Manager

**Purpose**: Manages Model Context Protocol servers for extensible tool integration.

**Key Interfaces**:
```typescript
interface MCPServerManager {
  loadServers(): Promise<MCPServer[]>;
  registerServer(config: MCPServerConfig): Promise<void>;
  executeServerTool(serverId: string, tool: string, params: any): Promise<any>;
  listAvailableTools(): Promise<ToolDefinition[]>;
}

interface MCPServerConfig {
  name: string;
  command: string;
  args: string[];
  env: Record<string, string>;
  autoApprove: string[];
  disabled: boolean;
}
```

**Implementation Strategy**:
- Dynamic server loading and management
- Tool discovery and registration
- Secure execution environment
- Integration with existing MCP infrastructure

### 8. GUI Companion Application

**Purpose**: Provides visual interface for autopilot interaction and monitoring.

**Key Interfaces**:
```typescript
interface GUICompanion {
  connectToCLI(): Promise<CLIConnection>;
  sendCommand(command: string): Promise<void>;
  displayProgress(progress: TaskProgress): void;
  showHistory(): Promise<InteractionHistory>;
}

interface CLIConnection {
  isConnected: boolean;
  cliProcess: ChildProcess;
  communicationChannel: MessageChannel;
}
```

**Implementation Strategy**:
- Electron-based desktop application
- WebSocket communication with CLI process
- Real-time progress visualization
- Chat-like interface for natural interaction

## Data Models

### Configuration Models

```typescript
interface SystemConfig {
  user: UserProfile;
  api: APIConfiguration;
  automation: AutomationSettings;
  security: SecuritySettings;
}

interface UserProfile {
  name: string;
  preferences: UserPreferences;
  setupComplete: boolean;
  lastUsed: Date;
}

interface APIConfiguration {
  geminiApiKey: string;
  model: 'gemini-2.5-pro';
  rateLimits: RateLimitConfig;
  validated: boolean;
}

interface AutomationSettings {
  browserAutomation: BrowserSettings;
  systemControl: SystemControlSettings;
  confirmationLevel: 'always' | 'risky' | 'never';
}
```

### Task Models

```typescript
interface TaskExecution {
  id: string;
  command: string;
  intent: TaskIntent;
  plan: ExecutionPlan;
  steps: ExecutionStep[];
  status: 'pending' | 'running' | 'completed' | 'failed';
  startTime: Date;
  endTime?: Date;
  result?: ExecutionResult;
}

interface ExecutionStep {
  id: string;
  type: 'browser' | 'system' | 'search' | 'wait';
  action: string;
  parameters: Record<string, any>;
  status: StepStatus;
  output?: any;
  error?: string;
}
```

### Memory Models

```typescript
interface ConversationContext {
  sessionId: string;
  interactions: UserInteraction[];
  activeTask?: TaskExecution;
  contextVector: number[];
  lastUpdated: Date;
}

interface LearningPattern {
  pattern: string;
  frequency: number;
  successRate: number;
  optimizations: string[];
  lastSeen: Date;
}
```

## Error Handling

### Error Categories

1. **Setup Errors**: OS detection failures, API key validation issues
2. **Automation Errors**: Browser connection failures, element not found, permission denied
3. **System Errors**: Mouse/keyboard control failures, screenshot capture issues
4. **Network Errors**: API rate limits, search service unavailable
5. **Security Errors**: Unauthorized access attempts, permission violations

### Error Recovery Strategies

```typescript
interface ErrorRecoveryStrategy {
  errorType: string;
  retryAttempts: number;
  fallbackActions: string[];
  userNotification: boolean;
  autoResearch: boolean;
}

const errorStrategies: Record<string, ErrorRecoveryStrategy> = {
  'browser-connection-failed': {
    errorType: 'browser',
    retryAttempts: 3,
    fallbackActions: ['try-extension', 'manual-setup-guide'],
    userNotification: true,
    autoResearch: true
  },
  'element-not-found': {
    errorType: 'browser',
    retryAttempts: 2,
    fallbackActions: ['alternative-selector', 'screenshot-analysis'],
    userNotification: false,
    autoResearch: false
  }
};
```

### Automatic Error Resolution

- Web search integration for common error patterns
- Solution ranking based on relevance and safety
- Automatic application of low-risk solutions
- User confirmation for medium/high-risk solutions

## Testing Strategy

### Unit Testing

- **Service Layer**: Individual automation services with mocked dependencies
- **Integration Layer**: Cross-service communication and data flow
- **API Layer**: Gemini API integration and response handling
- **Security Layer**: Permission validation and boundary enforcement

### Integration Testing

- **Browser Automation**: Real browser instances with test pages
- **System Control**: Sandboxed environment for mouse/keyboard testing
- **MCP Integration**: Test MCP servers for tool validation
- **End-to-End**: Complete task execution workflows

### Security Testing

- **Permission Boundaries**: Verify system access restrictions
- **Input Validation**: Malicious command injection prevention
- **Data Protection**: Sensitive information encryption and storage
- **Network Security**: Secure API communication and data transmission

### Performance Testing

- **Response Time**: Command processing and execution speed
- **Memory Usage**: Context storage and retrieval efficiency
- **Concurrent Operations**: Multiple automation tasks handling
- **Resource Management**: System resource utilization optimization

### Cross-Platform Testing

- **OS Compatibility**: Windows, macOS, and Linux support
- **Browser Support**: Chrome, Firefox, Safari, Edge compatibility
- **Permission Systems**: Different OS security models
- **Hardware Variations**: Different screen resolutions and input devices

## Security Considerations

### User Consent Framework

- **Explicit Confirmation**: High-risk actions require user approval
- **Action Preview**: Show what will be executed before running
- **Granular Permissions**: Fine-grained control over automation capabilities
- **Audit Trail**: Complete log of all automation actions

### System Boundaries

- **Sandboxed Execution**: Isolated environment for automation tasks
- **Resource Limits**: CPU, memory, and network usage constraints
- **File System Access**: Restricted to user-authorized directories
- **Network Access**: Controlled external communication

### Data Protection

- **Local Storage**: All sensitive data stored locally only
- **Encryption**: API keys and user data encrypted at rest
- **No Telemetry**: No usage data transmitted to external services
- **Privacy First**: User data never leaves the local system

### Browser Security

- **Same-Origin Policy**: Respect browser security boundaries
- **Content Security**: Validate all injected scripts and content
- **Extension Security**: Minimal permissions for browser extensions
- **Debug Protocol**: Secure connection to browser debugging interfaces