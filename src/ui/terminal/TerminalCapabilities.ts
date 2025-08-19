import * as os from 'os';
import * as fs from 'fs';
import { exec } from 'child_process';
import { promisify } from 'util';
import chalk from 'chalk';

const execAsync = promisify(exec);

/**
 * Terminal color support levels
 */
export enum ColorSupport {
  NONE = 0,
  BASIC = 1,      // 16 colors
  EXTENDED = 2,   // 256 colors
  TRUECOLOR = 3   // 16 million colors
}

/**
 * Terminal capabilities interface
 */
export interface TerminalCapabilities {
  // Basic terminal info
  name: string;
  version: string;
  program: string;
  
  // Display capabilities
  colorSupport: ColorSupport;
  supportsUnicode: boolean;
  supportsEmoji: boolean;
  supportsHyperlinks: boolean;
  
  // Size and layout
  columns: number;
  rows: number;
  isInteractive: boolean;
  
  // Platform info
  platform: NodeJS.Platform;
  isWSL: boolean;
  isSSH: boolean;
  isTTY: boolean;
  
  // Advanced features
  supportsMouseEvents: boolean;
  supportsAlternateScreen: boolean;
  supportsCursorPositioning: boolean;
  supportsScrollback: boolean;
  
  // Accessibility
  isHighContrast: boolean;
  hasScreenReader: boolean;
  reducedMotionPreferred: boolean;
  
  // Performance hints
  isSlowTerminal: boolean;
  recommendedRefreshRate: number;
}

/**
 * Terminal capability detection and management
 */
export class TerminalCapabilityDetector {
  private static instance: TerminalCapabilityDetector;
  private capabilities: TerminalCapabilities | null = null;
  private detectionPromise: Promise<TerminalCapabilities> | null = null;

  private constructor() {}

  public static getInstance(): TerminalCapabilityDetector {
    if (!TerminalCapabilityDetector.instance) {
      TerminalCapabilityDetector.instance = new TerminalCapabilityDetector();
    }
    return TerminalCapabilityDetector.instance;
  }

  /**
   * Detect terminal capabilities (cached)
   */
  public async detect(): Promise<TerminalCapabilities> {
    if (this.capabilities) {
      return this.capabilities;
    }

    if (this.detectionPromise) {
      return this.detectionPromise;
    }

    this.detectionPromise = this.performDetection();
    this.capabilities = await this.detectionPromise;
    return this.capabilities;
  }

  /**
   * Get cached capabilities (synchronous)
   */
  public getCached(): TerminalCapabilities | null {
    return this.capabilities;
  }

  /**
   * Force re-detection of capabilities
   */
  public async refresh(): Promise<TerminalCapabilities> {
    this.capabilities = null;
    this.detectionPromise = null;
    return this.detect();
  }

  /**
   * Perform comprehensive terminal detection
   */
  private async performDetection(): Promise<TerminalCapabilities> {
    const capabilities: TerminalCapabilities = {
      // Basic info
      name: this.detectTerminalName(),
      version: await this.detectTerminalVersion(),
      program: process.env.TERM_PROGRAM || 'unknown',
      
      // Display capabilities
      colorSupport: this.detectColorSupport(),
      supportsUnicode: this.detectUnicodeSupport(),
      supportsEmoji: this.detectEmojiSupport(),
      supportsHyperlinks: this.detectHyperlinkSupport(),
      
      // Size and layout
      columns: process.stdout.columns || 80,
      rows: process.stdout.rows || 24,
      isInteractive: this.detectInteractiveMode(),
      
      // Platform info
      platform: process.platform,
      isWSL: this.detectWSL(),
      isSSH: this.detectSSH(),
      isTTY: process.stdout.isTTY || false,
      
      // Advanced features
      supportsMouseEvents: this.detectMouseSupport(),
      supportsAlternateScreen: this.detectAlternateScreenSupport(),
      supportsCursorPositioning: this.detectCursorPositioning(),
      supportsScrollback: this.detectScrollbackSupport(),
      
      // Accessibility
      isHighContrast: this.detectHighContrast(),
      hasScreenReader: await this.detectScreenReader(),
      reducedMotionPreferred: this.detectReducedMotion(),
      
      // Performance hints
      isSlowTerminal: this.detectSlowTerminal(),
      recommendedRefreshRate: this.calculateRefreshRate()
    };

    return capabilities;
  }

  /**
   * Detect terminal name and type
   */
  private detectTerminalName(): string {
    const term = process.env.TERM || '';
    const termProgram = process.env.TERM_PROGRAM || '';
    const terminalApp = process.env.TERMINAL_EMULATOR || '';
    
    // Known terminal programs
    if (termProgram) {
      switch (termProgram.toLowerCase()) {
        case 'apple_terminal': return 'Terminal.app';
        case 'iterm.app': return 'iTerm2';
        case 'hyper': return 'Hyper';
        case 'vscode': return 'VS Code Terminal';
        case 'wezterm': return 'WezTerm';
        case 'alacritty': return 'Alacritty';
        case 'kitty': return 'Kitty';
        default: return termProgram;
      }
    }
    
    // Check terminal emulator
    if (terminalApp) {
      return terminalApp;
    }
    
    // Fallback to TERM variable
    if (term.includes('xterm')) return 'xterm-compatible';
    if (term.includes('screen')) return 'GNU Screen';
    if (term.includes('tmux')) return 'tmux';
    if (term.includes('linux')) return 'Linux Console';
    
    return term || 'unknown';
  }

  /**
   * Detect terminal version
   */
  private async detectTerminalVersion(): Promise<string> {
    const termProgram = process.env.TERM_PROGRAM || '';
    const termVersion = process.env.TERM_PROGRAM_VERSION || '';
    
    if (termVersion) {
      return termVersion;
    }
    
    // Try to detect version through other means
    try {
      switch (termProgram.toLowerCase()) {
        case 'iterm.app':
          // iTerm2 specific detection
          return await this.queryTerminalVersion('\x1b]1337;ReportVariable=name=iterm2_version\x07');
        
        case 'wezterm':
          // WezTerm specific detection
          return await this.queryTerminalVersion('\x1b]1337;GetVersion\x07');
        
        default:
          return 'unknown';
      }
    } catch {
      return 'unknown';
    }
  }

  /**
   * Query terminal for version information
   */
  private async queryTerminalVersion(query: string): Promise<string> {
    return new Promise((resolve) => {
      // Set a timeout for the query
      const timeout = setTimeout(() => resolve('unknown'), 100);
      
      // This is a simplified version - in practice, you'd need to handle
      // terminal responses properly
      clearTimeout(timeout);
      resolve('unknown');
    });
  }

  /**
   * Detect color support level
   */
  private detectColorSupport(): ColorSupport {
    // Use chalk's built-in detection as a base
    const chalkLevel = chalk.level;
    
    // Override based on environment variables
    if (process.env.FORCE_COLOR === '0' || process.env.NO_COLOR) {
      return ColorSupport.NONE;
    }
    
    if (process.env.FORCE_COLOR === '3' || process.env.COLORTERM === 'truecolor') {
      return ColorSupport.TRUECOLOR;
    }
    
    if (process.env.FORCE_COLOR === '2' || process.env.TERM?.includes('256')) {
      return ColorSupport.EXTENDED;
    }
    
    if (process.env.FORCE_COLOR === '1') {
      return ColorSupport.BASIC;
    }
    
    // Map chalk levels to our enum
    switch (chalkLevel) {
      case 0: return ColorSupport.NONE;
      case 1: return ColorSupport.BASIC;
      case 2: return ColorSupport.EXTENDED;
      case 3: return ColorSupport.TRUECOLOR;
      default: return ColorSupport.NONE;
    }
  }

  /**
   * Detect Unicode support
   */
  private detectUnicodeSupport(): boolean {
    // Check locale settings
    const locale = process.env.LC_ALL || process.env.LC_CTYPE || process.env.LANG || '';
    
    if (locale.toLowerCase().includes('utf-8') || locale.toLowerCase().includes('utf8')) {
      return true;
    }
    
    // Check terminal capabilities
    const term = process.env.TERM || '';
    const termProgram = process.env.TERM_PROGRAM || '';
    
    // Modern terminals generally support Unicode
    const modernTerminals = [
      'iterm.app', 'hyper', 'vscode', 'wezterm', 'alacritty', 'kitty'
    ];
    
    if (modernTerminals.some(t => termProgram.toLowerCase().includes(t))) {
      return true;
    }
    
    // xterm-256color and similar usually support Unicode
    if (term.includes('256') || term.includes('color')) {
      return true;
    }
    
    // Default to false for safety
    return false;
  }

  /**
   * Detect emoji support
   */
  private detectEmojiSupport(): boolean {
    // Emoji support is generally tied to Unicode support and terminal capabilities
    if (!this.detectUnicodeSupport()) {
      return false;
    }
    
    const termProgram = process.env.TERM_PROGRAM || '';
    
    // Known emoji-supporting terminals
    const emojiTerminals = [
      'iterm.app', 'hyper', 'wezterm', 'alacritty', 'kitty'
    ];
    
    return emojiTerminals.some(t => termProgram.toLowerCase().includes(t));
  }

  /**
   * Detect hyperlink support (OSC 8)
   */
  private detectHyperlinkSupport(): boolean {
    const termProgram = process.env.TERM_PROGRAM || '';
    
    // Known hyperlink-supporting terminals
    const hyperlinkTerminals = [
      'iterm.app', 'wezterm', 'alacritty', 'kitty', 'vte'
    ];
    
    return hyperlinkTerminals.some(t => termProgram.toLowerCase().includes(t));
  }

  /**
   * Detect interactive mode
   */
  private detectInteractiveMode(): boolean {
    return process.stdout.isTTY && process.stdin.isTTY;
  }

  /**
   * Detect WSL (Windows Subsystem for Linux)
   */
  private detectWSL(): boolean {
    if (process.platform !== 'linux') {
      return false;
    }
    
    try {
      // Check for WSL-specific files
      if (fs.existsSync('/proc/version')) {
        const version = fs.readFileSync('/proc/version', 'utf8');
        return version.toLowerCase().includes('microsoft') || version.toLowerCase().includes('wsl');
      }
    } catch {
      // Ignore errors
    }
    
    // Check environment variables
    return !!(process.env.WSL_DISTRO_NAME || process.env.WSLENV);
  }

  /**
   * Detect SSH connection
   */
  private detectSSH(): boolean {
    return !!(process.env.SSH_CLIENT || process.env.SSH_TTY || process.env.SSH_CONNECTION);
  }

  /**
   * Detect mouse support
   */
  private detectMouseSupport(): boolean {
    const term = process.env.TERM || '';
    const termProgram = process.env.TERM_PROGRAM || '';
    
    // Most modern terminals support mouse events
    const mouseTerminals = [
      'xterm', 'screen', 'tmux', 'iterm.app', 'wezterm', 'alacritty', 'kitty'
    ];
    
    return mouseTerminals.some(t => 
      term.includes(t) || termProgram.toLowerCase().includes(t)
    );
  }

  /**
   * Detect alternate screen support
   */
  private detectAlternateScreenSupport(): boolean {
    const term = process.env.TERM || '';
    
    // Most xterm-compatible terminals support alternate screen
    return term.includes('xterm') || term.includes('screen') || term.includes('tmux');
  }

  /**
   * Detect cursor positioning support
   */
  private detectCursorPositioning(): boolean {
    // Most terminals support ANSI cursor positioning
    return process.stdout.isTTY;
  }

  /**
   * Detect scrollback support
   */
  private detectScrollbackSupport(): boolean {
    // Most modern terminals have scrollback
    return process.stdout.isTTY;
  }

  /**
   * Detect high contrast mode
   */
  private detectHighContrast(): boolean {
    // Check Windows high contrast mode
    if (process.platform === 'win32') {
      return !!(process.env.HIGH_CONTRAST);
    }
    
    // Check macOS accessibility settings
    if (process.platform === 'darwin') {
      // This would require system calls in a real implementation
      return false;
    }
    
    // Linux accessibility settings
    const contrastEnv = process.env.GTK_THEME || process.env.QT_STYLE_OVERRIDE || '';
    return contrastEnv.toLowerCase().includes('high-contrast');
  }

  /**
   * Detect screen reader
   */
  private async detectScreenReader(): Promise<boolean> {
    // Check common screen reader environment variables
    if (process.env.NVDA || process.env.JAWS || process.env.ORCA) {
      return true;
    }
    
    // Platform-specific detection
    try {
      switch (process.platform) {
        case 'win32':
          // Check for Windows screen readers
          return await this.detectWindowsScreenReader();
        
        case 'darwin':
          // Check for macOS VoiceOver
          return await this.detectMacOSScreenReader();
        
        case 'linux':
          // Check for Linux screen readers
          return await this.detectLinuxScreenReader();
        
        default:
          return false;
      }
    } catch {
      return false;
    }
  }

  /**
   * Detect Windows screen readers
   */
  private async detectWindowsScreenReader(): Promise<boolean> {
    try {
      // Check for running screen reader processes
      const { stdout } = await execAsync('tasklist /FI "IMAGENAME eq nvda.exe" /FO CSV 2>nul');
      if (stdout.includes('nvda.exe')) return true;
      
      const { stdout: jawsCheck } = await execAsync('tasklist /FI "IMAGENAME eq jfw.exe" /FO CSV 2>nul');
      if (jawsCheck.includes('jfw.exe')) return true;
      
    } catch {
      // Ignore errors
    }
    
    return false;
  }

  /**
   * Detect macOS screen readers
   */
  private async detectMacOSScreenReader(): Promise<boolean> {
    try {
      // Check if VoiceOver is running
      const { stdout } = await execAsync('ps aux | grep -i voiceover | grep -v grep');
      return stdout.trim().length > 0;
    } catch {
      return false;
    }
  }

  /**
   * Detect Linux screen readers
   */
  private async detectLinuxScreenReader(): Promise<boolean> {
    try {
      // Check for Orca screen reader
      const { stdout } = await execAsync('ps aux | grep -i orca | grep -v grep');
      return stdout.trim().length > 0;
    } catch {
      return false;
    }
  }

  /**
   * Detect reduced motion preference
   */
  private detectReducedMotion(): boolean {
    // Check environment variable (custom)
    if (process.env.REDUCE_MOTION === '1' || process.env.PREFERS_REDUCED_MOTION === '1') {
      return true;
    }
    
    // Platform-specific checks would go here
    // This is a simplified implementation
    return false;
  }

  /**
   * Detect slow terminal (network, old hardware, etc.)
   */
  private detectSlowTerminal(): boolean {
    // SSH connections are generally slower
    if (this.detectSSH()) {
      return true;
    }
    
    // Serial connections
    if (process.env.TERM === 'linux' && !process.stdout.isTTY) {
      return true;
    }
    
    // Very old terminals
    const term = process.env.TERM || '';
    if (term === 'dumb' || term === 'vt100' || term === 'vt52') {
      return true;
    }
    
    return false;
  }

  /**
   * Calculate recommended refresh rate
   */
  private calculateRefreshRate(): number {
    if (this.detectSlowTerminal()) {
      return 10; // 10 FPS for slow terminals
    }
    
    if (this.detectSSH()) {
      return 15; // 15 FPS for SSH
    }
    
    return 30; // 30 FPS for local terminals
  }

  /**
   * Get responsive layout configuration based on terminal size
   */
  public getResponsiveLayout(): {
    columns: number;
    rows: number;
    isNarrow: boolean;
    isShort: boolean;
    recommendedWidth: number;
    shouldUseCompactMode: boolean;
  } {
    const capabilities = this.getCached();
    const columns = capabilities?.columns || process.stdout.columns || 80;
    const rows = capabilities?.rows || process.stdout.rows || 24;
    
    return {
      columns,
      rows,
      isNarrow: columns < 80,
      isShort: rows < 24,
      recommendedWidth: Math.min(columns - 4, 120), // Leave some margin
      shouldUseCompactMode: columns < 100 || rows < 30
    };
  }

  /**
   * Get fallback configuration for limited terminals
   */
  public getFallbackConfig(): {
    useColors: boolean;
    useUnicode: boolean;
    useAnimations: boolean;
    maxWidth: number;
  } {
    const capabilities = this.getCached();
    
    if (!capabilities) {
      return {
        useColors: false,
        useUnicode: false,
        useAnimations: false,
        maxWidth: 80
      };
    }
    
    return {
      useColors: capabilities.colorSupport > ColorSupport.NONE,
      useUnicode: capabilities.supportsUnicode,
      useAnimations: !capabilities.isSlowTerminal && !capabilities.reducedMotionPreferred,
      maxWidth: Math.min(capabilities.columns - 4, 120)
    };
  }
}

// Export singleton instance
export const terminalCapabilities = TerminalCapabilityDetector.getInstance();

// Export convenience functions
export async function detectTerminalCapabilities(): Promise<TerminalCapabilities> {
  return terminalCapabilities.detect();
}

export function getTerminalCapabilities(): TerminalCapabilities | null {
  return terminalCapabilities.getCached();
}

export function getResponsiveLayout() {
  return terminalCapabilities.getResponsiveLayout();
}

export function getFallbackConfig() {
  return terminalCapabilities.getFallbackConfig();
}