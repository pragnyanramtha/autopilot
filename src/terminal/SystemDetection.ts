import { exec } from 'child_process';
import { promisify } from 'util';
import * as path from 'path';
import { StatusIndicator, StatusType } from '../ui/components/StatusIndicator.js';
import { ProgressBar, Spinner, MultiStepProgress } from '../ui/components/ProgressBar.js';
import { SystemInfo, SystemData } from '../ui/formatters/SystemInfo.js';
import { ErrorDisplay } from '../ui/formatters/ErrorDisplay.js';
import { colors } from '../ui/utils/Colors.js';
import { symbols } from '../ui/utils/Symbols.js';

const execAsync = promisify(exec);

export interface DetectionOptions {
  verbose?: boolean;
  showProgress?: boolean;
  sections?: ('system' | 'hardware' | 'os' | 'packages' | 'tools' | 'network')[];
}

export class SystemDetection {
  private systemData: SystemData = {};
  private isDetected: boolean = false;

  /**
   * Run comprehensive system detection with visual progress
   */
  async detect(options: DetectionOptions = {}): Promise<SystemData> {
    const {
      verbose = false,
      showProgress = true,
      sections = ['system', 'hardware', 'os', 'packages', 'tools', 'network']
    } = options;

    if (showProgress) {
      StatusIndicator.info('Starting system detection...');
    }

    const steps = [
      'Detecting system information',
      'Gathering hardware details',
      'Checking operating system',
      'Scanning package managers',
      'Finding development tools',
      'Testing network connectivity'
    ];

    const progress = new MultiStepProgress(steps);

    try {
      // Step 1: Basic system information
      if (sections.includes('system')) {
        if (showProgress) progress.nextStep('Detecting system information...');
        await this.detectSystemInfo(verbose);
        if (showProgress) progress.completeStep();
      }

      // Step 2: Hardware information
      if (sections.includes('hardware')) {
        if (showProgress) progress.nextStep('Gathering hardware details...');
        await this.detectHardwareInfo(verbose);
        if (showProgress) progress.completeStep();
      }

      // Step 3: Operating system details
      if (sections.includes('os')) {
        if (showProgress) progress.nextStep('Checking operating system...');
        await this.detectOSInfo(verbose);
        if (showProgress) progress.completeStep();
      }

      // Step 4: Package managers
      if (sections.includes('packages')) {
        if (showProgress) progress.nextStep('Scanning package managers...');
        await this.detectPackageManagers(verbose);
        if (showProgress) progress.completeStep();
      }

      // Step 5: Development tools
      if (sections.includes('tools')) {
        if (showProgress) progress.nextStep('Finding development tools...');
        await this.detectDevelopmentTools(verbose);
        if (showProgress) progress.completeStep();
      }

      // Step 6: Network connectivity
      if (sections.includes('network')) {
        if (showProgress) progress.nextStep('Testing network connectivity...');
        await this.detectNetworkInfo(verbose);
        if (showProgress) progress.completeStep();
      }

      if (showProgress) {
        progress.complete('System detection completed successfully');
        StatusIndicator.success('System detection completed');
      }

      this.isDetected = true;
      return this.systemData;

    } catch (error: any) {
      if (showProgress) {
        StatusIndicator.error('System detection failed', {
          details: error.message
        });
      }

      ErrorDisplay.show(error, {
        title: 'System Detection Error',
        message: 'Failed to complete system detection',
        suggestions: [
          'Check if you have necessary permissions',
          'Verify system commands are available',
          'Try running with verbose mode for more details'
        ]
      });

      throw error;
    }
  }

  /**
   * Run system detection using the shell script
   */
  async detectWithScript(options: DetectionOptions = {}): Promise<SystemData> {
    const { verbose = false, showProgress = true } = options;

    const spinner = showProgress ? new Spinner('Running system detection script...') : null;
    
    try {
      if (spinner) spinner.start();

      const scriptPath = path.join(process.cwd(), 'scripts', 'detect-system.sh');
      const { stdout, stderr } = await execAsync(`bash "${scriptPath}"`, { timeout: 30000 });

      if (spinner) spinner.succeed('System detection script completed');

      try {
        this.systemData = JSON.parse(stdout);
        this.isDetected = true;

        if (verbose) {
          StatusIndicator.success('System data parsed successfully', {
            details: `Detected ${Object.keys(this.systemData).length} data sections`
          });
        }

        return this.systemData;

      } catch (parseError: any) {
        if (spinner) spinner.fail('Failed to parse system data');
        
        ErrorDisplay.show(parseError, {
          title: 'System Data Parse Error',
          message: 'Failed to parse system detection output',
          details: stderr || 'Invalid JSON output from detection script',
          suggestions: [
            'Check if the detection script is working correctly',
            'Verify all required system commands are available',
            'Try running the script manually to debug'
          ]
        });

        throw parseError;
      }

    } catch (error: any) {
      if (spinner) spinner.fail('System detection script failed');

      ErrorDisplay.show(error, {
        title: 'System Detection Script Error',
        message: 'Failed to execute system detection script',
        suggestions: [
          'Check if bash is available',
          'Verify the detection script exists and is executable',
          'Check file permissions on the scripts directory'
        ]
      });

      throw error;
    }
  }

  /**
   * Display system information with visual formatting
   */
  displaySystemInfo(options: { compact?: boolean; sections?: string[] } = {}): void {
    if (!this.isDetected) {
      StatusIndicator.warning('System detection has not been run yet');
      return;
    }

    const formatted = SystemInfo.format(this.systemData, {
      compact: options.compact || false,
      sections: options.sections as any || ['system', 'hardware', 'os', 'packages', 'tools', 'network'],
      showIcons: true
    });

    console.log(formatted);
  }

  /**
   * Display a summary of system information
   */
  displaySummary(): void {
    if (!this.isDetected) {
      StatusIndicator.warning('System detection has not been run yet');
      return;
    }

    const summary = SystemInfo.formatSummary(this.systemData);
    StatusIndicator.info('System Summary');
    console.log(`  ${summary}`);
  }

  /**
   * Get system data
   */
  getSystemData(): SystemData {
    return this.systemData;
  }

  /**
   * Check if detection has been run
   */
  isSystemDetected(): boolean {
    return this.isDetected;
  }

  // Private detection methods

  private async detectSystemInfo(verbose: boolean): Promise<void> {
    try {
      const system: SystemData['system'] = {};

      // Get hostname
      try {
        const { stdout } = await execAsync('hostname', { timeout: 5000 });
        system.hostname = stdout.trim();
      } catch (error) {
        if (verbose) StatusIndicator.warning('Could not detect hostname');
      }

      // Get username
      system.username = process.env.USER || process.env.USERNAME || 'unknown';

      // Get directories
      system.home_directory = process.env.HOME || process.env.USERPROFILE || 'unknown';
      system.current_directory = process.cwd();

      // Get shell
      system.shell = process.env.SHELL || 'unknown';

      // Get terminal
      system.terminal = process.env.TERM || 'unknown';

      // Get OS type
      system.os_type = process.platform;

      this.systemData.system = system;

      if (verbose) {
        StatusIndicator.success('System information detected');
      }

    } catch (error: any) {
      if (verbose) {
        StatusIndicator.warning('Partial system detection failure', {
          details: error.message
        });
      }
    }
  }

  private async detectHardwareInfo(verbose: boolean): Promise<void> {
    try {
      const hardware: SystemData['hardware'] = {};

      // CPU cores
      try {
        const cores = require('os').cpus().length;
        hardware.cpu_cores = cores.toString();
      } catch (error) {
        if (verbose) StatusIndicator.warning('Could not detect CPU cores');
      }

      // Memory
      try {
        const totalMem = require('os').totalmem();
        const freeMem = require('os').freemem();
        hardware.memory_total = `${Math.round(totalMem / 1024 / 1024 / 1024)}GB`;
        hardware.memory_available = `${Math.round(freeMem / 1024 / 1024 / 1024)}GB`;
      } catch (error) {
        if (verbose) StatusIndicator.warning('Could not detect memory information');
      }

      this.systemData.hardware = hardware;

      if (verbose) {
        StatusIndicator.success('Hardware information detected');
      }

    } catch (error: any) {
      if (verbose) {
        StatusIndicator.warning('Hardware detection failure', {
          details: error.message
        });
      }
    }
  }

  private async detectOSInfo(verbose: boolean): Promise<void> {
    try {
      const os: SystemData['os'] = {};

      // Kernel information
      try {
        const { stdout: kernel } = await execAsync('uname -s', { timeout: 5000 });
        os.kernel = kernel.trim();

        const { stdout: version } = await execAsync('uname -r', { timeout: 5000 });
        os.kernel_version = version.trim();

        const { stdout: arch } = await execAsync('uname -m', { timeout: 5000 });
        os.architecture = arch.trim();
      } catch (error) {
        if (verbose) StatusIndicator.warning('Could not detect kernel information');
      }

      this.systemData.os = os;

      if (verbose) {
        StatusIndicator.success('OS information detected');
      }

    } catch (error: any) {
      if (verbose) {
        StatusIndicator.warning('OS detection failure', {
          details: error.message
        });
      }
    }
  }

  private async detectPackageManagers(verbose: boolean): Promise<void> {
    try {
      const packageManagers = [
        'brew', 'port', 'mas', 'apt', 'apt-get', 'yum', 'dnf', 
        'pacman', 'zypper', 'apk', 'snap', 'flatpak', 'npm', 
        'pip', 'pip3', 'cargo'
      ];

      const detected: Record<string, boolean> = {};

      for (const pm of packageManagers) {
        try {
          await execAsync(`which ${pm}`, { timeout: 2000 });
          detected[pm] = true;
          if (verbose) StatusIndicator.success(`Found ${pm}`);
        } catch (error) {
          detected[pm] = false;
        }
      }

      this.systemData.package_managers = detected;

      if (verbose) {
        const available = Object.values(detected).filter(Boolean).length;
        StatusIndicator.success(`Package managers detected: ${available}/${packageManagers.length}`);
      }

    } catch (error: any) {
      if (verbose) {
        StatusIndicator.warning('Package manager detection failure', {
          details: error.message
        });
      }
    }
  }

  private async detectDevelopmentTools(verbose: boolean): Promise<void> {
    try {
      const tools = [
        'git', 'node', 'python', 'python3', 'docker', 
        'code', 'vim', 'nano', 'emacs'
      ];

      const detected: Record<string, string | boolean> = {};

      for (const tool of tools) {
        try {
          const { stdout } = await execAsync(`${tool} --version`, { timeout: 5000 });
          detected[tool] = stdout.split('\n')[0];
          if (verbose) StatusIndicator.success(`Found ${tool}`);
        } catch (error) {
          detected[tool] = false;
        }
      }

      this.systemData.development_tools = detected;

      if (verbose) {
        const available = Object.values(detected).filter(v => v !== false).length;
        StatusIndicator.success(`Development tools detected: ${available}/${tools.length}`);
      }

    } catch (error: any) {
      if (verbose) {
        StatusIndicator.warning('Development tools detection failure', {
          details: error.message
        });
      }
    }
  }

  private async detectNetworkInfo(verbose: boolean): Promise<void> {
    try {
      const network: SystemData['network'] = {};

      // Test internet connectivity
      try {
        await execAsync('ping -c 1 8.8.8.8', { timeout: 10000 });
        network.internet_connection = true;
        if (verbose) StatusIndicator.success('Internet connection available');
      } catch (error) {
        network.internet_connection = false;
        if (verbose) StatusIndicator.warning('No internet connection detected');
      }

      this.systemData.network = network;

    } catch (error: any) {
      if (verbose) {
        StatusIndicator.warning('Network detection failure', {
          details: error.message
        });
      }
    }
  }
}