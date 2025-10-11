"""Input controller module for mouse and keyboard control."""

import pyautogui
from typing import Optional, Literal


class InputController:
    """Controls mouse and keyboard input using pyautogui."""
    
    def __init__(self):
        """Initialize the input controller with safety settings."""
        # Enable fail-safe: moving mouse to upper-left corner raises exception
        pyautogui.FAILSAFE = True
        
        # Set a small pause between pyautogui calls for stability
        pyautogui.PAUSE = 0.1
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5) -> None:
        """
        Move the mouse to specified coordinates.
        
        Args:
            x: X coordinate to move to
            y: Y coordinate to move to
            duration: Time in seconds to take for the movement (default: 0.5)
            
        Requirements: 4.1 - Execute mouse movements to specified coordinates
        """
        pyautogui.moveTo(x, y, duration=duration)
    
    def click(
        self, 
        x: Optional[int] = None, 
        y: Optional[int] = None,
        button: Literal['left', 'right', 'middle'] = 'left',
        clicks: int = 1
    ) -> None:
        """
        Perform a mouse click at the specified location.
        
        Args:
            x: X coordinate to click (None for current position)
            y: Y coordinate to click (None for current position)
            button: Mouse button to click ('left', 'right', or 'middle')
            clicks: Number of clicks (1 for single, 2 for double-click)
            
        Requirements: 4.2 - Perform left-click, right-click, or double-click actions
        """
        if x is not None and y is not None:
            pyautogui.click(x=x, y=y, button=button, clicks=clicks)
        else:
            pyautogui.click(button=button, clicks=clicks)
    
    def type_text(self, text: str, interval: float = 0.05) -> None:
        """
        Type text using the keyboard.
        
        Args:
            text: Text string to type
            interval: Time in seconds between each keystroke (default: 0.05)
            
        Requirements: 4.3 - Send keyboard input with proper key sequences
        """
        pyautogui.write(text, interval=interval)
    
    def press_key(self, key: str) -> None:
        """
        Press a single key or key combination.
        
        Args:
            key: Key name to press (e.g., 'enter', 'esc', 'tab')
                 For special keys, use pyautogui key names
            
        Requirements: 4.3 - Send keyboard input with proper key sequences
        """
        pyautogui.press(key)
    
    def hotkey(self, *keys: str) -> None:
        """
        Press a combination of keys simultaneously (hotkey).
        
        Args:
            *keys: Variable number of key names to press together
                   Example: hotkey('ctrl', 'c') for copy
            
        Requirements: 4.3 - Send keyboard input with proper key sequences
        """
        pyautogui.hotkey(*keys)
    
    def get_mouse_position(self) -> tuple[int, int]:
        """
        Get the current mouse position.
        
        Returns:
            Tuple of (x, y) coordinates
        """
        return pyautogui.position()
    
    def get_screen_size(self) -> tuple[int, int]:
        """
        Get the screen size.
        
        Returns:
            Tuple of (width, height) in pixels
        """
        return pyautogui.size()
