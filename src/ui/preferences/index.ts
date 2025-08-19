/**
 * Visual Preferences Module
 * 
 * This module provides comprehensive visual customization and configuration
 * for the Kira CLI interface, including theme management, layout preferences,
 * accessibility options, and animation settings.
 */

// Core preferences
export {
  VisualPreferences,
  VisualPreferencesManager,
  DEFAULT_VISUAL_PREFERENCES,
  visualPreferences,
  getVisualPreferences,
  updateVisualPreferences,
  shouldShowAnimations,
  shouldShowIcons,
  shouldUseColors
} from './VisualPreferences.js';

// Configuration interface
export { PreferencesConfig } from './PreferencesConfig.js';

// Re-export theme-related functionality for convenience
export {
  ThemePreferences,
  themeManager,
  getCurrentTheme,
  setTheme,
  getThemeColors,
  getThemeStyles
} from '../themes/ThemeManager.js';