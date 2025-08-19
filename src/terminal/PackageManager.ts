import { exec } from 'child_process';
import { promisify } from 'util';
import { StatusIndicator, StatusType } from '../ui/components/StatusIndicator.js';
import { ProgressBar, Spinner } from '../ui/components/ProgressBar.js';
import { SystemInfo } from '../ui/formatters/SystemInfo.js';
import { ErrorDisplay } from '../ui/formatters/ErrorDisplay.js';
import { colors } from '../ui/utils/Colors.js';
import { symbols } from '../ui/utils/Symbols.js';

const execAsync = promisify(exec);

export interface PackageInfo {
  name: string;
  version?: string;
  description?: string;
  installed: boolean;
  availableIn: string[];
}

export interface PackageManager {
  name: string;
  installCommand: (pkg: string) => string;
  searchCommand: (pkg: string) => string;
  updateCommand: string;
  listInstalledCommand: string;
  isAvailable: () => Promise<boolean>;
}

export class PackageManagerService {
  private packageManagers: PackageManager[] = [
    // macOS Package Managers
    {
      name: 'brew',
      installCommand: (pkg: string) => `brew install ${pkg}`,
      searchCommand: (pkg: string) => `brew search ${pkg}`,
      updateCommand: 'brew update && brew upgrade',
      listInstalledCommand: 'brew list',
      isAvailable: async () => this.commandExists('brew')
    },
    {
      name: 'brew-cask',
      installCommand: (pkg: string) => `brew install --cask ${pkg}`,
      searchCommand: (pkg: string) => `brew search --cask ${pkg}`,
      updateCommand: 'brew update && brew upgrade --cask',
      listInstalledCommand: 'brew list --cask',
      isAvailable: async () => this.commandExists('brew')
    },
    {
      name: 'mas',
      installCommand: (pkg: string) => `mas install ${pkg}`,
      searchCommand: (pkg: string) => `mas search ${pkg}`,
      updateCommand: 'mas upgrade',
      listInstalledCommand: 'mas list',
      isAvailable: async () => this.commandExists('mas')
    },
    {
      name: 'port',
      installCommand: (pkg: string) => `sudo port install ${pkg}`,
      searchCommand: (pkg: string) => `port search ${pkg}`,
      updateCommand: 'sudo port selfupdate && sudo port upgrade outdated',
      listInstalledCommand: 'port installed',
      isAvailable: async () => this.commandExists('port')
    },
    // Linux Package Managers
    {
      name: 'apt',
      installCommand: (pkg: string) => `sudo apt install -y ${pkg}`,
      searchCommand: (pkg: string) => `apt search ${pkg}`,
      updateCommand: 'sudo apt update',
      listInstalledCommand: 'apt list --installed',
      isAvailable: async () => this.commandExists('apt')
    },
    {
      name: 'snap',
      installCommand: (pkg: string) => `sudo snap install ${pkg}`,
      searchCommand: (pkg: string) => `snap find ${pkg}`,
      updateCommand: 'sudo snap refresh',
      listInstalledCommand: 'snap list',
      isAvailable: async () => this.commandExists('snap')
    },
    {
      name: 'flatpak',
      installCommand: (pkg: string) => `flatpak install -y ${pkg}`,
      searchCommand: (pkg: string) => `flatpak search ${pkg}`,
      updateCommand: 'flatpak update -y',
      listInstalledCommand: 'flatpak list',
      isAvailable: async () => this.commandExists('flatpak')
    },
    {
      name: 'npm',
      installCommand: (pkg: string) => `npm install -g ${pkg}`,
      searchCommand: (pkg: string) => `npm search ${pkg}`,
      updateCommand: 'npm update -g',
      listInstalledCommand: 'npm list -g --depth=0',
      isAvailable: async () => this.commandExists('npm')
    },
    {
      name: 'pip',
      installCommand: (pkg: string) => `pip install ${pkg}`,
      searchCommand: (pkg: string) => `pip search ${pkg}`,
      updateCommand: 'pip list --outdated',
      listInstalledCommand: 'pip list',
      isAvailable: async () => this.commandExists('pip') || this.commandExists('pip3')
    },
    {
      name: 'cargo',
      installCommand: (pkg: string) => `cargo install ${pkg}`,
      searchCommand: (pkg: string) => `cargo search ${pkg}`,
      updateCommand: 'cargo install-update -a',
      listInstalledCommand: 'cargo install --list',
      isAvailable: async () => this.commandExists('cargo')
    }
  ];

  private availableManagers: PackageManager[] = [];
  private initialized = false;

  async initialize(): Promise<void> {
    if (this.initialized) return;

    const spinner = new Spinner('Detecting available package managers...');
    spinner.start();
    
    const detectedManagers: string[] = [];
    
    for (const manager of this.packageManagers) {
      spinner.update(`Checking ${manager.name}...`);
      if (await manager.isAvailable()) {
        this.availableManagers.push(manager);
        detectedManagers.push(manager.name);
      }
    }

    spinner.stop();

    if (this.availableManagers.length === 0) {
      StatusIndicator.warning('No package managers detected!', {
        details: 'Consider installing: apt, snap, flatpak, npm, pip, or cargo'
      });
    } else {
      StatusIndicator.success(`Found ${this.availableManagers.length} package manager(s)`, {
        details: detectedManagers.join(', ')
      });
    }

    this.initialized = true;
  }

  async installPackage(packageName: string): Promise<{ success: boolean; manager?: string; output?: string; error?: string }> {
    await this.initialize();

    if (this.availableManagers.length === 0) {
      StatusIndicator.error('No package managers available');
      return { success: false, error: 'No package managers available' };
    }

    // Try each package manager in order of preference
    const preferredOrder = this.getPreferredOrder();
    const progressBar = new ProgressBar({
      total: preferredOrder.length,
      message: `Installing ${packageName}...`,
      showPercentage: false,
      showNumbers: true
    });
    
    for (let i = 0; i < preferredOrder.length; i++) {
      const manager = preferredOrder[i];
      
      try {
        progressBar.update(i, `Trying ${manager.name}...`);
        
        const installCmd = manager.installCommand(packageName);
        const { stdout, stderr } = await execAsync(installCmd, { timeout: 300000 });
        
        progressBar.complete(`Successfully installed ${packageName} with ${manager.name}`);
        StatusIndicator.success(`Package ${packageName} installed successfully`, {
          details: `Using ${manager.name} package manager`
        });
        
        return { 
          success: true, 
          manager: manager.name, 
          output: stdout 
        };
        
      } catch (error: any) {
        StatusIndicator.warning(`Failed with ${manager.name}`, {
          details: error.message
        });
        
        // If this is the last manager, return the error
        if (manager === preferredOrder[preferredOrder.length - 1]) {
          progressBar.fail(`All package managers failed for ${packageName}`);
          
          ErrorDisplay.show(error, {
            title: 'Package Installation Failed',
            message: `Unable to install ${packageName} with any available package manager`,
            suggestions: [
              'Check if the package name is correct',
              'Verify your internet connection',
              'Try installing manually with your preferred package manager',
              'Check if you have sufficient permissions'
            ]
          });
          
          return { 
            success: false, 
            error: error.message,
            manager: manager.name 
          };
        }
        
        // Otherwise, continue to next manager
        continue;
      }
    }

    return { success: false, error: 'All package managers failed' };
  }

  async searchPackage(packageName: string): Promise<PackageInfo[]> {
    await this.initialize();

    const results: PackageInfo[] = [];
    
    for (const manager of this.availableManagers) {
      try {
        const searchCmd = manager.searchCommand(packageName);
        const { stdout } = await execAsync(searchCmd, { timeout: 30000 });
        
        // Parse search results (simplified - would need specific parsing for each manager)
        if (stdout.toLowerCase().includes(packageName.toLowerCase())) {
          results.push({
            name: packageName,
            installed: false,
            availableIn: [manager.name],
            description: `Available in ${manager.name}`
          });
        }
      } catch (error) {
        // Ignore search errors and continue
        continue;
      }
    }

    return results;
  }

  async isPackageInstalled(packageName: string): Promise<{ installed: boolean; manager?: string; version?: string }> {
    await this.initialize();

    for (const manager of this.availableManagers) {
      try {
        // Try to check if package is installed
        let checkCmd = '';
        
        switch (manager.name) {
          case 'brew':
            checkCmd = `brew list | grep ${packageName}`;
            break;
          case 'brew-cask':
            checkCmd = `brew list --cask | grep ${packageName}`;
            break;
          case 'mas':
            checkCmd = `mas list | grep ${packageName}`;
            break;
          case 'port':
            checkCmd = `port installed | grep ${packageName}`;
            break;
          case 'apt':
            checkCmd = `dpkg -l | grep ${packageName}`;
            break;
          case 'snap':
            checkCmd = `snap list | grep ${packageName}`;
            break;
          case 'flatpak':
            checkCmd = `flatpak list | grep ${packageName}`;
            break;
          case 'npm':
            checkCmd = `npm list -g ${packageName}`;
            break;
          case 'pip':
            checkCmd = `pip show ${packageName}`;
            break;
          case 'cargo':
            checkCmd = `cargo install --list | grep ${packageName}`;
            break;
          default:
            continue;
        }

        const { stdout } = await execAsync(checkCmd, { timeout: 10000 });
        
        if (stdout.trim()) {
          const version = this.extractVersion(stdout, manager.name);
          return { 
            installed: true, 
            manager: manager.name,
            ...(version && { version })
          };
        }
      } catch (error) {
        // Package not found with this manager, continue
        continue;
      }
    }

    return { installed: false };
  }

  async updatePackageLists(): Promise<void> {
    await this.initialize();

    if (this.availableManagers.length === 0) {
      StatusIndicator.warning('No package managers available to update');
      return;
    }

    StatusIndicator.info('Updating package lists...');
    
    const progressBar = new ProgressBar({
      total: this.availableManagers.length,
      message: 'Updating package managers...',
      showPercentage: true,
      showNumbers: true
    });
    
    const results: Array<{ manager: string; success: boolean; error?: string }> = [];
    
    for (let i = 0; i < this.availableManagers.length; i++) {
      const manager = this.availableManagers[i];
      
      try {
        progressBar.update(i, `Updating ${manager.name}...`);
        await execAsync(manager.updateCommand, { timeout: 120000 });
        
        results.push({ manager: manager.name, success: true });
        StatusIndicator.success(`${manager.name} updated successfully`);
        
      } catch (error: any) {
        results.push({ 
          manager: manager.name, 
          success: false, 
          error: error.message 
        });
        StatusIndicator.warning(`Failed to update ${manager.name}`, {
          details: error.message
        });
      }
    }
    
    progressBar.complete('Package list updates completed');
    
    // Display summary
    const successful = results.filter(r => r.success).length;
    const failed = results.filter(r => !r.success).length;
    
    if (failed === 0) {
      StatusIndicator.success(`All ${successful} package managers updated successfully`);
    } else {
      StatusIndicator.warning(`${successful} succeeded, ${failed} failed`, {
        details: `Failed: ${results.filter(r => !r.success).map(r => r.manager).join(', ')}`
      });
    }
  }

  getAvailableManagers(): string[] {
    return this.availableManagers.map(m => m.name);
  }

  /**
   * Display package manager status with visual indicators
   */
  async displayStatus(): Promise<void> {
    await this.initialize();

    const packageManagerData: Record<string, boolean> = {};
    
    // Create status data for all package managers
    for (const manager of this.packageManagers) {
      packageManagerData[manager.name] = this.availableManagers.some(am => am.name === manager.name);
    }

    // Use SystemInfo formatter to display package managers
    const systemData = { package_managers: packageManagerData };
    const formatted = SystemInfo.format(systemData, { 
      sections: ['packages'], 
      compact: false, 
      showIcons: true 
    });
    
    console.log(formatted);
  }

  /**
   * Display installation progress for multiple packages
   */
  async installMultiplePackages(packages: string[]): Promise<Array<{ package: string; success: boolean; manager?: string; error?: string }>> {
    await this.initialize();

    if (this.availableManagers.length === 0) {
      StatusIndicator.error('No package managers available');
      return packages.map(pkg => ({ package: pkg, success: false, error: 'No package managers available' }));
    }

    StatusIndicator.info(`Installing ${packages.length} packages...`);
    
    const overallProgress = new ProgressBar({
      total: packages.length,
      message: 'Installing packages...',
      showPercentage: true,
      showNumbers: true
    });

    const results: Array<{ package: string; success: boolean; manager?: string; error?: string }> = [];

    for (let i = 0; i < packages.length; i++) {
      const packageName = packages[i];
      overallProgress.update(i, `Installing ${packageName}...`);
      
      const result = await this.installPackage(packageName);
      results.push({
        package: packageName,
        success: result.success,
        ...(result.manager && { manager: result.manager }),
        ...(result.error && { error: result.error })
      });
    }

    overallProgress.complete('Package installation completed');

    // Display summary
    const successful = results.filter(r => r.success).length;
    const failed = results.filter(r => !r.success).length;

    StatusIndicator.summary('Installation Summary', [
      { 
        label: `Successful installations`, 
        status: successful > 0 ? StatusType.SUCCESS : StatusType.INFO,
        value: successful.toString()
      },
      { 
        label: `Failed installations`, 
        status: failed > 0 ? StatusType.ERROR : StatusType.SUCCESS,
        value: failed.toString()
      }
    ]);

    if (failed > 0) {
      const failedPackages = results.filter(r => !r.success);
      StatusIndicator.error('Failed packages:', {
        details: failedPackages.map(r => `${r.package}: ${r.error}`).join('\n')
      });
    }

    return results;
  }

  private async commandExists(command: string): Promise<boolean> {
    try {
      await execAsync(`which ${command}`, { timeout: 5000 });
      return true;
    } catch {
      return false;
    }
  }

  private getPreferredOrder(): PackageManager[] {
    // Get preference from environment or use default order based on OS
    const isMacOS = process.platform === 'darwin';
    const defaultOrder = isMacOS 
      ? ['brew', 'brew-cask', 'mas', 'port', 'npm', 'pip', 'cargo']
      : ['apt', 'pacman', 'dnf', 'yum', 'zypper', 'snap', 'flatpak', 'npm', 'pip', 'cargo'];
    
    const preference = process.env.PACKAGE_MANAGER_PREFERENCE?.split(',') || defaultOrder;
    
    const ordered: PackageManager[] = [];
    
    // Add managers in preferred order
    for (const prefName of preference) {
      const manager = this.availableManagers.find(m => m.name === prefName.trim());
      if (manager) {
        ordered.push(manager);
      }
    }
    
    // Add any remaining managers
    for (const manager of this.availableManagers) {
      if (!ordered.includes(manager)) {
        ordered.push(manager);
      }
    }
    
    return ordered;
  }

  private extractVersion(output: string, managerName: string): string | undefined {
    // Simplified version extraction - would need specific logic for each manager
    const versionPatterns = [
      /version[:\s]+([0-9]+\.[0-9]+\.[0-9]+)/i,
      /([0-9]+\.[0-9]+\.[0-9]+)/,
      /v([0-9]+\.[0-9]+)/i
    ];

    for (const pattern of versionPatterns) {
      const match = output.match(pattern);
      if (match) {
        return match[1];
      }
    }

    return undefined;
  }
}