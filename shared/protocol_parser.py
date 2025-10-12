"""
JSON Protocol Parser and Validator

This module provides comprehensive validation for the JSON Instruction Protocol,
including schema validation, action validation, macro validation, and timing validation.
"""

import json
from typing import Dict, List, Any, Set, Optional, Tuple
from dataclasses import dataclass
import re
import sys
import os

# Add parent directory to path for standalone testing
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.protocol_models import ProtocolSchema, ValidationError, ActionStep, MacroDefinition


# Define all valid actions in the protocol
VALID_ACTIONS = {
    # Keyboard actions
    "press_key", "shortcut", "type", "type_with_delay", "hold_key", "release_key",
    
    # Mouse actions
    "mouse_move", "mouse_click", "mouse_double_click", "mouse_right_click",
    "mouse_drag", "mouse_scroll", "mouse_position",
    
    # Window management
    "open_app", "close_app", "switch_window", "minimize_window",
    "maximize_window", "restore_window", "get_active_window",
    
    # Browser actions
    "open_url", "browser_back", "browser_forward", "browser_refresh",
    "browser_new_tab", "browser_close_tab", "browser_switch_tab",
    "browser_address_bar", "browser_bookmark", "browser_find",
    
    # Clipboard actions
    "copy", "paste", "cut", "get_clipboard", "set_clipboard", "paste_from_clipboard",
    
    # File system actions
    "open_file", "save_file", "save_as", "open_file_dialog",
    "create_folder", "delete_file",
    
    # Screen capture
    "capture_screen", "capture_region", "capture_window", "save_screenshot",
    
    # Timing and control
    "delay", "wait_for_window", "wait_for_image", "wait_for_color",
    
    # Visual verification
    "verify_screen", "verify_element", "find_element", "verify_text",
    
    # System control
    "lock_screen", "sleep_system", "shutdown_system", "restart_system",
    "volume_up", "volume_down", "volume_mute",
    
    # Text editing
    "select_all", "undo", "redo", "find_replace", "delete_line", "duplicate_line",
    
    # Macro execution
    "macro"
}


# Action parameter specifications
ACTION_PARAMS = {
    "press_key": {"required": ["key"], "optional": []},
    "shortcut": {"required": ["keys"], "optional": []},
    "type": {"required": ["text"], "optional": ["interval_ms"]},
    "type_with_delay": {"required": ["text", "delay_ms"], "optional": []},
    "hold_key": {"required": ["key"], "optional": []},
    "release_key": {"required": ["key"], "optional": []},
    
    "mouse_move": {"required": ["x", "y"], "optional": ["smooth", "speed"]},
    "mouse_click": {"required": [], "optional": ["button", "clicks"]},
    "mouse_double_click": {"required": [], "optional": ["button"]},
    "mouse_right_click": {"required": [], "optional": []},
    "mouse_drag": {"required": ["x", "y"], "optional": ["smooth"]},
    "mouse_scroll": {"required": ["direction", "amount"], "optional": []},
    "mouse_position": {"required": [], "optional": []},
    
    "open_app": {"required": ["app_name"], "optional": []},
    "close_app": {"required": ["app_name"], "optional": []},
    "switch_window": {"required": [], "optional": ["direction"]},
    "minimize_window": {"required": [], "optional": []},
    "maximize_window": {"required": [], "optional": []},
    "restore_window": {"required": [], "optional": []},
    "get_active_window": {"required": [], "optional": []},
    
    "open_url": {"required": ["url"], "optional": []},
    "browser_back": {"required": [], "optional": []},
    "browser_forward": {"required": [], "optional": []},
    "browser_refresh": {"required": [], "optional": []},
    "browser_new_tab": {"required": [], "optional": []},
    "browser_close_tab": {"required": [], "optional": []},
    "browser_switch_tab": {"required": [], "optional": ["direction"]},
    "browser_address_bar": {"required": [], "optional": []},
    "browser_bookmark": {"required": [], "optional": []},
    "browser_find": {"required": [], "optional": []},
    
    "copy": {"required": [], "optional": []},
    "paste": {"required": [], "optional": []},
    "cut": {"required": [], "optional": []},
    "get_clipboard": {"required": [], "optional": []},
    "set_clipboard": {"required": ["text"], "optional": []},
    "paste_from_clipboard": {"required": ["text"], "optional": []},
    
    "open_file": {"required": ["path"], "optional": []},
    "save_file": {"required": [], "optional": []},
    "save_as": {"required": [], "optional": []},
    "open_file_dialog": {"required": [], "optional": []},
    "create_folder": {"required": ["path"], "optional": []},
    "delete_file": {"required": ["path"], "optional": []},
    
    "capture_screen": {"required": [], "optional": []},
    "capture_region": {"required": ["x", "y", "width", "height"], "optional": []},
    "capture_window": {"required": [], "optional": []},
    "save_screenshot": {"required": ["path"], "optional": []},
    
    "delay": {"required": ["ms"], "optional": []},
    "wait_for_window": {"required": ["title"], "optional": ["timeout_ms"]},
    "wait_for_image": {"required": ["image_path"], "optional": ["timeout_ms", "confidence"]},
    "wait_for_color": {"required": ["x", "y", "color"], "optional": ["timeout_ms"]},
    
    "verify_screen": {"required": ["context", "expected"], "optional": ["confidence_threshold"]},
    "verify_element": {"required": ["element_description"], "optional": []},
    "find_element": {"required": ["element_description"], "optional": []},
    "verify_text": {"required": ["text"], "optional": []},
    
    "lock_screen": {"required": [], "optional": []},
    "sleep_system": {"required": [], "optional": []},
    "shutdown_system": {"required": [], "optional": []},
    "restart_system": {"required": [], "optional": []},
    "volume_up": {"required": [], "optional": ["amount"]},
    "volume_down": {"required": [], "optional": ["amount"]},
    "volume_mute": {"required": [], "optional": []},
    
    "select_all": {"required": [], "optional": []},
    "undo": {"required": [], "optional": []},
    "redo": {"required": [], "optional": []},
    "find_replace": {"required": [], "optional": []},
    "delete_line": {"required": [], "optional": []},
    "duplicate_line": {"required": [], "optional": []},
    
    "macro": {"required": ["name"], "optional": ["vars"]},
}


@dataclass
class ValidationResult:
    """Result of protocol validation"""
    is_valid: bool
    errors: List[str] = None
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []
    
    def add_error(self, error: str) -> None:
        """Add an error message"""
        self.is_valid = False
        self.errors.append(error)
    
    def add_warning(self, warning: str) -> None:
        """Add a warning message"""
        self.warnings.append(warning)


class JSONProtocolParser:
    """
    Parser and validator for JSON Instruction Protocol
    
    Provides comprehensive validation including:
    - Schema validation
    - Action name validation
    - Parameter validation
    - Macro validation
    - Circular dependency detection
    - Variable substitution validation
    - Timing validation
    - Coordinate bounds validation
    """
    
    def __init__(self, screen_width: int = 1920, screen_height: int = 1080):
        """
        Initialize parser
        
        Args:
            screen_width: Screen width for coordinate validation
            screen_height: Screen height for coordinate validation
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.valid_actions = VALID_ACTIONS
        self.action_params = ACTION_PARAMS
    
    def parse(self, json_str: str) -> ProtocolSchema:
        """
        Parse JSON string into ProtocolSchema
        
        Args:
            json_str: JSON string to parse
            
        Returns:
            ProtocolSchema instance
            
        Raises:
            ValidationError: If parsing or validation fails
        """
        try:
            protocol = ProtocolSchema.from_json(json_str)
        except ValidationError as e:
            raise ValidationError(f"Failed to parse protocol: {str(e)}")
        
        return protocol
    
    def parse_dict(self, data: Dict[str, Any]) -> ProtocolSchema:
        """
        Parse dictionary into ProtocolSchema
        
        Args:
            data: Dictionary containing protocol data
            
        Returns:
            ProtocolSchema instance
            
        Raises:
            ValidationError: If parsing or validation fails
        """
        try:
            protocol = ProtocolSchema.from_dict(data)
        except ValidationError as e:
            raise ValidationError(f"Failed to parse protocol: {str(e)}")
        
        return protocol
    
    def validate_protocol(self, protocol: ProtocolSchema) -> ValidationResult:
        """
        Comprehensive protocol validation
        
        Args:
            protocol: ProtocolSchema to validate
            
        Returns:
            ValidationResult with errors and warnings
        """
        result = ValidationResult(is_valid=True)
        
        # Basic schema validation
        try:
            protocol.validate(self.valid_actions)
        except ValidationError as e:
            result.add_error(f"Schema validation failed: {str(e)}")
            return result
        
        # Validate action parameters
        self._validate_action_parameters(protocol, result)
        
        # Validate macros
        self._validate_macros(protocol, result)
        
        # Validate timing
        self._validate_timing(protocol, result)
        
        # Validate coordinates
        self._validate_coordinates(protocol, result)
        
        return result
    
    def _validate_action_parameters(self, protocol: ProtocolSchema, result: ValidationResult) -> None:
        """Validate parameters for each action"""
        for i, action in enumerate(protocol.actions):
            self._validate_single_action_params(action, f"Action {i}", result)
        
        for macro_name, macro in protocol.macros.items():
            for i, action in enumerate(macro.actions):
                self._validate_single_action_params(
                    action, f"Macro '{macro_name}' action {i}", result
                )
    
    def _validate_single_action_params(
        self, action: ActionStep, context: str, result: ValidationResult
    ) -> None:
        """Validate parameters for a single action"""
        if action.action not in self.action_params:
            # Action not in spec, but already validated by VALID_ACTIONS
            return
        
        spec = self.action_params[action.action]
        required_params = spec["required"]
        optional_params = spec["optional"]
        all_valid_params = set(required_params + optional_params)
        
        # Check required parameters
        for param in required_params:
            if param not in action.params:
                # Check if it's a variable substitution
                if not self._is_variable_substitution(action.params):
                    result.add_error(
                        f"{context}: Missing required parameter '{param}' for action '{action.action}'"
                    )
        
        # Check for unknown parameters
        for param in action.params.keys():
            if param not in all_valid_params:
                result.add_warning(
                    f"{context}: Unknown parameter '{param}' for action '{action.action}'"
                )
        
        # Validate specific parameter types
        self._validate_param_types(action, context, result)
    
    def _validate_param_types(
        self, action: ActionStep, context: str, result: ValidationResult
    ) -> None:
        """Validate parameter types for specific actions"""
        params = action.params
        
        # Validate shortcut keys is a list
        if action.action == "shortcut":
            if "keys" in params and not isinstance(params["keys"], list):
                result.add_error(
                    f"{context}: 'keys' parameter must be a list for shortcut action"
                )
        
        # Validate coordinates are integers
        if action.action in ["mouse_move", "mouse_drag", "capture_region", "wait_for_color"]:
            for coord in ["x", "y"]:
                if coord in params:
                    value = params[coord]
                    if not isinstance(value, (int, str)):  # str for variable substitution
                        result.add_error(
                            f"{context}: '{coord}' must be an integer or variable, got {type(value)}"
                        )
        
        # Validate timing values are non-negative
        for timing_param in ["ms", "delay_ms", "interval_ms", "timeout_ms"]:
            if timing_param in params:
                value = params[timing_param]
                if isinstance(value, int) and value < 0:
                    result.add_error(
                        f"{context}: '{timing_param}' must be non-negative, got {value}"
                    )
        
        # Validate mouse button values
        if action.action in ["mouse_click", "mouse_double_click"]:
            if "button" in params:
                valid_buttons = ["left", "right", "middle"]
                if params["button"] not in valid_buttons:
                    result.add_error(
                        f"{context}: 'button' must be one of {valid_buttons}, got '{params['button']}'"
                    )
        
        # Validate scroll direction
        if action.action == "mouse_scroll":
            if "direction" in params:
                valid_directions = ["up", "down", "left", "right"]
                if params["direction"] not in valid_directions:
                    result.add_error(
                        f"{context}: 'direction' must be one of {valid_directions}, got '{params['direction']}'"
                    )
    
    def _is_variable_substitution(self, params: Dict[str, Any]) -> bool:
        """Check if params contain variable substitution syntax"""
        for value in params.values():
            if isinstance(value, str) and "{{" in value and "}}" in value:
                return True
        return False
    
    def _validate_macros(self, protocol: ProtocolSchema, result: ValidationResult) -> None:
        """Validate macro definitions and usage"""
        # Check macro existence
        for i, action in enumerate(protocol.actions):
            if action.action == "macro":
                macro_name = action.params.get("name")
                if macro_name and macro_name not in protocol.macros:
                    result.add_error(
                        f"Action {i}: Macro '{macro_name}' is not defined"
                    )
                
                # Validate variable substitution
                if "vars" in action.params:
                    self._validate_variable_substitution(
                        macro_name, action.params["vars"], protocol, result
                    )
        
        # Circular dependency detection is already done in ProtocolSchema.validate()
        # But we can add more detailed reporting here
        try:
            protocol._check_circular_macro_dependencies()
        except ValidationError as e:
            result.add_error(f"Circular dependency detected: {str(e)}")
    
    def _validate_variable_substitution(
        self, macro_name: str, vars_dict: Dict[str, Any],
        protocol: ProtocolSchema, result: ValidationResult
    ) -> None:
        """Validate variable substitution in macro calls"""
        if not isinstance(vars_dict, dict):
            result.add_error(f"Macro '{macro_name}': 'vars' must be a dictionary")
            return
        
        if macro_name not in protocol.macros:
            return  # Already reported as error
        
        macro = protocol.macros[macro_name]
        
        # Find all variables used in macro ({{var}} syntax)
        used_vars = set()
        for action in macro.actions:
            for param_value in action.params.values():
                if isinstance(param_value, str):
                    # Find all {{var}} patterns
                    matches = re.findall(r'\{\{(\w+)\}\}', param_value)
                    used_vars.update(matches)
        
        # Check if all used variables are provided
        provided_vars = set(vars_dict.keys())
        missing_vars = used_vars - provided_vars
        if missing_vars:
            result.add_warning(
                f"Macro '{macro_name}': Missing variables {missing_vars}"
            )
        
        # Check for unused variables
        unused_vars = provided_vars - used_vars
        if unused_vars:
            result.add_warning(
                f"Macro '{macro_name}': Unused variables {unused_vars}"
            )
    
    def _validate_timing(self, protocol: ProtocolSchema, result: ValidationResult) -> None:
        """Validate timing consistency"""
        # Calculate total wait time from actions
        total_wait_ms = 0
        
        for action in protocol.actions:
            total_wait_ms += action.wait_after_ms
            
            # Add explicit delays
            if action.action == "delay":
                total_wait_ms += action.params.get("ms", 0)
        
        # Check against estimated duration
        if protocol.metadata.estimated_duration_seconds:
            estimated_ms = protocol.metadata.estimated_duration_seconds * 1000
            
            # Allow 20% variance
            lower_bound = estimated_ms * 0.8
            upper_bound = estimated_ms * 1.2
            
            if total_wait_ms < lower_bound or total_wait_ms > upper_bound:
                result.add_warning(
                    f"Timing inconsistency: Total wait time ({total_wait_ms}ms) differs significantly "
                    f"from estimated duration ({estimated_ms}ms)"
                )
    
    def _validate_coordinates(self, protocol: ProtocolSchema, result: ValidationResult) -> None:
        """Validate screen coordinates are within bounds"""
        for i, action in enumerate(protocol.actions):
            self._validate_action_coordinates(action, f"Action {i}", result)
        
        for macro_name, macro in protocol.macros.items():
            for i, action in enumerate(macro.actions):
                self._validate_action_coordinates(
                    action, f"Macro '{macro_name}' action {i}", result
                )
    
    def _validate_action_coordinates(
        self, action: ActionStep, context: str, result: ValidationResult
    ) -> None:
        """Validate coordinates for a single action"""
        params = action.params
        
        # Check x coordinate
        if "x" in params:
            x = params["x"]
            if isinstance(x, int):
                if x < 0 or x > self.screen_width:
                    result.add_warning(
                        f"{context}: x coordinate {x} is outside screen bounds (0-{self.screen_width})"
                    )
        
        # Check y coordinate
        if "y" in params:
            y = params["y"]
            if isinstance(y, int):
                if y < 0 or y > self.screen_height:
                    result.add_warning(
                        f"{context}: y coordinate {y} is outside screen bounds (0-{self.screen_height})"
                    )
        
        # Check region bounds
        if action.action == "capture_region":
            if "width" in params and "x" in params:
                x = params["x"]
                width = params["width"]
                if isinstance(x, int) and isinstance(width, int):
                    if x + width > self.screen_width:
                        result.add_warning(
                            f"{context}: Region extends beyond screen width "
                            f"(x={x}, width={width}, screen_width={self.screen_width})"
                        )
            
            if "height" in params and "y" in params:
                y = params["y"]
                height = params["height"]
                if isinstance(y, int) and isinstance(height, int):
                    if y + height > self.screen_height:
                        result.add_warning(
                            f"{context}: Region extends beyond screen height "
                            f"(y={y}, height={height}, screen_height={self.screen_height})"
                        )


# Convenience function
def validate_protocol_json(json_str: str, screen_width: int = 1920, screen_height: int = 1080) -> ValidationResult:
    """
    Validate a JSON protocol string
    
    Args:
        json_str: JSON string to validate
        screen_width: Screen width for coordinate validation
        screen_height: Screen height for coordinate validation
        
    Returns:
        ValidationResult with errors and warnings
    """
    parser = JSONProtocolParser(screen_width, screen_height)
    
    try:
        protocol = parser.parse(json_str)
        return parser.validate_protocol(protocol)
    except ValidationError as e:
        result = ValidationResult(is_valid=False)
        result.add_error(str(e))
        return result


if __name__ == "__main__":
    # Test the parser
    example_json = """
    {
        "version": "1.0",
        "metadata": {
            "description": "Test protocol",
            "complexity": "simple",
            "uses_vision": false,
            "estimated_duration_seconds": 10
        },
        "macros": {
            "search": [
                {"action": "shortcut", "params": {"keys": ["ctrl", "l"]}, "wait_after_ms": 200},
                {"action": "type", "params": {"text": "{{query}}"}, "wait_after_ms": 100}
            ]
        },
        "actions": [
            {"action": "open_app", "params": {"app_name": "chrome"}, "wait_after_ms": 2000},
            {"action": "macro", "params": {"name": "search", "vars": {"query": "test"}}}
        ]
    }
    """
    
    result = validate_protocol_json(example_json)
    
    if result.is_valid:
        print("✓ Protocol is valid!")
    else:
        print("✗ Protocol validation failed!")
        for error in result.errors:
            print(f"  ERROR: {error}")
    
    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"  WARNING: {warning}")
