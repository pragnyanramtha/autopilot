// UI Components exports
export { Banner } from './Banner.js';
export { StatusIndicator } from './StatusIndicator.js';
export { Spinner, ProgressBar } from './ProgressBar.js';
export { Table, formatters } from './Table.js';
export { default as TableExamples } from './TableExamples.js';
export { Prompt, input, confirm, select, checkbox, password } from './Prompt.js';
export type { PromptOptions, ChoiceOption, MultiChoiceOptions, ConfirmOptions } from './Prompt.js';
export { StepProgress, createLinearProgress, createDependentProgress, runStepsWithProgress } from './StepProgress.js';
export type { Step, StepStatus, StepProgressOptions } from './StepProgress.js';
export { examples, runExample, runAllExamples } from './InteractiveExamples.js';

// Optimized Components exports
export { OptimizedBanner } from './OptimizedBanner.js';
export type { OptimizedBannerOptions } from './OptimizedBanner.js';
export { 
  OptimizedProgressBar, 
  OptimizedSpinner, 
  OptimizedMultiStepProgress 
} from './OptimizedProgressBar.js';
export type { OptimizedProgressOptions } from './OptimizedProgressBar.js';
export { OptimizedStatusIndicator, OptimizedStatusType } from './OptimizedStatusIndicator.js';
export type { OptimizedStatusOptions } from './OptimizedStatusIndicator.js';
export { OptimizedTable } from './OptimizedTable.js';
export type { 
  OptimizedTableColumn, 
  OptimizedTableRow, 
  OptimizedTableOptions, 
  OptimizedTableStyle 
} from './OptimizedTable.js';

// Re-export utilities for convenience
export { colors } from '../utils/Colors.js';
export { symbols } from '../utils/Symbols.js';
export { Layout } from '../utils/Layout.js';

// Performance utilities
export {
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
} from '../utils/Performance.js';

// Re-export preferences for convenience
export {
  visualPreferences,
  getVisualPreferences,
  updateVisualPreferences,
  shouldShowAnimations,
  shouldShowIcons,
  shouldUseColors,
  PreferencesConfig
} from '../preferences/index.js';

// Re-export terminal capabilities for convenience
export {
  terminalCapabilities,
  terminalAdapter,
  detectTerminalCapabilities,
  getAdaptiveConfig,
  isFeatureSupported,
  ColorSupport
} from '../terminal/index.js';