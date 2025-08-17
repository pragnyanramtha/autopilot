#!/usr/bin/env node

import * as dotenv from 'dotenv';
import { Command } from 'commander';
import chalk from 'chalk';
import { Banner } from './ui/components/Banner.js';
import { StatusIndicator } from './ui/components/StatusIndicator.js';
import { Spinner } from './ui/components/ProgressBar.js';

// Load environment variables
dotenv.config();
import { CommandInput, ExecutionMode } from './types/interfaces.js';
import { CommandParser } from './parser/CommandParser.js';
import { TaskPlanner } from './planner/TaskPlanner.js';
import { TerminalEngine } from './terminal/TerminalEngine.js';

const program = new Command();

// Color functions for terminal output
const success = chalk.green.bold;
const error = chalk.red.bold;
const info = chalk.cyan;
const warning = chalk.yellow;

// Main program setup
program
  .name('kira')
  .description('Kira - AI-powered OS automation for Linux and macOS')
  .version('0.1.0')
  .option('-v, --verbose', 'Enable verbose output')
  .option('-n, --dry-run', 'Show what would be executed without running')
  .option('-c, --config <path>', 'Config file path')
  .argument('[task...]', 'Task description')
  .action(async (taskArgs: string[]) => {
    if (taskArgs.length === 0) {
      program.help();
      return;
    }
    const task = taskArgs.join(' ');
    await executeTask(task, 'auto', true);
  });

// Init command - First-time setup
program
  .command('init')
  .description('Initialize Kira with system detection and user preferences')
  .action(async () => {
    const { InitWizard } = await import('./setup/InitWizard.js');
    const wizard = new InitWizard();
    await wizard.run();
  });

// Setup command
program
  .command('setup')
  .description('Setup Kira configuration and check system requirements')
  .action(async () => {
    const { SetupWizard } = await import('./setup/SetupWizard.js');
    const wizard = new SetupWizard();
    await wizard.run();
  });

// Demo command
program
  .command('demo')
  .description('Demonstrate error handling capabilities')
  .action(async () => {
    const { ErrorHandlingDemo } = await import('./terminal/ErrorHandlingDemo.js');
    const demo = new ErrorHandlingDemo();
    await demo.demonstrateErrorHandling();
  });

// Check API key function
function checkApiKey(): boolean {
  const apiKey = process.env.GEMINI_API_KEY;
  
  if (!apiKey || apiKey === 'your_gemini_api_key_here' || apiKey.trim() === '') {
    Banner.error(`Missing Gemini API Key

Kira requires a FREE Gemini API key to function.

🔑 Get your API key from Google AI Studio:
   👉 https://aistudio.google.com/app/apikey
   👉 https://makersuite.google.com/app/apikey (alternative)

📋 Quick setup steps:
   1. Visit: https://aistudio.google.com/app/apikey
   2. Sign in with your Google account
   3. Click "Create API Key"
   4. Copy the generated key

📝 Add it to your .env file:
   echo "GEMINI_API_KEY=your_api_key_here" >> .env

💡 Or run: kira init (for interactive setup)

ℹ️  The Gemini API is free with generous limits:
   • 15 requests per minute
   • 1 million tokens per minute
   • 1,500 requests per day`);
    return false;
  }
  
  return true;
}

// Main task execution function
async function executeTask(task: string, mode: string, isKiraCommand: boolean): Promise<void> {
  // Check API key first
  if (!checkApiKey()) {
    process.exit(1);
  }
  
  // Check if user has initialized Kira
  const { ProfileManager } = await import('./profile/ProfileManager.js');
  const profileManager = ProfileManager.getInstance();
  const isInitialized = await profileManager.isInitialized();
  
  if (!isInitialized) {
    Banner.displayMinimal();
    StatusIndicator.warning('Kira is not initialized yet.');
    StatusIndicator.info('For the best experience, please run: kira init');
    StatusIndicator.info('This will set up your preferences and system detection.');
    console.log();
  } else {
    const userName = await profileManager.getUserName();
    Banner.startup(userName, { compact: true });
  }
  
  StatusIndicator.info(`Task: ${task}`);
  
  if (isKiraCommand) {
    StatusIndicator.loading('Analyzing and executing task...');
  }
  
  try {
    await parseAndPlanTask(task, mode as ExecutionMode, isKiraCommand);
  } catch (err) {
    console.log(error(`❌ Error: ${err instanceof Error ? err.message : String(err)}`));
  }
}

// Parse and plan task function
async function parseAndPlanTask(task: string, mode: ExecutionMode, isKiraCommand: boolean): Promise<void> {
  const spinner = new Spinner('Parsing command...');
  spinner.start();
  
  try {
    // Create parser and planner instances
    const parser = new CommandParser();
    const planner = new TaskPlanner();
    
    // Create command input
    const input: CommandInput = {
      mode,
      task,
      isAlidoCommand: isKiraCommand
    };
    
    // Parse the command
    const parsedCmd = await parser.parse(input);
    
    spinner.succeed('Command parsed successfully');
    
    StatusIndicator.info(`Detected mode: ${parsedCmd.executionMode}`, { indent: 2 });
    StatusIndicator.info(`Required tools: ${parsedCmd.requiredTools.join(', ') || 'none'}`, { indent: 2 });
    StatusIndicator.info(`Complexity: ${parsedCmd.estimatedComplexity}`, { indent: 2 });
    StatusIndicator.info(`Steps: ${parsedCmd.steps.length}`, { indent: 2 });
    
    // Create execution plan
    const planSpinner = new Spinner('Creating execution plan...');
    planSpinner.start();
    
    const plan = await planner.createPlan(parsedCmd);
    
    planSpinner.succeed('Execution plan created');
    
    StatusIndicator.info(`Risk level: ${plan.riskLevel}`, { indent: 2 });
    StatusIndicator.info(`Requires root: ${plan.requiresRoot}`, { indent: 2 });
    StatusIndicator.info(`Dependencies: ${plan.dependencies.join(', ') || 'none'}`, { indent: 2 });
    
    // Display the execution steps
    console.log();
    StatusIndicator.info('Execution Steps:');
    plan.steps.forEach((step, i) => {
      let stepIcon = '🖥️';
      if (step.type === 'browser') stepIcon = '🌐';
      else if (step.type === 'file') stepIcon = '📄';
      else if (step.type === 'wait') stepIcon = '⏳';
      
      const authIndicator = step.requiresAuth ? ' 🔐' : '';
      StatusIndicator.info(`${stepIcon} ${step.command}${authIndicator}`, { 
        prefix: `${i + 1}`,
        indent: 2 
      });
    });
    
    // Execute terminal steps (for demonstration)
    console.log();
    StatusIndicator.info('Executing terminal steps...');
    
    const terminalEngine = new TerminalEngine();
    
    for (const step of plan.steps) {
      if (step.type === 'terminal' && step.command) {
        try {
          const execSpinner = new Spinner(`Executing: ${step.command}`);
          execSpinner.start();
          
          const result = await terminalEngine.executeCommand(step.command);
          
          if (result.exitCode === 0) {
            execSpinner.succeed(`Success (${result.duration}ms)`);
            if (result.stdout) {
              const output = result.stdout.substring(0, 200);
              const truncated = result.stdout.length > 200 ? '...' : '';
              StatusIndicator.info(`Output: ${output}${truncated}`, { indent: 4 });
            }
          } else {
            execSpinner.fail(`Failed with exit code ${result.exitCode}`);
            if (result.stderr) {
              const errorOutput = result.stderr.substring(0, 200);
              const truncated = result.stderr.length > 200 ? '...' : '';
              StatusIndicator.error(`Error: ${errorOutput}${truncated}`, { indent: 4 });
            }
          }
        } catch (err) {
          StatusIndicator.error(`Execution failed: ${err instanceof Error ? err.message : String(err)}`);
          StatusIndicator.error('Command execution failed after all retry attempts');
        }
      } else {
        StatusIndicator.warning(`Skipping ${step.type} step: ${step.command} (not implemented yet)`);
      }
    }
    
    console.log();
    Banner.success('Task execution completed! 🎉');
    
  } catch (err) {
    spinner.fail('Command parsing failed');
    throw err;
  }
}

// Handle different command invocations
const scriptName = process.argv[1];
if (scriptName?.includes('kira') || process.argv[2] === 'kira') {
  // Called as 'kira' - treat everything after as a single command
  const args = process.argv.slice(scriptName?.includes('kira') ? 2 : 3);
  if (args.length > 0) {
    executeTask(args.join(' '), 'auto', true).catch(console.error);
  } else {
    Banner.displayMinimal();
    StatusIndicator.error('Please provide a task description');
    
    console.log();
    StatusIndicator.info('Getting started:');
    StatusIndicator.info('kira init          # First-time setup (recommended)', { indent: 2 });
    StatusIndicator.info('kira setup         # Check system requirements', { indent: 2 });
    
    console.log();
    StatusIndicator.info('Examples:');
    StatusIndicator.info('kira install and open firefox', { indent: 2 });
    StatusIndicator.info('kira check disk space', { indent: 2 });
    StatusIndicator.info('kira create a website from my resume', { indent: 2 });
    StatusIndicator.info('kira help me set up development environment', { indent: 2 });
  }
} else {
  // Default command structure
  program.parse();
}