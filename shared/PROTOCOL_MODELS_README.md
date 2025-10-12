# Protocol Models Implementation

## Overview

This document describes the core data models for the JSON Instruction Protocol, implemented in `shared/protocol_models.py`.

## Components

### 1. Metadata
- **Purpose**: Stores protocol metadata (description, complexity, vision usage, duration)
- **Validation**: Ensures description is not empty and complexity is valid (simple/medium/complex)

### 2. ActionStep
- **Purpose**: Represents a single action in the protocol
- **Fields**:
  - `action`: Action name (e.g., "press_key", "type", "mouse_move")
  - `params`: Dictionary of action parameters
  - `wait_after_ms`: Delay after action execution
  - `description`: Optional human-readable description
- **Validation**: 
  - Validates action name against registered actions
  - Ensures params is a dictionary
  - Ensures wait_after_ms is non-negative
- **Serialization**: `to_dict()` and `from_dict()` methods

### 3. MacroDefinition
- **Purpose**: Represents a reusable sequence of actions
- **Fields**:
  - `name`: Macro name
  - `actions`: List of ActionStep objects
- **Validation**:
  - Ensures name is not empty
  - Ensures at least one action exists
  - Validates all actions in the sequence
  - Detects self-referencing circular dependencies
- **Serialization**: `to_dict()` and `from_dict()` methods

### 4. ProtocolSchema
- **Purpose**: Main protocol schema representing a complete automation workflow
- **Fields**:
  - `version`: Protocol version (e.g., "1.0")
  - `metadata`: Metadata object
  - `actions`: List of ActionStep objects
  - `macros`: Dictionary of MacroDefinition objects
- **Validation**:
  - Validates version is not empty
  - Validates metadata
  - Validates all macros
  - Detects circular dependencies between macros (using DFS)
  - Ensures at least one action exists
  - Validates all actions
  - Ensures referenced macros are defined
  - Validates macro variable substitution syntax
- **Serialization**: 
  - `to_dict()` and `to_json()` for serialization
  - `from_dict()` and `from_json()` for deserialization

## Key Features

### Validation
- Comprehensive validation at every level
- Clear error messages with context
- Circular dependency detection using depth-first search
- Parameter type checking

### Serialization/Deserialization
- Full JSON serialization support
- Preserves all data during round-trip conversion
- Handles optional fields gracefully
- Clear error messages for invalid JSON

### Error Handling
- Custom `ValidationError` exception
- Detailed error messages with context
- Fails fast on invalid data

## Usage Example

```python
from shared.protocol_models import ProtocolSchema, ActionStep, MacroDefinition, Metadata

# Create a protocol
protocol = ProtocolSchema(
    version="1.0",
    metadata=Metadata(
        description="Search for Elon Musk",
        complexity="simple",
        uses_vision=False
    ),
    macros={
        "search_in_browser": MacroDefinition(
            name="search_in_browser",
            actions=[
                ActionStep(action="shortcut", params={"keys": ["ctrl", "l"]}, wait_after_ms=200),
                ActionStep(action="type", params={"text": "{{query}}"}, wait_after_ms=100),
                ActionStep(action="press_key", params={"key": "enter"}, wait_after_ms=5000)
            ]
        )
    },
    actions=[
        ActionStep(action="open_app", params={"app_name": "chrome"}, wait_after_ms=2000),
        ActionStep(action="macro", params={"name": "search_in_browser", "vars": {"query": "elon musk"}})
    ]
)

# Validate
valid_actions = {"open_app", "shortcut", "type", "press_key", "macro"}
protocol.validate(valid_actions)

# Serialize to JSON
json_str = protocol.to_json()

# Deserialize from JSON
restored = ProtocolSchema.from_json(json_str)
```

## Testing

Comprehensive tests are available in:
- `tests/test_protocol_models_simple.py` - Standalone tests (no dependencies)
- `tests/test_protocol_models.py` - Pytest-based tests (requires pytest)

Run tests:
```bash
python tests/test_protocol_models_simple.py
```

All tests pass successfully, covering:
- Metadata validation
- ActionStep validation and serialization
- MacroDefinition validation and circular dependency detection
- ProtocolSchema validation and complex scenarios
- Full serialization/deserialization cycles
- Circular macro dependency detection
- Complex nested macro scenarios

## Requirements Satisfied

This implementation satisfies the following requirements from the spec:

- **Requirement 1.1**: JSON protocol structure with version, metadata, and actions
- **Requirement 1.2**: Structured format with validation
- **Requirement 1.3**: Schema validation before execution
- **Requirement 6.1-6.6**: Comprehensive error handling and validation
- **Requirement 7.1**: Macro composition support with circular dependency detection

## Next Steps

The next task in the implementation plan is to create the JSON protocol parser and validator that will use these data models to parse and validate incoming protocols.
