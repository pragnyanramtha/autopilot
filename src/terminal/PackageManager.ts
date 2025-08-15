import { exec } from 'child_process';
import { promisify } from 'util';

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

    console.log('🔍 Detecting available package managers...');
    
    for (const manager of this.packageManagers) {
      if (await manager.isAvailable()) {
        this.availableManagers.push(manager);
        console.log(`✅ Found: ${manager.name}`);
      }
    }

    if (this.availableManagers.length === 0) {
      console.warn('⚠️  No package managers detected!');
    } else {
      console.log(`📦 Available package managers: ${this.availableManagers.map(m => m.name).join(', ')}`);
    }

    this.initialized = true;
  }

  async installPackage(packageName: string): Promise<{ success: boolean; manager?: string; output?: string; error?: string }> {
    await this.initialize();

    if (this.availableManagers.length === 0) {
      return { success: false, error: 'No package managers available' };
    }

    // Try each package manager in order of preference
    const preferredOrder = this.getPreferredOrder();
    
    for (const manager of preferredOrder) {
      try {
        console.log(`📦 Trying to install ${packageName} with ${manager.name}...`);
        
        const installCmd = manager.installCommand(packageName);
        const { stdout, stderr } = await execAsync(installCmd, { timeout: 300000 });
        
        console.log(`✅ Successfully installed ${packageName} with ${manager.name}`);
        return { 
          success: true, 
          manager: manager.name, 
          output: stdout 
        };
        
      } catch (error: any) {
        console.log(`❌ Failed to install ${packageName} with ${manager.name}: ${error.message}`);
        
        // If this is the last manager, return the error
        if (manager === preferredOrder[preferredOrder.length - 1]) {
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
          return { 
            installed: true, 
            manager: manager.name,
            version: this.extractVersion(stdout, manager.name)
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

    console.log('🔄 Updating package lists...');
    
    for (const manager of this.availableManagers) {
      try {
        console.log(`   Updating ${manager.name}...`);
        await execAsync(manager.updateCommand, { timeout: 120000 });
        console.log(`   ✅ ${manager.name} updated`);
      } catch (error) {
        console.log(`   ❌ Failed to update ${manager.name}`);
      }
    }
  }

  getAvailableManagers(): string[] {
    return this.availableManagers.map(m => m.name);
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
    // Get preference from environment or use default order
    const preference = process.env.PACKAGE_MANAGER_PREFERENCE?.split(',') || ['apt', 'snap', 'flatpak', 'npm', 'pip', 'cargo'];
    
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