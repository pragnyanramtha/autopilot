"""
JSON Instruction Protocol Data Models

This module defines the core data models for the JSON Instruction Protocol,
including validation, serialization, and deserialization methods.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Union
import json
from enum import Enum


class ValidationError(Exception):
    """Raised when protocol validation fails"""
    pass


@dataclass
class Metadata:
    """Protocol metadata"""
    description: str
    complexity: str = "simple"  # simple, medium, complex
    uses_vision: bool = False
    estimated_duration_seconds: Optional[int] = None
    
    def validate(self) -> None:
        """Validate metadata fields"""
        if not self.description:
            raise ValidationError("Metadata description cannot be empty")
        
        valid_complexity = ["simple", "medium", "complex"]
        if self.complexity not in valid_complexity:
            raise ValidationError(
                f"Invalid complexity '{self.complexity}'. Must be one of: {valid_complexity}"
            )


@dataclass
class ActionStep:
    """Represents a single action in the protocol"""
    action: str
    params: Dict[str, Any] = field(default_factory=dict)
    wait_after_ms: int = 0
    description: Optional[str] = None
    
    def validate(self, valid_actions: set) -> None:
        """
        Validate action step
        
        Args:
            valid_actions: Set of valid action names
            
        Raises:
            ValidationError: If validation fails
        """
        if not self.action:
            raise ValidationError("Action name cannot be empty")
        
        if self.action not in valid_actions:
            raise ValidationError(
                f"Invalid action '{self.action}'. Must be one of the registered actions."
            )
        
        if not isinstance(self.params, dict):
            raise ValidationError(f"Action params must be a dictionary, got {type(self.params)}")
        
        if self.wait_after_ms < 0:
            raise ValidationError(f"wait_after_ms must be non-negative, got {self.wait_after_ms}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = {
            "action": self.action,
            "params": self.params,
            "wait_after_ms": self.wait_after_ms
        }
        if self.description:
            result["description"] = self.description
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionStep':
        """Create ActionStep from dictionary"""
        return cls(
            action=data.get("action", ""),
            params=data.get("params", {}),
            wait_after_ms=data.get("wait_after_ms", 0),
            description=data.get("description")
        )


@dataclass
class MacroDefinition:
    """Represents a reusable macro (sequence of actions)"""
    name: str
    actions: List[ActionStep] = field(default_factory=list)
    
    def validate(self, valid_actions: set, all_macro_names: set = None) -> None:
        """
        Validate macro definition
        
        Args:
            valid_actions: Set of valid action names
            all_macro_names: Set of all macro names (for circular dependency detection)
            
        Raises:
            ValidationError: If validation fails
        """
        if not self.name:
            raise ValidationError("Macro name cannot be empty")
        
        if not self.actions:
            raise ValidationError(f"Macro '{self.name}' has no actions")
        
        # Validate each action in the macro
        for i, action in enumerate(self.actions):
            try:
                action.validate(valid_actions)
            except ValidationError as e:
                raise ValidationError(f"Macro '{self.name}' action {i}: {str(e)}")
        
        # Check for circular dependencies (macro calling itself)
        if all_macro_names:
            for action in self.actions:
                if action.action == "macro":
                    macro_name = action.params.get("name")
                    if macro_name == self.name:
                        raise ValidationError(
                            f"Circular dependency detected: Macro '{self.name}' calls itself"
                        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "actions": [action.to_dict() for action in self.actions]
        }
    
    @classmethod
    def from_dict(cls, name: str, actions_data: List[Dict[str, Any]]) -> 'MacroDefinition':
        """Create MacroDefinition from dictionary"""
        actions = [ActionStep.from_dict(action_data) for action_data in actions_data]
        return cls(name=name, actions=actions)


@dataclass
class ProtocolSchema:
    """
    Main protocol schema representing a complete automation workflow
    """
    version: str
    metadata: Metadata
    actions: List[ActionStep] = field(default_factory=list)
    macros: Dict[str, MacroDefinition] = field(default_factory=dict)
    
    def validate(self, valid_actions: set) -> None:
        """
        Validate the entire protocol
        
        Args:
            valid_actions: Set of valid action names (including 'macro')
            
        Raises:
            ValidationError: If validation fails
        """
        # Validate version
        if not self.version:
            raise ValidationError("Protocol version cannot be empty")
        
        # Validate metadata
        try:
            self.metadata.validate()
        except ValidationError as e:
            raise ValidationError(f"Metadata validation failed: {str(e)}")
        
        # Validate macros
        macro_names = set(self.macros.keys())
        for macro_name, macro in self.macros.items():
            try:
                macro.validate(valid_actions, macro_names)
            except ValidationError as e:
                raise ValidationError(f"Macro '{macro_name}' validation failed: {str(e)}")
        
        # Check for circular dependencies between macros
        self._check_circular_macro_dependencies()
        
        # Validate actions
        if not self.actions:
            raise ValidationError("Protocol must have at least one action")
        
        for i, action in enumerate(self.actions):
            try:
                action.validate(valid_actions)
                
                # If action is a macro, verify it exists
                if action.action == "macro":
                    macro_name = action.params.get("name")
                    if not macro_name:
                        raise ValidationError("Macro action must specify 'name' parameter")
                    if macro_name not in self.macros:
                        raise ValidationError(f"Macro '{macro_name}' not defined")
                    
                    # Validate variable substitution syntax
                    vars_dict = action.params.get("vars", {})
                    if not isinstance(vars_dict, dict):
                        raise ValidationError("Macro 'vars' parameter must be a dictionary")
                        
            except ValidationError as e:
                raise ValidationError(f"Action {i} validation failed: {str(e)}")
    
    def _check_circular_macro_dependencies(self) -> None:
        """
        Check for circular dependencies between macros using depth-first search
        
        Raises:
            ValidationError: If circular dependency is detected
        """
        def visit(macro_name: str, visited: set, rec_stack: set) -> None:
            visited.add(macro_name)
            rec_stack.add(macro_name)
            
            if macro_name not in self.macros:
                return
            
            macro = self.macros[macro_name]
            for action in macro.actions:
                if action.action == "macro":
                    called_macro = action.params.get("name")
                    if called_macro:
                        if called_macro not in visited:
                            visit(called_macro, visited, rec_stack)
                        elif called_macro in rec_stack:
                            raise ValidationError(
                                f"Circular dependency detected: {macro_name} -> {called_macro}"
                            )
            
            rec_stack.remove(macro_name)
        
        visited = set()
        for macro_name in self.macros.keys():
            if macro_name not in visited:
                visit(macro_name, visited, set())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert protocol to dictionary"""
        result = {
            "version": self.version,
            "metadata": asdict(self.metadata),
            "actions": [action.to_dict() for action in self.actions]
        }
        
        if self.macros:
            result["macros"] = {
                name: [action.to_dict() for action in macro.actions]
                for name, macro in self.macros.items()
            }
        
        return result
    
    def to_json(self, indent: int = 2) -> str:
        """
        Serialize protocol to JSON string
        
        Args:
            indent: JSON indentation level
            
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), indent=indent)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProtocolSchema':
        """
        Deserialize protocol from dictionary
        
        Args:
            data: Dictionary containing protocol data
            
        Returns:
            ProtocolSchema instance
            
        Raises:
            ValidationError: If required fields are missing
        """
        if "version" not in data:
            raise ValidationError("Protocol must have 'version' field")
        
        if "metadata" not in data:
            raise ValidationError("Protocol must have 'metadata' field")
        
        if "actions" not in data:
            raise ValidationError("Protocol must have 'actions' field")
        
        # Parse metadata
        metadata_data = data["metadata"]
        metadata = Metadata(
            description=metadata_data.get("description", ""),
            complexity=metadata_data.get("complexity", "simple"),
            uses_vision=metadata_data.get("uses_vision", False),
            estimated_duration_seconds=metadata_data.get("estimated_duration_seconds")
        )
        
        # Parse macros
        macros = {}
        if "macros" in data:
            for macro_name, macro_actions in data["macros"].items():
                macros[macro_name] = MacroDefinition.from_dict(macro_name, macro_actions)
        
        # Parse actions
        actions = [ActionStep.from_dict(action_data) for action_data in data["actions"]]
        
        return cls(
            version=data["version"],
            metadata=metadata,
            actions=actions,
            macros=macros
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ProtocolSchema':
        """
        Deserialize protocol from JSON string
        
        Args:
            json_str: JSON string containing protocol data
            
        Returns:
            ProtocolSchema instance
            
        Raises:
            ValidationError: If JSON is invalid or required fields are missing
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON: {str(e)}")
        
        return cls.from_dict(data)


# Example usage and testing
if __name__ == "__main__":
    # Example protocol
    example_protocol = {
        "version": "1.0",
        "metadata": {
            "description": "Search for Elon Musk",
            "complexity": "simple",
            "uses_vision": False
        },
        "macros": {
            "search_in_browser": [
                {"action": "shortcut", "params": {"keys": ["ctrl", "l"]}, "wait_after_ms": 200},
                {"action": "type", "params": {"text": "{{query}}"}, "wait_after_ms": 100},
                {"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 5000}
            ]
        },
        "actions": [
            {
                "action": "open_app",
                "params": {"app_name": "chrome"},
                "wait_after_ms": 2000
            },
            {
                "action": "macro",
                "params": {
                    "name": "search_in_browser",
                    "vars": {"query": "elon musk"}
                }
            }
        ]
    }
    
    # Test deserialization
    protocol = ProtocolSchema.from_dict(example_protocol)
    print("Protocol loaded successfully!")
    print(f"Description: {protocol.metadata.description}")
    print(f"Number of actions: {len(protocol.actions)}")
    print(f"Number of macros: {len(protocol.macros)}")
    
    # Test serialization
    json_output = protocol.to_json()
    print("\nSerialized JSON:")
    print(json_output)
    
    # Test validation (will need valid_actions set)
    valid_actions = {"open_app", "shortcut", "type", "press_key", "macro"}
    try:
        protocol.validate(valid_actions)
        print("\n✓ Protocol validation passed!")
    except ValidationError as e:
        print(f"\n✗ Validation error: {e}")
