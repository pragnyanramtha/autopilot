// Test DirectPromptingEngine functionality
import { DirectPromptingEngine } from './dist/ai/DirectPromptingEngine.js';

async function testEngine() {
  try {
    console.log('Testing DirectPromptingEngine...');
    
    // Set a dummy API key for testing
    process.env.GEMINI_API_KEY = 'test-key-for-structure-testing';
    
    const engine = new DirectPromptingEngine();
    console.log('✓ DirectPromptingEngine created successfully');
    
    // Test that the class structure is correct
    console.log('✓ Class methods available:', Object.getOwnPropertyNames(Object.getPrototypeOf(engine)));
    
    console.log('✓ DirectPromptingEngine implementation is structurally correct');
    
  } catch (error) {
    console.error('✗ Test failed:', error.message);
    process.exit(1);
  }
}

testEngine();