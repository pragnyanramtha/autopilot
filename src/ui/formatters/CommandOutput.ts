import { colors } from '../utils/Colors.js';
import { symbols } from '../utils/Symbols.js';
import { Layout } from '../utils/Layout.js';

export interface CommandResult {
  command: string;
  output: string;
  error?: string;
  exitCode: number;
  duration?: number;
}

export interface FormatOptions {
  showCommand?: boolean;
  showDuration?: boolean;
  highlightSyntax?: boolean;
  maxWidth?: number;
}

export class CommandOutput {
  /**
   * Format command execution results with proper styling and structure
   */
  static format(result: CommandResult, options: FormatOptions = {}): string {
    const {
      showCommand = true,
      showDuration = true,
      highlightSyntax = true,
      maxWidth = 80
    } = options;

    const lines: string[] = [];

    // Command header
    if (showCommand) {
      lines.push(this.formatCommandHeader(result.command, result.exitCode, result.duration, showDuration));
      lines.push('');
    }

    // Output content
    if (result.output) {
      const formattedOutput = highlightSyntax 
        ? this.highlightContent(result.output)
        : result.output;
      
      lines.push(...this.wrapContent(formattedOutput, maxWidth));
    }

    // Error content
    if (result.error) {
      if (result.output) lines.push('');
      lines.push(colors.error('Error:'));
      lines.push(...this.wrapContent(result.error, maxWidth).map(line => 
        colors.error(Layout.indent(line))
      ));
    }

    return lines.join('\n');
  }

  /**
   * Format command header with status indicator
   */
  private static formatCommandHeader(command: string, exitCode: number, duration?: number, showDuration = true): string {
    const statusIcon = exitCode === 0 ? symbols.success : symbols.error;
    const statusColor = exitCode === 0 ? colors.success : colors.error;
    
    let header = `${statusColor(statusIcon)} ${colors.bold('Command:')} ${this.highlightCommand(command)}`;
    
    if (showDuration && duration !== undefined) {
      header += ` ${colors.muted(`(${duration}ms)`)}`;
    }
    
    return header;
  }

  /**
   * Highlight command syntax
   */
  private static highlightCommand(command: string): string {
    // Basic command highlighting - highlight the main command and flags
    return command.replace(/^(\w+)/, colors.primary('$1'))
                 .replace(/(\s-{1,2}\w+)/g, colors.info('$1'))
                 .replace(/(['"].*?['"])/g, colors.success('$1'));
  }

  /**
   * Highlight content based on type detection
   */
  private static highlightContent(content: string): string {
    // Try to detect content type and apply appropriate highlighting
    if (this.isJson(content)) {
      return this.highlightJson(content);
    }
    
    if (this.isFilePath(content)) {
      return this.highlightFilePaths(content);
    }
    
    if (this.hasUrls(content)) {
      return this.highlightUrls(content);
    }
    
    return content;
  }

  /**
   * Check if content is JSON
   */
  private static isJson(content: string): boolean {
    try {
      JSON.parse(content.trim());
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Highlight JSON content with proper indentation and colors
   */
  private static highlightJson(content: string): string {
    try {
      const parsed = JSON.parse(content.trim());
      const formatted = JSON.stringify(parsed, null, 2);
      
      return formatted
        .replace(/"([^"]+)":/g, colors.primary('"$1"') + ':')  // Keys
        .replace(/:\s*"([^"]+)"/g, ': ' + colors.success('"$1"'))  // String values
        .replace(/:\s*(\d+)/g, ': ' + colors.info('$1'))  // Number values
        .replace(/:\s*(true|false)/g, ': ' + colors.warning('$1'))  // Boolean values
        .replace(/:\s*null/g, ': ' + colors.muted('null'));  // Null values
    } catch {
      return content;
    }
  }

  /**
   * Check if content contains file paths
   */
  private static isFilePath(content: string): boolean {
    return /[\/\\][\w\-\.\/\\]+/.test(content);
  }

  /**
   * Highlight file paths in content
   */
  private static highlightFilePaths(content: string): string {
    return content.replace(/([\/\\][\w\-\.\/\\]+)/g, colors.info('$1'));
  }

  /**
   * Check if content contains URLs
   */
  private static hasUrls(content: string): boolean {
    return /https?:\/\/[^\s]+/.test(content);
  }

  /**
   * Highlight URLs in content
   */
  private static highlightUrls(content: string): string {
    return content.replace(/(https?:\/\/[^\s]+)/g, colors.primary('$1'));
  }

  /**
   * Wrap content to specified width
   */
  private static wrapContent(content: string, maxWidth: number): string[] {
    return content.split('\n').flatMap(line => 
      Layout.wrap(line, maxWidth)
    );
  }

  /**
   * Format structured data with proper indentation
   */
  static formatStructuredData(data: Record<string, any>, options: { indent?: number } = {}): string {
    const { indent = 0 } = options;
    const lines: string[] = [];

    for (const [key, value] of Object.entries(data)) {
      const keyStr = colors.primary(key + ':');
      
      if (typeof value === 'object' && value !== null) {
        lines.push(Layout.indent(keyStr, indent));
        if (Array.isArray(value)) {
          value.forEach((item, index) => {
            const prefix = `${colors.muted(`[${index}]`)} `;
            if (typeof item === 'object') {
              lines.push(Layout.indent(prefix, indent + 1));
              lines.push(this.formatStructuredData(item, { indent: indent + 2 }));
            } else {
              lines.push(Layout.indent(prefix + String(item), indent + 1));
            }
          });
        } else {
          lines.push(this.formatStructuredData(value, { indent: indent + 1 }));
        }
      } else {
        const valueStr = this.formatValue(value);
        lines.push(Layout.indent(`${keyStr} ${valueStr}`, indent));
      }
    }

    return lines.join('\n');
  }

  /**
   * Format individual values with appropriate colors
   */
  private static formatValue(value: any): string {
    if (value === null || value === undefined) {
      return colors.muted('null');
    }
    
    if (typeof value === 'boolean') {
      return colors.warning(String(value));
    }
    
    if (typeof value === 'number') {
      return colors.info(String(value));
    }
    
    if (typeof value === 'string') {
      // Check for special string types
      if (this.hasUrls(value)) {
        return this.highlightUrls(value);
      }
      if (this.isFilePath(value)) {
        return this.highlightFilePaths(value);
      }
      return colors.success(value);
    }
    
    return String(value);
  }
}