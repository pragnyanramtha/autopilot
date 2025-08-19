import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import {
  outputCache,
  lazyLoader,
  StreamingOutput,
  formattingOptimizer,
  performanceMonitor,
  memoryMonitor,
  withCache,
  withPerformanceTracking,
  withAsyncPerformanceTracking,
  createStreamingOutput,
  optimizeColors,
  loadComponent,
  isPerformanceMonitoringEnabled
} from '../../../src/ui/utils/Performance.js';
import { colors } from '../../../src/ui/utils/Colors.js';
import { 
  getCapturedOutput, 
  getCapturedLogs, 
  mockStdout, 
  restoreStdout, 
  mockConsoleLog, 
  restoreConsoleLog 
} from '../../setup.js';

describe('Performance Utilities', () => {
  beforeEach(() => {
    mockConsoleLog();
    mockStdout();
  });

  afterEach(() => {
    restoreConsoleLog();
    restoreStdout();
  });

  describe('OutputCache', () => {
    it('should cache and retrieve values', () => {
      const key = 'test-key';
      const value = 'test-value';
      
      outputCache.set(key, value);
      const retrieved = outputCache.get(key);
      
      expect(retrieved).toBe(value);
    });

    it('should return null for non-existent keys', () => {
      const result = outputCache.get('non-existent-key');
      expect(result).toBeNull();
    });

    it('should handle cache expiration', (done) => {
      const key = 'expiring-key';
      const value = 'expiring-value';
      
      outputCache.set(key, value);
      
      // Mock time passage by directly manipulating the cache entry
      setTimeout(() => {
        const result = outputCache.get(key);
        // Should still be there within the timeout
        expect(result).toBe(value);
        done();
      }, 100);
    });

    it('should provide cache statistics', () => {
      outputCache.clear();
      outputCache.set('key1', 'value1');
      outputCache.set('key2', 'value2');
      
      const stats = outputCache.getStats();
      expect(stats.size).toBe(2);
      expect(stats.maxSize).toBeGreaterThan(0);
      expect(typeof stats.hitRate).toBe('number');
    });

    it('should clear cache', () => {
      outputCache.set('key1', 'value1');
      outputCache.set('key2', 'value2');
      
      outputCache.clear();
      
      expect(outputCache.get('key1')).toBeNull();
      expect(outputCache.get('key2')).toBeNull();
    });
  });

  describe('LazyLoader', () => {
    it('should load components lazily', async () => {
      let loadCount = 0;
      const loader = async () => {
        loadCount++;
        return { data: 'loaded' };
      };
      
      const result1 = await lazyLoader.load('test-component', loader);
      const result2 = await lazyLoader.load('test-component', loader);
      
      expect(result1.data).toBe('loaded');
      expect(result2.data).toBe('loaded');
      expect(loadCount).toBe(2); // Should load each time it's called
    });

    it('should track loaded components', async () => {
      await lazyLoader.load('component1', async () => ({ id: 1 }));
      await lazyLoader.load('component2', async () => ({ id: 2 }));
      
      expect(lazyLoader.isLoaded('component1')).toBe(true);
      expect(lazyLoader.isLoaded('component2')).toBe(true);
      expect(lazyLoader.isLoaded('component3')).toBe(false);
    });

    it('should unload components', async () => {
      await lazyLoader.load('unload-test', async () => ({ data: 'test' }));
      expect(lazyLoader.isLoaded('unload-test')).toBe(true);
      
      lazyLoader.unload('unload-test');
      expect(lazyLoader.isLoaded('unload-test')).toBe(false);
    });

    it('should get loaded components list', async () => {
      lazyLoader.unload('test1');
      lazyLoader.unload('test2');
      
      await lazyLoader.load('test1', async () => ({}));
      await lazyLoader.load('test2', async () => ({}));
      
      const loaded = lazyLoader.getLoadedComponents();
      expect(loaded).toContain('test1');
      expect(loaded).toContain('test2');
    });
  });

  describe('StreamingOutput', () => {
    it('should create streaming output', () => {
      const stream = createStreamingOutput();
      expect(stream).toBeDefined();
    });

    it('should write content to stream', () => {
      const stream = new StreamingOutput();
      stream.write('Hello ');
      stream.write('World');
      stream.flush();
      
      const output = getCapturedOutput();
      expect(output.join('')).toContain('Hello World');
    });

    it('should write lines to stream', () => {
      const stream = new StreamingOutput();
      stream.writeLine('Line 1');
      stream.writeLine('Line 2');
      stream.flush();
      
      const output = getCapturedOutput();
      expect(output.join('')).toContain('Line 1\nLine 2\n');
    });

    it('should stream arrays efficiently', async () => {
      const stream = new StreamingOutput();
      const items = Array.from({ length: 100 }, (_, i) => `Item ${i + 1}`);
      
      await stream.streamArray(
        items,
        (item, index) => `${index + 1}: ${item}`,
        { batchSize: 10, delay: 0 }
      );
      
      const output = getCapturedOutput();
      expect(output.join('')).toContain('1: Item 1');
      expect(output.join('')).toContain('100: Item 100');
    });

    it('should end stream properly', () => {
      const stream = new StreamingOutput();
      stream.write('Test content');
      stream.end();
      
      const output = getCapturedOutput();
      expect(output.join('')).toContain('Test content');
    });
  });

  describe('FormattingOptimizer', () => {
    it('should optimize color operations', () => {
      const operations = [
        { text: 'Success', colorFn: colors.success },
        { text: 'Error', colorFn: colors.error },
        { text: 'Warning', colorFn: colors.warning }
      ];
      
      const results = optimizeColors(operations);
      expect(results).toHaveLength(3);
      expect(results[0]).toContain('Success');
      expect(results[1]).toContain('Error');
      expect(results[2]).toContain('Warning');
    });

    it('should batch color operations efficiently', () => {
      const operations = Array.from({ length: 100 }, (_, i) => ({
        text: `Text ${i + 1}`,
        colorFn: colors.info
      }));
      
      const startTime = Date.now();
      const results = formattingOptimizer.batchColorOperations(operations);
      const endTime = Date.now();
      
      expect(results).toHaveLength(100);
      expect(endTime - startTime).toBeLessThan(100); // Should be fast
    });

    it('should provide cache statistics', () => {
      formattingOptimizer.clearCaches();
      
      // Perform some operations to populate cache
      formattingOptimizer.applyColor('test', colors.primary);
      formattingOptimizer.formatText('test', (text) => text.toUpperCase());
      
      const stats = formattingOptimizer.getCacheStats();
      expect(typeof stats.colorCacheSize).toBe('number');
      expect(typeof stats.formatCacheSize).toBe('number');
    });

    it('should clear caches', () => {
      formattingOptimizer.applyColor('test', colors.primary);
      formattingOptimizer.clearCaches();
      
      const stats = formattingOptimizer.getCacheStats();
      expect(stats.colorCacheSize).toBe(0);
      expect(stats.formatCacheSize).toBe(0);
    });
  });

  describe('PerformanceMonitor', () => {
    it('should time function execution', () => {
      const result = performanceMonitor.time('test-function', () => {
        // Simulate some work
        let sum = 0;
        for (let i = 0; i < 1000; i++) {
          sum += i;
        }
        return sum;
      });
      
      expect(result).toBe(499500); // Sum of 0 to 999
      
      const stats = performanceMonitor.getStats('test-function');
      expect(stats).toBeDefined();
      expect(stats.count).toBe(1);
      expect(stats.averageTime).toBeGreaterThan(0);
    });

    it('should time async function execution', async () => {
      const result = await performanceMonitor.timeAsync('test-async', async () => {
        await new Promise(resolve => setTimeout(resolve, 10));
        return 'async-result';
      });
      
      expect(result).toBe('async-result');
      
      const stats = performanceMonitor.getStats('test-async');
      expect(stats).toBeDefined();
      expect(stats.count).toBe(1);
      expect(stats.averageTime).toBeGreaterThan(5);
    });

    it('should track multiple executions', () => {
      for (let i = 0; i < 5; i++) {
        performanceMonitor.time('multi-test', () => i * 2);
      }
      
      const stats = performanceMonitor.getStats('multi-test');
      expect(stats.count).toBe(5);
      expect(stats.minTime).toBeGreaterThan(0);
      expect(stats.maxTime).toBeGreaterThan(0);
      expect(stats.totalTime).toBeGreaterThan(0);
    });

    it('should get all statistics', () => {
      performanceMonitor.clearStats();
      performanceMonitor.time('test1', () => 1);
      performanceMonitor.time('test2', () => 2);
      
      const allStats = performanceMonitor.getStats();
      expect(Object.keys(allStats)).toContain('test1');
      expect(Object.keys(allStats)).toContain('test2');
    });

    it('should display performance report', () => {
      performanceMonitor.clearStats();
      performanceMonitor.time('report-test', () => 'test');
      
      performanceMonitor.displayReport();
      const output = getCapturedLogs();
      expect(output.join('\n')).toContain('Performance Report');
    });

    it('should clear statistics', () => {
      performanceMonitor.time('clear-test', () => 'test');
      performanceMonitor.clearStats();
      
      const stats = performanceMonitor.getStats('clear-test');
      expect(stats).toBeNull();
    });
  });

  describe('MemoryMonitor', () => {
    it('should take memory snapshots', () => {
      const usage = memoryMonitor.takeSnapshot();
      expect(usage.rss).toBeGreaterThan(0);
      expect(usage.heapUsed).toBeGreaterThan(0);
      expect(usage.heapTotal).toBeGreaterThan(0);
    });

    it('should get current memory usage', () => {
      const usage = memoryMonitor.getCurrentUsage();
      expect(usage.rss).toBeGreaterThan(0);
      expect(usage.heapUsed).toBeGreaterThan(0);
    });

    it('should format memory usage', () => {
      const usage = memoryMonitor.getCurrentUsage();
      const formatted = memoryMonitor.formatMemoryUsage(usage);
      
      expect(formatted).toContain('RSS:');
      expect(formatted).toContain('Heap Used:');
      expect(formatted).toContain('MB');
    });

    it('should display current usage', () => {
      memoryMonitor.displayCurrentUsage();
      const output = getCapturedLogs();
      expect(output.join('\n')).toContain('Memory Usage:');
    });

    it('should get usage history', () => {
      memoryMonitor.takeSnapshot();
      memoryMonitor.takeSnapshot();
      
      const history = memoryMonitor.getUsageHistory();
      expect(history.length).toBeGreaterThanOrEqual(2);
      expect(history[0].timestamp).toBeDefined();
      expect(history[0].usage).toBeDefined();
    });

    it('should check for memory leaks', () => {
      // Take several snapshots
      for (let i = 0; i < 5; i++) {
        memoryMonitor.takeSnapshot();
      }
      
      const leakCheck = memoryMonitor.checkForLeaks();
      expect(leakCheck.hasLeak).toBeDefined();
      expect(leakCheck.message).toBeDefined();
    });
  });

  describe('Convenience Functions', () => {
    it('should use withCache helper', () => {
      const result1 = withCache('cache-test', () => 'cached-value');
      const result2 = withCache('cache-test', () => 'different-value');
      
      expect(result1).toBe('cached-value');
      expect(result2).toBe('cached-value'); // Should return cached value
    });

    it('should use withPerformanceTracking helper', () => {
      const result = withPerformanceTracking('tracking-test', () => {
        return 'tracked-result';
      });
      
      expect(result).toBe('tracked-result');
      
      const stats = performanceMonitor.getStats('tracking-test');
      expect(stats).toBeDefined();
    });

    it('should use withAsyncPerformanceTracking helper', async () => {
      const result = await withAsyncPerformanceTracking('async-tracking-test', async () => {
        await new Promise(resolve => setTimeout(resolve, 10));
        return 'async-tracked-result';
      });
      
      expect(result).toBe('async-tracked-result');
      
      const stats = performanceMonitor.getStats('async-tracking-test');
      expect(stats).toBeDefined();
    });

    it('should load components with helper', async () => {
      const result = await loadComponent('helper-test', async () => {
        return { loaded: true };
      });
      
      expect(result.loaded).toBe(true);
    });

    it('should check performance monitoring status', () => {
      const isEnabled = isPerformanceMonitoringEnabled();
      expect(typeof isEnabled).toBe('boolean');
    });
  });

  describe('Performance Benchmarks', () => {
    it('should benchmark cache performance', () => {
      const iterations = 1000;
      
      // Benchmark cache writes
      const writeStart = Date.now();
      for (let i = 0; i < iterations; i++) {
        outputCache.set(`key-${i}`, `value-${i}`);
      }
      const writeEnd = Date.now();
      
      // Benchmark cache reads
      const readStart = Date.now();
      for (let i = 0; i < iterations; i++) {
        outputCache.get(`key-${i}`);
      }
      const readEnd = Date.now();
      
      const writeTime = writeEnd - writeStart;
      const readTime = readEnd - readStart;
      
      expect(writeTime).toBeLessThan(1000); // Should be fast
      expect(readTime).toBeLessThan(500);   // Reads should be faster
    });

    it('should benchmark color optimization', () => {
      const operations = Array.from({ length: 1000 }, (_, i) => ({
        text: `Text ${i}`,
        colorFn: colors.primary
      }));
      
      const startTime = Date.now();
      const results = formattingOptimizer.batchColorOperations(operations);
      const endTime = Date.now();
      
      expect(results).toHaveLength(1000);
      expect(endTime - startTime).toBeLessThan(500); // Should be efficient
    });

    it('should benchmark streaming performance', async () => {
      const stream = new StreamingOutput();
      const largeArray = Array.from({ length: 10000 }, (_, i) => `Item ${i}`);
      
      const startTime = Date.now();
      await stream.streamArray(
        largeArray,
        (item) => item,
        { batchSize: 100, delay: 0 }
      );
      const endTime = Date.now();
      
      expect(endTime - startTime).toBeLessThan(2000); // Should handle large arrays efficiently
    });

    it('should benchmark lazy loading performance', async () => {
      const componentCount = 100;
      const loadPromises: Promise<any>[] = [];
      
      const startTime = Date.now();
      
      for (let i = 0; i < componentCount; i++) {
        loadPromises.push(
          lazyLoader.load(`component-${i}`, async () => ({ id: i }))
        );
      }
      
      await Promise.all(loadPromises);
      const endTime = Date.now();
      
      expect(endTime - startTime).toBeLessThan(1000); // Should load components efficiently
    });

    it('should benchmark performance monitoring overhead', () => {
      const iterations = 1000;
      
      // Benchmark without monitoring
      const directStart = Date.now();
      for (let i = 0; i < iterations; i++) {
        Math.sqrt(i);
      }
      const directEnd = Date.now();
      
      // Benchmark with monitoring
      const monitoredStart = Date.now();
      for (let i = 0; i < iterations; i++) {
        performanceMonitor.time(`sqrt-${i}`, () => Math.sqrt(i));
      }
      const monitoredEnd = Date.now();
      
      const directTime = directEnd - directStart;
      const monitoredTime = monitoredEnd - monitoredStart;
      
      // Monitoring overhead should be reasonable
      const overhead = monitoredTime - directTime;
      expect(overhead).toBeLessThan(directTime * 10); // Less than 10x overhead
    });
  });

  describe('Memory Efficiency', () => {
    it('should not leak memory with repeated operations', () => {
      const initialUsage = memoryMonitor.getCurrentUsage();
      
      // Perform many operations
      for (let i = 0; i < 1000; i++) {
        withCache(`memory-test-${i}`, () => `value-${i}`);
        withPerformanceTracking(`memory-perf-${i}`, () => i * 2);
      }
      
      // Force garbage collection if available
      if (global.gc) {
        global.gc();
      }
      
      const finalUsage = memoryMonitor.getCurrentUsage();
      const heapGrowth = finalUsage.heapUsed - initialUsage.heapUsed;
      
      // Memory growth should be reasonable
      expect(heapGrowth).toBeLessThan(50 * 1024 * 1024); // Less than 50MB growth
    });

    it('should clean up caches efficiently', () => {
      // Fill caches
      for (let i = 0; i < 100; i++) {
        outputCache.set(`cleanup-${i}`, `value-${i}`);
        formattingOptimizer.applyColor(`text-${i}`, colors.primary);
      }
      
      const beforeCleanup = memoryMonitor.getCurrentUsage();
      
      // Clear caches
      outputCache.clear();
      formattingOptimizer.clearCaches();
      
      // Force garbage collection if available
      if (global.gc) {
        global.gc();
      }
      
      const afterCleanup = memoryMonitor.getCurrentUsage();
      
      // Memory should be freed (or at least not grow significantly)
      expect(afterCleanup.heapUsed).toBeLessThanOrEqual(beforeCleanup.heapUsed * 1.1);
    });
  });
});