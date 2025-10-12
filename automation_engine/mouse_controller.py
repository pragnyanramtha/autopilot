"""
Advanced Mouse Controller with Smooth Curved Movements
Provides natural-looking mouse movements using Bezier curves and easing functions.
"""

import pyautogui
import numpy as np
import time
import random
from typing import Tuple, List, Optional, Literal
from dataclasses import dataclass


@dataclass
class MouseConfig:
    """Configuration for mouse movement behavior."""
    # Movement settings
    curve_intensity: float = 0.3  # 0.0 = straight line, 1.0 = very curved
    speed: float = 1.0  # Movement speed multiplier
    overshoot: bool = True  # Slightly overshoot target then correct
    overshoot_amount: float = 0.05  # Percentage of distance to overshoot
    
    # Randomization for human-like behavior
    add_noise: bool = True  # Add small random variations
    noise_amount: float = 2.0  # Pixels of random noise
    
    # Timing
    min_duration: float = 0.3  # Minimum time for movement (seconds)
    max_duration: float = 1.5  # Maximum time for movement (seconds)
    
    # Click settings
    click_delay_min: float = 0.05  # Min delay before click
    click_delay_max: float = 0.15  # Max delay before click
    
    # Safety
    boundary_margin: int = 5  # Pixels from screen edge to avoid


class MouseController:
    """
    Advanced mouse controller with smooth, human-like movements.
    
    Features:
    - Bezier curve movements (smooth curves, not straight lines)
    - Easing functions (acceleration/deceleration)
    - Overshoot and correction (natural human behavior)
    - Random noise (micro-adjustments)
    - Configurable speed and curve intensity
    """
    
    def __init__(self, config: Optional[MouseConfig] = None):
        """
        Initialize the mouse controller.
        
        Args:
            config: MouseConfig object with movement settings
        """
        self.config = config or MouseConfig()
        
        # Get screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Disable pyautogui's built-in pause
        pyautogui.PAUSE = 0
        
        # Enable fail-safe (move to corner to stop)
        pyautogui.FAILSAFE = True
    
    def move_to(
        self, 
        x: int, 
        y: int, 
        duration: Optional[float] = None,
        curve_type: Literal['bezier', 'arc', 'wave'] = 'bezier'
    ) -> None:
        """
        Move mouse to target position using smooth curved path.
        
        Args:
            x: Target X coordinate
            y: Target Y coordinate
            duration: Time to take for movement (auto-calculated if None)
            curve_type: Type of curve to use ('bezier', 'arc', 'wave')
        """
        # Get current position
        start_x, start_y = pyautogui.position()
        
        # Validate target coordinates
        x, y = self._clamp_coordinates(x, y)
        
        # Calculate distance
        distance = self._calculate_distance(start_x, start_y, x, y)
        
        # Auto-calculate duration based on distance
        if duration is None:
            duration = self._calculate_duration(distance)
        
        # Apply speed multiplier
        duration = duration / self.config.speed
        
        # Generate path points
        if curve_type == 'bezier':
            path = self._generate_bezier_path(start_x, start_y, x, y, duration)
        elif curve_type == 'arc':
            path = self._generate_arc_path(start_x, start_y, x, y, duration)
        elif curve_type == 'wave':
            path = self._generate_wave_path(start_x, start_y, x, y, duration)
        else:
            path = self._generate_bezier_path(start_x, start_y, x, y, duration)
        
        # Add overshoot if enabled
        if self.config.overshoot and distance > 50:
            path = self._add_overshoot(path, x, y)
        
        # Execute movement along path
        self._execute_path(path)
    
    def click(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        button: Literal['left', 'right', 'middle'] = 'left',
        clicks: int = 1,
        move_first: bool = True
    ) -> None:
        """
        Click at specified position with natural timing.
        
        Args:
            x: Target X coordinate (None for current position)
            y: Target Y coordinate (None for current position)
            button: Mouse button to click
            clicks: Number of clicks
            move_first: Whether to move to position first
        """
        # Move to position if specified
        if x is not None and y is not None and move_first:
            self.move_to(x, y)
        
        # Random delay before click (human-like)
        delay = random.uniform(
            self.config.click_delay_min,
            self.config.click_delay_max
        )
        time.sleep(delay)
        
        # Perform click
        if x is not None and y is not None and not move_first:
            pyautogui.click(x=x, y=y, button=button, clicks=clicks)
        else:
            pyautogui.click(button=button, clicks=clicks)
        
        # Small delay after click
        time.sleep(0.05)
    
    def drag_to(
        self,
        x: int,
        y: int,
        button: Literal['left', 'right', 'middle'] = 'left',
        duration: Optional[float] = None
    ) -> None:
        """
        Drag mouse to target position while holding button.
        
        Args:
            x: Target X coordinate
            y: Target Y coordinate
            button: Mouse button to hold
            duration: Time to take for drag
        """
        # Get current position
        start_x, start_y = pyautogui.position()
        
        # Validate coordinates
        x, y = self._clamp_coordinates(x, y)
        
        # Calculate duration
        distance = self._calculate_distance(start_x, start_y, x, y)
        if duration is None:
            duration = self._calculate_duration(distance)
        
        # Generate smooth path
        path = self._generate_bezier_path(start_x, start_y, x, y, duration)
        
        # Press button down
        pyautogui.mouseDown(button=button)
        time.sleep(0.05)
        
        try:
            # Execute drag along path
            self._execute_path(path)
        finally:
            # Always release button
            time.sleep(0.05)
            pyautogui.mouseUp(button=button)
    
    def scroll(
        self,
        amount: int,
        x: Optional[int] = None,
        y: Optional[int] = None
    ) -> None:
        """
        Scroll at specified position.
        
        Args:
            amount: Scroll amount (positive = up, negative = down)
            x: X coordinate to scroll at (None for current)
            y: Y coordinate to scroll at (None for current)
        """
        if x is not None and y is not None:
            self.move_to(x, y)
        
        # Add small delay
        time.sleep(0.1)
        
        # Perform scroll
        pyautogui.scroll(amount)
    
    def get_position(self) -> Tuple[int, int]:
        """Get current mouse position."""
        return pyautogui.position()
    
    # ========================================
    # Path Generation Methods
    # ========================================
    
    def _generate_bezier_path(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: float
    ) -> List[Tuple[int, int, float]]:
        """
        Generate smooth path using cubic Bezier curve.
        
        Returns:
            List of (x, y, timestamp) tuples
        """
        # Calculate control points for Bezier curve
        cp1_x, cp1_y, cp2_x, cp2_y = self._calculate_control_points(
            start_x, start_y, end_x, end_y
        )
        
        # Number of points based on duration (60 FPS)
        num_points = max(int(duration * 60), 10)
        
        path = []
        start_time = time.time()
        
        for i in range(num_points + 1):
            # Parameter t from 0 to 1
            t = i / num_points
            
            # Apply easing function for natural acceleration/deceleration
            t_eased = self._ease_in_out_cubic(t)
            
            # Calculate point on Bezier curve
            x, y = self._cubic_bezier(
                t_eased,
                start_x, start_y,
                cp1_x, cp1_y,
                cp2_x, cp2_y,
                end_x, end_y
            )
            
            # Add noise for human-like imperfection
            if self.config.add_noise and i > 0 and i < num_points:
                x += random.uniform(-self.config.noise_amount, self.config.noise_amount)
                y += random.uniform(-self.config.noise_amount, self.config.noise_amount)
            
            # Calculate timestamp
            timestamp = start_time + (duration * t)
            
            path.append((int(x), int(y), timestamp))
        
        return path
    
    def _generate_arc_path(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: float
    ) -> List[Tuple[int, int, float]]:
        """Generate path following a circular arc."""
        # Calculate arc parameters
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Perpendicular offset for arc height
        dx = end_x - start_x
        dy = end_y - start_y
        distance = np.sqrt(dx**2 + dy**2)
        
        # Arc height based on curve intensity
        arc_height = distance * self.config.curve_intensity
        
        # Perpendicular direction
        if distance > 0:
            perp_x = -dy / distance
            perp_y = dx / distance
        else:
            perp_x, perp_y = 0, 0
        
        # Arc center
        center_x = mid_x + perp_x * arc_height
        center_y = mid_y + perp_y * arc_height
        
        num_points = max(int(duration * 60), 10)
        path = []
        start_time = time.time()
        
        for i in range(num_points + 1):
            t = i / num_points
            t_eased = self._ease_in_out_cubic(t)
            
            # Interpolate along arc
            angle = t_eased * np.pi
            x = start_x + (end_x - start_x) * t_eased + perp_x * arc_height * np.sin(angle)
            y = start_y + (end_y - start_y) * t_eased + perp_y * arc_height * np.sin(angle)
            
            timestamp = start_time + (duration * t)
            path.append((int(x), int(y), timestamp))
        
        return path
    
    def _generate_wave_path(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: float
    ) -> List[Tuple[int, int, float]]:
        """Generate path with wave-like motion."""
        num_points = max(int(duration * 60), 10)
        path = []
        start_time = time.time()
        
        # Wave parameters
        wave_frequency = 2.0  # Number of waves
        wave_amplitude = 10 * self.config.curve_intensity
        
        for i in range(num_points + 1):
            t = i / num_points
            t_eased = self._ease_in_out_cubic(t)
            
            # Linear interpolation
            x = start_x + (end_x - start_x) * t_eased
            y = start_y + (end_y - start_y) * t_eased
            
            # Add wave perpendicular to movement direction
            dx = end_x - start_x
            dy = end_y - start_y
            distance = np.sqrt(dx**2 + dy**2)
            
            if distance > 0:
                perp_x = -dy / distance
                perp_y = dx / distance
                
                wave_offset = wave_amplitude * np.sin(t * wave_frequency * 2 * np.pi)
                x += perp_x * wave_offset
                y += perp_y * wave_offset
            
            timestamp = start_time + (duration * t)
            path.append((int(x), int(y), timestamp))
        
        return path
    
    def _add_overshoot(
        self,
        path: List[Tuple[int, int, float]],
        target_x: int,
        target_y: int
    ) -> List[Tuple[int, int, float]]:
        """Add overshoot and correction to path."""
        if len(path) < 2:
            return path
        
        # Get last point and direction
        last_x, last_y, last_time = path[-1]
        prev_x, prev_y, _ = path[-2]
        
        # Calculate overshoot direction
        dx = last_x - prev_x
        dy = last_y - prev_y
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance < 1:
            return path
        
        # Overshoot amount
        overshoot_dist = distance * self.config.overshoot_amount * 10
        overshoot_x = int(last_x + (dx / distance) * overshoot_dist)
        overshoot_y = int(last_y + (dy / distance) * overshoot_dist)
        
        # Add overshoot point
        overshoot_time = last_time + 0.05
        path.append((overshoot_x, overshoot_y, overshoot_time))
        
        # Add correction back to target
        correction_time = overshoot_time + 0.1
        path.append((target_x, target_y, correction_time))
        
        return path
    
    # ========================================
    # Helper Methods
    # ========================================
    
    def _calculate_control_points(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int
    ) -> Tuple[float, float, float, float]:
        """Calculate control points for Bezier curve."""
        # Distance and direction
        dx = end_x - start_x
        dy = end_y - start_y
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance < 1:
            return start_x, start_y, end_x, end_y
        
        # Control point offset
        offset = distance * self.config.curve_intensity
        
        # Perpendicular direction
        perp_x = -dy / distance
        perp_y = dx / distance
        
        # Random side for curve
        side = random.choice([-1, 1])
        
        # Control points
        cp1_x = start_x + dx * 0.25 + perp_x * offset * side
        cp1_y = start_y + dy * 0.25 + perp_y * offset * side
        
        cp2_x = start_x + dx * 0.75 + perp_x * offset * side
        cp2_y = start_y + dy * 0.75 + perp_y * offset * side
        
        return cp1_x, cp1_y, cp2_x, cp2_y
    
    def _cubic_bezier(
        self,
        t: float,
        p0_x: float, p0_y: float,
        p1_x: float, p1_y: float,
        p2_x: float, p2_y: float,
        p3_x: float, p3_y: float
    ) -> Tuple[float, float]:
        """Calculate point on cubic Bezier curve."""
        # Cubic Bezier formula
        t2 = t * t
        t3 = t2 * t
        mt = 1 - t
        mt2 = mt * mt
        mt3 = mt2 * mt
        
        x = mt3 * p0_x + 3 * mt2 * t * p1_x + 3 * mt * t2 * p2_x + t3 * p3_x
        y = mt3 * p0_y + 3 * mt2 * t * p1_y + 3 * mt * t2 * p2_y + t3 * p3_y
        
        return x, y
    
    def _ease_in_out_cubic(self, t: float) -> float:
        """Cubic easing function for smooth acceleration/deceleration."""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2
    
    def _calculate_distance(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int
    ) -> float:
        """Calculate Euclidean distance between two points."""
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def _calculate_duration(self, distance: float) -> float:
        """Calculate appropriate duration based on distance."""
        # Base duration on distance (pixels per second)
        base_speed = 1000  # pixels per second
        duration = distance / base_speed
        
        # Clamp to min/max
        duration = max(self.config.min_duration, duration)
        duration = min(self.config.max_duration, duration)
        
        return duration
    
    def _clamp_coordinates(self, x: int, y: int) -> Tuple[int, int]:
        """Clamp coordinates to screen boundaries with margin."""
        margin = self.config.boundary_margin
        
        x = max(margin, min(x, self.screen_width - margin))
        y = max(margin, min(y, self.screen_height - margin))
        
        return x, y
    
    def _execute_path(self, path: List[Tuple[int, int, float]]) -> None:
        """Execute movement along generated path."""
        for x, y, target_time in path:
            # Move to position
            pyautogui.moveTo(x, y, _pause=False)
            
            # Wait until target time
            current_time = time.time()
            sleep_time = target_time - current_time
            
            if sleep_time > 0:
                time.sleep(sleep_time)
