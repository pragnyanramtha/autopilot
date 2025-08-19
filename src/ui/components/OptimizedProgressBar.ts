import { colors } from '../utils/Colors.js';
import { symbols, SpinnerAnimation } from '../utils/Symbols.js';
import { Layout } from '../utils/Layout.js';
import { 
  withCache, 
  withPerformanceTracking, 
  StreamingOutput,
  formattingOptimizer 
} from '../utils/Performance.js';

export interface OptimizedProgressOptions {
  total?: number;
  current?: number;
  message?: string;
  showPercentage?: boolean;
  showNumbers?: boolean;
  showEta?: boolean;
  width?: number;
  style?: 'bar' | 'dots' | 'blocks';
  useCache?: boolean;
  throttleMs?: number; // Throttle updates to improve performance
}

export class OptimizedProgressBar {
  private current: number = 0;
  private total: number = 100;
  private message: string = '';
  private startTime: number = Date.now();
  private options: Required<OptimizedProgressOptions>;
  private lastRenderTime: number = 0;
  private lastRenderedOutput: string = '';

  constructor(options: OptimizedProgressOptions = {}) {
    this.options = {
      total: 100,
      current: 0,
      message: '',
      showPercentage: true,
      showNumbers: false,
      showEta: false,
      width: 40,
      style: 'bar',
      useCache: true,
      throttleMs: 16, // ~60fps
      ...options
    };

    this.total = this.options.total;
    this.current = this.options.current;
    this.message = this.options.message;
  }

  // Optimized update with throttling
  update(current: number, message?: string): void {
    withPerformanceTracking('progress-update', () => {
      this.current = Math.min(current, this.total);
      if (message) this.message = message;
      
      // Throttle updates for better performance
      const now = Date.now();
      if (now - this.lastRenderTime < this.options.throttleMs) {
        return;
      }
      
      this.render();
      this.lastRenderTime = now;
    });
  }

  // Increment progress
  increment(amount: number = 1, message?: string): void {
    this.update(this.current + amount, message);
  }

  // Complete the progress bar
  complete(message?: string): void {
    withPerformanceTracking('progress-complete', () => {
      this.current = this.total;
      if (message) this.message = message;
      this.render();
      console.log(); // New line after completion
    });
  }

  // Fail the progress bar
  fail(message?: string): void {
    withPerformanceTracking('progress-fail', () => {
      if (message) this.message = message;
      this.renderFailed();
      console.log(); // New line after failure
    });
  }

  // Optimized render with caching
  private render(): void {
    const percentage = Math.min(100, Math.max(0, (this.current / this.total) * 100));
    
    // Generate cache key for this state
    const cacheKey = this.options.useCache ? 
      `progress-${this.current}-${this.total}-${this.message}-${JSON.stringify(this.options)}` : 
      null;
    
    let output = '';
    
    if (cacheKey) {
      const cached = withCache(cacheKey, () => null);
      if (cached && cached === this.lastRenderedOutput) {
        return; // Skip rendering if output hasn't changed
      }
    }

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

    // Cache the output if caching is enabled
    if (cacheKey) {
      withCache(cacheKey, () => output);
    }
    
    this.lastRenderedOutput = output;
    process.stdout.write(output);
  }

  // Optimized failed state rendering
  private renderFailed(): void {
    withPerformanceTracking('progress-render-failed', () => {
      process.stdout.write('\r\x1b[K');
      
      let output = '';
      if (this.message) {
        output += colors.error(this.message) + ' ';
      }
      
      const failedBar = colors.error('█'.repeat(Math.floor(this.options.width / 2))) + 
                       colors.muted('░'.repeat(Math.ceil(this.options.width / 2)));
      output += `[${failedBar}] ${colors.error('FAILED')}`;
      
      process.stdout.write(output);
    });
  }

  // Optimized progress bar creation with caching
  private createProgressBar(percentage: number): string {
    const cacheKey = this.options.useCache ? 
      `progress-bar-${percentage}-${this.options.width}-${this.options.style}` : 
      null;
    
    if (cacheKey) {
      const cached = withCache(cacheKey, () => null);
      if (cached) return cached;
    }

    const width = this.options.width;
    const filled = Math.floor((percentage / 100) * width);
    const empty = width - filled;

    let result: string;
    switch (this.options.style) {
      case 'dots':
        result = this.createDotsBar(filled, empty);
        break;
      case 'blocks':
        result = this.createBlocksBar(filled, empty);
        break;
      case 'bar':
      default:
        result = this.createStandardBar(filled, empty);
        break;
    }

    if (cacheKey) {
      withCache(cacheKey, () => result);
    }

    return result;
  }

  // Optimized bar creation methods
  private createStandardBar(filled: number, empty: number): string {
    // Batch color operations for better performance
    const operations = [
      { text: symbols.progressFull.repeat(filled), colorFn: colors.success },
      { text: symbols.progressEmpty.repeat(empty), colorFn: colors.muted }
    ];
    
    const [filledBar, emptyBar] = formattingOptimizer.batchColorOperations(operations);
    return `[${filledBar}${emptyBar}]`;
  }

  private createDotsBar(filled: number, empty: number): string {
    const operations = [
      { text: '●'.repeat(filled), colorFn: colors.success },
      { text: '○'.repeat(empty), colorFn: colors.muted }
    ];
    
    const [filledDots, emptyDots] = formattingOptimizer.batchColorOperations(operations);
    return `${filledDots}${emptyDots}`;
  }

  private createBlocksBar(filled: number, empty: number): string {
    const operations = [
      { text: '▓'.repeat(filled), colorFn: colors.success },
      { text: '░'.repeat(empty), colorFn: colors.muted }
    ];
    
    const [filledBlocks, emptyBlocks] = formattingOptimizer.batchColorOperations(operations);
    return `${filledBlocks}${emptyBlocks}`;
  }

  // Cached ETA calculation
  private calculateEta(): string | null {
    const elapsed = Date.now() - this.startTime;
    const rate = this.current / elapsed;
    const remaining = this.total - this.current;
    
    if (rate <= 0 || remaining <= 0) return null;
    
    const etaMs = remaining / rate;
    const etaSeconds = Math.round(etaMs / 1000);
    
    // Cache ETA formatting
    const cacheKey = `eta-${etaSeconds}`;
    return withCache(cacheKey, () => {
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
    });
  }

  // Static optimized methods
  static simple(current: number, total: number, message?: string): void {
    withPerformanceTracking('progress-simple', () => {
      const options: OptimizedProgressOptions = { total, useCache: true };
      if (message) options.message = message;
      const bar = new OptimizedProgressBar(options);
      bar.update(current);
    });
  }

  static complete(message: string): void {
    withPerformanceTracking('progress-static-complete', () => {
      const bar = new OptimizedProgressBar({ total: 1, message, useCache: true });
      bar.complete();
    });
  }

  static fail(message: string): void {
    withPerformanceTracking('progress-static-fail', () => {
      const bar = new OptimizedProgressBar({ total: 1, message, useCache: true });
      bar.fail();
    });
  }
}

// Optimized Spinner class
export class OptimizedSpinner {
  private animation: SpinnerAnimation;
  private message: string;
  private interval: NodeJS.Timeout | null = null;
  private isSpinning: boolean = false;
  private lastRenderTime: number = 0;
  private throttleMs: number = 100;

  constructor(message: string = '', frames?: string[], throttleMs: number = 100) {
    this.message = message;
    this.animation = new SpinnerAnimation(frames);
    this.throttleMs = throttleMs;
  }

  // Optimized start with throttling
  start(): void {
    if (this.isSpinning) return;
    
    withPerformanceTracking('spinner-start', () => {
      this.isSpinning = true;
      this.render();
      
      this.interval = setInterval(() => {
        const now = Date.now();
        if (now - this.lastRenderTime >= this.throttleMs) {
          this.render();
          this.lastRenderTime = now;
        }
      }, this.throttleMs);
    });
  }

  // Update spinner message
  update(message: string): void {
    this.message = message;
    if (this.isSpinning) {
      this.render();
    }
  }

  // Stop with success
  succeed(message?: string): void {
    withPerformanceTracking('spinner-succeed', () => {
      this.stop();
      const finalMessage = message || this.message;
      console.log(`${colors.success(symbols.success)} ${colors.success(finalMessage)}`);
    });
  }

  // Stop with failure
  fail(message?: string): void {
    withPerformanceTracking('spinner-fail', () => {
      this.stop();
      const finalMessage = message || this.message;
      console.log(`${colors.error(symbols.error)} ${colors.error(finalMessage)}`);
    });
  }

  // Stop with warning
  warn(message?: string): void {
    withPerformanceTracking('spinner-warn', () => {
      this.stop();
      const finalMessage = message || this.message;
      console.log(`${colors.warning(symbols.warning)} ${colors.warning(finalMessage)}`);
    });
  }

  // Stop with info
  info(message?: string): void {
    withPerformanceTracking('spinner-info', () => {
      this.stop();
      const finalMessage = message || this.message;
      console.log(`${colors.info(symbols.info)} ${colors.info(finalMessage)}`);
    });
  }

  // Stop spinner
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

  // Optimized render with caching
  private render(): void {
    const frame = this.animation.next();
    
    // Cache the spinner output
    const cacheKey = `spinner-${frame}-${this.message}`;
    const output = withCache(cacheKey, () => {
      const spinner = colors.primary(frame);
      const message = this.message ? ` ${colors.info(this.message)}` : '';
      return `\r${spinner}${message}`;
    });
    
    process.stdout.write(output);
  }

  // Static optimized methods
  static create(message: string, throttleMs: number = 100): OptimizedSpinner {
    return new OptimizedSpinner(message, undefined, throttleMs);
  }

  static async spin<T>(message: string, operation: () => Promise<T>): Promise<T> {
    return withPerformanceTracking('spinner-operation', async () => {
      const spinner = new OptimizedSpinner(message);
      spinner.start();
      
      try {
        const result = await operation();
        spinner.succeed();
        return result;
      } catch (error) {
        spinner.fail();
        throw error;
      }
    });
  }
}

// Optimized multi-step progress tracker
export class OptimizedMultiStepProgress {
  private steps: Array<{ name: string; completed: boolean; current?: boolean }> = [];
  private currentStepIndex: number = 0;
  private streamOutput: StreamingOutput | null = null;

  constructor(steps: string[], useStreaming: boolean = false) {
    this.steps = steps.map((name, index) => ({
      name,
      completed: false,
      current: index === 0
    }));
    
    if (useStreaming) {
      this.streamOutput = new StreamingOutput();
    }
  }

  // Optimized step progression
  nextStep(message?: string): void {
    withPerformanceTracking('multi-step-next', () => {
      if (this.currentStepIndex < this.steps.length) {
        this.steps[this.currentStepIndex].completed = true;
        this.steps[this.currentStepIndex].current = false;
      }
      
      this.currentStepIndex++;
      
      if (this.currentStepIndex < this.steps.length) {
        this.steps[this.currentStepIndex].current = true;
      }
      
      this.render(message);
    });
  }

  // Complete current step
  completeStep(message?: string): void {
    withPerformanceTracking('multi-step-complete', () => {
      if (this.currentStepIndex < this.steps.length) {
        this.steps[this.currentStepIndex].completed = true;
        this.steps[this.currentStepIndex].current = false;
      }
      
      this.render(message);
    });
  }

  // Complete all steps
  complete(message?: string): void {
    withPerformanceTracking('multi-step-complete-all', () => {
      this.steps.forEach(step => {
        step.completed = true;
        step.current = false;
      });
      
      this.render(message);
    });
  }

  // Optimized render with caching and optional streaming
  private render(message?: string): void {
    const cacheKey = `multi-step-${this.currentStepIndex}-${message || ''}`;
    
    const output = withCache(cacheKey, () => {
      let result = '\n'; // New line
      
      if (message) {
        result += colors.info(message) + '\n';
      }
      
      // Batch color operations for all steps
      const stepOperations: Array<{ text: string; colorFn: (text: string) => string }> = [];
      
      this.steps.forEach((step, index) => {
        let icon: string;
        let colorFn: (text: string) => string;
        
        if (step.completed) {
          icon = symbols.success;
          colorFn = colors.success;
        } else if (step.current) {
          icon = symbols.loading[0];
          colorFn = colors.primary;
        } else {
          icon = symbols.bullet;
          colorFn = colors.muted;
        }
        
        stepOperations.push({ text: icon, colorFn });
        stepOperations.push({ text: step.name, colorFn });
      });
      
      const coloredElements = formattingOptimizer.batchColorOperations(stepOperations);
      
      // Reconstruct the step display
      for (let i = 0; i < this.steps.length; i++) {
        const stepNumber = colors.muted(`${i + 1}.`);
        const icon = coloredElements[i * 2];
        const name = coloredElements[i * 2 + 1];
        result += `  ${stepNumber} ${icon} ${name}\n`;
      }
      
      return result;
    });

    if (this.streamOutput) {
      this.streamOutput.write(output);
      this.streamOutput.flush();
    } else {
      console.log(output);
    }
  }

  // Finish streaming if used
  finish(): void {
    if (this.streamOutput) {
      this.streamOutput.end();
    }
  }
}