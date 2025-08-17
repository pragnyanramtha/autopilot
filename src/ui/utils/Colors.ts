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

// Detect terminal color capabilities
export function detectColorSupport(): {
  hasColor: boolean;
  has256Color: boolean;
  hasTrueColor: boolean;
} {
  const hasColor = chalk.level > 0;
  const has256Color = chalk.level >= 2;
  const hasTrueColor = chalk.level >= 3;

  return {
    hasColor,
    has256Color,
    hasTrueColor
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

// Text styling utilities
export const styles: TextStyles = {
  bold: chalk.bold,
  dim: chalk.dim,
  italic: chalk.italic,
  underline: chalk.underline,
  strikethrough: chalk.strikethrough
};

// Current active theme
let currentTheme: ColorTheme = defaultTheme;

export function setTheme(theme: ColorTheme): void {
  currentTheme = theme;
}

export function getTheme(): ColorTheme {
  return currentTheme;
}

// Auto-detect and set appropriate theme
export function autoDetectTheme(): ColorTheme {
  const colorSupport = detectColorSupport();
  
  if (!colorSupport.hasColor) {
    // Fallback to no colors
    return Object.keys(defaultTheme).reduce((theme, key) => {
      theme[key as keyof ColorTheme] = chalk.reset;
      return theme;
    }, {} as ColorTheme);
  }

  // For now, use default theme
  // In the future, we could detect terminal background color
  return defaultTheme;
}

// Utility functions for common color operations
export const colors = {
  // Status colors
  success: (text: string) => currentTheme.success(text),
  error: (text: string) => currentTheme.error(text),
  warning: (text: string) => currentTheme.warning(text),
  info: (text: string) => currentTheme.info(text),
  
  // Semantic colors
  primary: (text: string) => currentTheme.primary(text),
  secondary: (text: string) => currentTheme.secondary(text),
  muted: (text: string) => currentTheme.muted(text),
  accent: (text: string) => currentTheme.accent(text),
  highlight: (text: string) => currentTheme.highlight(text),
  
  // Text styles
  bold: (text: string) => styles.bold(text),
  dim: (text: string) => styles.dim(text),
  italic: (text: string) => styles.italic(text),
  underline: (text: string) => styles.underline(text),
  
  // Combinations
  successBold: (text: string) => currentTheme.success(styles.bold(text)),
  errorBold: (text: string) => currentTheme.error(styles.bold(text)),
  warningBold: (text: string) => currentTheme.warning(styles.bold(text)),
  infoBold: (text: string) => currentTheme.info(styles.bold(text)),
  primaryBold: (text: string) => currentTheme.primary(styles.bold(text)),
  
  // Special formatting
  code: (text: string) => chalk.bgBlackBright.white(` ${text} `),
  path: (text: string) => currentTheme.accent(text),
  url: (text: string) => currentTheme.info(styles.underline(text)),
  command: (text: string) => chalk.bgBlack.white(` ${text} `),
  
  // Reset
  reset: chalk.reset
};

// Initialize theme on import
setTheme(autoDetectTheme());