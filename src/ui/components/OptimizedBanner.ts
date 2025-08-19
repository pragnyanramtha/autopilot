import { colors } from '../utils/Colors.js';
import { Layout } from '../utils/Layout.js';
import { symbols } from '../utils/Symbols.js';
import { 
  withCache, 
  withPerformanceTracking, 
  lazyLoader,
  formattingOptimizer 
} from '../utils/Performance.js';

export interface OptimizedBannerOptions {
  showVersion?: boolean;
  showTagline?: boolean;
  compact?: boolean;
  showPlatform?: boolean;
  animated?: boolean;
  useCache?: boolean;
}

export class OptimizedBanner {
  private static readonly VERSION = '0.1.0';
  private static readonly TAGLINE = 'AI-powered OS automation for Linux & macOS';
  
  // Lazy-loaded ASCII art
  private static asciiArt: string | null = null;
  private static asciiArtCompact: string | null = null;
  private static asciiArtMini: string | null = null;

  // Lazy load ASCII art to reduce initial memory footprint
  private static async loadAsciiArt(): Promise<void> {
    if (this.asciiArt !== null) return;

    await lazyLoader.load('banner-ascii', async () => {
      this.asciiArt = `
██╗  ██╗██╗██████╗  █████╗ 
██║ ██╔╝██║██╔══██╗██╔══██╗
█████╔╝ ██║██████╔╝███████║
██╔═██╗ ██║██╔══██╗██╔══██║
██║  ██╗██║██║  ██║██║  ██║
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝`;

      this.asciiArtCompact = `
██╗  ██╗██╗██████╗  █████╗ 
██║ ██╔╝██║██╔══██╗██╔══██╗
█████╔╝ ██║██████╔╝███████║
██╔═██╗ ██║██╔══██╗██╔══██║
██║  ██╗██║██║  ██║██║  ██║
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝`;

      this.asciiArtMini = `
██╗  ██╗██╗██████╗  █████╗ 
██║ ██╔╝██║██╔══██╗██╔══██╗
█████╔╝ ██║██████╔╝███████║
██╔═██╗ ██║██╔══██╗██╔══██║
██║  ██╗██║██║  ██║██║  ██║
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝`;
      
      return true;
    });
  }

  static async display(options: OptimizedBannerOptions = {}): Promise<void> {
    return withPerformanceTracking('banner-display', async () => {
      const opts = {
        showVersion: true,
        showTagline: true,
        compact: false,
        showPlatform: true,
        animated: false,
        useCache: true,
        ...options
      };

      // Generate cache key for this configuration
      const cacheKey = `banner-${JSON.stringify(opts)}`;
      
      if (opts.useCache) {
        const cached = withCache(cacheKey, () => null);
        if (cached) {
          console.log(cached);
          return;
        }
      }

      // Load ASCII art lazily
      await this.loadAsciiArt();

      const termWidth = Layout.getTerminalWidth();
      let output = '';

      // Choose appropriate ASCII art based on terminal width and options
      let logo: string;
      if (opts.compact || termWidth < 60) {
        logo = this.asciiArtMini!;
      } else if (termWidth < 80) {
        logo = this.asciiArtCompact!;
      } else {
        logo = this.asciiArt!;
      }

      // Optimize color operations by batching them
      const colorOperations = logo.split('\n').map(line => ({
        text: line,
        colorFn: colors.primary
      }));

      const coloredLines = formattingOptimizer.batchColorOperations(colorOperations);
      const coloredLogo = coloredLines.join('\n');

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

      // Cache the result if caching is enabled
      if (opts.useCache) {
        withCache(cacheKey, () => output);
      }

      console.log(output);
    });
  }

  static displayCompact(): void {
    withPerformanceTracking('banner-compact', () => {
      const cacheKey = 'banner-compact-display';
      
      const output = withCache(cacheKey, () => {
        const logo = colors.primary('KIRA');
        const version = colors.muted(`v${this.VERSION}`);
        const platform = colors.muted(this.getPlatformInfo());
        
        return `${logo} ${version} ${colors.muted('•')} ${platform}`;
      });

      console.log(output);
    });
  }

  static displayMinimal(): void {
    withPerformanceTracking('banner-minimal', () => {
      const cacheKey = 'banner-minimal-display';
      
      const output = withCache(cacheKey, () => {
        const logo = colors.primary('🤖 Kira');
        const version = colors.muted(`v${this.VERSION}`);
        
        return `${logo} ${version}`;
      });

      console.log(output);
    });
  }

  static async getAsciiArt(compact: boolean = false): Promise<string> {
    await this.loadAsciiArt();
    return compact ? this.asciiArtCompact! : this.asciiArt!;
  }

  static getVersionInfo(): string {
    return `v${this.VERSION}`;
  }

  static getTagline(): string {
    return this.TAGLINE;
  }

  private static getPlatformInfo(): string {
    return withCache('platform-info', () => {
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
    });
  }

  // Optimized welcome message with caching
  static async welcome(options: OptimizedBannerOptions = {}): Promise<void> {
    return withPerformanceTracking('banner-welcome', async () => {
      await this.display(options);
      
      const welcomeMessage = withCache('welcome-message', () => {
        return Layout.spacing(1) +
               colors.info('Welcome to Kira! 🚀') + '\n' +
               colors.muted('Your AI-powered automation assistant is ready to help.') + '\n' +
               Layout.spacing(1);
      });

      console.log(welcomeMessage);
    });
  }

  // Optimized startup banner with caching
  static async startup(userName?: string, options: OptimizedBannerOptions = {}): Promise<void> {
    return withPerformanceTracking('banner-startup', async () => {
      await this.display(options);
      
      const cacheKey = `startup-message-${userName || 'anonymous'}`;
      const startupMessage = withCache(cacheKey, () => {
        let message = Layout.spacing(1);
        
        if (userName) {
          message += colors.info(`Hello ${colors.accent(userName)}! 👋`) + '\n';
        } else {
          message += colors.info('Hello! 👋') + '\n';
        }
        
        message += colors.muted('Ready to automate your system tasks.') + '\n';
        message += Layout.spacing(1);
        
        return message;
      });

      console.log(startupMessage);
    });
  }

  // Optimized error banner
  static error(message: string): void {
    withPerformanceTracking('banner-error', () => {
      const cacheKey = `error-banner-${message}`;
      
      const errorBox = withCache(cacheKey, () => {
        return Layout.box(
          colors.error('⚠ CRITICAL ERROR ⚠') + '\n\n' + message,
          'KIRA ERROR',
          { style: 'double', padding: 2 }
        );
      });
      
      console.log(Layout.center(errorBox));
    });
  }

  // Optimized success banner
  static success(message: string): void {
    withPerformanceTracking('banner-success', () => {
      const cacheKey = `success-banner-${message}`;
      
      const successBox = withCache(cacheKey, () => {
        return Layout.box(
          colors.success(`${symbols.success} SUCCESS`) + '\n\n' + message,
          'KIRA',
          { style: 'rounded', padding: 2 }
        );
      });
      
      console.log(Layout.center(successBox));
    });
  }

  // Optimized info banner
  static info(title: string, message: string): void {
    withPerformanceTracking('banner-info', () => {
      const cacheKey = `info-banner-${title}-${message}`;
      
      const infoBox = withCache(cacheKey, () => {
        return Layout.box(
          colors.info(`${symbols.info} ${title.toUpperCase()}`) + '\n\n' + message,
          'KIRA INFO',
          { style: 'single', padding: 2 }
        );
      });
      
      console.log(Layout.center(infoBox));
    });
  }

  // Optimized separator
  static separator(label?: string): void {
    withPerformanceTracking('banner-separator', () => {
      const cacheKey = `separator-${label || 'default'}`;
      
      const separator = withCache(cacheKey, () => {
        const separatorLabel = label ? `KIRA ${label}` : 'KIRA';
        return colors.muted(Layout.separator(undefined, undefined, separatorLabel));
      });
      
      console.log(separator);
    });
  }

  // Optimized footer
  static footer(): void {
    withPerformanceTracking('banner-footer', () => {
      const footer = withCache('banner-footer', () => {
        return Layout.spacing(1) +
               colors.muted(Layout.center('Thank you for using Kira! 🤖')) + '\n' +
               colors.muted(Layout.center('Visit https://github.com/pragnyanramtha/autopilot for more info'));
      });
      
      console.log(footer);
    });
  }

  // Preload all banner components for better performance
  static async preload(): Promise<void> {
    await this.loadAsciiArt();
    
    // Pre-generate common cached items
    this.getPlatformInfo();
    withCache('welcome-message', () => {
      return Layout.spacing(1) +
             colors.info('Welcome to Kira! 🚀') + '\n' +
             colors.muted('Your AI-powered automation assistant is ready to help.') + '\n' +
             Layout.spacing(1);
    });
    
    withCache('banner-footer', () => {
      return Layout.spacing(1) +
             colors.muted(Layout.center('Thank you for using Kira! 🤖')) + '\n' +
             colors.muted(Layout.center('Visit https://github.com/pragnyanramtha/autopilot for more info'));
    });
  }

  // Clear all cached banner content
  static clearCache(): void {
    // This would need to be implemented in the cache system
    // For now, we'll just reset the ASCII art
    this.asciiArt = null;
    this.asciiArtCompact = null;
    this.asciiArtMini = null;
  }
}