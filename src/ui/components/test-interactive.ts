#!/usr/bin/env node

/**
 * Simple test script for interactive components
 * Run with: npx tsx src/ui/components/test-interactive.ts
 */

import { input, confirm, select, checkbox } from './Prompt.js';
import { createLinearProgress } from './StepProgress.js';

async function testPrompts() {
  console.log('🧪 Testing Interactive Components\n');

  try {
    // Test basic input
    const name = await input('What is your name?', { required: true });
    console.log(`Hello, ${name}!\n`);

    // Test confirmation
    const proceed = await confirm('Continue with more tests?', true);
    if (!proceed) {
      console.log('Tests cancelled.');
      return;
    }

    // Test selection
    const color = await select('Choose your favorite color:', [
      { name: 'Red', value: 'red', description: 'The color of passion' },
      { name: 'Blue', value: 'blue', description: 'The color of the sky' },
      { name: 'Green', value: 'green', description: 'The color of nature' }
    ]);
    console.log(`You chose: ${color}\n`);

    // Test checkbox
    const features = await checkbox('Select features you like:', [
      { name: 'Colors', value: 'colors', description: 'Colorful output' },
      { name: 'Animations', value: 'animations', description: 'Smooth animations' },
      { name: 'Icons', value: 'icons', description: 'Unicode symbols' }
    ]);
    console.log(`Selected features: ${features.join(', ')}\n`);

    console.log('✅ All prompt tests completed successfully!');

  } catch (error) {
    console.error('❌ Test failed:', error);
  }
}

async function testStepProgress() {
  console.log('\n🧪 Testing Step Progress\n');

  const stepProgress = createLinearProgress([
    'Initialize',
    'Process data',
    'Generate output',
    'Complete'
  ], {
    showEstimatedTime: true,
    showProgress: true
  });

  stepProgress.start();

  for (let i = 1; i <= 4; i++) {
    const stepId = `step-${i}`;
    stepProgress.startStep(stepId);
    
    // Simulate work with progress updates
    for (let progress = 0; progress <= 100; progress += 25) {
      stepProgress.updateStepProgress(stepId, progress, `Working... ${progress}%`);
      await new Promise(resolve => setTimeout(resolve, 200));
    }
    
    stepProgress.completeStep(stepId);
  }

  stepProgress.complete();
  console.log('✅ Step progress test completed successfully!');
}

async function main() {
  await testPrompts();
  await testStepProgress();
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}