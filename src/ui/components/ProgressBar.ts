import { colors } from '../utils/Colors.js';
import { symbols, SpinnerAnimation } from '../utils/Symbols.js';
import { Layout } from '../utils/Layout.js';

export interface ProgressOptions {
  total?: number;
  current?: number;
  message?: string;
  showPercentage?: boolean;
  showNumbers?: boolean;
  showEta?: boolean;
  width?: number;
  style?: 'bar' | 'dots' | 'blocks';
}

export class ProgressBar {
  private current: number = 0;
  private total: number = 100;
  private message: string = '';
  private startTime: number = Date.now();
  private options: Required<ProgressOptions>;

  constructor(options: ProgressOptions = {}) {
    this.options = {
      total: 100,
      current: 0,
      message: '',
      showPercentage: true,
      showNumbers: false,
      showEta: false,
      width: 40,
      style: 'bar',
      ...options
    };

    this.total = this.options.total;
    this.current = this.options.current;
    this.message = this.options.message;
  }

  // Update progress
  update(current: number, message?: string): void {
    this.current = Math.min(current, this.total);
    if (message) this.message = message;
    this.render();
  }

  // Increment progress
  increment(amount: number = 1, message?: string): void {
    this.update(this.current + amount, message);
  }

  // Complete the progress bar
  complete(message?: string): void {
    this.current = this.total;
    if (message) this.message = message;
    this.render();
    console.log(); // New line after completion
  }

  // Fail the progress bar
  fail(message?: string): void {
    if (message) this.message = message;
    this.renderFailed();
    console.log(); // New line after failure
  }

  // Render the progress bar
  private render(): void {
    const percentage = Math.min(100, Math.max(0, (this.current / this.total) * 100));
    let output = '';

    // Clear the current line
    process.stdout.write('\r\x1b[K');

    // Add message if provided
    if (this.message) {
      output += colors.info(this.message) + ' ';
    }

    // Create the progress bar based on style
    const bar = this.createProgressBar(percentage);
    output += bar;

    // Add percentage if requested
    if (this.options.showPercentage) {
      const percentText = `${Math.round(percentage)}%`;
      output += ` ${colors.muted(percentText)}`;
    }

    // Add numbers if requested
    if (this.options.showNumbers) {
      const numbersText = `(${this.current}/${this.total})`;
      output += ` ${colors.muted(numbersText)}`;
    }

    // Add ETA if requested
    if (this.options.showEta && this.current > 0) {
      const eta = this.calculateEta();
      if (eta) {
        output += ` ${colors.muted(`ETA: ${eta}`)}`;
      }
    }

    process.stdout.write(output);
  }

  // Render failed state
  private renderFailed(): void {
    process.stdout.write('\r\x1b[K');
    
    let output = '';
    if (this.message) {
      output += colors.error(this.message) + ' ';
    }
    
    const failedBar = colors.error('█'.repeat(Math.floor(this.options.width / 2))) + 
                     colors.muted('░'.repeat(Math.ceil(this.options.width / 2)));
    output += `[${failedBar}] ${colors.error('FAILED')}`;
    
    process.stdout.write(output);
  }

  // Create progress bar based on style
  private createProgressBar(percentage: number): string {
    const width = this.options.width;
    const filled = Math.floor((percentage / 100) * width);
    const empty = width - filled;

    switch (this.options.style) {
      case 'dots':
        return this.createDotsBar(filled, empty);
      case 'blocks':
        return this.createBlocksBar(filled, empty);
      case 'bar':
      default:
        return this.createStandardBar(filled, empty);
    }
  }

  // Create standard progress bar
  private createStandardBar(filled: number, empty: number): string {
    const filledBar = colors.success(symbols.progressFull.repeat(filled));
    const emptyBar = colors.muted(symbols.progressEmpty.repeat(empty));
    return `[${filledBar}${emptyBar}]`;
  }

  // Create dots-style progress bar
  private createDotsBar(filled: number, empty: number): string {
    const filledDots = colors.success('●'.repeat(filled));
    const emptyDots = colors.muted('○'.repeat(empty));
    return `${filledDots}${emptyDots}`;
  }

  // Create blocks-style progress bar
  private createBlocksBar(filled: number, empty: number): string {
    const filledBlocks = colors.success('▓'.repeat(filled));
    const emptyBlocks = colors.muted('░'.repeat(empty));
    return `${filledBlocks}${emptyBlocks}`;
  }

  // Calculate estimated time of arrival
  private calculateEta(): string | null {
    const elapsed = Date.now() - this.startTime;
    const rate = this.current / elapsed;
    const remaining = this.total - this.current;
    
    if (rate <= 0 || remaining <= 0) return null;
    
    const etaMs = remaining / rate;
    const etaSeconds = Math.round(etaMs / 1000);
    
    if (etaSeconds < 60) {
      return `${etaSeconds}s`;
    } else if (etaSeconds < 3600) {
      const minutes = Math.floor(etaSeconds / 60);
      const seconds = etaSeconds % 60;
      return `${minutes}m ${seconds}s`;
    } else {
      const hours = Math.floor(etaSeconds / 3600);
      const minutes = Math.floor((etaSeconds % 3600) / 60);
      return `${hours}h ${minutes}m`;
    }
  }

  // Static method to create a simple progress bar
  static simple(current: number, total: number, message?: string): void {
    const options: ProgressOptions = { total };
    if (message) options.message = message;
    const bar = new ProgressBar(options);
    bar.update(current);
  }

  // Static method to create and complete a progress bar
  static complete(message: string): void {
    const bar = new ProgressBar({ total: 1, message });
    bar.complete();
  }

  // Static method to create and fail a progress bar
  static fail(message: string): void {
    const bar = new ProgressBar({ total: 1, message });
    bar.fail();
  }
}

// Spinner class for indeterminate progress
export class Spinner {
  private animation: SpinnerAnimation;
  private message: string;
  private interval: NodeJS.Timeout | null = null;
  private isSpinning: boolean = false;

  constructor(message: string = '', frames?: string[]) {
    this.message = message;
    this.animation = new SpinnerAnimation(frames);
  }

  // Start the spinner
  start(): void {
    if (this.isSpinning) return;
    
    this.isSpinning = true;
    this.render();
    
    this.interval = setInterval(() => {
      this.render();
    }, 100);
  }

  // Update the spinner message
  update(message: string): void {
    this.message = message;
    if (this.isSpinning) {
      this.render();
    }
  }

  // Stop the spinner with success
  succeed(message?: string): void {
    this.stop();
    const finalMessage = message || this.message;
    console.log(`${colors.success(symbols.success)} ${colors.success(finalMessage)}`);
  }

  // Stop the spinner with failure
  fail(message?: string): void {
    this.stop();
    const finalMessage = message || this.message;
    console.log(`${colors.error(symbols.error)} ${colors.error(finalMessage)}`);
  }

  // Stop the spinner with warning
  warn(message?: string): void {
    this.stop();
    const finalMessage = message || this.message;
    console.log(`${colors.warning(symbols.warning)} ${colors.warning(finalMessage)}`);
  }

  // Stop the spinner with info
  info(message?: string): void {
    this.stop();
    const finalMessage = message || this.message;
    console.log(`${colors.info(symbols.info)} ${colors.info(finalMessage)}`);
  }

  // Stop the spinner
  stop(): void {
    if (!this.isSpinning) return;
    
    this.isSpinning = false;
    if (this.interval) {
      clearInterval(this.interval);
      this.interval = null;
    }
    
    // Clear the current line
    process.stdout.write('\r\x1b[K');
  }

  // Render the spinner
  private render(): void {
    const frame = this.animation.next();
    const spinner = colors.primary(frame);
    const message = this.message ? ` ${colors.info(this.message)}` : '';
    
    process.stdout.write(`\r${spinner}${message}`);
  }

  // Static method to create a simple spinner
  static create(message: string): Spinner {
    return new Spinner(message);
  }

  // Static method for a quick spinning operation
  static async spin<T>(message: string, operation: () => Promise<T>): Promise<T> {
    const spinner = new Spinner(message);
    spinner.start();
    
    try {
      const result = await operation();
      spinner.succeed();
      return result;
    } catch (error) {
      spinner.fail();
      throw error;
    }
  }
}

// Multi-step progress tracker
export class MultiStepProgress {
  private steps: Array<{ name: string; completed: boolean; current?: boolean }> = [];
  private currentStepIndex: number = 0;

  constructor(steps: string[]) {
    this.steps = steps.map((name, index) => ({
      name,
      completed: false,
      current: index === 0
    }));
  }

  // Start the next step
  nextStep(message?: string): void {
    if (this.currentStepIndex < this.steps.length) {
      this.steps[this.currentStepIndex].completed = true;
      this.steps[this.currentStepIndex].current = false;
    }
    
    this.currentStepIndex++;
    
    if (this.currentStepIndex < this.steps.length) {
      this.steps[this.currentStepIndex].current = true;
    }
    
    this.render(message);
  }

  // Complete the current step
  completeStep(message?: string): void {
    if (this.currentStepIndex < this.steps.length) {
      this.steps[this.currentStepIndex].completed = true;
      this.steps[this.currentStepIndex].current = false;
    }
    
    this.render(message);
  }

  // Complete all steps
  complete(message?: string): void {
    this.steps.forEach(step => {
      step.completed = true;
      step.current = false;
    });
    
    this.render(message);
  }

  // Render the multi-step progress
  private render(message?: string): void {
    console.log(); // New line
    
    if (message) {
      console.log(colors.info(message));
    }
    
    this.steps.forEach((step, index) => {
      let icon: string;
      let color: (text: string) => string;
      
      if (step.completed) {
        icon = symbols.success;
        color = colors.success;
      } else if (step.current) {
        icon = symbols.loading[0];
        color = colors.primary;
      } else {
        icon = symbols.bullet;
        color = colors.muted;
      }
      
      const stepNumber = colors.muted(`${index + 1}.`);
      console.log(`  ${stepNumber} ${color(icon)} ${color(step.name)}`);
    });
  }
}