"""
Smart wait times and page load detection.
Provides adaptive waiting based on what's being loaded.
"""
import time
from typing import Optional
import mss
from PIL import Image
import numpy as np


# Adaptive wait times based on action type
WAIT_TIMES = {
    # Application launches
    'chrome_launch': 3000,
    'firefox_launch': 3000,
    'edge_launch': 2500,
    'notepad_launch': 500,
    'explorer_launch': 1000,
    
    # Website loads (initial)
    'linkedin.com': 8000,
    'facebook.com': 6000,
    'x.com': 4000,
    'twitter.com': 4000,
    'instagram.com': 5000,
    'youtube.com': 4000,
    'github.com': 3000,
    'gmail.com': 5000,
    'google.com': 2000,
    
    # Actions
    'page_navigation': 3000,
    'form_submit': 2000,
    'button_click': 500,
    'dialog_open': 1000,
    'search_results': 2000,
    
    # Default
    'default': 2000
}


class SmartWaiter:
    """Smart waiting with page load detection."""
    
    def __init__(self):
        self.last_screenshot = None
        self.screenshot_threshold = 0.95  # 95% similarity = still loading
    
    def get_wait_time(self, action_type: str, target: str = "") -> int:
        """
        Get adaptive wait time based on action type.
        
        Args:
            action_type: Type of action (e.g., 'app_launch', 'page_load')
            target: Target app or URL
            
        Returns:
            Wait time in milliseconds
        """
        # Check for specific app launches
        if action_type == 'app_launch':
            app_lower = target.lower()
            for app_name, wait_time in WAIT_TIMES.items():
                if app_name.replace('_launch', '') in app_lower:
                    return wait_time
            return WAIT_TIMES['default']
        
        # Check for specific website loads
        if action_type == 'page_load':
            url_lower = target.lower()
            for domain, wait_time in WAIT_TIMES.items():
                if domain in url_lower:
                    return wait_time
            return WAIT_TIMES['page_navigation']
        
        # Check for specific actions
        return WAIT_TIMES.get(action_type, WAIT_TIMES['default'])
    
    def wait_for_page_load(self, max_wait_ms: int = 10000, check_interval_ms: int = 500) -> bool:
        """
        Wait for page to finish loading by detecting screen changes.
        
        Args:
            max_wait_ms: Maximum time to wait
            check_interval_ms: How often to check
            
        Returns:
            True if page loaded, False if timeout
        """
        start_time = time.time()
        max_wait_sec = max_wait_ms / 1000
        check_interval_sec = check_interval_ms / 1000
        
        stable_count = 0
        required_stable = 2  # Need 2 consecutive stable checks
        
        while (time.time() - start_time) < max_wait_sec:
            # Take screenshot
            current_screenshot = self._capture_screen()
            
            if self.last_screenshot is not None:
                # Compare with previous screenshot
                similarity = self._compare_screenshots(self.last_screenshot, current_screenshot)
                
                if similarity > self.screenshot_threshold:
                    stable_count += 1
                    if stable_count >= required_stable:
                        # Page is stable (loaded)
                        return True
                else:
                    # Still changing
                    stable_count = 0
            
            self.last_screenshot = current_screenshot
            time.sleep(check_interval_sec)
        
        # Timeout
        return False
    
    def wait_for_element_visible(self, element_description: str, max_wait_ms: int = 5000) -> bool:
        """
        Wait for an element to become visible (placeholder for future OCR/vision).
        
        Args:
            element_description: Description of element to wait for
            max_wait_ms: Maximum time to wait
            
        Returns:
            True if element found, False if timeout
        """
        # For now, just wait the specified time
        # Future: Use OCR or Gemini vision to detect element
        time.sleep(max_wait_ms / 1000)
        return True
    
    def smart_wait(self, action_type: str, target: str = "", use_detection: bool = True) -> int:
        """
        Smart wait that combines adaptive timing with load detection.
        
        Args:
            action_type: Type of action
            target: Target app/URL
            use_detection: Whether to use page load detection
            
        Returns:
            Actual wait time in milliseconds
        """
        # Get base wait time
        base_wait = self.get_wait_time(action_type, target)
        
        if use_detection and action_type in ['page_load', 'page_navigation']:
            # Use detection for page loads
            start = time.time()
            loaded = self.wait_for_page_load(max_wait_ms=base_wait)
            actual_wait = int((time.time() - start) * 1000)
            
            if loaded:
                print(f"  Page loaded in {actual_wait}ms (detected)")
            else:
                print(f"  Waited {actual_wait}ms (timeout, continuing anyway)")
            
            return actual_wait
        else:
            # Use fixed wait time
            time.sleep(base_wait / 1000)
            return base_wait
    
    def _capture_screen(self) -> Optional[np.ndarray]:
        """Capture current screen as numpy array."""
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]  # Primary monitor
                screenshot = sct.grab(monitor)
                # Convert to numpy array and resize for faster comparison
                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                img = img.resize((320, 180))  # Smaller for faster comparison
                return np.array(img)
        except Exception:
            return None
    
    def _compare_screenshots(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """
        Compare two screenshots and return similarity score.
        
        Args:
            img1: First screenshot
            img2: Second screenshot
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        try:
            # Calculate mean squared error
            mse = np.mean((img1 - img2) ** 2)
            
            # Convert to similarity (0 = identical, higher = more different)
            # Normalize to 0-1 range
            max_mse = 255 ** 2  # Maximum possible MSE for 8-bit images
            similarity = 1.0 - (mse / max_mse)
            
            return similarity
        except Exception:
            return 0.0


# Global instance
_smart_waiter = SmartWaiter()


def get_smart_wait_time(action_type: str, target: str = "") -> int:
    """Get adaptive wait time for an action."""
    return _smart_waiter.get_wait_time(action_type, target)


def smart_wait(action_type: str, target: str = "", use_detection: bool = True) -> int:
    """Perform a smart wait with optional load detection."""
    return _smart_waiter.smart_wait(action_type, target, use_detection)


def wait_for_page_load(max_wait_ms: int = 10000) -> bool:
    """Wait for page to finish loading."""
    return _smart_waiter.wait_for_page_load(max_wait_ms)
