"""
AI Vision Navigator for intelligent screen interaction.

This module provides vision-based navigation capabilities, allowing the AI to
analyze screenshots and determine optimal mouse coordinates and actions.
"""

from dataclasses import dataclass
from typing import Optional, Tuple, List
from datetime import datetime, timezone
import json
import os
import re
import time
from PIL import Image


@dataclass
class VisionNavigationResult:
    """Result from vision analysis of a screenshot.
    
    Attributes:
        action: Type of action to perform ('click', 'double_click', 'right_click', 
                'type', 'no_action', 'complete')
        coordinates: Target (x, y) coordinates for mouse action, None if no action needed
        confidence: Confidence score from 0.0 to 1.0 indicating AI's certainty
        reasoning: AI's explanation for the chosen action and coordinates
        requires_followup: Whether to capture a new screenshot after executing this action
        text_to_type: Text content to type (only used when action is 'type')
    """
    action: str
    coordinates: Optional[Tuple[int, int]]
    confidence: float
    reasoning: str
    requires_followup: bool
    text_to_type: Optional[str] = None
    
    def __post_init__(self):
        """Validate the result data."""
        valid_actions = {'click', 'double_click', 'right_click', 'type', 'no_action', 'complete'}
        if self.action not in valid_actions:
            raise ValueError(f"Invalid action '{self.action}'. Must be one of {valid_actions}")
        
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {self.confidence}")
        
        if self.action in {'click', 'double_click', 'right_click'} and self.coordinates is None:
            raise ValueError(f"Action '{self.action}' requires coordinates")
        
        if self.action == 'type' and not self.text_to_type:
            raise ValueError("Action 'type' requires text_to_type")


@dataclass
class VisualNavigationAuditEntry:
    """Audit log entry for visual navigation actions.
    
    This dataclass captures all relevant information about a visual navigation
    action for debugging, compliance, and analysis purposes.
    
    Attributes:
        timestamp: ISO format timestamp when the action occurred
        request_id: Unique identifier for the navigation request
        iteration: Current iteration number in the navigation workflow
        task_description: Description of the task being performed
        screenshot_path: File path where the screenshot was saved
        mouse_position_before: (x, y) coordinates before the action
        action_taken: Type of action executed
        coordinates: Target (x, y) coordinates for the action
        confidence: AI's confidence score for this action
        reasoning: AI's explanation for choosing this action
        status: Execution status ('success', 'error', 'skipped')
        error: Error message if status is 'error', None otherwise
    """
    timestamp: str
    request_id: str
    iteration: int
    task_description: str
    screenshot_path: str
    mouse_position_before: Tuple[int, int]
    action_taken: str
    coordinates: Optional[Tuple[int, int]]
    confidence: float
    reasoning: str
    status: str
    error: Optional[str] = None
    
    def __post_init__(self):
        """Validate the audit entry data."""
        valid_statuses = {'success', 'error', 'skipped'}
        if self.status not in valid_statuses:
            raise ValueError(f"Invalid status '{self.status}'. Must be one of {valid_statuses}")
        
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {self.confidence}")
    
    @classmethod
    def create(
        cls,
        request_id: str,
        iteration: int,
        task_description: str,
        screenshot_path: str,
        mouse_position_before: Tuple[int, int],
        action_taken: str,
        coordinates: Optional[Tuple[int, int]],
        confidence: float,
        reasoning: str,
        status: str,
        error: Optional[str] = None
    ) -> 'VisualNavigationAuditEntry':
        """Factory method to create an audit entry with automatic timestamp.
        
        Args:
            request_id: Unique identifier for the navigation request
            iteration: Current iteration number
            task_description: Description of the task
            screenshot_path: Path to saved screenshot
            mouse_position_before: Mouse position before action
            action_taken: Type of action executed
            coordinates: Target coordinates
            confidence: AI confidence score
            reasoning: AI's reasoning
            status: Execution status
            error: Optional error message
            
        Returns:
            New VisualNavigationAuditEntry instance
        """
        return cls(
            timestamp=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            request_id=request_id,
            iteration=iteration,
            task_description=task_description,
            screenshot_path=screenshot_path,
            mouse_position_before=mouse_position_before,
            action_taken=action_taken,
            coordinates=coordinates,
            confidence=confidence,
            reasoning=reasoning,
            status=status,
            error=error
        )
    
    def to_dict(self) -> dict:
        """Convert audit entry to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the audit entry
        """
        return {
            'timestamp': self.timestamp,
            'request_id': self.request_id,
            'iteration': self.iteration,
            'task_description': self.task_description,
            'screenshot_path': self.screenshot_path,
            'mouse_position_before': list(self.mouse_position_before),
            'action_taken': self.action_taken,
            'coordinates': list(self.coordinates) if self.coordinates else None,
            'confidence': self.confidence,
            'reasoning': self.reasoning,
            'status': self.status,
            'error': self.error
        }



class VisionNavigator:
    """Handles vision-based navigation using AI to analyze screenshots and determine actions.
    
    This class uses Gemini's vision capabilities to intelligently analyze screen content
    and determine optimal mouse coordinates and actions for automation tasks.
    
    Attributes:
        gemini_client: GeminiClient instance for vision model API calls
        config: Configuration dictionary with vision navigation settings
        vision_model: Name of the vision model to use
        max_iterations: Maximum number of iterations allowed in a workflow
        confidence_threshold: Minimum confidence score to accept an action
        enable_audit_log: Whether to save audit logs
        audit_log_path: Path to save audit log entries
        critical_keywords: List of keywords that trigger confirmation prompts
    """
    
    def __init__(self, gemini_client, config: dict):
        """Initialize VisionNavigator with Gemini client and configuration.
        
        Args:
            gemini_client: GeminiClient instance for making vision API calls
            config: Configuration dictionary containing visual_navigation settings
                Expected keys:
                - vision_model: Model name for vision analysis (default: gemini-2.0-flash-exp)
                - vision_model_dev: Model for dev mode (default: gemini-2.0-flash-exp)
                - max_iterations: Max workflow iterations (default: 10)
                - confidence_threshold: Min confidence to accept action (default: 0.6)
                - enable_audit_log: Whether to log actions (default: True)
                - audit_log_path: Path for audit logs (default: logs/visual_navigation_audit.json)
                - critical_keywords: List of keywords requiring confirmation
                - loop_detection_threshold: Number of repeated clicks to detect loop (default: 3)
                - loop_detection_buffer_size: Size of action history buffer (default: 10)
        """
        self.gemini_client = gemini_client
        self.config = config
        
        # Extract configuration with defaults
        visual_nav_config = config.get('visual_navigation', {})
        
        # Determine which vision model to use based on mode
        if gemini_client.use_ultra_fast:
            # Dev mode: use dev vision model
            self.vision_model = visual_nav_config.get('vision_model_dev', 'gemini-2.0-flash-exp')
        else:
            # Normal mode: use standard vision model
            self.vision_model = visual_nav_config.get('vision_model', 'gemini-2.0-flash-exp')
        
        self.max_iterations = visual_nav_config.get('max_iterations', 10)
        self.confidence_threshold = visual_nav_config.get('confidence_threshold', 0.6)
        self.enable_audit_log = visual_nav_config.get('enable_audit_log', True)
        self.audit_log_path = visual_nav_config.get('audit_log_path', 'logs/visual_navigation_audit.json')
        self.critical_keywords = visual_nav_config.get('critical_keywords', [
            'delete', 'format', 'shutdown', 'remove', 'erase', 'destroy', 'wipe'
        ])
        
        # Loop detection configuration
        self.loop_detection_threshold = visual_nav_config.get('loop_detection_threshold', 3)
        self.loop_detection_buffer_size = visual_nav_config.get('loop_detection_buffer_size', 10)
        
        # Initialize action history buffer for loop detection (circular buffer)
        self.action_history = []
        
        # Retry configuration
        self.max_retries = 3
        self.retry_base_delay = 1.0  # Base delay in seconds for exponential backoff
        
        # Initialize audit log directory if enabled
        if self.enable_audit_log:
            os.makedirs(os.path.dirname(self.audit_log_path), exist_ok=True)
            
        print(f"  VisionNavigator initialized with model: {self.vision_model}")
        print(f"  Max iterations: {self.max_iterations}, Confidence threshold: {self.confidence_threshold}")
        print(f"  Loop detection: threshold={self.loop_detection_threshold}, buffer_size={self.loop_detection_buffer_size}")
        print(f"  Retry configuration: max_retries={self.max_retries}, base_delay={self.retry_base_delay}s")
    
    def _call_vision_api_with_retry(self, prompt: str, *images) -> str:
        """Call vision API with retry logic and exponential backoff.
        
        Implements exponential backoff for vision API calls.
        Retries up to 3 times on failure.
        Logs retry attempts.
        
        Args:
            prompt: Text prompt for the vision model
            *images: Variable number of PIL Image objects to analyze
            
        Returns:
            Response text from the vision model
            
        Raises:
            Exception: If all retries fail
            
        Requirements: 6.5
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                # Prepare content list with prompt and images
                content = [prompt] + list(images)
                
                # Call vision model
                response = self.gemini_client.vision_model.generate_content(content)
                
                # Check if response was blocked
                if not response.candidates or not response.candidates[0].content.parts:
                    raise Exception("Response blocked by safety filters")
                
                # Success - return response text
                if attempt > 0:
                    print(f"  ✓ Vision API call succeeded on attempt {attempt + 1}")
                return response.text
                
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_retries - 1:
                    # Calculate exponential backoff delay
                    delay = self.retry_base_delay * (2 ** attempt)
                    print(f"  ⚠ Vision API call failed (attempt {attempt + 1}/{self.max_retries}): {str(e)}")
                    print(f"  ⏳ Retrying in {delay:.1f} seconds...")
                    time.sleep(delay)
                else:
                    # Final attempt failed
                    print(f"  ✗ Vision API call failed after {self.max_retries} attempts: {str(e)}")
        
        # All retries exhausted
        raise last_exception
    
    def analyze_screen_for_action(
        self,
        screenshot: Image.Image,
        current_mouse_pos: Tuple[int, int],
        task_description: str,
        screen_size: Tuple[int, int]
    ) -> VisionNavigationResult:
        """Analyze a screenshot and determine the next action to take.
        
        This method sends the screenshot to the vision model along with context about
        the current task and mouse position, then parses the AI's response to extract
        the recommended action, coordinates, and confidence level.
        
        Args:
            screenshot: PIL Image of the current screen
            current_mouse_pos: Current (x, y) mouse coordinates
            task_description: Description of what task to perform
            screen_size: Screen dimensions as (width, height)
            
        Returns:
            VisionNavigationResult containing action, coordinates, confidence, and reasoning
            
        Raises:
            Exception: If vision model API call fails after retries
        """
        # Build the vision prompt
        prompt = self._build_vision_prompt(
            task_description=task_description,
            current_mouse_pos=current_mouse_pos,
            screen_size=screen_size
        )
        
        try:
            # Send to vision model with retry logic
            response_text = self._call_vision_api_with_retry(prompt, screenshot)
            
            # Parse the response
            result = self._parse_vision_response(response_text, screen_size)
            
            # Validate coordinates are within bounds
            if result.coordinates:
                result = self._validate_coordinates(result, screen_size)
            
            return result
            
        except Exception as e:
            print(f"  ⚠ Error in vision analysis: {str(e)}")
            # Return error result
            return VisionNavigationResult(
                action='no_action',
                coordinates=None,
                confidence=0.0,
                reasoning=f'Error: {str(e)}',
                requires_followup=False
            )
    
    def verify_action_result(
        self,
        before_screenshot: Image.Image,
        after_screenshot: Image.Image,
        expected_outcome: str
    ) -> bool:
        """Compare before and after screenshots to verify an action succeeded.
        
        This method uses the vision model to analyze two screenshots and determine
        if the expected outcome was achieved.
        
        Args:
            before_screenshot: PIL Image before the action
            after_screenshot: PIL Image after the action
            expected_outcome: Description of what should have changed
            
        Returns:
            True if the action succeeded, False otherwise
        """
        prompt = f"""Compare these two screenshots (before and after an action).

Expected outcome: {expected_outcome}

Analyze the differences between the screenshots and determine if the expected outcome occurred.

Return your analysis as JSON:
{{
    "success": true/false,
    "reasoning": "explanation of what changed and whether it matches expectations",
    "confidence": 0.0-1.0
}}

Return ONLY the JSON, no other text."""
        
        try:
            # Send both images to vision model with retry logic
            response_text = self._call_vision_api_with_retry(prompt, before_screenshot, after_screenshot)
            
            # Parse response
            result = self._parse_json_response(response_text)
            
            success = result.get('success', False)
            reasoning = result.get('reasoning', 'Unknown')
            confidence = result.get('confidence', 0.0)
            
            print(f"  Verification result: {'Success' if success else 'Failed'} (confidence: {confidence:.2f})")
            print(f"  Reasoning: {reasoning}")
            
            return success
            
        except Exception as e:
            print(f"  ⚠ Error verifying action result: {str(e)}")
            return False
    
    def should_continue(
        self,
        current_screenshot: Image.Image,
        workflow_goal: str,
        actions_taken: List[dict]
    ) -> Tuple[bool, Optional[str]]:
        """Determine if the workflow should continue or is complete.
        
        This method analyzes the current screen state and the history of actions
        to determine if the workflow goal has been achieved or if more actions are needed.
        
        Args:
            current_screenshot: PIL Image of current screen state
            workflow_goal: Overall goal of the workflow
            actions_taken: List of actions taken so far (each dict has action, coordinates, reasoning)
            
        Returns:
            Tuple of (should_continue, next_task_description)
            - should_continue: True if more actions needed, False if complete
            - next_task_description: Description of next task, or None if complete
        """
        # Build action history summary
        action_summary = "\n".join([
            f"- {i+1}. {action.get('action')} at {action.get('coordinates')}: {action.get('reasoning')}"
            for i, action in enumerate(actions_taken)
        ])
        
        prompt = f"""Analyze this screenshot in the context of a workflow.

Workflow goal: {workflow_goal}

Actions taken so far:
{action_summary if action_summary else "None yet"}

Determine if the workflow goal has been achieved or if more actions are needed.

Return your analysis as JSON:
{{
    "goal_achieved": true/false,
    "reasoning": "explanation of current state and whether goal is met",
    "next_task": "description of next task if goal not achieved, or null if complete",
    "confidence": 0.0-1.0
}}

Return ONLY the JSON, no other text."""
        
        try:
            # Send to vision model with retry logic
            response_text = self._call_vision_api_with_retry(prompt, current_screenshot)
            
            result = self._parse_json_response(response_text)
            
            goal_achieved = result.get('goal_achieved', False)
            reasoning = result.get('reasoning', 'Unknown')
            next_task = result.get('next_task')
            confidence = result.get('confidence', 0.0)
            
            should_continue = not goal_achieved
            
            print(f"  Workflow status: {'Continue' if should_continue else 'Complete'} (confidence: {confidence:.2f})")
            print(f"  Reasoning: {reasoning}")
            if next_task:
                print(f"  Next task: {next_task}")
            
            return (should_continue, next_task)
            
        except Exception as e:
            print(f"  ⚠ Error determining workflow continuation: {str(e)}")
            # Default to not continuing on error
            return (False, None)
    
    def _build_vision_prompt(
        self,
        task_description: str,
        current_mouse_pos: Tuple[int, int],
        screen_size: Tuple[int, int]
    ) -> str:
        """Build the prompt for vision analysis.
        
        Args:
            task_description: What task to perform
            current_mouse_pos: Current mouse position
            screen_size: Screen dimensions
            
        Returns:
            Formatted prompt string
        """
        width, height = screen_size
        mouse_x, mouse_y = current_mouse_pos
        
        prompt = f"""Analyze this screenshot and determine the next action to accomplish the task.

Task: {task_description}

Current mouse position: ({mouse_x}, {mouse_y})
Screen size: {width}x{height} pixels

Identify the UI element that should be interacted with to accomplish this task.
Determine:
1. What action to perform (click, double_click, right_click, type, or complete if task is done)
2. The exact pixel coordinates (x, y) to click
3. Your confidence level (0.0 to 1.0)
4. Whether you need to see the result after this action (requires_followup)

Return your analysis as JSON:
{{
    "action": "click|double_click|right_click|type|no_action|complete",
    "coordinates": {{"x": 123, "y": 456}},
    "confidence": 0.95,
    "reasoning": "explanation of why you chose this element and action",
    "requires_followup": true/false,
    "text_to_type": "text content if action is 'type', otherwise null"
}}

Important:
- Use "complete" action when the task is already done
- Use "no_action" if you cannot identify the correct element
- Coordinates must be within screen bounds (0-{width}, 0-{height})
- Be precise with coordinates - identify the center of the target element
- Set requires_followup to true if you need to verify the result

Return ONLY the JSON, no other text."""
        
        return prompt
    
    def _parse_vision_response(self, response_text: str, screen_size: Tuple[int, int]) -> VisionNavigationResult:
        """Parse the vision model's response into a VisionNavigationResult.
        
        Args:
            response_text: Raw text response from vision model
            screen_size: Screen dimensions for coordinate validation
            
        Returns:
            VisionNavigationResult object
        """
        try:
            result = self._parse_json_response(response_text)
            
            # Extract fields
            action = result.get('action', 'no_action')
            coords_dict = result.get('coordinates')
            confidence = float(result.get('confidence', 0.0))
            reasoning = result.get('reasoning', 'No reasoning provided')
            requires_followup = result.get('requires_followup', False)
            text_to_type = result.get('text_to_type')
            
            # Parse coordinates
            coordinates = None
            if coords_dict and isinstance(coords_dict, dict):
                x = coords_dict.get('x')
                y = coords_dict.get('y')
                if x is not None and y is not None:
                    coordinates = (int(x), int(y))
            
            return VisionNavigationResult(
                action=action,
                coordinates=coordinates,
                confidence=confidence,
                reasoning=reasoning,
                requires_followup=requires_followup,
                text_to_type=text_to_type
            )
            
        except Exception as e:
            print(f"  ⚠ Error parsing vision response: {str(e)}")
            print(f"  Response text: {response_text[:200]}...")
            
            # Return safe default
            return VisionNavigationResult(
                action='no_action',
                coordinates=None,
                confidence=0.0,
                reasoning=f'Failed to parse response: {str(e)}',
                requires_followup=False
            )
    
    def _parse_json_response(self, response_text: str) -> dict:
        """Parse JSON from response text, handling markdown code blocks.
        
        Args:
            response_text: Raw response text that may contain JSON
            
        Returns:
            Parsed JSON as dictionary
            
        Raises:
            json.JSONDecodeError: If JSON cannot be parsed
        """
        cleaned = response_text.strip()
        
        # Remove markdown code blocks
        if '```json' in cleaned:
            cleaned = cleaned.split('```json')[1].split('```')[0].strip()
        elif '```' in cleaned:
            cleaned = cleaned.split('```')[1].split('```')[0].strip()
        
        return json.loads(cleaned)
    
    def _validate_coordinates(
        self,
        result: VisionNavigationResult,
        screen_size: Tuple[int, int],
        margin: int = 10
    ) -> VisionNavigationResult:
        """Validate and clamp coordinates to screen bounds.
        
        Validates coordinates are within screen bounds before execution.
        Clamps coordinates to valid range if slightly out of bounds.
        Rejects action if coordinates are severely invalid.
        
        Args:
            result: VisionNavigationResult to validate
            screen_size: Screen dimensions as (width, height)
            margin: Acceptable margin for clamping (default: 10 pixels)
            
        Returns:
            VisionNavigationResult with validated coordinates, or no_action if severely invalid
            
        Requirements: 3.4, 7.2
        """
        if not result.coordinates:
            return result
        
        width, height = screen_size
        x, y = result.coordinates
        
        # Check if coordinates are within bounds
        if 0 <= x <= width and 0 <= y <= height:
            return result
        
        # Calculate how far out of bounds
        x_overflow = max(0, -x, x - width)
        y_overflow = max(0, -y, y - height)
        max_overflow = max(x_overflow, y_overflow)
        
        # If severely out of bounds (more than margin), reject the action
        if max_overflow > margin:
            print(f"  ⚠ Coordinates ({x}, {y}) severely out of bounds (overflow: {max_overflow}px)")
            print(f"  ✗ Action rejected - coordinates invalid")
            return VisionNavigationResult(
                action='no_action',
                coordinates=None,
                confidence=0.0,
                reasoning=f"Coordinates ({x}, {y}) are severely out of screen bounds ({width}x{height}). Overflow: {max_overflow}px",
                requires_followup=False
            )
        
        # If slightly out of bounds (within margin), clamp to valid range
        clamped_x = max(0, min(x, width))
        clamped_y = max(0, min(y, height))
        
        print(f"  ⚠ Coordinates ({x}, {y}) slightly out of bounds, clamped to ({clamped_x}, {clamped_y})")
        
        # Create new result with clamped coordinates
        return VisionNavigationResult(
            action=result.action,
            coordinates=(clamped_x, clamped_y),
            confidence=result.confidence * 0.9,  # Reduce confidence slightly
            reasoning=f"{result.reasoning} [Coordinates clamped to screen bounds]",
            requires_followup=result.requires_followup,
            text_to_type=result.text_to_type
        )
    
    def is_critical_action(self, reasoning: str, action: str = None) -> Tuple[bool, List[str]]:
        """Check if an action is critical based on keywords in reasoning.
        
        Checks action reasoning for critical keywords (delete, format, shutdown, etc.).
        Flags actions as critical based on keyword matching.
        Requires user confirmation for critical actions.
        
        Args:
            reasoning: The AI's reasoning for the action
            action: Optional action type for additional context
            
        Returns:
            Tuple of (is_critical, matched_keywords)
            - is_critical: True if action contains critical keywords, False otherwise
            - matched_keywords: List of critical keywords found in reasoning
            
        Requirements: 7.1
        """
        reasoning_lower = reasoning.lower()
        matched_keywords = []
        
        # Check for critical keywords
        for keyword in self.critical_keywords:
            if keyword in reasoning_lower:
                matched_keywords.append(keyword)
        
        # Additional checks for specific action types
        if action:
            action_lower = action.lower()
            # Right-click actions near system areas could be critical
            if action_lower == 'right_click' and any(word in reasoning_lower for word in ['system', 'taskbar', 'tray']):
                matched_keywords.append('system_area')
        
        is_critical = len(matched_keywords) > 0
        
        if is_critical:
            print(f"  ⚠ Critical action detected! Keywords: {', '.join(matched_keywords)}")
        
        return (is_critical, matched_keywords)
    
    def add_action_to_history(self, action: str, coordinates: Optional[Tuple[int, int]]) -> None:
        """Add an action to the history buffer for loop detection.
        
        Tracks last N actions with coordinates in a circular buffer.
        
        Args:
            action: Type of action performed
            coordinates: Coordinates where action was performed
            
        Requirements: 7.4
        """
        # Add to history
        self.action_history.append({
            'action': action,
            'coordinates': coordinates,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
        
        # Maintain circular buffer size
        if len(self.action_history) > self.loop_detection_buffer_size:
            self.action_history.pop(0)
    
    def detect_loop(self, coordinates: Optional[Tuple[int, int]], tolerance: int = 5) -> Tuple[bool, Optional[str]]:
        """Detect if same coordinates are being clicked repeatedly (loop detection).
        
        Detects if same coordinates clicked multiple times (threshold: 3).
        Halts execution and logs warning if loop detected.
        
        Args:
            coordinates: Current coordinates to check
            tolerance: Pixel tolerance for considering coordinates "same" (default: 5)
            
        Returns:
            Tuple of (loop_detected, warning_message)
            - loop_detected: True if loop detected, False otherwise
            - warning_message: Description of detected loop, or None if no loop
            
        Requirements: 7.4
        """
        if not coordinates:
            return (False, None)
        
        # Count how many times similar coordinates appear in recent history
        similar_count = 0
        x, y = coordinates
        
        for entry in self.action_history:
            entry_coords = entry.get('coordinates')
            if entry_coords:
                ex, ey = entry_coords
                # Check if coordinates are within tolerance
                if abs(ex - x) <= tolerance and abs(ey - y) <= tolerance:
                    similar_count += 1
        
        # Check if threshold exceeded
        if similar_count >= self.loop_detection_threshold:
            warning = (
                f"Loop detected: Coordinates ({x}, {y}) clicked {similar_count} times "
                f"(threshold: {self.loop_detection_threshold}). "
                f"Recent actions: {len(self.action_history)}"
            )
            print(f"  ⚠ {warning}")
            return (True, warning)
        
        return (False, None)
    
    def reset_action_history(self) -> None:
        """Reset the action history buffer.
        
        Should be called at the start of a new visual navigation workflow.
        """
        self.action_history = []
    
    def check_iteration_limit(self, current_iteration: int) -> Tuple[bool, Optional[str]]:
        """Check if iteration limit has been reached.
        
        Tracks current iteration count and stops workflow when max_iterations reached.
        Logs timeout warning with partial results.
        
        Args:
            current_iteration: Current iteration number (1-based)
            
        Returns:
            Tuple of (limit_reached, warning_message)
            - limit_reached: True if limit reached, False otherwise
            - warning_message: Warning about timeout, or None if within limit
            
        Requirements: 4.6, 7.3
        """
        if current_iteration >= self.max_iterations:
            warning = (
                f"Iteration limit reached: {current_iteration}/{self.max_iterations}. "
                f"Workflow timeout. Actions taken: {len(self.action_history)}"
            )
            print(f"  ⚠ {warning}")
            return (True, warning)
        
        return (False, None)
    
    def save_audit_entry(self, entry: VisualNavigationAuditEntry) -> None:
        """Save an audit entry to the audit log file.
        
        Args:
            entry: VisualNavigationAuditEntry to save
        """
        if not self.enable_audit_log:
            return
        
        try:
            # Read existing entries
            entries = []
            if os.path.exists(self.audit_log_path):
                with open(self.audit_log_path, 'r') as f:
                    entries = json.load(f)
            
            # Append new entry
            entries.append(entry.to_dict())
            
            # Write back
            with open(self.audit_log_path, 'w') as f:
                json.dump(entries, f, indent=2)
                
        except Exception as e:
            print(f"  ⚠ Error saving audit entry: {str(e)}")
