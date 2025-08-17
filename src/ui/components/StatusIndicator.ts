import { colors } from '../utils/Colors.js';
import { symbols } from '../utils/Symbols.js';
import { Layout } from '../utils/Layout.js';

export enum StatusType {
  SUCCESS = 'success',
  ERROR = 'error',
  WARNING = 'warning',
  INFO = 'info',
  LOADING = 'loading',
  QUESTION = 'question'
}

export interface StatusOptions {
  prefix?: string;
  indent?: number;
  timestamp?: boolean;
  details?: string;
  showIcon?: boolean;
}

export class StatusIndicator {
  // Display success message
  static success(message: string, options: StatusOptions = {}): void {
    this.display(StatusType.SUCCESS, message, options);
  }

  // Display error message
  static error(message: string, options: StatusOptions = {}): void {
    this.display(StatusType.ERROR, message, options);
  }

  // Display warning message
  static warning(message: string, options: StatusOptions = {}): void {
    this.display(StatusType.WARNING, message, options);
  }

  // Display info message
  static info(message: string, options: StatusOptions = {}): void {
    this.display(StatusType.INFO, message, options);
  }

  // Display loading message
  static loading(message: string, options: StatusOptions = {}): void {
    this.display(StatusType.LOADING, message, options);
  }

  // Display question message
  static question(message: string, options: StatusOptions = {}): void {
    this.display(StatusType.QUESTION, message, options);
  }

  // Generic display method
  private static display(type: StatusType, message: string, options: StatusOptions = {}): void {
    const opts = {
      showIcon: true,
      indent: 0,
      timestamp: false,
      ...options
    };

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

    // Add icon and colored message based on type
    if (opts.showIcon) {
      const icon = this.getIcon(type);
      const coloredIcon = this.colorizeIcon(icon, type);
      output += `${coloredIcon} `;
    }

    const coloredMessage = this.colorizeMessage(message, type);
    output += coloredMessage;

    // Add details if provided
    if (opts.details) {
      output += '\n' + Layout.indent(colors.muted(opts.details), opts.indent ? opts.indent + 1 : 1);
    }

    console.log(output);
  }

  // Get icon for status type
  private static getIcon(type: StatusType): string {
    switch (type) {
      case StatusType.SUCCESS:
        return symbols.success;
      case StatusType.ERROR:
        return symbols.error;
      case StatusType.WARNING:
        return symbols.warning;
      case StatusType.INFO:
        return symbols.info;
      case StatusType.LOADING:
        return symbols.loading[0]; // Use first frame for static display
      case StatusType.QUESTION:
        return symbols.question;
      default:
        return symbols.bullet;
    }
  }

  // Colorize icon based on status type
  private static colorizeIcon(icon: string, type: StatusType): string {
    switch (type) {
      case StatusType.SUCCESS:
        return colors.success(icon);
      case StatusType.ERROR:
        return colors.error(icon);
      case StatusType.WARNING:
        return colors.warning(icon);
      case StatusType.INFO:
        return colors.info(icon);
      case StatusType.LOADING:
        return colors.primary(icon);
      case StatusType.QUESTION:
        return colors.accent(icon);
      default:
        return colors.muted(icon);
    }
  }

  // Colorize message based on status type
  private static colorizeMessage(message: string, type: StatusType): string {
    switch (type) {
      case StatusType.SUCCESS:
        return colors.success(message);
      case StatusType.ERROR:
        return colors.error(message);
      case StatusType.WARNING:
        return colors.warning(message);
      case StatusType.INFO:
        return colors.info(message);
      case StatusType.LOADING:
        return colors.primary(message);
      case StatusType.QUESTION:
        return colors.accent(message);
      default:
        return message;
    }
  }

  // Display a step in a process
  static step(stepNumber: number, totalSteps: number, message: string, status: StatusType = StatusType.INFO): void {
    const stepIndicator = colors.muted(`[${stepNumber}/${totalSteps}]`);
    const icon = this.getIcon(status);
    const coloredIcon = this.colorizeIcon(icon, status);
    const coloredMessage = this.colorizeMessage(message, status);
    
    console.log(`${stepIndicator} ${coloredIcon} ${coloredMessage}`);
  }

  // Display a list of status items
  static list(items: Array<{ message: string; status: StatusType; details?: string }>): void {
    items.forEach(item => {
      const options: StatusOptions = {};
      if (item.details) options.details = item.details;
      this.display(item.status, item.message, options);
    });
  }

  // Display a summary box with multiple status items
  static summary(title: string, items: Array<{ label: string; status: StatusType; value?: string }>): void {
    let content = colors.bold(title) + '\n\n';
    
    items.forEach(item => {
      const icon = this.colorizeIcon(this.getIcon(item.status), item.status);
      const value = item.value ? colors.muted(` (${item.value})`) : '';
      content += `${icon} ${item.label}${value}\n`;
    });

    const box = Layout.box(content.trim(), undefined, { padding: 2 });
    console.log(box);
  }

  // Display progress with status
  static progress(current: number, total: number, message: string, status: StatusType = StatusType.LOADING): void {
    const percentage = Math.round((current / total) * 100);
    const progressBar = Layout.progressBar(current, total, 30, { showPercentage: true });
    const icon = this.colorizeIcon(this.getIcon(status), status);
    const coloredMessage = this.colorizeMessage(message, status);
    
    console.log(`${icon} ${coloredMessage}`);
    console.log(`   ${colors.muted(progressBar)}`);
  }

  // Clear the current line (useful for updating status)
  static clearLine(): void {
    process.stdout.write('\r\x1b[K');
  }

  // Update status on the same line
  static updateLine(type: StatusType, message: string): void {
    this.clearLine();
    const icon = this.colorizeIcon(this.getIcon(type), type);
    const coloredMessage = this.colorizeMessage(message, type);
    process.stdout.write(`${icon} ${coloredMessage}`);
  }

  // Display a divider between status sections
  static divider(label?: string): void {
    console.log(colors.muted(Layout.separator('─', undefined, label)));
  }

  // Display multiple columns of status information
  static columns(columns: Array<{ title: string; items: Array<{ message: string; status: StatusType }> }>): void {
    const termWidth = Layout.getTerminalWidth();
    const columnWidth = Math.floor(termWidth / columns.length) - 2;
    
    // Display column headers
    const headers = columns.map(col => 
      Layout.pad(colors.bold(col.title), columnWidth, ' ', 'center')
    ).join('  ');
    console.log(headers);
    console.log(colors.muted('─'.repeat(termWidth)));
    
    // Find the maximum number of items in any column
    const maxItems = Math.max(...columns.map(col => col.items.length));
    
    // Display items row by row
    for (let i = 0; i < maxItems; i++) {
      const row = columns.map(col => {
        const item = col.items[i];
        if (item) {
          const icon = this.colorizeIcon(this.getIcon(item.status), item.status);
          const message = Layout.truncate(item.message, columnWidth - 3);
          return Layout.pad(`${icon} ${message}`, columnWidth);
        } else {
          return ' '.repeat(columnWidth);
        }
      }).join('  ');
      console.log(row);
    }
  }
}