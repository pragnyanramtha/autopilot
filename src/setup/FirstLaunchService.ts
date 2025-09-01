import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { createInterface } from 'readline';
import { GoogleGenerativeAI } from '@google/generative-ai';
import chalk from 'chalk';
import { StatusIndicator } from '../ui/components/StatusIndicator.js';
import { Banner } from '../ui/components/Banner.js';

export interface OSInfo {
  platform: 'windows' | 'macos' | 'linux';
  version: string;
  architecture: string;
  capabilities: SystemCapabilities;
}

export interface SystemCapabilities {
  hasNodeJS: boolean;
  hasNPM: boolean;
  hasBash: boolean;
  hasGit: boolean;
  packageManagers: string[];
}

export interface APIConfig {
  geminiApiKey: string;
  model: 'gemini-2.5-pro';
  validated: boolean;
  validatedAt: string;
}

export interface SystemConfig {
  osInfo: OSInfo;
  apiConfig: APIConfig;
  setupComplete: boolean;
  createdAt: string;
}

export class FirstLaunchService {
  private configDir: string;
  private configPath: string;
  private envPath: string;

  constructor() {
    this.configDir = path.join(os.homedir(), '.ap');
    this.configPath = path.join(this.configDir, 'autopilot-config.json');
    this.envPath = path.join(process.cwd(), '.env');
  }

  /**
   * Check if this is the first launch
   */
  public isFirstLaunch(): boolean {
    return !fs.existsSync(this.configPath);
  }

  /**
   * Run the complete first-launch setup flow
   */
  public async runFirstLaunchSetup(): Promise<void> {
    Banner.display({ showVersion: true, showTagline: true });
    
    console.log(chalk.cyan.bold('\n🚀 Welcome to AP Autopilot System!\n'));
    console.log('Setting up your AI-powered automation assistant...\n');

    try {
      // Step 1: Detect Operating System
      StatusIndicator.info('Detecting your operating system...');
      const osInfo = await this.detectOperatingSystem();
      StatusIndicator.success(`Detected: ${osInfo.platform} ${osInfo.version} (${osInfo.architecture})`);

      // Step 2: Setup Gemini 2.5 Pro API
      StatusIndicator.info('Setting up Gemini 2.5 Pro API...');
      const apiConfig = await this.setupGeminiAPI();
      StatusIndicator.success('Gemini 2.5 Pro API configured successfully');

      // Step 3: Save configuration
      const config: SystemConfig = {
        osInfo,
        apiConfig,
        setupComplete: true,
        createdAt: new Date().toISOString()
      };

      await this.saveConfiguration(config);
      StatusIndicator.success('Configuration saved successfully');

      console.log(chalk.green.bold('\n🎉 AP Autopilot System is ready!'));
      console.log(chalk.cyan('\nYou can now use natural language commands like:'));
      console.log('  • "install firefox and open it"');
      console.log('  • "create a new folder called projects"');
      console.log('  • "check my system status"');
      console.log('  • "help me set up a development environment"\n');

    } catch (error) {
      StatusIndicator.error('First-launch setup failed', {
        details: error instanceof Error ? error.message : String(error)
      });
      throw error;
    }
  }

  /**
   * Detect operating system using Node.js platform APIs and system commands
   */
  public async detectOperatingSystem(): Promise<OSInfo> {
    const platform = process.platform;
    const arch = process.arch;
    const release = os.release();

    let detectedPlatform: 'windows' | 'macos' | 'linux';
    let version = release;

    // Map Node.js platform to our platform types
    switch (platform) {
      case 'darwin':
        detectedPlatform = 'macos';
        version = await this.getMacOSVersion();
        break;
      case 'win32':
        detectedPlatform = 'windows';
        version = await this.getWindowsVersion();
        break;
      case 'linux':
        detectedPlatform = 'linux';
        version = await this.getLinuxVersion();
        break;
      default:
        throw new Error(`Unsupported platform: ${platform}`);
    }

    // Detect system capabilities
    const capabilities = await this.detectSystemCapabilities();

    return {
      platform: detectedPlatform,
      version,
      architecture: arch,
      capabilities
    };
  }

  /**
   * Get macOS version information
   */
  private async getMacOSVersion(): Promise<string> {
    try {
      const { exec } = await import('child_process');
      const { promisify } = await import('util');
      const execAsync = promisify(exec);
      
      const { stdout } = await execAsync('sw_vers -productVersion');
      return `macOS ${stdout.trim()}`;
    } catch (error) {
      return `macOS ${os.release()}`;
    }
  }

  /**
   * Get Windows version information
   */
  private async getWindowsVersion(): Promise<string> {
    try {
      const { exec } = await import('child_process');
      const { promisify } = await import('util');
      const execAsync = promisify(exec);
      
      const { stdout } = await execAsync('ver');
      const versionMatch = stdout.match(/\d+\.\d+\.\d+/);
      return versionMatch ? `Windows ${versionMatch[0]}` : `Windows ${os.release()}`;
    } catch (error) {
      return `Windows ${os.release()}`;
    }
  }

  /**
   * Get Linux version information
   */
  private async getLinuxVersion(): Promise<string> {
    try {
      // Try to read /etc/os-release first
      if (fs.existsSync('/etc/os-release')) {
        const osRelease = fs.readFileSync('/etc/os-release', 'utf8');
        const prettyNameMatch = osRelease.match(/PRETTY_NAME="([^"]+)"/);
        if (prettyNameMatch) {
          return prettyNameMatch[1];
        }
      }

      // Fallback to lsb_release
      const { exec } = await import('child_process');
      const { promisify } = await import('util');
      const execAsync = promisify(exec);
      
      const { stdout } = await execAsync('lsb_release -d -s');
      return stdout.trim().replace(/"/g, '');
    } catch (error) {
      return `Linux ${os.release()}`;
    }
  }

  /**
   * Detect system capabilities
   */
  private async detectSystemCapabilities(): Promise<SystemCapabilities> {
    const capabilities: SystemCapabilities = {
      hasNodeJS: false,
      hasNPM: false,
      hasBash: false,
      hasGit: false,
      packageManagers: []
    };

    try {
      const { exec } = await import('child_process');
      const { promisify } = await import('util');
      const execAsync = promisify(exec);

      // Check Node.js
      try {
        await execAsync('node --version');
        capabilities.hasNodeJS = true;
      } catch {}

      // Check NPM
      try {
        await execAsync('npm --version');
        capabilities.hasNPM = true;
      } catch {}

      // Check Bash
      try {
        await execAsync('bash --version');
        capabilities.hasBash = true;
      } catch {}

      // Check Git
      try {
        await execAsync('git --version');
        capabilities.hasGit = true;
      } catch {}

      // Detect package managers
      const packageManagers = ['apt', 'brew', 'yum', 'dnf', 'pacman', 'zypper', 'apk', 'winget', 'choco'];
      
      for (const pm of packageManagers) {
        try {
          await execAsync(`${pm} --version`);
          capabilities.packageManagers.push(pm);
        } catch {}
      }

    } catch (error) {
      console.warn('Error detecting system capabilities:', error);
    }

    return capabilities;
  }

  /**
   * Setup Gemini 2.5 Pro API with interactive key input and validation
   */
  public async setupGeminiAPI(): Promise<APIConfig> {
    console.log(chalk.yellow('\n📋 AP requires a FREE Gemini API key for AI automation.'));
    console.log(chalk.cyan('Get your API key from: https://aistudio.google.com/app/apikey\n'));

    const hasApiKey = await this.askYesNo('Do you have a Gemini API key?');

    if (!hasApiKey) {
      console.log(chalk.yellow('\n📖 How to get your FREE API key:'));
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

    let apiKey: string;
    let isValid = false;

    while (!isValid) {
      apiKey = await this.askPassword('Enter your Gemini API key:');

      if (!apiKey || apiKey.trim() === '') {
        StatusIndicator.error('API key cannot be empty');
        continue;
      }

      if (apiKey.length < 20) {
        StatusIndicator.error('API key seems too short. Please check and try again.');
        continue;
      }

      // Validate API key with real-time validation against Gemini 2.5 Pro
      StatusIndicator.info('Validating API key with Gemini 2.5 Pro...');
      isValid = await this.validateAPIKey(apiKey.trim());

      if (!isValid) {
        StatusIndicator.error('API key validation failed. Please check your key and try again.');
        const retry = await this.askYesNo('Would you like to try again?');
        if (!retry) {
          throw new Error('API key setup cancelled by user');
        }
      }
    }

    // Save API key to .env file
    await this.saveApiKeyToEnv(apiKey!.trim());

    return {
      geminiApiKey: apiKey!.trim(),
      model: 'gemini-2.5-pro',
      validated: true,
      validatedAt: new Date().toISOString()
    };
  }

  /**
   * Validate API key against Gemini 2.5 Pro model
   */
  public async validateAPIKey(apiKey: string): Promise<boolean> {
    try {
      const genAI = new GoogleGenerativeAI(apiKey);
      
      // Try to use Gemini 2.5 Pro model specifically
      const model = genAI.getGenerativeModel({ model: 'gemini-2.5-pro' });
      
      // Send a simple test prompt
      const result = await model.generateContent('Hello, please respond with "API key is valid"');
      const response = await result.response;
      const text = response.text();
      
      // Check if we got a valid response
      return text && text.length > 0;
      
    } catch (error: any) {
      // Check for specific error types
      if (error.message?.includes('API_KEY_INVALID') || 
          error.message?.includes('invalid API key') ||
          error.status === 400) {
        return false;
      }
      
      // For other errors (network, etc.), we'll assume the key might be valid
      console.warn('API validation warning:', error.message);
      return true;
    }
  }

  /**
   * Save API key to .env file
   */
  private async saveApiKeyToEnv(apiKey: string): Promise<void> {
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
   * Save configuration to file
   */
  public async saveConfiguration(config: SystemConfig): Promise<void> {
    // Ensure config directory exists
    if (!fs.existsSync(this.configDir)) {
      fs.mkdirSync(this.configDir, { recursive: true });
    }

    fs.writeFileSync(this.configPath, JSON.stringify(config, null, 2));
  }

  /**
   * Load configuration from file
   */
  public async loadConfiguration(): Promise<SystemConfig | null> {
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
   * Check if API key is configured
   */
  public isApiKeyConfigured(): boolean {
    // Check environment variable first
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
   * Simple password prompt (shows input for API keys)
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
}