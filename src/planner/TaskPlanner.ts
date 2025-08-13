import { ParsedCommand, ExecutionPlan, TaskStep, RiskLevel, ExecutionMode } from '../types/interfaces';

interface TaskPattern {
  name: string;
  steps: TaskStep[];
  dependencies: string[];
  riskLevel: RiskLevel;
  requiresRoot: boolean;
}

export class TaskPlanner {
  private taskPatterns: Record<string, TaskPattern>;

  constructor() {
    this.taskPatterns = this.initializeTaskPatterns();
  }

  async createPlan(cmd: ParsedCommand): Promise<ExecutionPlan> {
    // Analyze the steps to determine dependencies and risk level
    const dependencies = this.analyzeDependencies(cmd.steps, cmd.requiredTools);
    const riskLevel = this.assessRiskLevel(cmd.steps, cmd.requiredTools);
    const requiresRoot = this.checkRootRequirement(cmd.steps, cmd.requiredTools);
    
    // Optimize the step order based on dependencies
    const optimizedSteps = this.optimizeStepOrder(cmd.steps, dependencies);
    
    return {
      steps: optimizedSteps,
      dependencies,
      riskLevel,
      requiresRoot
    };
  }

  async breakdownTask(task: string, mode: ExecutionMode): Promise<TaskStep[]> {
    const taskLower = task.toLowerCase().trim();
    
    // Check if we have a known pattern for this task
    for (const [patternName, pattern] of Object.entries(this.taskPatterns)) {
      if (this.matchesPattern(taskLower, patternName)) {
        return this.adaptPatternSteps(pattern.steps, taskLower);
      }
    }
    
    // If no pattern matches, create a generic breakdown
    return this.createGenericBreakdown(taskLower, mode);
  }

  estimateComplexity(steps: TaskStep[]): number {
    let complexity = 0;
    
    for (const step of steps) {
      // Base complexity per step
      complexity += 10;
      
      // Additional complexity based on step type
      switch (step.type) {
        case 'browser':
          complexity += 15; // Browser operations are more complex
          break;
        case 'terminal':
          complexity += 5;
          break;
        case 'file':
          complexity += 8;
          break;
        case 'wait':
          complexity += 3;
          break;
      }
      
      // Additional complexity for special requirements
      if (step.requiresAuth) {
        complexity += 20;
      }
      
      if (step.fallbackSteps && step.fallbackSteps.length > 0) {
        complexity += step.fallbackSteps.length * 5;
      }
      
      // Complexity based on command content
      if (step.command?.includes('install')) {
        complexity += 10;
      }
      if (step.command?.includes('compile') || step.command?.includes('build')) {
        complexity += 15;
      }
      if (step.command?.includes('deploy')) {
        complexity += 25;
      }
    }
    
    return complexity;
  }

  private analyzeDependencies(steps: TaskStep[], requiredTools: string[]): string[] {
    const dependencies: string[] = [...requiredTools];
    
    // Analyze step dependencies
    for (const step of steps) {
      const stepDeps = this.getStepDependencies(step);
      dependencies.push(...stepDeps);
    }
    
    // Remove duplicates
    return [...new Set(dependencies)];
  }

  private assessRiskLevel(steps: TaskStep[], requiredTools: string[]): RiskLevel {
    let riskScore = 0;
    
    // Risk from tools
    const highRiskTools = ['rm', 'dd', 'mkfs', 'fdisk', 'parted'];
    const mediumRiskTools = ['sudo', 'chmod', 'chown', 'systemctl'];
    
    for (const tool of requiredTools) {
      for (const highRisk of highRiskTools) {
        if (tool.includes(highRisk)) {
          riskScore += 30;
        }
      }
      for (const mediumRisk of mediumRiskTools) {
        if (tool.includes(mediumRisk)) {
          riskScore += 15;
        }
      }
    }
    
    // Risk from steps
    for (const step of steps) {
      if (step.command?.includes('delete') || step.command?.includes('remove')) {
        riskScore += 20;
      }
      if (step.command?.includes('format') || step.command?.includes('wipe')) {
        riskScore += 40;
      }
      if (step.requiresAuth) {
        riskScore += 10;
      }
      if (step.type === 'browser' && step.command?.includes('login')) {
        riskScore += 15;
      }
    }
    
    // Determine risk level
    if (riskScore >= 40) {
      return 'high';
    } else if (riskScore >= 20) {
      return 'medium';
    }
    return 'low';
  }

  private checkRootRequirement(steps: TaskStep[], requiredTools: string[]): boolean {
    const rootTools = ['apt', 'snap', 'flatpak', 'systemctl', 'service'];
    
    for (const tool of requiredTools) {
      if (rootTools.includes(tool)) {
        return true;
      }
    }
    
    for (const step of steps) {
      if (step.command?.includes('install_package')) {
        return true;
      }
      if (step.command?.includes('sudo')) {
        return true;
      }
      if (step.command?.includes('systemctl')) {
        return true;
      }
    }
    
    return false;
  }

  private optimizeStepOrder(steps: TaskStep[], dependencies: string[]): TaskStep[] {
    // For now, return steps as-is
    // TODO: Implement dependency-based ordering
    return steps;
  }

  private matchesPattern(task: string, patternName: string): boolean {
    switch (patternName) {
      case 'install_and_open':
        return task.includes('install') && task.includes('open');
      case 'search_wallpapers':
        return task.includes('search') && task.includes('wallpaper');
      case 'gmail_summary':
        return task.includes('gmail') || task.includes('mail summary');
      case 'portfolio_from_pdf':
        return task.includes('portfolio') && task.includes('.pdf');
      case 'git_repo_create':
        return task.includes('git') && (task.includes('repo') || task.includes('repository'));
      default:
        return false;
    }
  }

  private adaptPatternSteps(patternSteps: TaskStep[], task: string): TaskStep[] {
    return patternSteps.map((step, i) => ({
      ...step,
      id: `step_${i + 1}`,
      command: step.command
        ?.replace('PACKAGE_NAME', this.extractPackageName(task))
        .replace('FILE_PATH', this.extractFilePath(task)) || step.command || ''
    }));
  }

  private createGenericBreakdown(task: string, mode: ExecutionMode): TaskStep[] {
    const stepType = mode === 'browser' ? 'browser' : 'terminal';
    
    // Create a single generic step
    const step: TaskStep = {
      id: 'step_1',
      type: stepType,
      command: task
    };
    
    // Add authentication requirement for browser tasks that might need it
    if (stepType === 'browser') {
      const authKeywords = ['login', 'gmail', 'email', 'account', 'profile'];
      for (const keyword of authKeywords) {
        if (task.includes(keyword)) {
          step.requiresAuth = true;
          break;
        }
      }
    }
    
    return [step];
  }

  private getStepDependencies(step: TaskStep): string[] {
    const deps: string[] = [];
    
    if (step.command?.includes('install_package')) {
      deps.push('package_manager');
    }
    if (step.command?.includes('npm')) {
      deps.push('nodejs', 'npm');
    }
    if (step.command?.includes('git')) {
      deps.push('git');
    }
    if (step.command?.includes('docker')) {
      deps.push('docker');
    }
    if (step.type === 'browser') {
      deps.push('browser');
    }
    if (step.command?.includes('pdf')) {
      deps.push('pdf_reader');
    }
    
    return deps;
  }

  private extractPackageName(task: string): string {
    // Simple extraction - look for word after "install" or "open"
    const words = task.split(/\s+/);
    for (let i = 0; i < words.length; i++) {
      if ((words[i] === 'install' || words[i] === 'open') && i + 1 < words.length) {
        return words[i + 1];
      }
    }
    return 'unknown';
  }

  private extractFilePath(task: string): string {
    // Look for file paths in the task
    const words = task.split(/\s+/);
    for (const word of words) {
      if (word.includes('/') || word.startsWith('~')) {
        return word;
      }
    }
    return '';
  }

  private initializeTaskPatterns(): Record<string, TaskPattern> {
    return {
      install_and_open: {
        name: 'Install and Open Application',
        steps: [
          {
            id: 'step_1',
            type: 'terminal',
            command: 'install_package:PACKAGE_NAME'
          },
          {
            id: 'step_2',
            type: 'terminal',
            command: 'launch_application:PACKAGE_NAME'
          }
        ],
        dependencies: ['package_manager'],
        riskLevel: 'low',
        requiresRoot: true
      },
      search_wallpapers: {
        name: 'Search for Wallpapers',
        steps: [
          {
            id: 'step_1',
            type: 'browser',
            command: 'search_wallpapers'
          }
        ],
        dependencies: ['browser'],
        riskLevel: 'low',
        requiresRoot: false
      },
      gmail_summary: {
        name: 'Gmail Summary',
        steps: [
          {
            id: 'step_1',
            type: 'browser',
            command: 'open_gmail',
            requiresAuth: true
          },
          {
            id: 'step_2',
            type: 'browser',
            command: 'extract_emails'
          },
          {
            id: 'step_3',
            type: 'browser',
            command: 'summarize_emails'
          }
        ],
        dependencies: ['browser'],
        riskLevel: 'low',
        requiresRoot: false
      },
      portfolio_from_pdf: {
        name: 'Create Portfolio from PDF',
        steps: [
          {
            id: 'step_1',
            type: 'file',
            command: 'read_pdf:FILE_PATH'
          },
          {
            id: 'step_2',
            type: 'terminal',
            command: 'create_project_structure'
          },
          {
            id: 'step_3',
            type: 'terminal',
            command: 'npm_init'
          },
          {
            id: 'step_4',
            type: 'file',
            command: 'generate_website'
          },
          {
            id: 'step_5',
            type: 'terminal',
            command: 'start_dev_server'
          },
          {
            id: 'step_6',
            type: 'browser',
            command: 'open_localhost'
          }
        ],
        dependencies: ['nodejs', 'npm', 'pdf_reader'],
        riskLevel: 'low',
        requiresRoot: false
      }
    };
  }
}