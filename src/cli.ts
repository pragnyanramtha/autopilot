#!/usr/bin/env node

import * as dotenv from 'dotenv';
import { Command } from 'commander';
import chalk from 'chalk';

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
  .description('Kira - AI-powered OS automation for Linux')
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

// Main task execution function
async function executeTask(task: string, mode: string, isKiraCommand: boolean): Promise<void> {
  console.log(info('🤖 Kira AI Autopilot'));
  console.log(`Task: ${task}`);
  
  if (isKiraCommand) {
    console.log(info('Analyzing and executing task...'));
  }
  
  try {
    await parseAndPlanTask(task, mode as ExecutionMode, isKiraCommand);
  } catch (err) {
    console.log(error(`❌ Error: ${err instanceof Error ? err.message : String(err)}`));
  }
}

// Parse and plan task function
async function parseAndPlanTask(task: string, mode: ExecutionMode, isKiraCommand: boolean): Promise<void> {
  console.log(info('🔍 Parsing command...'));
  
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
  
  console.log(success('✓ Command parsed successfully'));
  console.log(`  Detected mode: ${parsedCmd.executionMode}`);
  console.log(`  Required tools: ${parsedCmd.requiredTools.join(', ') || 'none'}`);
  console.log(`  Complexity: ${parsedCmd.estimatedComplexity}`);
  console.log(`  Steps: ${parsedCmd.steps.length}`);
  
  // Create execution plan
  console.log(info('📋 Creating execution plan...'));
  const plan = await planner.createPlan(parsedCmd);
  
  console.log(success('✓ Execution plan created'));
  console.log(`  Risk level: ${plan.riskLevel}`);
  console.log(`  Requires root: ${plan.requiresRoot}`);
  console.log(`  Dependencies: ${plan.dependencies.join(', ') || 'none'}`);
  
  // Display the execution steps
  console.log('\n📝 Execution Steps:');
  plan.steps.forEach((step, i) => {
    let stepIcon = '🖥️';
    if (step.type === 'browser') stepIcon = '🌐';
    else if (step.type === 'file') stepIcon = '📄';
    else if (step.type === 'wait') stepIcon = '⏳';
    
    const authIndicator = step.requiresAuth ? ' 🔐' : '';
    console.log(`  ${i + 1}. ${stepIcon} ${step.command}${authIndicator}`);
  });
  
  // Execute terminal steps (for demonstration)
  console.log(info('\n🚀 Executing terminal steps...'));
  
  const terminalEngine = new TerminalEngine();
  
  for (const step of plan.steps) {
    if (step.type === 'terminal' && step.command) {
      try {
        console.log(`\n▶️  Executing: ${step.command}`);
        const result = await terminalEngine.executeCommand(step.command);
        
        if (result.exitCode === 0) {
          console.log(success(`✅ Success (${result.duration}ms)`));
          if (result.stdout) {
            console.log(`   Output: ${result.stdout.substring(0, 200)}${result.stdout.length > 200 ? '...' : ''}`);
          }
        } else {
          console.log(error(`❌ Failed with exit code ${result.exitCode}`));
          if (result.stderr) {
            console.log(`   Error: ${result.stderr.substring(0, 200)}${result.stderr.length > 200 ? '...' : ''}`);
          }
        }
      } catch (err) {
        console.log(error(`❌ Execution failed: ${err instanceof Error ? err.message : String(err)}`));
        
        // The error handling is now built into executeCommand with progressive retry
        console.log(error(`💥 Command execution failed after all retry attempts`));
      }
    } else {
      console.log(warning(`⏭️  Skipping ${step.type} step: ${step.command} (not implemented yet)`));
    }
  }
  
  console.log(success('\n🎉 Task execution completed!'));
}

// Handle different command invocations
const scriptName = process.argv[1];
if (scriptName?.includes('kira') || process.argv[2] === 'kira') {
  // Called as 'kira' - treat everything after as a single command
  const args = process.argv.slice(scriptName?.includes('kira') ? 2 : 3);
  if (args.length > 0) {
    executeTask(args.join(' '), 'auto', true).catch(console.error);
  } else {
    console.log(error('❌ Please provide a task description'));
    console.log('Examples:');
    console.log('  kira install and open firefox');
    console.log('  kira check disk space');
    console.log('  kira create a website from my resume');
  }
} else {
  // Default command structure
  program.parse();
}