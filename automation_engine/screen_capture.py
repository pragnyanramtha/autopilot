"""Screen capture module for capturing screenshots and screen regions."""

import mss
from PIL import Image
from typing import Optional, Tuple


class ScreenCapture:
    """Handles screen capture operations using mss library."""
    
    def __init__(self):
        """Initialize the screen capture with mss."""
        self.sct = mss.mss()
    
    def capture_screen(self) -> Image.Image:
        """
        Capture the entire screen.
        
        Returns:
            PIL Image object of the captured screen
            
        Requirements: 3.1 - Capture and analyze current screen state
        """
        # Capture the primary monitor
        monitor = self.sct.monitors[1]  # monitors[0] is all monitors combined
        screenshot = self.sct.grab(monitor)
        
        # Convert to PIL Image
        img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        return img
    
    def capture_region(self, x: int, y: int, width: int, height: int) -> Image.Image:
        """
        Capture a specific region of the screen.
        
        Args:
            x: X coordinate of the top-left corner
            y: Y coordinate of the top-left corner
            width: Width of the region to capture
            height: Height of the region to capture
            
        Returns:
            PIL Image object of the captured region
            
        Requirements: 3.1 - Capture and analyze current screen state
        """
        # Define the region to capture
        region = {
            'left': x,
            'top': y,
            'width': width,
            'height': height
        }
        
        # Capture the specified region
        screenshot = self.sct.grab(region)
        
        # Convert to PIL Image
        img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        return img
    
    def get_screen_size(self) -> Tuple[int, int]:
        """
        Get the size of the primary monitor.
        
        Returns:
            Tuple of (width, height) in pixels
        """
        monitor = self.sct.monitors[1]
        return (monitor['width'], monitor['height'])
    
    def __del__(self):
        """Clean up mss resources."""
        if hasattr(self, 'sct'):
            self.sct.close()
