import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { Banner } from '../../../src/ui/components/Banner.js';
import { StatusIndicator, StatusType } from '../../../src/ui/components/StatusIndicator.js';
import { Table } from '../../../src/ui/components/Table.js';
import { ProgressBar } from '../../../src/ui/components/ProgressBar.js';
import { 
  getCapturedLogs, 
  mockConsoleLog, 
  restoreConsoleLog 
} from '../../setup.js';

describe('Visual Component Snapshots', () => {
  beforeEach(() => {
    mockConsoleLog();
    
    // Set consistent environment for snapshots
    Object.defineProperty(process.stdout, 'columns', { value: 80 });
    Object.defineProperty(process, 'platform', { value: 'linux' });
    process.env.TERM = 'xterm-256color';
    process.env.COLORTERM = 'truecolor';
    process.env.LANG = 'en_US.UTF-8';
    
    // Disable colors for consistent snapshots
    process.env.NO_COLOR = '1';
    process.env.FORCE_ASCII = 'true';
  });

  afterEach(() => {
    restoreConsoleLog();
    delete process.env.NO_COLOR;
    delete process.env.FORCE_ASCII;
  });

  describe('Banner Snapshots', () => {
    it('should match banner display snapshot', () => {
      Banner.display({
        showVersion: true,
        showTagline: true,
        showPlatform: true,
        compact: false
      });
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('banner-full-display');
    });

    it('should match compact banner snapshot', () => {
      Banner.displayCompact();
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('banner-compact-display');
    });

    it('should match minimal banner snapshot', () => {
      Banner.displayMinimal();
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('banner-minimal-display');
    });

    it('should match welcome banner snapshot', () => {
      Banner.welcome({
        showVersion: true,
        showTagline: true,
        compact: false
      });
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('banner-welcome-display');
    });

    it('should match startup banner snapshot', () => {
      Banner.startup('TestUser', {
        showVersion: true,
        showPlatform: true
      });
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('banner-startup-display');
    });

    it('should match error banner snapshot', () => {
      Banner.error('Critical system error occurred');
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('banner-error-display');
    });

    it('should match success banner snapshot', () => {
      Banner.success('Operation completed successfully');
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('banner-success-display');
    });

    it('should match info banner snapshot', () => {
      Banner.info('System Information', 'Current system status and configuration details');
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('banner-info-display');
    });

    it('should match separator snapshot', () => {
      Banner.separator('SECTION');
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('banner-separator-display');
    });

    it('should match footer snapshot', () => {
      Banner.footer();
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('banner-footer-display');
    });
  });

  describe('StatusIndicator Snapshots', () => {
    it('should match success status snapshot', () => {
      StatusIndicator.success('Operation completed successfully');
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('status-success');
    });

    it('should match error status snapshot', () => {
      StatusIndicator.error('An error occurred during processing');
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('status-error');
    });

    it('should match warning status snapshot', () => {
      StatusIndicator.warning('This is a warning message');
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('status-warning');
    });

    it('should match info status snapshot', () => {
      StatusIndicator.info('Information about the current process');
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('status-info');
    });

    it('should match loading status snapshot', () => {
      StatusIndicator.loading('Loading data from server...');
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('status-loading');
    });

    it('should match question status snapshot', () => {
      StatusIndicator.question('Are you sure you want to continue?');
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('status-question');
    });

    it('should match status with options snapshot', () => {
      StatusIndicator.success('Success with options', {
        prefix: 'TEST',
        indent: 2,
        timestamp: false, // Disable timestamp for consistent snapshots
        details: 'Additional details about the operation'
      });
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('status-with-options');
    });

    it('should match step status snapshot', () => {
      StatusIndicator.step(3, 5, 'Processing step 3 of 5', StatusType.INFO);
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('status-step');
    });

    it('should match status list snapshot', () => {
      const items = [
        { message: 'First operation completed', status: StatusType.SUCCESS },
        { message: 'Second operation has warnings', status: StatusType.WARNING, details: 'Minor issues detected' },
        { message: 'Third operation failed', status: StatusType.ERROR },
        { message: 'Fourth operation in progress', status: StatusType.LOADING }
      ];
      
      StatusIndicator.list(items);
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('status-list');
    });

    it('should match status summary snapshot', () => {
      const items = [
        { label: 'Files processed', status: StatusType.SUCCESS, value: '1,250' },
        { label: 'Warnings generated', status: StatusType.WARNING, value: '15' },
        { label: 'Errors encountered', status: StatusType.ERROR, value: '3' },
        { label: 'Processing time', status: StatusType.INFO, value: '2m 34s' }
      ];
      
      StatusIndicator.summary('Processing Summary', items);
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('status-summary');
    });

    it('should match divider snapshot', () => {
      StatusIndicator.divider('PROCESSING RESULTS');
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('status-divider');
    });
  });

  describe('Table Snapshots', () => {
    it('should match basic table snapshot', () => {
      const table = new Table({
        title: 'Sample Data Table',
        showHeaders: true,
        showBorders: true
      });
      
      table.addColumns([
        { key: 'id', title: 'ID', align: 'center' },
        { key: 'name', title: 'Name', align: 'left' },
        { key: 'status', title: 'Status', align: 'center' },
        { key: 'score', title: 'Score', align: 'right' }
      ]);
      
      table.setData([
        { id: 1, name: 'Alice Johnson', status: 'Active', score: 95 },
        { id: 2, name: 'Bob Smith', status: 'Inactive', score: 87 },
        { id: 3, name: 'Charlie Brown', status: 'Active', score: 92 },
        { id: 4, name: 'Diana Prince', status: 'Pending', score: 88 }
      ]);
      
      const output = table.render();
      expect(output).toMatchSnapshot('table-basic');
    });

    it('should match table without borders snapshot', () => {
      const table = new Table({
        title: 'Borderless Table',
        showHeaders: true,
        showBorders: false
      });
      
      table.addColumns([
        { key: 'item', title: 'Item', align: 'left' },
        { key: 'quantity', title: 'Qty', align: 'right' },
        { key: 'price', title: 'Price', align: 'right' }
      ]);
      
      table.setData([
        { item: 'Widget A', quantity: 10, price: '$19.99' },
        { item: 'Widget B', quantity: 25, price: '$29.99' },
        { item: 'Widget C', quantity: 5, price: '$39.99' }
      ]);
      
      const output = table.render();
      expect(output).toMatchSnapshot('table-no-borders');
    });

    it('should match table with row numbers snapshot', () => {
      const table = new Table({
        title: 'Numbered Rows Table',
        showHeaders: true,
        showBorders: true,
        showRowNumbers: true
      });
      
      table.addColumns([
        { key: 'task', title: 'Task', align: 'left' },
        { key: 'priority', title: 'Priority', align: 'center' },
        { key: 'assignee', title: 'Assignee', align: 'left' }
      ]);
      
      table.setData([
        { task: 'Implement user authentication', priority: 'High', assignee: 'Alice' },
        { task: 'Design database schema', priority: 'Medium', assignee: 'Bob' },
        { task: 'Write unit tests', priority: 'Low', assignee: 'Charlie' },
        { task: 'Deploy to staging', priority: 'High', assignee: 'Diana' }
      ]);
      
      const output = table.render();
      expect(output).toMatchSnapshot('table-with-row-numbers');
    });

    it('should match table with alternate row colors snapshot', () => {
      const table = new Table({
        title: 'Alternating Colors Table',
        showHeaders: true,
        showBorders: true,
        alternateRowColors: true
      });
      
      table.addColumns([
        { key: 'date', title: 'Date', align: 'left' },
        { key: 'event', title: 'Event', align: 'left' },
        { key: 'status', title: 'Status', align: 'center' }
      ]);
      
      table.setData([
        { date: '2023-01-01', event: 'System startup', status: 'Success' },
        { date: '2023-01-02', event: 'Database backup', status: 'Success' },
        { date: '2023-01-03', event: 'Security scan', status: 'Warning' },
        { date: '2023-01-04', event: 'Update deployment', status: 'Success' },
        { date: '2023-01-05', event: 'Performance test', status: 'Failed' }
      ]);
      
      const output = table.render();
      expect(output).toMatchSnapshot('table-alternate-colors');
    });

    it('should match compact table snapshot', () => {
      const table = new Table({
        compact: true,
        showHeaders: false,
        showBorders: false
      });
      
      table.addColumn({ key: 'item', title: 'Item', align: 'left' });
      
      table.setData([
        { item: 'First item in compact list' },
        { item: 'Second item in compact list' },
        { item: 'Third item in compact list' }
      ]);
      
      const output = table.render();
      expect(output).toMatchSnapshot('table-compact');
    });

    it('should match static simple table snapshot', () => {
      const data = [
        { name: 'John Doe', age: 30, city: 'New York' },
        { name: 'Jane Smith', age: 25, city: 'Los Angeles' },
        { name: 'Mike Johnson', age: 35, city: 'Chicago' }
      ];
      
      const output = Table.simple(data);
      expect(output).toMatchSnapshot('table-static-simple');
    });

    it('should match static key-value table snapshot', () => {
      const data = {
        applicationName: 'AP CLI',
        version: '0.1.0',
        platform: 'Linux x64',
        nodeVersion: 'v18.17.0',
        memoryUsage: '45.2 MB',
        uptime: '2h 15m 30s'
      };
      
      const output = Table.keyValue(data, 'System Information');
      expect(output).toMatchSnapshot('table-key-value');
    });

    it('should match static list table snapshot', () => {
      const items = [
        'Initialize application',
        'Load configuration files',
        'Connect to database',
        'Start HTTP server',
        'Register signal handlers',
        'Application ready'
      ];
      
      const output = Table.list(items, 'Startup Sequence', true);
      expect(output).toMatchSnapshot('table-list-numbered');
    });

    it('should match empty table snapshot', () => {
      const table = new Table({ title: 'Empty Table' });
      table.addColumn({ key: 'data', title: 'Data' });
      
      const output = table.render();
      expect(output).toMatchSnapshot('table-empty');
    });

    it('should match no columns table snapshot', () => {
      const table = new Table();
      table.addRow({ data: 'Some data' });
      
      const output = table.render();
      expect(output).toMatchSnapshot('table-no-columns');
    });
  });

  describe('ProgressBar Snapshots', () => {
    it('should match progress bar at different stages', () => {
      const outputs: string[] = [];
      
      // Capture progress at different stages
      const stages = [0, 25, 50, 75, 100];
      
      stages.forEach(progress => {
        const bar = new ProgressBar({
          total: 100,
          showPercentage: true,
          showNumbers: true,
          width: 40,
          message: `Processing... ${progress}%`
        });
        
        // Mock stdout.write to capture output
        let capturedOutput = '';
        const originalWrite = process.stdout.write;
        process.stdout.write = ((chunk: any) => {
          capturedOutput += chunk.toString();
          return true;
        }) as any;
        
        bar.update(progress);
        
        // Restore stdout.write
        process.stdout.write = originalWrite;
        
        outputs.push(capturedOutput);
      });
      
      expect(outputs).toMatchSnapshot('progress-bar-stages');
    });

    it('should match different progress bar styles', () => {
      const styles = ['bar', 'dots', 'blocks'] as const;
      const outputs: string[] = [];
      
      styles.forEach(style => {
        const bar = new ProgressBar({
          total: 10,
          style,
          width: 20,
          showPercentage: true
        });
        
        let capturedOutput = '';
        const originalWrite = process.stdout.write;
        process.stdout.write = ((chunk: any) => {
          capturedOutput += chunk.toString();
          return true;
        }) as any;
        
        bar.update(7); // 70% progress
        
        process.stdout.write = originalWrite;
        outputs.push(capturedOutput);
      });
      
      expect(outputs).toMatchSnapshot('progress-bar-styles');
    });

    it('should match progress bar with ETA', () => {
      const bar = new ProgressBar({
        total: 100,
        showPercentage: true,
        showNumbers: true,
        showEta: true,
        width: 30,
        message: 'Processing with ETA'
      });
      
      let capturedOutput = '';
      const originalWrite = process.stdout.write;
      process.stdout.write = ((chunk: any) => {
        capturedOutput += chunk.toString();
        return true;
      }) as any;
      
      // Simulate progress over time
      bar.update(60);
      
      process.stdout.write = originalWrite;
      
      // Remove dynamic ETA part for consistent snapshot
      const cleanOutput = capturedOutput.replace(/ETA: \d+[smh\s]+/, 'ETA: [TIME]');
      expect(cleanOutput).toMatchSnapshot('progress-bar-with-eta');
    });

    it('should match completed progress bar', () => {
      const bar = new ProgressBar({
        total: 50,
        showPercentage: true,
        message: 'Task completed'
      });
      
      let capturedOutput = '';
      const originalWrite = process.stdout.write;
      process.stdout.write = ((chunk: any) => {
        capturedOutput += chunk.toString();
        return true;
      }) as any;
      
      bar.complete('All done!');
      
      process.stdout.write = originalWrite;
      
      expect(capturedOutput).toMatchSnapshot('progress-bar-completed');
    });

    it('should match failed progress bar', () => {
      const bar = new ProgressBar({
        total: 50,
        showPercentage: true,
        message: 'Task processing'
      });
      
      let capturedOutput = '';
      const originalWrite = process.stdout.write;
      process.stdout.write = ((chunk: any) => {
        capturedOutput += chunk.toString();
        return true;
      }) as any;
      
      bar.fail('Operation failed');
      
      process.stdout.write = originalWrite;
      
      expect(capturedOutput).toMatchSnapshot('progress-bar-failed');
    });
  });

  describe('Complex Layout Snapshots', () => {
    it('should match complex dashboard layout', () => {
      // Create a complex layout combining multiple components
      Banner.display({
        showVersion: true,
        showTagline: false,
        compact: true
      });
      
      StatusIndicator.divider('SYSTEM STATUS');
      
      const systemData = [
        { component: 'Database', status: 'Connected', uptime: '99.9%' },
        { component: 'API Server', status: 'Running', uptime: '99.8%' },
        { component: 'Cache', status: 'Active', uptime: '100%' },
        { component: 'Queue', status: 'Processing', uptime: '99.7%' }
      ];
      
      console.log(Table.simple(systemData));
      
      StatusIndicator.divider('RECENT ACTIVITY');
      
      const activities = [
        { message: 'User authentication successful', status: StatusType.SUCCESS },
        { message: 'Database backup completed', status: StatusType.SUCCESS },
        { message: 'High memory usage detected', status: StatusType.WARNING },
        { message: 'Processing queue items', status: StatusType.LOADING }
      ];
      
      StatusIndicator.list(activities);
      
      Banner.footer();
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('complex-dashboard-layout');
    });

    it('should match error report layout', () => {
      Banner.error('System Error Detected');
      
      StatusIndicator.divider('ERROR DETAILS');
      
      const errorDetails = {
        errorCode: 'ERR_DB_CONNECTION',
        timestamp: '2023-01-01T12:00:00Z',
        severity: 'Critical',
        affectedUsers: '1,250',
        estimatedDowntime: '15 minutes'
      };
      
      console.log(Table.keyValue(errorDetails, 'Error Information'));
      
      StatusIndicator.divider('RECOVERY STEPS');
      
      const recoverySteps = [
        'Restart database service',
        'Verify connection pool',
        'Check network connectivity',
        'Validate configuration',
        'Monitor system health'
      ];
      
      console.log(Table.list(recoverySteps, 'Recovery Checklist', true));
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('error-report-layout');
    });

    it('should match installation progress layout', () => {
      Banner.welcome({ compact: true });
      
      StatusIndicator.divider('INSTALLATION PROGRESS');
      
      const installSteps = [
        { message: 'Downloading packages', status: StatusType.SUCCESS },
        { message: 'Verifying checksums', status: StatusType.SUCCESS },
        { message: 'Installing dependencies', status: StatusType.LOADING },
        { message: 'Configuring services', status: StatusType.INFO },
        { message: 'Running tests', status: StatusType.INFO }
      ];
      
      StatusIndicator.list(installSteps);
      
      StatusIndicator.divider('SYSTEM REQUIREMENTS');
      
      const requirements = [
        { requirement: 'Node.js >= 18.0.0', status: 'Satisfied', version: 'v18.17.0' },
        { requirement: 'Memory >= 4GB', status: 'Satisfied', version: '8GB' },
        { requirement: 'Disk Space >= 1GB', status: 'Satisfied', version: '2.5GB free' }
      ];
      
      console.log(Table.simple(requirements));
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('installation-progress-layout');
    });
  });

  describe('Responsive Layout Snapshots', () => {
    it('should match narrow terminal layout', () => {
      Object.defineProperty(process.stdout, 'columns', { value: 40 });
      
      Banner.display({ compact: true });
      
      const data = [
        { name: 'Item 1', value: 100 },
        { name: 'Item 2', value: 200 }
      ];
      
      console.log(Table.simple(data));
      
      StatusIndicator.success('Narrow layout test');
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('narrow-terminal-layout');
    });

    it('should match wide terminal layout', () => {
      Object.defineProperty(process.stdout, 'columns', { value: 120 });
      
      Banner.display({ compact: false });
      
      const data = [
        { id: 1, name: 'Long item name here', description: 'Detailed description of the item', status: 'Active', priority: 'High' },
        { id: 2, name: 'Another long item name', description: 'Another detailed description', status: 'Inactive', priority: 'Medium' }
      ];
      
      console.log(Table.simple(data));
      
      StatusIndicator.success('Wide layout test with more detailed information');
      
      const output = getCapturedLogs().join('\n');
      expect(output).toMatchSnapshot('wide-terminal-layout');
    });
  });
});