#!/usr/bin/env node

import * as dotenv from 'dotenv';
import { Command } from 'commander';
import chalk from 'chalk';
import { Banner } from './ui/components/Banner.js';
import { StatusIndicator, StatusType } from './ui/components/StatusIndicator.js';
import { Spinner, ProgressBar } from './ui/components/ProgressBar.js';
import { Layout } from './ui/utils/Layout.js';
import { getThemeColors } from './ui/themes/ThemeManager.js';
import { FirstLaunchService } from './setup/FirstLaunchService.js';
import { DirectPromptingEngine, AutomationPlan } from './ai/DirectPromptingEngine.js';

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

// Initialize first-launch service
const firstLaunchService = new FirstLaunchService();

// Main program setup
program
  .name('ap')
  .description('AP - AI-powered autopilot system for seamless automation')
  .version('0.1.0')
  .option('-v, --verbose', 'Enable verbose output')
  .option('-n, --dry-run', 'Show what would be executed without running')
  .option('-c, --config <path>', 'Config file path')
  .argument('[task...]', 'Natural language task description')
  .action(async (taskArgs: string[]) => {
    // Handle first-launch setup
    await handleFirstLaunch();
    
    if (taskArgs.length === 0) {
      // Enter direct prompting mode
      await enterDirectPromptingMode();
      return;
    }
    
    const task = taskArgs.join(' ');
    await executeDirectCommand(task);
  });

// File management command
program
  .command('file')
  .description('File management operations')
  .option('-r, --read <path>', 'Read file content')
  .option('-w, --write <path>', 'Write content to file (use with --content)')
  .option('-a, --append <path>', 'Append content to file (use with --content)')
  .option('-c, --content <text>', 'Content to write or append')
  .option('-l, --list <path>', 'List directory contents')
  .option('-i, --info <path>', 'Get file information')
  .option('-s, --search <pattern>', 'Search for files (use with --in)')
  .option('--in <directory>', 'Directory to search in')
  .action(async (options) => {
    const { FileManager } = await import('./utils/FileManager.js');
    
    Banner.displayMinimal();
    
    try {
      if (options.read) {
        const result = FileManager.readFile(options.read);
        if (result.success) {
          StatusIndicator.success(result.message);
          console.log('\n' + Layout.box(result.data));
        } else {
          StatusIndicator.error(result.message);
        }
      }
      
      else if (options.write) {
        if (!options.content) {
          StatusIndicator.error('Content is required for write operation. Use --content "your text"');
          return;
        }
        const result = FileManager.writeFile(options.write, options.content, { createDir: true });
        StatusIndicator[result.success ? 'success' : 'error'](result.message);
      }
      
      else if (options.append) {
        if (!options.content) {
          StatusIndicator.error('Content is required for append operation. Use --content "your text"');
          return;
        }
        const result = FileManager.appendFile(options.append, options.content, { createDir: true });
        StatusIndicator[result.success ? 'success' : 'error'](result.message);
      }
      
      else if (options.list) {
        const result = FileManager.listDirectory(options.list);
        if (result.success) {
          StatusIndicator.success(result.message);
          console.log();
          result.data.files.forEach((file: any) => {
            const icon = file.isDirectory ? '📁' : '📄';
            const size = file.isFile ? ` (${file.size} bytes)` : '';
            StatusIndicator.info(`${icon} ${file.name}${size}`, { indent: 2 });
          });
        } else {
          StatusIndicator.error(result.message);
        }
      }
      
      else if (options.info) {
        const result = FileManager.getFileInfo(options.info);
        if (result.success) {
          StatusIndicator.success(result.message);
          const info = result.data;
          console.log();
          StatusIndicator.info(`Type: ${info.isFile ? 'File' : 'Directory'}`, { indent: 2 });
          StatusIndicator.info(`Size: ${info.size} bytes`, { indent: 2 });
          StatusIndicator.info(`Created: ${info.created}`, { indent: 2 });
          StatusIndicator.info(`Modified: ${info.modified}`, { indent: 2 });
        } else {
          StatusIndicator.error(result.message);
        }
      }
      
      else if (options.search) {
        const searchDir = options.in || process.cwd();
        const result = FileManager.searchFiles(searchDir, options.search);
        if (result.success) {
          StatusIndicator.success(`${result.message} - Found ${result.data.count} matches`);
          if (result.data.matches.length > 0) {
            console.log();
            result.data.matches.forEach((match: string) => {
              StatusIndicator.info(`📄 ${match}`, { indent: 2 });
            });
          }
        } else {
          StatusIndicator.error(result.message);
        }
      }
      
      else {
        StatusIndicator.info('File management operations:');
        StatusIndicator.info('ap file --read <path>                    # Read file', { indent: 2 });
        StatusIndicator.info('ap file --write <path> --content "text"  # Write file', { indent: 2 });
        StatusIndicator.info('ap file --append <path> --content "text" # Append to file', { indent: 2 });
        StatusIndicator.info('ap file --list <directory>               # List directory', { indent: 2 });
        StatusIndicator.info('ap file --info <path>                    # File info', { indent: 2 });
        StatusIndicator.info('ap file --search <pattern> --in <dir>    # Search files', { indent: 2 });
      }
      
    } catch (error) {
      StatusIndicator.error(`File operation failed: ${error instanceof Error ? error.message : String(error)}`);
    }
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
      StatusIndicator.divider('AP Configuration');

      // Configuration Status
      const config = await firstLaunchService.loadConfiguration();
      
      if (config) {
        StatusIndicator.success('AP Autopilot: Configured', {
          details: `OS: ${config.osInfo.platform} ${config.osInfo.version}\nSetup: ${config.setupComplete ? 'Complete' : 'Incomplete'}`
        });
      } else {
        StatusIndicator.warning('AP configuration not found', {
          details: 'Configuration will be created on first run'
        });
      }

      // API Configuration
      if (firstLaunchService.isApiKeyConfigured()) {
        StatusIndicator.success('Gemini 2.5 Pro: Configured and ready', {
          details: 'Enhanced natural language processing enabled'
        });
      } else {
        StatusIndicator.warning('Gemini AI: Not configured', {
          details: 'Delete ~/.ap/autopilot-config.json to restart setup'
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

// Handle first-launch setup
async function handleFirstLaunch(): Promise<void> {
  // Check if this is the first launch
  if (firstLaunchService.isFirstLaunch()) {
    try {
      await firstLaunchService.runFirstLaunchSetup();
      // Reload environment variables after API key setup
      dotenv.config();
    } catch (error) {
      StatusIndicator.error('First-launch setup failed', {
        details: error instanceof Error ? error.message : String(error)
      });
      process.exit(1);
    }
    return;
  }

  // Check if API key is configured
  if (!firstLaunchService.isApiKeyConfigured()) {
    Banner.error(`Missing Gemini API Key

AP Autopilot System requires a FREE Gemini API key to function.

🔑 Get your API key from Google AI Studio:
   👉 https://aistudio.google.com/app/apikey

📋 Quick setup steps:
   1. Visit: https://aistudio.google.com/app/apikey
   2. Sign in with your Google account
   3. Click "Create API Key"
   4. Copy the generated key

📝 Add it to your .env file:
   echo "GEMINI_API_KEY=your_api_key_here" >> .env

💡 Or delete ~/.ap/autopilot-config.json to restart setup

ℹ️  The Gemini API is free with generous limits:
   • 15 requests per minute
   • 1 million tokens per minute
   • 1,500 requests per day`);
    process.exit(1);
  }
}

// Enter direct prompting mode with enhanced AI integration
async function enterDirectPromptingMode(): Promise<void> {
  const config = await firstLaunchService.loadConfiguration();
  const osInfo = config?.osInfo;
  
  Banner.startup('Autopilot', { compact: true });
  
  console.log(chalk.cyan.bold('\n🤖 AP Autopilot System - Enhanced Direct Prompting Mode\n'));
  console.log(`System: ${osInfo?.platform} ${osInfo?.version} (${osInfo?.architecture})`);
  console.log(`AI Model: Gemini 2.5 Pro with context-aware processing`);
  console.log(chalk.gray('Type your commands in natural language. Press Ctrl+C to exit.\n'));
  
  console.log(chalk.yellow('Enhanced Features:'));
  console.log('  • Context-aware command understanding');
  console.log('  • Multi-step task decomposition');
  console.log('  • Intelligent error recovery');
  console.log('  • Learning from conversation history\n');
  
  console.log(chalk.yellow('Example Commands:'));
  console.log('  • "install firefox and open it"');
  console.log('  • "create a development environment for React"');
  console.log('  • "check system performance and optimize if needed"');
  console.log('  • "help me troubleshoot the last error"\n');

  // Initialize the enhanced prompting engine
  const promptingEngine = new DirectPromptingEngine();
  await promptingEngine.initialize();
  
  StatusIndicator.success('Enhanced AI prompting engine initialized');
  console.log();

  const { createInterface } = await import('readline');
  const rl = createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: chalk.cyan('ap> ')
  });

  rl.prompt();

  rl.on('line', async (input) => {
    const command = input.trim();
    
    if (command === '') {
      rl.prompt();
      return;
    }

    if (command.toLowerCase() === 'exit' || command.toLowerCase() === 'quit') {
      console.log(chalk.green('Goodbye! 👋'));
      rl.close();
      return;
    }

    // Handle special commands
    if (command.toLowerCase() === 'help' || command.toLowerCase() === '?') {
      displayDirectPromptingHelp();
      rl.prompt();
      return;
    }

    if (command.toLowerCase() === 'history') {
      displayCommandHistory(promptingEngine);
      rl.prompt();
      return;
    }

    try {
      await executeDirectCommandWithEngine(command, promptingEngine);
    } catch (error) {
      StatusIndicator.error('Command execution failed', {
        details: error instanceof Error ? error.message : String(error)
      });
      
      // Provide contextual help for errors
      try {
        const help = await promptingEngine.getContextualHelp(error instanceof Error ? error.message : String(error));
        if (help.length > 0) {
          console.log(chalk.yellow('\n💡 AI Suggestions:'));
          help.forEach((suggestion, index) => {
            console.log(`   ${index + 1}. ${suggestion}`);
          });
        }
      } catch (helpError) {
        console.log(chalk.gray('Unable to provide contextual help at this time.'));
      }
    }

    console.log(); // Add spacing
    rl.prompt();
  });

  rl.on('close', () => {
    console.log(chalk.green('\nAutopilot session ended. Goodbye! 👋'));
    process.exit(0);
  });
}

// Display help for direct prompting mode
function displayDirectPromptingHelp(): void {
  console.log(chalk.cyan('\n📖 Direct Prompting Help\n'));
  
  console.log(chalk.yellow('Special Commands:'));
  console.log('  help, ?     - Show this help message');
  console.log('  history     - Show recent command history');
  console.log('  exit, quit  - Exit the prompting mode\n');
  
  console.log(chalk.yellow('Natural Language Examples:'));
  console.log('  System Management:');
  console.log('    • "check disk space and memory usage"');
  console.log('    • "update system packages"');
  console.log('    • "install docker and configure it"\n');
  
  console.log('  Development:');
  console.log('    • "set up a Node.js project with TypeScript"');
  console.log('    • "create a React app and start development server"');
  console.log('    • "clone my repository and install dependencies"\n');
  
  console.log('  File Operations:');
  console.log('    • "create a backup of my documents folder"');
  console.log('    • "find all Python files in the current directory"');
  console.log('    • "compress the project folder into a zip file"\n');
  
  console.log(chalk.gray('The AI will break down complex tasks into manageable steps and execute them safely.'));
}

// Display command history
function displayCommandHistory(engine: DirectPromptingEngine): void {
  console.log(chalk.cyan('\n📜 Recent Command History\n'));
  
  // Access conversation history (this would need to be exposed by the engine)
  console.log(chalk.gray('Command history tracking is active. Recent commands are used for context-aware processing.'));
  console.log(chalk.gray('This helps the AI understand your workflow and provide better suggestions.'));
}

// Execute direct command using new prompting engine
async function executeDirectCommand(command: string): Promise<void> {
  const promptingEngine = new DirectPromptingEngine();
  await promptingEngine.initialize();
  await executeDirectCommandWithEngine(command, promptingEngine);
}

// Execute direct command with provided engine instance
async function executeDirectCommandWithEngine(command: string, promptingEngine: DirectPromptingEngine): Promise<void> {
  try {
    StatusIndicator.info(`Processing: "${command}"`);
    
    // Process the command with enhanced AI
    const plan = await promptingEngine.processCommand(command);
    
    // Show enhanced execution plan
    console.log(chalk.cyan('\n📋 Enhanced Execution Plan:'));
    console.log(`Intent: ${plan.intent.action} ${plan.intent.target}`);
    console.log(`Category: ${plan.intent.category} | Complexity: ${plan.intent.complexity}`);
    console.log(`Confidence: ${Math.round(plan.intent.confidence * 100)}%`);
    console.log(`Risk Level: ${plan.riskLevel}`);
    console.log(`Steps: ${plan.steps.length}`);
    
    if (plan.contextualInfo) {
      console.log(`Context: ${plan.contextualInfo}`);
    }
    
    if (plan.estimatedDuration) {
      console.log(`Estimated Duration: ${Math.round(plan.estimatedDuration / 1000)}s`);
    }
    
    // Show detailed steps
    if (plan.steps.length > 0) {
      console.log(chalk.cyan('\n📝 Execution Steps:'));
      plan.steps.forEach((step, index) => {
        const stepIcon = step.type === 'browser' ? '🌐' : step.type === 'system' ? '⚙️' : '🖥️';
        const authIcon = step.requiresAuth ? ' 🔐' : '';
        console.log(`  ${index + 1}. ${stepIcon} ${step.description}${authIcon}`);
        
        if (step.fallbackActions && step.fallbackActions.length > 0) {
          console.log(chalk.gray(`     Fallbacks: ${step.fallbackActions.join(', ')}`));
        }
      });
    }
    
    if (plan.requiresConfirmation) {
      const { createInterface } = await import('readline');
      const rl = createInterface({
        input: process.stdin,
        output: process.stdout
      });

      const confirmed = await new Promise<boolean>((resolve) => {
        rl.question(chalk.yellow('\nThis action requires confirmation. Continue? (y/N): '), (answer) => {
          rl.close();
          resolve(answer.toLowerCase().startsWith('y'));
        });
      });

      if (!confirmed) {
        StatusIndicator.warning('Command execution cancelled by user');
        return;
      }
    }
    
    // Execute the plan with enhanced feedback
    console.log(chalk.cyan('\n🚀 Executing Automation Plan...\n'));
    const result = await promptingEngine.executeTask(plan);
    
    if (result.success) {
      StatusIndicator.success('Command executed successfully');
      
      // Show execution summary
      const successfulSteps = result.stepResults.filter(r => r.success).length;
      const failedSteps = result.stepResults.filter(r => !r.success).length;
      
      console.log(chalk.green(`✓ Completed ${successfulSteps}/${result.stepResults.length} steps`));
      console.log(chalk.gray(`⏱️  Total execution time: ${Math.round(result.duration / 1000)}s`));
      
      if (result.contextLearned && result.contextLearned.length > 0) {
        console.log(chalk.blue(`🧠 Learned: ${result.contextLearned.join(', ')}`));
      }
      
      if (result.suggestions && result.suggestions.length > 0) {
        console.log(chalk.yellow('\n💡 AI Suggestions for next time:'));
        result.suggestions.forEach((suggestion, index) => {
          console.log(`   ${index + 1}. ${suggestion}`);
        });
      }
      
    } else {
      StatusIndicator.error('Command execution failed');
      
      if (result.error) {
        console.log(chalk.red(`❌ Error: ${result.error}`));
      }
      
      // Show step-by-step results
      if (result.stepResults.length > 0) {
        console.log(chalk.cyan('\n📊 Step Results:'));
        result.stepResults.forEach((stepResult, index) => {
          const status = stepResult.success ? chalk.green('✓') : chalk.red('✗');
          const duration = Math.round(stepResult.duration / 1000);
          console.log(`  ${status} Step ${index + 1}: ${duration}s`);
          
          if (!stepResult.success && stepResult.error) {
            console.log(chalk.red(`    Error: ${stepResult.error}`));
          }
          
          if (stepResult.retryCount && stepResult.retryCount > 0) {
            console.log(chalk.yellow(`    Retries: ${stepResult.retryCount}`));
          }
        });
      }
      
      // Provide enhanced contextual help
      if (result.error) {
        const help = await promptingEngine.getContextualHelp(result.error);
        if (help.length > 0) {
          console.log(chalk.yellow('\n🔧 AI-Powered Troubleshooting Suggestions:'));
          help.forEach((suggestion, index) => {
            console.log(`   ${index + 1}. ${suggestion}`);
          });
        }
      }
    }
    
  } catch (error) {
    StatusIndicator.error('Failed to process command', {
      details: error instanceof Error ? error.message : String(error)
    });
    
    // Try to provide help even for processing errors
    try {
      const help = await promptingEngine.getContextualHelp(error instanceof Error ? error.message : String(error));
      if (help.length > 0) {
        console.log(chalk.yellow('\n💡 Troubleshooting Suggestions:'));
        help.forEach((suggestion, index) => {
          console.log(`   ${index + 1}. ${suggestion}`);
        });
      }
    } catch (helpError) {
      console.log(chalk.gray('Unable to provide contextual help at this time.'));
    }
  }
}

// Legacy task execution function (kept for compatibility with existing commands)
async function executeTask(task: string, mode: string, isApCommand: boolean): Promise<void> {
  // For legacy compatibility, redirect to new direct command execution
  await executeDirectCommand(task);
}

// Parse and plan task function
async function parseAndPlanTask(task: string, mode: ExecutionMode, isApCommand: boolean): Promise<void> {
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
      isAlidoCommand: isApCommand
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
if (scriptName?.includes('ap') || process.argv[2] === 'ap') {
  // Called as 'ap' - treat everything after as a single command
  const args = process.argv.slice(scriptName?.includes('ap') ? 2 : 3);
  if (args.length > 0) {
    // Handle first launch, then execute command
    handleFirstLaunch().then(() => {
      return executeDirectCommand(args.join(' '));
    }).catch(console.error);
  } else {
    // Handle first launch, then enter direct prompting mode
    handleFirstLaunch().then(() => {
      return enterDirectPromptingMode();
    }).catch(console.error);
  }
} else {
  // Default command structure
  program.parse();
}