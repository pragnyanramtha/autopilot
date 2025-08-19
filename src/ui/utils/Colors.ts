import chalk, { ChalkInstance } from 'chalk';

export interface ColorTheme {
  primary: ChalkInstance;
  secondary: ChalkInstance;
  success: ChalkInstance;
  error: ChalkInstance;
  warning: ChalkInstance;
  info: ChalkInstance;
  muted: ChalkInstance;
  accent: ChalkInstance;
  highlight: ChalkInstance;
}

export interface TextStyles {
  bold: ChalkInstance;
  dim: ChalkInstance;
  italic: ChalkInstance;
  underline: ChalkInstance;
  strikethrough: ChalkInstance;
}

// Enhanced terminal color capabilities detection
export function detectColorSupport(): {
  hasColor: boolean;
  has256Color: boolean;
  hasTrueColor: boolean;
  isHighContrast: boolean;
  terminalType: string;
  platform: string;
} {
  const hasColor = chalk.level > 0;
  const has256Color = chalk.level >= 2;
  const hasTrueColor = chalk.level >= 3;
  
  // Detect high contrast mode
  const isHighContrast = process.env.FORCE_HIGH_CONTRAST === 'true' ||
    process.env.TERM === 'linux' ||
    process.env.COLORTERM === 'monochrome' ||
    (process.platform === 'win32' && !process.env.WT_SESSION);
  
  // Detect terminal type for better compatibility
  const termProgram = process.env.TERM_PROGRAM || '';
  const term = process.env.TERM || '';
  let terminalType = 'unknown';
  
  if (termProgram.includes('iTerm')) terminalType = 'iterm';
  else if (termProgram.includes('Terminal')) terminalType = 'terminal';
  else if (termProgram.includes('Hyper')) terminalType = 'hyper';
  else if (process.env.WT_SESSION) terminalType = 'windows-terminal';
  else if (term.includes('xterm')) terminalType = 'xterm';
  else if (term.includes('screen')) terminalType = 'screen';
  else if (term.includes('tmux')) terminalType = 'tmux';
  else if (process.platform === 'win32') terminalType = 'cmd';

  return {
    hasColor,
    has256Color,
    hasTrueColor,
    isHighContrast,
    terminalType,
    platform: process.platform
  };
}

// Default theme with vibrant colors
export const defaultTheme: ColorTheme = {
  primary: chalk.cyan.bold,
  secondary: chalk.blue,
  success: chalk.green.bold,
  error: chalk.red.bold,
  warning: chalk.yellow.bold,
  info: chalk.blue.bold,
  muted: chalk.gray,
  accent: chalk.magenta,
  highlight: chalk.bgYellow.black
};

// Dark theme optimized for dark terminals
export const darkTheme: ColorTheme = {
  primary: chalk.cyanBright.bold,
  secondary: chalk.blueBright,
  success: chalk.greenBright.bold,
  error: chalk.redBright.bold,
  warning: chalk.yellowBright.bold,
  info: chalk.blueBright.bold,
  muted: chalk.gray,
  accent: chalk.magentaBright,
  highlight: chalk.bgYellowBright.black
};

// Light theme optimized for light terminals
export const lightTheme: ColorTheme = {
  primary: chalk.cyan,
  secondary: chalk.blue,
  success: chalk.green,
  error: chalk.red,
  warning: chalk.yellow,
  info: chalk.blue,
  muted: chalk.blackBright,
  accent: chalk.magenta,
  highlight: chalk.bgYellow.black
};

// High contrast theme for accessibility
export const highContrastTheme: ColorTheme = {
  primary: chalk.white.bold,
  secondary: chalk.white,
  success: chalk.black.bgGreen.bold,
  error: chalk.white.bgRed.bold,
  warning: chalk.black.bgYellow.bold,
  info: chalk.white.bgBlue.bold,
  muted: chalk.gray,
  accent: chalk.white.bold,
  highlight: chalk.black.bgWhite
};

// Color-blind friendly theme (Deuteranopia/Protanopia safe)
export const colorBlindFriendlyTheme: ColorTheme = {
  primary: chalk.blue.bold,        // Blue is safe for most color blindness
  secondary: chalk.cyan,           // Cyan is distinguishable
  success: chalk.blue.bold,        // Use blue instead of green
  error: chalk.magenta.bold,       // Use magenta instead of red
  warning: chalk.yellow.bold,      // Yellow is generally safe
  info: chalk.cyan.bold,           // Cyan for info
  muted: chalk.gray,
  accent: chalk.white.bold,        // High contrast white
  highlight: chalk.bgYellow.black  // Yellow background is safe
};

// Monochrome theme for terminals without color support
export const monochromeTheme: ColorTheme = {
  primary: chalk.bold,
  secondary: chalk.dim,
  success: chalk.bold,
  error: chalk.inverse,
  warning: chalk.underline,
  info: chalk.italic,
  muted: chalk.dim,
  accent: chalk.bold,
  highlight: chalk.inverse
};

// Enhanced high contrast theme with better accessibility
export const enhancedHighContrastTheme: ColorTheme = {
  primary: chalk.black.bgWhite.bold,
  secondary: chalk.white.bgBlack,
  success: chalk.black.bgGreen.bold,
  error: chalk.white.bgRed.bold,
  warning: chalk.black.bgYellow.bold,
  info: chalk.white.bgBlue.bold,
  muted: chalk.white.dim,
  accent: chalk.black.bgCyan.bold,
  highlight: chalk.white.bgMagenta.bold
};

// Text styling utilities
export const styles: TextStyles = {
  bold: chalk.bold,
  dim: chalk.dim,
  italic: chalk.italic,
  underline: chalk.underline,
  strikethrough: chalk.strikethrough
};

// Import the new theme manager
import { themeManager, getCurrentTheme } from '../themes/ThemeManager.js';

// Legacy support - map new theme to old ColorTheme interface
function mapThemeToColorTheme(): ColorTheme {
  const theme = getCurrentTheme();
  return {
    primary: theme.colors.primary,
    secondary: theme.colors.secondary,
    success: theme.colors.success,
    error: theme.colors.error,
    warning: theme.colors.warning,
    info: theme.colors.info,
    muted: theme.colors.muted,
    accent: theme.colors.accent,
    highlight: theme.colors.highlight
  };
}

// Current active theme (legacy support)
let currentTheme: ColorTheme = mapThemeToColorTheme();

export function setTheme(theme: ColorTheme): void {
  currentTheme = theme;
}

export function getTheme(): ColorTheme {
  return mapThemeToColorTheme();
}

// Auto-detect and set appropriate theme based on environment
export function autoDetectTheme(): ColorTheme {
  const support = detectColorSupport();
  
  // Check for accessibility preferences
  if (process.env.FORCE_HIGH_CONTRAST === 'true' || support.isHighContrast) {
    return enhancedHighContrastTheme;
  }
  
  // Check for color-blind friendly mode
  if (process.env.COLOR_BLIND_FRIENDLY === 'true') {
    return colorBlindFriendlyTheme;
  }
  
  // Check if colors are supported at all
  if (!support.hasColor) {
    return monochromeTheme;
  }
  
  // Use theme manager for modern terminals
  return mapThemeToColorTheme();
}

// Get theme based on specific accessibility needs
export function getAccessibilityTheme(type: 'high-contrast' | 'color-blind' | 'monochrome'): ColorTheme {
  switch (type) {
    case 'high-contrast':
      return enhancedHighContrastTheme;
    case 'color-blind':
      return colorBlindFriendlyTheme;
    case 'monochrome':
      return monochromeTheme;
    default:
      return defaultTheme;
  }
}

// Utility functions for common color operations using the theme manager
export const colors = {
  // Status colors
  success: (text: string) => getCurrentTheme().colors.success(text),
  error: (text: string) => getCurrentTheme().colors.error(text),
  warning: (text: string) => getCurrentTheme().colors.warning(text),
  info: (text: string) => getCurrentTheme().colors.info(text),
  
  // Semantic colors
  primary: (text: string) => getCurrentTheme().colors.primary(text),
  secondary: (text: string) => getCurrentTheme().colors.secondary(text),
  muted: (text: string) => getCurrentTheme().colors.muted(text),
  accent: (text: string) => getCurrentTheme().colors.accent(text),
  highlight: (text: string) => getCurrentTheme().colors.highlight(text),
  
  // Text colors
  text: (text: string) => getCurrentTheme().colors.text(text),
  textSecondary: (text: string) => getCurrentTheme().colors.textSecondary(text),
  textMuted: (text: string) => getCurrentTheme().colors.textMuted(text),
  
  // Interactive colors
  link: (text: string) => getCurrentTheme().colors.link(text),
  button: (text: string) => getCurrentTheme().colors.button(text),
  input: (text: string) => getCurrentTheme().colors.input(text),
  
  // Text styles
  bold: (text: string) => getCurrentTheme().styles.bold(text),
  dim: (text: string) => getCurrentTheme().styles.dim(text),
  italic: (text: string) => getCurrentTheme().styles.italic(text),
  underline: (text: string) => getCurrentTheme().styles.underline(text),
  
  // Combinations
  successBold: (text: string) => getCurrentTheme().colors.success(getCurrentTheme().styles.bold(text)),
  errorBold: (text: string) => getCurrentTheme().colors.error(getCurrentTheme().styles.bold(text)),
  warningBold: (text: string) => getCurrentTheme().colors.warning(getCurrentTheme().styles.bold(text)),
  infoBold: (text: string) => getCurrentTheme().colors.info(getCurrentTheme().styles.bold(text)),
  primaryBold: (text: string) => getCurrentTheme().colors.primary(getCurrentTheme().styles.bold(text)),
  
  // Special formatting
  code: (text: string) => getCurrentTheme().colors.code(` ${text} `),
  path: (text: string) => getCurrentTheme().colors.accent(text),
  url: (text: string) => getCurrentTheme().colors.link(text),
  command: (text: string) => getCurrentTheme().colors.code(` ${text} `),
  
  // Reset
  reset: chalk.reset
};

// Platform-specific color adjustments
export function getPlatformOptimizedTheme(): ColorTheme {
  const support = detectColorSupport();
  const baseTheme = autoDetectTheme();
  
  // Windows-specific adjustments
  if (support.platform === 'win32') {
    // Windows Command Prompt has limited color support
    if (support.terminalType === 'cmd') {
      return {
        ...baseTheme,
        primary: chalk.white.bold,
        success: chalk.green,
        error: chalk.red,
        warning: chalk.yellow,
        info: chalk.cyan
      };
    }
  }
  
  // macOS Terminal.app adjustments
  if (support.platform === 'darwin' && support.terminalType === 'terminal') {
    return {
      ...baseTheme,
      // Terminal.app has good color support, use brighter variants
      primary: chalk.cyanBright.bold,
      accent: chalk.magentaBright
    };
  }
  
  // Linux console adjustments
  if (support.platform === 'linux' && support.terminalType === 'unknown') {
    return {
      ...baseTheme,
      // Conservative colors for basic Linux console
      primary: chalk.white.bold,
      secondary: chalk.white,
      accent: chalk.yellow.bold
    };
  }
  
  return baseTheme;
}

// Validate color output for accessibility
export function validateColorContrast(foreground: string, background: string): boolean {
  // Simple validation - in a real implementation, you'd calculate actual contrast ratios
  // This is a placeholder for accessibility validation
  const darkColors = ['black', 'red', 'green', 'blue', 'magenta'];
  const lightColors = ['white', 'yellow', 'cyan', 'gray'];
  
  const fgIsDark = darkColors.some(color => foreground.includes(color));
  const bgIsLight = lightColors.some(color => background.includes(color));
  
  return fgIsDark !== bgIsLight; // Good contrast if one is dark and one is light
}

// Color testing utilities
export function testColorSupport(): void {
  const support = detectColorSupport();
  console.log('Color Support Detection:');
  console.log(`  Platform: ${support.platform}`);
  console.log(`  Terminal: ${support.terminalType}`);
  console.log(`  Has Color: ${support.hasColor}`);
  console.log(`  256 Colors: ${support.has256Color}`);
  console.log(`  True Color: ${support.hasTrueColor}`);
  console.log(`  High Contrast: ${support.isHighContrast}`);
  
  console.log('\nColor Theme Test:');
  const theme = getPlatformOptimizedTheme();
  console.log(theme.success('✓ Success'));
  console.log(theme.error('✗ Error'));
  console.log(theme.warning('⚠ Warning'));
  console.log(theme.info('ℹ Info'));
  console.log(theme.primary('Primary'));
  console.log(theme.secondary('Secondary'));
}

// Initialize theme on import
setTheme(getPlatformOptimizedTheme());