import { TerminalEngine } from './TerminalEngine';

export class ErrorHandlingDemo {
  private terminalEngine: TerminalEngine;

  constructor() {
    this.terminalEngine = new TerminalEngine();
  }

  async demonstrateErrorHandling(): Promise<void> {
    console.log('🧪 Error Handling Demonstration\n');

    const testCases = [
      {
        name: 'Command Not Found Error',
        command: 'thisisnotarealcommand123456789',
        description: 'Tests handling of missing commands'
      },
      {
        name: 'Permission Denied Error',
        command: 'cat /etc/shadow',
        description: 'Tests permission error handling'
      },
      {
        name: 'Invalid Directory Access',
        command: 'ls /root/nonexistent',
        description: 'Tests directory access error handling'
      },
      {
        name: 'Network Error Simulation',
        command: 'curl --connect-timeout 1 http://192.0.2.1/nonexistent',
        description: 'Tests network timeout handling'
      }
    ];

    for (const testCase of testCases) {
      console.log(`\n📋 Test Case: ${testCase.name}`);
      console.log(`   Description: ${testCase.description}`);
      console.log(`   Command: ${testCase.command}`);
      console.log('   ' + '─'.repeat(50));

      try {
        const result = await this.terminalEngine.executeCommand(testCase.command);
        console.log(`✅ Unexpected success: ${result.stdout.substring(0, 100)}`);
      } catch (error: any) {
        console.log(`❌ Final failure (as expected):`);
        console.log(`   Error: ${error.stderr || error.message || String(error)}`);
        console.log(`   Exit code: ${error.exitCode || 'unknown'}`);
      }

      console.log('   ' + '─'.repeat(50));
      await this.delay(2000); // Pause between tests
    }

    console.log('\n🎯 Error handling demonstration completed!');
  }

  private async delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}