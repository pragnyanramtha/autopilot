// Export all theme-related functionality
export { 
  Theme, 
  ThemePreferences, 
  ThemeManager, 
  themeManager,
  getCurrentTheme,
  setTheme,
  getThemeColors,
  getThemeStyles
} from './ThemeManager.js';

export { createDefaultTheme } from './DefaultTheme.js';
export { createDarkTheme } from './DarkTheme.js';
export { createLightTheme } from './LightTheme.js';