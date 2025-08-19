import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { Banner } from '../../../src/ui/components/Banner.js';
import { OptimizedBanner } from '../../../src/ui/components/OptimizedBanner.js';
import { getCapturedLogs, mockConsoleLog, restoreConsoleLog } from '../../setup.js';

describe('Banner Component', () => {
  beforeEach(() => {
    mockConsoleLog();
  });

  afterEach(() => {
    restoreConsoleLog();
  });

  describe('Basic Banner', () => {
    it('should display banner with default options', () => {
      Banner.display();
      const output = getCapturedLogs();
      
      expect(output.length).toBeGreaterThan(0);
      expect(output.join('\n')).toContain('KIRA');
    });

    it('should display compact banner', () => {
      Banner.displayCompact();
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('KIRA');
      expect(output[0]).toContain('v0.1.0');
    });

    it('should display minimal banner', () => {
      Banner.displayMinimal();
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('Kira');
      expect(output[0]).toContain('v0.1.0');
    });

    it('should display banner with custom options', () => {
      Banner.display({
        showVersion: false,
        showTagline: false,
        compact: true
      });
      
      const output = getCapturedLogs();
      expect(output.join('\n')).toContain('KIRA');
    });

    it('should display welcome message', () => {
      Banner.welcome();
      const output = getCapturedLogs();
      
      expect(output.join('\n')).toContain('Welcome to Kira!');
    });

    it('should display startup message with username', () => {
      Banner.startup('TestUser');
      const output = getCapturedLogs();
      
      expect(output.join('\n')).toContain('Hello TestUser!');
    });

    it('should display error banner', () => {
      Banner.error('Test error message');
      const output = getCapturedLogs();
      
      expect(output.join('\n')).toContain('CRITICAL ERROR');
      expect(output.join('\n')).toContain('Test error message');
    });

    it('should display success banner', () => {
      Banner.success('Test success message');
      const output = getCapturedLogs();
      
      expect(output.join('\n')).toContain('SUCCESS');
      expect(output.join('\n')).toContain('Test success message');
    });

    it('should display info banner', () => {
      Banner.info('Test Title', 'Test info message');
      const output = getCapturedLogs();
      
      expect(output.join('\n')).toContain('TEST TITLE');
      expect(output.join('\n')).toContain('Test info message');
    });

    it('should display separator', () => {
      Banner.separator('TEST');
      const output = getCapturedLogs();
      
      expect(output.join('\n')).toContain('KIRA TEST');
    });

    it('should display footer', () => {
      Banner.footer();
      const output = getCapturedLogs();
      
      expect(output.join('\n')).toContain('Thank you for using Kira!');
    });
  });

  describe('Optimized Banner', () => {
    it('should display optimized banner with caching', async () => {
      await OptimizedBanner.display({ useCache: true });
      const output = getCapturedLogs();
      
      expect(output.length).toBeGreaterThan(0);
      expect(output.join('\n')).toContain('KIRA');
    });

    it('should display optimized compact banner', () => {
      OptimizedBanner.displayCompact();
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('KIRA');
    });

    it('should display optimized minimal banner', () => {
      OptimizedBanner.displayMinimal();
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('Kira');
    });

    it('should preload banner components', async () => {
      await OptimizedBanner.preload();
      // Should not throw any errors
      expect(true).toBe(true);
    });

    it('should get ASCII art', async () => {
      const art = await OptimizedBanner.getAsciiArt();
      expect(art).toContain('██');
    });

    it('should get version info', () => {
      const version = OptimizedBanner.getVersionInfo();
      expect(version).toBe('v0.1.0');
    });

    it('should get tagline', () => {
      const tagline = OptimizedBanner.getTagline();
      expect(tagline).toContain('AI-powered');
    });

    it('should display optimized welcome message', async () => {
      await OptimizedBanner.welcome({ useCache: true });
      const output = getCapturedLogs();
      
      expect(output.join('\n')).toContain('Welcome to Kira!');
    });

    it('should display optimized startup message', async () => {
      await OptimizedBanner.startup('TestUser', { useCache: true });
      const output = getCapturedLogs();
      
      expect(output.join('\n')).toContain('Hello TestUser!');
    });

    it('should display optimized error banner', () => {
      OptimizedBanner.error('Test error');
      const output = getCapturedLogs();
      
      expect(output.join('\n')).toContain('CRITICAL ERROR');
    });

    it('should display optimized success banner', () => {
      OptimizedBanner.success('Test success');
      const output = getCapturedLogs();
      
      expect(output.join('\n')).toContain('SUCCESS');
    });

    it('should display optimized info banner', () => {
      OptimizedBanner.info('Test', 'Test info');
      const output = getCapturedLogs();
      
      expect(output.join('\n')).toContain('TEST');
    });

    it('should display optimized separator', () => {
      OptimizedBanner.separator('TEST');
      const output = getCapturedLogs();
      
      expect(output.join('\n')).toContain('KIRA TEST');
    });

    it('should display optimized footer', () => {
      OptimizedBanner.footer();
      const output = getCapturedLogs();
      
      expect(output.join('\n')).toContain('Thank you for using Kira!');
    });

    it('should clear cache', () => {
      OptimizedBanner.clearCache();
      // Should not throw any errors
      expect(true).toBe(true);
    });
  });

  describe('Cross-platform compatibility', () => {
    it('should work on different platforms', () => {
      const originalPlatform = process.platform;
      
      // Test macOS
      Object.defineProperty(process, 'platform', { value: 'darwin' });
      Banner.displayCompact();
      let output = getCapturedLogs();
      expect(output[0]).toContain('macOS');
      
      // Test Windows
      Object.defineProperty(process, 'platform', { value: 'win32' });
      Banner.displayCompact();
      output = getCapturedLogs();
      expect(output[output.length - 1]).toContain('Windows');
      
      // Restore original platform
      Object.defineProperty(process, 'platform', { value: originalPlatform });
    });

    it('should adapt to terminal width', () => {
      const originalColumns = process.stdout.columns;
      
      // Test narrow terminal
      Object.defineProperty(process.stdout, 'columns', { value: 40 });
      Banner.display({ compact: false });
      let output = getCapturedLogs();
      expect(output.length).toBeGreaterThan(0);
      
      // Test wide terminal
      Object.defineProperty(process.stdout, 'columns', { value: 120 });
      Banner.display({ compact: false });
      output = getCapturedLogs();
      expect(output.length).toBeGreaterThan(0);
      
      // Restore original columns
      Object.defineProperty(process.stdout, 'columns', { value: originalColumns });
    });
  });
});