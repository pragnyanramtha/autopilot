// Core type definitions for Alvioli

export type ExecutionMode = 'terminal' | 'browser' | 'auto';
export type TaskStepType = 'terminal' | 'browser' | 'file' | 'wait';
export type TaskStatus = 'running' | 'completed' | 'failed' | 'waiting_auth';
export type RiskLevel = 'low' | 'medium' | 'high';

// Command Input and Parsing
export interface CommandInput {
  mode: ExecutionMode;
  task: string;
  context?: string;
  isAlidoCommand?: boolean;
}

export interface ParsedCommand {
  executionMode: ExecutionMode;
  steps: TaskStep[];
  requiredTools: string[];
  estimatedComplexity: number;
}

export interface TaskStep {
  id: string;
  type: TaskStepType;
  command?: string;
  selector?: string;
  expectedOutput?: string;
  fallbackSteps?: TaskStep[];
  requiresAuth?: boolean;
}

export interface ExecutionPlan {
  steps: TaskStep[];
  dependencies: string[];
  riskLevel: RiskLevel;
  requiresRoot: boolean;
}

// Execution Results
export interface CommandResult {
  exitCode: number;
  stdout: string;
  stderr: string;
  duration: number;
}

export interface TaskExecution {
  id: string;
  originalCommand: string;
  mode: ExecutionMode;
  steps: ExecutedStep[];
  status: TaskStatus;
  startTime: Date;
  endTime?: Date;
  context: Record<string, any>;
}

export interface ExecutedStep {
  step: TaskStep;
  result?: CommandResult;
  error?: string;
  retryCount: number;
  duration: number;
}

// Error Handling
export interface CommandError {
  command: string;
  exitCode: number;
  stderr: string;
  timestamp: Date;
}

export interface RetryStrategy {
  shouldRetry: boolean;
  alternativeCmd?: string;
  delaySeconds: number;
  maxRetries: number;
  searchSolutions: boolean;
}

export interface Solution {
  description: string;
  commands: string[];
  source: string;
  confidence: number;
}

// Context and Memory
export interface ContextData {
  key: string;
  value: string;
  context: string;
  relevanceScore: number;
  createdAt: Date;
  expiresAt?: Date;
}

export interface SessionData {
  id: string;
  command: string;
  success: boolean;
  timestamp: Date;
  duration: number;
}

// Core Interfaces
export interface CommandParser {
  parse(input: CommandInput): Promise<ParsedCommand>;
  detectMode(task: string): ExecutionMode;
  extractContext(task: string): Record<string, any>;
}

export interface TaskPlanner {
  createPlan(cmd: ParsedCommand): Promise<ExecutionPlan>;
  breakdownTask(task: string, mode: ExecutionMode): Promise<TaskStep[]>;
  estimateComplexity(steps: TaskStep[]): number;
}

export interface TerminalEngine {
  executeCommand(command: string): Promise<CommandResult>;
  handleError(error: CommandError): Promise<RetryStrategy>;
  searchSolution(error: string): Promise<Solution[]>;
  requestRootAccess(reason: string): Promise<boolean>;
}

export interface BrowserEngine {
  launchBrowser(): Promise<void>;
  navigateToUrl(url: string): Promise<void>;
  waitForAuth(): Promise<void>;
  extractContent(selector: string): Promise<string>;
  detectLoginScreen(): Promise<boolean>;
  close(): Promise<void>;
}

export interface ContextManager {
  storeInformation(key: string, value: any, context: string): Promise<void>;
  retrieveRelevant(task: string): Promise<ContextData[]>;
  updateLearning(command: string, success: boolean): Promise<void>;
  getSessionHistory(): Promise<SessionData[]>;
}

export interface ExecutionCoordinator {
  execute(plan: ExecutionPlan): Promise<TaskExecution>;
  handleStepFailure(step: TaskStep, error: CommandError): Promise<RetryStrategy>;
  switchMode(from: ExecutionMode, to: ExecutionMode): Promise<void>;
}