#!/usr/bin/env node

import { ErrorDisplay, ErrorType } from './ErrorDisplay.js';
import { HelpDisplay } from './HelpDisplay.js';
import type { CommandInfo, TroubleshootingStep } from './HelpDisplay.js';

/**
 * Demonstration of error display capabilities
 */
function demonstrateErrorDisplay(): void {
  console.log('='.repeat(60));
  console.log('ERROR DISPLAY EXAMPLES');
  console.log('='.repeat(60));

  // API Key Error
  console.log('\n1. API Key Error:');
  ErrorDisplay.showApiKeyError();

  // System Error
  console.log('\n2. System Error:');
  const systemError = new Error('Permission denied') as any;
  systemError.code = 'EACCES';
  systemError.path = '/usr/local/bin/kira';
  ErrorDisplay.showSystemError(systemError);

  // Network Error
  console.log('\n3. Network Error:');
  const networkError = new Error('Request failed') as any;
  networkError.status = 401;
  networkError.url = 'https://api.gemini.com/v1/chat';
  ErrorDisplay.showNetworkError(networkError);

  // Command Error
  console.log('\n4. Command Error:');
  ErrorDisplay.showCommandError('npm install', new Error('Command not found'), 127);

  // Validation Error
  console.log('\n5. Validation Error:');
  ErrorDisplay.showValidationError('email', 'invalid-email', [
    'be a valid email address',
    'contain an @ symbol',
    'have a valid domain'
  ]);

  // Custom Error with Stack Trace
  console.log('\n6. Custom Error with Debug Info:');
  const customError = new Error('Something went wrong in the AI service');
  customError.stack = `Error: Something went wrong in the AI service
    at GeminiService.chat (/path/to/GeminiService.ts:45:12)
    at CLI.handleAskCommand (/path/to/cli.ts:123:23)
    at CLI.run (/path/to/cli.ts:67:18)`;
  
  ErrorDisplay.show(customError, {
    title: 'AI Service Error',
    message: 'Failed to process your request',
    details: 'The AI service encountered an unexpected error while processing your query.',
    suggestions: [
      'Check your API key configuration',
      'Verify your internet connection',
      'Try a simpler query',
      'Contact support if the issue persists'
    ],
    showHelp: true,
    showStackTrace: true,
    type: ErrorType.API_KEY
  });
}

/**
 * Demonstration of help display capabilities
 */
function demonstrateHelpDisplay(): void {
  console.log('\n' + '='.repeat(60));
  console.log('HELP DISPLAY EXAMPLES');
  console.log('='.repeat(60));

  // Command-specific help
  console.log('\n1. Command Help:');
  const askCommand: CommandInfo = {
    name: 'ask',
    description: 'Ask the AI assistant a question',
    usage: 'kira ask [options] <question>',
    aliases: ['chat', 'query'],
    options: [
      {
        name: 'model',
        alias: 'm',
        description: 'Specify the AI model to use',
        type: 'string',
        default: 'gemini-pro'
      },
      {
        name: 'temperature',
        alias: 't',
        description: 'Control response creativity (0.0-1.0)',
        type: 'number',
        default: 0.7
      },
      {
        name: 'stream',
        alias: 's',
        description: 'Stream the response in real-time',
        type: 'boolean',
        default: false
      },
      {
        name: 'context',
        alias: 'c',
        description: 'Include file context in the query',
        type: 'string'
      }
    ],
    examples: [
      {
        command: 'kira ask "What is TypeScript?"',
        description: 'Ask a simple question',
        output: 'TypeScript is a strongly typed programming language...'
      },
      {
        command: 'kira ask --stream "Explain async/await"',
        description: 'Stream the response for long answers'
      },
      {
        command: 'kira ask --context src/app.ts "How can I improve this code?"',
        description: 'Ask about specific code with context'
      }
    ]
  };

  HelpDisplay.showCommand(askCommand);

  // General help
  console.log('\n2. General Help:');
  const commands: CommandInfo[] = [
    {
      name: 'init',
      description: 'Initialize Kira configuration',
      aliases: ['setup']
    },
    {
      name: 'ask',
      description: 'Ask the AI assistant a question',
      aliases: ['chat', 'query']
    },
    {
      name: 'doctor',
      description: 'Check system configuration and health'
    },
    {
      name: 'config',
      description: 'Manage configuration settings',
      subcommands: [
        { name: 'get', description: 'Get configuration value' },
        { name: 'set', description: 'Set configuration value' },
        { name: 'list', description: 'List all configuration' }
      ]
    }
  ];

  HelpDisplay.showGeneral(commands);

  // API Key Setup Guide
  console.log('\n3. API Key Setup Guide:');
  HelpDisplay.showApiKeySetup();

  // System Requirements
  console.log('\n4. System Requirements:');
  HelpDisplay.showSystemRequirements();

  // Troubleshooting Steps
  console.log('\n5. Custom Troubleshooting:');
  const troubleshootingSteps: TroubleshootingStep[] = [
    {
      step: 1,
      title: 'Check Kira Installation',
      description: 'Verify that Kira is properly installed and accessible.',
      command: 'kira --version',
      expectedResult: 'Kira version 1.0.0'
    },
    {
      step: 2,
      title: 'Verify API Key',
      description: 'Ensure your Gemini API key is configured correctly.',
      command: 'kira config get apiKey',
      expectedResult: 'API key is set (shows masked value)'
    },
    {
      step: 3,
      title: 'Test Connection',
      description: 'Test the connection to the Gemini API.',
      command: 'kira ask "Hello"',
      expectedResult: 'AI responds with a greeting'
    },
    {
      step: 4,
      title: 'Check System Health',
      description: 'Run a comprehensive system check.',
      command: 'kira doctor',
      expectedResult: 'All systems show as healthy'
    }
  ];

  HelpDisplay.showTroubleshooting(troubleshootingSteps, 'Connection Issues');
}

/**
 * Main demonstration function
 */
function main(): void {
  console.log('KIRA CLI - ERROR AND HELP DISPLAY DEMONSTRATION');
  console.log('This demonstrates the new error handling and help display capabilities.');
  
  demonstrateErrorDisplay();
  demonstrateHelpDisplay();
  
  console.log('\n' + '='.repeat(60));
  console.log('DEMONSTRATION COMPLETE');
  console.log('='.repeat(60));
  console.log('\nThese components provide:');
  console.log('• Comprehensive error categorization and display');
  console.log('• Contextual help and suggestions');
  console.log('• Formatted command documentation');
  console.log('• Step-by-step troubleshooting guides');
  console.log('• Cross-platform compatibility');
  console.log('• Accessibility-friendly formatting');
}

// Run demonstration if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export { demonstrateErrorDisplay, demonstrateHelpDisplay };