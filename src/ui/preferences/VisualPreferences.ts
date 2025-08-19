import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { themeManager, ThemePreferences } from '../themes/ThemeManager.js';

/**
 * Comprehensive visual preferences interface
 * Extends the basic theme preferences with additional visual customization options
 */
export interface VisualPreferences extends ThemePreferences {
  // Theme and appearance
  theme: 'auto' | 'default' | 'dark' | 'light' | 'high-contrast' | 'minimal';
  autoDetect: boolean;
  forceColor: boolean;
  
  // Animation and interaction
  animations: boolean;
  animationSpeed: 'slow' | 'normal' | 'fast';
  progressStyle: 'bar' | 'spinner' | 'dots' | 'minimal';
  
  // Layout and spacing
  compactMode: boolean;
  density: 'comfortable' | 'normal' | 'compact';
  indentSize: number;
  maxWidth: number;
  
  // Visual elements
  showIcons: boolean;
  showBorders: boolean;
  showShadows: boolean;
  roundedCorners: boolean;
  
  // Accessibility
  highContrast: boolean;
  reducedMotion: boolean;
  largeText: boolean;
  screenReaderMode: boolean;
  
  // Advanced options
  customColors: Record<string, string>;
  customSymbols: Record<string, string>;
  fallbackMode: boolean;
}

/**
 * Default visual preferences
 */
export const DEFAULT_VISUAL_PREFERENCES: VisualPreferences = {
  // Theme and appearance
  theme: 'auto',
  autoDetect: true,
  forceColor: false,
  
  // Animation and interaction
  animations: true,
  animationSpeed: 'normal',
  progressStyle: 'bar',
  
  // Layout and spacing
  compactMode: false,
  density: 'normal',
  indentSize: 2,
  maxWidth: 120,
  
  // Visual elements
  showIcons: true,
  showBorders: true,
  showShadows: false,
  roundedCorners: true,
  
  // Accessibility
  highContrast: false,
  reducedMotion: false,
  largeText: false,
  screenReaderMode: false,
  
  // Advanced options
  customColors: {},
  customSymbols: {},
  fallbackMode: false
};

/**
 * Visual preferences manager
 * Handles loading, saving, and managing visual customization preferences
 */
export class VisualPreferencesManager {
  private static instance: VisualPreferencesManager;
  private preferences: VisualPreferences;
  private configPath: string;
  private watchers: Array<(preferences: VisualPreferences) => void> = [];

  private constructor() {
    this.configPath = path.join(os.homedir(), '.ap', 'visual-preferences.json');
    this.preferences = this.loadPreferences();
    this.syncWithThemeManager();
  }

  public static getInstance(): VisualPreferencesManager {
    if (!VisualPreferencesManager.instance) {
      VisualPreferencesManager.instance = new VisualPreferencesManager();
    }
    return VisualPreferencesManager.instance;
  }

  /**
   * Load preferences from config file
   */
  private loadPreferences(): VisualPreferences {
    try {
      if (fs.existsSync(this.configPath)) {
        const configData = fs.readFileSync(this.configPath, 'utf8');
        const config = JSON.parse(configData);
        
        // Merge with defaults to ensure all properties exist
        return { ...DEFAULT_VISUAL_PREFERENCES, ...config };
      }
    } catch (error) {
      console.warn('Failed to load visual preferences, using defaults:', error);
    }

    return { ...DEFAULT_VISUAL_PREFERENCES };
  }

  /**
   * Save preferences to config file
   */
  private savePreferences(): void {
    try {
      const configDir = path.dirname(this.configPath);
      if (!fs.existsSync(configDir)) {
        fs.mkdirSync(configDir, { recursive: true });
      }
      
      fs.writeFileSync(this.configPath, JSON.stringify(this.preferences, null, 2));
      this.notifyWatchers();
    } catch (error) {
      console.warn('Failed to save visual preferences:', error);
    }
  }

  /**
   * Sync with theme manager to keep preferences in sync
   */
  private syncWithThemeManager(): void {
    const themePrefs: ThemePreferences = {
      theme: this.preferences.theme,
      autoDetect: this.preferences.autoDetect,
      forceColor: this.preferences.forceColor,
      animations: this.preferences.animations,
      compactMode: this.preferences.compactMode
    };
    
    themeManager.updatePreferences(themePrefs);
  }

  /**
   * Notify watchers of preference changes
   */
  private notifyWatchers(): void {
    this.watchers.forEach(watcher => {
      try {
        watcher(this.preferences);
      } catch (error) {
        console.warn('Error in preference watcher:', error);
      }
    });
  }

  // Public API methods

  /**
   * Get current visual preferences
   */
  public getPreferences(): VisualPreferences {
    return { ...this.preferences };
  }

  /**
   * Update visual preferences
   */
  public updatePreferences(updates: Partial<VisualPreferences>): void {
    this.preferences = { ...this.preferences, ...updates };
    this.savePreferences();
    this.syncWithThemeManager();
  }

  /**
   * Reset preferences to defaults
   */
  public resetToDefaults(): void {
    this.preferences = { ...DEFAULT_VISUAL_PREFERENCES };
    this.savePreferences();
    this.syncWithThemeManager();
  }

  /**
   * Watch for preference changes
   */
  public watch(callback: (preferences: VisualPreferences) => void): () => void {
    this.watchers.push(callback);
    
    // Return unwatch function
    return () => {
      const index = this.watchers.indexOf(callback);
      if (index > -1) {
        this.watchers.splice(index, 1);
      }
    };
  }

  // Convenience methods for specific preference categories

  /**
   * Get theme-related preferences
   */
  public getThemePreferences(): ThemePreferences {
    return {
      theme: this.preferences.theme,
      autoDetect: this.preferences.autoDetect,
      forceColor: this.preferences.forceColor,
      animations: this.preferences.animations,
      compactMode: this.preferences.compactMode
    };
  }

  /**
   * Update theme preferences
   */
  public updateThemePreferences(updates: Partial<ThemePreferences>): void {
    this.updatePreferences(updates);
  }

  /**
   * Get animation preferences
   */
  public getAnimationPreferences() {
    return {
      animations: this.preferences.animations,
      animationSpeed: this.preferences.animationSpeed,
      progressStyle: this.preferences.progressStyle,
      reducedMotion: this.preferences.reducedMotion
    };
  }

  /**
   * Get layout preferences
   */
  public getLayoutPreferences() {
    return {
      compactMode: this.preferences.compactMode,
      density: this.preferences.density,
      indentSize: this.preferences.indentSize,
      maxWidth: this.preferences.maxWidth
    };
  }

  /**
   * Get accessibility preferences
   */
  public getAccessibilityPreferences() {
    return {
      highContrast: this.preferences.highContrast,
      reducedMotion: this.preferences.reducedMotion,
      largeText: this.preferences.largeText,
      screenReaderMode: this.preferences.screenReaderMode
    };
  }

  /**
   * Check if animations should be enabled
   */
  public shouldShowAnimations(): boolean {
    return this.preferences.animations && !this.preferences.reducedMotion;
  }

  /**
   * Check if icons should be shown
   */
  public shouldShowIcons(): boolean {
    return this.preferences.showIcons && !this.preferences.screenReaderMode;
  }

  /**
   * Check if colors should be used
   */
  public shouldUseColors(): boolean {
    return !this.preferences.fallbackMode && themeManager.isColorSupported();
  }

  /**
   * Get effective density based on preferences and accessibility
   */
  public getEffectiveDensity(): 'comfortable' | 'normal' | 'compact' {
    if (this.preferences.largeText) {
      return 'comfortable';
    }
    if (this.preferences.compactMode) {
      return 'compact';
    }
    return this.preferences.density;
  }

  /**
   * Get effective animation speed
   */
  public getEffectiveAnimationSpeed(): number {
    if (!this.shouldShowAnimations()) {
      return 0;
    }
    
    switch (this.preferences.animationSpeed) {
      case 'slow': return 200;
      case 'fast': return 50;
      default: return 100;
    }
  }

  /**
   * Import preferences from a JSON object
   */
  public importPreferences(preferences: Partial<VisualPreferences>): void {
    // Validate and sanitize imported preferences
    const validatedPreferences = this.validatePreferences(preferences);
    this.updatePreferences(validatedPreferences);
  }

  /**
   * Export preferences as JSON
   */
  public exportPreferences(): VisualPreferences {
    return { ...this.preferences };
  }

  /**
   * Validate preferences object
   */
  private validatePreferences(preferences: Partial<VisualPreferences>): Partial<VisualPreferences> {
    const validated: Partial<VisualPreferences> = {};

    // Validate theme
    if (preferences.theme && ['auto', 'default', 'dark', 'light', 'high-contrast', 'minimal'].includes(preferences.theme)) {
      validated.theme = preferences.theme;
    }

    // Validate animation speed
    if (preferences.animationSpeed && ['slow', 'normal', 'fast'].includes(preferences.animationSpeed)) {
      validated.animationSpeed = preferences.animationSpeed;
    }

    // Validate progress style
    if (preferences.progressStyle && ['bar', 'spinner', 'dots', 'minimal'].includes(preferences.progressStyle)) {
      validated.progressStyle = preferences.progressStyle;
    }

    // Validate density
    if (preferences.density && ['comfortable', 'normal', 'compact'].includes(preferences.density)) {
      validated.density = preferences.density;
    }

    // Validate numeric values
    if (typeof preferences.indentSize === 'number' && preferences.indentSize >= 0 && preferences.indentSize <= 8) {
      validated.indentSize = preferences.indentSize;
    }

    if (typeof preferences.maxWidth === 'number' && preferences.maxWidth >= 40 && preferences.maxWidth <= 200) {
      validated.maxWidth = preferences.maxWidth;
    }

    // Validate boolean values
    const booleanFields: (keyof VisualPreferences)[] = [
      'autoDetect', 'forceColor', 'animations', 'compactMode', 'showIcons',
      'showBorders', 'showShadows', 'roundedCorners', 'highContrast',
      'reducedMotion', 'largeText', 'screenReaderMode', 'fallbackMode'
    ];

    booleanFields.forEach(field => {
      if (typeof preferences[field] === 'boolean') {
        (validated as any)[field] = preferences[field];
      }
    });

    // Validate custom colors and symbols
    if (preferences.customColors && typeof preferences.customColors === 'object') {
      validated.customColors = preferences.customColors;
    }

    if (preferences.customSymbols && typeof preferences.customSymbols === 'object') {
      validated.customSymbols = preferences.customSymbols;
    }

    return validated;
  }
}

// Export singleton instance
export const visualPreferences = VisualPreferencesManager.getInstance();

// Export convenience functions
export function getVisualPreferences(): VisualPreferences {
  return visualPreferences.getPreferences();
}

export function updateVisualPreferences(updates: Partial<VisualPreferences>): void {
  visualPreferences.updatePreferences(updates);
}

export function shouldShowAnimations(): boolean {
  return visualPreferences.shouldShowAnimations();
}

export function shouldShowIcons(): boolean {
  return visualPreferences.shouldShowIcons();
}

export function shouldUseColors(): boolean {
  return visualPreferences.shouldUseColors();
}