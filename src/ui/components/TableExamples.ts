import { Table, formatters } from './Table.js';
import { colors } from '../utils/Colors.js';

// Example usage and demonstrations of the Table component

export class TableExamples {
  
  // Example 1: System Information Table
  static systemInfo(): string {
    const table = new Table({
      title: 'System Information',
      showBorders: true,
      alternateRowColors: true
    });

    table.addColumns([
      { key: 'property', title: 'Property', align: 'left', width: 20 },
      { key: 'value', title: 'Value', align: 'left' },
      { key: 'status', title: 'Status', align: 'center', formatter: formatters.status }
    ]);

    table.addRows([
      { property: 'Operating System', value: 'Ubuntu 22.04 LTS', status: 'Active' },
      { property: 'Architecture', value: 'x86_64', status: 'Supported' },
      { property: 'Memory', value: '16 GB', status: 'Available' },
      { property: 'Disk Space', value: '512 GB SSD', status: 'Healthy' },
      { property: 'Network', value: 'Connected', status: 'Active' }
    ]);

    return table.render();
  }

  // Example 2: Package Manager Status
  static packageManagers(): string {
    const table = new Table({
      title: 'Package Managers',
      showBorders: true,
      showRowNumbers: true
    });

    table.addColumns([
      { key: 'name', title: 'Package Manager', align: 'left' },
      { key: 'available', title: 'Available', align: 'center', formatter: formatters.boolean },
      { key: 'version', title: 'Version', align: 'left' },
      { key: 'packages', title: 'Packages', align: 'right', formatter: formatters.number }
    ]);

    table.addRows([
      { name: 'apt', available: true, version: '2.4.8', packages: 73542 },
      { name: 'snap', available: true, version: '2.58', packages: 8234 },
      { name: 'flatpak', available: false, version: 'N/A', packages: 0 },
      { name: 'npm', available: true, version: '9.5.1', packages: 2156789 },
      { name: 'pip', available: true, version: '23.0.1', packages: 421567 }
    ]);

    return table.render();
  }

  // Example 3: File Listing
  static fileList(): string {
    const table = new Table({
      title: 'Project Files',
      compact: true,
      alternateRowColors: true
    });

    table.addColumns([
      { key: 'name', title: 'Name', align: 'left', formatter: formatters.path },
      { key: 'size', title: 'Size', align: 'right', formatter: formatters.fileSize },
      { key: 'modified', title: 'Modified', align: 'left', formatter: formatters.date },
      { key: 'type', title: 'Type', align: 'center' }
    ]);

    table.addRows([
      { name: 'package.json', size: 2048, modified: new Date('2024-01-15'), type: 'JSON' },
      { name: 'README.md', size: 15360, modified: new Date('2024-01-14'), type: 'Markdown' },
      { name: 'src/', size: 0, modified: new Date('2024-01-16'), type: 'Directory' },
      { name: 'node_modules/', size: 157286400, modified: new Date('2024-01-13'), type: 'Directory' },
      { name: '.gitignore', size: 512, modified: new Date('2024-01-10'), type: 'Text' }
    ]);

    return table.render();
  }

  // Example 4: Command Execution Results
  static commandResults(): string {
    const table = new Table({
      title: 'Command Execution Results',
      showBorders: false,
      showRowNumbers: true
    });

    table.addColumns([
      { key: 'command', title: 'Command', align: 'left', formatter: formatters.code },
      { key: 'exitCode', title: 'Exit Code', align: 'center' },
      { key: 'duration', title: 'Duration (ms)', align: 'right', formatter: formatters.number },
      { key: 'status', title: 'Status', align: 'center', formatter: formatters.status }
    ]);

    table.addRows([
      { command: 'npm install', exitCode: 0, duration: 15420, status: 'Success' },
      { command: 'npm test', exitCode: 0, duration: 3250, status: 'Success' },
      { command: 'npm run build', exitCode: 1, duration: 890, status: 'Failed' },
      { command: 'git status', exitCode: 0, duration: 120, status: 'Success' }
    ]);

    return table.render();
  }

  // Example 5: Network Status
  static networkStatus(): string {
    const table = new Table({
      title: 'Network Interfaces',
      alternateRowColors: true
    });

    table.addColumns([
      { key: 'interface', title: 'Interface', align: 'left' },
      { key: 'ip', title: 'IP Address', align: 'left' },
      { key: 'status', title: 'Status', align: 'center', formatter: formatters.status },
      { key: 'speed', title: 'Speed', align: 'right' },
      { key: 'usage', title: 'Usage', align: 'right', formatter: formatters.percentage }
    ]);

    table.addRows([
      { interface: 'eth0', ip: '192.168.1.100', status: 'Active', speed: '1 Gbps', usage: 0.15 },
      { interface: 'wlan0', ip: '192.168.1.101', status: 'Active', speed: '300 Mbps', usage: 0.45 },
      { interface: 'lo', ip: '127.0.0.1', status: 'Active', speed: 'N/A', usage: 0.01 }
    ]);

    return table.render();
  }

  // Example 6: Simple Key-Value Display
  static keyValueExample(): string {
    const data = {
      'API Key': colors.success('Configured'),
      'Profile': colors.info('Initialized'),
      'Theme': 'Auto',
      'Terminal': 'xterm-256color',
      'Shell': '/bin/bash',
      'Package Manager': 'apt'
    };

    return Table.keyValue(data, 'Configuration Status');
  }

  // Example 7: Simple List
  static simpleList(): string {
    const items = [
      'Install and configure development environment',
      'Set up package managers and dependencies',
      'Initialize user profile and preferences',
      'Configure AI service and API keys',
      'Test system integration and functionality'
    ];

    return Table.list(items, 'Setup Tasks', true);
  }

  // Example 8: Minimal Table (no borders)
  static minimalTable(): string {
    const data = [
      { name: 'Docker', status: 'Running', port: 2376 },
      { name: 'Nginx', status: 'Stopped', port: 80 },
      { name: 'MySQL', status: 'Running', port: 3306 },
      { name: 'Redis', status: 'Running', port: 6379 }
    ];

    return Table.simple(data);
  }

  // Example 9: Sortable Table
  static sortableTable(): string {
    const table = new Table({
      title: 'Installed Packages (sorted by size)',
      sortBy: 'size',
      sortDirection: 'desc',
      alternateRowColors: true
    });

    table.addColumns([
      { key: 'name', title: 'Package', align: 'left', sortable: true },
      { key: 'version', title: 'Version', align: 'left', sortable: true },
      { key: 'size', title: 'Size', align: 'right', formatter: formatters.fileSize, sortable: true },
      { key: 'installed', title: 'Installed', align: 'left', formatter: formatters.date, sortable: true }
    ]);

    table.addRows([
      { name: 'nodejs', version: '18.17.0', size: 45678912, installed: new Date('2024-01-10') },
      { name: 'git', version: '2.34.1', size: 12345678, installed: new Date('2024-01-08') },
      { name: 'docker', version: '24.0.5', size: 156789012, installed: new Date('2024-01-12') },
      { name: 'vim', version: '8.2.4919', size: 3456789, installed: new Date('2024-01-05') }
    ]);

    return table.render();
  }

  // Demonstration method that shows all examples
  static showAllExamples(): void {
    console.log(colors.primaryBold('Table Component Examples'));
    console.log(colors.muted('=' .repeat(50)));
    console.log();

    console.log(this.systemInfo());
    console.log('\n');

    console.log(this.packageManagers());
    console.log('\n');

    console.log(this.fileList());
    console.log('\n');

    console.log(this.commandResults());
    console.log('\n');

    console.log(this.networkStatus());
    console.log('\n');

    console.log(this.keyValueExample());
    console.log('\n');

    console.log(this.simpleList());
    console.log('\n');

    console.log(this.minimalTable());
    console.log('\n');

    console.log(this.sortableTable());
  }
}

// Export for easy testing
export default TableExamples;