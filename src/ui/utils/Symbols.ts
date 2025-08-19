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
  
  // File system symbols
  home: string;
  folder: string;
  file: string;
  link: string;
  
  // Directional symbols
  up: string;
  down: string;
  left: string;
  right: string;
  
  // Animation symbols
  spinner: string[];
  
  // Border symbols
  borderHorizontal: string;
  borderVertical: string;
  borderTopLeft: string;
  borderTopRight: string;
  borderBottomLeft: string;
  borderBottomRight: string;
  borderCross: string;
  borderTop: string;
  borderBottom: string;
  borderLeft: string;
  borderRight: string;
  
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
  
  // File system symbols
  home: '~',
  folder: '📁',
  file: '📄',
  link: '🔗',
  
  // Directional symbols
  up: '↑',
  down: '↓',
  left: '←',
  right: '→',
  
  // Animation symbols
  spinner: ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
  
  // Border symbols
  borderHorizontal: '─',
  borderVertical: '│',
  borderTopLeft: '┌',
  borderTopRight: '┐',
  borderBottomLeft: '└',
  borderBottomRight: '┘',
  borderCross: '┼',
  borderTop: '┬',
  borderBottom: '┴',
  borderLeft: '├',
  borderRight: '┤',
  
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
  
  // File system symbols
  home: '~',
  folder: '[DIR]',
  file: '[FILE]',
  link: '->',
  
  // Directional symbols
  up: '^',
  down: 'v',
  left: '<',
  right: '>',
  
  // Animation symbols
  spinner: ['|', '/', '-', '\\'],
  
  // Border symbols
  borderHorizontal: '-',
  borderVertical: '|',
  borderTopLeft: '+',
  borderTopRight: '+',
  borderBottomLeft: '+',
  borderBottomRight: '+',
  borderCross: '+',
  borderTop: '+',
  borderBottom: '+',
  borderLeft: '+',
  borderRight: '+',
  
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
  loading: ['.', '..', '...'],
  spinner: ['.', '..', '...']
};

// High contrast symbols for accessibility
export const highContrastSymbols: SymbolSet = {
  // Status symbols - use text for maximum clarity
  success: '[OK]',
  error: '[ERR]',
  warning: '[WARN]',
  info: '[INFO]',
  question: '[?]',
  
  // Progress symbols
  loading: ['[.]', '[..]', '[...]', '[....]'],
  bullet: '>>',
  arrow: '-->',
  arrowRight: '-->',
  arrowLeft: '<--',
  arrowUp: '^^^',
  arrowDown: 'vvv',
  
  // UI symbols
  checkbox: '[ ]',
  checkboxChecked: '[X]',
  radio: '( )',
  radioSelected: '(X)',
  
  // Decorative symbols
  star: '[*]',
  heart: '<3',
  diamond: '<>',
  circle: '(o)',
  square: '[#]',
  
  // File system symbols
  home: '[HOME]',
  folder: '[FOLDER]',
  file: '[FILE]',
  link: '[LINK]',
  
  // Directional symbols
  up: '[UP]',
  down: '[DOWN]',
  left: '[LEFT]',
  right: '[RIGHT]',
  
  // Animation symbols
  spinner: ['[.]', '[..]', '[...]', '[....]'],
  
  // Border symbols
  borderHorizontal: '-',
  borderVertical: '|',
  borderTopLeft: '+',
  borderTopRight: '+',
  borderBottomLeft: '+',
  borderBottomRight: '+',
  borderCross: '+',
  borderTop: '+',
  borderBottom: '+',
  borderLeft: '+',
  borderRight: '+',
  
  // Box drawing - use clear ASCII
  boxVertical: '|',
  boxHorizontal: '-',
  boxTopLeft: '+',
  boxTopRight: '+',
  boxBottomLeft: '+',
  boxBottomRight: '+',
  boxCross: '+',
  
  // Progress bars
  progressFull: '=',
  progressEmpty: '-',
  progressLeft: '[',
  progressRight: ']'
};

// Screen reader friendly symbols
export const screenReaderSymbols: SymbolSet = {
  // Status symbols - descriptive text
  success: 'SUCCESS',
  error: 'ERROR',
  warning: 'WARNING',
  info: 'INFO',
  question: 'QUESTION',
  
  // Progress symbols
  loading: ['LOADING', 'LOADING.', 'LOADING..', 'LOADING...'],
  bullet: '-',
  arrow: 'ARROW',
  arrowRight: 'RIGHT',
  arrowLeft: 'LEFT',
  arrowUp: 'UP',
  arrowDown: 'DOWN',
  
  // UI symbols
  checkbox: 'UNCHECKED',
  checkboxChecked: 'CHECKED',
  radio: 'UNSELECTED',
  radioSelected: 'SELECTED',
  
  // Decorative symbols
  star: 'STAR',
  heart: 'HEART',
  diamond: 'DIAMOND',
  circle: 'CIRCLE',
  square: 'SQUARE',
  
  // File system symbols
  home: 'HOME',
  folder: 'FOLDER',
  file: 'FILE',
  link: 'LINK',
  
  // Directional symbols
  up: 'UP',
  down: 'DOWN',
  left: 'LEFT',
  right: 'RIGHT',
  
  // Animation symbols
  spinner: ['LOADING', 'LOADING.', 'LOADING..', 'LOADING...'],
  
  // Border symbols
  borderHorizontal: 'HORIZONTAL',
  borderVertical: 'VERTICAL',
  borderTopLeft: 'TOP-LEFT',
  borderTopRight: 'TOP-RIGHT',
  borderBottomLeft: 'BOTTOM-LEFT',
  borderBottomRight: 'BOTTOM-RIGHT',
  borderCross: 'CROSS',
  borderTop: 'TOP',
  borderBottom: 'BOTTOM',
  borderLeft: 'LEFT',
  borderRight: 'RIGHT',
  
  // Box drawing
  boxVertical: 'VERTICAL',
  boxHorizontal: 'HORIZONTAL',
  boxTopLeft: 'TOP-LEFT',
  boxTopRight: 'TOP-RIGHT',
  boxBottomLeft: 'BOTTOM-LEFT',
  boxBottomRight: 'BOTTOM-RIGHT',
  boxCross: 'CROSS',
  
  // Progress bars
  progressFull: 'FULL',
  progressEmpty: 'EMPTY',
  progressLeft: 'START',
  progressRight: 'END'
};

// Enhanced symbol support detection
export function detectSymbolSupport(): {
  hasUnicode: boolean;
  hasBoxDrawing: boolean;
  hasEmoji: boolean;
  terminalType: string;
  platform: string;
  encoding: string;
  isAccessibilityMode: boolean;
} {
  const platform = process.platform;
  const term = process.env.TERM || '';
  const termProgram = process.env.TERM_PROGRAM || '';
  const lang = process.env.LANG || process.env.LC_ALL || '';
  
  // Detect terminal type
  let terminalType = 'unknown';
  if (termProgram.includes('iTerm')) terminalType = 'iterm';
  else if (termProgram.includes('Terminal')) terminalType = 'terminal';
  else if (termProgram.includes('Hyper')) terminalType = 'hyper';
  else if (process.env.WT_SESSION) terminalType = 'windows-terminal';
  else if (termProgram.includes('Alacritty')) terminalType = 'alacritty';
  else if (termProgram.includes('kitty')) terminalType = 'kitty';
  else if (term.includes('xterm')) terminalType = 'xterm';
  else if (term.includes('screen')) terminalType = 'screen';
  else if (term.includes('tmux')) terminalType = 'tmux';
  else if (platform === 'win32') terminalType = 'cmd';
  
  // Modern terminals that support Unicode
  const modernTerminals = [
    'iTerm.app',
    'Hyper',
    'Windows Terminal',
    'Alacritty',
    'kitty',
    'wezterm'
  ];
  
  // Check encoding support
  const encoding = lang.includes('UTF-8') || lang.includes('utf8') ? 'utf8' : 'ascii';
  
  // Unicode support detection
  const hasUnicode = encoding === 'utf8' && (
    platform !== 'win32' || 
    modernTerminals.some(t => termProgram.includes(t)) ||
    term.includes('256color') ||
    term.includes('truecolor') ||
    process.env.WT_SESSION // Windows Terminal
  );
  
  // Box drawing support (more conservative)
  const hasBoxDrawing = hasUnicode && 
    !term.includes('screen') && 
    terminalType !== 'cmd' &&
    terminalType !== 'unknown';
  
  // Emoji support (very selective)
  const hasEmoji = hasUnicode && (
    terminalType === 'iterm' ||
    terminalType === 'hyper' ||
    terminalType === 'windows-terminal' ||
    terminalType === 'alacritty' ||
    terminalType === 'kitty'
  );
  
  // Accessibility mode detection
  const isAccessibilityMode = process.env.FORCE_ASCII === 'true' ||
    process.env.NO_UNICODE === 'true' ||
    process.env.ACCESSIBILITY_MODE === 'true';
  
  return {
    hasUnicode: Boolean(hasUnicode && !isAccessibilityMode),
    hasBoxDrawing: Boolean(hasBoxDrawing && !isAccessibilityMode),
    hasEmoji: Boolean(hasEmoji && !isAccessibilityMode),
    terminalType,
    platform,
    encoding,
    isAccessibilityMode
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

// Auto-detect and set appropriate symbols based on environment
export function autoDetectSymbols(): SymbolSet {
  const support = detectSymbolSupport();
  
  // Check for accessibility modes first
  if (process.env.SCREEN_READER === 'true' || process.env.NVDA === 'true' || process.env.JAWS === 'true') {
    return screenReaderSymbols;
  }
  
  if (support.isAccessibilityMode || process.env.FORCE_HIGH_CONTRAST === 'true') {
    return highContrastSymbols;
  }
  
  // Platform-specific detection
  if (support.platform === 'win32') {
    if (support.terminalType === 'windows-terminal' && support.hasUnicode) {
      return unicodeSymbols;
    } else if (support.hasUnicode) {
      return windowsSymbols;
    } else {
      return asciiSymbols;
    }
  }
  
  // Unix-like systems
  if (support.hasUnicode && support.hasBoxDrawing) {
    return unicodeSymbols;
  } else if (support.hasUnicode) {
    // Unicode but no box drawing (e.g., screen/tmux)
    return {
      ...unicodeSymbols,
      boxVertical: '|',
      boxHorizontal: '-',
      boxTopLeft: '+',
      boxTopRight: '+',
      boxBottomLeft: '+',
      boxBottomRight: '+',
      boxCross: '+'
    };
  } else {
    return asciiSymbols;
  }
}

// Get symbols based on specific accessibility needs
export function getAccessibilitySymbols(type: 'high-contrast' | 'screen-reader' | 'ascii'): SymbolSet {
  switch (type) {
    case 'high-contrast':
      return highContrastSymbols;
    case 'screen-reader':
      return screenReaderSymbols;
    case 'ascii':
      return asciiSymbols;
    default:
      return unicodeSymbols;
  }
}

// Platform-optimized symbols
export function getPlatformOptimizedSymbols(): SymbolSet {
  const support = detectSymbolSupport();
  const baseSymbols = autoDetectSymbols();
  
  // Windows Command Prompt optimizations
  if (support.platform === 'win32' && support.terminalType === 'cmd') {
    return {
      ...baseSymbols,
      loading: ['.', '..', '...', '....'],
      success: 'OK',
      error: 'ERR'
    };
  }
  
  // macOS Terminal optimizations
  if (support.platform === 'darwin' && support.terminalType === 'terminal') {
    return {
      ...baseSymbols,
      // macOS Terminal has good Unicode support
      success: '✓',
      error: '✗'
    };
  }
  
  // Linux console optimizations
  if (support.platform === 'linux' && support.terminalType === 'unknown') {
    return {
      ...baseSymbols,
      // Conservative symbols for basic Linux console
      success: '[OK]',
      error: '[ERR]',
      loading: ['|', '/', '-', '\\']
    };
  }
  
  return baseSymbols;
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

// Symbol testing utilities
export function testSymbolSupport(): void {
  const support = detectSymbolSupport();
  console.log('Symbol Support Detection:');
  console.log(`  Platform: ${support.platform}`);
  console.log(`  Terminal: ${support.terminalType}`);
  console.log(`  Encoding: ${support.encoding}`);
  console.log(`  Has Unicode: ${support.hasUnicode}`);
  console.log(`  Box Drawing: ${support.hasBoxDrawing}`);
  console.log(`  Emoji Support: ${support.hasEmoji}`);
  console.log(`  Accessibility Mode: ${support.isAccessibilityMode}`);
  
  console.log('\nSymbol Set Test:');
  const symbols = getPlatformOptimizedSymbols();
  console.log(`Success: ${symbols.success}`);
  console.log(`Error: ${symbols.error}`);
  console.log(`Warning: ${symbols.warning}`);
  console.log(`Info: ${symbols.info}`);
  console.log(`Loading: ${symbols.loading.join(' ')}`);
  console.log(`Arrow: ${symbols.arrow}`);
  console.log(`Checkbox: ${symbols.checkbox} / ${symbols.checkboxChecked}`);
  
  if (support.hasBoxDrawing) {
    console.log('\nBox Drawing Test:');
    console.log(`${symbols.boxTopLeft}${symbols.boxHorizontal.repeat(10)}${symbols.boxTopRight}`);
    console.log(`${symbols.boxVertical}${' '.repeat(10)}${symbols.boxVertical}`);
    console.log(`${symbols.boxBottomLeft}${symbols.boxHorizontal.repeat(10)}${symbols.boxBottomRight}`);
  }
}

// Validate symbol accessibility
export function validateSymbolAccessibility(symbolSet: SymbolSet): {
  isAccessible: boolean;
  issues: string[];
  recommendations: string[];
} {
  const issues: string[] = [];
  const recommendations: string[] = [];
  
  // Check for potentially problematic Unicode characters
  const problematicChars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
  if (problematicChars.some(char => symbolSet.loading.includes(char))) {
    issues.push('Loading animation uses Braille characters that may not be screen reader friendly');
    recommendations.push('Consider using text-based loading indicators for accessibility');
  }
  
  // Check for single-character symbols that might be unclear
  if (symbolSet.success.length === 1 && !symbolSet.success.match(/[a-zA-Z]/)) {
    issues.push('Success symbol is a single non-alphabetic character');
    recommendations.push('Consider using text like "OK" or "SUCCESS" for better accessibility');
  }
  
  const isAccessible = issues.length === 0;
  
  return {
    isAccessible,
    issues,
    recommendations
  };
}

// Initialize symbols on import
setSymbols(getPlatformOptimizedSymbols());