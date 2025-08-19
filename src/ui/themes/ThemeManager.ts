import chalk, { ChalkInstance } from 'chalk';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { createDefaultTheme } from './DefaultTheme.js';
import { createDarkTheme } from './DarkTheme.js';
import { createLightTheme } from './LightTheme.js';

// Enhanced theme interface with more semantic colors
export interface Theme {
  name: string;
  description: string;
  colors: {
    // Primary colors
    primary: ChalkInstance;
    secondary: ChalkInstance;
    tertiary: ChalkInstance;
    
    // Status colors
    success: ChalkInstance;
    error: ChalkInstance;
    warning: ChalkInstance;
    info: ChalkInstance;
    
    // UI colors
    muted: ChalkInstance;
    accent: ChalkInstance;
    highlight: ChalkInstance;
    border: ChalkInstance;
    background: ChalkInstance;
    
    // Text colors
    text: ChalkInstance;
    textSecondary: ChalkInstance;
    textMuted: ChalkInstance;
    
    // Interactive colors
    link: ChalkInstance;
    button: ChalkInstance;
    input: ChalkInstance;
    
    // Code colors
    code: ChalkInstance;
    codeBackground: ChalkInstance;
    keyword: ChalkInstance;
    string: ChalkInstance;
    number: ChalkInstance;
    comment: ChalkInstance;
  };
  
  // Text styles
  styles: {
    bold: ChalkInstance;
    dim: ChalkInstance;
    italic: ChalkInstance;
    underline: ChalkInstance;
    strikethrough: ChalkInstance;
    inverse: ChalkInstance;
  };
  
  // Theme metadata
  metadata: {
    isDark: boolean;
    isHighContrast: boolean;
    supportsColor: boolean;
    supports256Color: boolean;
    supportsTrueColor: boolean;
  };
}

export interface ThemePreferences {
  theme: 'auto' | 'default' | 'dark' | 'light' | 'high-contrast' | 'minimal';
  autoDetect: boolean;
  forceColor: boolean;
  animations: boolean;
  compactMode: boolean;
}

export class ThemeManager {
  private static instance: ThemeManager;
  private currentTheme: Theme;
  private preferences: ThemePreferences;
  private configPath: string;
  private themes: Map<string, Theme> = new Map();

  private constructor() {
    this.configPath = path.join(os.homedir(), '.kira', 'theme.json');
    this.preferences = this.loadPreferences();
    this.initializeThemes();
    this.currentTheme = this.selectTheme();
  }

  public static getInstance(): ThemeManager {
    if (!ThemeManager.instance) {
      ThemeManager.instance = new ThemeManager();
    }
    return ThemeManager.instance;
  }

  // Initialize all available themes
  private initializeThemes(): void {
    this.themes.set('default', createDefaultTheme());
    this.themes.set('dark', createDarkTheme());
    this.themes.set('light', createLightTheme());
    this.themes.set('high-contrast', this.createHighContrastTheme());
    this.themes.set('minimal', this.createMinimalTheme());
  }

  // Detect terminal capabilities
  private detectTerminalCapabilities(): {
    hasColor: boolean;
    has256Color: boolean;
    hasTrueColor: boolean;
    isDarkBackground: boolean;
  } {
    const hasColor = chalk.level > 0;
    const has256Color = chalk.level >= 2;
    const hasTrueColor = chalk.level >= 3;
    
    // Try to detect dark background (heuristic approach)
    const term = process.env.TERM || '';
    const termProgram = process.env.TERM_PROGRAM || '';
    
    // Most modern terminals default to dark backgrounds
    const isDarkBackground = !term.includes('light') && 
                            !termProgram.includes('Light') &&
                            termProgram !== 'Apple_Terminal'; // Terminal.app defaults to light

    return {
      hasColor,
      has256Color,
      hasTrueColor,
      isDarkBackground
    };
  }



  // Create high contrast theme (accessibility focused)
  private createHighContrastTheme(): Theme {
    const capabilities = this.detectTerminalCapabilities();
    
    return {
      name: 'high-contrast',
      description: 'High contrast theme for accessibility',
      colors: {
        primary: chalk.white.bold,
        secondary: chalk.white,
        tertiary: chalk.whiteBright,
        
        success: chalk.black.bgGreen.bold,
        error: chalk.white.bgRed.bold,
        warning: chalk.black.bgYellow.bold,
        info: chalk.white.bgBlue.bold,
        
        muted: chalk.gray,
        accent: chalk.white.bold,
        highlight: chalk.black.bgWhite,
        border: chalk.white,
        background: chalk.reset,
        
        text: chalk.white.bold,
        textSecondary: chalk.white,
        textMuted: chalk.gray,
        
        link: chalk.white.underline.bold,
        button: chalk.black.bgWhite.bold,
        input: chalk.black.bgWhite,
        
        code: chalk.black.bgWhite,
        codeBackground: chalk.bgWhite,
        keyword: chalk.black.bgWhite.bold,
        string: chalk.black.bgGreen,
        number: chalk.black.bgYellow,
        comment: chalk.gray
      },
      styles: {
        bold: chalk.bold,
        dim: chalk.reset, // No dim in high contrast
        italic: chalk.italic,
        underline: chalk.underline,
        strikethrough: chalk.strikethrough,
        inverse: chalk.inverse
      },
      metadata: {
        isDark: true,
        isHighContrast: true,
        supportsColor: capabilities.hasColor,
        supports256Color: capabilities.has256Color,
        supportsTrueColor: capabilities.hasTrueColor
      }
    };
  }

  // Create minimal theme (no colors, ASCII only)
  private createMinimalTheme(): Theme {
    return {
      name: 'minimal',
      description: 'Minimal theme with no colors for basic terminals',
      colors: {
        primary: chalk.reset,
        secondary: chalk.reset,
        tertiary: chalk.reset,
        
        success: chalk.reset,
        error: chalk.reset,
        warning: chalk.reset,
        info: chalk.reset,
        
        muted: chalk.reset,
        accent: chalk.reset,
        highlight: chalk.inverse,
        border: chalk.reset,
        background: chalk.reset,
        
        text: chalk.reset,
        textSecondary: chalk.reset,
        textMuted: chalk.reset,
        
        link: chalk.underline,
        button: chalk.inverse,
        input: chalk.underline,
        
        code: chalk.inverse,
        codeBackground: chalk.reset,
        keyword: chalk.reset,
        string: chalk.reset,
        number: chalk.reset,
        comment: chalk.reset
      },
      styles: {
        bold: chalk.bold,
        dim: chalk.reset,
        italic: chalk.reset,
        underline: chalk.underline,
        strikethrough: chalk.reset,
        inverse: chalk.inverse
      },
      metadata: {
        isDark: false,
        isHighContrast: false,
        supportsColor: false,
        supports256Color: false,
        supportsTrueColor: false
      }
    };
  }

  // Select appropriate theme based on preferences and capabilities
  private selectTheme(): Theme {
    const capabilities = this.detectTerminalCapabilities();
    
    // Force minimal theme if no color support
    if (!capabilities.hasColor && this.preferences.theme !== 'minimal') {
      return this.themes.get('minimal')!;
    }

    // Handle auto theme selection
    if (this.preferences.theme === 'auto' && this.preferences.autoDetect) {
      if (!capabilities.hasColor) {
        return this.themes.get('minimal')!;
      } else if (capabilities.isDarkBackground) {
        return this.themes.get('dark')!;
      } else {
        return this.themes.get('light')!;
      }
    }

    // Return requested theme or fallback to default
    return this.themes.get(this.preferences.theme) || this.themes.get('default')!;
  }

  // Load theme preferences from config file
  private loadPreferences(): ThemePreferences {
    const defaultPreferences: ThemePreferences = {
      theme: 'auto',
      autoDetect: true,
      forceColor: false,
      animations: true,
      compactMode: false
    };

    try {
      if (fs.existsSync(this.configPath)) {
        const configData = fs.readFileSync(this.configPath, 'utf8');
        const config = JSON.parse(configData);
        return { ...defaultPreferences, ...config };
      }
    } catch (error) {
      // Ignore errors and use defaults
    }

    return defaultPreferences;
  }

  // Save theme preferences to config file
  private savePreferences(): void {
    try {
      const configDir = path.dirname(this.configPath);
      if (!fs.existsSync(configDir)) {
        fs.mkdirSync(configDir, { recursive: true });
      }
      
      fs.writeFileSync(this.configPath, JSON.stringify(this.preferences, null, 2));
    } catch (error) {
      console.warn('Failed to save theme preferences:', error);
    }
  }

  // Public API methods
  public getCurrentTheme(): Theme {
    return this.currentTheme;
  }

  public getAvailableThemes(): string[] {
    return Array.from(this.themes.keys());
  }

  public getTheme(name: string): Theme | undefined {
    return this.themes.get(name);
  }

  public setTheme(themeName: string): boolean {
    const theme = this.themes.get(themeName);
    if (theme) {
      this.currentTheme = theme;
      this.preferences.theme = themeName as any;
      this.savePreferences();
      return true;
    }
    return false;
  }

  public getPreferences(): ThemePreferences {
    return { ...this.preferences };
  }

  public updatePreferences(updates: Partial<ThemePreferences>): void {
    this.preferences = { ...this.preferences, ...updates };
    this.savePreferences();
    
    // Reselect theme if auto-detect changed
    if (updates.autoDetect !== undefined || updates.theme !== undefined) {
      this.currentTheme = this.selectTheme();
    }
  }

  public detectCapabilities() {
    return this.detectTerminalCapabilities();
  }

  // Utility methods for common theme operations
  public isColorSupported(): boolean {
    return this.currentTheme.metadata.supportsColor;
  }

  public isDarkTheme(): boolean {
    return this.currentTheme.metadata.isDark;
  }

  public isHighContrast(): boolean {
    return this.currentTheme.metadata.isHighContrast;
  }

  public supportsAnimations(): boolean {
    return this.preferences.animations && this.isColorSupported();
  }

  public isCompactMode(): boolean {
    return this.preferences.compactMode;
  }

  // Reset to defaults
  public resetToDefaults(): void {
    this.preferences = {
      theme: 'auto',
      autoDetect: true,
      forceColor: false,
      animations: true,
      compactMode: false
    };
    this.currentTheme = this.selectTheme();
    this.savePreferences();
  }
}

// Export singleton instance
export const themeManager = ThemeManager.getInstance();

// Export convenience functions
export function getCurrentTheme(): Theme {
  return themeManager.getCurrentTheme();
}

export function setTheme(themeName: string): boolean {
  return themeManager.setTheme(themeName);
}

export function getThemeColors() {
  return themeManager.getCurrentTheme().colors;
}

export function getThemeStyles() {
  return themeManager.getCurrentTheme().styles;
}