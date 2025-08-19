import chalk from 'chalk';
import { Theme } from './ThemeManager.js';

/**
 * Default theme - vibrant colors that work well on both dark and light backgrounds
 * This is the primary theme for Kira CLI
 */
export function createDefaultTheme(): Theme {
  return {
    name: 'default',
    description: 'Default vibrant theme optimized for most terminals',
    colors: {
      primary: chalk.cyan.bold,
      secondary: chalk.blue,
      tertiary: chalk.blueBright,
      
      success: chalk.green.bold,
      error: chalk.red.bold,
      warning: chalk.yellow.bold,
      info: chalk.blue.bold,
      
      muted: chalk.gray,
      accent: chalk.magenta,
      highlight: chalk.bgYellow.black,
      border: chalk.gray,
      background: chalk.reset,
      
      text: chalk.white,
      textSecondary: chalk.gray,
      textMuted: chalk.blackBright,
      
      link: chalk.blue.underline,
      button: chalk.bgBlue.white,
      input: chalk.bgBlackBright.white,
      
      code: chalk.bgBlackBright.white,
      codeBackground: chalk.bgBlack,
      keyword: chalk.magenta,
      string: chalk.green,
      number: chalk.yellow,
      comment: chalk.gray
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