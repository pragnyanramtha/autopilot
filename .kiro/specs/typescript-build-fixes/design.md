# Design Document

## Overview

This design addresses TypeScript compilation errors by implementing backward-compatible interfaces and proper type handling across the UI component system. The solution maintains existing functionality while ensuring type safety.

## Architecture

The fix involves three main areas:
1. **Table Component Interface Enhancement** - Making the Table component backward compatible with existing usage patterns
2. **Symbol System Type Consistency** - Ensuring SymbolSet interface matches all implementations
3. **Error Display Type Safety** - Proper handling of optional parameters in error display components

## Components and Interfaces

### Table Component Redesign

**Current Issues:**
- Files use `header` property but interface expects `title`
- Constructor expects `TableOptions` but files pass column arrays
- Missing properties in TableColumn interface

**Solution:**
- Make `title` optional in TableColumn interface
- Add `header` as legacy support property
- Update constructor to accept both `TableOptions` and `TableColumn[]`
- Map `header` to `title` in constructor logic

```typescript
export interface TableColumn {
  key: string;
  title?: string;
  header?: string; // Legacy support
  width?: number;
  align?: 'left' | 'center' | 'right';
  formatter?: (value: any) => string;
  sortable?: boolean;
}

constructor(optionsOrColumns: TableOptions | TableColumn[] = {}) {
  if (Array.isArray(optionsOrColumns)) {
    // Handle legacy column array usage
    this.columns = optionsOrColumns.map(col => ({
      ...col,
      title: col.header || col.title || col.key || ''
    }));
  }
}
```

### Symbol System Consistency

**Current Issues:**
- TerminalAdapter uses properties not in SymbolSet interface
- Loading property expects string[] but receives string

**Solution:**
- Remove non-standard properties from symbol objects
- Ensure loading property is always string[]
- Add missing imports (chalk)

### Error Display Type Safety

**Current Issues:**
- ErrorDisplayOptions.message is optional but used without null check
- Color function return types inconsistent

**Solution:**
- Add null check for message parameter
- Fallback to error.message when message is undefined
- Ensure consistent return types for color functions

## Data Models

### TableColumn Interface
```typescript
interface TableColumn {
  key: string;
  title?: string;      // Made optional
  header?: string;     // Legacy support
  width?: number;
  align?: 'left' | 'center' | 'right';
  formatter?: (value: any) => string;
  sortable?: boolean;
}
```

### SymbolSet Consistency
- Ensure all symbol objects conform to SymbolSet interface
- Remove non-standard properties like 'check', 'cross'
- Use standard properties like 'checkbox', 'checkboxChecked'

## Error Handling

- **Graceful Degradation**: When `header` is used instead of `title`, map it automatically
- **Null Safety**: Check for undefined/null values before using them
- **Type Consistency**: Ensure return types match interface definitions

## Testing Strategy

1. **Unit Tests**: Test Table constructor with both legacy and new syntax
2. **Type Tests**: Verify TypeScript compilation succeeds
3. **Integration Tests**: Test UI components render correctly with fixed types
4. **Regression Tests**: Ensure existing functionality still works