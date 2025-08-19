import { colors } from './Colors.js';
import { symbols } from './Symbols.js';
import { Layout } from './Layout.js';

// Cache for formatted output to avoid recomputation
class OutputCache {
  private cache = new Map<string, { value: string; timestamp: number; hits: number }>();
  private maxSize = 1000;
  private maxAge = 5 * 60 * 1000; // 5 minutes

  get(key: string): string | null {
    const entry = this.cache.get(key);
    if (!entry) return null;

    // Check if entry is expired
    if (Date.now() - entry.timestamp > this.maxAge) {
      this.cache.delete(key);
      return null;
    }

    entry.hits++;
    return entry.value;
  }

  set(key: string, value: string): void {
    // Clean up old entries if cache is full
    if (this.cache.size >= this.maxSize) {
      this.cleanup();
    }

    this.cache.set(key, {
      value,
      timestamp: Date.now(),
      hits: 0
    });
  }

  private cleanup(): void {
    const now = Date.now();
    const entries = Array.from(this.cache.entries());
    
    // Remove expired entries first
    entries.forEach(([key, entry]) => {
      if (now - entry.timestamp > this.maxAge) {
        this.cache.delete(key);
      }
    });

    // If still too large, remove least recently used entries
    if (this.cache.size >= this.maxSize) {
      const sortedEntries = entries
        .filter(([key]) => this.cache.has(key))
        .sort((a, b) => a[1].hits - b[1].hits);
      
      const toRemove = Math.floor(this.maxSize * 0.2); // Remove 20%
      for (let i = 0; i < toRemove && i < sortedEntries.length; i++) {
        this.cache.delete(sortedEntries[i][0]);
      }
    }
  }

  clear(): void {
    this.cache.clear();
  }

  getStats(): { size: number; maxSize: number; hitRate: number } {
    const entries = Array.from(this.cache.values());
    const totalHits = entries.reduce((sum, entry) => sum + entry.hits, 0);
    const totalRequests = entries.length + totalHits;
    const hitRate = totalRequests > 0 ? totalHits / totalRequests : 0;

    return {
      size: this.cache.size,
      maxSize: this.maxSize,
      hitRate
    };
  }
}

// Global output cache instance
const outputCache = new OutputCache();

// Lazy loading utility for visual components
class LazyLoader {
  private loadedComponents = new Set<string>();
  private loadPromises = new Map<string, Promise<any>>();

  async load<T>(componentName: string, loader: () => Promise<T>): Promise<T> {
    if (this.loadedComponents.has(componentName)) {
      return loader(); // Already loaded, just return
    }

    if (this.loadPromises.has(componentName)) {
      return this.loadPromises.get(componentName)!;
    }

    const promise = loader().then(result => {
      this.loadedComponents.add(componentName);
      this.loadPromises.delete(componentName);
      return result;
    }).catch(error => {
      this.loadPromises.delete(componentName);
      throw error;
    });

    this.loadPromises.set(componentName, promise);
    return promise;
  }

  isLoaded(componentName: string): boolean {
    return this.loadedComponents.has(componentName);
  }

  unload(componentName: string): void {
    this.loadedComponents.delete(componentName);
    this.loadPromises.delete(componentName);
  }

  getLoadedComponents(): string[] {
    return Array.from(this.loadedComponents);
  }
}

// Global lazy loader instance
const lazyLoader = new LazyLoader();

// Streaming output utility for large content
class StreamingOutput {
  private buffer: string[] = [];
  private bufferSize = 0;
  private maxBufferSize = 8192; // 8KB buffer
  private flushThreshold = 4096; // 4KB flush threshold

  write(content: string): void {
    this.buffer.push(content);
    this.bufferSize += content.length;

    if (this.bufferSize >= this.flushThreshold) {
      this.flush();
    }
  }

  writeLine(content: string): void {
    this.write(content + '\n');
  }

  flush(): void {
    if (this.buffer.length > 0) {
      process.stdout.write(this.buffer.join(''));
      this.buffer = [];
      this.bufferSize = 0;
    }
  }

  end(): void {
    this.flush();
  }

  // Stream large arrays of data
  streamArray<T>(
    items: T[], 
    formatter: (item: T, index: number) => string,
    options?: { batchSize?: number; delay?: number }
  ): Promise<void> {
    const opts = { batchSize: 100, delay: 0, ...options };
    
    return new Promise((resolve) => {
      let index = 0;
      
      const processBatch = () => {
        const endIndex = Math.min(index + opts.batchSize, items.length);
        
        for (let i = index; i < endIndex; i++) {
          this.writeLine(formatter(items[i], i));
        }
        
        index = endIndex;
        
        if (index >= items.length) {
          this.end();
          resolve();
        } else if (opts.delay > 0) {
          setTimeout(processBatch, opts.delay);
        } else {
          setImmediate(processBatch);
        }
      };
      
      processBatch();
    });
  }
}

// Color and formatting operation optimizations
class FormattingOptimizer {
  private colorCache = new Map<string, string>();
  private formatCache = new Map<string, string>();

  // Optimized color application with caching
  applyColor(text: string, colorFn: (text: string) => string): string {
    const cacheKey = `${colorFn.toString()}_${text}`;
    
    let cached = this.colorCache.get(cacheKey);
    if (cached !== undefined) {
      return cached;
    }

    const result = colorFn(text);
    this.colorCache.set(cacheKey, result);
    return result;
  }

  // Batch color operations for better performance
  batchColorOperations(
    operations: Array<{ text: string; colorFn: (text: string) => string }>
  ): string[] {
    return operations.map(op => this.applyColor(op.text, op.colorFn));
  }

  // Optimized text formatting with caching
  formatText(text: string, formatter: (text: string) => string): string {
    const cacheKey = `${formatter.toString()}_${text}`;
    
    let cached = this.formatCache.get(cacheKey);
    if (cached !== undefined) {
      return cached;
    }

    const result = formatter(text);
    this.formatCache.set(cacheKey, result);
    return result;
  }

  // Clear caches to free memory
  clearCaches(): void {
    this.colorCache.clear();
    this.formatCache.clear();
  }

  // Get cache statistics
  getCacheStats(): { colorCacheSize: number; formatCacheSize: number } {
    return {
      colorCacheSize: this.colorCache.size,
      formatCacheSize: this.formatCache.size
    };
  }
}

// Global formatting optimizer instance
const formattingOptimizer = new FormattingOptimizer();

// Performance monitoring utilities
class PerformanceMonitor {
  private metrics = new Map<string, { 
    count: number; 
    totalTime: number; 
    minTime: number; 
    maxTime: number; 
    lastTime: number;
  }>();

  // Time a function execution
  time<T>(name: string, fn: () => T): T {
    const start = performance.now();
    const result = fn();
    const end = performance.now();
    
    this.recordMetric(name, end - start);
    return result;
  }

  // Time an async function execution
  async timeAsync<T>(name: string, fn: () => Promise<T>): Promise<T> {
    const start = performance.now();
    const result = await fn();
    const end = performance.now();
    
    this.recordMetric(name, end - start);
    return result;
  }

  private recordMetric(name: string, time: number): void {
    const existing = this.metrics.get(name);
    
    if (existing) {
      existing.count++;
      existing.totalTime += time;
      existing.minTime = Math.min(existing.minTime, time);
      existing.maxTime = Math.max(existing.maxTime, time);
      existing.lastTime = time;
    } else {
      this.metrics.set(name, {
        count: 1,
        totalTime: time,
        minTime: time,
        maxTime: time,
        lastTime: time
      });
    }
  }

  // Get performance statistics
  getStats(name?: string): any {
    if (name) {
      const metric = this.metrics.get(name);
      if (!metric) return null;
      
      return {
        name,
        count: metric.count,
        averageTime: metric.totalTime / metric.count,
        minTime: metric.minTime,
        maxTime: metric.maxTime,
        lastTime: metric.lastTime,
        totalTime: metric.totalTime
      };
    }

    const allStats: any = {};
    for (const [metricName, metric] of this.metrics) {
      allStats[metricName] = {
        count: metric.count,
        averageTime: metric.totalTime / metric.count,
        minTime: metric.minTime,
        maxTime: metric.maxTime,
        lastTime: metric.lastTime,
        totalTime: metric.totalTime
      };
    }
    
    return allStats;
  }

  // Clear all metrics
  clearStats(): void {
    this.metrics.clear();
  }

  // Display performance report
  displayReport(): void {
    const stats = this.getStats();
    const entries = Object.entries(stats);
    
    if (entries.length === 0) {
      console.log(colors.muted('No performance metrics recorded'));
      return;
    }

    console.log(colors.primaryBold('Performance Report'));
    console.log(colors.muted('─'.repeat(60)));
    
    entries
      .sort((a, b) => (b[1] as any).totalTime - (a[1] as any).totalTime)
      .forEach(([name, metric]: [string, any]) => {
        console.log(colors.accent(name));
        console.log(`  Count: ${colors.info(metric.count.toString())}`);
        console.log(`  Average: ${colors.warning(metric.averageTime.toFixed(2))}ms`);
        console.log(`  Min/Max: ${colors.success(metric.minTime.toFixed(2))}ms / ${colors.error(metric.maxTime.toFixed(2))}ms`);
        console.log(`  Total: ${colors.primary(metric.totalTime.toFixed(2))}ms`);
        console.log();
      });
  }
}

// Global performance monitor instance
const performanceMonitor = new PerformanceMonitor();

// Memory usage monitoring
class MemoryMonitor {
  private snapshots: Array<{ timestamp: number; usage: NodeJS.MemoryUsage }> = [];
  private maxSnapshots = 100;

  takeSnapshot(): NodeJS.MemoryUsage {
    const usage = process.memoryUsage();
    this.snapshots.push({
      timestamp: Date.now(),
      usage
    });

    // Keep only recent snapshots
    if (this.snapshots.length > this.maxSnapshots) {
      this.snapshots = this.snapshots.slice(-this.maxSnapshots);
    }

    return usage;
  }

  getCurrentUsage(): NodeJS.MemoryUsage {
    return process.memoryUsage();
  }

  getUsageHistory(): Array<{ timestamp: number; usage: NodeJS.MemoryUsage }> {
    return [...this.snapshots];
  }

  formatMemoryUsage(usage: NodeJS.MemoryUsage): string {
    const formatBytes = (bytes: number): string => {
      const mb = bytes / 1024 / 1024;
      return `${mb.toFixed(2)} MB`;
    };

    return [
      `RSS: ${formatBytes(usage.rss)}`,
      `Heap Used: ${formatBytes(usage.heapUsed)}`,
      `Heap Total: ${formatBytes(usage.heapTotal)}`,
      `External: ${formatBytes(usage.external)}`
    ].join(' | ');
  }

  displayCurrentUsage(): void {
    const usage = this.getCurrentUsage();
    console.log(colors.info('Memory Usage: ') + colors.muted(this.formatMemoryUsage(usage)));
  }

  // Check for potential memory leaks
  checkForLeaks(): { hasLeak: boolean; message: string } {
    if (this.snapshots.length < 10) {
      return { hasLeak: false, message: 'Not enough data to detect leaks' };
    }

    const recent = this.snapshots.slice(-10);
    const first = recent[0].usage.heapUsed;
    const last = recent[recent.length - 1].usage.heapUsed;
    const growth = last - first;
    const growthPercent = (growth / first) * 100;

    if (growthPercent > 50) { // 50% growth in recent snapshots
      return {
        hasLeak: true,
        message: `Potential memory leak detected: ${growthPercent.toFixed(1)}% growth in heap usage`
      };
    }

    return { hasLeak: false, message: 'No memory leaks detected' };
  }
}

// Global memory monitor instance
const memoryMonitor = new MemoryMonitor();

// Export all performance utilities
export {
  OutputCache,
  outputCache,
  LazyLoader,
  lazyLoader,
  StreamingOutput,
  FormattingOptimizer,
  formattingOptimizer,
  PerformanceMonitor,
  performanceMonitor,
  MemoryMonitor,
  memoryMonitor
};

// Convenience functions for common operations
export function withCache<T>(key: string, generator: () => T): T {
  const cached = outputCache.get(key);
  if (cached !== null) {
    return cached as T;
  }

  const result = generator();
  if (typeof result === 'string') {
    outputCache.set(key, result);
  }
  return result;
}

export function withPerformanceTracking<T>(name: string, fn: () => T): T {
  return performanceMonitor.time(name, fn);
}

export async function withAsyncPerformanceTracking<T>(name: string, fn: () => Promise<T>): Promise<T> {
  return performanceMonitor.timeAsync(name, fn);
}

export function createStreamingOutput(): StreamingOutput {
  return new StreamingOutput();
}

export function optimizeColors(operations: Array<{ text: string; colorFn: (text: string) => string }>): string[] {
  return formattingOptimizer.batchColorOperations(operations);
}

// Performance-optimized component loader
export async function loadComponent<T>(name: string, loader: () => Promise<T>): Promise<T> {
  return lazyLoader.load(name, loader);
}

// Utility to check if performance monitoring is enabled
export function isPerformanceMonitoringEnabled(): boolean {
  return process.env.KIRA_PERFORMANCE_MONITORING === 'true' || process.env.NODE_ENV === 'development';
}

// Auto-cleanup function to prevent memory leaks
export function setupPerformanceCleanup(): void {
  // Clean up caches periodically
  setInterval(() => {
    outputCache.clear();
    formattingOptimizer.clearCaches();
    
    // Check for memory leaks
    memoryMonitor.takeSnapshot();
    const leakCheck = memoryMonitor.checkForLeaks();
    if (leakCheck.hasLeak && isPerformanceMonitoringEnabled()) {
      console.warn(colors.warning(`⚠ ${leakCheck.message}`));
    }
  }, 5 * 60 * 1000); // Every 5 minutes

  // Clean up on process exit
  process.on('exit', () => {
    if (isPerformanceMonitoringEnabled()) {
      console.log(colors.muted('\nPerformance cleanup completed'));
    }
  });
}

// Initialize performance monitoring if enabled
if (isPerformanceMonitoringEnabled()) {
  setupPerformanceCleanup();
}