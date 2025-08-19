import chalk from 'chalk';
import { visualPreferences, VisualPreferences, DEFAULT_VISUAL_PREFERENCES } from './VisualPreferences.js';
import { themeManager } from '../themes/ThemeManager.js';
import { Table } from '../components/Table.js';
import { StatusIndicator } from '../components/StatusIndicator.js';
import { Banner } from '../components/Banner.js';

/**
 * Configuration interface for visual preferences
 * Provides CLI commands to view and modify visual settings
 */
export class PreferencesConfig {
  
  /**
   * Display current visual preferences
   */
  public static displayCurrentPreferences(): void {
    const prefs = visualPreferences.getPreferences();
    const theme = themeManager.getCurrentTheme();
    
    console.log(chalk.cyan.bold('\n🎨 Current Visual Preferences\n'));
    
    // Theme section
    console.log(chalk.yellow.bold('Theme & Appearance:'));
    const themeTable = new Table([
      { header: 'Setting', key: 'setting', width: 20 },
      { header: 'Value', key: 'value', width: 30 },
      { header: 'Description', key: 'description', width: 40 }
    ]);
    
    themeTable.addRow({
      setting: 'Theme',
      value: `${prefs.theme} ${prefs.autoDetect ? '(auto-detect)' : ''}`,
      description: `Current: ${theme.name} - ${theme.description}`
    });
    
    themeTable.addRow({
      setting: 'Colors',
      value: prefs.forceColor ? 'Forced On' : (themeManager.isColorSupported() ? 'Enabled' : 'Disabled'),
      description: 'Color support in terminal'
    });
    
    themeTable.addRow({
      setting: 'High Contrast',
      value: prefs.highContrast ? 'Enabled' : 'Disabled',
      description: 'Enhanced contrast for accessibility'
    });
    
    console.log(themeTable.render());
    
    // Animation section
    console.log(chalk.yellow.bold('\nAnimation & Interaction:'));
    const animationTable = new Table([
      { header: 'Setting', key: 'setting', width: 20 },
      { header: 'Value', key: 'value', width: 30 },
      { header: 'Description', key: 'description', width: 40 }
    ]);
    
    animationTable.addRow({
      setting: 'Animations',
      value: prefs.animations ? `Enabled (${prefs.animationSpeed})` : 'Disabled',
      description: 'Progress bars, spinners, and transitions'
    });
    
    animationTable.addRow({
      setting: 'Progress Style',
      value: prefs.progressStyle,
      description: 'Style for progress indicators'
    });
    
    animationTable.addRow({
      setting: 'Reduced Motion',
      value: prefs.reducedMotion ? 'Enabled' : 'Disabled',
      description: 'Accessibility setting for motion sensitivity'
    });
    
    console.log(animationTable.render());
    
    // Layout section
    console.log(chalk.yellow.bold('\nLayout & Spacing:'));
    const layoutTable = new Table([
      { header: 'Setting', key: 'setting', width: 20 },
      { header: 'Value', key: 'value', width: 30 },
      { header: 'Description', key: 'description', width: 40 }
    ]);
    
    layoutTable.addRow({
      setting: 'Density',
      value: `${prefs.density} ${prefs.compactMode ? '(compact mode)' : ''}`,
      description: 'Information density and spacing'
    });
    
    layoutTable.addRow({
      setting: 'Indent Size',
      value: `${prefs.indentSize} spaces`,
      description: 'Indentation for nested content'
    });
    
    layoutTable.addRow({
      setting: 'Max Width',
      value: `${prefs.maxWidth} characters`,
      description: 'Maximum width for formatted output'
    });
    
    console.log(layoutTable.render());
    
    // Visual elements section
    console.log(chalk.yellow.bold('\nVisual Elements:'));
    const elementsTable = new Table([
      { header: 'Setting', key: 'setting', width: 20 },
      { header: 'Value', key: 'value', width: 30 },
      { header: 'Description', key: 'description', width: 40 }
    ]);
    
    elementsTable.addRow({
      setting: 'Icons',
      value: prefs.showIcons ? 'Enabled' : 'Disabled',
      description: 'Unicode icons and symbols'
    });
    
    elementsTable.addRow({
      setting: 'Borders',
      value: prefs.showBorders ? 'Enabled' : 'Disabled',
      description: 'Table borders and separators'
    });
    
    elementsTable.addRow({
      setting: 'Rounded Corners',
      value: prefs.roundedCorners ? 'Enabled' : 'Disabled',
      description: 'Rounded corners for boxes'
    });
    
    console.log(elementsTable.render());
    
    // Accessibility section
    console.log(chalk.yellow.bold('\nAccessibility:'));
    const accessibilityTable = new Table([
      { header: 'Setting', key: 'setting', width: 20 },
      { header: 'Value', key: 'value', width: 30 },
      { header: 'Description', key: 'description', width: 40 }
    ]);
    
    accessibilityTable.addRow({
      setting: 'Large Text',
      value: prefs.largeText ? 'Enabled' : 'Disabled',
      description: 'Increased text size and spacing'
    });
    
    accessibilityTable.addRow({
      setting: 'Screen Reader',
      value: prefs.screenReaderMode ? 'Enabled' : 'Disabled',
      description: 'Screen reader optimized output'
    });
    
    accessibilityTable.addRow({
      setting: 'Fallback Mode',
      value: prefs.fallbackMode ? 'Enabled' : 'Disabled',
      description: 'Basic terminal compatibility mode'
    });
    
    console.log(accessibilityTable.render());
    
    console.log(chalk.gray('\nUse "kira config visual set <setting> <value>" to change settings'));
    console.log(chalk.gray('Use "kira config visual reset" to restore defaults\n'));
  }
  
  /**
   * Set a specific preference value
   */
  public static setPreference(setting: string, value: string): boolean {
    const prefs = visualPreferences.getPreferences();
    const updates: Partial<VisualPreferences> = {};
    
    try {
      switch (setting.toLowerCase()) {
        case 'theme':
          if (['auto', 'default', 'dark', 'light', 'high-contrast', 'minimal'].includes(value)) {
            updates.theme = value as any;
          } else {
            throw new Error(`Invalid theme: ${value}. Valid options: auto, default, dark, light, high-contrast, minimal`);
          }
          break;
          
        case 'autodetect':
        case 'auto-detect':
          updates.autoDetect = this.parseBoolean(value);
          break;
          
        case 'forcecolor':
        case 'force-color':
          updates.forceColor = this.parseBoolean(value);
          break;
          
        case 'animations':
          updates.animations = this.parseBoolean(value);
          break;
          
        case 'animationspeed':
        case 'animation-speed':
          if (['slow', 'normal', 'fast'].includes(value)) {
            updates.animationSpeed = value as any;
          } else {
            throw new Error(`Invalid animation speed: ${value}. Valid options: slow, normal, fast`);
          }
          break;
          
        case 'progressstyle':
        case 'progress-style':
          if (['bar', 'spinner', 'dots', 'minimal'].includes(value)) {
            updates.progressStyle = value as any;
          } else {
            throw new Error(`Invalid progress style: ${value}. Valid options: bar, spinner, dots, minimal`);
          }
          break;
          
        case 'compactmode':
        case 'compact-mode':
        case 'compact':
          updates.compactMode = this.parseBoolean(value);
          break;
          
        case 'density':
          if (['comfortable', 'normal', 'compact'].includes(value)) {
            updates.density = value as any;
          } else {
            throw new Error(`Invalid density: ${value}. Valid options: comfortable, normal, compact`);
          }
          break;
          
        case 'indentsize':
        case 'indent-size':
        case 'indent':
          const indentSize = parseInt(value);
          if (isNaN(indentSize) || indentSize < 0 || indentSize > 8) {
            throw new Error(`Invalid indent size: ${value}. Must be a number between 0 and 8`);
          }
          updates.indentSize = indentSize;
          break;
          
        case 'maxwidth':
        case 'max-width':
        case 'width':
          const maxWidth = parseInt(value);
          if (isNaN(maxWidth) || maxWidth < 40 || maxWidth > 200) {
            throw new Error(`Invalid max width: ${value}. Must be a number between 40 and 200`);
          }
          updates.maxWidth = maxWidth;
          break;
          
        case 'showicons':
        case 'show-icons':
        case 'icons':
          updates.showIcons = this.parseBoolean(value);
          break;
          
        case 'showborders':
        case 'show-borders':
        case 'borders':
          updates.showBorders = this.parseBoolean(value);
          break;
          
        case 'roundedcorners':
        case 'rounded-corners':
        case 'rounded':
          updates.roundedCorners = this.parseBoolean(value);
          break;
          
        case 'highcontrast':
        case 'high-contrast':
          updates.highContrast = this.parseBoolean(value);
          break;
          
        case 'reducedmotion':
        case 'reduced-motion':
          updates.reducedMotion = this.parseBoolean(value);
          break;
          
        case 'largetext':
        case 'large-text':
          updates.largeText = this.parseBoolean(value);
          break;
          
        case 'screenreader':
        case 'screen-reader':
          updates.screenReaderMode = this.parseBoolean(value);
          break;
          
        case 'fallback':
        case 'fallbackmode':
        case 'fallback-mode':
          updates.fallbackMode = this.parseBoolean(value);
          break;
          
        default:
          throw new Error(`Unknown setting: ${setting}`);
      }
      
      visualPreferences.updatePreferences(updates);
      StatusIndicator.success(`Updated ${setting} to ${value}`);
      return true;
      
    } catch (error) {
      StatusIndicator.error(`Failed to set ${setting}: ${error instanceof Error ? error.message : error}`);
      return false;
    }
  }
  
  /**
   * Reset preferences to defaults
   */
  public static resetPreferences(): void {
    visualPreferences.resetToDefaults();
    StatusIndicator.success('Visual preferences reset to defaults');
  }
  
  /**
   * Show available themes with preview
   */
  public static showAvailableThemes(): void {
    console.log(chalk.cyan.bold('\n🎨 Available Themes\n'));
    
    const themes = themeManager.getAvailableThemes();
    const currentTheme = themeManager.getCurrentTheme().name;
    
    themes.forEach(themeName => {
      const theme = themeManager.getTheme(themeName);
      if (theme) {
        const isCurrent = themeName === currentTheme;
        const marker = isCurrent ? '●' : '○';
        
        console.log(`${marker} ${chalk.bold(theme.name)} ${isCurrent ? chalk.green('(current)') : ''}`);
        console.log(`  ${theme.description}`);
        
        // Show color preview
        const colors = theme.colors;
        console.log(`  Preview: ${colors.success('success')} ${colors.error('error')} ${colors.warning('warning')} ${colors.info('info')}`);
        console.log();
      }
    });
    
    console.log(chalk.gray('Use "kira config visual set theme <name>" to change theme\n'));
  }
  
  /**
   * Export preferences to a file
   */
  public static exportPreferences(filePath?: string): void {
    const prefs = visualPreferences.exportPreferences();
    const exportPath = filePath || './kira-visual-preferences.json';
    
    try {
      const fs = require('fs');
      fs.writeFileSync(exportPath, JSON.stringify(prefs, null, 2));
      StatusIndicator.success(`Preferences exported to ${exportPath}`);
    } catch (error) {
      StatusIndicator.error(`Failed to export preferences: ${error instanceof Error ? error.message : error}`);
    }
  }
  
  /**
   * Import preferences from a file
   */
  public static importPreferences(filePath: string): void {
    try {
      const fs = require('fs');
      const data = fs.readFileSync(filePath, 'utf8');
      const prefs = JSON.parse(data);
      
      visualPreferences.importPreferences(prefs);
      StatusIndicator.success(`Preferences imported from ${filePath}`);
    } catch (error) {
      StatusIndicator.error(`Failed to import preferences: ${error instanceof Error ? error.message : error}`);
    }
  }
  
  /**
   * Show quick setup wizard
   */
  public static showQuickSetup(): void {
    console.log(chalk.cyan.bold('\n🚀 Quick Visual Setup\n'));
    
    console.log(chalk.yellow('Choose a preset configuration:\n'));
    
    console.log('1. ' + chalk.bold('Default') + ' - Balanced colors and animations');
    console.log('   Theme: auto, Animations: enabled, Density: normal\n');
    
    console.log('2. ' + chalk.bold('Minimal') + ' - Clean and simple');
    console.log('   Theme: minimal, Animations: disabled, Compact: enabled\n');
    
    console.log('3. ' + chalk.bold('Accessible') + ' - High contrast and screen reader friendly');
    console.log('   Theme: high-contrast, Large text: enabled, Reduced motion: enabled\n');
    
    console.log('4. ' + chalk.bold('Performance') + ' - Fast and lightweight');
    console.log('   Animations: disabled, Fallback mode: enabled, Minimal icons\n');
    
    console.log(chalk.gray('Use "kira config visual preset <number>" to apply a preset'));
    console.log(chalk.gray('Use "kira config visual" to see current settings\n'));
  }
  
  /**
   * Apply a preset configuration
   */
  public static applyPreset(presetName: string): boolean {
    const presets: Record<string, Partial<VisualPreferences>> = {
      '1': {
        theme: 'auto',
        animations: true,
        animationSpeed: 'normal',
        density: 'normal',
        compactMode: false,
        showIcons: true,
        highContrast: false,
        reducedMotion: false,
        largeText: false,
        fallbackMode: false
      },
      'default': {
        theme: 'auto',
        animations: true,
        animationSpeed: 'normal',
        density: 'normal',
        compactMode: false,
        showIcons: true,
        highContrast: false,
        reducedMotion: false,
        largeText: false,
        fallbackMode: false
      },
      '2': {
        theme: 'minimal',
        animations: false,
        compactMode: true,
        density: 'compact',
        showIcons: false,
        showBorders: false,
        fallbackMode: true
      },
      'minimal': {
        theme: 'minimal',
        animations: false,
        compactMode: true,
        density: 'compact',
        showIcons: false,
        showBorders: false,
        fallbackMode: true
      },
      '3': {
        theme: 'high-contrast',
        highContrast: true,
        largeText: true,
        reducedMotion: true,
        animations: false,
        density: 'comfortable',
        screenReaderMode: false
      },
      'accessible': {
        theme: 'high-contrast',
        highContrast: true,
        largeText: true,
        reducedMotion: true,
        animations: false,
        density: 'comfortable',
        screenReaderMode: false
      },
      '4': {
        animations: false,
        fallbackMode: true,
        showIcons: false,
        compactMode: true,
        density: 'compact',
        progressStyle: 'minimal'
      },
      'performance': {
        animations: false,
        fallbackMode: true,
        showIcons: false,
        compactMode: true,
        density: 'compact',
        progressStyle: 'minimal'
      }
    };
    
    const preset = presets[presetName.toLowerCase()];
    if (preset) {
      visualPreferences.updatePreferences(preset);
      StatusIndicator.success(`Applied ${presetName} preset`);
      return true;
    } else {
      StatusIndicator.error(`Unknown preset: ${presetName}. Available: default, minimal, accessible, performance`);
      return false;
    }
  }
  
  /**
   * Parse boolean value from string
   */
  private static parseBoolean(value: string): boolean {
    const lowerValue = value.toLowerCase();
    if (['true', '1', 'yes', 'on', 'enable', 'enabled'].includes(lowerValue)) {
      return true;
    } else if (['false', '0', 'no', 'off', 'disable', 'disabled'].includes(lowerValue)) {
      return false;
    } else {
      throw new Error(`Invalid boolean value: ${value}. Use true/false, yes/no, on/off, or enable/disable`);
    }
  }
}