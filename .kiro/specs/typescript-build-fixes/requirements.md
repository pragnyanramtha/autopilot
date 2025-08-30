# Requirements Document

## Introduction

This spec addresses TypeScript compilation errors in the autopilot project. The build is currently failing due to type mismatches, missing properties, and interface inconsistencies across multiple files.

## Requirements

### Requirement 1

**User Story:** As a developer, I want the TypeScript build to compile successfully, so that I can build and deploy the application.

#### Acceptance Criteria

1. WHEN running `npm run build` THEN the system SHALL compile without TypeScript errors
2. WHEN using Table components THEN the system SHALL accept both `header` and `title` properties for column definitions
3. WHEN creating Table instances THEN the system SHALL support both legacy column array syntax and new options object syntax

### Requirement 2

**User Story:** As a developer, I want consistent type definitions across UI components, so that I can use them reliably without type errors.

#### Acceptance Criteria

1. WHEN defining TableColumn objects THEN the system SHALL accept either `header` or `title` properties
2. WHEN using SymbolSet interface THEN the system SHALL have consistent property definitions across all implementations
3. WHEN using color functions THEN the system SHALL have proper type definitions that match the actual implementation

### Requirement 3

**User Story:** As a developer, I want proper error handling in display components, so that optional parameters are handled correctly.

#### Acceptance Criteria

1. WHEN ErrorDisplay.show() is called with undefined message THEN the system SHALL use the error.message as fallback
2. WHEN TerminalAdapter returns color functions THEN the system SHALL return consistent function signatures
3. WHEN loading symbols are used THEN the system SHALL expect string arrays not single strings