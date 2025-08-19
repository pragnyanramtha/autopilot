#!/usr/bin/env node

import * as dotenv from 'dotenv';
import { Command } from 'commander';
import chalk from 'chalk';
import { Banner } from './ui/components/Banner.js';
import { StatusIndicator, StatusType } from './ui/components/StatusIndicator.js';
import { Spinner, ProgressBar } from './ui/components/ProgressBar.js';
import { Layout } from './ui/utils/Layout.js';
import { getThemeColors } from './ui/themes/ThemeManager.js';

// Load environment variables
dotenv.config();
import { CommandInput, ExecutionMode } from './types/interfaces.js';
import { CommandParser } from './parser/CommandParser.js';
import { TaskPlanner } from './planner/TaskPlanner.js';
import { TerminalEngine } from './terminal/TerminalEngine.js';

const program = new Command();

// Get theme colors for consistent styling
const colors = getThemeColors();
const success = colors.success;
const error = colors.error;
const info = colors.info;
const warning = colors.warning;

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

// Package management command
program
  .command('package')
  .description('Package management operations with visual progress')
  .option('-i, --install <packages...>', 'Install packages')
  .option('-u, --update', 'Update package lists')
  .option('-s, --status', 'Show package manager status')
  .action(async (options) => {
    const { PackageManagerService } = await import('./terminal/PackageManager.js');
    
    Banner.displayMinimal();
    
    try {
      const packageManager = new PackageManagerService();
      
      if (options.status) {
        StatusIndicator.info('Displaying package manager status...');
        await packageManager.displayStatus();
        return;
      }
      
      if (options.update) {
        StatusIndicator.info('Updating package lists...');
        await packageManager.updatePackageLists();
        return;
      }
      
      if (options.install && options.install.length > 0) {
        StatusIndicator.info(`Installing ${options.install.length} package(s)...`);
        await packageManager.installMultiplePackages(options.install);
        return;
      }
      
      // Default: show status
      await packageManager.displayStatus();
      
    } catch (error) {
      StatusIndicator.error(`Package management failed: ${error instanceof Error ? error.message : String(error)}`);
    }
  });

// System detection command
program
  .command('detect')
  .description('Run comprehensive system detection')
  .option('-v, --verbose', 'Enable verbose output')
  .option('-s, --sections <sections>', 'Comma-separated list of sections (system,hardware,os,packages,tools,network)')
  .option('--script', 'Use detection script (faster)')
  .action(async (options) => {
    const { SystemDetection } = await import('./terminal/SystemDetection.js');
    
    Banner.displayMinimal();
    
    try {
      const systemDetection = new SystemDetection();
      const sections = options.sections ? 
        options.sections.split(',').map((s: string) => s.trim()) : 
        undefined;

      if (options.script) {
        await systemDetection.detectWithScript({ 
          verbose: options.verbose, 
          showProgress: true,
          sections 
        });
      } else {
        await systemDetection.detect({ 
          verbose: options.verbose, 
          showProgress: true,
          sections 
        });
      }

      // Display results
      systemDetection.displaySystemInfo({ 
        compact: false,
        sections 
      });
      
    } catch (error) {
      StatusIndicator.error(`System detection failed: ${error instanceof Error ? error.message : String(error)}`);
    }
  });

// Status command - Show system status with enhanced visual formatting
program
  .command('status')
  .description('Display comprehensive system status and information')
  .option('-c, --compact', 'Display compact view')
  .option('-s, --sections <sections>', 'Comma-separated list of sections to display (system,hardware,os,packages,tools,network)')
  .action(async (options) => {
    const { SystemDetection } = await import('./terminal/SystemDetection.js');
    const { PackageManagerService } = await import('./terminal/PackageManager.js');
    const { ProfileManager } = await import('./profile/ProfileManager.js');
    
    Banner.displayMinimal();
    
    try {
      // Parse sections option
      const sections = options.sections ? 
        options.sections.split(',').map((s: string) => s.trim()) : 
        ['system', 'hardware', 'os', 'packages', 'tools', 'network'];

      // Run comprehensive system detection
      const systemDetection = new SystemDetection();
      await systemDetection.detectWithScript({ 
        verbose: false, 
        showProgress: true,
        sections 
      });

      // Display system information with enhanced formatting
      systemDetection.displaySystemInfo({ 
        compact: options.compact,
        sections 
      });

      console.log();
      StatusIndicator.divider('Kira Configuration');

      // Profile Status
      const profileManager = ProfileManager.getInstance();
      const isInitialized = await profileManager.isInitialized();
      
      if (isInitialized) {
        const userName = await profileManager.getUserName();
        StatusIndicator.success('Kira Profile: Initialized', {
          details: `User: ${userName}\nLocation: ~/.kira/profile.json`
        });
      } else {
        StatusIndicator.warning('Kira profile not initialized', {
          details: 'Run "kira init" to set up your profile'
        });
      }

      // API Configuration
      const apiKey = process.env.GEMINI_API_KEY;
      if (apiKey && apiKey !== 'your_gemini_api_key_here') {
        StatusIndicator.success('Gemini AI: Configured and ready', {
          details: 'Enhanced natural language processing enabled'
        });
      } else {
        StatusIndicator.warning('Gemini AI: Not configured', {
          details: 'Add GEMINI_API_KEY to .env for enhanced AI features'
        });
      }

      // Package Manager Status with enhanced display
      console.log();
      StatusIndicator.divider('Package Management');
      
      const packageManager = new PackageManagerService();
      await packageManager.displayStatus();
      
      StatusIndicator.success('System status check completed');
      
    } catch (error) {
      StatusIndicator.error(`Failed to gather system information: ${error instanceof Error ? error.message : String(error)}`);
    }
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
  const { MultiStepProgress } = await import('./ui/components/ProgressBar.js');
  const { CommandOutput } = await import('./ui/formatters/CommandOutput.js');
  
  // Create multi-step progress tracker
  const steps = ['Parse Command', 'Create Plan', 'Execute Steps'];
  const progress = new MultiStepProgress(steps);
  
  try {
    // Step 1: Parse the command with enhanced visual feedback
    const parseSpinner = new Spinner('Analyzing command structure...');
    parseSpinner.start();
    
    // Create parser and planner instances
    const parser = new CommandParser();
    const planner = new TaskPlanner();
    
    // Create command input
    const input: CommandInput = {
      mode,
      task,
      isAlidoCommand: isKiraCommand
    };
    
    // Parse the command with progress updates
    parseSpinner.update('Detecting execution mode...');
    await new Promise(resolve => setTimeout(resolve, 300)); // Brief pause for visual feedback
    
    parseSpinner.update('Analyzing command complexity...');
    const parsedCmd = await parser.parse(input);
    
    parseSpinner.succeed('Command analysis complete');
    progress.nextStep('Command parsed successfully');
    
    // Display parsing results with enhanced formatting
    console.log();
    StatusIndicator.divider('Parsing Results');
    
    const parsingResults = [
      { label: 'Execution Mode', status: StatusType.INFO, value: parsedCmd.executionMode },
      { label: 'Required Tools', status: StatusType.INFO, value: parsedCmd.requiredTools.join(', ') || 'none' },
      { label: 'Complexity Score', status: parsedCmd.estimatedComplexity > 50 ? StatusType.WARNING : StatusType.SUCCESS, value: parsedCmd.estimatedComplexity.toString() },
      { label: 'Steps Identified', status: StatusType.INFO, value: parsedCmd.steps.length.toString() }
    ];
    
    StatusIndicator.summary('Command Analysis', parsingResults);
    
    // Step 2: Create execution plan with visual feedback
    const planSpinner = new Spinner('Building execution strategy...');
    planSpinner.start();
    
    planSpinner.update('Assessing risks and dependencies...');
    await new Promise(resolve => setTimeout(resolve, 200));
    
    planSpinner.update('Optimizing execution order...');
    const plan = await planner.createPlan(parsedCmd);
    
    planSpinner.succeed('Execution plan ready');
    progress.nextStep('Execution plan created');
    
    // Display plan details with enhanced formatting
    console.log();
    StatusIndicator.divider('Execution Plan');
    
    const planResults = [
      { label: 'Risk Level', status: plan.riskLevel === 'high' ? StatusType.ERROR : plan.riskLevel === 'medium' ? StatusType.WARNING : StatusType.SUCCESS, value: plan.riskLevel },
      { label: 'Root Access', status: plan.requiresRoot ? StatusType.WARNING : StatusType.SUCCESS, value: plan.requiresRoot ? 'Required' : 'Not required' },
      { label: 'Dependencies', status: StatusType.INFO, value: plan.dependencies.join(', ') || 'none' }
    ];
    
    StatusIndicator.summary('Plan Overview', planResults);
    
    // Display execution steps with enhanced formatting
    console.log();
    StatusIndicator.info('Execution Steps:');
    plan.steps.forEach((step, i) => {
      let stepIcon = '🖥️';
      if (step.type === 'browser') stepIcon = '🌐';
      else if (step.type === 'file') stepIcon = '📄';
      else if (step.type === 'wait') stepIcon = '⏳';
      
      const authIndicator = step.requiresAuth ? ' 🔐' : '';
      const stepStatus = step.requiresAuth ? StatusType.WARNING : StatusType.INFO;
      
      StatusIndicator.step(i + 1, plan.steps.length, `${stepIcon} ${step.command}${authIndicator}`, stepStatus);
    });
    
    // Step 3: Execute with real-time progress and enhanced feedback
    console.log();
    StatusIndicator.divider('Execution');
    progress.nextStep('Starting execution...');
    
    const terminalEngine = new TerminalEngine();
    let successCount = 0;
    let failureCount = 0;
    
    for (let i = 0; i < plan.steps.length; i++) {
      const step = plan.steps[i];
      
      if (step.type === 'terminal' && step.command) {
        try {
          // Create execution progress bar
          const execProgress = new ProgressBar({
            total: 100,
            message: `Step ${i + 1}/${plan.steps.length}: ${step.command}`,
            showPercentage: true,
            style: 'bar'
          });
          
          // Simulate progress updates during execution
          execProgress.update(10, 'Initializing...');
          await new Promise(resolve => setTimeout(resolve, 100));
          
          execProgress.update(30, 'Executing command...');
          const result = await terminalEngine.executeCommand(step.command);
          
          execProgress.update(90, 'Processing results...');
          await new Promise(resolve => setTimeout(resolve, 100));
          
          if (result.exitCode === 0) {
            execProgress.complete('✓ Success');
            successCount++;
            
            // Display formatted command output
            if (result.stdout && result.stdout.trim()) {
              const formattedOutput = CommandOutput.format({
                command: step.command,
                output: result.stdout,
                exitCode: result.exitCode,
                duration: result.duration
              }, { 
                showCommand: false, 
                maxWidth: 100,
                highlightSyntax: true 
              });
              
              console.log(Layout.indent(formattedOutput, 2));
            }
          } else {
            execProgress.fail('✗ Failed');
            failureCount++;
            
            // Display formatted error output
            const formattedError = CommandOutput.format({
              command: step.command,
              output: result.stdout || '',
              error: result.stderr,
              exitCode: result.exitCode,
              duration: result.duration
            }, { 
              showCommand: false, 
              maxWidth: 100 
            });
            
            console.log(Layout.indent(formattedError, 2));
          }
          
          console.log(); // Add spacing between steps
          
        } catch (err) {
          failureCount++;
          StatusIndicator.error(`Step ${i + 1} failed: ${err instanceof Error ? err.message : String(err)}`);
          StatusIndicator.error('Command execution failed after all retry attempts', { indent: 2 });
          console.log();
        }
      } else {
        StatusIndicator.warning(`Skipping ${step.type} step: ${step.command} (not implemented yet)`);
        console.log();
      }
    }
    
    // Final execution summary
    progress.complete('Execution completed');
    console.log();
    StatusIndicator.divider('Execution Summary');
    
    const executionSummary = [
      { label: 'Total Steps', status: StatusType.INFO, value: plan.steps.length.toString() },
      { label: 'Successful', status: StatusType.SUCCESS, value: successCount.toString() },
      { label: 'Failed', status: failureCount > 0 ? StatusType.ERROR : StatusType.SUCCESS, value: failureCount.toString() },
      { label: 'Success Rate', status: failureCount === 0 ? StatusType.SUCCESS : successCount > failureCount ? StatusType.WARNING : StatusType.ERROR, value: `${Math.round((successCount / plan.steps.length) * 100)}%` }
    ];
    
    StatusIndicator.summary('Results', executionSummary);
    
    if (failureCount === 0) {
      console.log();
      Banner.success('Task execution completed successfully! 🎉');
    } else if (successCount > failureCount) {
      console.log();
      StatusIndicator.warning('Task completed with some failures. Check the logs above for details.');
    } else {
      console.log();
      StatusIndicator.error('Task execution failed. Please review the errors above.');
    }
    
  } catch (err) {
    progress.complete('Parsing failed');
    StatusIndicator.error(`Command parsing failed: ${err instanceof Error ? err.message : String(err)}`);
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