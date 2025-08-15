import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { exec } from 'child_process';
import { promisify } from 'util';
import chalk from 'chalk';

const execAsync = promisify(exec);

export interface SystemInfo {
  timestamp: string;
  system: {
    hostname: string;
    username: string;
    home_directory: string;
    current_directory: string;
    shell: string;
    shell_version: string;
    terminal: string;
    display: string;
  };
  os: {
    kernel: string;
    kernel_version: string;
    architecture: string;
    platform: string;
    os_release: Record<string, string>;
  };
  hardware: {
    cpu_info: string;
    cpu_cores: string;
    memory_total: string;
    memory_available: string;
    disk_usage: string;
  };
  package_managers: Record<string, boolean>;
  development_tools: Record<string, string | boolean>;
  desktop_environment: Record<string, string>;
  network: {
    hostname_fqdn: string;
    ip_address: string;
    internet_connection: boolean;
  };
  paths: Record<string, string>;
}

export interface UserPreferences {
  name: string;
  preferred_name: string;
  text_editor: string;
  code_editor: string;
  terminal_preference: string;
  package_manager_preference: string[];
  development_languages: string[];
  work_style: string;
  automation_level: string;
  notification_preference: string;
  theme_preference: string;
  timezone: string;
}

export interface KiraProfile {
  version: string;
  created_at: string;
  updated_at: string;
  system_info: SystemInfo;
  user_preferences: UserPreferences;
  ai_context: string;
}

export class InitWizard {
  private profilePath: string;
  private systemInfo: SystemInfo | null = null;

  constructor() {
    this.profilePath = path.join(os.homedir(), '.kira', 'profile.json');
  }

  async run(): Promise<void> {
    console.log(chalk.cyan.bold('\n🚀 Kira Initialization Wizard\n'));
    console.log('Welcome! Let\'s set up Kira to work perfectly with your system and preferences.\n');

    // Check if already initialized
    if (await this.isAlreadyInitialized()) {
      const shouldReinit = await this.askYesNo('Kira is already initialized. Do you want to reinitialize?');
      if (!shouldReinit) {
        console.log(chalk.green('✅ Kira initialization skipped.'));
        return;
      }
    }

    try {
      // Step 1: Detect system information
      console.log(chalk.yellow('🔍 Step 1: Detecting your system...'));
      await this.detectSystemInfo();

      // Step 2: Gather user preferences
      console.log(chalk.yellow('\n👤 Step 2: Setting up your preferences...'));
      const userPreferences = await this.gatherUserPreferences();

      // Step 3: Create AI context
      console.log(chalk.yellow('\n🤖 Step 3: Creating AI context...'));
      const aiContext = this.createAIContext(userPreferences);

      // Step 4: Save profile
      console.log(chalk.yellow('\n💾 Step 4: Saving your profile...'));
      await this.saveProfile(userPreferences, aiContext);

      // Step 5: Final setup
      console.log(chalk.yellow('\n⚙️  Step 5: Final configuration...'));
      await this.finalSetup();

      console.log(chalk.green.bold('\n🎉 Kira initialization complete!'));
      console.log(chalk.cyan('\n📋 What\'s next:'));
      console.log('• Try: kira check my system');
      console.log('• Try: kira install my favorite editor');
      console.log('• Try: kira help me set up a development environment');
      console.log('• Your preferences are saved in ~/.kira/profile.json');

    } catch (error) {
      console.error(chalk.red('\n❌ Initialization failed:'), error);
      console.log(chalk.yellow('You can try running "kira init" again.'));
    }
  }

  private async isAlreadyInitialized(): Promise<boolean> {
    return fs.existsSync(this.profilePath);
  }

  private async detectSystemInfo(): Promise<void> {
    try {
      console.log('   Gathering system information...');
      
      // Run the system detection script
      const scriptPath = path.join(process.cwd(), 'scripts', 'detect-system.sh');
      const { stdout } = await execAsync(`bash ${scriptPath}`);
      
      this.systemInfo = JSON.parse(stdout);
      
      console.log(chalk.green('   ✅ System detected:'));
      console.log(`      OS: ${this.systemInfo?.os.os_release.PRETTY_NAME || 'Unknown'}`);
      console.log(`      Architecture: ${this.systemInfo?.os.architecture}`);
      console.log(`      Shell: ${this.systemInfo?.system.shell}`);
      console.log(`      CPU: ${this.systemInfo?.hardware.cpu_info}`);
      console.log(`      Memory: ${this.systemInfo?.hardware.memory_total}`);
      
    } catch (error) {
      console.warn(chalk.yellow('   ⚠️  Could not detect all system information'));
      // Create minimal system info
      this.systemInfo = {
        timestamp: new Date().toISOString(),
        system: {
          hostname: os.hostname(),
          username: os.userInfo().username,
          home_directory: os.homedir(),
          current_directory: process.cwd(),
          shell: process.env.SHELL || '/bin/bash',
          shell_version: 'unknown',
          terminal: process.env.TERM || 'unknown',
          display: process.env.DISPLAY || ''
        },
        os: {
          kernel: os.type(),
          kernel_version: os.release(),
          architecture: os.arch(),
          platform: os.platform(),
          os_release: {}
        },
        hardware: {
          cpu_info: os.cpus()[0]?.model || 'unknown',
          cpu_cores: os.cpus().length.toString(),
          memory_total: Math.round(os.totalmem() / 1024 / 1024 / 1024) + 'GB',
          memory_available: Math.round(os.freemem() / 1024 / 1024 / 1024) + 'GB',
          disk_usage: 'unknown'
        },
        package_managers: {},
        development_tools: {},
        desktop_environment: {},
        network: {
          hostname_fqdn: os.hostname(),
          ip_address: 'unknown',
          internet_connection: false
        },
        paths: {}
      };
    }
  }

  private async gatherUserPreferences(): Promise<UserPreferences> {
    console.log('   Please answer a few questions to personalize Kira:\n');

    const preferences: UserPreferences = {
      name: this.systemInfo?.system.username || 'user',
      preferred_name: await this.askQuestion('What should Kira call you?', this.systemInfo?.system.username || 'user'),
      text_editor: await this.askChoice('What\'s your preferred text editor?', 
        ['nano', 'vim', 'emacs', 'code', 'other'], 'nano'),
      code_editor: await this.askChoice('What\'s your preferred code editor?', 
        ['vscode', 'vim', 'emacs', 'sublime', 'atom', 'jetbrains', 'other'], 'vscode'),
      terminal_preference: await this.askChoice('What\'s your preferred terminal?', 
        ['bash', 'zsh', 'fish', 'current'], 'current'),
      package_manager_preference: await this.askMultiChoice('Preferred package managers (in order)?', 
        this.getPackageManagerOptions(), this.detectPreferredPackageManagers()),
      development_languages: await this.askMultiChoice('What programming languages do you use?', 
        ['javascript', 'typescript', 'python', 'rust', 'go', 'java', 'c++', 'php', 'ruby', 'other'], []),
      work_style: await this.askChoice('How do you prefer to work?', 
        ['minimal-commands', 'detailed-explanations', 'step-by-step', 'autonomous'], 'step-by-step'),
      automation_level: await this.askChoice('How much automation do you want?', 
        ['conservative', 'moderate', 'aggressive', 'ask-first'], 'moderate'),
      notification_preference: await this.askChoice('Notification preference?', 
        ['minimal', 'important-only', 'verbose', 'silent'], 'important-only'),
      theme_preference: await this.askChoice('Interface theme preference?', 
        ['dark', 'light', 'auto', 'colorful'], 'auto'),
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
    };

    return preferences;
  }

  private createAIContext(preferences: UserPreferences): string {
    const isMacOS = this.systemInfo?.system.os_type === 'Darwin';
    const osName = isMacOS ? 'macOS' : 'Linux';
    const distro = isMacOS ? 'macos' : (this.systemInfo?.os.os_release.ID || 'linux');
    const packageManagers = Object.entries(this.systemInfo?.package_managers || {})
      .filter(([_, available]) => available)
      .map(([name, _]) => name);

    return `User Profile for AI Context:
- Name: ${preferences.preferred_name}
- Operating System: ${osName}
- System: ${this.systemInfo?.os.os_release.PRETTY_NAME || osName} (${this.systemInfo?.os.architecture})
- Distribution: ${distro}
- Shell: ${this.systemInfo?.system.shell}
- Available Package Managers: ${packageManagers.join(', ')}
- Preferred Package Managers: ${preferences.package_manager_preference.join(', ')}
- Text Editor: ${preferences.text_editor}
- Code Editor: ${preferences.code_editor}
- Programming Languages: ${preferences.development_languages.join(', ')}
- Work Style: ${preferences.work_style}
- Automation Level: ${preferences.automation_level}
- CPU: ${this.systemInfo?.hardware.cpu_info}
- Memory: ${this.systemInfo?.hardware.memory_total}

Instructions for AI:
- Always address the user as "${preferences.preferred_name}"
- Operating System: ${osName} - use appropriate commands and package managers
- Use ${preferences.package_manager_preference[0]} as the primary package manager
- ${isMacOS ? 'For macOS: Use brew for CLI tools, brew --cask for GUI apps, mas for App Store apps' : 'For Linux: Use appropriate package manager based on distribution'}
- Prefer ${preferences.text_editor} for text editing tasks
- Prefer ${preferences.code_editor} for code editing tasks
- Automation level is "${preferences.automation_level}" - adjust command suggestions accordingly
- Work style is "${preferences.work_style}" - provide appropriate level of detail
- When suggesting installations, prioritize: ${preferences.package_manager_preference.join(' > ')}
- System has ${this.systemInfo?.hardware.cpu_cores} CPU cores and ${this.systemInfo?.hardware.memory_total} memory
- User develops in: ${preferences.development_languages.join(', ')}
- ${isMacOS ? 'macOS-specific: Use open command for launching apps, prefer GUI applications when available' : 'Linux-specific: Use appropriate desktop environment commands'}`;
  }

  private async saveProfile(preferences: UserPreferences, aiContext: string): Promise<void> {
    const profile: KiraProfile = {
      version: '1.0.0',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      system_info: this.systemInfo!,
      user_preferences: preferences,
      ai_context: aiContext
    };

    // Ensure .kira directory exists
    const kiraDir = path.dirname(this.profilePath);
    if (!fs.existsSync(kiraDir)) {
      fs.mkdirSync(kiraDir, { recursive: true });
    }

    // Save profile
    fs.writeFileSync(this.profilePath, JSON.stringify(profile, null, 2));
    console.log(`   ✅ Profile saved to ${this.profilePath}`);
  }

  private async finalSetup(): Promise<void> {
    // Create any additional configuration files or setup
    console.log('   ✅ Configuration complete');
  }

  // Helper methods for user interaction
  private async askQuestion(question: string, defaultValue: string = ''): Promise<string> {
    // In a real implementation, this would use a proper prompt library
    // For now, return default or simulate user input
    console.log(`   ${question} ${defaultValue ? `(default: ${defaultValue})` : ''}`);
    return defaultValue || 'user';
  }

  private async askChoice(question: string, choices: string[], defaultChoice: string): Promise<string> {
    console.log(`   ${question}`);
    console.log(`   Options: ${choices.join(', ')} (default: ${defaultChoice})`);
    return defaultChoice;
  }

  private async askMultiChoice(question: string, choices: string[], defaultChoices: string[]): Promise<string[]> {
    console.log(`   ${question}`);
    console.log(`   Options: ${choices.join(', ')} (default: ${defaultChoices.join(', ')})`);
    return defaultChoices;
  }

  private async askYesNo(question: string): Promise<boolean> {
    console.log(`   ${question} (y/N)`);
    return false; // Default to no for safety
  }

  private getPackageManagerOptions(): string[] {
    const isMacOS = process.platform === 'darwin';
    return isMacOS 
      ? ['brew', 'brew-cask', 'mas', 'port', 'npm', 'pip', 'cargo']
      : ['apt', 'pacman', 'yum', 'dnf', 'zypper', 'snap', 'flatpak', 'npm', 'pip', 'cargo'];
  }

  private detectPreferredPackageManagers(): string[] {
    if (!this.systemInfo?.package_managers) {
      return process.platform === 'darwin' ? ['brew'] : ['apt'];
    }
    
    const available = Object.entries(this.systemInfo.package_managers)
      .filter(([_, isAvailable]) => isAvailable)
      .map(([name, _]) => name);

    // Order by preference based on OS
    const isMacOS = process.platform === 'darwin';
    const preferenceOrder = isMacOS
      ? ['brew', 'brew-cask', 'mas', 'port', 'npm', 'pip', 'cargo']
      : ['apt', 'pacman', 'dnf', 'yum', 'zypper', 'apk', 'snap', 'flatpak', 'npm', 'pip', 'cargo'];
    
    return preferenceOrder.filter(pm => available.includes(pm));
  }
}