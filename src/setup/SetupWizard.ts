import * as fs from 'fs';
import * as path from 'path';
import chalk from 'chalk';
import { PackageManagerService } from '../terminal/PackageManager';
import { GeminiService } from '../ai/GeminiService';

export class SetupWizard {
  private packageManager: PackageManagerService;

  constructor() {
    this.packageManager = new PackageManagerService();
  }

  async run(): Promise<void> {
    console.log(chalk.cyan.bold('\n🚀 Alvioli Setup Wizard\n'));
    console.log('This wizard will help you configure Alvioli for optimal performance.\n');

    // Check system requirements
    await this.checkSystemRequirements();

    // Check package managers
    await this.checkPackageManagers();

    // Check AI configuration
    await this.checkAIConfiguration();

    // Create .env file if it doesn't exist
    await this.createEnvFile();

    // Final recommendations
    this.showFinalRecommendations();
  }

  private async checkSystemRequirements(): Promise<void> {
    console.log(chalk.yellow('📋 Checking System Requirements...\n'));

    const requirements = [
      { name: 'Node.js', command: 'node --version', required: true },
      { name: 'npm', command: 'npm --version', required: true },
      { name: 'bash', command: 'bash --version', required: true },
      { name: 'curl', command: 'curl --version', required: false },
      { name: 'wget', command: 'wget --version', required: false },
      { name: 'git', command: 'git --version', required: false },
      { name: 'docker', command: 'docker --version', required: false }
    ];

    for (const req of requirements) {
      try {
        const { exec } = await import('child_process');
        const { promisify } = await import('util');
        const execAsync = promisify(exec);
        
        const { stdout } = await execAsync(req.command, { timeout: 5000 });
        const version = stdout.split('\n')[0];
        
        console.log(`✅ ${req.name}: ${version}`);
      } catch (error) {
        if (req.required) {
          console.log(`❌ ${req.name}: Not found (REQUIRED)`);
        } else {
          console.log(`⚠️  ${req.name}: Not found (optional)`);
        }
      }
    }

    console.log('');
  }

  private async checkPackageManagers(): Promise<void> {
    console.log(chalk.yellow('📦 Checking Package Managers...\n'));

    await this.packageManager.initialize();
    const available = this.packageManager.getAvailableManagers();

    if (available.length === 0) {
      console.log('❌ No package managers found!');
      console.log('   Please install at least one: apt, snap, flatpak, npm, pip, or cargo\n');
    } else {
      console.log(`✅ Found ${available.length} package manager(s): ${available.join(', ')}\n`);
    }
  }

  private async checkAIConfiguration(): Promise<void> {
    console.log(chalk.yellow('🤖 Checking AI Configuration...\n'));

    const geminiService = new GeminiService();
    
    if (geminiService.isAIEnabled()) {
      console.log('✅ Gemini AI: Configured and ready');
      console.log('   Enhanced natural language processing enabled\n');
    } else {
      console.log('⚠️  Gemini AI: Not configured');
      console.log('   Add your GEMINI_API_KEY to .env for enhanced AI features');
      console.log('   Get your API key from: https://makersuite.google.com/app/apikey\n');
    }
  }

  private async createEnvFile(): Promise<void> {
    const envPath = '.env';
    const envExamplePath = '.env.example';

    if (fs.existsSync(envPath)) {
      console.log(chalk.yellow('📄 Configuration File...\n'));
      console.log('✅ .env file already exists');
      console.log('   Edit .env to customize your configuration\n');
      return;
    }

    if (fs.existsSync(envExamplePath)) {
      console.log(chalk.yellow('📄 Creating Configuration File...\n'));
      
      try {
        const exampleContent = fs.readFileSync(envExamplePath, 'utf8');
        fs.writeFileSync(envPath, exampleContent);
        console.log('✅ Created .env file from .env.example');
        console.log('   Please edit .env and add your API keys\n');
      } catch (error) {
        console.log('❌ Failed to create .env file');
        console.log('   Please manually copy .env.example to .env\n');
      }
    } else {
      console.log('⚠️  .env.example not found');
      console.log('   Please create a .env file with your configuration\n');
    }
  }

  private showFinalRecommendations(): void {
    console.log(chalk.green.bold('🎉 Setup Complete!\n'));
    
    console.log(chalk.cyan('📝 Next Steps:\n'));
    console.log('1. Edit .env file and add your Gemini API key for enhanced AI features');
    console.log('2. Test the installation: alido check disk space');
    console.log('3. Try some examples:');
    console.log('   • alido install and open upscayl');
    console.log('   • alido list files');
    console.log('   • alido create directory named test-folder');
    console.log('   • ali demo-errors (to see error handling)');
    
    console.log(chalk.cyan('\n🔧 Configuration:\n'));
    console.log('• Configuration file: .env');
    console.log('• Logs: Check terminal output');
    console.log('• Package managers: Automatically detected');
    console.log('• Browser: Uses system default browser');
    
    console.log(chalk.cyan('\n📚 Documentation:\n'));
    console.log('• GitHub: [Repository URL]');
    console.log('• Issues: [Issues URL]');
    console.log('• API Keys: https://makersuite.google.com/app/apikey');
    
    console.log(chalk.green('\n✨ Alvioli is ready to automate your Linux workflows!\n'));
  }
}