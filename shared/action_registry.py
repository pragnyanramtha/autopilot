"""
Action Registry for JSON Instruction Protocol

This module provides a comprehensive registry of action handlers that map
action names to Python functions. It includes parameter validation, type checking,
and documentation generation capabilities.
"""

import time
import inspect
import pyperclip
import webbrowser
import os
import subprocess
import platform
from typing import Dict, Any, Callable, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ActionCategory(Enum):
    """Categories for organizing actions."""
    KEYBOARD = "keyboard"
    MOUSE = "mouse"
    WINDOW = "window"
    BROWSER = "browser"
    CLIPBOARD = "clipboard"
    FILE = "file"
    SCREEN = "screen"
    TIMING = "timing"
    VISION = "vision"
    SYSTEM = "system"
    EDIT = "edit"
    MACRO = "macro"


@dataclass
class ActionHandler:
    """Represents a registered action handler."""
    name: str
    category: ActionCategory
    description: str
    handler: Callable
    required_params: List[str] = field(default_factory=list)
    optional_params: Dict[str, Any] = field(default_factory=dict)
    returns: Optional[Dict[str, str]] = None
    examples: List[Any] = field(default_factory=list)
    
    def validate_params(self, params: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate parameters for this action.
        
        Args:
            params: Dictionary of parameters to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check required parameters
        for required in self.required_params:
            if required not in params:
                return False, f"Missing required parameter: {required}"
        
        # Check for unknown parameters
        all_params = set(self.required_params) | set(self.optional_params.keys())
        for param in params:
            if param not in all_params:
                return False, f"Unknown parameter: {param}"
        
        return True, None
    
    def get_signature(self) -> str:
        """Get the function signature as a string."""
        params = []
        for param in self.required_params:
            params.append(f"{param}")
        for param, default in self.optional_params.items():
            params.append(f"{param}={default}")
        return f"{self.name}({', '.join(params)})"


class ActionRegistry:
    """
    Registry for all action handlers in the JSON Instruction Protocol.
    
    This class manages the mapping between action names and their handler functions,
    provides parameter validation, and generates documentation.
    """
    
    def __init__(self):
        """Initialize the action registry."""
        self._handlers: Dict[str, ActionHandler] = {}
        self._categories: Dict[ActionCategory, List[str]] = {
            category: [] for category in ActionCategory
        }
        
        # Dependencies (will be injected)
        self.input_controller = None
        self.mouse_controller = None
        self.screen_capture = None
        self.visual_verifier = None
        self.macro_executor = None
    
    def register(
        self,
        name: str,
        category: ActionCategory,
        description: str,
        handler: Callable,
        required_params: Optional[List[str]] = None,
        optional_params: Optional[Dict[str, Any]] = None,
        returns: Optional[Dict[str, str]] = None,
        examples: Optional[List[Any]] = None
    ) -> None:
        """
        Register an action handler.
        
        Args:
            name: Action name (e.g., "press_key")
            category: Action category
            description: Human-readable description
            handler: Callable function to execute the action
            required_params: List of required parameter names
            optional_params: Dict of optional parameters with defaults
            returns: Dict describing return values
            examples: List of example parameter values
        """
        action_handler = ActionHandler(
            name=name,
            category=category,
            description=description,
            handler=handler,
            required_params=required_params or [],
            optional_params=optional_params or {},
            returns=returns,
            examples=examples or []
        )
        
        self._handlers[name] = action_handler
        self._categories[category].append(name)
    
    def execute(self, action_name: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute an action by name with given parameters.
        
        Args:
            action_name: Name of the action to execute
            params: Dictionary of parameters
            
        Returns:
            Result from the action handler
            
        Raises:
            ValueError: If action not found or parameters invalid
        """
        params = params or {}
        
        # Check if action exists
        if action_name not in self._handlers:
            raise ValueError(f"Unknown action: {action_name}")
        
        handler = self._handlers[action_name]
        
        # Validate parameters
        is_valid, error_msg = handler.validate_params(params)
        if not is_valid:
            raise ValueError(f"Invalid parameters for action '{action_name}': {error_msg}")
        
        # Merge with defaults
        final_params = {**handler.optional_params, **params}
        
        # Execute handler
        try:
            return handler.handler(**final_params)
        except Exception as e:
            raise RuntimeError(f"Error executing action '{action_name}': {str(e)}") from e
    
    def get_handler(self, action_name: str) -> Optional[ActionHandler]:
        """Get handler information for an action."""
        return self._handlers.get(action_name)
    
    def list_actions(self, category: Optional[ActionCategory] = None) -> List[str]:
        """
        List all registered actions, optionally filtered by category.
        
        Args:
            category: Optional category filter
            
        Returns:
            List of action names
        """
        if category:
            return self._categories.get(category, [])
        return list(self._handlers.keys())
    
    def generate_documentation(self, category: Optional[ActionCategory] = None) -> str:
        """
        Generate documentation for all actions.
        
        Args:
            category: Optional category filter
            
        Returns:
            Formatted documentation string
        """
        doc_lines = ["# Action Library Documentation\n"]
        
        categories = [category] if category else list(ActionCategory)
        
        for cat in categories:
            actions = self._categories.get(cat, [])
            if not actions:
                continue
            
            doc_lines.append(f"\n## {cat.value.upper()} ACTIONS\n")
            
            for action_name in actions:
                handler = self._handlers[action_name]
                doc_lines.append(f"### {action_name}")
                doc_lines.append(f"\n**Description:** {handler.description}\n")
                doc_lines.append(f"**Signature:** `{handler.get_signature()}`\n")
                
                if handler.required_params:
                    doc_lines.append("**Required Parameters:**")
                    for param in handler.required_params:
                        doc_lines.append(f"- `{param}`")
                    doc_lines.append("")
                
                if handler.optional_params:
                    doc_lines.append("**Optional Parameters:**")
                    for param, default in handler.optional_params.items():
                        doc_lines.append(f"- `{param}` (default: {default})")
                    doc_lines.append("")
                
                if handler.returns:
                    doc_lines.append("**Returns:**")
                    for key, desc in handler.returns.items():
                        doc_lines.append(f"- `{key}`: {desc}")
                    doc_lines.append("")
                
                if handler.examples:
                    doc_lines.append("**Examples:**")
                    for example in handler.examples:
                        doc_lines.append(f"```json\n{example}\n```")
                    doc_lines.append("")
        
        return "\n".join(doc_lines)
    
    def get_action_library_for_ai(self) -> Dict[str, Dict[str, Any]]:
        """
        Generate action library in format suitable for AI prompt.
        
        Returns:
            Dictionary mapping action names to their specifications
        """
        library = {}
        
        for name, handler in self._handlers.items():
            library[name] = {
                "category": handler.category.value,
                "description": handler.description,
                "params": {
                    "required": handler.required_params,
                    "optional": handler.optional_params
                }
            }
            
            if handler.returns:
                library[name]["returns"] = handler.returns
            
            if handler.examples:
                library[name]["examples"] = handler.examples
        
        return library
    
    def inject_dependencies(
        self,
        input_controller=None,
        mouse_controller=None,
        screen_capture=None,
        visual_verifier=None,
        macro_executor=None
    ):
        """
        Inject dependencies needed by action handlers.
        
        Args:
            input_controller: InputController instance
            mouse_controller: MouseController instance
            screen_capture: ScreenCapture instance
            visual_verifier: VisualVerifier instance
            macro_executor: MacroExecutor instance
        """
        self.input_controller = input_controller
        self.mouse_controller = mouse_controller
        self.screen_capture = screen_capture
        self.visual_verifier = visual_verifier
        self.macro_executor = macro_executor
