#!/usr/bin/env node

import { Command } from 'commander';
import chalk from 'chalk';
import { CommandInput, ExecutionMode } from './types/interfaces';
import { CommandParser } from './parser/CommandParser';
import { TaskPlanner } from './planner/TaskPlanner';

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
  
  // Show what would happen next
  console.log(warning('\n⚠️  Actual execution not yet implemented'));
  console.log('Next implementation phase will execute these steps.');
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