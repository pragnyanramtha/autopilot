"""
Mock action handlers for testing without API calls or actual automation.

These handlers simulate the behavior of real actions but don't:
- Make API calls to Gemini
- Move the mouse or click
- Type on the keyboard
- Capture screenshots

Perfect for testing protocol generation and execution flow.
"""
import time
import random
from typing import Dict, Any


class MockActionHandlers:
    """Mock implementations of action handlers for testing."""
    
    def __init__(self, action_registry):
        """Initialize mock handlers with action registry."""
        self.action_registry = action_registry
        self.execution_log = []
    
    def register_all_mock_actions(self):
        """Register all mock actions with the action registry."""
        
        from shared.action_registry import ActionCategory
        
        # Mouse actions
        self.action_registry.register(
            name='mouse_move',
            category=ActionCategory.MOUSE,
            description='[MOCK] Simulate mouse movement',
            handler=self._mock_mouse_move,
            required_params=['x', 'y'],
            optional_params={'smooth': True, 'duration_ms': 200}
        )
        
        self.action_registry.register(
            name='mouse_click',
            category=ActionCategory.MOUSE,
            description='[MOCK] Simulate mouse click',
            handler=self._mock_mouse_click,
            required_params=[],
            optional_params={'button': 'left', 'clicks': 1}
        )
        
        # Keyboard actions
        self.action_registry.register(
            name='type',
            category=ActionCategory.KEYBOARD,
            description='[MOCK] Simulate typing text',
            handler=self._mock_type,
            required_params=['text'],
            optional_params={'interval': 0.05}
        )
        
        self.action_registry.register(
            name='press_key',
            category=ActionCategory.KEYBOARD,
            description='[MOCK] Simulate key press',
            handler=self._mock_press_key,
            required_params=['key'],
            optional_params={}
        )
        
        self.action_registry.register(
            name='shortcut',
            category=ActionCategory.KEYBOARD,
            description='[MOCK] Simulate keyboard shortcut',
            handler=self._mock_shortcut,
            required_params=['keys'],
            optional_params={}
        )
        
        # Application actions
        self.action_registry.register(
            name='open_app',
            category=ActionCategory.SYSTEM,
            description='[MOCK] Simulate opening application',
            handler=self._mock_open_app,
            required_params=['app_name'],
            optional_params={}
        )
        
        self.action_registry.register(
            name='open_url',
            category=ActionCategory.BROWSER,
            description='[MOCK] Simulate opening URL',
            handler=self._mock_open_url,
            required_params=['url'],
            optional_params={}
        )
        
        # Visual actions
        self.action_registry.register(
            name='visual_navigate',
            category=ActionCategory.VISION,
            description='[MOCK] Simulate visual navigation',
            handler=self._mock_visual_navigate,
            required_params=['task'],
            optional_params={'goal': None, 'max_iterations': 10}
        )
        
        self.action_registry.register(
            name='verify_screen',
            category=ActionCategory.VISION,
            description='[MOCK] Simulate screen verification',
            handler=self._mock_verify_screen,
            required_params=['context', 'expected'],
            optional_params={'confidence_threshold': 0.7}
        )
        
        # Utility actions
        self.action_registry.register(
            name='wait',
            category=ActionCategory.TIMING,
            description='[MOCK] Simulate wait/delay',
            handler=self._mock_wait,
            required_params=['duration_ms'],
            optional_params={}
        )
        
        print("✓ Mock action handlers registered (no API calls, no actual automation)")
    
    def _log_action(self, action_name: str, params: Dict[str, Any], result: Any = None):
        """Log action execution for debugging."""
        self.execution_log.append({
            'action': action_name,
            'params': params,
            'result': result,
            'timestamp': time.time()
        })
    
    # Mouse action mocks
    def _mock_mouse_move(self, x: int, y: int, smooth: bool = True, duration_ms: int = 200, **kwargs) -> Dict[str, Any]:
        """Mock mouse movement."""
        print(f"  [MOCK] Moving mouse to ({x}, {y})")
        time.sleep(duration_ms / 1000.0)
        result = {'x': x, 'y': y, 'success': True}
        self._log_action('mouse_move', {'x': x, 'y': y}, result)
        return result
    
    def _mock_mouse_click(self, button: str = 'left', clicks: int = 1, **kwargs) -> Dict[str, Any]:
        """Mock mouse click."""
        print(f"  [MOCK] Clicking {button} button ({clicks}x)")
        time.sleep(0.1)
        result = {'button': button, 'clicks': clicks, 'success': True}
        self._log_action('mouse_click', {'button': button, 'clicks': clicks}, result)
        return result
    
    # Keyboard action mocks
    def _mock_type(self, text: str, interval: float = 0.05, **kwargs) -> Dict[str, Any]:
        """Mock typing text."""
        print(f"  [MOCK] Typing: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        time.sleep(len(text) * interval)
        result = {'text': text, 'length': len(text), 'success': True}
        self._log_action('type', {'text': text}, result)
        return result
    
    def _mock_press_key(self, key: str, **kwargs) -> Dict[str, Any]:
        """Mock key press."""
        print(f"  [MOCK] Pressing key: {key}")
        time.sleep(0.05)
        result = {'key': key, 'success': True}
        self._log_action('press_key', {'key': key}, result)
        return result
    
    def _mock_shortcut(self, keys: list, **kwargs) -> Dict[str, Any]:
        """Mock keyboard shortcut."""
        shortcut_str = '+'.join(keys)
        print(f"  [MOCK] Pressing shortcut: {shortcut_str}")
        time.sleep(0.1)
        result = {'keys': keys, 'success': True}
        self._log_action('shortcut', {'keys': keys}, result)
        return result
    
    # Application action mocks
    def _mock_open_app(self, app_name: str, **kwargs) -> Dict[str, Any]:
        """Mock opening application."""
        print(f"  [MOCK] Opening application: {app_name}")
        time.sleep(1.0)  # Simulate app launch time
        result = {'app_name': app_name, 'success': True}
        self._log_action('open_app', {'app_name': app_name}, result)
        return result
    
    def _mock_open_url(self, url: str, **kwargs) -> Dict[str, Any]:
        """Mock opening URL."""
        print(f"  [MOCK] Opening URL: {url}")
        time.sleep(0.5)
        result = {'url': url, 'success': True}
        self._log_action('open_url', {'url': url}, result)
        return result
    
    # Visual action mocks
    def _mock_visual_navigate(self, task: str, goal: str = None, max_iterations: int = 10, **kwargs) -> Dict[str, Any]:
        """Mock visual navigation."""
        print(f"  [MOCK] Visual navigate: {task}")
        print(f"    Goal: {goal or task}")
        
        # Simulate some iterations
        iterations = random.randint(1, 3)
        for i in range(iterations):
            print(f"    Iteration {i+1}/{iterations}: Analyzing screen...")
            time.sleep(0.3)
        
        # Simulate success
        mock_coords = {'x': random.randint(100, 1800), 'y': random.randint(100, 1000)}
        print(f"    ✓ Found target at ({mock_coords['x']}, {mock_coords['y']})")
        print(f"    ✓ Clicked successfully")
        
        result = {
            'task': task,
            'iterations': iterations,
            'coordinates': mock_coords,
            'success': True
        }
        self._log_action('visual_navigate', {'task': task}, result)
        return result
    
    def _mock_verify_screen(self, context: str, expected: str, confidence_threshold: float = 0.7, **kwargs) -> Dict[str, Any]:
        """Mock screen verification."""
        print(f"  [MOCK] Verifying screen")
        print(f"    Context: {context}")
        print(f"    Expected: {expected}")
        
        time.sleep(0.5)  # Simulate analysis time
        
        # Randomly succeed or fail (80% success rate)
        safe = random.random() > 0.2
        confidence = random.uniform(0.7, 0.95) if safe else random.uniform(0.3, 0.6)
        
        if safe:
            print(f"    ✓ SAFE (confidence: {confidence:.2f})")
            mock_coords = {'x': random.randint(100, 1800), 'y': random.randint(100, 1000)}
            result = {
                'safe_to_proceed': True,
                'confidence': confidence,
                'analysis': f"Mock: {expected} is visible and ready",
                'verified_x': mock_coords['x'],
                'verified_y': mock_coords['y']
            }
        else:
            print(f"    ✗ NOT SAFE (confidence: {confidence:.2f})")
            result = {
                'safe_to_proceed': False,
                'confidence': confidence,
                'analysis': f"Mock: {expected} is not visible or not ready",
                'suggested_actions': ['Wait for page to load', 'Refresh the page']
            }
        
        self._log_action('verify_screen', {'context': context, 'expected': expected}, result)
        return result
    
    # Utility action mocks
    def _mock_wait(self, duration_ms: int, **kwargs) -> Dict[str, Any]:
        """Mock wait/delay."""
        print(f"  [MOCK] Waiting {duration_ms}ms")
        time.sleep(duration_ms / 1000.0)
        result = {'duration_ms': duration_ms, 'success': True}
        self._log_action('wait', {'duration_ms': duration_ms}, result)
        return result
    
    def get_execution_log(self) -> list:
        """Get the execution log."""
        return self.execution_log
    
    def clear_log(self):
        """Clear the execution log."""
        self.execution_log = []
        print("  Execution log cleared")
    
    def print_summary(self):
        """Print execution summary."""
        print(f"\n{'='*60}")
        print(f"MOCK EXECUTION SUMMARY")
        print(f"{'='*60}")
        print(f"Total actions executed: {len(self.execution_log)}")
        
        # Count by action type
        action_counts = {}
        for entry in self.execution_log:
            action = entry['action']
            action_counts[action] = action_counts.get(action, 0) + 1
        
        print(f"\nActions by type:")
        for action, count in sorted(action_counts.items()):
            print(f"  {action}: {count}")
        
        print(f"{'='*60}\n")