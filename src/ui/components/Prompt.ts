import { input as inquirerInput, select as inquirerSelect, checkbox as inquirerCheckbox, confirm as inquirerConfirm, password as inquirerPassword } from '@inquirer/prompts';
import { colors } from '../utils/Colors.js';
import { symbols } from '../utils/Symbols.js';
import { Layout } from '../utils/Layout.js';
import { getCurrentTheme } from '../themes/ThemeManager.js';

export interface PromptOptions {
  message: string;
  default?: string;
  required?: boolean;
  validate?: (input: string) => boolean | string;
  transform?: (input: string) => string;
  mask?: boolean; // For password inputs
  prefix?: string;
  suffix?: string;
}

export interface ChoiceOption {
  name: string;
  value: any;
  description?: string;
  disabled?: boolean;
  hint?: string;
}

export interface MultiChoiceOptions {
  message: string;
  choices: ChoiceOption[];
  default?: number;
  pageSize?: number;
  loop?: boolean;
  prefix?: string;
}

export interface ConfirmOptions {
  message: string;
  default?: boolean;
  prefix?: string;
}

export interface ValidationResult {
  isValid: boolean;
  message?: string;
}

export class Prompt {
  private theme = getCurrentTheme();

  constructor() {
    // No need for readline interface with inquirer
  }

  /**
   * Basic text input prompt with validation and visual feedback
   */
  async input(options: PromptOptions): Promise<string> {
    const { message, default: defaultValue, required = false, validate, transform, prefix } = options;
    
    // Create styled message with prefix
    const promptPrefix = prefix || this.theme.colors.info(symbols.question);
    const styledMessage = `${promptPrefix} ${this.theme.colors.text(message)}`;
    
    try {
      const result = await inquirerInput({
        message: styledMessage,
        default: defaultValue,
        required,
        validate: validate ? (input: string) => {
          if (required && !input.trim()) {
            return this.theme.colors.error('This field is required');
          }
          const validationResult = validate(input);
          if (validationResult !== true) {
            const errorMessage = typeof validationResult === 'string' ? validationResult : 'Invalid input';
            return this.theme.colors.error(errorMessage);
          }
          return true;
        } : undefined
      });
      
      return transform ? transform(result) : result;
    } catch (error) {
      throw new Error('Input cancelled');
    }
  }

  /**
   * Multi-choice selection with highlighting and navigation
   */
  async select(options: MultiChoiceOptions): Promise<any> {
    const { message, choices, default: defaultIndex = 0, prefix } = options;
    
    const promptPrefix = prefix || this.theme.colors.info(symbols.question);
    const styledMessage = `${promptPrefix} ${this.theme.colors.text(message)}`;
    
    // Convert our choice format to inquirer format
    const inquirerChoices = choices.map((choice, index) => ({
      name: choice.description ? 
        `${choice.name} ${this.theme.colors.muted(`- ${choice.description}`)}` : 
        choice.name,
      value: choice.value,
      disabled: choice.disabled
    }));
    
    try {
      return await inquirerSelect({
        message: styledMessage,
        choices: inquirerChoices,
        default: choices[defaultIndex]?.value
      });
    } catch (error) {
      throw new Error('Selection cancelled');
    }
  }

  /**
   * Confirmation dialog with clear visual options
   */
  async confirm(options: ConfirmOptions): Promise<boolean> {
    const { message, default: defaultValue = false, prefix } = options;
    
    const promptPrefix = prefix || this.theme.colors.info(symbols.question);
    const styledMessage = `${promptPrefix} ${this.theme.colors.text(message)}`;
    
    try {
      return await inquirerConfirm({
        message: styledMessage,
        default: defaultValue
      });
    } catch (error) {
      throw new Error('Confirmation cancelled');
    }
  }

  /**
   * Multi-select checkbox prompt
   */
  async checkbox(options: MultiChoiceOptions): Promise<any[]> {
    const { message, choices, prefix } = options;
    
    const promptPrefix = prefix || this.theme.colors.info(symbols.question);
    const styledMessage = `${promptPrefix} ${this.theme.colors.text(message)}`;
    
    // Convert our choice format to inquirer format
    const inquirerChoices = choices.map(choice => ({
      name: choice.description ? 
        `${choice.name} ${this.theme.colors.muted(`- ${choice.description}`)}` : 
        choice.name,
      value: choice.value,
      disabled: choice.disabled,
      checked: false
    }));
    
    try {
      return await inquirerCheckbox({
        message: styledMessage,
        choices: inquirerChoices
      });
    } catch (error) {
      throw new Error('Selection cancelled');
    }
  }

  /**
   * Password input with masking
   */
  async password(options: Omit<PromptOptions, 'mask'>): Promise<string> {
    const { message, required = false, validate, prefix } = options;
    
    const promptPrefix = prefix || this.theme.colors.info(symbols.question);
    const styledMessage = `${promptPrefix} ${this.theme.colors.text(message)}`;
    
    try {
      return await inquirerPassword({
        message: styledMessage,
        validate: validate ? (input: string) => {
          if (required && !input.trim()) {
            return this.theme.colors.error('This field is required');
          }
          const validationResult = validate(input);
          if (validationResult !== true) {
            const errorMessage = typeof validationResult === 'string' ? validationResult : 'Invalid input';
            return this.theme.colors.error(errorMessage);
          }
          return true;
        } : undefined
      });
    } catch (error) {
      throw new Error('Password input cancelled');
    }
  }

  /**
   * Number input with validation
   */
  async number(options: Omit<PromptOptions, 'validate'> & {
    min?: number;
    max?: number;
    integer?: boolean;
  }): Promise<number> {
    const { min, max, integer = false, ...promptOptions } = options;
    
    const validate = (input: string): boolean | string => {
      const num = parseFloat(input);
      
      if (isNaN(num)) {
        return 'Please enter a valid number';
      }
      
      if (integer && !Number.isInteger(num)) {
        return 'Please enter a whole number';
      }
      
      if (min !== undefined && num < min) {
        return `Number must be at least ${min}`;
      }
      
      if (max !== undefined && num > max) {
        return `Number must be at most ${max}`;
      }
      
      return true;
    };

    const result = await this.input({ ...promptOptions, validate });
    return parseFloat(result);
  }

  /**
   * Email input with validation
   */
  async email(options: Omit<PromptOptions, 'validate'>): Promise<string> {
    const validate = (input: string): boolean | string => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(input) || 'Please enter a valid email address';
    };

    return this.input({ ...options, validate });
  }

  /**
   * URL input with validation
   */
  async url(options: Omit<PromptOptions, 'validate'>): Promise<string> {
    const validate = (input: string): boolean | string => {
      try {
        new URL(input);
        return true;
      } catch {
        return 'Please enter a valid URL';
      }
    };

    return this.input({ ...options, validate });
  }

  /**
   * Close the prompt interface
   */
  close(): void {
    // No cleanup needed with inquirer
  }
}

// Utility functions for common prompt patterns

/**
 * Quick input prompt
 */
export async function input(message: string, options?: Partial<PromptOptions>): Promise<string> {
  const prompt = new Prompt();
  return await prompt.input({ message, ...options });
}

/**
 * Quick confirmation prompt
 */
export async function confirm(message: string, defaultValue?: boolean): Promise<boolean> {
  const prompt = new Prompt();
  const options: ConfirmOptions = { message };
  if (defaultValue !== undefined) {
    options.default = defaultValue;
  }
  return await prompt.confirm(options);
}

/**
 * Quick selection prompt
 */
export async function select(message: string, choices: ChoiceOption[]): Promise<any> {
  const prompt = new Prompt();
  return await prompt.select({ message, choices });
}

/**
 * Quick checkbox prompt
 */
export async function checkbox(message: string, choices: ChoiceOption[]): Promise<any[]> {
  const prompt = new Prompt();
  return await prompt.checkbox({ message, choices });
}

/**
 * Quick password prompt
 */
export async function password(message: string, options?: Partial<Omit<PromptOptions, 'mask'>>): Promise<string> {
  const prompt = new Prompt();
  return await prompt.password({ message, ...options });
}