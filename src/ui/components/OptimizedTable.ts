import { colors } from '../utils/Colors.js';
import { symbols } from '../utils/Symbols.js';
import { Layout } from '../utils/Layout.js';
import { 
  withCache, 
  withPerformanceTracking, 
  StreamingOutput,
  formattingOptimizer 
} from '../utils/Performance.js';

export interface OptimizedTableColumn {
  key: string;
  title: string;
  width?: number;
  align?: 'left' | 'center' | 'right';
  formatter?: (value: any) => string;
  sortable?: boolean;
}

export interface OptimizedTableRow {
  [key: string]: any;
}

export interface OptimizedTableOptions {
  title?: string;
  showHeaders?: boolean;
  showBorders?: boolean;
  showRowNumbers?: boolean;
  alternateRowColors?: boolean;
  maxWidth?: number;
  compact?: boolean;
  sortBy?: string;
  sortDirection?: 'asc' | 'desc';
  useCache?: boolean;
  useStreaming?: boolean;
  streamBatchSize?: number;
}

export interface OptimizedTableStyle {
  headerColor: (text: string) => string;
  rowColor: (text: string) => string;
  alternateRowColor: (text: string) => string;
  borderColor: (text: string) => string;
  numberColor: (text: string) => string;
}

export class OptimizedTable {
  private columns: OptimizedTableColumn[] = [];
  private rows: OptimizedTableRow[] = [];
  private options: OptimizedTableOptions;
  private style: OptimizedTableStyle;
  private columnWidthsCache: Map<string, number> | null = null;

  constructor(options: OptimizedTableOptions = {}) {
    this.options = {
      showHeaders: true,
      showBorders: true,
      showRowNumbers: false,
      alternateRowColors: false,
      compact: false,
      sortDirection: 'asc',
      useCache: true,
      useStreaming: false,
      streamBatchSize: 50,
      ...options
    };

    this.style = {
      headerColor: colors.primaryBold,
      rowColor: colors.reset,
      alternateRowColor: colors.muted,
      borderColor: colors.muted,
      numberColor: colors.secondary
    };
  }

  // Optimized column addition
  addColumn(column: OptimizedTableColumn): this {
    this.columns.push(column);
    this.columnWidthsCache = null; // Invalidate cache
    return this;
  }

  addColumns(columns: OptimizedTableColumn[]): this {
    this.columns.push(...columns);
    this.columnWidthsCache = null; // Invalidate cache
    return this;
  }

  // Optimized row addition
  addRow(row: OptimizedTableRow): this {
    this.rows.push(row);
    return this;
  }

  addRows(rows: OptimizedTableRow[]): this {
    this.rows.push(...rows);
    return this;
  }

  setData(rows: OptimizedTableRow[]): this {
    this.rows = [...rows];
    return this;
  }

  setStyle(style: Partial<OptimizedTableStyle>): this {
    this.style = { ...this.style, ...style };
    return this;
  }

  // Cached column width calculation
  private calculateColumnWidths(): Map<string, number> {
    if (this.columnWidthsCache && this.options.useCache) {
      return this.columnWidthsCache;
    }

    return withPerformanceTracking('table-calculate-widths', () => {
      const terminalWidth = Layout.getTerminalWidth();
      const maxTableWidth = Math.min(this.options.maxWidth || terminalWidth - 4, terminalWidth - 4);
      const columnWidths = new Map<string, number>();
      
      // Calculate minimum widths based on content
      for (const column of this.columns) {
        let maxWidth = column.title.length;
        
        // Check all row values for this column
        for (const row of this.rows) {
          const value = this.formatCellValue(row[column.key], column);
          maxWidth = Math.max(maxWidth, value.length);
        }
        
        // Use specified width or calculated width
        const width = column.width || maxWidth;
        columnWidths.set(column.key, width);
      }

      // Adjust widths if table is too wide
      const totalWidth = Array.from(columnWidths.values()).reduce((sum, width) => sum + width, 0);
      const borderWidth = this.options.showBorders ? (this.columns.length + 1) * 3 : this.columns.length - 1;
      const rowNumberWidth = this.options.showRowNumbers ? 6 : 0;
      const actualTableWidth = totalWidth + borderWidth + rowNumberWidth;

      if (actualTableWidth > maxTableWidth) {
        // Proportionally reduce column widths
        const ratio = (maxTableWidth - borderWidth - rowNumberWidth) / totalWidth;
        for (const [key, width] of columnWidths) {
          columnWidths.set(key, Math.max(3, Math.floor(width * ratio)));
        }
      }

      if (this.options.useCache) {
        this.columnWidthsCache = columnWidths;
      }

      return columnWidths;
    });
  }

  // Cached cell value formatting
  private formatCellValue(value: any, column: OptimizedTableColumn): string {
    if (value === null || value === undefined) {
      return '';
    }

    const cacheKey = this.options.useCache ? 
      `cell-${column.key}-${JSON.stringify(value)}-${column.formatter?.toString()}` : 
      null;

    if (cacheKey) {
      const cached = withCache(cacheKey, () => null);
      if (cached) return cached;
    }

    let result: string;
    if (column.formatter) {
      result = column.formatter(value);
    } else {
      result = String(value);
    }

    if (cacheKey) {
      withCache(cacheKey, () => result);
    }

    return result;
  }

  // Optimized text alignment
  private alignText(text: string, width: number, align: 'left' | 'center' | 'right' = 'left'): string {
    const cacheKey = this.options.useCache ? `align-${text}-${width}-${align}` : null;
    
    if (cacheKey) {
      const cached = withCache(cacheKey, () => null);
      if (cached) return cached;
    }

    const truncated = Layout.truncate(text, width);
    const result = Layout.pad(truncated, width, ' ', align);

    if (cacheKey) {
      withCache(cacheKey, () => result);
    }

    return result;
  }

  // Cached border creation
  private createBorder(type: 'top' | 'middle' | 'bottom', columnWidths: Map<string, number>): string {
    if (!this.options.showBorders) return '';

    const cacheKey = this.options.useCache ? 
      `border-${type}-${Array.from(columnWidths.values()).join(',')}-${this.options.showRowNumbers}` : 
      null;

    if (cacheKey) {
      const cached = withCache(cacheKey, () => null);
      if (cached) return cached;
    }

    const rowNumberWidth = this.options.showRowNumbers ? 6 : 0;
    let border = '';

    // Row number section
    if (this.options.showRowNumbers) {
      if (type === 'top') {
        border += symbols.boxTopLeft + symbols.boxHorizontal.repeat(rowNumberWidth - 2) + symbols.boxHorizontal;
      } else if (type === 'middle') {
        border += symbols.boxVertical + symbols.boxHorizontal.repeat(rowNumberWidth - 2) + symbols.boxCross;
      } else {
        border += symbols.boxBottomLeft + symbols.boxHorizontal.repeat(rowNumberWidth - 2) + symbols.boxHorizontal;
      }
    } else {
      if (type === 'top') {
        border += symbols.boxTopLeft;
      } else if (type === 'bottom') {
        border += symbols.boxBottomLeft;
      } else {
        border += symbols.boxVertical;
      }
    }

    // Column sections
    for (let i = 0; i < this.columns.length; i++) {
      const column = this.columns[i];
      const width = columnWidths.get(column.key) || 10;
      
      border += symbols.boxHorizontal.repeat(width + 2);
      
      if (i < this.columns.length - 1) {
        if (type === 'top') {
          border += symbols.boxHorizontal;
        } else if (type === 'middle') {
          border += symbols.boxCross;
        } else {
          border += symbols.boxHorizontal;
        }
      }
    }

    // End border
    if (type === 'top') {
      border += symbols.boxTopRight;
    } else if (type === 'bottom') {
      border += symbols.boxBottomRight;
    } else {
      border += symbols.boxVertical;
    }

    const result = this.style.borderColor(border);

    if (cacheKey) {
      withCache(cacheKey, () => result);
    }

    return result;
  }

  // Optimized header row creation
  private createHeaderRow(columnWidths: Map<string, number>): string {
    if (!this.options.showHeaders) return '';

    const cacheKey = this.options.useCache ? 
      `header-${this.columns.map(c => c.title).join(',')}-${Array.from(columnWidths.values()).join(',')}` : 
      null;

    if (cacheKey) {
      const cached = withCache(cacheKey, () => null);
      if (cached) return cached;
    }

    let row = '';

    // Row number header
    if (this.options.showRowNumbers) {
      if (this.options.showBorders) {
        row += this.style.borderColor(symbols.boxVertical) + ' ';
      }
      row += this.style.headerColor(Layout.pad('#', 4, ' ', 'center'));
      if (this.options.showBorders) {
        row += ' ';
      }
    }

    // Batch color operations for headers
    const headerOperations = this.columns.map(column => {
      const width = columnWidths.get(column.key) || 10;
      const headerText = this.alignText(column.title, width, column.align);
      return { text: headerText, colorFn: this.style.headerColor };
    });

    const coloredHeaders = formattingOptimizer.batchColorOperations(headerOperations);

    // Build header row
    for (let i = 0; i < this.columns.length; i++) {
      if (this.options.showBorders) {
        row += this.style.borderColor(symbols.boxVertical) + ' ';
      } else if (i > 0) {
        row += ' ';
      }

      row += coloredHeaders[i];

      if (this.options.showBorders) {
        row += ' ';
      }
    }

    if (this.options.showBorders) {
      row += this.style.borderColor(symbols.boxVertical);
    }

    if (cacheKey) {
      withCache(cacheKey, () => row);
    }

    return row;
  }

  // Optimized data row creation
  private createDataRow(rowData: OptimizedTableRow, rowIndex: number, columnWidths: Map<string, number>): string {
    const cacheKey = this.options.useCache ? 
      `row-${rowIndex}-${JSON.stringify(rowData)}-${Array.from(columnWidths.values()).join(',')}` : 
      null;

    if (cacheKey) {
      const cached = withCache(cacheKey, () => null);
      if (cached) return cached;
    }

    let row = '';
    const isAlternate = this.options.alternateRowColors && rowIndex % 2 === 1;
    const rowColorFn = isAlternate ? this.style.alternateRowColor : this.style.rowColor;

    // Row number
    if (this.options.showRowNumbers) {
      if (this.options.showBorders) {
        row += this.style.borderColor(symbols.boxVertical) + ' ';
      }
      row += this.style.numberColor(Layout.pad(String(rowIndex + 1), 4, ' ', 'right'));
      if (this.options.showBorders) {
        row += ' ';
      }
    }

    // Batch color operations for row data
    const cellOperations = this.columns.map(column => {
      const width = columnWidths.get(column.key) || 10;
      const cellValue = this.formatCellValue(rowData[column.key], column);
      const alignedText = this.alignText(cellValue, width, column.align);
      return { text: alignedText, colorFn: rowColorFn };
    });

    const coloredCells = formattingOptimizer.batchColorOperations(cellOperations);

    // Build data row
    for (let i = 0; i < this.columns.length; i++) {
      if (this.options.showBorders) {
        row += this.style.borderColor(symbols.boxVertical) + ' ';
      } else if (i > 0) {
        row += ' ';
      }

      row += coloredCells[i];

      if (this.options.showBorders) {
        row += ' ';
      }
    }

    if (this.options.showBorders) {
      row += this.style.borderColor(symbols.boxVertical);
    }

    if (cacheKey) {
      withCache(cacheKey, () => row);
    }

    return row;
  }

  // Cached row sorting
  private sortRows(): OptimizedTableRow[] {
    if (!this.options.sortBy) {
      return this.rows;
    }

    const cacheKey = this.options.useCache ? 
      `sorted-${this.options.sortBy}-${this.options.sortDirection}-${this.rows.length}` : 
      null;

    if (cacheKey) {
      const cached = withCache(cacheKey, () => null);
      if (cached) return JSON.parse(cached);
    }

    const column = this.columns.find(col => col.key === this.options.sortBy);
    if (!column || !column.sortable) {
      return this.rows;
    }

    const sortedRows = [...this.rows].sort((a, b) => {
      const aValue = a[column.key];
      const bValue = b[column.key];

      // Handle null/undefined values
      if (aValue == null && bValue == null) return 0;
      if (aValue == null) return 1;
      if (bValue == null) return -1;

      // Compare values
      let comparison = 0;
      if (typeof aValue === 'number' && typeof bValue === 'number') {
        comparison = aValue - bValue;
      } else {
        comparison = String(aValue).localeCompare(String(bValue));
      }

      return this.options.sortDirection === 'desc' ? -comparison : comparison;
    });

    if (cacheKey) {
      withCache(cacheKey, () => JSON.stringify(sortedRows));
    }

    return sortedRows;
  }

  // Optimized render with streaming support
  render(): string {
    return withPerformanceTracking('table-render', () => {
      if (this.columns.length === 0) {
        return colors.warning('No columns defined for table');
      }

      if (this.rows.length === 0) {
        return colors.muted('No data to display');
      }

      // Use streaming for large tables
      if (this.options.useStreaming && this.rows.length > (this.options.streamBatchSize || 50)) {
        this.renderStreaming();
        return '';
      }

      const columnWidths = this.calculateColumnWidths();
      const sortedRows = this.sortRows();
      const lines: string[] = [];

      // Table title
      if (this.options.title) {
        lines.push(colors.primaryBold(this.options.title));
        if (!this.options.compact) {
          lines.push('');
        }
      }

      // Top border
      if (this.options.showBorders) {
        lines.push(this.createBorder('top', columnWidths));
      }

      // Header row
      if (this.options.showHeaders) {
        lines.push(this.createHeaderRow(columnWidths));
        
        if (this.options.showBorders) {
          lines.push(this.createBorder('middle', columnWidths));
        }
      }

      // Data rows
      for (let i = 0; i < sortedRows.length; i++) {
        lines.push(this.createDataRow(sortedRows[i], i, columnWidths));
      }

      // Bottom border
      if (this.options.showBorders) {
        lines.push(this.createBorder('bottom', columnWidths));
      }

      return lines.join('\n');
    });
  }

  // Streaming render for large tables
  private renderStreaming(): void {
    withPerformanceTracking('table-render-streaming', async () => {
      const streamOutput = new StreamingOutput();
      const columnWidths = this.calculateColumnWidths();
      const sortedRows = this.sortRows();

      // Table title
      if (this.options.title) {
        streamOutput.writeLine(colors.primaryBold(this.options.title));
        if (!this.options.compact) {
          streamOutput.writeLine('');
        }
      }

      // Top border
      if (this.options.showBorders) {
        streamOutput.writeLine(this.createBorder('top', columnWidths));
      }

      // Header row
      if (this.options.showHeaders) {
        streamOutput.writeLine(this.createHeaderRow(columnWidths));
        
        if (this.options.showBorders) {
          streamOutput.writeLine(this.createBorder('middle', columnWidths));
        }
      }

      // Stream data rows in batches
      const streamOptions: { batchSize?: number; delay?: number } = { delay: 1 };
      if (this.options.streamBatchSize) {
        streamOptions.batchSize = this.options.streamBatchSize;
      }
      
      await streamOutput.streamArray(
        sortedRows,
        (row, index) => this.createDataRow(row, index, columnWidths),
        streamOptions
      );

      // Bottom border
      if (this.options.showBorders) {
        streamOutput.writeLine(this.createBorder('bottom', columnWidths));
      }

      streamOutput.end();
    });
  }

  // Clear caches
  clearCache(): void {
    this.columnWidthsCache = null;
  }

  // Static optimized helper methods
  static simple(data: OptimizedTableRow[], columns?: string[]): string {
    return withPerformanceTracking('table-simple', () => {
      if (data.length === 0) return colors.muted('No data to display');

      const table = new OptimizedTable({ compact: true, useCache: true });
      const keys = columns || Object.keys(data[0]);

      // Add columns
      for (const key of keys) {
        table.addColumn({
          key,
          title: key.charAt(0).toUpperCase() + key.slice(1).replace(/([A-Z])/g, ' $1'),
          align: 'left'
        });
      }

      // Add data
      table.setData(data);

      return table.render();
    });
  }

  static keyValue(data: Record<string, any>, title?: string): string {
    return withPerformanceTracking('table-key-value', () => {
      const table = new OptimizedTable({ 
        ...(title && { title }),
        compact: true,
        showBorders: false,
        useCache: true
      });

      table.addColumns([
        { key: 'key', title: 'Property', align: 'left' },
        { key: 'value', title: 'Value', align: 'left' }
      ]);

      const rows = Object.entries(data).map(([key, value]) => ({
        key: colors.accent(key),
        value: String(value)
      }));

      table.setData(rows);
      return table.render();
    });
  }

  static list(items: string[], title?: string, numbered: boolean = false): string {
    return withPerformanceTracking('table-list', () => {
      const table = new OptimizedTable({ 
        ...(title && { title }),
        compact: true,
        showBorders: false,
        showHeaders: false,
        showRowNumbers: numbered,
        useCache: true
      });

      table.addColumn({
        key: 'item',
        title: 'Item',
        align: 'left'
      });

      const rows = items.map(item => ({ item }));
      table.setData(rows);

      return table.render();
    });
  }
}