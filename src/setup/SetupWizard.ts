import * as fs from 'fs';
import * as path from 'path';
import chalk from 'chalk';
import { PackageManagerService } from '../terminal/PackageManager.js';
import { SystemDetection } from '../terminal/SystemDetection.js';
import { GeminiService } from '../ai/GeminiService.js';
import { StatusIndicator, StatusType } from '../ui/components/StatusIndicator.js';
import { ProgressBar, MultiStepProgress } from '../ui/components/ProgressBar.js';
import { Banner } from '../ui/components/Banner.js';
import { colors } from '../ui/utils/Colors.js';
import { Layout } from '../ui/utils/Layout.js';

export class SetupWizard {
  private packageManager: PackageManagerService;
  private systemDetection: SystemDetection;

  constructor() {
    this.packageManager = new PackageManagerService();
    this.systemDetection = new SystemDetection();
  }

  async run(): Promise<void> {
    // Display banner
    Banner.display({ showVersion: true, showTagline: true });
    
    StatusIndicator.info('Starting Kira setup wizard...');
    console.log('This wizard will help you configure Kira for optimal performance.\n');

    const steps = [
      'System Detection',
      'System Requirements Check', 
      'Package Manager Detection',
      'AI Configuration Check',
      'Environment Setup',
      'Final Configuration'
    ];

    const progress = new MultiStepProgress(steps);

    try {
      // Step 1: System Detection
      progress.nextStep('Running comprehensive system detection...');
      await this.runSystemDetection();
      progress.completeStep();

      // Step 2: Check system requirements
      progress.nextStep('Checking system requirements...');
      await this.checkSystemRequirements();
      progress.completeStep();

      // Step 3: Check package managers
      progress.nextStep('Analyzing package managers...');
      await this.checkPackageManagers();
      progress.completeStep();

      // Step 4: Check AI configuration
      progress.nextStep('Verifying AI configuration...');
      await this.checkAIConfiguration();
      progress.completeStep();

      // Step 5: Create .env file if it doesn't exist
      progress.nextStep('Setting up environment configuration...');
      await this.createEnvFile();
      progress.completeStep();

      // Step 6: Final recommendations
      progress.nextStep('Generating recommendations...');
      this.showFinalRecommendations();
      progress.complete('Setup wizard completed successfully!');

    } catch (error: any) {
      StatusIndicator.error('Setup wizard failed', {
        details: error.message
      });
      throw error;
    }
  }

  private async runSystemDetection(): Promise<void> {
    try {
      await this.systemDetection.detectWithScript({ verbose: false, showProgress: true });
      StatusIndicator.success('System detection completed');
      
      // Display summary
      this.systemDetection.displaySummary();
      
    } catch (error: any) {
      StatusIndicator.warning('System detection failed, using fallback method');
      await this.systemDetection.detect({ verbose: false, showProgress: true });
    }
  }

  private async checkSystemRequirements(): Promise<void> {
    StatusIndicator.info('Checking system requirements...');

    const requirements = [
      { name: 'Node.js', command: 'node --version', required: true },
      { name: 'npm', command: 'npm --version', required: true },
      { name: 'bash', command: 'bash --version', required: true },
      { name: 'curl', command: 'curl --version', required: false },
      { name: 'wget', command: 'wget --version', required: false },
      { name: 'git', command: 'git --version', required: false },
      { name: 'docker', command: 'docker --version', required: false }
    ];

    const results: Array<{ name: string; status: StatusType; version?: string; required: boolean }> = [];

    for (const req of requirements) {
      try {
        const { exec } = await import('child_process');
        const { promisify } = await import('util');
        const execAsync = promisify(exec);
        
        const { stdout } = await execAsync(req.command, { timeout: 5000 });
        const version = stdout.split('\n')[0];
        
        results.push({
          name: req.name,
          status: StatusType.SUCCESS,
          version,
          required: req.required
        });
        
      } catch (error) {
        results.push({
          name: req.name,
          status: req.required ? StatusType.ERROR : StatusType.WARNING,
          required: req.required
        });
      }
    }

    // Display results
    const requiredMissing = results.filter(r => r.required && r.status === StatusType.ERROR);
    const optionalMissing = results.filter(r => !r.required && r.status === StatusType.WARNING);
    const available = results.filter(r => r.status === StatusType.SUCCESS);

    StatusIndicator.summary('System Requirements', 
      results.map(r => ({
        label: `${r.name}${r.required ? ' (required)' : ''}`,
        status: r.status,
        value: r.version ? r.version.substring(0, 20) : undefined
      }))
    );

    if (requiredMissing.length > 0) {
      StatusIndicator.error(`Missing required dependencies: ${requiredMissing.map(r => r.name).join(', ')}`);
    } else {
      StatusIndicator.success('All required dependencies are available');
    }

    if (optionalMissing.length > 0) {
      StatusIndicator.info(`Optional tools not found: ${optionalMissing.map(r => r.name).join(', ')}`);
    }
  }

  private async checkPackageManagers(): Promise<void> {
    StatusIndicator.info('Analyzing package managers...');

    await this.packageManager.displayStatus();
    
    const available = this.packageManager.getAvailableManagers();

    if (available.length === 0) {
      StatusIndicator.error('No package managers found!', {
        details: 'Please install at least one: apt, snap, flatpak, npm, pip, or cargo'
      });
    } else {
      StatusIndicator.success(`Found ${available.length} package manager(s)`, {
        details: available.join(', ')
      });
    }
  }

  private async checkAIConfiguration(): Promise<void> {
    StatusIndicator.info('Checking AI configuration...');

    const geminiService = new GeminiService();
    
    if (geminiService.isAIEnabled()) {
      StatusIndicator.success('Gemini AI: Configured and ready', {
        details: 'Enhanced natural language processing enabled'
      });
    } else {
      StatusIndicator.warning('Gemini AI: Not configured', {
        details: 'Add your GEMINI_API_KEY to .env for enhanced AI features\nGet your API key from: https://makersuite.google.com/app/apikey'
      });
    }
  }

  private async createEnvFile(): Promise<void> {
    const envPath = '.env';
    const envExamplePath = '.env.example';

    StatusIndicator.info('Setting up environment configuration...');

    if (fs.existsSync(envPath)) {
      StatusIndicator.success('.env file already exists', {
        details: 'Edit .env to customize your configuration'
      });
      return;
    }

    if (fs.existsSync(envExamplePath)) {
      try {
        const exampleContent = fs.readFileSync(envExamplePath, 'utf8');
        fs.writeFileSync(envPath, exampleContent);
        StatusIndicator.success('Created .env file from .env.example', {
          details: 'Please edit .env and add your API keys'
        });
      } catch (error: any) {
        StatusIndicator.error('Failed to create .env file', {
          details: 'Please manually copy .env.example to .env'
        });
      }
    } else {
      StatusIndicator.warning('.env.example not found', {
        details: 'Please create a .env file with your configuration'
      });
    }
  }

  private showFinalRecommendations(): void {
    StatusIndicator.success('Setup Complete!');
    
    console.log('\n' + Layout.box(
      colors.bold('🎉 Kira Setup Complete!\n\n') +
      colors.primary('📝 Next Steps:\n') +
      '1. Edit .env file and add your Gemini API key for enhanced AI features\n' +
      '2. Test the installation: kira check disk space\n' +
      '3. Try some examples:\n' +
      '   • kira install and open firefox\n' +
      '   • kira list files\n' +
      '   • kira create directory named test-folder\n' +
      '   • kira demo (to see error handling)\n\n' +
      colors.primary('🔧 Configuration:\n') +
      '• Configuration file: .env\n' +
      '• Logs: Check terminal output\n' +
      '• Package managers: Automatically detected\n' +
      '• Browser: Uses system default browser\n\n' +
      colors.primary('📚 Documentation:\n') +
      '• GitHub: https://github.com/pragnyanramtha/autopilot\n' +
      '• Issues: https://github.com/pragnyanramtha/autopilot/issues\n' +
      '• API Keys: https://makersuite.google.com/app/apikey\n\n' +
      colors.success('✨ Kira is ready to automate your workflows!')
    ));
  }
}