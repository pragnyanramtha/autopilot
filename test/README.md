# Visual CLI Enhancement Test Suite

This directory contains comprehensive tests for the visual CLI enhancement components, including unit tests, performance benchmarks, cross-platform compatibility tests, and snapshot tests.

## Test Structure

```
test/
├── setup.ts                    # Test setup and utilities
├── run-tests.ts               # Custom test runner
├── README.md                  # This file
├── ui/
│   ├── components/
│   │   ├── Banner.test.ts           # Banner component tests
│   │   ├── ProgressBar.test.ts      # Progress bar component tests
│   │   ├── StatusIndicator.test.ts  # Status indicator tests
│   │   ├── Table.test.ts            # Table component tests
│   │   └── Snapshots.test.ts        # Visual output snapshots
│   └── utils/
│       ├── Performance.test.ts      # Performance utility tests
│       └── CrossPlatform.test.ts    # Cross-platform compatibility
└── __snapshots__/             # Jest snapshots (auto-generated)
```

## Test Categories

### 🧪 Unit Tests
- **Component Tests**: Test individual visual components (Banner, StatusIndicator, Table, ProgressBar)
- **Utility Tests**: Test utility functions (Colors, Symbols, Layout, Performance)
- **Integration Tests**: Test component interactions and workflows

### 📸 Snapshot Tests
- **Visual Regression**: Ensure consistent output formatting across changes
- **Layout Tests**: Verify responsive behavior and terminal adaptation
- **Cross-Platform Output**: Consistent rendering across different platforms

### ⚡ Performance Tests
- **Benchmarks**: Measure rendering performance and optimization effectiveness
- **Memory Tests**: Monitor memory usage and detect leaks
- **Caching Tests**: Verify cache efficiency and hit rates
- **Streaming Tests**: Test large output handling

### 🌍 Cross-Platform Tests
- **Platform Detection**: Test platform-specific optimizations
- **Terminal Compatibility**: Verify support across different terminals
- **Encoding Support**: Test Unicode, ASCII, and accessibility modes
- **Color Support**: Test color detection and fallbacks

## Running Tests

### Basic Commands

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage report
npm run test:coverage

# Run specific test categories
npm run test:components      # Component tests only
npm run test:performance     # Performance benchmarks
npm run test:cross-platform  # Cross-platform tests
npm run test:snapshots       # Snapshot tests only
npm run test:utils          # Utility tests only

# Update snapshots
npm run test:update-snapshots

# CI/CD optimized run
npm run test:ci
```

### Advanced Usage

```bash
# Run specific test patterns
npm test -- --pattern "Banner"
npm test -- --pattern "Performance"

# Verbose output
npm test -- --verbose

# Stop on first failure
npm test -- --bail

# Run with performance monitoring
npm test -- --performance

# Help and options
npm test -- --help
```

## Test Configuration

### Jest Configuration
- **Framework**: Jest with TypeScript support
- **Environment**: Node.js with mocked terminal capabilities
- **Coverage**: Comprehensive coverage reporting with HTML output
- **Snapshots**: Automated visual regression testing

### Environment Setup
Tests run with consistent environment settings:
- Terminal width: 80 columns (configurable per test)
- Platform: Linux (overridable for cross-platform tests)
- Colors: Disabled for consistent snapshots
- Unicode: ASCII mode for snapshot consistency

## Writing Tests

### Test Structure
```typescript
import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { ComponentName } from '../../../src/ui/components/ComponentName.js';
import { getCapturedLogs, mockConsoleLog, restoreConsoleLog } from '../../setup.js';

describe('ComponentName', () => {
  beforeEach(() => {
    mockConsoleLog();
  });

  afterEach(() => {
    restoreConsoleLog();
  });

  it('should test specific functionality', () => {
    ComponentName.method();
    const output = getCapturedLogs();
    expect(output).toContain('expected content');
  });
});
```

### Snapshot Testing
```typescript
it('should match component output snapshot', () => {
  Component.render();
  const output = getCapturedLogs().join('\n');
  expect(output).toMatchSnapshot('component-output');
});
```

### Performance Testing
```typescript
it('should perform efficiently', () => {
  const startTime = Date.now();
  
  // Perform operations
  for (let i = 0; i < 1000; i++) {
    Component.operation();
  }
  
  const endTime = Date.now();
  expect(endTime - startTime).toBeLessThan(1000);
});
```

### Cross-Platform Testing
```typescript
it('should work across platforms', () => {
  const platforms = ['linux', 'darwin', 'win32'];
  
  platforms.forEach(platform => {
    Object.defineProperty(process, 'platform', { value: platform });
    Component.render();
    const output = getCapturedLogs();
    expect(output.length).toBeGreaterThan(0);
  });
});
```

## Test Utilities

### Setup Functions
- `mockConsoleLog()`: Capture console output
- `mockStdout()`: Capture stdout writes
- `mockTerminalCapabilities()`: Set consistent terminal environment
- `getCapturedLogs()`: Retrieve captured console output
- `getCapturedOutput()`: Retrieve captured stdout output

### Performance Utilities
- `withPerformanceTracking()`: Measure execution time
- `memoryMonitor`: Track memory usage
- `outputCache`: Test caching functionality

## Coverage Requirements

### Minimum Coverage Targets
- **Statements**: 90%
- **Branches**: 85%
- **Functions**: 90%
- **Lines**: 90%

### Coverage Reports
- **HTML**: `coverage/lcov-report/index.html`
- **LCOV**: `coverage/lcov.info`
- **Text**: Console output during test run

## Performance Benchmarks

### Target Performance Metrics
- **Component Rendering**: < 10ms per component
- **Large Table Rendering**: < 100ms for 1000 rows
- **Cache Hit Rate**: > 80% for repeated operations
- **Memory Growth**: < 50MB for 1000 operations
- **Streaming Throughput**: > 1000 items/second

### Benchmark Tests
Performance tests automatically run benchmarks and compare against targets:
- Rendering speed tests
- Memory usage monitoring
- Cache efficiency measurement
- Cross-platform performance comparison

## Continuous Integration

### CI Configuration
```yaml
# Example GitHub Actions configuration
- name: Run Tests
  run: npm run test:ci
  
- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage/lcov.info
```

### Pre-commit Hooks
```bash
# Run tests before commit
npm run test:components
npm run test:performance
```

## Troubleshooting

### Common Issues

#### Snapshot Mismatches
```bash
# Update snapshots after intentional changes
npm run test:update-snapshots

# Review snapshot differences
git diff test/__snapshots__/
```

#### Performance Test Failures
```bash
# Run performance tests in isolation
npm run test:performance -- --verbose

# Check system resources during tests
npm run test:performance -- --pattern "memory"
```

#### Cross-Platform Issues
```bash
# Test specific platform
npm run test:cross-platform -- --pattern "Windows"

# Debug platform detection
npm test -- --pattern "Platform Detection" --verbose
```

### Environment Issues
- Ensure Node.js >= 18.0.0
- Clear Jest cache: `npx jest --clearCache`
- Reset test environment: `rm -rf coverage/ test/__snapshots__/`

## Contributing

### Adding New Tests
1. Create test file in appropriate directory
2. Follow existing test patterns and naming conventions
3. Include both positive and negative test cases
4. Add performance benchmarks for new components
5. Update snapshots if visual output changes
6. Ensure cross-platform compatibility

### Test Guidelines
- Write descriptive test names
- Use consistent setup/teardown patterns
- Mock external dependencies
- Test edge cases and error conditions
- Include performance considerations
- Document complex test scenarios

### Review Checklist
- [ ] All tests pass locally
- [ ] Coverage meets minimum requirements
- [ ] Snapshots are up to date
- [ ] Performance benchmarks pass
- [ ] Cross-platform tests pass
- [ ] No memory leaks detected
- [ ] Documentation updated if needed