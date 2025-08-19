#!/usr/bin/env tsx

/**
 * Test runner for visual components
 * Provides different test execution modes and reporting
 */

import { execSync } from 'child_process';
import { existsSync } from 'fs';
import { join } from 'path';

interface TestOptions {
  watch?: boolean;
  coverage?: boolean;
  verbose?: boolean;
  pattern?: string;
  updateSnapshots?: boolean;
  performance?: boolean;
  crossPlatform?: boolean;
  bail?: boolean;
}

class TestRunner {
  private options: TestOptions;

  constructor(options: TestOptions = {}) {
    this.options = options;
  }

  run(): void {
    console.log('🧪 Running Visual Component Tests\n');

    // Check if Jest config exists
    if (!existsSync('jest.config.js')) {
      console.error('❌ Jest configuration not found. Please run from project root.');
      process.exit(1);
    }

    const jestArgs = this.buildJestArgs();
    const command = `npx jest ${jestArgs.join(' ')}`;

    console.log(`📋 Command: ${command}\n`);

    try {
      execSync(command, { 
        stdio: 'inherit',
        env: {
          ...process.env,
          NODE_ENV: 'test',
          // Enable performance monitoring for performance tests
          ...(this.options.performance && { AP_PERFORMANCE_MONITORING: 'true' })
        }
      });
      
      console.log('\n✅ All tests completed successfully!');
      
      if (this.options.coverage) {
        console.log('\n📊 Coverage report generated in ./coverage/');
      }
      
    } catch (error) {
      console.error('\n❌ Tests failed!');
      process.exit(1);
    }
  }

  private buildJestArgs(): string[] {
    const args: string[] = [];

    // Test pattern
    if (this.options.pattern) {
      args.push(`--testNamePattern="${this.options.pattern}"`);
    }

    // Watch mode
    if (this.options.watch) {
      args.push('--watch');
    }

    // Coverage
    if (this.options.coverage) {
      args.push('--coverage');
    }

    // Verbose output
    if (this.options.verbose) {
      args.push('--verbose');
    }

    // Update snapshots
    if (this.options.updateSnapshots) {
      args.push('--updateSnapshot');
    }

    // Bail on first failure
    if (this.options.bail) {
      args.push('--bail');
    }

    // Specific test suites
    if (this.options.performance) {
      args.push('--testPathPattern="Performance|Benchmark"');
    }

    if (this.options.crossPlatform) {
      args.push('--testPathPattern="CrossPlatform"');
    }

    return args;
  }

  static printUsage(): void {
    console.log(`
🧪 Visual Component Test Runner

Usage: npm run test [options]

Options:
  --watch              Run tests in watch mode
  --coverage           Generate coverage report
  --verbose            Show detailed test output
  --pattern <pattern>  Run tests matching pattern
  --update-snapshots   Update test snapshots
  --performance        Run performance tests only
  --cross-platform     Run cross-platform tests only
  --bail               Stop on first test failure
  --help               Show this help message

Examples:
  npm run test                           # Run all tests
  npm run test -- --watch                # Run in watch mode
  npm run test -- --coverage             # Run with coverage
  npm run test -- --pattern "Banner"     # Run Banner tests only
  npm run test -- --update-snapshots     # Update snapshots
  npm run test -- --performance          # Run performance tests
  npm run test -- --cross-platform       # Run cross-platform tests
  npm run test -- --verbose --bail       # Verbose output, stop on failure

Test Categories:
  📦 Component Tests     - Unit tests for visual components
  📸 Snapshot Tests      - Visual output regression tests
  ⚡ Performance Tests   - Benchmarks and optimization tests
  🌍 Cross-Platform     - Platform compatibility tests
  🎯 Integration Tests   - End-to-end component integration
    `);
  }
}

// Parse command line arguments
function parseArgs(): TestOptions {
  const args = process.argv.slice(2);
  const options: TestOptions = {};

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    switch (arg) {
      case '--watch':
        options.watch = true;
        break;
      case '--coverage':
        options.coverage = true;
        break;
      case '--verbose':
        options.verbose = true;
        break;
      case '--pattern':
        options.pattern = args[++i];
        break;
      case '--update-snapshots':
        options.updateSnapshots = true;
        break;
      case '--performance':
        options.performance = true;
        break;
      case '--cross-platform':
        options.crossPlatform = true;
        break;
      case '--bail':
        options.bail = true;
        break;
      case '--help':
        TestRunner.printUsage();
        process.exit(0);
        break;
    }
  }

  return options;
}

// Main execution
if (require.main === module) {
  const options = parseArgs();
  const runner = new TestRunner(options);
  runner.run();
}

export { TestRunner, TestOptions };