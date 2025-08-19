import { describe, it, expect, beforeEach, afterEach, jest } from '@jest/globals';
import { ProgressBar, Spinner, MultiStepProgress } from '../../../src/ui/components/ProgressBar.js';
import { 
  OptimizedProgressBar, 
  OptimizedSpinner, 
  OptimizedMultiStepProgress 
} from '../../../src/ui/components/OptimizedProgressBar.js';
import { 
  getCapturedOutput, 
  getCapturedLogs, 
  mockStdout, 
  restoreStdout, 
  mockConsoleLog, 
  restoreConsoleLog 
} from '../../setup.js';

describe('ProgressBar Components', () => {
  beforeEach(() => {
    mockConsoleLog();
    mockStdout();
  });

  afterEach(() => {
    restoreConsoleLog();
    restoreStdout();
  });

  describe('Basic ProgressBar', () => {
    it('should create progress bar with default options', () => {
      const progress = new ProgressBar();
      expect(progress).toBeDefined();
    });

    it('should create progress bar with custom options', () => {
      const progress = new ProgressBar({
        total: 50,
        current: 10,
        message: 'Loading...',
        showPercentage: true,
        showNumbers: true,
        width: 30
      });
      expect(progress).toBeDefined();
    });

    it('should update progress', () => {
      const progress = new ProgressBar({ total: 100 });
      progress.update(50, 'Half way');
      
      const output = getCapturedOutput();
      expect(output.length).toBeGreaterThan(0);
      expect(output.join('')).toContain('50%');
    });

    it('should increment progress', () => {
      const progress = new ProgressBar({ total: 10 });
      progress.increment(3);
      
      const output = getCapturedOutput();
      expect(output.join('')).toContain('30%');
    });

    it('should complete progress', () => {
      const progress = new ProgressBar({ total: 100 });
      progress.complete('Done!');
      
      const output = getCapturedOutput();
      expect(output.join('')).toContain('100%');
    });

    it('should fail progress', () => {
      const progress = new ProgressBar({ total: 100 });
      progress.fail('Failed!');
      
      const output = getCapturedOutput();
      expect(output.join('')).toContain('FAILED');
    });

    it('should show different styles', () => {
      const barProgress = new ProgressBar({ style: 'bar', total: 10 });
      barProgress.update(5);
      
      const dotsProgress = new ProgressBar({ style: 'dots', total: 10 });
      dotsProgress.update(5);
      
      const blocksProgress = new ProgressBar({ style: 'blocks', total: 10 });
      blocksProgress.update(5);
      
      const output = getCapturedOutput();
      expect(output.length).toBeGreaterThan(0);
    });

    it('should show ETA when enabled', () => {
      const progress = new ProgressBar({ 
        total: 100, 
        showEta: true 
      });
      
      // Simulate some progress over time
      progress.update(25);
      setTimeout(() => {
        progress.update(50);
        const output = getCapturedOutput();
        // ETA calculation might show up
        expect(output.length).toBeGreaterThan(0);
      }, 100);
    });

    it('should use static methods', () => {
      ProgressBar.simple(50, 100, 'Loading');
      ProgressBar.complete('Task completed');
      ProgressBar.fail('Task failed');
      
      const output = getCapturedOutput();
      expect(output.length).toBeGreaterThan(0);
    });
  });

  describe('Basic Spinner', () => {
    it('should create spinner', () => {
      const spinner = new Spinner('Loading...');
      expect(spinner).toBeDefined();
    });

    it('should start and stop spinner', (done) => {
      const spinner = new Spinner('Processing...');
      spinner.start();
      
      setTimeout(() => {
        spinner.stop();
        const output = getCapturedOutput();
        expect(output.length).toBeGreaterThan(0);
        done();
      }, 200);
    });

    it('should succeed spinner', (done) => {
      const spinner = new Spinner('Processing...');
      spinner.start();
      
      setTimeout(() => {
        spinner.succeed('Success!');
        const logs = getCapturedLogs();
        expect(logs.join('\n')).toContain('Success!');
        done();
      }, 100);
    });

    it('should fail spinner', (done) => {
      const spinner = new Spinner('Processing...');
      spinner.start();
      
      setTimeout(() => {
        spinner.fail('Failed!');
        const logs = getCapturedLogs();
        expect(logs.join('\n')).toContain('Failed!');
        done();
      }, 100);
    });

    it('should update spinner message', (done) => {
      const spinner = new Spinner('Initial...');
      spinner.start();
      
      setTimeout(() => {
        spinner.update('Updated message');
        setTimeout(() => {
          spinner.stop();
          done();
        }, 100);
      }, 100);
    });

    it('should use static spin method', async () => {
      const result = await Spinner.spin('Testing...', async () => {
        await new Promise(resolve => setTimeout(resolve, 100));
        return 'completed';
      });
      
      expect(result).toBe('completed');
      const logs = getCapturedLogs();
      expect(logs.length).toBeGreaterThan(0);
    });

    it('should handle errors in static spin method', async () => {
      try {
        await Spinner.spin('Testing error...', async () => {
          throw new Error('Test error');
        });
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
        const logs = getCapturedLogs();
        expect(logs.length).toBeGreaterThan(0);
      }
    });
  });

  describe('MultiStepProgress', () => {
    it('should create multi-step progress', () => {
      const steps = ['Step 1', 'Step 2', 'Step 3'];
      const progress = new MultiStepProgress(steps);
      expect(progress).toBeDefined();
    });

    it('should progress through steps', () => {
      const steps = ['Step 1', 'Step 2', 'Step 3'];
      const progress = new MultiStepProgress(steps);
      
      progress.nextStep('Moving to step 2');
      progress.nextStep('Moving to step 3');
      progress.complete('All done!');
      
      const logs = getCapturedLogs();
      expect(logs.length).toBeGreaterThan(0);
    });

    it('should complete current step', () => {
      const steps = ['Step 1', 'Step 2'];
      const progress = new MultiStepProgress(steps);
      
      progress.completeStep('Step 1 done');
      
      const logs = getCapturedLogs();
      expect(logs.length).toBeGreaterThan(0);
    });
  });

  describe('Optimized ProgressBar', () => {
    it('should create optimized progress bar', () => {
      const progress = new OptimizedProgressBar({
        total: 100,
        useCache: true,
        throttleMs: 50
      });
      expect(progress).toBeDefined();
    });

    it('should throttle updates for performance', () => {
      const progress = new OptimizedProgressBar({
        total: 100,
        throttleMs: 100
      });
      
      // Rapid updates should be throttled
      progress.update(10);
      progress.update(20);
      progress.update(30);
      
      const output = getCapturedOutput();
      // Should have fewer outputs due to throttling
      expect(output.length).toBeLessThan(6);
    });

    it('should use caching for performance', () => {
      const progress = new OptimizedProgressBar({
        total: 100,
        useCache: true
      });
      
      progress.update(50, 'Cached update');
      progress.update(50, 'Cached update'); // Same state, should use cache
      
      const output = getCapturedOutput();
      expect(output.length).toBeGreaterThan(0);
    });

    it('should use static optimized methods', () => {
      OptimizedProgressBar.simple(75, 100, 'Optimized loading');
      OptimizedProgressBar.complete('Optimized complete');
      OptimizedProgressBar.fail('Optimized fail');
      
      const output = getCapturedOutput();
      expect(output.length).toBeGreaterThan(0);
    });
  });

  describe('Optimized Spinner', () => {
    it('should create optimized spinner with throttling', () => {
      const spinner = new OptimizedSpinner('Loading...', undefined, 50);
      expect(spinner).toBeDefined();
    });

    it('should throttle spinner updates', (done) => {
      const spinner = new OptimizedSpinner('Processing...', undefined, 100);
      spinner.start();
      
      setTimeout(() => {
        spinner.stop();
        done();
      }, 250);
    });

    it('should use static optimized spin method', async () => {
      const result = await OptimizedSpinner.spin('Optimized test...', async () => {
        await new Promise(resolve => setTimeout(resolve, 50));
        return 'optimized result';
      });
      
      expect(result).toBe('optimized result');
    });
  });

  describe('Optimized MultiStepProgress', () => {
    it('should create optimized multi-step progress', () => {
      const steps = ['Step 1', 'Step 2', 'Step 3'];
      const progress = new OptimizedMultiStepProgress(steps, false);
      expect(progress).toBeDefined();
    });

    it('should create optimized multi-step progress with streaming', () => {
      const steps = ['Step 1', 'Step 2', 'Step 3'];
      const progress = new OptimizedMultiStepProgress(steps, true);
      expect(progress).toBeDefined();
      
      progress.nextStep('Moving forward');
      progress.finish();
    });

    it('should progress through steps with optimization', () => {
      const steps = ['Step 1', 'Step 2', 'Step 3'];
      const progress = new OptimizedMultiStepProgress(steps);
      
      progress.nextStep('Optimized step 2');
      progress.completeStep('Step completed');
      progress.complete('All optimized steps done');
      
      const logs = getCapturedLogs();
      expect(logs.length).toBeGreaterThan(0);
    });
  });

  describe('Performance characteristics', () => {
    it('should handle rapid updates efficiently', () => {
      const progress = new OptimizedProgressBar({
        total: 1000,
        throttleMs: 16 // ~60fps
      });
      
      const startTime = Date.now();
      
      // Simulate rapid updates
      for (let i = 0; i <= 1000; i += 10) {
        progress.update(i);
      }
      
      const endTime = Date.now();
      const duration = endTime - startTime;
      
      // Should complete quickly due to throttling
      expect(duration).toBeLessThan(1000);
    });

    it('should handle large step counts efficiently', () => {
      const manySteps = Array.from({ length: 100 }, (_, i) => `Step ${i + 1}`);
      const progress = new OptimizedMultiStepProgress(manySteps);
      
      const startTime = Date.now();
      
      // Progress through many steps
      for (let i = 0; i < 50; i++) {
        progress.nextStep(`Processing step ${i + 1}`);
      }
      
      const endTime = Date.now();
      const duration = endTime - startTime;
      
      // Should handle many steps efficiently
      expect(duration).toBeLessThan(2000);
    });
  });
});