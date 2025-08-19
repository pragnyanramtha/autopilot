import { symbols } from './Symbols.js';

export interface LayoutOptions {
  indent?: number;
  spacing?: number;
  maxWidth?: number;
  padding?: number;
}

export class Layout {
  private static defaultOptions: LayoutOptions = {
    indent: 2,
    spacing: 1,
    maxWidth: 80,
    padding: 1
  };

  // Get terminal width with fallback
  static getTerminalWidth(): number {
    return process.stdout.columns || 80;
  }

  // Indent text by specified number of spaces
  static indent(text: string, level: number = 1, char: string = ' '): string {
    const indentStr = char.repeat(level * (this.defaultOptions.indent || 2));
    return text.split('\n').map(line => indentStr + line).join('\n');
  }

  // Center text within specified width
  static center(text: string, width?: number): string {
    const termWidth = width || this.getTerminalWidth();
    const lines = text.split('\n');
    
    return lines.map(line => {
      const padding = Math.max(0, Math.floor((termWidth - line.length) / 2));
      return ' '.repeat(padding) + line;
    }).join('\n');
  }

  // Wrap text to specified width
  static wrap(text: string, width?: number): string[] {
    const maxWidth = width || this.defaultOptions.maxWidth || 80;
    const words = text.split(' ');
    const lines: string[] = [];
    let currentLine = '';

    for (const word of words) {
      if (currentLine.length + word.length + 1 <= maxWidth) {
        currentLine += (currentLine ? ' ' : '') + word;
      } else {
        if (currentLine) lines.push(currentLine);
        currentLine = word;
      }
    }
    
    if (currentLine) lines.push(currentLine);
    return lines;
  }

  // Create a box around content
  static box(content: string, title?: string, options?: { 
    padding?: number; 
    width?: number; 
    style?: 'single' | 'double' | 'rounded' 
  }): string {
    const opts = { padding: 1, style: 'single' as const, ...options };
    const termWidth = this.getTerminalWidth();
    const maxWidth = Math.min(opts.width || termWidth - 4, termWidth - 4);
    
    // Box drawing characters based on style
    const chars = {
      single: {
        horizontal: symbols.boxHorizontal,
        vertical: symbols.boxVertical,
        topLeft: symbols.boxTopLeft,
        topRight: symbols.boxTopRight,
        bottomLeft: symbols.boxBottomLeft,
        bottomRight: symbols.boxBottomRight
      },
      double: {
        horizontal: '═',
        vertical: '║',
        topLeft: '╔',
        topRight: '╗',
        bottomLeft: '╚',
        bottomRight: '╝'
      },
      rounded: {
        horizontal: '─',
        vertical: '│',
        topLeft: '╭',
        topRight: '╮',
        bottomLeft: '╰',
        bottomRight: '╯'
      }
    };

    const boxChars = chars[opts.style];
    const lines = content.split('\n');
    const contentWidth = Math.max(...lines.map(line => line.length));
    const boxWidth = Math.min(Math.max(contentWidth + opts.padding * 2, title ? title.length + 4 : 0), maxWidth);
    
    let result = '';
    
    // Top border
    if (title) {
      const titlePadding = Math.max(0, boxWidth - title.length - 2);
      const leftPadding = Math.floor(titlePadding / 2);
      const rightPadding = titlePadding - leftPadding;
      result += boxChars.topLeft + 
                boxChars.horizontal.repeat(leftPadding) + 
                ` ${title} ` + 
                boxChars.horizontal.repeat(rightPadding) + 
                boxChars.topRight + '\n';
    } else {
      result += boxChars.topLeft + boxChars.horizontal.repeat(boxWidth) + boxChars.topRight + '\n';
    }
    
    // Content with padding
    const paddingStr = ' '.repeat(opts.padding);
    for (const line of lines) {
      const paddedLine = paddingStr + line + ' '.repeat(Math.max(0, boxWidth - line.length - opts.padding * 2)) + paddingStr;
      result += boxChars.vertical + paddedLine + boxChars.vertical + '\n';
    }
    
    // Bottom border
    result += boxChars.bottomLeft + boxChars.horizontal.repeat(boxWidth) + boxChars.bottomRight;
    
    return result;
  }

  // Create a horizontal separator
  static separator(char?: string, width?: number, label?: string): string {
    const sepChar = char || symbols.boxHorizontal;
    const termWidth = width || this.getTerminalWidth();
    
    if (label) {
      const labelWithSpaces = ` ${label} `;
      const sideLength = Math.floor((termWidth - labelWithSpaces.length) / 2);
      return sepChar.repeat(sideLength) + labelWithSpaces + sepChar.repeat(sideLength);
    }
    
    return sepChar.repeat(termWidth);
  }

  // Create vertical spacing
  static spacing(lines: number = 1): string {
    return '\n'.repeat(lines);
  }

  // Align text (left, center, right)
  static align(text: string, alignment: 'left' | 'center' | 'right', width?: number): string {
    const termWidth = width || this.getTerminalWidth();
    const lines = text.split('\n');
    
    return lines.map(line => {
      switch (alignment) {
        case 'center':
          const centerPadding = Math.max(0, Math.floor((termWidth - line.length) / 2));
          return ' '.repeat(centerPadding) + line;
        case 'right':
          const rightPadding = Math.max(0, termWidth - line.length);
          return ' '.repeat(rightPadding) + line;
        case 'left':
        default:
          return line;
      }
    }).join('\n');
  }

  // Create a progress bar
  static progressBar(current: number, total: number, width?: number, options?: {
    showPercentage?: boolean;
    showNumbers?: boolean;
    char?: string;
    emptyChar?: string;
  }): string {
    const opts = {
      showPercentage: true,
      showNumbers: false,
      char: symbols.progressFull,
      emptyChar: symbols.progressEmpty,
      ...options
    };
    
    const barWidth = (width || 40) - (opts.showPercentage ? 6 : 0) - (opts.showNumbers ? ` ${total}`.length * 2 + 1 : 0);
    const percentage = Math.min(100, Math.max(0, (current / total) * 100));
    const filled = Math.floor((percentage / 100) * barWidth);
    const empty = barWidth - filled;
    
    let bar = opts.char.repeat(filled) + opts.emptyChar.repeat(empty);
    
    if (opts.showNumbers) {
      bar = `${current}/${total} ${bar}`;
    }
    
    if (opts.showPercentage) {
      bar += ` ${Math.round(percentage)}%`;
    }
    
    return bar;
  }

  // Create a list with bullets
  static list(items: string[], options?: {
    bullet?: string;
    indent?: number;
    spacing?: boolean;
  }): string {
    const opts = {
      bullet: symbols.bullet,
      indent: 0,
      spacing: false,
      ...options
    };
    
    const indentStr = ' '.repeat(opts.indent);
    const separator = opts.spacing ? '\n' : '';
    
    return items.map(item => `${indentStr}${opts.bullet} ${item}`).join('\n' + separator);
  }

  // Create a numbered list
  static numberedList(items: string[], options?: {
    indent?: number;
    spacing?: boolean;
    startFrom?: number;
  }): string {
    const opts = {
      indent: 0,
      spacing: false,
      startFrom: 1,
      ...options
    };
    
    const indentStr = ' '.repeat(opts.indent);
    const separator = opts.spacing ? '\n' : '';
    
    return items.map((item, index) => {
      const number = opts.startFrom + index;
      return `${indentStr}${number}. ${item}`;
    }).join('\n' + separator);
  }

  // Truncate text with ellipsis
  static truncate(text: string, maxLength: number, ellipsis: string = '...'): string {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength - ellipsis.length) + ellipsis;
  }

  // Pad text to specified length
  static pad(text: string, length: number, char: string = ' ', align: 'left' | 'right' | 'center' = 'left'): string {
    if (text.length >= length) return text;
    
    const padding = length - text.length;
    
    switch (align) {
      case 'right':
        return char.repeat(padding) + text;
      case 'center':
        const leftPad = Math.floor(padding / 2);
        const rightPad = padding - leftPad;
        return char.repeat(leftPad) + text + char.repeat(rightPad);
      case 'left':
      default:
        return text + char.repeat(padding);
    }
  }

  // Set default layout options
  static setDefaults(options: Partial<LayoutOptions>): void {
    this.defaultOptions = { ...this.defaultOptions, ...options };
  }

  // Get current default options
  static getDefaults(): LayoutOptions {
    return { ...this.defaultOptions };
  }
}