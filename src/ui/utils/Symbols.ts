// Unicode symbols with fallbacks for different platforms and terminals

export interface SymbolSet {
  // Status symbols
  success: string;
  error: string;
  warning: string;
  info: string;
  question: string;
  
  // Progress symbols
  loading: string[];
  bullet: string;
  arrow: string;
  arrowRight: string;
  arrowLeft: string;
  arrowUp: string;
  arrowDown: string;
  
  // UI symbols
  checkbox: string;
  checkboxChecked: string;
  radio: string;
  radioSelected: string;
  
  // Decorative symbols
  star: string;
  heart: string;
  diamond: string;
  circle: string;
  square: string;
  
  // Box drawing
  boxVertical: string;
  boxHorizontal: string;
  boxTopLeft: string;
  boxTopRight: string;
  boxBottomLeft: string;
  boxBottomRight: string;
  boxCross: string;
  
  // Progress bars
  progressFull: string;
  progressEmpty: string;
  progressLeft: string;
  progressRight: string;
}

// Full Unicode symbol set for modern terminals
export const unicodeSymbols: SymbolSet = {
  // Status symbols
  success: '✓',
  error: '✗',
  warning: '⚠',
  info: 'ℹ',
  question: '?',
  
  // Progress symbols
  loading: ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
  bullet: '•',
  arrow: '→',
  arrowRight: '→',
  arrowLeft: '←',
  arrowUp: '↑',
  arrowDown: '↓',
  
  // UI symbols
  checkbox: '☐',
  checkboxChecked: '☑',
  radio: '○',
  radioSelected: '●',
  
  // Decorative symbols
  star: '★',
  heart: '♥',
  diamond: '♦',
  circle: '●',
  square: '■',
  
  // Box drawing
  boxVertical: '│',
  boxHorizontal: '─',
  boxTopLeft: '┌',
  boxTopRight: '┐',
  boxBottomLeft: '└',
  boxBottomRight: '┘',
  boxCross: '┼',
  
  // Progress bars
  progressFull: '█',
  progressEmpty: '░',
  progressLeft: '▌',
  progressRight: '▐'
};

// ASCII fallback symbols for basic terminals
export const asciiSymbols: SymbolSet = {
  // Status symbols
  success: 'v',
  error: 'x',
  warning: '!',
  info: 'i',
  question: '?',
  
  // Progress symbols
  loading: ['|', '/', '-', '\\'],
  bullet: '*',
  arrow: '>',
  arrowRight: '>',
  arrowLeft: '<',
  arrowUp: '^',
  arrowDown: 'v',
  
  // UI symbols
  checkbox: '[ ]',
  checkboxChecked: '[x]',
  radio: '( )',
  radioSelected: '(*)',
  
  // Decorative symbols
  star: '*',
  heart: '<3',
  diamond: '<>',
  circle: 'o',
  square: '#',
  
  // Box drawing
  boxVertical: '|',
  boxHorizontal: '-',
  boxTopLeft: '+',
  boxTopRight: '+',
  boxBottomLeft: '+',
  boxBottomRight: '+',
  boxCross: '+',
  
  // Progress bars
  progressFull: '#',
  progressEmpty: '-',
  progressLeft: '[',
  progressRight: ']'
};

// Windows-specific symbols
export const windowsSymbols: SymbolSet = {
  ...asciiSymbols,
  success: '√',
  error: '×',
  loading: ['.', '..', '...']
};

// Detect symbol support
export function detectSymbolSupport(): {
  hasUnicode: boolean;
  hasBoxDrawing: boolean;
  hasEmoji: boolean;
} {
  const isWindows = process.platform === 'win32';
  const term = process.env.TERM || '';
  const termProgram = process.env.TERM_PROGRAM || '';
  
  // Modern terminals that support Unicode
  const modernTerminals = [
    'iTerm.app',
    'Hyper',
    'Windows Terminal',
    'Alacritty',
    'kitty'
  ];
  
  const hasUnicode = !isWindows || 
    modernTerminals.includes(termProgram) ||
    term.includes('256color') ||
    term.includes('truecolor');
  
  const hasBoxDrawing = hasUnicode && !term.includes('screen');
  const hasEmoji = hasUnicode && (
    termProgram === 'iTerm.app' ||
    termProgram === 'Hyper' ||
    termProgram === 'Windows Terminal'
  );
  
  return {
    hasUnicode,
    hasBoxDrawing,
    hasEmoji
  };
}

// Current active symbol set
let currentSymbols: SymbolSet = unicodeSymbols;

export function setSymbols(symbols: SymbolSet): void {
  currentSymbols = symbols;
}

export function getSymbols(): SymbolSet {
  return currentSymbols;
}

// Auto-detect and set appropriate symbols
export function autoDetectSymbols(): SymbolSet {
  const support = detectSymbolSupport();
  
  if (process.platform === 'win32' && !support.hasUnicode) {
    return windowsSymbols;
  } else if (!support.hasUnicode) {
    return asciiSymbols;
  } else {
    return unicodeSymbols;
  }
}

// Utility object for easy access to current symbols
export const symbols = new Proxy({} as SymbolSet, {
  get(target, prop: keyof SymbolSet) {
    return currentSymbols[prop];
  }
});

// Spinner animation helper
export class SpinnerAnimation {
  private frames: string[];
  private currentFrame: number = 0;
  
  constructor(frames?: string[]) {
    this.frames = frames || currentSymbols.loading;
  }
  
  next(): string {
    const frame = this.frames[this.currentFrame];
    this.currentFrame = (this.currentFrame + 1) % this.frames.length;
    return frame;
  }
  
  reset(): void {
    this.currentFrame = 0;
  }
}

// Initialize symbols on import
setSymbols(autoDetectSymbols());