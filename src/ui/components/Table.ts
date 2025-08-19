import { colors } from '../utils/Colors.js';
import { symbols } from '../utils/Symbols.js';
import { Layout } from '../utils/Layout.js';

export interface TableColumn {
  key: string;
  title: string;
  width?: number;
  align?: 'left' | 'center' | 'right';
  formatter?: (value: any) => string;
  sortable?: boolean;
}

export interface TableRow {
  [key: string]: any;
}

export interface TableOptions {
  title?: string;
  showHeaders?: boolean;
  showBorders?: boolean;
  showRowNumbers?: boolean;
  alternateRowColors?: boolean;
  maxWidth?: number;
  compact?: boolean;
  sortBy?: string;
  sortDirection?: 'asc' | 'desc';
}

export interface TableStyle {
  headerColor: (text: string) => string;
  rowColor: (text: string) => string;
  alternateRowColor: (text: string) => string;
  borderColor: (text: string) => string;
  numberColor: (text: string) => string;
}

export class Table {
  private columns: TableColumn[] = [];
  private rows: TableRow[] = [];
  private options: TableOptions;
  private style: TableStyle;

  constructor(options: TableOptions = {}) {
    this.options = {
      showHeaders: true,
      showBorders: true,
      showRowNumbers: false,
      alternateRowColors: false,
      compact: false,
      sortDirection: 'asc',
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

  // Add a column to the table
  addColumn(column: TableColumn): this {
    this.columns.push(column);
    return this;
  }

  // Add multiple columns
  addColumns(columns: TableColumn[]): this {
    this.columns.push(...columns);
    return this;
  }

  // Add a row to the table
  addRow(row: TableRow): this {
    this.rows.push(row);
    return this;
  }

  // Add multiple rows
  addRows(rows: TableRow[]): this {
    this.rows.push(...rows);
    return this;
  }

  // Set table data (replaces existing rows)
  setData(rows: TableRow[]): this {
    this.rows = [...rows];
    return this;
  }

  // Set table style
  setStyle(style: Partial<TableStyle>): this {
    this.style = { ...this.style, ...style };
    return this;
  }

  // Calculate column widths
  private calculateColumnWidths(): Map<string, number> {
    const terminalWidth = Layout.getTerminalWidth();
    const maxTableWidth = this.options.maxWidth || terminalWidth - 4;
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

    return columnWidths;
  }

  // Format cell value using column formatter
  private formatCellValue(value: any, column: TableColumn): string {
    if (value === null || value === undefined) {
      return '';
    }

    if (column.formatter) {
      return column.formatter(value);
    }

    return String(value);
  }

  // Align text within cell
  private alignText(text: string, width: number, align: 'left' | 'center' | 'right' = 'left'): string {
    const truncated = Layout.truncate(text, width);
    return Layout.pad(truncated, width, ' ', align);
  }

  // Create table border
  private createBorder(type: 'top' | 'middle' | 'bottom', columnWidths: Map<string, number>): string {
    if (!this.options.showBorders) return '';

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

    return this.style.borderColor(border);
  }

  // Create header row
  private createHeaderRow(columnWidths: Map<string, number>): string {
    if (!this.options.showHeaders) return '';

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

    // Column headers
    for (let i = 0; i < this.columns.length; i++) {
      const column = this.columns[i];
      const width = columnWidths.get(column.key) || 10;
      
      if (this.options.showBorders) {
        row += this.style.borderColor(symbols.boxVertical) + ' ';
      } else if (i > 0) {
        row += ' ';
      }

      const headerText = this.alignText(column.title, width, column.align);
      row += this.style.headerColor(headerText);

      if (this.options.showBorders) {
        row += ' ';
      }
    }

    if (this.options.showBorders) {
      row += this.style.borderColor(symbols.boxVertical);
    }

    return row;
  }

  // Create data row
  private createDataRow(rowData: TableRow, rowIndex: number, columnWidths: Map<string, number>): string {
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

    // Column data
    for (let i = 0; i < this.columns.length; i++) {
      const column = this.columns[i];
      const width = columnWidths.get(column.key) || 10;
      
      if (this.options.showBorders) {
        row += this.style.borderColor(symbols.boxVertical) + ' ';
      } else if (i > 0) {
        row += ' ';
      }

      const cellValue = this.formatCellValue(rowData[column.key], column);
      const alignedText = this.alignText(cellValue, width, column.align);
      row += rowColorFn(alignedText);

      if (this.options.showBorders) {
        row += ' ';
      }
    }

    if (this.options.showBorders) {
      row += this.style.borderColor(symbols.boxVertical);
    }

    return row;
  }

  // Sort rows by column
  private sortRows(): TableRow[] {
    if (!this.options.sortBy) {
      return this.rows;
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

    return sortedRows;
  }

  // Render the complete table
  render(): string {
    if (this.columns.length === 0) {
      return colors.warning('No columns defined for table');
    }

    if (this.rows.length === 0) {
      return colors.muted('No data to display');
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
  }

  // Static helper methods for quick table creation
  static simple(data: TableRow[], columns?: string[]): string {
    if (data.length === 0) return colors.muted('No data to display');

    const table = new Table({ compact: true });
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
  }

  static keyValue(data: Record<string, any>, title?: string): string {
    const table = new Table({ 
      ...(title && { title }),
      compact: true,
      showBorders: false 
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
  }

  static list(items: string[], title?: string, numbered: boolean = false): string {
    const table = new Table({ 
      ...(title && { title }),
      compact: true,
      showBorders: false,
      showHeaders: false,
      showRowNumbers: numbered
    });

    table.addColumn({
      key: 'item',
      title: 'Item',
      align: 'left'
    });

    const rows = items.map(item => ({ item }));
    table.setData(rows);

    return table.render();
  }
}

// Export commonly used formatters
export const formatters = {
  // Format file sizes
  fileSize: (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  },

  // Format percentages
  percentage: (value: number): string => {
    return `${Math.round(value * 100)}%`;
  },

  // Format boolean values
  boolean: (value: boolean): string => {
    return value ? colors.success('✓') : colors.error('✗');
  },

  // Format status with colors
  status: (status: string): string => {
    const statusLower = status.toLowerCase();
    if (statusLower.includes('success') || statusLower.includes('active') || statusLower.includes('running')) {
      return colors.success(status);
    } else if (statusLower.includes('error') || statusLower.includes('failed') || statusLower.includes('stopped')) {
      return colors.error(status);
    } else if (statusLower.includes('warning') || statusLower.includes('pending')) {
      return colors.warning(status);
    } else {
      return colors.info(status);
    }
  },

  // Format dates
  date: (date: Date | string): string => {
    const d = typeof date === 'string' ? new Date(date) : date;
    return d.toLocaleDateString();
  },

  // Format timestamps
  timestamp: (date: Date | string): string => {
    const d = typeof date === 'string' ? new Date(date) : date;
    return d.toLocaleString();
  },

  // Format numbers with commas
  number: (num: number): string => {
    return num.toLocaleString();
  },

  // Truncate long text
  truncate: (maxLength: number) => (text: string): string => {
    return Layout.truncate(text, maxLength);
  },

  // Format code/command text
  code: (text: string): string => {
    return colors.code(text);
  },

  // Format file paths
  path: (path: string): string => {
    return colors.path(path);
  },

  // Format URLs
  url: (url: string): string => {
    return colors.url(url);
  }
};