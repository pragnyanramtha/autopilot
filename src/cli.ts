#!/usr/bin/env node

import * as dotenv from 'dotenv';
import { Command } from 'commander';
import chalk from 'chalk';

// Load environment variables
dotenv.config();
import { CommandInput, ExecutionMode } from './types/interfaces';
import { CommandParser } from './parser/CommandParser';
import { TaskPlanner } from './planner/TaskPlanner';
import { TerminalEngine } from './terminal/TerminalEngine';

const program = new Command();

// Color functions for terminal output
const success = chalk.green.bold;
const error = chalk.red.bold;
const info = chalk.cyan;
const warning = chalk.yellow;

// Main program setup
program
  .name('alvioli')
  .description('AI-powered OS automation for Linux')
  .version('0.1.0')
  .option('-v, --verbose', 'Enable verbose output')
  .option('-n, --dry-run', 'Show what would be executed without running')
  .option('-c, --config <path>', 'Config file path');

// Alido command - main general-purpose command
program
  .command('alido')
  .description('Execute general-purpose AI automation tasks')
  .argument('<task...>', 'Task description (everything after alido)')
  .action(async (taskArgs: string[]) => {
    const task = taskArgs.join(' ');
    await executeTask(task, 'auto', true);
  });

// Ali command with subcommands
const aliCommand = program
  .command('ali')
  .description('AI automation with mode selection');

// Terminal-first execution
aliCommand
  .command('ter')
  .description('Execute task with terminal-first approach')
  .argument('<task...>', 'Task description')
  .action(async (taskArgs: string[]) => {
    const task = taskArgs.join(' ');
    await executeTask(task, 'terminal', false);
  });

// Browser-first execution
aliCommand
  .command('brw')
  .description('Execute task with browser-first approach')
  .argument('<task...>', 'Task description')
  .action(async (taskArgs: string[]) => {
    const task = taskArgs.join(' ');
    await executeTask(task, 'browser', false);
  });

// Auto-mode execution
aliCommand
  .command('do')
  .description('Execute task with automatic mode detection')
  .argument('<task...>', 'Task description')
  .action(async (taskArgs: string[]) => {
    const task = taskArgs.join(' ');
    await executeTask(task, 'auto', false);
  });

// Error handling demo
aliCommand
  .command('demo-errors')
  .description('Demonstrate progressive error handling capabilities')
  .action(async () => {
    const { ErrorHandlingDemo } = await import('./terminal/ErrorHandlingDemo');
    const demo = new ErrorHandlingDemo();
    await demo.demonstrateErrorHandling();
  });

// Setup command
program
  .command('setup')
  .description('Setup Alvioli configuration and check system requirements')
  .action(async () => {
    const { SetupWizard } = await import('./setup/SetupWizard');
    const wizard = new SetupWizard();
    await wizard.run();
  });

// Main task execution function
async function executeTask(task: string, mode: string, isAlidoCommand: boolean): Promise<void> {
  console.log(info('🤖 Alvioli AI Automation'));
  console.log(`Task: ${task}`);
  console.log(`Mode: ${mode}`);
  
  if (isAlidoCommand) {
    console.log(info('Using general-purpose alido command'));
  }
  
  try {
    await parseAndPlanTask(task, mode as ExecutionMode, isAlidoCommand);
  } catch (err) {
    console.log(error(`❌ Error: ${err instanceof Error ? err.message : String(err)}`));
  }
}

// Parse and plan task function
async function parseAndPlanTask(task: string, mode: ExecutionMode, isAlidoCommand: boolean): Promise<void> {
  console.log(info('🔍 Parsing command...'));
  
  // Create parser and planner instances
  const parser = new CommandParser();
  const planner = new TaskPlanner();
  
  // Create command input
  const input: CommandInput = {
    mode,
    task,
    isAlidoCommand
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

// Handle different command invocations based on process.argv[1]
const scriptName = process.argv[1];
if (scriptName?.includes('alido')) {
  // Called as 'alido' - treat everything after as a single command
  const args = process.argv.slice(2);
  if (args.length > 0) {
    executeTask(args.join(' '), 'auto', true).catch(console.error);
  } else {
    console.log(error('❌ Please provide a task description'));
    console.log('Example: alido install and open upscayl');
  }
} else if (scriptName?.includes('ali') && !scriptName.includes('alvioli')) {
  // Called as 'ali' - use subcommands
  if (process.argv.length <= 2) {
    console.log(error('❌ Please use ali with a subcommand'));
    console.log('Examples:');
    console.log('  ali ter "install something"');
    console.log('  ali brw "search for wallpapers"');
    console.log('  ali do "create a website"');
  } else {
    program.parse();
  }
} else {
  // Called as 'alvioli' - use full command structure
  program.parse();
}