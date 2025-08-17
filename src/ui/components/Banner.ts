import { colors } from '../utils/Colors.js';
import { Layout } from '../utils/Layout.js';
import { symbols } from '../utils/Symbols.js';

export interface BannerOptions {
  showVersion?: boolean;
  showTagline?: boolean;
  compact?: boolean;
  showPlatform?: boolean;
  animated?: boolean;
}

export class Banner {
  private static readonly VERSION = '0.1.0';
  private static readonly TAGLINE = 'AI-powered OS automation for Linux & macOS';

  // ASCII art for Kira logo
  private static readonly ASCII_ART = `
██╗  ██╗██╗██████╗  █████╗ 
██║ ██╔╝██║██╔══██╗██╔══██╗
█████╔╝ ██║██████╔╝███████║
██╔═██╗ ██║██╔══██╗██╔══██║
██║  ██╗██║██║  ██║██║  ██║
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝`;

  // Compact ASCII art for smaller displays
  private static readonly ASCII_ART_COMPACT = `
██╗  ██╗██╗██████╗  █████╗ 
██║ ██╔╝██║██╔══██╗██╔══██╗
█████╔╝ ██║██████╔╝███████║
██╔═██╗ ██║██╔══██╗██╔══██║
██║  ██╗██║██║  ██║██║  ██║
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝`;

  // Mini ASCII art for very compact displays
  private static readonly ASCII_ART_MINI = `
██╗  ██╗██╗██████╗  █████╗ 
██║ ██╔╝██║██╔══██╗██╔══██╗
█████╔╝ ██║██████╔╝███████║
██╔═██╗ ██║██╔══██╗██╔══██║
██║  ██╗██║██║  ██║██║  ██║
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝`;

  // Text-only logo for terminals without Unicode support
  private static readonly TEXT_LOGO = `
 _  _ _ ____  ____ 
 |_/  | |__/  |__|
 | \\_ | |  \\  |  |`;

  static display(options: BannerOptions = {}): void {
    const opts = {
      showVersion: true,
      showTagline: true,
      compact: false,
      showPlatform: true,
      animated: false,
      ...options
    };

    const termWidth = Layout.getTerminalWidth();
    let output = '';

    // Choose appropriate ASCII art based on terminal width and options
    let logo: string;
    if (opts.compact || termWidth < 60) {
      logo = this.ASCII_ART_MINI;
    } else if (termWidth < 80) {
      logo = this.ASCII_ART_COMPACT;
    } else {
      logo = this.ASCII_ART;
    }

    // Apply colors to the logo
    const coloredLogo = logo
      .split('\n')
      .map(line => colors.primary(line))
      .join('\n');

    // Center the logo
    output += Layout.center(coloredLogo) + '\n';

    // Add tagline if requested
    if (opts.showTagline) {
      const tagline = colors.secondary(this.TAGLINE);
      output += Layout.center(tagline) + '\n';
    }

    // Add version and platform info
    if (opts.showVersion || opts.showPlatform) {
      let infoLine = '';
      
      if (opts.showVersion) {
        infoLine += colors.muted(`v${this.VERSION}`);
      }
      
      if (opts.showPlatform) {
        const platform = this.getPlatformInfo();
        if (infoLine) infoLine += colors.muted(' • ');
        infoLine += colors.muted(platform);
      }
      
      if (infoLine) {
        output += Layout.center(infoLine) + '\n';
      }
    }

    console.log(output);
  }

  static displayCompact(): void {
    const logo = colors.primary('KIRA');
    const version = colors.muted(`v${this.VERSION}`);
    const platform = colors.muted(this.getPlatformInfo());
    
    console.log(`${logo} ${version} ${colors.muted('•')} ${platform}`);
  }

  static displayMinimal(): void {
    const logo = colors.primary('🤖 Kira');
    const version = colors.muted(`v${this.VERSION}`);
    
    console.log(`${logo} ${version}`);
  }

  static getAsciiArt(compact: boolean = false): string {
    return compact ? this.ASCII_ART_COMPACT : this.ASCII_ART;
  }

  static getVersionInfo(): string {
    return `v${this.VERSION}`;
  }

  static getTagline(): string {
    return this.TAGLINE;
  }

  private static getPlatformInfo(): string {
    const platform = process.platform;
    const arch = process.arch;
    
    const platformNames: Record<string, string> = {
      'darwin': 'macOS',
      'linux': 'Linux',
      'win32': 'Windows',
      'freebsd': 'FreeBSD',
      'openbsd': 'OpenBSD'
    };
    
    const platformName = platformNames[platform] || platform;
    return `${platformName} ${arch}`;
  }

  // Display a welcome message with banner
  static welcome(options: BannerOptions = {}): void {
    this.display(options);
    
    console.log(Layout.spacing(1));
    console.log(colors.info('Welcome to Kira! 🚀'));
    console.log(colors.muted('Your AI-powered automation assistant is ready to help.'));
    console.log(Layout.spacing(1));
  }

  // Display startup banner with system info
  static startup(userName?: string, options: BannerOptions = {}): void {
    this.display(options);
    
    console.log(Layout.spacing(1));
    
    if (userName) {
      console.log(colors.info(`Hello ${colors.accent(userName)}! 👋`));
    } else {
      console.log(colors.info('Hello! 👋'));
    }
    
    console.log(colors.muted('Ready to automate your system tasks.'));
    console.log(Layout.spacing(1));
  }

  // Display error banner for critical issues
  static error(message: string): void {
    const errorBox = Layout.box(
      colors.error('⚠ CRITICAL ERROR ⚠') + '\n\n' + message,
      'KIRA ERROR',
      { style: 'double', padding: 2 }
    );
    
    console.log(Layout.center(errorBox));
  }

  // Display success banner for completed operations
  static success(message: string): void {
    const successBox = Layout.box(
      colors.success(`${symbols.success} SUCCESS`) + '\n\n' + message,
      'KIRA',
      { style: 'rounded', padding: 2 }
    );
    
    console.log(Layout.center(successBox));
  }

  // Display info banner
  static info(title: string, message: string): void {
    const infoBox = Layout.box(
      colors.info(`${symbols.info} ${title.toUpperCase()}`) + '\n\n' + message,
      'KIRA INFO',
      { style: 'single', padding: 2 }
    );
    
    console.log(Layout.center(infoBox));
  }

  // Display a separator with Kira branding
  static separator(label?: string): void {
    const separatorLabel = label ? `KIRA ${label}` : 'KIRA';
    console.log(colors.muted(Layout.separator(undefined, undefined, separatorLabel)));
  }

  // Display footer
  static footer(): void {
    console.log(Layout.spacing(1));
    console.log(colors.muted(Layout.center('Thank you for using Kira! 🤖')));
    console.log(colors.muted(Layout.center('Visit https://github.com/pragnyanramtha/autopilot for more info')));
  }
}