import { CommandInput, ParsedCommand, ExecutionMode, TaskStep, TaskStepType } from '../types/interfaces';

export class CommandParser {
  private terminalPatterns: string[] = [
    'install\\s+\\w+',
    'update\\s+system',
    'create\\s+directory',
    'download\\s+.*\\.(zip|tar|gz|deb|rpm)',
    'extract\\s+',
    'unzip\\s+',
    'tar\\s+',
    'apt\\s+install',
    'snap\\s+install',
    'flatpak\\s+install',
    'git\\s+clone',
    'npm\\s+install',
    'docker\\s+run',
    'systemctl\\s+',
    'service\\s+',
    'chmod\\s+',
    'chown\\s+',
    'mkdir\\s+',
    'cp\\s+',
    'mv\\s+',
    'rm\\s+',
    'find\\s+',
    'grep\\s+',
    'sed\\s+',
    'awk\\s+'
  ];

  private browserPatterns: string[] = [
    'gmail',
    'email',
    'mail\\s+summary',
    'browse\\s+',
    'search\\s+.*wallpaper',
    'search\\s+.*online',
    'login\\s+to',
    'navigate\\s+to',
    'open\\s+.*\\.com',
    'visit\\s+website',
    'web\\s+search',
    'google\\s+',
    'youtube\\s+',
    'github\\s+.*create',
    'deploy\\s+to\\s+vercel',
    'upload\\s+to\\s+git'
  ];

  private filePatterns: string[] = [
    '\\.pdf$',
    '\\.txt$',
    '\\.doc$',
    '\\.docx$',
    '\\.jpg$',
    '\\.png$',
    '~/\\w+',
    '/home/\\w+',
    'read\\s+.*file',
    'extract\\s+.*from\\s+.*\\.pdf',
    'use\\s+.*\\.pdf'
  ];

  private toolIndicators: Record<string, string[]> = {
    apt: ['install', 'update', 'upgrade', 'remove'],
    snap: ['install', 'remove', 'refresh'],
    flatpak: ['install', 'uninstall', 'update'],
    git: ['clone', 'pull', 'push', 'commit', 'init'],
    npm: ['install', 'init', 'start', 'build', 'run'],
    docker: ['run', 'build', 'pull', 'push', 'ps'],
    curl: ['download', 'fetch', 'get'],
    wget: ['download', 'fetch'],
    unzip: ['extract', 'unpack'],
    tar: ['extract', 'compress', 'archive'],
    browser: ['gmail', 'search', 'browse', 'navigate', 'login']
  };

  async parse(input: CommandInput): Promise<ParsedCommand> {
    // Normalize the task string
    const task = input.task.toLowerCase().trim();
    
    // Detect execution mode if not specified or if auto
    let executionMode = input.mode;
    if (executionMode === 'auto' || input.isAlidoCommand) {
      executionMode = this.detectMode(task);
    }
    
    // Break down the task into steps
    const steps = await this.breakdownTask(task, executionMode);
    
    // Identify required tools
    const requiredTools = this.identifyRequiredTools(task);
    
    // Estimate complexity
    const complexity = this.estimateComplexity(steps, requiredTools);
    
    return {
      executionMode,
      steps,
      requiredTools,
      estimatedComplexity: complexity
    };
  }

  detectMode(task: string): ExecutionMode {
    const taskLower = task.toLowerCase();
    
    // Count matches for each mode
    let terminalScore = 0;
    let browserScore = 0;
    
    // Check terminal patterns
    for (const pattern of this.terminalPatterns) {
      if (new RegExp(pattern, 'i').test(taskLower)) {
        terminalScore++;
      }
    }
    
    // Check browser patterns
    for (const pattern of this.browserPatterns) {
      if (new RegExp(pattern, 'i').test(taskLower)) {
        browserScore++;
      }
    }
    
    // Check for file operations (usually terminal)
    for (const pattern of this.filePatterns) {
      if (new RegExp(pattern, 'i').test(taskLower)) {
        terminalScore++;
      }
    }
    
    // Special cases that strongly indicate browser mode
    const browserKeywords = ['gmail', 'email', 'mail summary', 'search wallpaper', 'browse', 'website'];
    for (const keyword of browserKeywords) {
      if (taskLower.includes(keyword)) {
        browserScore += 2; // Higher weight
      }
    }
    
    // Special cases that strongly indicate terminal mode
    const terminalKeywords = ['install', 'apt', 'snap', 'flatpak', 'git clone', 'npm', 'docker', 'extract', 'unzip'];
    for (const keyword of terminalKeywords) {
      if (taskLower.includes(keyword)) {
        terminalScore += 2; // Higher weight
      }
    }
    
    // Decide based on scores
    if (browserScore > terminalScore) {
      return 'browser';
    }
    
    // Default to terminal (as per requirements - terminal-first approach)
    return 'terminal';
  }

  extractContext(task: string): Record<string, any> {
    const context: Record<string, any> = {};
    
    // Extract file paths
    const filePaths = this.extractFilePaths(task);
    if (filePaths.length > 0) {
      context.filePaths = filePaths;
    }
    
    // Extract URLs
    const urls = this.extractURLs(task);
    if (urls.length > 0) {
      context.urls = urls;
    }
    
    // Extract package names
    const packages = this.extractPackageNames(task);
    if (packages.length > 0) {
      context.packages = packages;
    }
    
    // Extract project names
    const projects = this.extractProjectNames(task);
    if (projects.length > 0) {
      context.projects = projects;
    }
    
    return context;
  }

  private async breakdownTask(task: string, mode: ExecutionMode): Promise<TaskStep[]> {
    const steps: TaskStep[] = [];
    let stepID = 1;
    
    // Analyze the task for different components
    if (task.includes('install') && task.includes('open')) {
      // Install and open pattern
      const packageName = this.extractPackageFromInstallCommand(task);
      if (packageName) {
        steps.push({
          id: `step_${stepID++}`,
          type: 'terminal',
          command: `install_package:${packageName}`
        });
        
        steps.push({
          id: `step_${stepID++}`,
          type: 'terminal',
          command: `launch_application:${packageName}`
        });
      }
    } else if (task.includes('search') && task.includes('wallpaper')) {
      // Search wallpapers pattern
      steps.push({
        id: `step_${stepID++}`,
        type: 'browser',
        command: 'search_wallpapers'
      });
    } else if (task.includes('gmail') || task.includes('mail summary')) {
      // Gmail/email pattern
      steps.push({
        id: `step_${stepID++}`,
        type: 'browser',
        command: 'open_gmail',
        requiresAuth: true
      });
      
      steps.push({
        id: `step_${stepID++}`,
        type: 'browser',
        command: 'extract_emails'
      });
      
      steps.push({
        id: `step_${stepID++}`,
        type: 'browser',
        command: 'summarize_emails'
      });
    } else if (task.includes('portfolio') && task.includes('.pdf')) {
      // Portfolio creation from PDF pattern
      const pdfPaths = this.extractFilePaths(task);
      if (pdfPaths.length > 0) {
        steps.push({
          id: `step_${stepID++}`,
          type: 'file',
          command: `read_pdf:${pdfPaths[0]}`
        });
        
        steps.push({
          id: `step_${stepID++}`,
          type: 'terminal',
          command: 'create_project_structure'
        });
        
        steps.push({
          id: `step_${stepID++}`,
          type: 'terminal',
          command: 'npm_init'
        });
        
        steps.push({
          id: `step_${stepID++}`,
          type: 'file',
          command: 'generate_website'
        });
        
        steps.push({
          id: `step_${stepID++}`,
          type: 'terminal',
          command: 'start_dev_server'
        });
        
        steps.push({
          id: `step_${stepID++}`,
          type: 'browser',
          command: 'open_localhost'
        });
      }
    } else {
      // Generic task - create a single step
      const stepType: TaskStepType = mode === 'browser' ? 'browser' : 'terminal';
      
      steps.push({
        id: `step_${stepID++}`,
        type: stepType,
        command: task
      });
    }
    
    return steps;
  }

  private identifyRequiredTools(task: string): string[] {
    const tools: string[] = [];
    const taskLower = task.toLowerCase();
    
    for (const [tool, indicators] of Object.entries(this.toolIndicators)) {
      for (const indicator of indicators) {
        if (taskLower.includes(indicator)) {
          tools.push(tool);
          break;
        }
      }
    }
    
    // Remove duplicates
    return [...new Set(tools)];
  }

  private estimateComplexity(steps: TaskStep[], tools: string[]): number {
    let complexity = steps.length * 10; // Base complexity from number of steps
    
    // Add complexity for each tool
    complexity += tools.length * 5;
    
    // Add complexity for special operations
    for (const step of steps) {
      if (step.requiresAuth) {
        complexity += 15; // Authentication adds complexity
      }
      if (step.type === 'browser') {
        complexity += 10; // Browser operations are more complex
      }
      if (step.fallbackSteps && step.fallbackSteps.length > 0) {
        complexity += step.fallbackSteps.length * 5;
      }
    }
    
    return complexity;
  }

  // Helper functions for extraction
  private extractFilePaths(task: string): string[] {
    const pathRegex = /[~./][\w/.-]*\.\w+/g;
    return task.match(pathRegex) || [];
  }

  private extractURLs(task: string): string[] {
    const urlRegex = /https?:\/\/[^\s]+/g;
    return task.match(urlRegex) || [];
  }

  private extractPackageNames(task: string): string[] {
    const packages: string[] = [];
    
    // Look for install commands
    const installRegex = /install\s+(\w+)/g;
    let match;
    while ((match = installRegex.exec(task)) !== null) {
      packages.push(match[1]);
    }
    
    return packages;
  }

  private extractProjectNames(task: string): string[] {
    const projects: string[] = [];
    
    // Look for project creation patterns
    const projectRegex = /(?:create|make|init).*?(?:project|repo|repository)\s+(?:named\s+)?(\w+)/g;
    let match;
    while ((match = projectRegex.exec(task)) !== null) {
      projects.push(match[1]);
    }
    
    return projects;
  }

  private extractPackageFromInstallCommand(task: string): string | null {
    // Extract package name from "install and open X" pattern
    const installOpenRegex = /install\s+(?:and\s+open\s+)?(\w+)/;
    const match = task.match(installOpenRegex);
    return match ? match[1] : null;
  }
}