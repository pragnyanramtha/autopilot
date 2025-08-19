import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { colors, detectColorSupport, getPlatformOptimizedTheme } from '../../../src/ui/utils/Colors.js';
import { symbols, detectSymbolSupport, getPlatformOptimizedSymbols } from '../../../src/ui/utils/Symbols.js';
import { Layout } from '../../../src/ui/utils/Layout.js';
import { Banner } from '../../../src/ui/components/Banner.js';
import { StatusIndicator } from '../../../src/ui/components/StatusIndicator.js';
import { 
  getCapturedLogs, 
  mockConsoleLog, 
  restoreConsoleLog 
} from '../../setup.js';

describe('Cross-Platform Compatibility', () => {
  let originalPlatform: string;
  let originalColumns: number | undefined;
  let originalEnv: NodeJS.ProcessEnv;

  beforeEach(() => {
    mockConsoleLog();
    originalPlatform = process.platform;
    originalColumns = process.stdout.columns;
    originalEnv = { ...process.env };
  });

  afterEach(() => {
    restoreConsoleLog();
    Object.defineProperty(process, 'platform', { value: originalPlatform });
    Object.defineProperty(process.stdout, 'columns', { value: originalColumns });
    process.env = originalEnv;
  });

  describe('Platform Detection', () => {
    it('should detect Linux platform', () => {
      Object.defineProperty(process, 'platform', { value: 'linux' });
      
      const colorSupport = detectColorSupport();
      const symbolSupport = detectSymbolSupport();
      
      expect(colorSupport.platform).toBe('linux');
      expect(symbolSupport.platform).toBe('linux');
    });

    it('should detect macOS platform', () => {
      Object.defineProperty(process, 'platform', { value: 'darwin' });
      
      const colorSupport = detectColorSupport();
      const symbolSupport = detectSymbolSupport();
      
      expect(colorSupport.platform).toBe('darwin');
      expect(symbolSupport.platform).toBe('darwin');
    });

    it('should detect Windows platform', () => {
      Object.defineProperty(process, 'platform', { value: 'win32' });
      
      const colorSupport = detectColorSupport();
      const symbolSupport = detectSymbolSupport();
      
      expect(colorSupport.platform).toBe('win32');
      expect(symbolSupport.platform).toBe('win32');
    });

    it('should detect FreeBSD platform', () => {
      Object.defineProperty(process, 'platform', { value: 'freebsd' });
      
      Banner.displayCompact();
      const output = getCapturedLogs();
      expect(output[0]).toContain('FreeBSD');
    });

    it('should detect OpenBSD platform', () => {
      Object.defineProperty(process, 'platform', { value: 'openbsd' });
      
      Banner.displayCompact();
      const output = getCapturedLogs();
      expect(output[0]).toContain('OpenBSD');
    });
  });

  describe('Terminal Type Detection', () => {
    it('should detect iTerm', () => {
      process.env.TERM_PROGRAM = 'iTerm.app';
      
      const colorSupport = detectColorSupport();
      const symbolSupport = detectSymbolSupport();
      
      expect(colorSupport.terminalType).toBe('iterm');
      expect(symbolSupport.terminalType).toBe('iterm');
    });

    it('should detect Terminal.app', () => {
      process.env.TERM_PROGRAM = 'Apple_Terminal';
      
      const colorSupport = detectColorSupport();
      const symbolSupport = detectSymbolSupport();
      
      expect(colorSupport.terminalType).toBe('terminal');
      expect(symbolSupport.terminalType).toBe('terminal');
    });

    it('should detect Hyper', () => {
      process.env.TERM_PROGRAM = 'Hyper';
      
      const colorSupport = detectColorSupport();
      const symbolSupport = detectSymbolSupport();
      
      expect(colorSupport.terminalType).toBe('hyper');
      expect(symbolSupport.terminalType).toBe('hyper');
    });

    it('should detect Windows Terminal', () => {
      Object.defineProperty(process, 'platform', { value: 'win32' });
      process.env.WT_SESSION = 'some-session-id';
      
      const colorSupport = detectColorSupport();
      const symbolSupport = detectSymbolSupport();
      
      expect(colorSupport.terminalType).toBe('windows-terminal');
      expect(symbolSupport.terminalType).toBe('windows-terminal');
    });

    it('should detect xterm', () => {
      process.env.TERM = 'xterm-256color';
      delete process.env.TERM_PROGRAM;
      
      const colorSupport = detectColorSupport();
      const symbolSupport = detectSymbolSupport();
      
      expect(colorSupport.terminalType).toBe('xterm');
      expect(symbolSupport.terminalType).toBe('xterm');
    });

    it('should detect screen/tmux', () => {
      process.env.TERM = 'screen-256color';
      delete process.env.TERM_PROGRAM;
      
      const colorSupport = detectColorSupport();
      const symbolSupport = detectSymbolSupport();
      
      expect(colorSupport.terminalType).toBe('screen');
      expect(symbolSupport.terminalType).toBe('screen');
    });

    it('should detect Alacritty', () => {
      process.env.TERM_PROGRAM = 'Alacritty';
      
      const symbolSupport = detectSymbolSupport();
      expect(symbolSupport.terminalType).toBe('alacritty');
    });

    it('should detect kitty', () => {
      process.env.TERM_PROGRAM = 'kitty';
      
      const symbolSupport = detectSymbolSupport();
      expect(symbolSupport.terminalType).toBe('kitty');
    });
  });

  describe('Color Support Detection', () => {
    it('should detect basic color support', () => {
      process.env.TERM = 'xterm';
      delete process.env.COLORTERM;
      
      const support = detectColorSupport();
      expect(typeof support.hasColor).toBe('boolean');
    });

    it('should detect 256 color support', () => {
      process.env.TERM = 'xterm-256color';
      
      const support = detectColorSupport();
      expect(support.has256Color).toBe(true);
    });

    it('should detect true color support', () => {
      process.env.COLORTERM = 'truecolor';
      
      const support = detectColorSupport();
      expect(support.hasTrueColor).toBe(true);
    });

    it('should detect high contrast mode', () => {
      process.env.FORCE_HIGH_CONTRAST = 'true';
      
      const support = detectColorSupport();
      expect(support.isHighContrast).toBe(true);
    });

    it('should work without color support', () => {
      process.env.TERM = 'dumb';
      delete process.env.COLORTERM;
      
      const theme = getPlatformOptimizedTheme();
      expect(theme).toBeDefined();
    });
  });

  describe('Symbol Support Detection', () => {
    it('should detect Unicode support', () => {
      process.env.LANG = 'en_US.UTF-8';
      process.env.TERM = 'xterm-256color';
      
      const support = detectSymbolSupport();
      expect(support.hasUnicode).toBe(true);
    });

    it('should detect box drawing support', () => {
      process.env.LANG = 'en_US.UTF-8';
      process.env.TERM = 'xterm-256color';
      process.env.TERM_PROGRAM = 'iTerm.app';
      
      const support = detectSymbolSupport();
      expect(support.hasBoxDrawing).toBe(true);
    });

    it('should detect emoji support', () => {
      process.env.TERM_PROGRAM = 'iTerm.app';
      process.env.LANG = 'en_US.UTF-8';
      
      const support = detectSymbolSupport();
      expect(support.hasEmoji).toBe(true);
    });

    it('should handle ASCII-only terminals', () => {
      process.env.FORCE_ASCII = 'true';
      
      const symbols = getPlatformOptimizedSymbols();
      expect(symbols.success).toBe('v');
      expect(symbols.error).toBe('x');
    });

    it('should detect accessibility mode', () => {
      process.env.ACCESSIBILITY_MODE = 'true';
      
      const support = detectSymbolSupport();
      expect(support.isAccessibilityMode).toBe(true);
    });
  });

  describe('Terminal Width Adaptation', () => {
    it('should adapt to narrow terminals', () => {
      Object.defineProperty(process.stdout, 'columns', { value: 40 });
      
      Banner.display();
      const output = getCapturedLogs();
      expect(output.length).toBeGreaterThan(0);
    });

    it('should adapt to wide terminals', () => {
      Object.defineProperty(process.stdout, 'columns', { value: 120 });
      
      Banner.display();
      const output = getCapturedLogs();
      expect(output.length).toBeGreaterThan(0);
    });

    it('should handle very narrow terminals', () => {
      Object.defineProperty(process.stdout, 'columns', { value: 20 });
      
      Banner.display({ compact: true });
      const output = getCapturedLogs();
      expect(output.length).toBeGreaterThan(0);
    });

    it('should handle undefined terminal width', () => {
      Object.defineProperty(process.stdout, 'columns', { value: undefined });
      
      const width = Layout.getTerminalWidth();
      expect(width).toBe(80); // Should fallback to 80
    });
  });

  describe('Platform-Specific Optimizations', () => {
    it('should optimize for Windows Command Prompt', () => {
      Object.defineProperty(process, 'platform', { value: 'win32' });
      process.env.TERM = 'cmd';
      delete process.env.WT_SESSION;
      
      const theme = getPlatformOptimizedTheme();
      const symbols = getPlatformOptimizedSymbols();
      
      expect(theme).toBeDefined();
      expect(symbols.success).toBe('OK');
    });

    it('should optimize for Windows Terminal', () => {
      Object.defineProperty(process, 'platform', { value: 'win32' });
      process.env.WT_SESSION = 'session-id';
      process.env.LANG = 'en_US.UTF-8';
      
      const symbols = getPlatformOptimizedSymbols();
      expect(symbols.success).toBe('✓');
    });

    it('should optimize for macOS Terminal', () => {
      Object.defineProperty(process, 'platform', { value: 'darwin' });
      process.env.TERM_PROGRAM = 'Apple_Terminal';
      
      const theme = getPlatformOptimizedTheme();
      const symbols = getPlatformOptimizedSymbols();
      
      expect(theme).toBeDefined();
      expect(symbols.success).toBe('✓');
    });

    it('should optimize for Linux console', () => {
      Object.defineProperty(process, 'platform', { value: 'linux' });
      process.env.TERM = 'linux';
      delete process.env.TERM_PROGRAM;
      
      const theme = getPlatformOptimizedTheme();
      const symbols = getPlatformOptimizedSymbols();
      
      expect(theme).toBeDefined();
      expect(symbols.success).toBe('[OK]');
    });
  });

  describe('Accessibility Features', () => {
    it('should support screen readers', () => {
      process.env.SCREEN_READER = 'true';
      
      const symbols = getPlatformOptimizedSymbols();
      expect(symbols.success).toBe('SUCCESS');
      expect(symbols.error).toBe('ERROR');
    });

    it('should support NVDA screen reader', () => {
      process.env.NVDA = 'true';
      
      const symbols = getPlatformOptimizedSymbols();
      expect(symbols.success).toBe('SUCCESS');
    });

    it('should support JAWS screen reader', () => {
      process.env.JAWS = 'true';
      
      const symbols = getPlatformOptimizedSymbols();
      expect(symbols.success).toBe('SUCCESS');
    });

    it('should support high contrast mode', () => {
      process.env.FORCE_HIGH_CONTRAST = 'true';
      
      StatusIndicator.success('High contrast test');
      const output = getCapturedLogs();
      expect(output.length).toBe(1);
    });

    it('should support color-blind friendly mode', () => {
      process.env.COLOR_BLIND_FRIENDLY = 'true';
      
      StatusIndicator.success('Color-blind friendly test');
      StatusIndicator.error('Color-blind friendly error');
      
      const output = getCapturedLogs();
      expect(output.length).toBe(2);
    });

    it('should disable Unicode when requested', () => {
      process.env.NO_UNICODE = 'true';
      
      const symbols = getPlatformOptimizedSymbols();
      expect(symbols.success).toBe('v');
      expect(symbols.boxVertical).toBe('|');
    });
  });

  describe('Encoding Support', () => {
    it('should handle UTF-8 encoding', () => {
      process.env.LANG = 'en_US.UTF-8';
      
      const support = detectSymbolSupport();
      expect(support.encoding).toBe('utf8');
    });

    it('should handle ASCII encoding', () => {
      process.env.LANG = 'C';
      
      const support = detectSymbolSupport();
      expect(support.encoding).toBe('ascii');
    });

    it('should handle missing LANG variable', () => {
      delete process.env.LANG;
      delete process.env.LC_ALL;
      
      const support = detectSymbolSupport();
      expect(support.encoding).toBe('ascii');
    });
  });

  describe('Component Cross-Platform Behavior', () => {
    it('should render banner consistently across platforms', () => {
      const platforms = ['linux', 'darwin', 'win32', 'freebsd'];
      
      platforms.forEach(platform => {
        Object.defineProperty(process, 'platform', { value: platform });
        
        Banner.displayCompact();
        const output = getCapturedLogs();
        expect(output.length).toBe(1);
        expect(output[0]).toContain('KIRA');
      });
    });

    it('should render status indicators consistently', () => {
      const platforms = ['linux', 'darwin', 'win32'];
      
      platforms.forEach(platform => {
        Object.defineProperty(process, 'platform', { value: platform });
        
        StatusIndicator.success('Cross-platform test');
        StatusIndicator.error('Cross-platform error');
        
        const output = getCapturedLogs();
        expect(output.length).toBe(2);
      });
    });

    it('should handle different terminal capabilities gracefully', () => {
      const terminalConfigs = [
        { TERM: 'dumb', COLORTERM: undefined },
        { TERM: 'xterm', COLORTERM: undefined },
        { TERM: 'xterm-256color', COLORTERM: undefined },
        { TERM: 'xterm-256color', COLORTERM: 'truecolor' }
      ];
      
      terminalConfigs.forEach(config => {
        process.env.TERM = config.TERM;
        if (config.COLORTERM) {
          process.env.COLORTERM = config.COLORTERM;
        } else {
          delete process.env.COLORTERM;
        }
        
        StatusIndicator.info('Terminal capability test');
        const output = getCapturedLogs();
        expect(output.length).toBeGreaterThan(0);
      });
    });
  });

  describe('Performance Across Platforms', () => {
    it('should perform consistently on different platforms', () => {
      const platforms = ['linux', 'darwin', 'win32'];
      const results: number[] = [];
      
      platforms.forEach(platform => {
        Object.defineProperty(process, 'platform', { value: platform });
        
        const startTime = Date.now();
        
        // Perform standard operations
        for (let i = 0; i < 100; i++) {
          StatusIndicator.info(`Test ${i}`);
        }
        
        const endTime = Date.now();
        results.push(endTime - startTime);
      });
      
      // Performance should be reasonably consistent
      const maxTime = Math.max(...results);
      const minTime = Math.min(...results);
      const variance = maxTime - minTime;
      
      expect(variance).toBeLessThan(1000); // Less than 1 second variance
    });

    it('should handle large outputs efficiently across platforms', () => {
      const platforms = ['linux', 'darwin', 'win32'];
      
      platforms.forEach(platform => {
        Object.defineProperty(process, 'platform', { value: platform });
        
        const startTime = Date.now();
        
        // Generate large output
        for (let i = 0; i < 1000; i++) {
          colors.primary(`Large text output ${i} with colors and formatting`);
        }
        
        const endTime = Date.now();
        expect(endTime - startTime).toBeLessThan(2000);
      });
    });
  });

  describe('Error Handling Across Platforms', () => {
    it('should handle missing environment variables gracefully', () => {
      delete process.env.TERM;
      delete process.env.TERM_PROGRAM;
      delete process.env.COLORTERM;
      delete process.env.LANG;
      delete process.env.LC_ALL;
      
      expect(() => {
        detectColorSupport();
        detectSymbolSupport();
        Banner.displayCompact();
        StatusIndicator.info('Test with missing env vars');
      }).not.toThrow();
    });

    it('should handle invalid environment variables gracefully', () => {
      process.env.TERM = 'invalid-terminal-type';
      process.env.COLORTERM = 'invalid-color-type';
      process.env.LANG = 'invalid-locale';
      
      expect(() => {
        detectColorSupport();
        detectSymbolSupport();
        Banner.displayCompact();
        StatusIndicator.info('Test with invalid env vars');
      }).not.toThrow();
    });

    it('should handle platform edge cases', () => {
      // Test with unusual platform values
      const unusualPlatforms = ['aix', 'sunos', 'netbsd'];
      
      unusualPlatforms.forEach(platform => {
        Object.defineProperty(process, 'platform', { value: platform });
        
        expect(() => {
          Banner.displayCompact();
          const output = getCapturedLogs();
          expect(output.length).toBe(1);
        }).not.toThrow();
      });
    });
  });
});