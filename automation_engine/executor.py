"""
Automation executor module with safety controls.
Executes workflows with pause/resume/stop functionality and safety checks.
"""

import time
import threading
from typing import Optional
from datetime import datetime

from shared.data_models import Workflow, WorkflowStep, ExecutionResult
from automation_engine.input_controller import InputController
from automation_engine.screen_capture import ScreenCapture


class AutomationExecutor:
    """
    Main executor for automation workflows with safety controls.
    
    Requirements:
    - 4.4: Respect timing delays between actions
    - 4.5: Report errors and halt execution on failure
    - 4.6: Provide real-time feedback on progress
    - 7.1: Provide emergency stop mechanism
    - 7.2: Require confirmation for dangerous actions
    - 7.3: Implement dry-run mode for testing
    """
    
    # Dangerous action patterns that require confirmation
    DANGEROUS_ACTIONS = {
        'delete', 'remove', 'format', 'shutdown', 'restart', 
        'kill', 'terminate', 'rm ', 'del ', 'rmdir'
    }
    
    def __init__(self, dry_run: bool = False):
        """
        Initialize the automation executor.
        
        Args:
            dry_run: If True, simulate execution without performing actual actions
        """
        self.input_controller = InputController()
        self.screen_capture = ScreenCapture()
        self.dry_run = dry_run
        
        # Execution state
        self._is_running = False
        self._is_paused = False
        self._should_stop = False
        self._current_workflow: Optional[Workflow] = None
        self._current_step_index = 0
        
        # Thread lock for state management
        self._lock = threading.Lock()
        
        # Mouse position monitoring for safety
        self._initial_mouse_pos: Optional[tuple[int, int]] = None
        self._mouse_move_threshold = 50  # pixels
    
    def execute_workflow(self, workflow: Workflow) -> ExecutionResult:
        """
        Execute a complete workflow sequentially.
        
        Args:
            workflow: The workflow to execute
            
        Returns:
            ExecutionResult with execution status and details
            
        Requirements:
        - 4.4: Execute workflows respecting timing delays
        - 4.5: Report errors and halt on failure
        - 4.6: Provide real-time feedback
        """
        with self._lock:
            if self._is_running:
                return ExecutionResult(
                    workflow_id=workflow.id,
                    status="failed",
                    steps_completed=0,
                    error="Another workflow is already running",
                    duration_ms=0
                )
            
            self._is_running = True
            self._should_stop = False
            self._is_paused = False
            self._current_workflow = workflow
            self._current_step_index = 0
        
        start_time = time.time()
        steps_completed = 0
        error_message = None
        
        try:
            # Store initial mouse position for safety monitoring
            self._initial_mouse_pos = self.input_controller.get_mouse_position()
            
            print(f"{'[DRY RUN] ' if self.dry_run else ''}Starting workflow: {workflow.id}")
            print(f"Total steps: {len(workflow.steps)}")
            
            # Execute each step sequentially
            for i, step in enumerate(workflow.steps):
                self._current_step_index = i
                
                # Check for stop signal
                if self._should_stop:
                    error_message = "Execution stopped by user"
                    break
                
                # Handle pause
                while self._is_paused and not self._should_stop:
                    time.sleep(0.1)
                
                if self._should_stop:
                    error_message = "Execution stopped by user"
                    break
                
                # Check for user mouse movement (safety feature)
                if self._check_user_interrupt():
                    error_message = "Execution interrupted: user moved mouse"
                    break
                
                # Execute the step
                print(f"{'[DRY RUN] ' if self.dry_run else ''}Executing step {i + 1}/{len(workflow.steps)}: {step.type}")
                
                try:
                    self._execute_step(step)
                    steps_completed += 1
                    
                    # Apply delay after step execution
                    if step.delay_ms > 0:
                        time.sleep(step.delay_ms / 1000.0)
                    
                except Exception as step_error:
                    error_message = f"Step {i + 1} failed: {str(step_error)}"
                    print(f"Error: {error_message}")
                    break
            
            # Determine final status
            if error_message:
                status = "interrupted" if "stopped" in error_message or "interrupted" in error_message else "failed"
            elif steps_completed == len(workflow.steps):
                status = "success"
                print(f"{'[DRY RUN] ' if self.dry_run else ''}Workflow completed successfully!")
            else:
                status = "failed"
                error_message = "Workflow incomplete"
            
        except Exception as e:
            status = "failed"
            error_message = f"Workflow execution error: {str(e)}"
            print(f"Fatal error: {error_message}")
        
        finally:
            with self._lock:
                self._is_running = False
                self._current_workflow = None
                self._current_step_index = 0
        
        duration_ms = int((time.time() - start_time) * 1000)
        
        return ExecutionResult(
            workflow_id=workflow.id,
            status=status,
            steps_completed=steps_completed,
            error=error_message,
            duration_ms=duration_ms
        )
    
    def _execute_step(self, step: WorkflowStep) -> None:
        """
        Execute a single workflow step.
        
        Args:
            step: The workflow step to execute
            
        Raises:
            ValueError: If step type is unknown or parameters are invalid
        """
        # Validate dangerous actions
        if step.type == "type" and step.data:
            if self._is_dangerous_action(step.data):
                if not self.dry_run:
                    raise ValueError(
                        f"Dangerous action detected: '{step.data}'. "
                        "This action requires explicit user confirmation."
                    )
                else:
                    print(f"[DRY RUN] Would block dangerous action: {step.data}")
        
        # Execute based on step type
        if step.type == "mouse_move":
            self._execute_mouse_move(step)
        
        elif step.type == "click":
            self._execute_click(step)
        
        elif step.type == "type":
            self._execute_type(step)
        
        elif step.type == "press_key":
            self._execute_press_key(step)
        
        elif step.type == "hotkey":
            self._execute_hotkey(step)
        
        elif step.type == "wait":
            self._execute_wait(step)
        
        elif step.type == "capture":
            self._execute_capture(step)
        
        else:
            raise ValueError(f"Unknown step type: {step.type}")
    
    def _execute_mouse_move(self, step: WorkflowStep) -> None:
        """Execute a mouse move step."""
        if not step.coordinates:
            raise ValueError("Mouse move requires coordinates")
        
        x, y = step.coordinates
        
        if self.dry_run:
            print(f"  [DRY RUN] Would move mouse to ({x}, {y})")
        else:
            self.input_controller.move_mouse(x, y)
    
    def _execute_click(self, step: WorkflowStep) -> None:
        """Execute a mouse click step."""
        button = step.validation.get('button', 'left') if step.validation else 'left'
        clicks = step.validation.get('clicks', 1) if step.validation else 1
        
        if self.dry_run:
            coord_str = f" at {step.coordinates}" if step.coordinates else ""
            print(f"  [DRY RUN] Would {button}-click{coord_str} ({clicks}x)")
        else:
            if step.coordinates:
                x, y = step.coordinates
                self.input_controller.click(x, y, button=button, clicks=clicks)
            else:
                self.input_controller.click(button=button, clicks=clicks)
    
    def _execute_type(self, step: WorkflowStep) -> None:
        """Execute a keyboard typing step."""
        if not step.data:
            raise ValueError("Type step requires data")
        
        interval = step.validation.get('interval', 0.05) if step.validation else 0.05
        
        if self.dry_run:
            print(f"  [DRY RUN] Would type: '{step.data}'")
        else:
            self.input_controller.type_text(step.data, interval=interval)
    
    def _execute_press_key(self, step: WorkflowStep) -> None:
        """Execute a key press step."""
        if not step.data:
            raise ValueError("Press key step requires data (key name)")
        
        if self.dry_run:
            print(f"  [DRY RUN] Would press key: '{step.data}'")
        else:
            self.input_controller.press_key(step.data)
    
    def _execute_hotkey(self, step: WorkflowStep) -> None:
        """Execute a hotkey combination step."""
        if not step.data:
            raise ValueError("Hotkey step requires data (comma-separated keys)")
        
        keys = [k.strip() for k in step.data.split(',')]
        
        if self.dry_run:
            print(f"  [DRY RUN] Would press hotkey: {' + '.join(keys)}")
        else:
            self.input_controller.hotkey(*keys)
    
    def _execute_wait(self, step: WorkflowStep) -> None:
        """Execute a wait/delay step."""
        wait_ms = step.delay_ms if step.delay_ms > 0 else 1000
        
        if self.dry_run:
            print(f"  [DRY RUN] Would wait {wait_ms}ms")
        else:
            time.sleep(wait_ms / 1000.0)
    
    def _execute_capture(self, step: WorkflowStep) -> None:
        """Execute a screen capture step."""
        if self.dry_run:
            if step.coordinates:
                print(f"  [DRY RUN] Would capture region at {step.coordinates}")
            else:
                print(f"  [DRY RUN] Would capture full screen")
        else:
            if step.coordinates and len(step.coordinates) == 4:
                x, y, width, height = step.coordinates
                self.screen_capture.capture_region(x, y, width, height)
            else:
                self.screen_capture.capture_screen()
    
    def _is_dangerous_action(self, text: str) -> bool:
        """
        Check if text contains dangerous action keywords.
        
        Args:
            text: Text to check
            
        Returns:
            True if dangerous action detected
            
        Requirements: 7.2 - Require confirmation for dangerous actions
        """
        text_lower = text.lower()
        return any(dangerous in text_lower for dangerous in self.DANGEROUS_ACTIONS)
    
    def _check_user_interrupt(self) -> bool:
        """
        Check if user has moved the mouse significantly (safety feature).
        
        Returns:
            True if user interrupt detected
            
        Requirements: 7.1 - Emergency stop mechanism
        """
        if not self._initial_mouse_pos or self.dry_run:
            return False
        
        current_pos = self.input_controller.get_mouse_position()
        dx = abs(current_pos[0] - self._initial_mouse_pos[0])
        dy = abs(current_pos[1] - self._initial_mouse_pos[1])
        
        # If mouse moved significantly, consider it an interrupt
        return (dx > self._mouse_move_threshold or dy > self._mouse_move_threshold)
    
    def pause_execution(self) -> bool:
        """
        Pause the currently running workflow.
        
        Returns:
            True if paused successfully, False if not running
            
        Requirements: 7.1 - Pause/resume controls
        """
        with self._lock:
            if self._is_running and not self._is_paused:
                self._is_paused = True
                print("Execution paused")
                return True
            return False
    
    def resume_execution(self) -> bool:
        """
        Resume a paused workflow.
        
        Returns:
            True if resumed successfully, False if not paused
            
        Requirements: 7.1 - Pause/resume controls
        """
        with self._lock:
            if self._is_running and self._is_paused:
                self._is_paused = False
                print("Execution resumed")
                return True
            return False
    
    def stop_execution(self) -> bool:
        """
        Stop the currently running workflow (emergency stop).
        
        Returns:
            True if stop signal sent, False if not running
            
        Requirements: 7.1 - Emergency stop mechanism
        """
        with self._lock:
            if self._is_running:
                self._should_stop = True
                self._is_paused = False  # Unpause if paused
                print("Emergency stop triggered!")
                return True
            return False
    
    def get_execution_status(self) -> dict:
        """
        Get the current execution status.
        
        Returns:
            Dictionary with execution state information
            
        Requirements: 4.6 - Provide real-time feedback
        """
        with self._lock:
            return {
                'is_running': self._is_running,
                'is_paused': self._is_paused,
                'workflow_id': self._current_workflow.id if self._current_workflow else None,
                'current_step': self._current_step_index + 1 if self._current_workflow else 0,
                'total_steps': len(self._current_workflow.steps) if self._current_workflow else 0,
                'dry_run': self.dry_run
            }
    
    def is_running(self) -> bool:
        """Check if a workflow is currently executing."""
        with self._lock:
            return self._is_running
