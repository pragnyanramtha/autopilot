import { colors } from '../utils/Colors.js';
import { symbols } from '../utils/Symbols.js';
import { Layout } from '../utils/Layout.js';
import { Table } from '../components/Table.js';

export interface SystemData {
  timestamp?: string;
  system?: {
    hostname?: string;
    username?: string;
    home_directory?: string;
    current_directory?: string;
    shell?: string;
    shell_version?: string;
    terminal?: string;
    os_type?: string;
  };
  os?: {
    kernel?: string;
    kernel_version?: string;
    architecture?: string;
    platform?: string;
    os_release?: {
      NAME?: string;
      VERSION?: string;
      ID?: string;
      PRETTY_NAME?: string;
    };
  };
  hardware?: {
    cpu_info?: string;
    cpu_cores?: string;
    memory_total?: string;
    memory_available?: string;
    disk_usage?: string;
  };
  package_managers?: Record<string, boolean>;
  development_tools?: Record<string, string | boolean>;
  network?: {
    hostname_fqdn?: string;
    ip_address?: string;
    internet_connection?: boolean;
  };
}

export interface SystemInfoOptions {
  sections?: ('system' | 'hardware' | 'os' | 'packages' | 'tools' | 'network')[];
  compact?: boolean;
  showIcons?: boolean;
}

export class SystemInfo {
  /**
   * Format complete system information display
   */
  static format(data: SystemData, options: SystemInfoOptions = {}): string {
    const {
      sections = ['system', 'hardware', 'os', 'packages', 'tools', 'network'],
      compact = false,
      showIcons = true
    } = options;

    const output: string[] = [];

    // Header
    if (!compact) {
      output.push(colors.bold('System Information'));
      output.push(Layout.separator('═', 50));
      output.push('');
    }

    // System Overview
    if (sections.includes('system') && data.system) {
      output.push(this.formatSystemOverview(data.system, { compact, showIcons }));
      if (!compact) output.push('');
    }

    // Hardware Information
    if (sections.includes('hardware') && data.hardware) {
      output.push(this.formatHardwareInfo(data.hardware, { compact, showIcons }));
      if (!compact) output.push('');
    }

    // Operating System
    if (sections.includes('os') && data.os) {
      output.push(this.formatOSInfo(data.os, { compact, showIcons }));
      if (!compact) output.push('');
    }

    // Package Managers
    if (sections.includes('packages') && data.package_managers) {
      output.push(this.formatPackageManagers(data.package_managers, { compact, showIcons }));
      if (!compact) output.push('');
    }

    // Development Tools
    if (sections.includes('tools') && data.development_tools) {
      output.push(this.formatDevelopmentTools(data.development_tools, { compact, showIcons }));
      if (!compact) output.push('');
    }

    // Network Information
    if (sections.includes('network') && data.network) {
      output.push(this.formatNetworkInfo(data.network, { compact, showIcons }));
    }

    return output.join('\n');
  }

  /**
   * Format system overview section
   */
  private static formatSystemOverview(system: SystemData['system'], options: { compact?: boolean; showIcons?: boolean }): string {
    const { compact, showIcons } = options;
    const lines: string[] = [];

    if (!compact) {
      const icon = showIcons ? '🖥️  ' : '';
      lines.push(colors.primary(`${icon}System Overview`));
      lines.push(Layout.separator('─', 30));
    }

    const table = new Table([
      { header: 'Property', key: 'property', width: 15, align: 'left' },
      { header: 'Value', key: 'value', width: 35, align: 'left' }
    ]);

    if (system?.hostname) {
      table.addRow({ property: 'Hostname', value: colors.info(system.hostname) });
    }
    if (system?.username) {
      table.addRow({ property: 'User', value: colors.success(system.username) });
    }
    if (system?.os_type) {
      table.addRow({ property: 'OS Type', value: colors.primary(system.os_type) });
    }
    if (system?.shell) {
      const shellName = system.shell.split('/').pop() || system.shell;
      table.addRow({ property: 'Shell', value: colors.info(shellName) });
    }
    if (system?.terminal) {
      table.addRow({ property: 'Terminal', value: colors.muted(system.terminal) });
    }

    lines.push(table.render());
    return lines.join('\n');
  }

  /**
   * Format hardware information section
   */
  private static formatHardwareInfo(hardware: SystemData['hardware'], options: { compact?: boolean; showIcons?: boolean }): string {
    const { compact, showIcons } = options;
    const lines: string[] = [];

    if (!compact) {
      const icon = showIcons ? '⚙️  ' : '';
      lines.push(colors.primary(`${icon}Hardware Information`));
      lines.push(Layout.separator('─', 30));
    }

    const table = new Table([
      { header: 'Component', key: 'component', width: 15, align: 'left' },
      { header: 'Details', key: 'details', width: 35, align: 'left' }
    ]);

    if (hardware?.cpu_info) {
      table.addRow({ 
        component: 'CPU', 
        value: colors.info(hardware.cpu_info.length > 40 ? hardware.cpu_info.substring(0, 37) + '...' : hardware.cpu_info)
      });
    }
    if (hardware?.cpu_cores) {
      table.addRow({ component: 'Cores', value: colors.warning(hardware.cpu_cores) });
    }
    if (hardware?.memory_total) {
      table.addRow({ component: 'Memory', value: colors.success(hardware.memory_total) });
    }
    if (hardware?.disk_usage) {
      table.addRow({ component: 'Disk Usage', value: colors.muted(hardware.disk_usage) });
    }

    lines.push(table.render());
    return lines.join('\n');
  }

  /**
   * Format operating system information
   */
  private static formatOSInfo(os: SystemData['os'], options: { compact?: boolean; showIcons?: boolean }): string {
    const { compact, showIcons } = options;
    const lines: string[] = [];

    if (!compact) {
      const icon = showIcons ? '💿 ' : '';
      lines.push(colors.primary(`${icon}Operating System`));
      lines.push(Layout.separator('─', 30));
    }

    const table = new Table([
      { header: 'Property', key: 'property', width: 15, align: 'left' },
      { header: 'Value', key: 'value', width: 35, align: 'left' }
    ]);

    if (os?.os_release?.PRETTY_NAME) {
      table.addRow({ property: 'Distribution', value: colors.primary(os.os_release.PRETTY_NAME) });
    }
    if (os?.kernel) {
      table.addRow({ property: 'Kernel', value: colors.info(os.kernel) });
    }
    if (os?.kernel_version) {
      table.addRow({ property: 'Version', value: colors.muted(os.kernel_version) });
    }
    if (os?.architecture) {
      table.addRow({ property: 'Architecture', value: colors.warning(os.architecture) });
    }

    lines.push(table.render());
    return lines.join('\n');
  }

  /**
   * Format package managers with status indicators
   */
  private static formatPackageManagers(packages: Record<string, boolean>, options: { compact?: boolean; showIcons?: boolean }): string {
    const { compact, showIcons } = options;
    const lines: string[] = [];

    if (!compact) {
      const icon = showIcons ? '📦 ' : '';
      lines.push(colors.primary(`${icon}Package Managers`));
      lines.push(Layout.separator('─', 30));
    }

    // Group package managers by type
    const systemPMs = ['apt', 'apt-get', 'yum', 'dnf', 'pacman', 'zypper', 'apk', 'brew', 'port'];
    const universalPMs = ['snap', 'flatpak'];
    const devPMs = ['npm', 'pip', 'pip3', 'cargo'];

    const available = Object.entries(packages).filter(([_, available]) => available);
    const unavailable = Object.entries(packages).filter(([_, available]) => !available);

    if (available.length > 0) {
      lines.push(colors.success(`${symbols.success} Available (${available.length}):`));
      available.forEach(([name]) => {
        const category = this.getPackageManagerCategory(name, systemPMs, universalPMs, devPMs);
        lines.push(Layout.indent(`${colors.success('●')} ${colors.bold(name)} ${colors.muted(`(${category})`)}`));
      });
    }

    if (!compact && unavailable.length > 0) {
      lines.push('');
      lines.push(colors.muted(`${symbols.info} Not Available (${unavailable.length}):`));
      unavailable.slice(0, 5).forEach(([name]) => {
        lines.push(Layout.indent(`${colors.muted('○')} ${colors.muted(name)}`));
      });
      if (unavailable.length > 5) {
        lines.push(Layout.indent(colors.muted(`... and ${unavailable.length - 5} more`)));
      }
    }

    return lines.join('\n');
  }

  /**
   * Get package manager category
   */
  private static getPackageManagerCategory(name: string, systemPMs: string[], universalPMs: string[], devPMs: string[]): string {
    if (systemPMs.includes(name)) return 'system';
    if (universalPMs.includes(name)) return 'universal';
    if (devPMs.includes(name)) return 'development';
    return 'other';
  }

  /**
   * Format development tools
   */
  private static formatDevelopmentTools(tools: Record<string, string | boolean>, options: { compact?: boolean; showIcons?: boolean }): string {
    const { compact, showIcons } = options;
    const lines: string[] = [];

    if (!compact) {
      const icon = showIcons ? '🛠️  ' : '';
      lines.push(colors.primary(`${icon}Development Tools`));
      lines.push(Layout.separator('─', 30));
    }

    const available = Object.entries(tools).filter(([_, value]) => value !== false);
    const unavailable = Object.entries(tools).filter(([_, value]) => value === false);

    if (available.length > 0) {
      lines.push(colors.success(`${symbols.success} Available (${available.length}):`));
      available.forEach(([name, version]) => {
        const versionStr = typeof version === 'string' ? version : '';
        const displayVersion = versionStr.length > 30 ? versionStr.substring(0, 27) + '...' : versionStr;
        lines.push(Layout.indent(`${colors.success('●')} ${colors.bold(name)} ${colors.muted(displayVersion)}`));
      });
    }

    if (!compact && unavailable.length > 0) {
      lines.push('');
      lines.push(colors.muted(`${symbols.info} Not Available (${unavailable.length}):`));
      unavailable.slice(0, 3).forEach(([name]) => {
        lines.push(Layout.indent(`${colors.muted('○')} ${colors.muted(name)}`));
      });
      if (unavailable.length > 3) {
        lines.push(Layout.indent(colors.muted(`... and ${unavailable.length - 3} more`)));
      }
    }

    return lines.join('\n');
  }

  /**
   * Format network information with status icons
   */
  private static formatNetworkInfo(network: SystemData['network'], options: { compact?: boolean; showIcons?: boolean }): string {
    const { compact, showIcons } = options;
    const lines: string[] = [];

    if (!compact) {
      const icon = showIcons ? '🌐 ' : '';
      lines.push(colors.primary(`${icon}Network Information`));
      lines.push(Layout.separator('─', 30));
    }

    const table = new Table([
      { header: 'Property', key: 'property', width: 15, align: 'left' },
      { header: 'Value', key: 'value', width: 35, align: 'left' }
    ]);

    if (network?.hostname_fqdn) {
      table.addRow({ property: 'FQDN', value: colors.info(network.hostname_fqdn) });
    }
    if (network?.ip_address) {
      table.addRow({ property: 'IP Address', value: colors.warning(network.ip_address) });
    }
    if (network?.internet_connection !== undefined) {
      const status = network.internet_connection;
      const statusIcon = status ? symbols.success : symbols.error;
      const statusColor = status ? colors.success : colors.error;
      const statusText = status ? 'Connected' : 'Disconnected';
      table.addRow({ 
        property: 'Internet', 
        value: `${statusColor(statusIcon)} ${statusColor(statusText)}`
      });
    }

    lines.push(table.render());
    return lines.join('\n');
  }

  /**
   * Create a summary view of system information
   */
  static formatSummary(data: SystemData): string {
    const lines: string[] = [];

    // System name and user
    if (data.system?.hostname && data.system?.username) {
      lines.push(`${colors.primary(data.system.hostname)} ${colors.muted('as')} ${colors.success(data.system.username)}`);
    }

    // OS and architecture
    if (data.os?.os_release?.PRETTY_NAME && data.os?.architecture) {
      lines.push(`${colors.info(data.os.os_release.PRETTY_NAME)} ${colors.muted(`(${data.os.architecture})`)}`);
    }

    // Hardware summary
    if (data.hardware?.cpu_cores && data.hardware?.memory_total) {
      lines.push(`${colors.warning(data.hardware.cpu_cores)} cores, ${colors.success(data.hardware.memory_total)} RAM`);
    }

    // Network status
    if (data.network?.internet_connection !== undefined) {
      const status = data.network.internet_connection;
      const statusIcon = status ? symbols.success : symbols.error;
      const statusColor = status ? colors.success : colors.error;
      lines.push(`${statusColor(statusIcon)} ${statusColor(status ? 'Online' : 'Offline')}`);
    }

    return lines.join(' • ');
  }
}