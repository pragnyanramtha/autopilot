import { spawn, exec } from 'child_process';
import { promisify } from 'util';
import { CommandResult, CommandError, RetryStrategy, Solution } from '../types/interfaces';
import { GeminiService } from '../ai/GeminiService';
import { PackageManagerService } from './PackageManager';

const execAsync = promisify(exec);

export class TerminalEngine {
  private maxRetries: number = 3;
  private commandTimeout: number = 300000; // 5 minutes in milliseconds
  private geminiService: GeminiService;
  private packageManager: PackageManagerService;

  constructor() {
    this.geminiService = new GeminiService();
    this.packageManager = new PackageManagerService();
  }

  async executeCommand(command: string): Promise<CommandResult> {
    return await this.executeCommandWithRetry(command, 0);
  }

  private async executeCommandWithRetry(command: string, retryCount: number): Promise<CommandResult> {
    const startTime = Date.now();
    
    try {
      console.log(`🔧 Executing: ${command}${retryCount > 0 ? ` (retry ${retryCount})` : ''}`);
      
      // Handle special command patterns
      if (command.startsWith('install_package:')) {
        return await this.handlePackageInstall(command);
      } else if (command.startsWith('launch_application:')) {
        return await this.handleApplicationLaunch(command);
      } else if (command === 'create_project_structure') {
        return await this.handleProjectStructureCreation();
      } else if (command === 'npm_init') {
        return await this.handleNpmInit();
      } else if (command === 'start_dev_server') {
        return await this.handleDevServerStart();
      } else {
        // Execute generic command
        return await this.executeGenericCommand(command);
      }
    } catch (error) {
      const duration = Date.now() - startTime;
      
      let errorMessage = '';
      let exitCode = 1;
      
      if (error && typeof error === 'object') {
        const err = error as any;
        exitCode = err.code || err.exitCode || 1;
        
        if (err.stderr && typeof err.stderr === 'string') {
          errorMessage = err.stderr.trim();
        } else if (err.message && typeof err.message === 'string') {
          errorMessage = err.message;
        } else {
          errorMessage = String(error);
        }
      } else {
        errorMessage = String(error);
      }
      
      const commandError: CommandError = {
        command,
        exitCode,
        stderr: errorMessage,
        timestamp: new Date()
      };
      
      // Progressive error handling
      return await this.handleCommandFailure(commandError, retryCount);
    }
  }

  private async handleCommandFailure(error: CommandError, retryCount: number): Promise<CommandResult> {
    console.log(`❌ Command failed: ${error.command}`);
    
    // Fix the error message display
    let errorMessage = '';
    if (typeof error.stderr === 'string') {
      errorMessage = error.stderr;
    } else if (error.stderr && typeof error.stderr === 'object') {
      errorMessage = JSON.stringify(error.stderr);
    } else {
      errorMessage = String(error.stderr || 'Unknown error');
    }
    
    console.log(`   Error: ${errorMessage}`);
    console.log(`   Exit code: ${error.exitCode}`);

    // Phase 1: Immediate retry (for transient issues)
    if (retryCount === 0 && this.isTransientError(error)) {
      console.log(`🔄 Phase 1: Immediate retry for transient error`);
      await this.delay(1000); // 1 second delay
      return await this.executeCommandWithRetry(error.command, retryCount + 1);
    }

    // Phase 2: Smart retry with alternative command
    if (retryCount <= 1) {
      const retryStrategy = await this.handleError(error);
      if (retryStrategy.shouldRetry && retryStrategy.alternativeCmd && retryStrategy.alternativeCmd !== error.command) {
        console.log(`🧠 Phase 2: Smart retry with alternative command`);
        console.log(`   Trying: ${retryStrategy.alternativeCmd}`);
        await this.delay(retryStrategy.delaySeconds * 1000);
        return await this.executeCommandWithRetry(retryStrategy.alternativeCmd, retryCount + 1);
      }
    }

    // Phase 3: Search for solutions online (AI-enhanced)
    if (retryCount <= 2) {
      console.log(`🔍 Phase 3: Searching for solutions...`);
      
      // Try AI solution first
      if (this.geminiService.isAIEnabled()) {
        console.log(`🤖 Consulting AI for error solution...`);
        const aiSolution = await this.geminiService.findErrorSolution(error.command, error.stderr);
        
        if (aiSolution && aiSolution.confidence > 0.6) {
          console.log(`💡 AI Solution: ${aiSolution.description}`);
          console.log(`   Reasoning: ${aiSolution.reasoning}`);
          console.log(`   Confidence: ${aiSolution.confidence}`);
          
          if (aiSolution.commands.length > 0) {
            const solutionCommand = aiSolution.commands[0];
            console.log(`🔧 Trying AI solution: ${solutionCommand}`);
            await this.delay(2000);
            return await this.executeCommandWithRetry(solutionCommand, retryCount + 1);
          }
        }
      }
      
      // Fallback to built-in solutions
      const solutions = await this.searchSolution(error.stderr);
      
      if (solutions.length > 0) {
        const bestSolution = solutions[0]; // Use the highest confidence solution
        console.log(`💡 Built-in solution: ${bestSolution.description}`);
        console.log(`   Source: ${bestSolution.source} (confidence: ${bestSolution.confidence})`);
        console.log(`   Available commands: ${bestSolution.commands.join(', ')}`);
        
        if (bestSolution.commands.length > 0) {
          const solutionCommand = bestSolution.commands[0].replace('<original-command>', error.command);
          console.log(`🔧 Trying solution: ${solutionCommand}`);
          await this.delay(2000); // 2 second delay
          return await this.executeCommandWithRetry(solutionCommand, retryCount + 1);
        }
      } else {
        console.log(`🔍 No solutions found for this error`);
      }
    }

    // Phase 4: Final fallback - throw the original error
    console.log(`🛑 All retry attempts exhausted. Command failed permanently.`);
    throw error;
  }

  private isTransientError(error: CommandError): boolean {
    const transientPatterns = [
      'temporary failure',
      'timeout',
      'connection timed out',
      'network is unreachable',
      'resource temporarily unavailable',
      'device or resource busy',
      'interrupted system call'
    ];

    const errorMsg = error.stderr.toLowerCase();
    return transientPatterns.some(pattern => errorMsg.includes(pattern));
  }

  private async delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async handleError(error: CommandError): Promise<RetryStrategy> {
    console.log(`❌ Command failed: ${error.command}`);
    console.log(`   Error: ${error.stderr}`);
    console.log(`   Exit code: ${error.exitCode}`);

    // Analyze the error and determine retry strategy
    const strategy = this.analyzeError(error);
    
    if (strategy.shouldRetry) {
      console.log(`🔄 Will retry with strategy: ${strategy.alternativeCmd || 'same command'}`);
    } else {
      console.log(`🛑 No retry strategy available`);
    }

    return strategy;
  }

  async searchSolution(errorMessage: string): Promise<Solution[]> {
    const solutions: Solution[] = [];
    const errorLower = errorMessage.toLowerCase();

    // Built-in solution database
    const solutionDatabase = [
      {
        patterns: ['command not found', 'not found'],
        solution: {
          description: 'Install the missing command or package',
          commands: ['sudo apt update', 'sudo apt install <package-name>', 'which <command>'],
          source: 'built-in',
          confidence: 0.85
        }
      },
      {
        patterns: ['permission denied', 'access denied'],
        solution: {
          description: 'Fix permissions or run with elevated privileges',
          commands: ['sudo <original-command>', 'chmod +x <file>', 'chown $USER:$USER <file>'],
          source: 'built-in',
          confidence: 0.9
        }
      },
      {
        patterns: ['no space left on device', 'disk full'],
        solution: {
          description: 'Free up disk space',
          commands: ['df -h', 'sudo apt autoremove -y', 'sudo apt autoclean', 'sudo journalctl --vacuum-time=7d'],
          source: 'built-in',
          confidence: 0.8
        }
      },
      {
        patterns: ['unable to locate package', 'package not found', 'no installation candidate'],
        solution: {
          description: 'Update package lists or try alternative package managers',
          commands: ['sudo apt update', 'sudo snap install <package>', 'flatpak install <package>'],
          source: 'built-in',
          confidence: 0.75
        }
      },
      {
        patterns: ['connection refused', 'network unreachable', 'timeout'],
        solution: {
          description: 'Check network connectivity and retry',
          commands: ['ping -c 3 8.8.8.8', 'sudo systemctl restart NetworkManager', 'curl -I https://google.com'],
          source: 'built-in',
          confidence: 0.7
        }
      },
      {
        patterns: ['port already in use', 'address already in use'],
        solution: {
          description: 'Kill process using the port or use a different port',
          commands: ['sudo lsof -i :<port>', 'sudo kill -9 <pid>', 'netstat -tulpn | grep <port>'],
          source: 'built-in',
          confidence: 0.85
        }
      },
      {
        patterns: ['module not found', 'cannot import'],
        solution: {
          description: 'Install missing Python/Node.js dependencies',
          commands: ['pip install <module>', 'npm install <module>', 'pip3 install <module>'],
          source: 'built-in',
          confidence: 0.8
        }
      },
      {
        patterns: ['git: command not found'],
        solution: {
          description: 'Install Git version control system',
          commands: ['sudo apt install git', 'git --version'],
          source: 'built-in',
          confidence: 0.95
        }
      },
      {
        patterns: ['npm: command not found', 'node: command not found'],
        solution: {
          description: 'Install Node.js and npm',
          commands: ['curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -', 'sudo apt install nodejs', 'node --version && npm --version'],
          source: 'built-in',
          confidence: 0.9
        }
      },
      {
        patterns: ['docker: command not found'],
        solution: {
          description: 'Install Docker container platform',
          commands: ['sudo apt update', 'sudo apt install docker.io', 'sudo systemctl start docker', 'sudo usermod -aG docker $USER'],
          source: 'built-in',
          confidence: 0.9
        }
      },
      {
        patterns: ['snap: command not found'],
        solution: {
          description: 'Install Snap package manager',
          commands: ['sudo apt update', 'sudo apt install snapd', 'sudo systemctl enable snapd'],
          source: 'built-in',
          confidence: 0.9
        }
      },
      {
        patterns: ['flatpak: command not found'],
        solution: {
          description: 'Install Flatpak package manager',
          commands: ['sudo apt install flatpak', 'flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo'],
          source: 'built-in',
          confidence: 0.9
        }
      }
    ];

    // Search through solution database
    for (const entry of solutionDatabase) {
      if (entry.patterns.some(pattern => errorLower.includes(pattern))) {
        solutions.push(entry.solution);
      }
    }

    // Add context-aware solutions
    solutions.push(...this.getContextAwareSolutions(errorMessage));

    // Sort by confidence (highest first)
    solutions.sort((a, b) => b.confidence - a.confidence);

    // Simulate web search results (in a real implementation, this would query Stack Overflow, etc.)
    if (solutions.length === 0) {
      solutions.push(...await this.simulateWebSearch(errorMessage));
    }

    return solutions.slice(0, 3); // Return top 3 solutions
  }

  private getContextAwareSolutions(errorMessage: string): Solution[] {
    const solutions: Solution[] = [];
    const errorLower = errorMessage.toLowerCase();

    // Check if error mentions specific tools and provide installation solutions
    const toolInstallMap = {
      'curl': 'sudo apt install curl',
      'wget': 'sudo apt install wget',
      'unzip': 'sudo apt install unzip',
      'tar': 'sudo apt install tar',
      'vim': 'sudo apt install vim',
      'nano': 'sudo apt install nano',
      'htop': 'sudo apt install htop',
      'tree': 'sudo apt install tree',
      'jq': 'sudo apt install jq'
    };

    for (const [tool, installCmd] of Object.entries(toolInstallMap)) {
      if (errorLower.includes(tool) && errorLower.includes('not found')) {
        solutions.push({
          description: `Install ${tool} utility`,
          commands: [installCmd, `${tool} --help`],
          source: 'context-aware',
          confidence: 0.85
        });
      }
    }

    return solutions;
  }

  private async simulateWebSearch(errorMessage: string): Promise<Solution[]> {
    // Simulate web search delay
    await this.delay(1000);

    // Return generic solutions based on common patterns
    const genericSolutions: Solution[] = [
      {
        description: 'Check system logs for more details',
        commands: ['journalctl -xe', 'dmesg | tail -20', 'cat /var/log/syslog | tail -20'],
        source: 'web-search',
        confidence: 0.6
      },
      {
        description: 'Verify system dependencies and update',
        commands: ['sudo apt update', 'sudo apt install -f', 'sudo dpkg --configure -a'],
        source: 'web-search',
        confidence: 0.65
      },
      {
        description: 'Check available disk space and memory',
        commands: ['df -h', 'free -h', 'sudo du -sh /var/log/*'],
        source: 'web-search',
        confidence: 0.5
      }
    ];

    return genericSolutions;
  }

  async requestRootAccess(reason: string): Promise<boolean> {
    console.log(`🔐 Root access required: ${reason}`);
    console.log('   The system will prompt for your password when needed.');
    return true; // In a real implementation, this might show a confirmation dialog
  }

  private async executeGenericCommand(command: string): Promise<CommandResult> {
    const startTime = Date.now();

    try {
      // For sudo commands, inherit stdio to allow password input
      if (command.includes('sudo')) {
        return await this.executeSudoCommand(command, startTime);
      }

      const { stdout, stderr } = await execAsync(command, {
        timeout: this.commandTimeout,
        maxBuffer: 1024 * 1024 * 10 // 10MB buffer
      });

      const duration = Date.now() - startTime;

      return {
        exitCode: 0,
        stdout: stdout.trim(),
        stderr: stderr.trim(),
        duration
      };
    } catch (error: any) {
      const duration = Date.now() - startTime;
      
      // If the command failed, throw an error to trigger retry logic
      if (error.code && error.code !== 0) {
        let errorMessage = '';
        
        // Properly extract error message
        if (error.stderr && typeof error.stderr === 'string') {
          errorMessage = error.stderr.trim();
        } else if (error.message && typeof error.message === 'string') {
          errorMessage = error.message;
        } else if (error.stderr) {
          errorMessage = String(error.stderr);
        } else {
          errorMessage = `Command failed with exit code ${error.code}`;
        }
        
        const commandError: CommandError = {
          command,
          exitCode: error.code,
          stderr: errorMessage,
          timestamp: new Date()
        };
        throw commandError;
      }
      
      return {
        exitCode: error.code || 1,
        stdout: error.stdout?.trim() || '',
        stderr: error.stderr?.trim() || error.message,
        duration
      };
    }
  }

  private async executeSudoCommand(command: string, startTime: number): Promise<CommandResult> {
    return new Promise((resolve, reject) => {
      console.log(`🔐 Executing sudo command: ${command}`);
      console.log(`   Please enter your password when prompted...`);
      
      const child = spawn('bash', ['-c', command], {
        stdio: 'inherit' // This allows password input
      });

      child.on('close', (code) => {
        const duration = Date.now() - startTime;
        
        if (code === 0) {
          resolve({
            exitCode: 0,
            stdout: 'Command executed successfully',
            stderr: '',
            duration
          });
        } else {
          const error: CommandError = {
            command,
            exitCode: code || 1,
            stderr: `Command failed with exit code ${code}`,
            timestamp: new Date()
          };
          reject(error);
        }
      });

      child.on('error', (error) => {
        const duration = Date.now() - startTime;
        const commandError: CommandError = {
          command,
          exitCode: 1,
          stderr: error.message,
          timestamp: new Date()
        };
        reject(commandError);
      });
    });
  }

  private async handlePackageInstall(command: string): Promise<CommandResult> {
    const packageName = command.split(':')[1];
    
    if (!packageName) {
      throw new Error('Package name not specified');
    }

    console.log(`📦 Installing package: ${packageName}`);

    // Check if already installed
    const installCheck = await this.packageManager.isPackageInstalled(packageName);
    if (installCheck.installed) {
      console.log(`✅ Package ${packageName} is already installed (${installCheck.manager} v${installCheck.version})`);
      return {
        exitCode: 0,
        stdout: `Package ${packageName} already installed`,
        stderr: '',
        duration: 0
      };
    }

    // Use the enhanced package manager service
    const result = await this.packageManager.installPackage(packageName);
    
    if (result.success) {
      return {
        exitCode: 0,
        stdout: result.output || `Successfully installed ${packageName} with ${result.manager}`,
        stderr: '',
        duration: 0
      };
    } else {
      throw new Error(result.error || `Failed to install ${packageName}`);
    }
  }

  private async handleApplicationLaunch(command: string): Promise<CommandResult> {
    const appName = command.split(':')[1];
    
    if (!appName) {
      throw new Error('Application name not specified');
    }

    console.log(`🚀 Launching application: ${appName}`);

    // Try different ways to launch the application
    const launchCommands = [
      `${appName} &`,
      `nohup ${appName} > /dev/null 2>&1 &`,
      `gtk-launch ${appName}`,
      `xdg-open ${appName}`
    ];

    for (const launchCmd of launchCommands) {
      try {
        const result = await this.executeGenericCommand(launchCmd);
        if (result.exitCode === 0) {
          console.log(`✅ Successfully launched ${appName}`);
          return result;
        }
      } catch (error) {
        continue;
      }
    }

    throw new Error(`Failed to launch ${appName}`);
  }

  private async handleProjectStructureCreation(): Promise<CommandResult> {
    console.log(`📁 Creating project structure...`);

    const commands = [
      'mkdir -p portfolio-website',
      'cd portfolio-website',
      'mkdir -p src public assets',
      'touch src/index.html src/style.css src/script.js',
      'echo "Project structure created" > README.md'
    ];

    const combinedCommand = commands.join(' && ');
    return await this.executeGenericCommand(combinedCommand);
  }

  private async handleNpmInit(): Promise<CommandResult> {
    console.log(`📦 Initializing npm project...`);

    const command = 'cd portfolio-website && npm init -y';
    return await this.executeGenericCommand(command);
  }

  private async handleDevServerStart(): Promise<CommandResult> {
    console.log(`🌐 Starting development server...`);

    // Install a simple HTTP server if not available
    const installCmd = 'npm install -g http-server 2>/dev/null || echo "http-server already installed"';
    await this.executeGenericCommand(installCmd);

    // Start the server in the background
    const startCmd = 'cd portfolio-website && nohup http-server -p 3000 > server.log 2>&1 & echo "Server started on http://localhost:3000"';
    return await this.executeGenericCommand(startCmd);
  }

  private analyzeError(error: CommandError): RetryStrategy {
    const errorMsg = error.stderr.toLowerCase();

    // Command not found - try to install or suggest alternatives
    if (errorMsg.includes('command not found')) {
      return {
        shouldRetry: true,
        alternativeCmd: this.suggestAlternativeCommand(error.command),
        delaySeconds: 1,
        maxRetries: 2,
        searchSolutions: true
      };
    }

    // Permission denied - try with sudo
    if (errorMsg.includes('permission denied') && !error.command.includes('sudo')) {
      return {
        shouldRetry: true,
        alternativeCmd: `sudo ${error.command}`,
        delaySeconds: 1,
        maxRetries: 1,
        searchSolutions: false
      };
    }

    // Package not found - try different package managers
    if (errorMsg.includes('unable to locate package') || errorMsg.includes('package not found')) {
      return {
        shouldRetry: true,
        alternativeCmd: this.suggestAlternativePackageManager(error.command),
        delaySeconds: 2,
        maxRetries: 2,
        searchSolutions: true
      };
    }

    // Network issues - retry with delay
    if (errorMsg.includes('network') || errorMsg.includes('timeout') || errorMsg.includes('connection')) {
      return {
        shouldRetry: true,
        alternativeCmd: error.command,
        delaySeconds: 5,
        maxRetries: 3,
        searchSolutions: false
      };
    }

    // Default: no retry
    return {
      shouldRetry: false,
      delaySeconds: 0,
      maxRetries: 0,
      searchSolutions: true
    };
  }

  private suggestAlternativeCommand(command: string): string {
    // Map common commands to alternatives
    const alternatives: Record<string, string> = {
      'python': 'python3',
      'pip': 'pip3',
      'node': 'nodejs',
      'vim': 'nano',
      'emacs': 'nano',
      'curl': 'wget',
      'wget': 'curl'
    };

    const cmdParts = command.split(' ');
    const baseCmd = cmdParts[0];

    if (alternatives[baseCmd]) {
      cmdParts[0] = alternatives[baseCmd];
      return cmdParts.join(' ');
    }

    return command;
  }

  private suggestAlternativePackageManager(command: string): string {
    if (command.includes('apt install')) {
      const packageName = command.split(' ').pop();
      return `sudo snap install ${packageName}`;
    } else if (command.includes('snap install')) {
      const packageName = command.split(' ').pop();
      return `flatpak install -y ${packageName}`;
    } else if (command.includes('flatpak install')) {
      const packageName = command.split(' ').pop();
      return `sudo apt install -y ${packageName}`;
    }

    return command;
  }
}