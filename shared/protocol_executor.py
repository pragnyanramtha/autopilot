"""
Protocol Executor for JSON Instruction Protocol

This module provides the execution engine for the JSON Instruction Protocol,
handling sequential action execution, timing, context management, and control flow.
"""

import time
import threading
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime

from shared.protocol_models import ProtocolSchema, ActionStep
from shared.action_registry import ActionRegistry


@dataclass
class ExecutionContext:
    """
    Maintains state and context during protocol execution.
    Stores results from previous actions and variables for reference.
    """
    protocol_id: str
    start_time: datetime = field(default_factory=datetime.now)
    variables: Dict[str, Any] = field(default_factory=dict)
    action_results: List[Dict[str, Any]] = field(default_factory=list)
    current_action_index: int = 0
    
    def add_result(self, action_name: str, result: Any, error: Optional[str] = None) -> None:
        """Add an action result to the context."""
        self.action_results.append({
            'index': self.current_action_index,
            'action': action_name,
            'result': result,
            'error': error,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_last_result(self) -> Optional[Any]:
        """Get the result from the last executed action."""
        if self.action_results:
            return self.action_results[-1].get('result')
        return None
    
    def set_variable(self, name: str, value: Any) -> None:
        """Set a variable in the execution context."""
        self.variables[name] = value
    
    def get_variable(self, name: str, default: Any = None) -> Any:
        """Get a variable from the execution context."""
        return self.variables.get(name, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary for serialization."""
        return {
            'protocol_id': self.protocol_id,
            'start_time': self.start_time.isoformat(),
            'variables': self.variables,
            'action_results': self.action_results,
            'current_action_index': self.current_action_index
        }


@dataclass
class ExecutionError:
    """Structured error information for protocol execution."""
    action_index: int
    action_name: str
    error_type: str
    error_message: str
    timestamp: str
    params: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            'action_index': self.action_index,
            'action_name': self.action_name,
            'error_type': self.error_type,
            'error_message': self.error_message,
            'timestamp': self.timestamp
        }
        if self.params:
            result['params'] = self.params
        return result


@dataclass
class ExecutionResult:
    """Result of protocol execution."""
    protocol_id: str
    status: str  # 'success', 'failed', 'stopped', 'paused'
    actions_completed: int
    total_actions: int
    duration_ms: int
    error: Optional[str] = None
    error_details: Optional[ExecutionError] = None
    context: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            'protocol_id': self.protocol_id,
            'status': self.status,
            'actions_completed': self.actions_completed,
            'total_actions': self.total_actions,
            'duration_ms': self.duration_ms
        }
        if self.error:
            result['error'] = self.error
        if self.error_details:
            result['error_details'] = self.error_details.to_dict()
        if self.context:
            result['context'] = self.context
        return result


class ProtocolExecutor:
    """
    Executes JSON Instruction Protocols with support for:
    - Sequential action execution
    - Execution context management
    - Timing control (wait_after_ms)
    - Pause/resume/stop controls
    - Error handling and recovery
    - Macro execution with variable substitution
    
    Requirements:
    - 4.1: Sequential action execution
    - 4.2: Execution context management
    - 4.3: Timing control
    - 4.4: Pause/resume/stop controls
    - 10.1: Context and state management
    - 10.2: Result storage and retrieval
    """
    
    def __init__(self, action_registry: ActionRegistry, dry_run: bool = False):
        """
        Initialize the protocol executor.
        
        Args:
            action_registry: ActionRegistry instance with registered handlers
            dry_run: If True, simulate execution without performing actions
        """
        self.action_registry = action_registry
        self.dry_run = dry_run
        
        # Execution state
        self._is_running = False
        self._is_paused = False
        self._should_stop = False
        self._current_protocol: Optional[ProtocolSchema] = None
        self._current_context: Optional[ExecutionContext] = None
        self._current_error: Optional[ExecutionError] = None
        
        # Thread lock for state management
        self._lock = threading.Lock()
    
    def execute_protocol(self, protocol: ProtocolSchema) -> ExecutionResult:
        """
        Execute a complete protocol sequentially.
        
        Args:
            protocol: The protocol to execute
            
        Returns:
            ExecutionResult with execution status and details
            
        Requirements:
        - 4.1: Execute actions in sequence
        - 4.2: Maintain execution context
        - 4.3: Respect wait_after_ms timing
        - 4.4: Support pause/resume/stop
        """
        with self._lock:
            if self._is_running:
                return ExecutionResult(
                    protocol_id=protocol.metadata.description,
                    status='failed',
                    actions_completed=0,
                    total_actions=len(protocol.actions),
                    duration_ms=0,
                    error='Another protocol is already running'
                )
            
            self._is_running = True
            self._should_stop = False
            self._is_paused = False
            self._current_protocol = protocol
            self._current_context = ExecutionContext(
                protocol_id=protocol.metadata.description
            )
            self._current_error = None
        
        start_time = time.time()
        actions_completed = 0
        error_message = None
        
        try:
            print(f"{'[DRY RUN] ' if self.dry_run else ''}Starting protocol: {protocol.metadata.description}")
            print(f"Total actions: {len(protocol.actions)}")
            print(f"Complexity: {protocol.metadata.complexity}")
            
            # Execute each action sequentially
            for i, action in enumerate(protocol.actions):
                self._current_context.current_action_index = i
                
                # Check for stop signal
                if self._should_stop:
                    error_message = 'Execution stopped by user'
                    break
                
                # Handle pause
                while self._is_paused and not self._should_stop:
                    time.sleep(0.1)
                
                if self._should_stop:
                    error_message = 'Execution stopped by user'
                    break
                
                # Execute the action
                print(f"{'[DRY RUN] ' if self.dry_run else ''}[{i + 1}/{len(protocol.actions)}] Executing: {action.action}")
                if action.description:
                    print(f"  Description: {action.description}")
                
                try:
                    result = self._execute_action(action)
                    self._current_context.add_result(action.action, result)
                    actions_completed += 1
                    
                    # Apply wait_after_ms timing
                    if action.wait_after_ms > 0:
                        wait_seconds = action.wait_after_ms / 1000.0
                        if self.dry_run:
                            print(f"  [DRY RUN] Would wait {action.wait_after_ms}ms")
                        else:
                            time.sleep(wait_seconds)
                    
                except Exception as action_error:
                    # Create structured error information
                    error_details = ExecutionError(
                        action_index=i,
                        action_name=action.action,
                        error_type=type(action_error).__name__,
                        error_message=str(action_error),
                        timestamp=datetime.now().isoformat(),
                        params=action.params
                    )
                    
                    error_message = f"Action {i + 1} ({action.action}) failed: {str(action_error)}"
                    self._current_context.add_result(action.action, None, error=str(action_error))
                    print(f"  ERROR: {error_message}")
                    
                    # Store error details for result
                    self._current_error = error_details
                    break
            
            # Determine final status
            if error_message:
                status = 'stopped' if 'stopped' in error_message else 'failed'
            elif actions_completed == len(protocol.actions):
                status = 'success'
                print(f"{'[DRY RUN] ' if self.dry_run else ''}Protocol completed successfully!")
            else:
                status = 'failed'
                error_message = 'Protocol incomplete'
        
        except Exception as e:
            status = 'failed'
            error_message = f"Protocol execution error: {str(e)}"
            print(f"FATAL ERROR: {error_message}")
        
        finally:
            with self._lock:
                self._is_running = False
                context_dict = self._current_context.to_dict() if self._current_context else None
                error_details = self._current_error
                self._current_protocol = None
                self._current_context = None
                self._current_error = None
        
        duration_ms = int((time.time() - start_time) * 1000)
        
        return ExecutionResult(
            protocol_id=protocol.metadata.description,
            status=status,
            actions_completed=actions_completed,
            total_actions=len(protocol.actions),
            duration_ms=duration_ms,
            error=error_message,
            error_details=error_details,
            context=context_dict
        )
    
    def _execute_action(self, action: ActionStep) -> Any:
        """
        Execute a single action step.
        
        Args:
            action: The action to execute
            
        Returns:
            Result from the action handler
            
        Raises:
            Exception: If action execution fails
            
        Requirements:
        - 11.5: Parse AI vision response
        - 11.6: Extract updated coordinates
        - 11.7: Update execution context
        - 12.4: Resume with adapted parameters
        """
        # Handle macro actions specially (will be implemented in task 4.2)
        if action.action == 'macro':
            return self._execute_macro_action(action)
        
        # Substitute variables in parameters
        params = self._substitute_variables(action.params)
        
        # Log parameters
        if params:
            print(f"  Parameters: {params}")
        
        # Execute action via registry
        if self.dry_run:
            print(f"  [DRY RUN] Would execute: {action.action}({params})")
            return None
        else:
            result = self.action_registry.execute(action.action, params)
            
            # Handle visual verification results
            if action.action == 'verify_screen' and isinstance(result, dict):
                self._handle_verification_result(result)
            
            return result
    
    def _handle_verification_result(self, result: Dict[str, Any]) -> None:
        """
        Handle visual verification result and update execution context.
        
        This method:
        1. Checks if verification was successful (safe_to_proceed)
        2. Extracts updated coordinates if provided
        3. Updates execution context variables for use in subsequent actions
        
        Args:
            result: Verification result dictionary from VisualVerifier
            
        Requirements:
        - 11.5: Parse safe_to_proceed vs requires_adaptation
        - 11.6: Extract updated coordinates from AI response
        - 11.7: Update execution context with new coordinates
        - 12.4: Resume execution with adapted parameters
        """
        if not self._current_context:
            return
        
        # Check if verification was successful
        safe_to_proceed = result.get('safe_to_proceed', False)
        confidence = result.get('confidence', 0.0)
        analysis = result.get('analysis', '')
        
        if not safe_to_proceed:
            # Verification failed - log warning but continue
            # (The calling code can decide whether to stop based on the result)
            print(f"  ⚠ Verification Warning: Not safe to proceed")
            print(f"    Analysis: {analysis}")
            print(f"    Confidence: {confidence:.2f}")
        
        # Extract and store updated coordinates in context
        updated_coordinates = result.get('updated_coordinates')
        if updated_coordinates:
            x = updated_coordinates.get('x')
            y = updated_coordinates.get('y')
            
            if x is not None and y is not None:
                # Store coordinates as context variables
                # These can be referenced in subsequent actions using {{verified_x}} and {{verified_y}}
                self._current_context.set_variable('verified_x', x)
                self._current_context.set_variable('verified_y', y)
                
                print(f"  ✓ Updated coordinates stored: x={x}, y={y}")
                print(f"    Use {{{{verified_x}}}} and {{{{verified_y}}}} in subsequent actions")
        
        # Store suggested actions if provided
        suggested_actions = result.get('suggested_actions')
        if suggested_actions:
            self._current_context.set_variable('suggested_actions', suggested_actions)
            print(f"  ℹ Suggested actions: {suggested_actions}")
        
        # Store verification metadata
        self._current_context.set_variable('last_verification_safe', safe_to_proceed)
        self._current_context.set_variable('last_verification_confidence', confidence)
        self._current_context.set_variable('last_verification_analysis', analysis)
    
    def _execute_macro_action(self, action: ActionStep) -> Any:
        """
        Execute a macro action with variable substitution.
        
        Args:
            action: The macro action to execute
            
        Returns:
            Result from macro execution
            
        Requirements:
        - 7.1: Macro execution with variable substitution
        """
        if not self._current_protocol:
            raise RuntimeError("Cannot execute macro without active protocol")
        
        # Get macro name
        macro_name = action.params.get('name')
        if not macro_name:
            raise ValueError("Macro action must specify 'name' parameter")
        
        # Get macro definition
        if macro_name not in self._current_protocol.macros:
            raise ValueError(f"Macro '{macro_name}' not defined in protocol")
        
        macro = self._current_protocol.macros[macro_name]
        
        # Get variables for substitution
        macro_vars = action.params.get('vars', {})
        
        print(f"  Executing macro: {macro_name}")
        if macro_vars:
            print(f"  Variables: {macro_vars}")
        
        # Execute each action in the macro
        results = []
        for i, macro_action in enumerate(macro.actions):
            # Substitute variables in macro action parameters
            substituted_params = self._substitute_variables_in_dict(
                macro_action.params,
                macro_vars
            )
            
            # Create a new action with substituted parameters
            substituted_action = ActionStep(
                action=macro_action.action,
                params=substituted_params,
                wait_after_ms=macro_action.wait_after_ms,
                description=macro_action.description
            )
            
            # Check for nested macro calls
            if substituted_action.action == 'macro':
                # Recursive macro execution
                result = self._execute_macro_action(substituted_action)
            else:
                # Execute regular action
                print(f"    [{i + 1}/{len(macro.actions)}] {substituted_action.action}")
                if substituted_params:
                    print(f"      Parameters: {substituted_params}")
                
                if self.dry_run:
                    print(f"      [DRY RUN] Would execute: {substituted_action.action}({substituted_params})")
                    result = None
                else:
                    result = self.action_registry.execute(
                        substituted_action.action,
                        substituted_params
                    )
            
            results.append(result)
            
            # Apply wait_after_ms timing
            if substituted_action.wait_after_ms > 0:
                wait_seconds = substituted_action.wait_after_ms / 1000.0
                if self.dry_run:
                    print(f"      [DRY RUN] Would wait {substituted_action.wait_after_ms}ms")
                else:
                    time.sleep(wait_seconds)
        
        return results
    
    def _substitute_variables(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Substitute variables in parameters using execution context.
        
        This method substitutes:
        1. Context variables (from execution context)
        2. Special variables like {{verified_x}}, {{verified_y}} from visual verification
        
        Args:
            params: Parameters that may contain variable references
            
        Returns:
            Parameters with variables substituted
            
        Requirements:
        - 7.1: Variable substitution
        """
        if not self._current_context:
            return params.copy()
        
        return self._substitute_variables_in_dict(params, self._current_context.variables)
    
    def _substitute_variables_in_dict(
        self,
        data: Dict[str, Any],
        variables: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Recursively substitute variables in a dictionary.
        
        Variables are specified using {{variable_name}} syntax.
        
        Args:
            data: Dictionary that may contain variable references
            variables: Dictionary of variable values
            
        Returns:
            Dictionary with variables substituted
            
        Raises:
            ValueError: If a required variable is not found in context
            
        Requirements:
        - 7.1: Variable substitution with {{var}} syntax
        """
        import re
        
        result = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                # Substitute variables in string values
                # Pattern: {{variable_name}}
                pattern = r'\{\{(\w+)\}\}'
                
                # Check if there are any variables to substitute
                matches = re.findall(pattern, value)
                if matches:
                    # Check if all variables exist
                    missing_vars = [var for var in matches if var not in variables]
                    if missing_vars:
                        raise ValueError(
                            f"Missing required variables in context: {', '.join(missing_vars)}. "
                            f"Available variables: {', '.join(variables.keys()) if variables else 'none'}. "
                            f"Hint: Variables like 'verified_x' and 'verified_y' come from 'verify_screen' action results."
                        )
                    
                    # Special case: if the entire value is a single variable, return the actual value (preserving type)
                    if len(matches) == 1 and value == f"{{{{{matches[0]}}}}}":
                        result[key] = variables[matches[0]]
                        continue
                
                def replace_var(match):
                    var_name = match.group(1)
                    return str(variables[var_name])
                
                result[key] = re.sub(pattern, replace_var, value)
                
            elif isinstance(value, dict):
                # Recursively substitute in nested dictionaries
                result[key] = self._substitute_variables_in_dict(value, variables)
                
            elif isinstance(value, list):
                # Substitute in list items
                result[key] = [
                    self._substitute_variables_in_dict({'item': item}, variables)['item']
                    if isinstance(item, (dict, str)) else item
                    for item in value
                ]
            else:
                # Keep other types as-is
                result[key] = value
        
        return result
    
    def pause_execution(self) -> bool:
        """
        Pause the currently running protocol.
        
        Returns:
            True if paused successfully, False if not running
            
        Requirements: 4.4 - Pause control
        """
        with self._lock:
            if self._is_running and not self._is_paused:
                self._is_paused = True
                print("Execution paused")
                return True
            return False
    
    def resume_execution(self) -> bool:
        """
        Resume a paused protocol.
        
        Returns:
            True if resumed successfully, False if not paused
            
        Requirements: 4.4 - Resume control
        """
        with self._lock:
            if self._is_running and self._is_paused:
                self._is_paused = False
                print("Execution resumed")
                return True
            return False
    
    def stop_execution(self) -> bool:
        """
        Stop the currently running protocol (emergency stop).
        
        Returns:
            True if stop signal sent, False if not running
            
        Requirements: 4.4 - Stop control
        """
        with self._lock:
            if self._is_running:
                self._should_stop = True
                self._is_paused = False  # Unpause if paused
                print("Emergency stop triggered!")
                return True
            return False
    
    def get_execution_status(self) -> Dict[str, Any]:
        """
        Get the current execution status.
        
        Returns:
            Dictionary with execution state information
            
        Requirements: 10.2 - State retrieval
        """
        with self._lock:
            status = {
                'is_running': self._is_running,
                'is_paused': self._is_paused,
                'dry_run': self.dry_run
            }
            
            if self._current_protocol:
                status['protocol_id'] = self._current_protocol.metadata.description
                status['current_action'] = self._current_context.current_action_index + 1
                status['total_actions'] = len(self._current_protocol.actions)
            
            return status
    
    def is_running(self) -> bool:
        """Check if a protocol is currently executing."""
        with self._lock:
            return self._is_running
    
    def get_context(self) -> Optional[Dict[str, Any]]:
        """
        Get the current execution context.
        
        Returns:
            Current context as dictionary, or None if not running
            
        Requirements: 10.2 - Context retrieval
        """
        with self._lock:
            if self._current_context:
                return self._current_context.to_dict()
            return None
    
    def get_last_error(self) -> Optional[Dict[str, Any]]:
        """
        Get the last error that occurred during execution.
        
        Returns:
            Error details as dictionary, or None if no error
            
        Requirements: 4.5 - Error information retrieval
        """
        with self._lock:
            if self._current_error:
                return self._current_error.to_dict()
            return None
