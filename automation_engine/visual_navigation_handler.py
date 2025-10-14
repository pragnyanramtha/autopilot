"""
Visual Navigation Handler for Automation Engine.
Handles visual navigation requests from AI Brain, captures screen state,
and executes vision-guided mouse actions.
"""

import base64
import io
from typing import Optional, Tuple, Dict, Any
from PIL import Image

from automation_engine.screen_capture import ScreenCapture
from automation_engine.mouse_controller import MouseController
from shared.communication import MessageBroker


class VisualNavigationHandler:
    """
    Handles visual navigation requests in the Automation Engine.
    
    Responsibilities:
    - Capture current screen state and mouse position
    - Send screenshots to AI Brain for analysis
    - Execute vision-guided mouse actions
    - Validate coordinates and handle errors
    
    Requirements: 3.1, 3.2, 3.3
    """
    
    def __init__(
        self,
        screen_capture: ScreenCapture,
        mouse_controller: MouseController,
        message_broker: MessageBroker
    ):
        """
        Initialize the visual navigation handler.
        
        Args:
            screen_capture: ScreenCapture instance for capturing screenshots
            mouse_controller: MouseController instance for mouse actions
            message_broker: MessageBroker instance for communication
            
        Requirements: 3.1, 3.2, 3.3
        """
        self.screen_capture = screen_capture
        self.mouse_controller = mouse_controller
        self.message_broker = message_broker
    
    def capture_current_state(self) -> Dict[str, Any]:
        """
        Capture current screen state and mouse position.
        
        Returns:
            Dictionary containing:
                - screenshot_base64: Base64 encoded screenshot
                - mouse_position: Dict with x, y coordinates
                - screen_size: Dict with width, height
                
        Requirements: 1.1, 1.2, 1.3, 1.4
        """
        # Capture screenshot
        screenshot = self.screen_capture.capture_screen()
        
        # Get current mouse position
        mouse_x, mouse_y = self.mouse_controller.get_position()
        
        # Get screen size
        screen_width, screen_height = self.screen_capture.get_screen_size()
        
        # Encode screenshot to base64
        screenshot_base64 = self._encode_screenshot(screenshot)
        
        return {
            "screenshot_base64": screenshot_base64,
            "mouse_position": {"x": mouse_x, "y": mouse_y},
            "screen_size": {"width": screen_width, "height": screen_height}
        }
    
    def handle_visual_navigation_request(self, request: dict) -> None:
        """
        Handle incoming visual navigation request.
        Captures current state and sends response to AI Brain.
        
        Args:
            request: Visual navigation request dictionary containing:
                - request_id: Unique identifier for this request
                - task_description: Description of the task
                - workflow_goal: Overall goal of the workflow
                
        Requirements: 1.1, 1.2, 1.3, 4.1, 4.2
        """
        request_id = request.get('request_id', 'unknown')
        
        try:
            # Capture current state
            state = self.capture_current_state()
            
            # Build response
            response = {
                "request_id": request_id,
                "screenshot_base64": state["screenshot_base64"],
                "mouse_position": state["mouse_position"],
                "screen_size": state["screen_size"]
            }
            
            # Send response to AI Brain
            self.message_broker.send_visual_navigation_response(response)
            
        except Exception as e:
            # Send error response
            error_response = {
                "request_id": request_id,
                "error": str(e),
                "screenshot_base64": None,
                "mouse_position": {"x": 0, "y": 0},
                "screen_size": {"width": 0, "height": 0}
            }
            self.message_broker.send_visual_navigation_response(error_response)
    
    def execute_visual_action(self, command: dict) -> dict:
        """
        Execute action from AI Brain's vision analysis.
        
        Args:
            command: Visual action command dictionary containing:
                - request_id: Unique identifier
                - action: Action type ('click', 'double_click', 'right_click', 'type')
                - coordinates: Dict with x, y coordinates
                - text: Text to type (for 'type' actions)
                - request_followup: Whether to capture new screenshot after action
                
        Returns:
            Action result dictionary with status and optional new screenshot
            
        Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 4.2
        """
        request_id = command.get('request_id', 'unknown')
        action = command.get('action', 'click')
        coordinates = command.get('coordinates', {})
        text = command.get('text')
        request_followup = command.get('request_followup', False)
        
        try:
            # Extract coordinates
            x = coordinates.get('x', 0)
            y = coordinates.get('y', 0)
            
            # Validate coordinates are within screen bounds
            screen_width, screen_height = self.screen_capture.get_screen_size()
            is_valid, error_message = self._validate_coordinates(x, y, screen_width, screen_height)
            if not is_valid:
                return {
                    "request_id": request_id,
                    "status": "error",
                    "error": f"Coordinate validation failed: {error_message}",
                    "screenshot_base64": None,
                    "mouse_position": {"x": 0, "y": 0}
                }
            
            # Execute the action
            if action == 'click':
                self.mouse_controller.click(x, y, button='left')
            elif action == 'double_click':
                self.mouse_controller.click(x, y, button='left', clicks=2)
            elif action == 'right_click':
                self.mouse_controller.click(x, y, button='right')
            elif action == 'type':
                # Move to position first, then type
                self.mouse_controller.move_to(x, y)
                if text:
                    import pyautogui
                    pyautogui.write(text)
            else:
                return {
                    "request_id": request_id,
                    "status": "error",
                    "error": f"Unknown action type: {action}",
                    "screenshot_base64": None,
                    "mouse_position": {"x": x, "y": y}
                }
            
            # Get new mouse position
            mouse_x, mouse_y = self.mouse_controller.get_position()
            
            # Capture new screenshot if requested
            screenshot_base64 = None
            if request_followup:
                screenshot = self.screen_capture.capture_screen()
                screenshot_base64 = self._encode_screenshot(screenshot)
            
            # Return success result
            return {
                "request_id": request_id,
                "status": "success",
                "error": None,
                "screenshot_base64": screenshot_base64,
                "mouse_position": {"x": mouse_x, "y": mouse_y}
            }
            
        except Exception as e:
            # Return error result
            return {
                "request_id": request_id,
                "status": "error",
                "error": str(e),
                "screenshot_base64": None,
                "mouse_position": {"x": 0, "y": 0}
            }
    
    def _encode_screenshot(self, screenshot: Image.Image, quality: int = 85) -> str:
        """
        Encode PIL Image to base64 string.
        
        Args:
            screenshot: PIL Image object
            quality: JPEG quality (1-100)
            
        Returns:
            Base64 encoded string
            
        Requirements: 1.3
        """
        # Convert to RGB if necessary
        if screenshot.mode != 'RGB':
            screenshot = screenshot.convert('RGB')
        
        # Save to bytes buffer with compression
        buffer = io.BytesIO()
        screenshot.save(buffer, format='JPEG', quality=quality)
        buffer.seek(0)
        
        # Encode to base64
        screenshot_bytes = buffer.read()
        screenshot_base64 = base64.b64encode(screenshot_bytes).decode('utf-8')
        
        return screenshot_base64
    
    def _validate_coordinates(
        self,
        x: int,
        y: int,
        screen_width: int,
        screen_height: int,
        margin: int = 5
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate that coordinates are within screen bounds.
        
        Validates coordinates are within screen bounds before execution.
        Provides detailed error messages for invalid coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
            margin: Safety margin from edges (default: 5 pixels)
            
        Returns:
            Tuple of (is_valid, error_message)
            - is_valid: True if coordinates are valid, False otherwise
            - error_message: Description of validation failure, or None if valid
            
        Requirements: 3.4, 7.2
        """
        # Check if coordinates are within bounds with margin
        if margin <= x < screen_width - margin and margin <= y < screen_height - margin:
            return (True, None)
        
        # Build detailed error message
        errors = []
        if x < margin:
            errors.append(f"X coordinate {x} is too close to left edge (min: {margin})")
        elif x >= screen_width - margin:
            errors.append(f"X coordinate {x} is too close to right edge (max: {screen_width - margin})")
        
        if y < margin:
            errors.append(f"Y coordinate {y} is too close to top edge (min: {margin})")
        elif y >= screen_height - margin:
            errors.append(f"Y coordinate {y} is too close to bottom edge (max: {screen_height - margin})")
        
        error_message = "; ".join(errors)
        return (False, error_message)
