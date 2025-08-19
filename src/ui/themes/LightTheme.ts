import chalk from 'chalk';
import { Theme } from './ThemeManager.js';

/**
 * Light theme - optimized for light terminal backgrounds
 * Uses darker colors for better visibility on light backgrounds
 */
export function createLightTheme(): Theme {
  return {
    name: 'light',
    description: 'Light theme optimized for light terminal backgrounds',
    colors: {
      primary: chalk.blue.bold,
      secondary: chalk.blueBright,
      tertiary: chalk.cyan,
      
      success: chalk.green.bold,
      error: chalk.red.bold,
      warning: chalk.yellow.bold,
      info: chalk.blue.bold,
      
      muted: chalk.blackBright,
      accent: chalk.magenta,
      highlight: chalk.bgBlue.white,
      border: chalk.blackBright,
      background: chalk.reset,
      
      text: chalk.black,
      textSecondary: chalk.blackBright,
      textMuted: chalk.gray,
      
      link: chalk.blue.underline,
      button: chalk.bgBlue.white,
      input: chalk.bgBlackBright.white,
      
      code: chalk.bgBlackBright.white,
      codeBackground: chalk.bgBlackBright,
      keyword: chalk.magenta,
      string: chalk.green,
      number: chalk.yellow,
      comment: chalk.blackBright
    },
    styles: {
      bold: chalk.bold,
      dim: chalk.dim,
      italic: chalk.italic,
      underline: chalk.underline,
      strikethrough: chalk.strikethrough,
      inverse: chalk.inverse
    },
    metadata: {
      isDark: false,
      isHighContrast: false,
      supportsColor: chalk.level > 0,
      supports256Color: chalk.level >= 2,
      supportsTrueColor: chalk.level >= 3
    }
  };
}