import { colors } from '../utils/Colors.js';
import { symbols } from '../utils/Symbols.js';
import { Layout } from '../utils/Layout.js';
import { getCurrentTheme } from '../themes/ThemeManager.js';

export interface Step {
  id: string;
  title: string;
  description?: string;
  estimatedTime?: number; // in seconds
  optional?: boolean;
  dependencies?: string[]; // step IDs that must complete first
}

export interface StepStatus {
  id: string;
  status: 'pending' | 'active' | 'completed' | 'failed' | 'skipped';
  startTime?: Date;
  endTime?: Date;
  error?: string;
  progress?: number; // 0-100 for active steps
}

export interface StepProgressOptions {
  steps: Step[];
  showEstimatedTime?: boolean;
  showProgress?: boolean;
  compact?: boolean;
  showBreadcrumbs?: boolean;
  maxWidth?: number;
}

export class StepProgress {
  private steps: Step[];
  private stepStatuses: Map<string, StepStatus>;
  private options: StepProgressOptions;
  private theme = getCurrentTheme();
  private startTime?: Date;

  constructor(options: StepProgressOptions) {
    this.steps = options.steps;
    this.options = {
      showEstimatedTime: true,
      showProgress: true,
      compact: false,
      showBreadcrumbs: true,
      maxWidth: 80,
      ...options
    };
    
    // Initialize step statuses
    this.stepStatuses = new Map();
    this.steps.forEach(step => {
      this.stepStatuses.set(step.id, {
        id: step.id,
        status: 'pending'
      });
    });
  }

  /**
   * Start the progress tracking
   */
  start(): void {
    this.startTime = new Date();
    this.render();
  }

  /**
   * Start a specific step
   */
  startStep(stepId: string): void {
    const status = this.stepStatuses.get(stepId);
    if (status) {
      status.status = 'active';
      status.startTime = new Date();
      status.progress = 0;
      this.render();
    }
  }

  /**
   * Update progress of an active step
   */
  updateStepProgress(stepId: string, progress: number, description?: string): void {
    const status = this.stepStatuses.get(stepId);
    if (status && status.status === 'active') {
      status.progress = Math.max(0, Math.min(100, progress));
      
      // Update step description if provided
      const step = this.steps.find(s => s.id === stepId);
      if (step && description) {
        step.description = description;
      }
      
      this.render();
    }
  }

  /**
   * Complete a step successfully
   */
  completeStep(stepId: string): void {
    const status = this.stepStatuses.get(stepId);
    if (status) {
      status.status = 'completed';
      status.endTime = new Date();
      status.progress = 100;
      this.render();
    }
  }

  /**
   * Mark a step as failed
   */
  failStep(stepId: string, error?: string): void {
    const status = this.stepStatuses.get(stepId);
    if (status) {
      status.status = 'failed';
      status.endTime = new Date();
      status.error = error;
      this.render();
    }
  }

  /**
   * Skip a step (for optional steps)
   */
  skipStep(stepId: string): void {
    const status = this.stepStatuses.get(stepId);
    const step = this.steps.find(s => s.id === stepId);
    if (status && step?.optional) {
      status.status = 'skipped';
      status.endTime = new Date();
      this.render();
    }
  }

  /**
   * Get current progress summary
   */
  getProgress(): {
    completed: number;
    total: number;
    percentage: number;
    currentStep?: Step;
    estimatedTimeRemaining?: number;
  } {
    const completed = Array.from(this.stepStatuses.values())
      .filter(s => s.status === 'completed').length;
    const total = this.steps.length;
    const percentage = total > 0 ? (completed / total) * 100 : 0;
    
    const currentStatus = Array.from(this.stepStatuses.values())
      .find(s => s.status === 'active');
    const currentStep = currentStatus ? 
      this.steps.find(s => s.id === currentStatus.id) : undefined;

    let estimatedTimeRemaining: number | undefined;
    if (this.options.showEstimatedTime && this.startTime) {
      estimatedTimeRemaining = this.calculateEstimatedTimeRemaining();
    }

    return {
      completed,
      total,
      percentage,
      ...(currentStep && { currentStep }),
      ...(estimatedTimeRemaining && { estimatedTimeRemaining })
    };
  }

  /**
   * Render the current progress state
   */
  render(): void {
    // Clear previous output (move cursor up and clear lines)
    const linesToClear = this.calculateOutputLines();
    if (linesToClear > 0) {
      process.stdout.write(`\x1B[${linesToClear}A`); // Move cursor up
      process.stdout.write('\x1B[0J'); // Clear from cursor to end of screen
    }

    if (this.options.showBreadcrumbs) {
      this.renderBreadcrumbs();
    }

    if (this.options.compact) {
      this.renderCompact();
    } else {
      this.renderDetailed();
    }

    if (this.options.showEstimatedTime) {
      this.renderTimeInfo();
    }
  }

  /**
   * Render breadcrumb navigation
   */
  private renderBreadcrumbs(): void {
    const breadcrumbs: string[] = [];
    
    this.steps.forEach((step, index) => {
      const status = this.stepStatuses.get(step.id)!;
      let crumb = '';
      
      switch (status.status) {
        case 'completed':
          crumb = this.theme.colors.success(step.title);
          break;
        case 'active':
          crumb = this.theme.colors.primary(step.title);
          break;
        case 'failed':
          crumb = this.theme.colors.error(step.title);
          break;
        case 'skipped':
          crumb = this.theme.colors.muted(`${step.title} (skipped)`);
          break;
        default:
          crumb = this.theme.colors.textMuted(step.title);
      }
      
      breadcrumbs.push(crumb);
    });

    const separator = this.theme.colors.muted(` ${symbols.arrowRight} `);
    const breadcrumbLine = breadcrumbs.join(separator);
    
    console.log(Layout.wrap(breadcrumbLine, this.options.maxWidth || 80)[0]);
    console.log(); // Empty line
  }

  /**
   * Render compact progress view
   */
  private renderCompact(): void {
    const progress = this.getProgress();
    const progressBar = this.createProgressBar(progress.percentage);
    
    let line = `${progressBar} ${progress.completed}/${progress.total}`;
    
    if (progress.currentStep) {
      line += ` - ${this.theme.colors.primary(progress.currentStep.title)}`;
    }
    
    console.log(line);
  }

  /**
   * Render detailed progress view
   */
  private renderDetailed(): void {
    this.steps.forEach((step, index) => {
      const status = this.stepStatuses.get(step.id)!;
      this.renderStep(step, status, index + 1);
    });
  }

  /**
   * Render a single step
   */
  private renderStep(step: Step, status: StepStatus, stepNumber: number): void {
    let line = '';
    
    // Step number and status indicator
    const stepNum = this.theme.colors.muted(`${stepNumber}.`);
    let statusIcon = '';
    let titleColor = this.theme.colors.text;
    
    switch (status.status) {
      case 'completed':
        statusIcon = this.theme.colors.success(symbols.success);
        titleColor = this.theme.colors.success;
        break;
      case 'active':
        statusIcon = this.theme.colors.primary(symbols.loading[0]); // Use first loading symbol
        titleColor = this.theme.colors.primary;
        break;
      case 'failed':
        statusIcon = this.theme.colors.error(symbols.error);
        titleColor = this.theme.colors.error;
        break;
      case 'skipped':
        statusIcon = this.theme.colors.muted('-');
        titleColor = this.theme.colors.muted;
        break;
      default:
        statusIcon = this.theme.colors.muted(symbols.circle);
        titleColor = this.theme.colors.textMuted;
    }
    
    line += `${stepNum} ${statusIcon} ${titleColor(step.title)}`;
    
    // Add optional indicator
    if (step.optional) {
      line += ` ${this.theme.colors.muted('(optional)')}`;
    }
    
    console.log(line);
    
    // Show description if available
    if (step.description) {
      const descColor = status.status === 'active' ? 
        this.theme.colors.secondary : this.theme.colors.textMuted;
      console.log(`   ${descColor(step.description)}`);
    }
    
    // Show progress bar for active steps
    if (status.status === 'active' && this.options.showProgress && status.progress !== undefined) {
      const progressBar = this.createProgressBar(status.progress, 30);
      console.log(`   ${progressBar} ${status.progress.toFixed(0)}%`);
    }
    
    // Show error for failed steps
    if (status.status === 'failed' && status.error) {
      console.log(`   ${this.theme.colors.error(`Error: ${status.error}`)}`);
    }
    
    // Show timing info for completed steps
    if (status.status === 'completed' && status.startTime && status.endTime) {
      const duration = status.endTime.getTime() - status.startTime.getTime();
      const durationText = this.formatDuration(duration);
      console.log(`   ${this.theme.colors.muted(`Completed in ${durationText}`)}`);
    }
  }

  /**
   * Render time information
   */
  private renderTimeInfo(): void {
    const progress = this.getProgress();
    
    console.log(); // Empty line
    
    let timeInfo = '';
    
    if (this.startTime) {
      const elapsed = new Date().getTime() - this.startTime.getTime();
      timeInfo += `Elapsed: ${this.formatDuration(elapsed)}`;
    }
    
    if (progress.estimatedTimeRemaining !== undefined) {
      if (timeInfo) timeInfo += ' | ';
      timeInfo += `Remaining: ${this.formatDuration(progress.estimatedTimeRemaining * 1000)}`;
    }
    
    if (timeInfo) {
      console.log(this.theme.colors.muted(timeInfo));
    }
  }

  /**
   * Create a progress bar string
   */
  private createProgressBar(percentage: number, width: number = 20): string {
    const filled = Math.round((percentage / 100) * width);
    const empty = width - filled;
    
    const filledBar = this.theme.colors.success(symbols.progressFull.repeat(filled));
    const emptyBar = this.theme.colors.muted(symbols.progressEmpty.repeat(empty));
    
    return `[${filledBar}${emptyBar}]`;
  }

  /**
   * Calculate estimated time remaining
   */
  private calculateEstimatedTimeRemaining(): number {
    if (!this.startTime) return 0;
    
    const completedSteps = Array.from(this.stepStatuses.values())
      .filter(s => s.status === 'completed');
    
    if (completedSteps.length === 0) {
      // Use estimated times from step definitions
      return this.steps.reduce((total, step) => total + (step.estimatedTime || 30), 0);
    }
    
    // Calculate average time per completed step
    const totalElapsed = new Date().getTime() - this.startTime.getTime();
    const avgTimePerStep = totalElapsed / completedSteps.length;
    
    const remainingSteps = this.steps.length - completedSteps.length;
    return (avgTimePerStep * remainingSteps) / 1000; // Convert to seconds
  }

  /**
   * Format duration in milliseconds to human readable string
   */
  private formatDuration(ms: number): string {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    
    if (hours > 0) {
      return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
    } else if (minutes > 0) {
      return `${minutes}m ${seconds % 60}s`;
    } else {
      return `${seconds}s`;
    }
  }

  /**
   * Calculate how many lines the current output takes
   */
  private calculateOutputLines(): number {
    let lines = 0;
    
    if (this.options.showBreadcrumbs) {
      lines += 2; // Breadcrumb line + empty line
    }
    
    if (this.options.compact) {
      lines += 1;
    } else {
      this.steps.forEach(step => {
        const status = this.stepStatuses.get(step.id)!;
        lines += 1; // Main step line
        
        if (step.description) lines += 1;
        if (status.status === 'active' && this.options.showProgress) lines += 1;
        if (status.status === 'failed' && status.error) lines += 1;
        if (status.status === 'completed' && status.startTime && status.endTime) lines += 1;
      });
    }
    
    if (this.options.showEstimatedTime) {
      lines += 2; // Empty line + time info
    }
    
    return lines;
  }

  /**
   * Complete all steps and show final summary
   */
  complete(): void {
    const progress = this.getProgress();
    const totalTime = this.startTime ? 
      new Date().getTime() - this.startTime.getTime() : 0;
    
    console.log();
    console.log(this.theme.colors.success(`${symbols.success} All steps completed!`));
    
    if (totalTime > 0) {
      console.log(this.theme.colors.muted(`Total time: ${this.formatDuration(totalTime)}`));
    }
    
    console.log();
  }

  /**
   * Show failure summary
   */
  fail(error?: string): void {
    console.log();
    console.log(this.theme.colors.error(`${symbols.error} Process failed`));
    
    if (error) {
      console.log(this.theme.colors.error(error));
    }
    
    // Show failed steps
    const failedSteps = Array.from(this.stepStatuses.entries())
      .filter(([_, status]) => status.status === 'failed')
      .map(([stepId, _]) => this.steps.find(s => s.id === stepId))
      .filter(Boolean);
    
    if (failedSteps.length > 0) {
      console.log();
      console.log(this.theme.colors.error('Failed steps:'));
      failedSteps.forEach(step => {
        if (step) {
          const status = this.stepStatuses.get(step.id)!;
          console.log(`  ${this.theme.colors.error(symbols.error)} ${step.title}`);
          if (status.error) {
            console.log(`    ${this.theme.colors.muted(status.error)}`);
          }
        }
      });
    }
    
    console.log();
  }
}

// Utility functions for common step progress patterns

/**
 * Create a simple linear step progress
 */
export function createLinearProgress(stepTitles: string[], options?: Partial<StepProgressOptions>): StepProgress {
  const steps: Step[] = stepTitles.map((title, index) => ({
    id: `step-${index + 1}`,
    title,
    estimatedTime: 30 // Default 30 seconds per step
  }));
  
  return new StepProgress({
    steps,
    ...options
  });
}

/**
 * Create step progress with dependencies
 */
export function createDependentProgress(stepConfigs: Array<{
  title: string;
  dependencies?: string[];
  estimatedTime?: number;
  optional?: boolean;
}>, options?: Partial<StepProgressOptions>): StepProgress {
  const steps: Step[] = stepConfigs.map((config, index) => ({
    id: `step-${index + 1}`,
    ...config
  }));
  
  return new StepProgress({
    steps,
    ...options
  });
}

/**
 * Run steps with automatic progress tracking
 */
export async function runStepsWithProgress<T>(
  stepProgress: StepProgress,
  stepFunctions: Array<() => Promise<T>>
): Promise<T[]> {
  const results: T[] = [];
  
  stepProgress.start();
  
  try {
    for (let i = 0; i < stepFunctions.length; i++) {
      const stepId = `step-${i + 1}`;
      
      stepProgress.startStep(stepId);
      
      try {
        const result = await stepFunctions[i]();
        results.push(result);
        stepProgress.completeStep(stepId);
      } catch (error) {
        stepProgress.failStep(stepId, error instanceof Error ? error.message : 'Unknown error');
        throw error;
      }
    }
    
    stepProgress.complete();
    return results;
  } catch (error) {
    stepProgress.fail(error instanceof Error ? error.message : 'Process failed');
    throw error;
  }
}