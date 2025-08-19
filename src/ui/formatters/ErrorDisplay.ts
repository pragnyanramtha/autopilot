import { colors } from '../utils/Colors.js';
import { symbols } from '../utils/Symbols.js';
import { Layout } from '../utils/Layout.js';

export enum ErrorType {
  SYSTEM = 'system',
  NETWORK = 'network',
  API_KEY = 'api_key',
  VALIDATION = 'validation',
  COMMAND = 'command',
  CONFIGURATION = 'configuration',
  PERMISSION = 'permission',
  UNKNOWN = 'unknown'
}

export interface ErrorDisplayOptions {
  title?: string;
  message?: string;
  details?: string;
  suggestions?: string[];
  showHelp?: boolean;
  showStackTrace?: boolean;
  type?: ErrorType;
}

export interface SystemError extends Error {
  code?: string;
  errno?: number;
  syscall?: string;
  path?: string;
}

export interface NetworkError extends Error {
  code?: string;
  status?: number;
  url?: string;
}

export class ErrorDisplay {
  /**
   * Display a formatted error message with contextual information
   */
  static show(error: Error, options: ErrorDisplayOptions = {}): void {
    const {
      title,
      message,
      details,
      suggestions = [],
      showHelp = false,
      showStackTrace = false,
      type = ErrorType.UNKNOWN
    } = options;

    console.log(); // Add spacing

    // Display error header
    const errorTitle = title || this.getErrorTitle(type);
    console.log(colors.error(`${symbols.error} ${errorTitle}`));
    console.log(colors.muted(Layout.separator('─', 50)));

    // Display main error message
    if (message) {
      console.log(colors.bold(message));
    } else {
      console.log(colors.bold(error.message));
    }

    // Display error details if provided
    if (details) {
      console.log();
      console.log(colors.muted('Details:'));
      console.log(Layout.indent(details));
    }

    // Display error-specific information
    this.displayErrorSpecificInfo(error, type);

    // Display suggestions if provided
    if (suggestions.length > 0) {
      console.log();
      console.log(colors.info(`${symbols.info} Suggestions:`));
      suggestions.forEach(suggestion => {
        console.log(Layout.indent(`${symbols.bullet} ${suggestion}`));
      });
    }

    // Display help information if requested
    if (showHelp) {
      this.displayContextualHelp(type);
    }

    // Display stack trace in debug mode
    if (showStackTrace && error.stack) {
      console.log();
      console.log(colors.muted('Stack Trace:'));
      console.log(colors.dim(Layout.indent(error.stack)));
    }

    console.log(); // Add spacing
  }

  /**
   * Display API key setup error with instructions
   */
  static showApiKeyError(): void {
    console.log();
    console.log(colors.error(`${symbols.error} API Key Required`));
    console.log(colors.muted(Layout.separator('─', 50)));
    
    console.log(colors.bold('Kira requires a Gemini API key to function.'));
    console.log();
    
    console.log(colors.info(`${symbols.info} Setup Instructions:`));
    console.log(Layout.indent(`${symbols.bullet} Visit: ${colors.primary('https://makersuite.google.com/app/apikey')}`));
    console.log(Layout.indent(`${symbols.bullet} Create a new API key`));
    console.log(Layout.indent(`${symbols.bullet} Run: ${colors.primary('kira init')} to configure`));
    console.log(Layout.indent(`${symbols.bullet} Or set: ${colors.primary('GEMINI_API_KEY')} environment variable`));
    
    console.log();
    console.log(colors.warning(`${symbols.warning} Keep your API key secure and never share it publicly.`));
    console.log();
  }

  /**
   * Display system-related errors with platform-specific information
   */
  static showSystemError(error: SystemError): void {
    const suggestions: string[] = [];
    
    // Add platform-specific suggestions based on error code
    switch (error.code) {
      case 'ENOENT':
        suggestions.push('Check if the file or directory exists');
        suggestions.push('Verify the path is correct');
        break;
      case 'EACCES':
        suggestions.push('Check file permissions');
        suggestions.push('Try running with appropriate privileges');
        break;
      case 'ENOTDIR':
        suggestions.push('Verify the path points to a directory, not a file');
        break;
      default:
        suggestions.push('Check system logs for more information');
    }

    const options: ErrorDisplayOptions = {
      title: 'System Error',
      message: error.message,
      suggestions,
      type: ErrorType.SYSTEM,
      showHelp: true
    };
    if (error.path) {
      options.details = `Path: ${error.path}`;
    }
    this.show(error, options);
  }

  /**
   * Display network-related errors with connectivity information
   */
  static showNetworkError(error: NetworkError): void {
    const suggestions: string[] = [];
    
    // Add network-specific suggestions
    if (error.code === 'ENOTFOUND') {
      suggestions.push('Check your internet connection');
      suggestions.push('Verify the URL is correct');
      suggestions.push('Check if you are behind a proxy or firewall');
    } else if (error.status) {
      if (error.status >= 400 && error.status < 500) {
        suggestions.push('Check your API key and permissions');
        suggestions.push('Verify the request parameters');
      } else if (error.status >= 500) {
        suggestions.push('The service may be temporarily unavailable');
        suggestions.push('Try again in a few minutes');
      }
    }

    const details = [];
    if (error.url) details.push(`URL: ${error.url}`);
    if (error.status) details.push(`Status: ${error.status}`);

    this.show(error, {
      title: 'Network Error',
      message: error.message,
      details: details.join('\n'),
      suggestions,
      type: ErrorType.NETWORK,
      showHelp: true
    });
  }

  /**
   * Display command execution errors
   */
  static showCommandError(command: string, error: Error, exitCode?: number): void {
    const suggestions = [
      'Check if the command exists and is in your PATH',
      'Verify command syntax and arguments',
      'Check if you have necessary permissions'
    ];

    const details = [];
    details.push(`Command: ${command}`);
    if (exitCode !== undefined) details.push(`Exit Code: ${exitCode}`);

    this.show(error, {
      title: 'Command Execution Error',
      message: error.message,
      details: details.join('\n'),
      suggestions,
      type: ErrorType.COMMAND,
      showHelp: true
    });
  }

  /**
   * Display validation errors with specific field information
   */
  static showValidationError(field: string, value: any, rules: string[]): void {
    const message = `Invalid value for ${field}: ${value}`;
    const suggestions = rules.map(rule => `Must ${rule}`);

    this.show(new Error(message), {
      title: 'Validation Error',
      message,
      suggestions,
      type: ErrorType.VALIDATION
    });
  }

  /**
   * Get appropriate error title based on error type
   */
  private static getErrorTitle(type: ErrorType): string {
    switch (type) {
      case ErrorType.SYSTEM:
        return 'System Error';
      case ErrorType.NETWORK:
        return 'Network Error';
      case ErrorType.API_KEY:
        return 'API Key Error';
      case ErrorType.VALIDATION:
        return 'Validation Error';
      case ErrorType.COMMAND:
        return 'Command Error';
      case ErrorType.CONFIGURATION:
        return 'Configuration Error';
      case ErrorType.PERMISSION:
        return 'Permission Error';
      default:
        return 'Error';
    }
  }

  /**
   * Display error-specific information based on error type and content
   */
  private static displayErrorSpecificInfo(error: Error, type: ErrorType): void {
    if (type === ErrorType.SYSTEM && 'code' in error) {
      const systemError = error as SystemError;
      console.log();
      console.log(colors.muted('System Information:'));
      if (systemError.code) {
        console.log(Layout.indent(`Error Code: ${systemError.code}`));
      }
      if (systemError.errno) {
        console.log(Layout.indent(`Error Number: ${systemError.errno}`));
      }
      if (systemError.syscall) {
        console.log(Layout.indent(`System Call: ${systemError.syscall}`));
      }
    }

    if (type === ErrorType.NETWORK && 'status' in error) {
      const networkError = error as NetworkError;
      console.log();
      console.log(colors.muted('Network Information:'));
      if (networkError.status) {
        console.log(Layout.indent(`HTTP Status: ${networkError.status}`));
      }
      if (networkError.code) {
        console.log(Layout.indent(`Error Code: ${networkError.code}`));
      }
    }
  }

  /**
   * Display contextual help based on error type
   */
  private static displayContextualHelp(type: ErrorType): void {
    console.log();
    console.log(colors.info(`${symbols.info} Need Help?`));
    
    switch (type) {
      case ErrorType.API_KEY:
        console.log(Layout.indent(`${symbols.bullet} Run ${colors.primary('kira init')} to set up your API key`));
        console.log(Layout.indent(`${symbols.bullet} Visit the Gemini API documentation for more information`));
        break;
      case ErrorType.SYSTEM:
        console.log(Layout.indent(`${symbols.bullet} Check system requirements and permissions`));
        console.log(Layout.indent(`${symbols.bullet} Run ${colors.primary('kira doctor')} to diagnose system issues`));
        break;
      case ErrorType.NETWORK:
        console.log(Layout.indent(`${symbols.bullet} Check your internet connection`));
        console.log(Layout.indent(`${symbols.bullet} Verify proxy and firewall settings`));
        break;
      case ErrorType.COMMAND:
        console.log(Layout.indent(`${symbols.bullet} Run ${colors.primary('kira help')} for command documentation`));
        console.log(Layout.indent(`${symbols.bullet} Use ${colors.primary('--help')} flag with specific commands`));
        break;
      default:
        console.log(Layout.indent(`${symbols.bullet} Run ${colors.primary('kira help')} for general assistance`));
        console.log(Layout.indent(`${symbols.bullet} Check the documentation for troubleshooting guides`));
    }
  }
}