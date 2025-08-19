import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { StatusIndicator, StatusType } from '../../../src/ui/components/StatusIndicator.js';
import { 
  OptimizedStatusIndicator, 
  OptimizedStatusType 
} from '../../../src/ui/components/OptimizedStatusIndicator.js';
import { 
  getCapturedLogs, 
  mockConsoleLog, 
  restoreConsoleLog 
} from '../../setup.js';

describe('StatusIndicator Components', () => {
  beforeEach(() => {
    mockConsoleLog();
  });

  afterEach(() => {
    restoreConsoleLog();
  });

  describe('Basic StatusIndicator', () => {
    it('should display success status', () => {
      StatusIndicator.success('Operation completed successfully');
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('Operation completed successfully');
    });

    it('should display error status', () => {
      StatusIndicator.error('An error occurred');
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('An error occurred');
    });

    it('should display warning status', () => {
      StatusIndicator.warning('This is a warning');
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('This is a warning');
    });

    it('should display info status', () => {
      StatusIndicator.info('Information message');
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('Information message');
    });

    it('should display loading status', () => {
      StatusIndicator.loading('Loading data...');
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('Loading data...');
    });

    it('should display question status', () => {
      StatusIndicator.question('Are you sure?');
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('Are you sure?');
    });

    it('should display status with options', () => {
      StatusIndicator.success('Success with options', {
        prefix: 'TEST',
        indent: 2,
        timestamp: true,
        details: 'Additional details here'
      });
      
      const output = getCapturedLogs();
      expect(output.length).toBe(1);
      expect(output[0]).toContain('[TEST]');
      expect(output[0]).toContain('Success with options');
      expect(output[0]).toContain('Additional details here');
    });

    it('should display step status', () => {
      StatusIndicator.step(2, 5, 'Processing step 2', StatusType.INFO);
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('[2/5]');
      expect(output[0]).toContain('Processing step 2');
    });

    it('should display status list', () => {
      const items = [
        { message: 'First item', status: StatusType.SUCCESS },
        { message: 'Second item', status: StatusType.WARNING, details: 'Some details' },
        { message: 'Third item', status: StatusType.ERROR }
      ];
      
      StatusIndicator.list(items);
      const output = getCapturedLogs();
      
      expect(output.length).toBe(3);
      expect(output[0]).toContain('First item');
      expect(output[1]).toContain('Second item');
      expect(output[1]).toContain('Some details');
      expect(output[2]).toContain('Third item');
    });

    it('should display status summary', () => {
      const items = [
        { label: 'Files processed', status: StatusType.SUCCESS, value: '150' },
        { label: 'Warnings', status: StatusType.WARNING, value: '3' },
        { label: 'Errors', status: StatusType.ERROR, value: '0' }
      ];
      
      StatusIndicator.summary('Processing Summary', items);
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('Processing Summary');
      expect(output[0]).toContain('Files processed');
      expect(output[0]).toContain('150');
    });

    it('should display progress status', () => {
      StatusIndicator.progress(75, 100, 'Processing files', StatusType.LOADING);
      const output = getCapturedLogs();
      
      expect(output.length).toBe(2);
      expect(output[0]).toContain('Processing files');
      expect(output[1]).toContain('75%');
    });

    it('should display divider', () => {
      StatusIndicator.divider('SECTION');
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('SECTION');
    });

    it('should display columns', () => {
      const columns = [
        {
          title: 'Column 1',
          items: [
            { message: 'Item 1', status: StatusType.SUCCESS },
            { message: 'Item 2', status: StatusType.WARNING }
          ]
        },
        {
          title: 'Column 2',
          items: [
            { message: 'Item A', status: StatusType.INFO },
            { message: 'Item B', status: StatusType.ERROR }
          ]
        }
      ];
      
      StatusIndicator.columns(columns);
      const output = getCapturedLogs();
      
      expect(output.length).toBeGreaterThan(2);
      expect(output.join('\n')).toContain('Column 1');
      expect(output.join('\n')).toContain('Column 2');
    });
  });

  describe('Optimized StatusIndicator', () => {
    it('should display optimized success status', () => {
      OptimizedStatusIndicator.success('Optimized success message');
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('Optimized success message');
    });

    it('should display optimized error status', () => {
      OptimizedStatusIndicator.error('Optimized error message');
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('Optimized error message');
    });

    it('should display optimized warning status', () => {
      OptimizedStatusIndicator.warning('Optimized warning message');
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('Optimized warning message');
    });

    it('should display optimized info status', () => {
      OptimizedStatusIndicator.info('Optimized info message');
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('Optimized info message');
    });

    it('should display optimized loading status', () => {
      OptimizedStatusIndicator.loading('Optimized loading message');
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('Optimized loading message');
    });

    it('should display optimized question status', () => {
      OptimizedStatusIndicator.question('Optimized question message');
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('Optimized question message');
    });

    it('should use caching for repeated messages', () => {
      OptimizedStatusIndicator.success('Cached message', { useCache: true });
      OptimizedStatusIndicator.success('Cached message', { useCache: true });
      
      const output = getCapturedLogs();
      expect(output.length).toBe(2);
      expect(output[0]).toContain('Cached message');
      expect(output[1]).toContain('Cached message');
    });

    it('should display optimized step status', () => {
      OptimizedStatusIndicator.step(3, 7, 'Optimized step', OptimizedStatusType.SUCCESS);
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('[3/7]');
      expect(output[0]).toContain('Optimized step');
    });

    it('should display optimized status list with batching', () => {
      const items = [
        { message: 'Batch item 1', status: OptimizedStatusType.SUCCESS },
        { message: 'Batch item 2', status: OptimizedStatusType.WARNING },
        { message: 'Batch item 3', status: OptimizedStatusType.ERROR }
      ];
      
      OptimizedStatusIndicator.list(items);
      const output = getCapturedLogs();
      
      expect(output.length).toBe(3);
      expect(output[0]).toContain('Batch item 1');
      expect(output[1]).toContain('Batch item 2');
      expect(output[2]).toContain('Batch item 3');
    });

    it('should display optimized summary with caching', () => {
      const items = [
        { label: 'Optimized files', status: OptimizedStatusType.SUCCESS, value: '200' },
        { label: 'Cache hits', status: OptimizedStatusType.INFO, value: '95%' }
      ];
      
      OptimizedStatusIndicator.summary('Optimization Summary', items);
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('Optimization Summary');
      expect(output[0]).toContain('Optimized files');
      expect(output[0]).toContain('200');
    });

    it('should display optimized progress', () => {
      OptimizedStatusIndicator.progress(80, 100, 'Optimized processing', OptimizedStatusType.LOADING);
      const output = getCapturedLogs();
      
      expect(output.length).toBe(2);
      expect(output[0]).toContain('Optimized processing');
      expect(output[1]).toContain('80%');
    });

    it('should display optimized divider with caching', () => {
      OptimizedStatusIndicator.divider('OPTIMIZED');
      const output = getCapturedLogs();
      
      expect(output.length).toBe(1);
      expect(output[0]).toContain('OPTIMIZED');
    });

    it('should handle batch operations efficiently', () => {
      const operations = Array.from({ length: 10 }, (_, i) => ({
        type: OptimizedStatusType.INFO,
        message: `Batch operation ${i + 1}`,
        options: { useCache: true }
      }));
      
      OptimizedStatusIndicator.batch(operations);
      const output = getCapturedLogs();
      
      expect(output.length).toBe(10);
      expect(output[0]).toContain('Batch operation 1');
      expect(output[9]).toContain('Batch operation 10');
    });

    it('should handle large batch operations with streaming', () => {
      const operations = Array.from({ length: 60 }, (_, i) => ({
        type: OptimizedStatusType.SUCCESS,
        message: `Large batch ${i + 1}`,
        options: { useCache: true }
      }));
      
      OptimizedStatusIndicator.batch(operations);
      const output = getCapturedLogs();
      
      // Should handle large batches efficiently
      expect(output.length).toBeGreaterThan(50);
    });

    it('should get performance stats', () => {
      const stats = OptimizedStatusIndicator.getPerformanceStats();
      expect(stats).toBeDefined();
      expect(typeof stats).toBe('object');
    });
  });

  describe('Status type compatibility', () => {
    it('should handle all basic status types', () => {
      const types = [
        StatusType.SUCCESS,
        StatusType.ERROR,
        StatusType.WARNING,
        StatusType.INFO,
        StatusType.LOADING,
        StatusType.QUESTION
      ];
      
      types.forEach((type, index) => {
        StatusIndicator.step(index + 1, types.length, `Testing ${type}`, type);
      });
      
      const output = getCapturedLogs();
      expect(output.length).toBe(types.length);
    });

    it('should handle all optimized status types', () => {
      const types = [
        OptimizedStatusType.SUCCESS,
        OptimizedStatusType.ERROR,
        OptimizedStatusType.WARNING,
        OptimizedStatusType.INFO,
        OptimizedStatusType.LOADING,
        OptimizedStatusType.QUESTION
      ];
      
      types.forEach((type, index) => {
        OptimizedStatusIndicator.step(index + 1, types.length, `Testing optimized ${type}`, type);
      });
      
      const output = getCapturedLogs();
      expect(output.length).toBe(types.length);
    });
  });

  describe('Accessibility features', () => {
    it('should work with high contrast mode', () => {
      process.env.FORCE_HIGH_CONTRAST = 'true';
      
      StatusIndicator.success('High contrast success');
      StatusIndicator.error('High contrast error');
      
      const output = getCapturedLogs();
      expect(output.length).toBe(2);
      
      delete process.env.FORCE_HIGH_CONTRAST;
    });

    it('should work with accessibility mode', () => {
      process.env.ACCESSIBILITY_MODE = 'true';
      
      OptimizedStatusIndicator.success('Accessible success');
      OptimizedStatusIndicator.error('Accessible error');
      
      const output = getCapturedLogs();
      expect(output.length).toBe(2);
      
      delete process.env.ACCESSIBILITY_MODE;
    });

    it('should work without Unicode support', () => {
      process.env.FORCE_ASCII = 'true';
      
      StatusIndicator.success('ASCII success');
      StatusIndicator.warning('ASCII warning');
      
      const output = getCapturedLogs();
      expect(output.length).toBe(2);
      
      delete process.env.FORCE_ASCII;
    });
  });
});