import { colors } from '../utils/Colors.js';
import { symbols } from '../utils/Symbols.js';
import { Layout } from '../utils/Layout.js';
import { 
  withCache, 
  withPerformanceTracking, 
  formattingOptimizer,
  StreamingOutput 
} from '../utils/Performance.js';

export enum OptimizedStatusType {
  SUCCESS = 'success',
  ERROR = 'error',
  WARNING = 'warning',
  INFO = 'info',
  LOADING = 'loading',
  QUESTION = 'question'
}

export interface OptimizedStatusOptions {
  prefix?: string;
  indent?: number;
  timestamp?: boolean;
  details?: string;
  showIcon?: boolean;
  useCache?: boolean;
}

export class OptimizedStatusIndicator {
  private static iconCache = new Map<OptimizedStatusType, string>();
  private static colorFunctionCache = new Map<OptimizedStatusType, (text: string) => string>();

  // Initialize caches
  static {
    // Pre-populate icon cache
    this.iconCache.set(OptimizedStatusType.SUCCESS, symbols.success);
    this.iconCache.set(OptimizedStatusType.ERROR, symbols.error);
    this.iconCache.set(OptimizedStatusType.WARNING, symbols.warning);
    this.iconCache.set(OptimizedStatusType.INFO, symbols.info);
    this.iconCache.set(OptimizedStatusType.LOADING, symbols.loading[0]);
    this.iconCache.set(OptimizedStatusType.QUESTION, symbols.question);

    // Pre-populate color function cache
    this.colorFunctionCache.set(OptimizedStatusType.SUCCESS, colors.success);
    this.colorFunctionCache.set(OptimizedStatusType.ERROR, colors.error);
    this.colorFunctionCache.set(OptimizedStatusType.WARNING, colors.warning);
    this.colorFunctionCache.set(OptimizedStatusType.INFO, colors.info);
    this.colorFunctionCache.set(OptimizedStatusType.LOADING, colors.primary);
    this.colorFunctionCache.set(OptimizedStatusType.QUESTION, colors.accent);
  }

  // Optimized display methods
  static success(message: string, options: OptimizedStatusOptions = {}): void {
    this.display(OptimizedStatusType.SUCCESS, message, options);
  }

  static error(message: string, options: OptimizedStatusOptions = {}): void {
    this.display(OptimizedStatusType.ERROR, message, options);
  }

  static warning(message: string, options: OptimizedStatusOptions = {}): void {
    this.display(OptimizedStatusType.WARNING, message, options);
  }

  static info(message: string, options: OptimizedStatusOptions = {}): void {
    this.display(OptimizedStatusType.INFO, message, options);
  }

  static loading(message: string, options: OptimizedStatusOptions = {}): void {
    this.display(OptimizedStatusType.LOADING, message, options);
  }

  static question(message: string, options: OptimizedStatusOptions = {}): void {
    this.display(OptimizedStatusType.QUESTION, message, options);
  }

  // Optimized generic display method with caching
  private static display(type: OptimizedStatusType, message: string, options: OptimizedStatusOptions = {}): void {
    withPerformanceTracking('status-display', () => {
      const opts = {
        showIcon: true,
        indent: 0,
        timestamp: false,
        useCache: true,
        ...options
      };

      // Generate cache key
      const cacheKey = opts.useCache ? 
        `status-${type}-${message}-${JSON.stringify(opts)}` : 
        null;

      if (cacheKey) {
        const cached = withCache(cacheKey, () => null);
        if (cached) {
          console.log(cached);
          return;
        }
      }

      let output = '';

      // Add indentation
      if (opts.indent && opts.indent > 0) {
        output += ' '.repeat(opts.indent);
      }

      // Add prefix if provided
      if (opts.prefix) {
        output += colors.muted(`[${opts.prefix}] `);
      }

      // Add timestamp if requested
      if (opts.timestamp) {
        const timestamp = new Date().toLocaleTimeString();
        output += colors.muted(`[${timestamp}] `);
      }

      // Batch color operations for better performance
      const colorOperations: Array<{ text: string; colorFn: (text: string) => string }> = [];

      // Add icon and colored message based on type
      if (opts.showIcon) {
        const icon = this.getIcon(type);
        const iconColorFn = this.getColorFunction(type);
        colorOperations.push({ text: icon, colorFn: iconColorFn });
      }

      const messageColorFn = this.getMessageColorFunction(type);
      colorOperations.push({ text: message, colorFn: messageColorFn });

      // Apply colors in batch
      const coloredElements = formattingOptimizer.batchColorOperations(colorOperations);

      if (opts.showIcon) {
        output += `${coloredElements[0]} ${coloredElements[1]}`;
      } else {
        output += coloredElements[0];
      }

      // Add details if provided
      if (opts.details) {
        output += '\n' + Layout.indent(colors.muted(opts.details), opts.indent ? opts.indent + 1 : 1);
      }

      // Cache the result
      if (cacheKey) {
        withCache(cacheKey, () => output);
      }

      console.log(output);
    });
  }

  // Cached icon retrieval
  private static getIcon(type: OptimizedStatusType): string {
    return this.iconCache.get(type) || symbols.bullet;
  }

  // Cached color function retrieval
  private static getColorFunction(type: OptimizedStatusType): (text: string) => string {
    return this.colorFunctionCache.get(type) || colors.muted;
  }

  // Cached message color function retrieval
  private static getMessageColorFunction(type: OptimizedStatusType): (text: string) => string {
    return this.colorFunctionCache.get(type) || ((text: string) => text);
  }

  // Optimized step display
  static step(stepNumber: number, totalSteps: number, message: string, status: OptimizedStatusType = OptimizedStatusType.INFO): void {
    withPerformanceTracking('status-step', () => {
      const cacheKey = `step-${stepNumber}-${totalSteps}-${message}-${status}`;
      
      const output = withCache(cacheKey, () => {
        const stepIndicator = colors.muted(`[${stepNumber}/${totalSteps}]`);
        const icon = this.getIcon(status);
        const iconColorFn = this.getColorFunction(status);
        const messageColorFn = this.getMessageColorFunction(status);
        
        // Batch color operations
        const colorOperations = [
          { text: icon, colorFn: iconColorFn },
          { text: message, colorFn: messageColorFn }
        ];
        
        const [coloredIcon, coloredMessage] = formattingOptimizer.batchColorOperations(colorOperations);
        
        return `${stepIndicator} ${coloredIcon} ${coloredMessage}`;
      });
      
      console.log(output);
    });
  }

  // Optimized list display
  static list(items: Array<{ message: string; status: OptimizedStatusType; details?: string }>): void {
    withPerformanceTracking('status-list', () => {
      // Batch all color operations for the entire list
      const allColorOperations: Array<{ text: string; colorFn: (text: string) => string }> = [];
      
      items.forEach(item => {
        const iconColorFn = this.getColorFunction(item.status);
        const messageColorFn = this.getMessageColorFunction(item.status);
        
        allColorOperations.push(
          { text: this.getIcon(item.status), colorFn: iconColorFn },
          { text: item.message, colorFn: messageColorFn }
        );
      });
      
      const coloredElements = formattingOptimizer.batchColorOperations(allColorOperations);
      
      // Display items using pre-colored elements
      items.forEach((item, index) => {
        const iconIndex = index * 2;
        const messageIndex = index * 2 + 1;
        
        let output = `${coloredElements[iconIndex]} ${coloredElements[messageIndex]}`;
        
        if (item.details) {
          output += '\n' + Layout.indent(colors.muted(item.details), 1);
        }
        
        console.log(output);
      });
    });
  }

  // Optimized summary display
  static summary(title: string, items: Array<{ label: string; status: OptimizedStatusType; value?: string }>): void {
    withPerformanceTracking('status-summary', () => {
      const cacheKey = `summary-${title}-${JSON.stringify(items)}`;
      
      const content = withCache(cacheKey, () => {
        let result = colors.bold(title) + '\n\n';
        
        // Batch color operations for all items
        const colorOperations: Array<{ text: string; colorFn: (text: string) => string }> = [];
        
        items.forEach(item => {
          const iconColorFn = this.getColorFunction(item.status);
          colorOperations.push({ text: this.getIcon(item.status), colorFn: iconColorFn });
        });
        
        const coloredIcons = formattingOptimizer.batchColorOperations(colorOperations);
        
        items.forEach((item, index) => {
          const value = item.value ? colors.muted(` (${item.value})`) : '';
          result += `${coloredIcons[index]} ${item.label}${value}\n`;
        });

        return result.trim();
      });

      const box = Layout.box(content, undefined, { padding: 2 });
      console.log(box);
    });
  }

  // Optimized progress display
  static progress(current: number, total: number, message: string, status: OptimizedStatusType = OptimizedStatusType.LOADING): void {
    withPerformanceTracking('status-progress', () => {
      const percentage = Math.round((current / total) * 100);
      const progressBar = Layout.progressBar(current, total, 30, { showPercentage: true });
      
      const colorOperations = [
        { text: this.getIcon(status), colorFn: this.getColorFunction(status) },
        { text: message, colorFn: this.getMessageColorFunction(status) }
      ];
      
      const [coloredIcon, coloredMessage] = formattingOptimizer.batchColorOperations(colorOperations);
      
      console.log(`${coloredIcon} ${coloredMessage}`);
      console.log(`   ${colors.muted(progressBar)}`);
    });
  }

  // Optimized line operations
  static clearLine(): void {
    process.stdout.write('\r\x1b[K');
  }

  static updateLine(type: OptimizedStatusType, message: string): void {
    withPerformanceTracking('status-update-line', () => {
      this.clearLine();
      
      const colorOperations = [
        { text: this.getIcon(type), colorFn: this.getColorFunction(type) },
        { text: message, colorFn: this.getMessageColorFunction(type) }
      ];
      
      const [coloredIcon, coloredMessage] = formattingOptimizer.batchColorOperations(colorOperations);
      process.stdout.write(`${coloredIcon} ${coloredMessage}`);
    });
  }

  // Optimized divider
  static divider(label?: string): void {
    withPerformanceTracking('status-divider', () => {
      const cacheKey = `divider-${label || 'default'}`;
      
      const divider = withCache(cacheKey, () => {
        return colors.muted(Layout.separator('─', undefined, label));
      });
      
      console.log(divider);
    });
  }

  // Optimized columns display
  static columns(columns: Array<{ title: string; items: Array<{ message: string; status: OptimizedStatusType }> }>): void {
    withPerformanceTracking('status-columns', () => {
      const termWidth = Layout.getTerminalWidth();
      const columnWidth = Math.floor(termWidth / columns.length) - 2;
      
      // Batch all color operations
      const allColorOperations: Array<{ text: string; colorFn: (text: string) => string }> = [];
      
      // Add title operations
      columns.forEach(col => {
        allColorOperations.push({ text: col.title, colorFn: colors.bold });
      });
      
      // Add item operations
      columns.forEach(col => {
        col.items.forEach(item => {
          allColorOperations.push(
            { text: this.getIcon(item.status), colorFn: this.getColorFunction(item.status) },
            { text: item.message, colorFn: this.getMessageColorFunction(item.status) }
          );
        });
      });
      
      const coloredElements = formattingOptimizer.batchColorOperations(allColorOperations);
      
      // Display column headers
      let elementIndex = 0;
      const headers = columns.map(() => {
        const title = coloredElements[elementIndex++];
        return Layout.pad(title, columnWidth, ' ', 'center');
      }).join('  ');
      
      console.log(headers);
      console.log(colors.muted('─'.repeat(termWidth)));
      
      // Find the maximum number of items in any column
      const maxItems = Math.max(...columns.map(col => col.items.length));
      
      // Display items row by row
      for (let i = 0; i < maxItems; i++) {
        const row = columns.map(col => {
          const item = col.items[i];
          if (item) {
            const icon = coloredElements[elementIndex++];
            const message = coloredElements[elementIndex++];
            const truncatedMessage = Layout.truncate(message, columnWidth - 3);
            return Layout.pad(`${icon} ${truncatedMessage}`, columnWidth);
          } else {
            return ' '.repeat(columnWidth);
          }
        }).join('  ');
        console.log(row);
      }
    });
  }

  // Batch status operations for better performance
  static batch(operations: Array<{
    type: OptimizedStatusType;
    message: string;
    options?: OptimizedStatusOptions;
  }>): void {
    withPerformanceTracking('status-batch', () => {
      // Use streaming for large batches
      if (operations.length > 50) {
        const streamOutput = new StreamingOutput();
        
        operations.forEach(op => {
          const opts = { useCache: true, ...op.options };
          const cacheKey = `batch-${op.type}-${op.message}-${JSON.stringify(opts)}`;
          
          const output = withCache(cacheKey, () => {
            let result = '';
            
            if (opts.indent && opts.indent > 0) {
              result += ' '.repeat(opts.indent);
            }
            
            if (opts.prefix) {
              result += colors.muted(`[${opts.prefix}] `);
            }
            
            if (opts.timestamp) {
              const timestamp = new Date().toLocaleTimeString();
              result += colors.muted(`[${timestamp}] `);
            }
            
            if (opts.showIcon !== false) {
              const icon = this.getIcon(op.type);
              const iconColorFn = this.getColorFunction(op.type);
              result += `${iconColorFn(icon)} `;
            }
            
            const messageColorFn = this.getMessageColorFunction(op.type);
            result += messageColorFn(op.message);
            
            if (opts.details) {
              result += '\n' + Layout.indent(colors.muted(opts.details), opts.indent ? opts.indent + 1 : 1);
            }
            
            return result;
          });
          
          streamOutput.writeLine(output);
        });
        
        streamOutput.end();
      } else {
        // For smaller batches, use regular display
        operations.forEach(op => {
          this.display(op.type, op.message, op.options);
        });
      }
    });
  }

  // Performance monitoring for status operations
  static getPerformanceStats(): any {
    // This would integrate with the performance monitor
    // to provide statistics about status indicator performance
    return {
      cacheHitRate: 'N/A', // Would be calculated from cache statistics
      averageRenderTime: 'N/A', // Would be calculated from performance monitor
      totalOperations: 'N/A' // Would be tracked
    };
  }
}