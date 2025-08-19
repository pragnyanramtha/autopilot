import { terminalCapabilities, terminalAdapter, ColorSupport } from './index.js';
import { visualPreferences } from '../preferences/index.js';
import { StatusIndicator } from '../components/StatusIndicator.js';
import { Table } from '../components/Table.js';
import chalk from 'chalk';

/**
 * Test and demonstration of terminal capabilities
 */
export class TerminalCapabilitiesTest {
  
  /**
   * Run comprehensive terminal capability tests
   */
  public static async runTests(): Promise<void> {
    console.log(chalk.cyan.bold('\n🔍 Terminal Capability Detection Test\n'));
    
    try {
      // Initialize terminal detection
      console.log('Detecting terminal capabilities...');
      const capabilities = await terminalCapabilities.detect();
      
      // Initialize adaptive configuration
      console.log('Initializing adaptive configuration...');
      await terminalAdapter.initialize();
      const config = await terminalAdapter.getConfig();
      
      // Display results
      this.displayCapabilities(capabilities);
      this.displayAdaptiveConfig(config);
      
      // Test adaptive features
      await this.testAdaptiveFeatures();
      
      StatusIndicator.success('Terminal capability detection completed successfully');
      
    } catch (error) {
      StatusIndicator.error(`Terminal capability detection failed: ${error instanceof Error ? error.message : error}`);
    }
  }
  
  /**
   * Display detected terminal capabilities
   */
  private static displayCapabilities(capabilities: any): void {
    console.log(chalk.yellow.bold('\n📊 Detected Terminal Capabilities\n'));
    
    // Basic info table
    const basicTable = new Table([
      { header: 'Property', key: 'property', width: 25 },
      { header: 'Value', key: 'value', width: 40 },
      { header: 'Description', key: 'description', width: 35 }
    ]);
    
    basicTable.addRow({
      property: 'Terminal Name',
      value: capabilities.name,
      description: 'Detected terminal application'
    });
    
    basicTable.addRow({
      property: 'Version',
      value: capabilities.version,
      description: 'Terminal version if available'
    });
    
    basicTable.addRow({
      property: 'Program',
      value: capabilities.program,
      description: 'Terminal program identifier'
    });
    
    basicTable.addRow({
      property: 'Platform',
      value: capabilities.platform,
      description: 'Operating system platform'
    });
    
    console.log(basicTable.render());
    
    // Display capabilities table
    const capabilitiesTable = new Table([
      { header: 'Capability', key: 'capability', width: 25 },
      { header: 'Supported', key: 'supported', width: 15 },
      { header: 'Details', key: 'details', width: 60 }
    ]);
    
    capabilitiesTable.addRow({
      capability: 'Color Support',
      supported: this.getColorSupportText(capabilities.colorSupport),
      details: `Level ${capabilities.colorSupport}: ${this.getColorDescription(capabilities.colorSupport)}`
    });
    
    capabilitiesTable.addRow({
      capability: 'Unicode',
      supported: capabilities.supportsUnicode ? '✓ Yes' : '✗ No',
      details: capabilities.supportsUnicode ? 'Full Unicode character support' : 'Limited to ASCII characters'
    });
    
    capabilitiesTable.addRow({
      capability: 'Emoji',
      supported: capabilities.supportsEmoji ? '✓ Yes' : '✗ No',
      details: capabilities.supportsEmoji ? 'Emoji rendering supported' : 'Emoji may not display correctly'
    });
    
    capabilitiesTable.addRow({
      capability: 'Hyperlinks',
      supported: capabilities.supportsHyperlinks ? '✓ Yes' : '✗ No',
      details: capabilities.supportsHyperlinks ? 'OSC 8 hyperlink support' : 'No clickable link support'
    });
    
    capabilitiesTable.addRow({
      capability: 'Mouse Events',
      supported: capabilities.supportsMouseEvents ? '✓ Yes' : '✗ No',
      details: capabilities.supportsMouseEvents ? 'Mouse interaction supported' : 'Keyboard-only interaction'
    });
    
    console.log(capabilitiesTable.render());
    
    // Environment info table
    const envTable = new Table([
      { header: 'Environment', key: 'env', width: 25 },
      { header: 'Status', key: 'status', width: 15 },
      { header: 'Impact', key: 'impact', width: 60 }
    ]);
    
    envTable.addRow({
      env: 'Interactive Mode',
      status: capabilities.isInteractive ? '✓ Yes' : '✗ No',
      impact: capabilities.isInteractive ? 'Full interactive features available' : 'Limited to batch output'
    });
    
    envTable.addRow({
      env: 'TTY',
      status: capabilities.isTTY ? '✓ Yes' : '✗ No',
      impact: capabilities.isTTY ? 'Terminal control sequences work' : 'Plain text output only'
    });
    
    envTable.addRow({
      env: 'SSH Connection',
      status: capabilities.isSSH ? '⚠ Yes' : '✓ Local',
      impact: capabilities.isSSH ? 'Network latency may affect performance' : 'Local terminal performance'
    });
    
    envTable.addRow({
      env: 'WSL',
      status: capabilities.isWSL ? '⚠ Yes' : '✓ Native',
      impact: capabilities.isWSL ? 'Windows Subsystem for Linux detected' : 'Native Linux/macOS environment'
    });
    
    console.log(envTable.render());
    
    // Accessibility info
    const accessibilityTable = new Table([
      { header: 'Accessibility', key: 'accessibility', width: 25 },
      { header: 'Status', key: 'status', width: 15 },
      { header: 'Recommendation', key: 'recommendation', width: 60 }
    ]);
    
    accessibilityTable.addRow({
      accessibility: 'High Contrast',
      status: capabilities.isHighContrast ? '✓ Enabled' : '○ Normal',
      recommendation: capabilities.isHighContrast ? 'Using high contrast theme' : 'Standard contrast available'
    });
    
    accessibilityTable.addRow({
      accessibility: 'Screen Reader',
      status: capabilities.hasScreenReader ? '✓ Detected' : '○ None',
      recommendation: capabilities.hasScreenReader ? 'Screen reader optimizations enabled' : 'Visual interface optimized'
    });
    
    accessibilityTable.addRow({
      accessibility: 'Reduced Motion',
      status: capabilities.reducedMotionPreferred ? '✓ Preferred' : '○ Normal',
      recommendation: capabilities.reducedMotionPreferred ? 'Animations disabled for accessibility' : 'Animations available'
    });
    
    console.log(accessibilityTable.render());
  }
  
  /**
   * Display adaptive configuration
   */
  private static displayAdaptiveConfig(config: any): void {
    console.log(chalk.yellow.bold('\n⚙️ Adaptive Configuration\n'));
    
    const configTable = new Table([
      { header: 'Setting', key: 'setting', width: 25 },
      { header: 'Value', key: 'value', width: 20 },
      { header: 'Reason', key: 'reason', width: 55 }
    ]);
    
    configTable.addRow({
      setting: 'Colors',
      value: config.useColors ? '✓ Enabled' : '✗ Disabled',
      reason: config.useColors ? 'Terminal supports colors' : 'No color support or disabled by user'
    });
    
    configTable.addRow({
      setting: 'Unicode',
      value: config.useUnicode ? '✓ Enabled' : '✗ Disabled',
      reason: config.useUnicode ? 'Terminal supports Unicode' : 'Limited to ASCII characters'
    });
    
    configTable.addRow({
      setting: 'Animations',
      value: config.useAnimations ? `✓ ${config.animationSpeed}ms` : '✗ Disabled',
      reason: config.useAnimations ? 'Terminal supports animations' : 'Disabled for performance or accessibility'
    });
    
    configTable.addRow({
      setting: 'Compact Mode',
      value: config.compactMode ? '✓ Enabled' : '○ Normal',
      reason: config.compactMode ? 'Small terminal or user preference' : 'Sufficient space for full layout'
    });
    
    configTable.addRow({
      setting: 'Max Width',
      value: `${config.maxWidth} chars`,
      reason: `Optimized for ${config.columns}x${config.rows} terminal`
    });
    
    configTable.addRow({
      setting: 'Fallback Mode',
      value: config.fallbackMode ? '⚠ Active' : '✓ Normal',
      reason: config.fallbackMode ? 'Limited terminal capabilities detected' : 'Full feature set available'
    });
    
    console.log(configTable.render());
  }
  
  /**
   * Test adaptive features
   */
  private static async testAdaptiveFeatures(): Promise<void> {
    console.log(chalk.yellow.bold('\n🧪 Testing Adaptive Features\n'));
    
    // Test adaptive symbols
    console.log('Testing adaptive symbols:');
    const symbols = await terminalAdapter.getSymbols();
    console.log(`  Success: ${symbols.success}`);
    console.log(`  Error: ${symbols.error}`);
    console.log(`  Warning: ${symbols.warning}`);
    console.log(`  Info: ${symbols.info}`);
    console.log(`  Loading: ${symbols.loading}`);
    console.log();
    
    // Test adaptive colors
    console.log('Testing adaptive colors:');
    const successText = await terminalAdapter.formatText('Success message', 'success');
    const errorText = await terminalAdapter.formatText('Error message', 'error');
    const warningText = await terminalAdapter.formatText('Warning message', 'warning');
    const infoText = await terminalAdapter.formatText('Info message', 'info');
    
    console.log(`  ${successText}`);
    console.log(`  ${errorText}`);
    console.log(`  ${warningText}`);
    console.log(`  ${infoText}`);
    console.log();
    
    // Test feature support
    console.log('Feature support:');
    const features = ['colors', 'unicode', 'animations', 'hyperlinks', 'mouse'] as const;
    
    for (const feature of features) {
      const supported = await terminalAdapter.isFeatureSupported(feature);
      console.log(`  ${feature}: ${supported ? '✓ Supported' : '✗ Not supported'}`);
    }
    console.log();
    
    // Test progress indicator
    console.log('Testing adaptive progress indicator:');
    const progress = await terminalAdapter.createProgressIndicator(100, 'Testing progress');
    
    // Simulate progress
    for (let i = 0; i <= 100; i += 20) {
      progress.update(i, `Step ${i / 20 + 1}`);
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    progress.complete('Progress test completed');
    console.log();
  }
  
  /**
   * Get color support text representation
   */
  private static getColorSupportText(level: ColorSupport): string {
    switch (level) {
      case ColorSupport.NONE: return '✗ None';
      case ColorSupport.BASIC: return '○ Basic (16)';
      case ColorSupport.EXTENDED: return '◐ Extended (256)';
      case ColorSupport.TRUECOLOR: return '✓ True Color (16M)';
      default: return '? Unknown';
    }
  }
  
  /**
   * Get color support description
   */
  private static getColorDescription(level: ColorSupport): string {
    switch (level) {
      case ColorSupport.NONE: return 'No color support';
      case ColorSupport.BASIC: return '16 basic colors';
      case ColorSupport.EXTENDED: return '256 colors';
      case ColorSupport.TRUECOLOR: return '16 million colors (RGB)';
      default: return 'Unknown color support';
    }
  }
  
  /**
   * Show terminal environment variables
   */
  public static showEnvironmentInfo(): void {
    console.log(chalk.cyan.bold('\n🌍 Terminal Environment Variables\n'));
    
    const envVars = [
      'TERM', 'TERM_PROGRAM', 'TERM_PROGRAM_VERSION', 'COLORTERM',
      'FORCE_COLOR', 'NO_COLOR', 'CI', 'GITHUB_ACTIONS',
      'SSH_CLIENT', 'SSH_TTY', 'WSL_DISTRO_NAME', 'WSLENV',
      'DISPLAY', 'WAYLAND_DISPLAY', 'XDG_SESSION_TYPE',
      'LANG', 'LC_ALL', 'LC_CTYPE'
    ];
    
    const envTable = new Table([
      { header: 'Variable', key: 'variable', width: 25 },
      { header: 'Value', key: 'value', width: 55 }
    ]);
    
    envVars.forEach(varName => {
      const value = process.env[varName];
      envTable.addRow({
        variable: varName,
        value: value || '(not set)'
      });
    });
    
    console.log(envTable.render());
  }
}

// Export test runner
export async function runTerminalCapabilityTests(): Promise<void> {
  await TerminalCapabilitiesTest.runTests();
}

export function showTerminalEnvironment(): void {
  TerminalCapabilitiesTest.showEnvironmentInfo();
}