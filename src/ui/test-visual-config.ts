#!/usr/bin/env node

/**
 * Simple test script to verify visual configuration system
 */

import { visualPreferences, PreferencesConfig } from './preferences/index.js';
import { terminalCapabilities, terminalAdapter } from './terminal/index.js';
import { StatusIndicator } from './components/StatusIndicator.js';

async function testVisualConfiguration() {
  console.log('🧪 Testing Visual Configuration System\n');
  
  try {
    // Test 1: Visual Preferences
    console.log('1. Testing Visual Preferences...');
    const prefs = visualPreferences.getPreferences();
    console.log(`   Current theme: ${prefs.theme}`);
    console.log(`   Animations: ${prefs.animations ? 'enabled' : 'disabled'}`);
    console.log(`   Compact mode: ${prefs.compactMode ? 'enabled' : 'disabled'}`);
    StatusIndicator.success('Visual preferences loaded successfully');
    
    // Test 2: Terminal Capabilities
    console.log('\n2. Testing Terminal Capabilities...');
    const capabilities = await terminalCapabilities.detect();
    console.log(`   Terminal: ${capabilities.name}`);
    console.log(`   Color support: ${capabilities.colorSupport}`);
    console.log(`   Unicode support: ${capabilities.supportsUnicode}`);
    StatusIndicator.success('Terminal capabilities detected successfully');
    
    // Test 3: Adaptive Configuration
    console.log('\n3. Testing Adaptive Configuration...');
    await terminalAdapter.initialize();
    const config = await terminalAdapter.getConfig();
    console.log(`   Use colors: ${config.useColors}`);
    console.log(`   Use animations: ${config.useAnimations}`);
    console.log(`   Max width: ${config.maxWidth}`);
    StatusIndicator.success('Adaptive configuration initialized successfully');
    
    // Test 4: Feature Support
    console.log('\n4. Testing Feature Support...');
    const colorSupport = await terminalAdapter.isFeatureSupported('colors');
    const unicodeSupport = await terminalAdapter.isFeatureSupported('unicode');
    const animationSupport = await terminalAdapter.isFeatureSupported('animations');
    
    console.log(`   Colors: ${colorSupport ? 'supported' : 'not supported'}`);
    console.log(`   Unicode: ${unicodeSupport ? 'supported' : 'not supported'}`);
    console.log(`   Animations: ${animationSupport ? 'supported' : 'not supported'}`);
    StatusIndicator.success('Feature support detection working');
    
    // Test 5: Adaptive Text Formatting
    console.log('\n5. Testing Adaptive Text Formatting...');
    const successText = await terminalAdapter.formatText('Success message', 'success');
    const errorText = await terminalAdapter.formatText('Error message', 'error');
    const warningText = await terminalAdapter.formatText('Warning message', 'warning');
    
    console.log(`   ${successText}`);
    console.log(`   ${errorText}`);
    console.log(`   ${warningText}`);
    StatusIndicator.success('Adaptive text formatting working');
    
    console.log('\n✅ All visual configuration tests passed!');
    
  } catch (error) {
    StatusIndicator.error(`Test failed: ${error instanceof Error ? error.message : error}`);
    process.exit(1);
  }
}

// Run tests if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  testVisualConfiguration();
}

export { testVisualConfiguration };