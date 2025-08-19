import chalk from 'chalk';
import { Theme } from './ThemeManager.js';

/**
 * Dark theme - optimized for dark terminal backgrounds
 * Uses brighter colors for better visibility on dark backgrounds
 */
export function createDarkTheme(): Theme {
  return {
    name: 'dark',
    description: 'Dark theme optimized for dark terminal backgrounds',
    colors: {
      primary: chalk.cyanBright.bold,
      secondary: chalk.blueBright,
      tertiary: chalk.blue,
      
      success: chalk.greenBright.bold,
      error: chalk.redBright.bold,
      warning: chalk.yellowBright.bold,
      info: chalk.blueBright.bold,
      
      muted: chalk.gray,
      accent: chalk.magentaBright,
      highlight: chalk.bgYellowBright.black,
      border: chalk.gray,
      background: chalk.reset,
      
      text: chalk.whiteBright,
      textSecondary: chalk.white,
      textMuted: chalk.gray,
      
      link: chalk.blueBright.underline,
      button: chalk.bgBlueBright.black,
      input: chalk.bgWhite.black,
      
      code: chalk.bgBlack.whiteBright,
      codeBackground: chalk.bgBlack,
      keyword: chalk.magentaBright,
      string: chalk.greenBright,
      number: chalk.yellowBright,
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
      isDark: true,
      isHighContrast: false,
      supportsColor: chalk.level > 0,
      supports256Color: chalk.level >= 2,
      supportsTrueColor: chalk.level >= 3
    }
  };
}