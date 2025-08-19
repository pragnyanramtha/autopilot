/**
 * Terminal Capabilities and Adaptation Module
 * 
 * This module provides comprehensive terminal capability detection and adaptive
 * configuration for optimal display across different terminal environments.
 */

// Core capability detection
export {
  TerminalCapabilities,
  TerminalCapabilityDetector,
  ColorSupport,
  terminalCapabilities,
  detectTerminalCapabilities,
  getTerminalCapabilities,
  getResponsiveLayout,
  getFallbackConfig
} from './TerminalCapabilities.js';

// Adaptive terminal interface
export {
  AdaptiveConfig,
  TerminalAdapter,
  terminalAdapter,
  getAdaptiveConfig,
  isFeatureSupported,
  formatAdaptiveText
} from './TerminalAdapter.js';