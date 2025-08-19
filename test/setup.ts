// Test setup file for Jest
import { jest } from '@jest/globals';

// Mock process.stdout.write to capture output in tests
const originalWrite = process.stdout.write;
let capturedOutput: string[] = [];

export function mockStdout() {
  capturedOutput = [];
  process.stdout.write = jest.fn((chunk: any) => {
    capturedOutput.push(chunk.toString());
    return true;
  }) as any;
}

export function restoreStdout() {
  process.stdout.write = originalWrite;
}

export function getCapturedOutput(): string[] {
  return [...capturedOutput];
}

export function getLastOutput(): string {
  return capturedOutput[capturedOutput.length - 1] || '';
}

export function getAllOutput(): string {
  return capturedOutput.join('');
}

// Mock console.log to capture output
const originalLog = console.log;
let capturedLogs: string[] = [];

export function mockConsoleLog() {
  capturedLogs = [];
  console.log = jest.fn((...args: any[]) => {
    capturedLogs.push(args.map(arg => String(arg)).join(' '));
  });
}

export function restoreConsoleLog() {
  console.log = originalLog;
}

export function getCapturedLogs(): string[] {
  return [...capturedLogs];
}

export function getLastLog(): string {
  return capturedLogs[capturedLogs.length - 1] || '';
}

export function getAllLogs(): string {
  return capturedLogs.join('\n');
}

// Mock terminal capabilities for consistent testing
export function mockTerminalCapabilities() {
  // Mock terminal width
  Object.defineProperty(process.stdout, 'columns', {
    value: 80,
    writable: true
  });

  // Mock platform
  Object.defineProperty(process, 'platform', {
    value: 'linux',
    writable: true
  });

  // Mock environment variables
  process.env.TERM = 'xterm-256color';
  process.env.COLORTERM = 'truecolor';
  process.env.LANG = 'en_US.UTF-8';
}

// Setup before each test
beforeEach(() => {
  mockTerminalCapabilities();
  mockConsoleLog();
  mockStdout();
});

// Cleanup after each test
afterEach(() => {
  restoreConsoleLog();
  restoreStdout();
  
  // Clear environment variables
  delete process.env.FORCE_ASCII;
  delete process.env.NO_UNICODE;
  delete process.env.ACCESSIBILITY_MODE;
  delete process.env.FORCE_HIGH_CONTRAST;
  delete process.env.COLOR_BLIND_FRIENDLY;
  delete process.env.KIRA_PERFORMANCE_MONITORING;
});

// Global test utilities
global.testUtils = {
  mockStdout,
  restoreStdout,
  getCapturedOutput,
  getLastOutput,
  getAllOutput,
  mockConsoleLog,
  restoreConsoleLog,
  getCapturedLogs,
  getLastLog,
  getAllLogs,
  mockTerminalCapabilities
};