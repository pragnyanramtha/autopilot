// Simple test for DirectPromptingEngine
import { DirectPromptingEngine } from './src/ai/DirectPromptingEngine.js';

async function testDirectPrompting() {
  try {
    console.log('Testing DirectPromptingEngine...');
    
    // Check if we can create an instance
    const engine = new DirectPromptingEngine();
    console.log('✓ DirectPromptingEngine instance created');
    
    // Test initialization
    await engine.initialize();
    console.log('✓ Engine initialized successfully');
    
    console.log('✓ All tests passed!');
    
  } catch (error) {
    console.error('✗ Test failed:', error.message);
    process.exit(1);
  }
}

testDirectPrompting();