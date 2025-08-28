import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { createInterface } from 'readline';
import chalk from 'chalk';
import { Banner } from '../ui/components/Banner.js';
import { StatusIndicator } from '../ui/components/StatusIndicator.js';
import { SystemDetection } from '../terminal/SystemDetection.js';
import { PackageManagerService } from '../terminal/PackageManager.js';

export interface FirstTimeConfig {
  isFirstTime: boolean;
  apiKeyConfigured: boolean;
  systemDetected: boolean;
  preferencesSet: boolean;
  configPath: string;
}

export interface UserConfig {
  geminiApiKey: string;
  preferredPackageManager: string;
  preferredShell: string;
  systemInfo: any;
  userPreferences: {
    name: string;
    workingDirectory: string;
    autoUpdate: boolean;
    verboseOutput: boolean;
  };
  createdAt: string;
  updatedAt: string;
}

export class FirstTimeSetup {
  private configDir: string;
  private configPath: string;
  private envPath: string;

  constructor() {
    this.configDir = path.join(os.homedir(), '.ap');
    this.configPath = path.join(this.configDir, 'config.json');
    this.envPath = path.join(process.cwd(), '.env');
  }

  /**
   * Check if this is the first time running AP
   */
  public isFirstTime(): boolean {
    return !fs.existsSync(this.configPath);
  }

  /**
   * Check if API key is configured
   */
  public isApiKeyConfigured(): boolean {
    // Check both .env file and environment variable
    const envApiKey = process.env.GEMINI_API_KEY;
    if (envApiKey && envApiKey !== 'your_gemini_api_key_here' && envApiKey.trim() !== '') {
      return true;
    }

    // Check .env file
    if (fs.existsSync(this.envPath)) {
      const envContent = fs.readFileSync(this.envPath, 'utf8');
      const apiKeyMatch = envContent.match(/GEMINI_API_KEY=(.+)/);
      if (apiKeyMatch && apiKeyMatch[1] && apiKeyMatch[1] !== 'your_gemini_api_key_here') {
        return true;
      }
    }

    return false;
  }

  /**
   * Run the complete first-time setup flow
   */
  public async runFirstTimeSetup(): Promise<void> {
    Banner.display({ showVersion: true, showTagline: true });
    
    console.log(chalk.cyan.bold('\n🚀 Welcome to AP - AI-Powered Automation!\n'));
    console.log('This is your first time running AP. Let\'s get you set up!\n');

    try {
      // Step 1: API Key Setup
      await this.setupApiKey();

      // Step 2: System Detection
      await this.detectSystem();

      // Step 3: Create initial config
      await this.createInitialConfig();

      StatusIndicator.success('First-time setup completed successfully!');
      console.log(chalk.green('\n🎉 AP is now ready to use!'));
      console.log(chalk.cyan('\nTry these commands:'));
      console.log('  ap status          # Check system status');
      console.log('  ap install git     # Install packages');
      console.log('  ap help           # Show help');

    } catch (error) {
      StatusIndicator.error('First-time setup failed', {
        details: error instanceof Error ? error.message : String(error)
      });
      throw error;
    }
  }

  /**
   * Setup API key with user input
   */
  private async setupApiKey(): Promise<void> {
    StatusIndicator.info('Setting up Gemini AI API key...');
    
    console.log(chalk.yellow('\n📋 AP requires a FREE Gemini API key for AI features.'));
    console.log(chalk.cyan('Get your API key from: https://aistudio.google.com/app/apikey\n'));

    const hasApiKey = await this.askYesNo('Do you have a Gemini API key?');

    if (!hasApiKey) {
      console.log(chalk.yellow('\n📖 How to get your API key:'));
      console.log('1. Visit: https://aistudio.google.com/app/apikey');
      console.log('2. Sign in with your Google account');
      console.log('3. Click "Create API Key"');
      console.log('4. Copy the generated key');
      console.log('\nThe Gemini API is FREE with generous limits:');
      console.log('• 15 requests per minute');
      console.log('• 1 million tokens per minute');
      console.log('• 1,500 requests per day\n');

      const continueSetup = await this.askYesNo('Continue with API key setup?');

      if (!continueSetup) {
        throw new Error('API key setup cancelled by user');
      }
    }

    const apiKey = await this.askPassword('Enter your Gemini API key:');

    if (!apiKey || apiKey.trim() === '') {
      throw new Error('API key cannot be empty');
    }

    if (apiKey.length < 20) {
      throw new Error('API key seems too short. Please check and try again.');
    }

    // Save API key to .env file
    await this.saveApiKey(apiKey.trim());
    StatusIndicator.success('API key configured successfully');
  }

  /**
   * Save API key to .env file
   */
  private async saveApiKey(apiKey: string): Promise<void> {
    let envContent = '';
    
    // Read existing .env file if it exists
    if (fs.existsSync(this.envPath)) {
      envContent = fs.readFileSync(this.envPath, 'utf8');
    }

    // Update or add GEMINI_API_KEY
    const apiKeyRegex = /^GEMINI_API_KEY=.*$/m;
    const newApiKeyLine = `GEMINI_API_KEY=${apiKey}`;

    if (apiKeyRegex.test(envContent)) {
      envContent = envContent.replace(apiKeyRegex, newApiKeyLine);
    } else {
      envContent += envContent.endsWith('\n') ? '' : '\n';
      envContent += `${newApiKeyLine}\n`;
    }

    fs.writeFileSync(this.envPath, envContent);
    
    // Update process.env for immediate use
    process.env.GEMINI_API_KEY = apiKey;
  }

  /**
   * Detect system information using enhanced platform-specific scripts
   */
  private async detectSystem(): Promise<any> {
    StatusIndicator.info('Running enhanced system detection...');
    
    try {
      // Run platform-specific detection script
      const systemInfo = await this.runPlatformDetectionScript();
      
      // Use AI to analyze the system and get recommendations
      await this.analyzeSystemWithAI(systemInfo);
      
      StatusIndicator.success('System detection and analysis completed');
      return systemInfo;
      
    } catch (error) {
      StatusIndicator.warning('Enhanced detection failed, using fallback method');
      console.warn('Detection error:', error);
      
      // Fallback to existing system detection
      const systemDetection = new SystemDetection();
      await systemDetection.detect({ verbose: false, showProgress: true });
      return systemDetection.getSystemData();
    }
  }

  /**
   * Run platform-specific system detection script
   */
  private async runPlatformDetectionScript(): Promise<any> {
    const { exec } = await import('child_process');
    const { promisify } = await import('util');
    const execAsync = promisify(exec);
    
    let scriptPath: string;
    let command: string;
    
    // Determine platform and script
    switch (process.platform) {
      case 'darwin':
        scriptPath = path.join(process.cwd(), 'scripts', 'detect-system-macos.sh');
        command = `bash "${scriptPath}"`;
        break;
      case 'linux':
        scriptPath = path.join(process.cwd(), 'scripts', 'detect-system-linux.sh');
        command = `bash "${scriptPath}"`;
        break;
      case 'win32':
        scriptPath = path.join(process.cwd(), 'scripts', 'detect-system-windows.bat');
        command = `"${scriptPath}"`;
        break;
      default:
        throw new Error(`Unsupported platform: ${process.platform}`);
    }

    StatusIndicator.info(`Running ${process.platform} system detection script...`);
    
    try {
      const { stdout, stderr } = await execAsync(command, { timeout: 30000 });
      
      if (stderr) {
        console.warn('Script warnings:', stderr);
      }
      
      const systemData = JSON.parse(stdout);
      StatusIndicator.success('Platform detection script completed');
      
      return systemData;
      
    } catch (error) {
      throw new Error(`Script execution failed: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * Analyze system with AI and display recommendations
   */
  private async analyzeSystemWithAI(systemData: any): Promise<void> {
    try {
      const { SystemAnalyzer } = await import('../ai/SystemAnalyzer.js');
      const analyzer = new SystemAnalyzer();
      
      const analysis = await analyzer.analyzeSystem(systemData);
      
      // Display AI analysis results
      analyzer.displayAnalysis(analysis);
      
      // Store AI recommendations in system data
      systemData.ai_analysis = analysis;
      
      // Handle special cases (like missing Homebrew on macOS)
      await this.handleSpecialRecommendations(analysis, systemData);
      
    } catch (error) {
      StatusIndicator.warning('AI analysis failed, continuing without recommendations');
      console.warn('AI analysis error:', error);
    }
  }

  /**
   * Handle special recommendations like installing Homebrew
   */
  private async handleSpecialRecommendations(analysis: any, systemData: any): Promise<void> {
    // Check if Homebrew needs to be installed on macOS
    if (systemData.platform === 'darwin' && 
        analysis.recommendedPackageManager === 'brew' && 
        !systemData.package_managers?.brew?.available) {
      
      console.log(chalk.yellow('\n🍺 Homebrew is recommended but not installed.'));
      
      const installHomebrew = await this.askYesNo('Would you like to install Homebrew now? (Recommended)');
      
      if (installHomebrew) {
        await this.installHomebrew();
      } else {
        console.log(chalk.gray('You can install Homebrew later with:'));
        console.log(chalk.cyan('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'));
      }
    }
  }

  /**
   * Install Homebrew on macOS
   */
  private async installHomebrew(): Promise<void> {
    StatusIndicator.info('Installing Homebrew...');
    
    try {
      const { exec } = await import('child_process');
      const { promisify } = await import('util');
      const execAsync = promisify(exec);
      
      const installCommand = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"';
      
      console.log(chalk.yellow('\nHomebrew installation will start. This may take a few minutes...'));
      console.log(chalk.gray('You may be prompted for your password.\n'));
      
      // Run Homebrew installation
      const { stdout, stderr } = await execAsync(installCommand, { 
        timeout: 300000, // 5 minutes timeout
        stdio: 'inherit'
      });
      
      if (stdout) console.log(stdout);
      if (stderr) console.log(stderr);
      
      StatusIndicator.success('Homebrew installation completed!');
      
      // Update PATH for current session
      process.env.PATH = `/opt/homebrew/bin:/usr/local/bin:${process.env.PATH}`;
      
    } catch (error) {
      StatusIndicator.error('Homebrew installation failed', {
        details: error instanceof Error ? error.message : String(error)
      });
      console.log(chalk.yellow('\nYou can install Homebrew manually later with:'));
      console.log(chalk.cyan('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'));
    }
  }

  /**
   * Create initial configuration file
   */
  private async createInitialConfig(): Promise<void> {
    StatusIndicator.info('Creating initial configuration...');

    // Ensure config directory exists
    if (!fs.existsSync(this.configDir)) {
      fs.mkdirSync(this.configDir, { recursive: true });
    }

    // Detect package managers
    const packageManager = new PackageManagerService();
    const availableManagers = packageManager.getAvailableManagers();
    const preferredManager = availableManagers[0] || (process.platform === 'darwin' ? 'brew' : 'apt');

    const config: UserConfig = {
      geminiApiKey: process.env.GEMINI_API_KEY || '',
      preferredPackageManager: preferredManager,
      preferredShell: process.env.SHELL || '/bin/bash',
      systemInfo: {}, // Will be populated by system detection
      userPreferences: {
        name: os.userInfo().username,
        workingDirectory: process.cwd(),
        autoUpdate: false,
        verboseOutput: false
      },
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    fs.writeFileSync(this.configPath, JSON.stringify(config, null, 2));
    StatusIndicator.success(`Configuration saved to ${this.configPath}`);
  }

  /**
   * Run preferences setup (for subsequent launches)
   */
  public async runPreferencesSetup(): Promise<void> {
    Banner.displayMinimal();
    
    console.log(chalk.cyan.bold('\n⚙️  AP Preferences Setup\n'));
    console.log('Let\'s customize AP to work better for you.\n');
    console.log(chalk.gray('(Press Enter to skip any question and use defaults)\n'));

    try {
      const config = await this.loadConfig();
      if (!config) {
        throw new Error('Configuration not found. Please run first-time setup.');
      }

      // Package Manager Preference with AI recommendations
      const packageManager = new PackageManagerService();
      const availableManagers = packageManager.getAvailableManagers();
      
      // Check if we have AI analysis with recommendations
      const aiRecommendation = config.systemInfo?.ai_analysis?.recommendedPackageManager;
      
      if (availableManagers.length > 1) {
        console.log('\nAvailable package managers:');
        availableManagers.forEach((manager, index) => {
          const isRecommended = manager === aiRecommendation;
          const marker = isRecommended ? chalk.green(' (AI Recommended)') : '';
          console.log(`  ${index + 1}. ${manager}${marker}`);
        });
        console.log(`  ${availableManagers.length + 1}. Keep current (${config.preferredPackageManager})`);
        
        if (aiRecommendation) {
          console.log(chalk.cyan(`\n💡 AI Recommendation: ${aiRecommendation}`));
          console.log(chalk.gray(`   ${config.systemInfo?.ai_analysis?.packageManagerReason || 'Best for your system'}`));
        }
        
        const defaultChoice = aiRecommendation && availableManagers.includes(aiRecommendation) 
          ? (availableManagers.indexOf(aiRecommendation) + 1).toString()
          : '1';
        
        const choice = await this.askText(`Choose package manager (1-${availableManagers.length + 1})`, defaultChoice);
        const choiceNum = parseInt(choice) - 1;
        
        if (choiceNum >= 0 && choiceNum < availableManagers.length) {
          config.preferredPackageManager = availableManagers[choiceNum];
        }
      } else if (aiRecommendation && !availableManagers.includes(aiRecommendation)) {
        console.log(chalk.yellow(`\n💡 AI recommends installing: ${aiRecommendation}`));
        console.log(chalk.gray(`   ${config.systemInfo?.ai_analysis?.packageManagerReason || 'Best for your system'}`));
      }

      // User Preferences
      const name = await this.askText('What should AP call you? (optional)', config.userPreferences.name);
      const autoUpdate = await this.askYesNo('Auto-update package lists when needed? (optional)');
      const verboseOutput = await this.askYesNo('Enable verbose output by default? (optional)');

      const preferences = {
        name: name || config.userPreferences.name,
        autoUpdate,
        verboseOutput
      };

      // Update config
      config.userPreferences = { ...config.userPreferences, ...preferences };
      config.updatedAt = new Date().toISOString();

      await this.saveConfig(config);
      StatusIndicator.success('Preferences updated successfully!');

    } catch (error) {
      StatusIndicator.error('Preferences setup failed', {
        details: error instanceof Error ? error.message : String(error)
      });
      throw error;
    }
  }

  /**
   * Load configuration from file
   */
  public async loadConfig(): Promise<UserConfig | null> {
    try {
      if (fs.existsSync(this.configPath)) {
        const configData = fs.readFileSync(this.configPath, 'utf8');
        return JSON.parse(configData);
      }
    } catch (error) {
      console.warn('Could not load configuration:', error);
    }
    return null;
  }

  /**
   * Save configuration to file
   */
  public async saveConfig(config: UserConfig): Promise<void> {
    if (!fs.existsSync(this.configDir)) {
      fs.mkdirSync(this.configDir, { recursive: true });
    }
    
    config.updatedAt = new Date().toISOString();
    fs.writeFileSync(this.configPath, JSON.stringify(config, null, 2));
  }

  /**
   * Get configuration status
   */
  public getConfigStatus(): FirstTimeConfig {
    return {
      isFirstTime: this.isFirstTime(),
      apiKeyConfigured: this.isApiKeyConfigured(),
      systemDetected: fs.existsSync(this.configPath),
      preferencesSet: fs.existsSync(this.configPath),
      configPath: this.configPath
    };
  }

  /**
   * Read file utility
   */
  public readFile(filePath: string): string | null {
    try {
      if (fs.existsSync(filePath)) {
        return fs.readFileSync(filePath, 'utf8');
      }
    } catch (error) {
      console.warn(`Could not read file ${filePath}:`, error);
    }
    return null;
  }

  /**
   * Write file utility
   */
  public writeFile(filePath: string, content: string): boolean {
    try {
      const dir = path.dirname(filePath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      fs.writeFileSync(filePath, content);
      return true;
    } catch (error) {
      console.warn(`Could not write file ${filePath}:`, error);
      return false;
    }
  }

  /**
   * Append to file utility
   */
  public appendFile(filePath: string, content: string): boolean {
    try {
      const dir = path.dirname(filePath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      fs.appendFileSync(filePath, content);
      return true;
    } catch (error) {
      console.warn(`Could not append to file ${filePath}:`, error);
      return false;
    }
  }

  /**
   * Simple yes/no prompt
   */
  private async askYesNo(question: string): Promise<boolean> {
    const rl = createInterface({
      input: process.stdin,
      output: process.stdout
    });

    return new Promise((resolve) => {
      rl.question(`${question} (y/N): `, (answer) => {
        rl.close();
        resolve(answer.toLowerCase().startsWith('y'));
      });
    });
  }

  /**
   * Simple password prompt
   */
  private async askPassword(question: string): Promise<string> {
    const rl = createInterface({
      input: process.stdin,
      output: process.stdout
    });

    return new Promise((resolve) => {
      rl.question(`${question} `, (answer) => {
        rl.close();
        resolve(answer);
      });
    });
  }

  /**
   * Simple text prompt
   */
  private async askText(question: string, defaultValue?: string): Promise<string> {
    const rl = createInterface({
      input: process.stdin,
      output: process.stdout
    });

    const prompt = defaultValue ? `${question} (${defaultValue}): ` : `${question}: `;

    return new Promise((resolve) => {
      rl.question(prompt, (answer) => {
        rl.close();
        resolve(answer.trim() || defaultValue || '');
      });
    });
  }
}