import { terminalCapabilities, TerminalCapabilities, ColorSupport, getResponsiveLayout, getFallbackConfig } from './TerminalCapabilities.js';
import { visualPreferences, VisualPreferences } from '../preferences/VisualPreferences.js';
import { themeManager } from '../themes/ThemeManager.js';
import { symbols } from '../utils/Symbols.js';
import { colors } from '../utils/Colors.js';
import chalk from 'chalk';

/**
 * Adaptive configuration based on terminal capabilities and user preferences
 */
export interface AdaptiveConfig {
  // Display settings
  useColors: boolean;
  colorDepth: ColorSupport;
  useUnicode: boolean;
  useEmoji: boolean;
  
  // Layout settings
  maxWidth: number;
  columns: number;
  rows: number;
  indentSize: number;
  compactMode: boolean;
  
  // Animation settings
  useAnimations: boolean;
  animationSpeed: number;
  refreshRate: number;
  
  // Accessibility settings
  highContrast: boolean;
  largeText: boolean;
  screenReaderMode: boolean;
  reducedMotion: boolean;
  
  // Fallback settings
  fallbackMode: boolean;
  basicSymbols: boolean;
  minimalOutput: boolean;
}

/**
 * Terminal adapter that provides responsive and accessible output
 * based on terminal capabilities and user preferences
 */
export class TerminalAdapter {
  private static instance: TerminalAdapter;
  private config: AdaptiveConfig | null = null;
  private capabilities: TerminalCapabilities | null = null;
  private preferences: VisualPreferences | null = null;

  private constructor() {
    // Watch for preference changes
    visualPreferences.watch(() => {
      this.invalidateConfig();
    });
  }

  public static getInstance(): TerminalAdapter {
    if (!TerminalAdapter.instance) {
      TerminalAdapter.instance = new TerminalAdapter();
    }
    return TerminalAdapter.instance;
  }

  /**
   * Initialize the adapter with terminal capabilities
   */
  public async initialize(): Promise<void> {
    this.capabilities = await terminalCapabilities.detect();
    this.preferences = visualPreferences.getPreferences();
    this.config = this.calculateAdaptiveConfig();
  }

  /**
   * Get the current adaptive configuration
   */
  public async getConfig(): Promise<AdaptiveConfig> {
    if (!this.config) {
      await this.initialize();
    }
    return this.config!;
  }

  /**
   * Invalidate cached configuration (force recalculation)
   */
  public invalidateConfig(): void {
    this.config = null;
    this.preferences = null;
  }

  /**
   * Calculate adaptive configuration based on capabilities and preferences
   */
  private calculateAdaptiveConfig(): AdaptiveConfig {
    const caps = this.capabilities!;
    const prefs = this.preferences || visualPreferences.getPreferences();
    const layout = getResponsiveLayout();
    const fallback = getFallbackConfig();

    // Determine if we should use fallback mode
    const shouldUseFallback = prefs.fallbackMode || 
                             caps.colorSupport === ColorSupport.NONE ||
                             caps.isSlowTerminal ||
                             !caps.isTTY;

    // Calculate effective settings
    const useColors = !shouldUseFallback && 
                     fallback.useColors && 
                     !prefs.screenReaderMode &&
                     (prefs.forceColor || caps.colorSupport > ColorSupport.NONE);

    const useAnimations = !shouldUseFallback &&
                         prefs.animations &&
                         !caps.reducedMotionPreferred &&
                         !prefs.reducedMotion &&
                         !caps.isSlowTerminal &&
                         caps.isInteractive;

    const compactMode = prefs.compactMode ||
                       layout.shouldUseCompactMode ||
                       caps.isSlowTerminal ||
                       prefs.screenReaderMode;

    return {
      // Display settings
      useColors,
      colorDepth: useColors ? caps.colorSupport : ColorSupport.NONE,
      useUnicode: !shouldUseFallback && caps.supportsUnicode && !prefs.screenReaderMode,
      useEmoji: !shouldUseFallback && caps.supportsEmoji && prefs.showIcons && !prefs.screenReaderMode,
      
      // Layout settings
      maxWidth: Math.min(
        prefs.maxWidth,
        layout.recommendedWidth,
        caps.columns - 4
      ),
      columns: caps.columns,
      rows: caps.rows,
      indentSize: prefs.indentSize,
      compactMode,
      
      // Animation settings
      useAnimations,
      animationSpeed: useAnimations ? this.calculateAnimationSpeed(prefs, caps) : 0,
      refreshRate: caps.recommendedRefreshRate,
      
      // Accessibility settings
      highContrast: prefs.highContrast || caps.isHighContrast,
      largeText: prefs.largeText,
      screenReaderMode: prefs.screenReaderMode || caps.hasScreenReader,
      reducedMotion: prefs.reducedMotion || caps.reducedMotionPreferred,
      
      // Fallback settings
      fallbackMode: shouldUseFallback,
      basicSymbols: shouldUseFallback || !caps.supportsUnicode,
      minimalOutput: shouldUseFallback || caps.isSlowTerminal || prefs.screenReaderMode
    };
  }

  /**
   * Calculate effective animation speed
   */
  private calculateAnimationSpeed(prefs: VisualPreferences, caps: TerminalCapabilities): number {
    let baseSpeed: number;
    
    switch (prefs.animationSpeed) {
      case 'slow': baseSpeed = 200; break;
      case 'fast': baseSpeed = 50; break;
      default: baseSpeed = 100; break;
    }
    
    // Adjust for terminal performance
    if (caps.isSlowTerminal) {
      baseSpeed *= 2; // Slower animations for slow terminals
    }
    
    if (caps.isSSH) {
      baseSpeed *= 1.5; // Slightly slower for SSH
    }
    
    return baseSpeed;
  }

  /**
   * Get adaptive symbols based on terminal capabilities
   */
  public async getSymbols(): Promise<typeof symbols> {
    const config = await this.getConfig();
    
    if (config.basicSymbols) {
      // Return ASCII-only symbols for basic terminals
      return {
        // Status symbols
        success: config.useColors ? '✓' : '[OK]',
        error: config.useColors ? '✗' : '[ERROR]',
        warning: config.useColors ? '!' : '[WARN]',
        info: config.useColors ? 'i' : '[INFO]',
        question: '?',
        
        // Progress symbols
        loading: config.useAnimations ? ['...', '..', '.'] : ['[LOADING]'],
        bullet: '*',
        arrow: '->',
        arrowRight: '->',
        arrowLeft: '<-',
        arrowUp: '^',
        arrowDown: 'v',
        
        // UI symbols
        checkbox: config.useColors ? '☐' : '[ ]',
        checkboxChecked: config.useColors ? '☑' : '[x]',
        radio: '( )',
        radioSelected: '(*)',
        
        // Decorative symbols
        star: '*',
        heart: '<3',
        diamond: '<>',
        circle: 'o',
        square: '#',
        
        // File system symbols
        home: '~',
        folder: '[DIR]',
        file: '[FILE]',
        link: '->',
        
        // Directional symbols
        up: '^',
        down: 'v',
        left: '<',
        right: '>',
        
        // Animation symbols
        spinner: ['|', '/', '-', '\\'],
        
        // Border symbols
        borderHorizontal: '-',
        borderVertical: '|',
        borderTopLeft: '+',
        borderTopRight: '+',
        borderBottomLeft: '+',
        borderBottomRight: '+',
        borderCross: '+',
        borderTop: '+',
        borderBottom: '+',
        borderLeft: '+',
        borderRight: '+',
        
        // Box drawing
        boxVertical: '|',
        boxHorizontal: '-',
        boxTopLeft: '+',
        boxTopRight: '+',
        boxBottomLeft: '+',
        boxBottomRight: '+',
        boxCross: '+',
        
        // Progress bars
        progressFull: '=',
        progressEmpty: '-',
        progressLeft: '[',
        progressRight: ']'
      };
    }
    
    // Return full Unicode symbols for capable terminals
    return symbols;
  }

  /**
   * Get adaptive colors based on terminal capabilities
   */
  public async getColors(): Promise<typeof colors> {
    const config = await this.getConfig();
    
    if (!config.useColors) {
      // Return no-op color functions for terminals without color support
      const noColor = (text: string) => text;
      return {
        success: noColor,
        error: noColor,
        warning: noColor,
        info: noColor,
        primary: noColor,
        secondary: noColor,
        muted: noColor,
        accent: noColor,
        highlight: noColor,
        text: noColor,
        textSecondary: noColor,
        textMuted: noColor,
        link: noColor,
        button: noColor,
        input: noColor,
        bold: noColor,
        dim: noColor,
        italic: noColor,
        underline: noColor,
        successBold: noColor,
        errorBold: noColor,
        warningBold: noColor,
        infoBold: noColor,
        primaryBold: noColor,
        code: noColor,
        path: noColor,
        url: noColor,
        command: noColor,
        reset: chalk.reset
      };
    }
    
    // Return theme-appropriate colors
    const theme = themeManager.getCurrentTheme();
    
    if (config.highContrast) {
      // Return high contrast color variants
      return {
        success: (text: string) => theme.colors.success(text),
        error: (text: string) => theme.colors.error(text),
        warning: (text: string) => theme.colors.warning(text),
        info: (text: string) => theme.colors.info(text),
        primary: (text: string) => theme.colors.primary(text),
        secondary: (text: string) => theme.colors.text(text),
        muted: (text: string) => theme.colors.textMuted(text),
        accent: (text: string) => theme.colors.accent(text),
        highlight: (text: string) => theme.colors.highlight(text),
        text: (text: string) => theme.colors.text(text),
        textSecondary: (text: string) => theme.colors.textSecondary(text),
        textMuted: (text: string) => theme.colors.textMuted(text),
        link: (text: string) => theme.colors.link(text),
        button: (text: string) => theme.colors.button(text),
        input: (text: string) => theme.colors.input(text),
        bold: (text: string) => theme.styles.bold(text),
        dim: (text: string) => theme.styles.dim(text),
        italic: (text: string) => theme.styles.italic(text),
        underline: (text: string) => theme.styles.underline(text),
        successBold: (text: string) => theme.colors.success(theme.styles.bold(text)),
        errorBold: (text: string) => theme.colors.error(theme.styles.bold(text)),
        warningBold: (text: string) => theme.colors.warning(theme.styles.bold(text)),
        infoBold: (text: string) => theme.colors.info(theme.styles.bold(text)),
        primaryBold: (text: string) => theme.colors.primary(theme.styles.bold(text)),
        code: (text: string) => theme.colors.code(` ${text} `),
        path: (text: string) => theme.colors.accent(text),
        url: (text: string) => theme.colors.link(text),
        command: (text: string) => theme.colors.code(` ${text} `),
        reset: chalk.reset
      };
    }
    
    return colors;
  }

  /**
   * Format text with adaptive styling
   */
  public async formatText(text: string, style: 'primary' | 'success' | 'error' | 'warning' | 'info' | 'muted' | 'bold' | 'dim'): Promise<string> {
    const adaptiveColors = await this.getColors();
    const config = await this.getConfig();
    
    if (config.screenReaderMode) {
      // Add semantic prefixes for screen readers
      switch (style) {
        case 'success': return `SUCCESS: ${text}`;
        case 'error': return `ERROR: ${text}`;
        case 'warning': return `WARNING: ${text}`;
        case 'info': return `INFO: ${text}`;
        default: return text;
      }
    }
    
    return adaptiveColors[style](text);
  }

  /**
   * Create adaptive progress indicator
   */
  public async createProgressIndicator(total: number, message?: string): Promise<{
    update: (current: number, newMessage?: string) => void;
    complete: (finalMessage?: string) => void;
    fail: (errorMessage?: string) => void;
  }> {
    const config = await this.getConfig();
    const adaptiveSymbols = await this.getSymbols();
    
    if (config.minimalOutput) {
      // Minimal progress for slow terminals or screen readers
      let lastPercent = -1;
      
      return {
        update: (current: number, newMessage?: string) => {
          const percent = Math.floor((current / total) * 100);
          if (percent !== lastPercent && percent % 10 === 0) {
            process.stdout.write(`${percent}%${newMessage ? ` - ${newMessage}` : ''}\n`);
            lastPercent = percent;
          }
        },
        complete: (finalMessage?: string) => {
          process.stdout.write(`${adaptiveSymbols.success} Complete${finalMessage ? ` - ${finalMessage}` : ''}\n`);
        },
        fail: (errorMessage?: string) => {
          process.stdout.write(`${adaptiveSymbols.error} Failed${errorMessage ? ` - ${errorMessage}` : ''}\n`);
        }
      };
    }
    
    // Full progress bar for capable terminals
    const ProgressBar = (await import('../components/ProgressBar.js')).ProgressBar;
    const progressBar = new ProgressBar({ total, ...(message && { message }) });
    
    return {
      update: (current: number, newMessage?: string) => {
        progressBar.update(current, newMessage);
      },
      complete: (finalMessage?: string) => {
        progressBar.complete(finalMessage);
      },
      fail: (errorMessage?: string) => {
        progressBar.fail(errorMessage);
      }
    };
  }

  /**
   * Get adaptive table configuration
   */
  public async getTableConfig(): Promise<{
    showBorders: boolean;
    maxWidth: number;
    compactMode: boolean;
    alignmentSupported: boolean;
  }> {
    const config = await this.getConfig();
    
    return {
      showBorders: !config.minimalOutput && !config.screenReaderMode,
      maxWidth: config.maxWidth,
      compactMode: config.compactMode,
      alignmentSupported: !config.screenReaderMode
    };
  }

  /**
   * Check if feature is supported in current configuration
   */
  public async isFeatureSupported(feature: 'colors' | 'unicode' | 'animations' | 'hyperlinks' | 'mouse'): Promise<boolean> {
    const config = await this.getConfig();
    const caps = this.capabilities!;
    
    switch (feature) {
      case 'colors': return config.useColors;
      case 'unicode': return config.useUnicode;
      case 'animations': return config.useAnimations;
      case 'hyperlinks': return caps.supportsHyperlinks && !config.screenReaderMode;
      case 'mouse': return caps.supportsMouseEvents && caps.isInteractive;
      default: return false;
    }
  }

  /**
   * Get accessibility-friendly text representation
   */
  public async getAccessibleText(content: string, type: 'status' | 'progress' | 'table' | 'list'): Promise<string> {
    const config = await this.getConfig();
    
    if (!config.screenReaderMode) {
      return content;
    }
    
    // Transform content for screen readers
    switch (type) {
      case 'status':
        // Add semantic meaning to status messages
        return content.replace(/[✓✗⚠ℹ]/g, (match) => {
          switch (match) {
            case '✓': return 'SUCCESS: ';
            case '✗': return 'ERROR: ';
            case '⚠': return 'WARNING: ';
            case 'ℹ': return 'INFO: ';
            default: return '';
          }
        });
      
      case 'progress':
        // Describe progress in words
        return content.replace(/\[.*?\]/g, (match) => {
          const filled = (match.match(/=/g) || []).length;
          const total = match.length - 2; // Exclude brackets
          const percent = Math.round((filled / total) * 100);
          return `Progress: ${percent} percent complete`;
        });
      
      case 'table':
        // Convert table to list format
        return content.replace(/[│┌┐└┘├┤┬┴┼─]/g, '').replace(/\s+/g, ' ');
      
      case 'list':
        // Ensure proper list semantics
        return content.replace(/^[•*-]\s*/gm, 'Item: ');
      
      default:
        return content;
    }
  }
}

// Export singleton instance
export const terminalAdapter = TerminalAdapter.getInstance();

// Export convenience functions
export async function getAdaptiveConfig(): Promise<AdaptiveConfig> {
  return terminalAdapter.getConfig();
}

export async function isFeatureSupported(feature: 'colors' | 'unicode' | 'animations' | 'hyperlinks' | 'mouse'): Promise<boolean> {
  return terminalAdapter.isFeatureSupported(feature);
}

export async function formatAdaptiveText(text: string, style: 'primary' | 'success' | 'error' | 'warning' | 'info' | 'muted' | 'bold' | 'dim'): Promise<string> {
  return terminalAdapter.formatText(text, style);
}