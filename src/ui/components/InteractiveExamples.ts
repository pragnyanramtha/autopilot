import { Prompt, input, confirm, select, checkbox, password } from './Prompt.js';
import { StepProgress, createLinearProgress, createDependentProgress, runStepsWithProgress } from './StepProgress.js';
import { colors } from '../utils/Colors.js';
import { symbols } from '../utils/Symbols.js';
import { Layout } from '../utils/Layout.js';

/**
 * Example: Basic input prompts with validation
 */
export async function basicInputExample(): Promise<void> {
  console.log(colors.primary('=== Basic Input Examples ===\n'));

  // Simple text input
  const name = await input('What is your name?', {
    required: true,
    validate: (input) => input.length >= 2 || 'Name must be at least 2 characters'
  });

  // Email input with validation
  const email = await input('Enter your email address:', {
    required: true,
    validate: (input) => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(input) || 'Please enter a valid email address';
    }
  });

  // Number input with range validation
  const prompt = new Prompt();
  const age = await prompt.number({
    message: 'Enter your age:',
    min: 13,
    max: 120,
    integer: true,
    required: true
  });

  // Password input
  const userPassword = await password('Create a password:', {
    required: true,
    validate: (input) => input.length >= 8 || 'Password must be at least 8 characters'
  });

  prompt.close();

  console.log(colors.success('\n✓ Input collection completed!'));
  console.log(colors.muted(`Name: ${name}`));
  console.log(colors.muted(`Email: ${email}`));
  console.log(colors.muted(`Age: ${age}`));
  console.log(colors.muted('Password: [hidden]'));
}

/**
 * Example: Selection prompts
 */
export async function selectionExample(): Promise<void> {
  console.log(colors.primary('\n=== Selection Examples ===\n'));

  // Single selection
  const framework = await select('Choose your preferred framework:', [
    { name: 'React', value: 'react', description: 'A JavaScript library for building user interfaces' },
    { name: 'Vue.js', value: 'vue', description: 'The Progressive JavaScript Framework' },
    { name: 'Angular', value: 'angular', description: 'Platform for building mobile and desktop web applications' },
    { name: 'Svelte', value: 'svelte', description: 'Cybernetically enhanced web apps' },
    { name: 'Other', value: 'other', description: 'Something else entirely' }
  ]);

  // Multi-selection with checkboxes
  const features = await checkbox('Select desired features:', [
    { name: 'TypeScript Support', value: 'typescript', description: 'Add TypeScript configuration' },
    { name: 'Testing Setup', value: 'testing', description: 'Include Jest and testing utilities' },
    { name: 'Linting', value: 'linting', description: 'ESLint and Prettier configuration' },
    { name: 'CI/CD', value: 'cicd', description: 'GitHub Actions workflow' },
    { name: 'Docker', value: 'docker', description: 'Dockerfile and docker-compose' },
    { name: 'Documentation', value: 'docs', description: 'Auto-generated documentation setup' }
  ]);

  // Confirmation
  const proceed = await confirm('Proceed with the selected configuration?', true);

  console.log(colors.success('\n✓ Selection completed!'));
  console.log(colors.muted(`Framework: ${framework}`));
  console.log(colors.muted(`Features: ${features.join(', ')}`));
  console.log(colors.muted(`Proceed: ${proceed ? 'Yes' : 'No'}`));
}

/**
 * Example: Step-by-step progress with linear steps
 */
export async function linearProgressExample(): Promise<void> {
  console.log(colors.primary('\n=== Linear Progress Example ===\n'));

  const stepProgress = createLinearProgress([
    'Initialize project structure',
    'Install dependencies',
    'Configure build tools',
    'Set up development environment',
    'Generate initial files'
  ], {
    showEstimatedTime: true,
    showProgress: true,
    compact: false
  });

  const stepFunctions = [
    async () => {
      // Simulate project initialization
      for (let i = 0; i <= 100; i += 20) {
        stepProgress.updateStepProgress('step-1', i, `Creating directories... ${i}%`);
        await sleep(200);
      }
      return 'Project structure created';
    },
    async () => {
      // Simulate dependency installation
      for (let i = 0; i <= 100; i += 10) {
        stepProgress.updateStepProgress('step-2', i, `Installing packages... ${i}%`);
        await sleep(150);
      }
      return 'Dependencies installed';
    },
    async () => {
      // Simulate build configuration
      for (let i = 0; i <= 100; i += 25) {
        stepProgress.updateStepProgress('step-3', i, `Configuring webpack... ${i}%`);
        await sleep(300);
      }
      return 'Build tools configured';
    },
    async () => {
      // Simulate environment setup
      for (let i = 0; i <= 100; i += 33) {
        stepProgress.updateStepProgress('step-4', i, `Setting up dev server... ${i}%`);
        await sleep(250);
      }
      return 'Development environment ready';
    },
    async () => {
      // Simulate file generation
      for (let i = 0; i <= 100; i += 50) {
        stepProgress.updateStepProgress('step-5', i, `Generating boilerplate... ${i}%`);
        await sleep(200);
      }
      return 'Initial files generated';
    }
  ];

  try {
    const results = await runStepsWithProgress(stepProgress, stepFunctions);
    console.log(colors.success('\n🎉 Project setup completed successfully!'));
  } catch (error) {
    console.log(colors.error('\n❌ Project setup failed'));
  }
}

/**
 * Example: Complex workflow with dependencies and optional steps
 */
export async function complexWorkflowExample(): Promise<void> {
  console.log(colors.primary('\n=== Complex Workflow Example ===\n'));

  const stepProgress = createDependentProgress([
    {
      title: 'System Requirements Check',
      estimatedTime: 10
    },
    {
      title: 'Download Required Files',
      dependencies: ['step-1'],
      estimatedTime: 30
    },
    {
      title: 'Install Core Components',
      dependencies: ['step-2'],
      estimatedTime: 45
    },
    {
      title: 'Configure Database',
      dependencies: ['step-3'],
      estimatedTime: 20,
      optional: true
    },
    {
      title: 'Set up Authentication',
      dependencies: ['step-3'],
      estimatedTime: 25,
      optional: true
    },
    {
      title: 'Run Initial Tests',
      dependencies: ['step-3'],
      estimatedTime: 15
    },
    {
      title: 'Generate Documentation',
      dependencies: ['step-6'],
      estimatedTime: 10,
      optional: true
    }
  ], {
    showEstimatedTime: true,
    showProgress: true,
    showBreadcrumbs: true,
    compact: false
  });

  stepProgress.start();

  try {
    // Step 1: System check
    stepProgress.startStep('step-1');
    await sleep(1000);
    stepProgress.updateStepProgress('step-1', 50, 'Checking Node.js version...');
    await sleep(500);
    stepProgress.updateStepProgress('step-1', 100, 'System requirements verified');
    stepProgress.completeStep('step-1');

    // Step 2: Download files
    stepProgress.startStep('step-2');
    for (let i = 0; i <= 100; i += 10) {
      stepProgress.updateStepProgress('step-2', i, `Downloading... ${i}%`);
      await sleep(200);
    }
    stepProgress.completeStep('step-2');

    // Step 3: Install components
    stepProgress.startStep('step-3');
    for (let i = 0; i <= 100; i += 20) {
      stepProgress.updateStepProgress('step-3', i, `Installing components... ${i}%`);
      await sleep(300);
    }
    stepProgress.completeStep('step-3');

    // Step 4: Database (optional - simulate skip)
    const setupDatabase = await confirm('Set up database configuration?', false);
    if (setupDatabase) {
      stepProgress.startStep('step-4');
      for (let i = 0; i <= 100; i += 25) {
        stepProgress.updateStepProgress('step-4', i, `Configuring database... ${i}%`);
        await sleep(200);
      }
      stepProgress.completeStep('step-4');
    } else {
      stepProgress.skipStep('step-4');
    }

    // Step 5: Authentication (optional)
    const setupAuth = await confirm('Set up authentication?', true);
    if (setupAuth) {
      stepProgress.startStep('step-5');
      for (let i = 0; i <= 100; i += 33) {
        stepProgress.updateStepProgress('step-5', i, `Setting up auth... ${i}%`);
        await sleep(250);
      }
      stepProgress.completeStep('step-5');
    } else {
      stepProgress.skipStep('step-5');
    }

    // Step 6: Tests
    stepProgress.startStep('step-6');
    for (let i = 0; i <= 100; i += 50) {
      stepProgress.updateStepProgress('step-6', i, `Running tests... ${i}%`);
      await sleep(300);
    }
    
    // Simulate occasional test failure
    if (Math.random() > 0.8) {
      stepProgress.failStep('step-6', 'Some tests failed - please check the logs');
      stepProgress.fail('Workflow stopped due to test failures');
      return;
    }
    
    stepProgress.completeStep('step-6');

    // Step 7: Documentation (optional)
    stepProgress.startStep('step-7');
    for (let i = 0; i <= 100; i += 100) {
      stepProgress.updateStepProgress('step-7', i, 'Generating docs...');
      await sleep(500);
    }
    stepProgress.completeStep('step-7');

    stepProgress.complete();
    
  } catch (error) {
    stepProgress.fail(error instanceof Error ? error.message : 'Unknown error occurred');
  }
}

/**
 * Example: Interactive setup wizard combining prompts and progress
 */
export async function setupWizardExample(): Promise<void> {
  console.log(colors.primary('\n=== Interactive Setup Wizard ===\n'));

  // Collect user preferences
  console.log(colors.info('📋 Project Configuration\n'));

  const projectName = await input('Project name:', {
    required: true,
    validate: (input) => /^[a-z0-9-]+$/.test(input) || 'Use lowercase letters, numbers, and hyphens only'
  });

  const projectType = await select('Project type:', [
    { name: 'Web Application', value: 'web', description: 'Frontend web application' },
    { name: 'API Server', value: 'api', description: 'Backend REST API' },
    { name: 'CLI Tool', value: 'cli', description: 'Command-line application' },
    { name: 'Library', value: 'lib', description: 'Reusable library package' }
  ]);

  const features = await checkbox('Select features to include:', [
    { name: 'TypeScript', value: 'typescript', description: 'Type-safe JavaScript' },
    { name: 'Testing', value: 'testing', description: 'Unit and integration tests' },
    { name: 'Linting', value: 'linting', description: 'Code quality tools' },
    { name: 'CI/CD', value: 'cicd', description: 'Automated workflows' }
  ]);

  const useGit = await confirm('Initialize Git repository?', true);

  // Show configuration summary
  console.log(colors.info('\n📋 Configuration Summary:'));
  console.log(colors.muted(`  Project: ${projectName}`));
  console.log(colors.muted(`  Type: ${projectType}`));
  console.log(colors.muted(`  Features: ${features.join(', ') || 'None'}`));
  console.log(colors.muted(`  Git: ${useGit ? 'Yes' : 'No'}`));

  const proceed = await confirm('\nProceed with project creation?', true);
  
  if (!proceed) {
    console.log(colors.warning('Setup cancelled by user'));
    return;
  }

  // Create setup steps based on configuration
  const steps = [
    'Create project directory',
    'Initialize package.json',
    ...(features.includes('typescript') ? ['Set up TypeScript'] : []),
    ...(features.includes('testing') ? ['Configure testing framework'] : []),
    ...(features.includes('linting') ? ['Set up linting tools'] : []),
    ...(useGit ? ['Initialize Git repository'] : []),
    ...(features.includes('cicd') ? ['Create CI/CD workflows'] : []),
    'Install dependencies',
    'Generate initial files'
  ];

  const stepProgress = createLinearProgress(steps, {
    showEstimatedTime: true,
    showProgress: true,
    showBreadcrumbs: true
  });

  // Execute setup steps
  const stepFunctions = steps.map((step, index) => async () => {
    const stepId = `step-${index + 1}`;
    
    // Simulate different step durations
    const duration = Math.random() * 2000 + 500; // 500-2500ms
    const steps = Math.floor(duration / 100);
    
    for (let i = 0; i <= steps; i++) {
      const progress = (i / steps) * 100;
      stepProgress.updateStepProgress(stepId, progress, `${step}... ${Math.round(progress)}%`);
      await sleep(100);
    }
    
    return `${step} completed`;
  });

  try {
    await runStepsWithProgress(stepProgress, stepFunctions);
    
    console.log(colors.success(`\n🎉 Project "${projectName}" created successfully!`));
    console.log(colors.muted('\nNext steps:'));
    console.log(colors.muted(`  cd ${projectName}`));
    console.log(colors.muted('  npm start'));
    
  } catch (error) {
    console.log(colors.error('\n❌ Project creation failed'));
    console.log(colors.error(error instanceof Error ? error.message : 'Unknown error'));
  }
}

/**
 * Example: Compact progress mode for quick operations
 */
export async function compactProgressExample(): Promise<void> {
  console.log(colors.primary('\n=== Compact Progress Example ===\n'));

  const stepProgress = createLinearProgress([
    'Validate input',
    'Process data',
    'Generate output',
    'Save results'
  ], {
    compact: true,
    showEstimatedTime: false,
    showBreadcrumbs: false
  });

  stepProgress.start();

  for (let i = 1; i <= 4; i++) {
    const stepId = `step-${i}`;
    stepProgress.startStep(stepId);
    
    // Quick simulation
    await sleep(800);
    
    stepProgress.completeStep(stepId);
  }

  stepProgress.complete();
}

// Utility function for simulating async operations
function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Export all examples for easy testing
export const examples = {
  basicInput: basicInputExample,
  selection: selectionExample,
  linearProgress: linearProgressExample,
  complexWorkflow: complexWorkflowExample,
  setupWizard: setupWizardExample,
  compactProgress: compactProgressExample
};

// CLI runner for testing examples
export async function runExample(exampleName: keyof typeof examples): Promise<void> {
  const example = examples[exampleName];
  if (!example) {
    console.log(colors.error(`Unknown example: ${exampleName}`));
    console.log(colors.info('Available examples:'));
    Object.keys(examples).forEach(name => {
      console.log(colors.muted(`  - ${name}`));
    });
    return;
  }

  try {
    await example();
  } catch (error) {
    console.log(colors.error('\nExample failed:'));
    console.log(colors.error(error instanceof Error ? error.message : 'Unknown error'));
  }
}

// Run all examples in sequence
export async function runAllExamples(): Promise<void> {
  console.log(colors.primary('🚀 Running all interactive examples...\n'));
  
  for (const [name, example] of Object.entries(examples)) {
    console.log(colors.accent(`\n--- ${name.toUpperCase()} ---`));
    try {
      await example();
      console.log(colors.success(`✓ ${name} completed`));
    } catch (error) {
      console.log(colors.error(`✗ ${name} failed: ${error}`));
    }
    
    // Pause between examples
    await sleep(1000);
  }
  
  console.log(colors.primary('\n🎉 All examples completed!'));
}