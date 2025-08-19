import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { Table, formatters } from '../../../src/ui/components/Table.js';
import { OptimizedTable } from '../../../src/ui/components/OptimizedTable.js';
import { 
  getCapturedLogs, 
  mockConsoleLog, 
  restoreConsoleLog 
} from '../../setup.js';

describe('Table Components', () => {
  beforeEach(() => {
    mockConsoleLog();
  });

  afterEach(() => {
    restoreConsoleLog();
  });

  describe('Basic Table', () => {
    it('should create empty table', () => {
      const table = new Table();
      expect(table).toBeDefined();
    });

    it('should create table with options', () => {
      const table = new Table({
        title: 'Test Table',
        showHeaders: true,
        showBorders: true,
        showRowNumbers: true,
        alternateRowColors: true
      });
      expect(table).toBeDefined();
    });

    it('should add columns', () => {
      const table = new Table();
      table.addColumn({
        key: 'name',
        title: 'Name',
        align: 'left'
      });
      table.addColumn({
        key: 'age',
        title: 'Age',
        align: 'right'
      });
      
      expect(table).toBeDefined();
    });

    it('should add multiple columns at once', () => {
      const table = new Table();
      table.addColumns([
        { key: 'id', title: 'ID', align: 'center' },
        { key: 'name', title: 'Name', align: 'left' },
        { key: 'status', title: 'Status', align: 'center' }
      ]);
      
      expect(table).toBeDefined();
    });

    it('should add rows', () => {
      const table = new Table();
      table.addColumn({ key: 'name', title: 'Name' });
      table.addColumn({ key: 'value', title: 'Value' });
      
      table.addRow({ name: 'Test', value: 123 });
      table.addRow({ name: 'Another', value: 456 });
      
      expect(table).toBeDefined();
    });

    it('should add multiple rows at once', () => {
      const table = new Table();
      table.addColumn({ key: 'name', title: 'Name' });
      table.addColumn({ key: 'value', title: 'Value' });
      
      table.addRows([
        { name: 'Row 1', value: 100 },
        { name: 'Row 2', value: 200 },
        { name: 'Row 3', value: 300 }
      ]);
      
      expect(table).toBeDefined();
    });

    it('should set data', () => {
      const table = new Table();
      table.addColumn({ key: 'name', title: 'Name' });
      table.addColumn({ key: 'value', title: 'Value' });
      
      table.setData([
        { name: 'Data 1', value: 'A' },
        { name: 'Data 2', value: 'B' }
      ]);
      
      expect(table).toBeDefined();
    });

    it('should render table with data', () => {
      const table = new Table({ title: 'Sample Table' });
      table.addColumns([
        { key: 'name', title: 'Name', align: 'left' },
        { key: 'age', title: 'Age', align: 'right' },
        { key: 'city', title: 'City', align: 'center' }
      ]);
      
      table.setData([
        { name: 'Alice', age: 30, city: 'New York' },
        { name: 'Bob', age: 25, city: 'Los Angeles' },
        { name: 'Charlie', age: 35, city: 'Chicago' }
      ]);
      
      const output = table.render();
      expect(output).toContain('Sample Table');
      expect(output).toContain('Alice');
      expect(output).toContain('Bob');
      expect(output).toContain('Charlie');
    });

    it('should render table without borders', () => {
      const table = new Table({ showBorders: false });
      table.addColumn({ key: 'item', title: 'Item' });
      table.addRow({ item: 'Test item' });
      
      const output = table.render();
      expect(output).toContain('Test item');
      expect(output).not.toContain('│');
    });

    it('should render table with row numbers', () => {
      const table = new Table({ showRowNumbers: true });
      table.addColumn({ key: 'item', title: 'Item' });
      table.addRows([
        { item: 'First' },
        { item: 'Second' },
        { item: 'Third' }
      ]);
      
      const output = table.render();
      expect(output).toContain('1');
      expect(output).toContain('2');
      expect(output).toContain('3');
    });

    it('should render table with alternate row colors', () => {
      const table = new Table({ alternateRowColors: true });
      table.addColumn({ key: 'item', title: 'Item' });
      table.addRows([
        { item: 'Row 1' },
        { item: 'Row 2' },
        { item: 'Row 3' },
        { item: 'Row 4' }
      ]);
      
      const output = table.render();
      expect(output).toContain('Row 1');
      expect(output).toContain('Row 4');
    });

    it('should handle empty data', () => {
      const table = new Table();
      table.addColumn({ key: 'name', title: 'Name' });
      
      const output = table.render();
      expect(output).toContain('No data to display');
    });

    it('should handle no columns', () => {
      const table = new Table();
      table.addRow({ name: 'Test' });
      
      const output = table.render();
      expect(output).toContain('No columns defined');
    });

    it('should use column formatters', () => {
      const table = new Table();
      table.addColumns([
        { 
          key: 'size', 
          title: 'Size', 
          formatter: formatters.fileSize 
        },
        { 
          key: 'active', 
          title: 'Active', 
          formatter: formatters.boolean 
        },
        { 
          key: 'date', 
          title: 'Date', 
          formatter: formatters.date 
        }
      ]);
      
      table.setData([
        { 
          size: 1024, 
          active: true, 
          date: new Date('2023-01-01') 
        },
        { 
          size: 2048, 
          active: false, 
          date: new Date('2023-01-02') 
        }
      ]);
      
      const output = table.render();
      expect(output).toContain('KB');
      expect(output).toContain('✓');
      expect(output).toContain('✗');
    });

    it('should sort data when sortable', () => {
      const table = new Table({ 
        sortBy: 'age', 
        sortDirection: 'asc' 
      });
      
      table.addColumns([
        { key: 'name', title: 'Name' },
        { key: 'age', title: 'Age', sortable: true }
      ]);
      
      table.setData([
        { name: 'Charlie', age: 35 },
        { name: 'Alice', age: 30 },
        { name: 'Bob', age: 25 }
      ]);
      
      const output = table.render();
      // Should be sorted by age ascending
      const lines = output.split('\n');
      const dataLines = lines.filter(line => line.includes('Bob') || line.includes('Alice') || line.includes('Charlie'));
      expect(dataLines[0]).toContain('Bob'); // age 25
      expect(dataLines[1]).toContain('Alice'); // age 30
      expect(dataLines[2]).toContain('Charlie'); // age 35
    });

    it('should use static simple method', () => {
      const data = [
        { name: 'Item 1', value: 100 },
        { name: 'Item 2', value: 200 }
      ];
      
      const output = Table.simple(data);
      expect(output).toContain('Item 1');
      expect(output).toContain('Item 2');
      expect(output).toContain('100');
      expect(output).toContain('200');
    });

    it('should use static keyValue method', () => {
      const data = {
        name: 'Test Application',
        version: '1.0.0',
        author: 'Test Author'
      };
      
      const output = Table.keyValue(data, 'Application Info');
      expect(output).toContain('Application Info');
      expect(output).toContain('name');
      expect(output).toContain('Test Application');
    });

    it('should use static list method', () => {
      const items = ['First item', 'Second item', 'Third item'];
      
      const output = Table.list(items, 'Item List', true);
      expect(output).toContain('Item List');
      expect(output).toContain('First item');
      expect(output).toContain('1');
      expect(output).toContain('2');
      expect(output).toContain('3');
    });
  });

  describe('Optimized Table', () => {
    it('should create optimized table', () => {
      const table = new OptimizedTable({
        useCache: true,
        useStreaming: false
      });
      expect(table).toBeDefined();
    });

    it('should create optimized table with streaming', () => {
      const table = new OptimizedTable({
        useCache: true,
        useStreaming: true,
        streamBatchSize: 25
      });
      expect(table).toBeDefined();
    });

    it('should render optimized table with caching', () => {
      const table = new OptimizedTable({ 
        title: 'Optimized Table',
        useCache: true 
      });
      
      table.addColumns([
        { key: 'id', title: 'ID', align: 'center' },
        { key: 'name', title: 'Name', align: 'left' },
        { key: 'score', title: 'Score', align: 'right' }
      ]);
      
      table.setData([
        { id: 1, name: 'Alpha', score: 95 },
        { id: 2, name: 'Beta', score: 87 },
        { id: 3, name: 'Gamma', score: 92 }
      ]);
      
      const output = table.render();
      expect(output).toContain('Optimized Table');
      expect(output).toContain('Alpha');
      expect(output).toContain('Beta');
      expect(output).toContain('Gamma');
    });

    it('should handle large datasets efficiently', () => {
      const table = new OptimizedTable({
        useCache: true,
        useStreaming: true,
        streamBatchSize: 10
      });
      
      table.addColumns([
        { key: 'id', title: 'ID' },
        { key: 'data', title: 'Data' }
      ]);
      
      // Generate large dataset
      const largeData = Array.from({ length: 100 }, (_, i) => ({
        id: i + 1,
        data: `Data item ${i + 1}`
      }));
      
      table.setData(largeData);
      
      const startTime = Date.now();
      const output = table.render();
      const endTime = Date.now();
      
      // Should handle large datasets efficiently
      expect(endTime - startTime).toBeLessThan(1000);
      expect(output).toBeDefined();
    });

    it('should use optimized static methods', () => {
      const data = [
        { product: 'Widget A', price: 19.99, stock: 150 },
        { product: 'Widget B', price: 29.99, stock: 75 },
        { product: 'Widget C', price: 39.99, stock: 200 }
      ];
      
      const output = OptimizedTable.simple(data);
      expect(output).toContain('Widget A');
      expect(output).toContain('19.99');
      expect(output).toContain('150');
    });

    it('should use optimized keyValue method', () => {
      const config = {
        database: 'postgresql',
        host: 'localhost',
        port: 5432,
        ssl: true
      };
      
      const output = OptimizedTable.keyValue(config, 'Database Configuration');
      expect(output).toContain('Database Configuration');
      expect(output).toContain('database');
      expect(output).toContain('postgresql');
    });

    it('should use optimized list method', () => {
      const features = [
        'High performance caching',
        'Streaming support for large datasets',
        'Optimized color operations',
        'Memory usage monitoring'
      ];
      
      const output = OptimizedTable.list(features, 'Optimization Features', true);
      expect(output).toContain('Optimization Features');
      expect(output).toContain('High performance caching');
      expect(output).toContain('1');
    });

    it('should clear cache', () => {
      const table = new OptimizedTable({ useCache: true });
      table.addColumn({ key: 'test', title: 'Test' });
      table.addRow({ test: 'value' });
      
      // Render to populate cache
      table.render();
      
      // Clear cache should not throw
      table.clearCache();
      expect(true).toBe(true);
    });
  });

  describe('Table formatters', () => {
    it('should format file sizes', () => {
      expect(formatters.fileSize(0)).toBe('0 B');
      expect(formatters.fileSize(1024)).toBe('1 KB');
      expect(formatters.fileSize(1048576)).toBe('1 MB');
      expect(formatters.fileSize(1073741824)).toBe('1 GB');
    });

    it('should format percentages', () => {
      expect(formatters.percentage(0.5)).toBe('50%');
      expect(formatters.percentage(0.75)).toBe('75%');
      expect(formatters.percentage(1.0)).toBe('100%');
    });

    it('should format boolean values', () => {
      const trueResult = formatters.boolean(true);
      const falseResult = formatters.boolean(false);
      
      expect(trueResult).toContain('✓');
      expect(falseResult).toContain('✗');
    });

    it('should format numbers with commas', () => {
      expect(formatters.number(1000)).toBe('1,000');
      expect(formatters.number(1234567)).toBe('1,234,567');
    });

    it('should format dates', () => {
      const date = new Date('2023-01-01');
      const formatted = formatters.date(date);
      expect(formatted).toContain('2023');
    });

    it('should format timestamps', () => {
      const date = new Date('2023-01-01T12:00:00Z');
      const formatted = formatters.timestamp(date);
      expect(formatted).toContain('2023');
      expect(formatted).toContain('12');
    });

    it('should truncate long text', () => {
      const truncate10 = formatters.truncate(10);
      expect(truncate10('This is a very long text')).toBe('This is...');
    });

    it('should format status with colors', () => {
      const successStatus = formatters.status('success');
      const errorStatus = formatters.status('error');
      const warningStatus = formatters.status('warning');
      
      expect(successStatus).toContain('success');
      expect(errorStatus).toContain('error');
      expect(warningStatus).toContain('warning');
    });
  });

  describe('Performance characteristics', () => {
    it('should handle wide tables efficiently', () => {
      const table = new OptimizedTable({ useCache: true });
      
      // Create table with many columns
      const columns = Array.from({ length: 20 }, (_, i) => ({
        key: `col${i}`,
        title: `Column ${i + 1}`,
        align: 'left' as const
      }));
      
      table.addColumns(columns);
      
      // Add data
      const data = Array.from({ length: 10 }, (_, i) => {
        const row: any = {};
        columns.forEach((col, j) => {
          row[col.key] = `Data ${i + 1}-${j + 1}`;
        });
        return row;
      });
      
      table.setData(data);
      
      const startTime = Date.now();
      const output = table.render();
      const endTime = Date.now();
      
      expect(endTime - startTime).toBeLessThan(500);
      expect(output).toBeDefined();
    });

    it('should handle deep tables efficiently', () => {
      const table = new OptimizedTable({ 
        useCache: true,
        useStreaming: true,
        streamBatchSize: 50
      });
      
      table.addColumns([
        { key: 'id', title: 'ID' },
        { key: 'name', title: 'Name' },
        { key: 'description', title: 'Description' }
      ]);
      
      // Create table with many rows
      const data = Array.from({ length: 500 }, (_, i) => ({
        id: i + 1,
        name: `Item ${i + 1}`,
        description: `Description for item ${i + 1} with some additional text`
      }));
      
      table.setData(data);
      
      const startTime = Date.now();
      const output = table.render();
      const endTime = Date.now();
      
      expect(endTime - startTime).toBeLessThan(2000);
      expect(output).toBeDefined();
    });
  });
});