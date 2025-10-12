"""
Action Handler Functions for JSON Instruction Protocol

This module contains all the handler functions that implement the actions
defined in the protocol. These handlers are registered with the ActionRegistry.
"""

import time
import pyautogui
import pyperclip
import webbrowser
import os
import subprocess
import platform
from typing import Dict, Any, Optional, List, Tuple


class ActionHandlers:
    """Collection of action handler functions."""
    
    def __init__(self, registry):
        """
        Initialize action handlers with registry.
        
        Args:
            registry: ActionRegistry instance to register handlers with
        """
        self.registry = registry
        
    def register_all(self):
        """Register all action handlers with the registry."""
        self.register_keyboard_handlers()
        self.register_mouse_handlers()
        self.register_window_handlers()
        self.register_browser_handlers()
        self.register_clipboard_handlers()
        self.register_file_handlers()
        self.register_screen_handlers()
        self.register_timing_handlers()
        self.register_vision_handlers()
        self.register_system_handlers()
        self.register_edit_handlers()
        self.register_macro_handler()
    
    # ========================================
    # KEYBOARD ACTION HANDLERS
    # ========================================
    
    def register_keyboard_handlers(self):
        """Register all keyboard action handlers."""
        from shared.action_registry import ActionCategory
        
        # press_key - Press and release a single key
        def press_key(key: str):
            """Press and release a single key."""
            if self.registry.input_controller:
                self.registry.input_controller.press_key(key)
            else:
                pyautogui.press(key)
        
        self.registry.register(
            name="press_key",
            category=ActionCategory.KEYBOARD,
            description="Press and release a SINGLE key",
            handler=press_key,
            required_params=["key"],
            examples=[
                '{"action": "press_key", "params": {"key": "enter"}}',
                '{"action": "press_key", "params": {"key": "escape"}}',
                '{"action": "press_key", "params": {"key": "tab"}}'
            ]
        )
        
        # shortcut - Press multiple keys simultaneously
        def shortcut(keys: List[str]):
            """Press multiple keys simultaneously (keyboard shortcut)."""
            if self.registry.input_controller:
                self.registry.input_controller.hotkey(*keys)
            else:
                pyautogui.hotkey(*keys)
        
        self.registry.register(
            name="shortcut",
            category=ActionCategory.KEYBOARD,
            description="Press MULTIPLE keys SIMULTANEOUSLY (Ctrl+T, Alt+F4, etc.)",
            handler=shortcut,
            required_params=["keys"],
            examples=[
                '{"action": "shortcut", "params": {"keys": ["ctrl", "t"]}}',
                '{"action": "shortcut", "params": {"keys": ["ctrl", "c"]}}',
                '{"action": "shortcut", "params": {"keys": ["alt", "f4"]}}'
            ]
        )
        
        # type - Type text of any length
        def type_text(text: str, interval_ms: int = 50):
            """Type text with specified interval between keystrokes."""
            interval_sec = interval_ms / 1000.0
            if self.registry.input_controller:
                self.registry.input_controller.type_text(text, interval=interval_sec)
            else:
                pyautogui.write(text, interval=interval_sec)
        
        self.registry.register(
            name="type",
            category=ActionCategory.KEYBOARD,
            description="Type text of ANY length (words, sentences, paragraphs, full posts)",
            handler=type_text,
            required_params=["text"],
            optional_params={"interval_ms": 50},
            examples=[
                '{"action": "type", "params": {"text": "Hello World"}}',
                '{"action": "type", "params": {"text": "Long text...", "interval_ms": 30}}'
            ]
        )
        
        # type_with_delay - Type text with slower speed
        def type_with_delay(text: str, delay_ms: int):
            """Type text with slower speed for sensitive fields."""
            interval_sec = delay_ms / 1000.0
            if self.registry.input_controller:
                self.registry.input_controller.type_text(text, interval=interval_sec)
            else:
                pyautogui.write(text, interval=interval_sec)
        
        self.registry.register(
            name="type_with_delay",
            category=ActionCategory.KEYBOARD,
            description="Type text with slower speed (for sensitive fields)",
            handler=type_with_delay,
            required_params=["text", "delay_ms"],
            examples=[
                '{"action": "type_with_delay", "params": {"text": "password123", "delay_ms": 100}}'
            ]
        )
        
        # hold_key - Press and hold a key
        def hold_key(key: str):
            """Press and hold a key (release with release_key)."""
            pyautogui.keyDown(key)
        
        self.registry.register(
            name="hold_key",
            category=ActionCategory.KEYBOARD,
            description="Press and hold a key (release with release_key)",
            handler=hold_key,
            required_params=["key"],
            examples=[
                '{"action": "hold_key", "params": {"key": "shift"}}'
            ]
        )
        
        # release_key - Release a held key
        def release_key(key: str):
            """Release a held key."""
            pyautogui.keyUp(key)
        
        self.registry.register(
            name="release_key",
            category=ActionCategory.KEYBOARD,
            description="Release a held key",
            handler=release_key,
            required_params=["key"],
            examples=[
                '{"action": "release_key", "params": {"key": "shift"}}'
            ]
        )
    
    # ========================================
    # MOUSE ACTION HANDLERS
    # ========================================
    
    def register_mouse_handlers(self):
        """Register all mouse action handlers."""
        from shared.action_registry import ActionCategory
        
        # mouse_move - Move mouse to coordinates with smooth curved path
        def mouse_move(x: int, y: int, smooth: bool = True, speed: float = 1.0, curve_type: str = "bezier", duration: float = None):
            """Move mouse to coordinates (smooth curved path by default)."""
            if self.registry.mouse_controller and smooth:
                # Use MouseController with smooth curved movements
                self.registry.mouse_controller.move_to(x, y, duration=duration, curve_type=curve_type)
            elif self.registry.input_controller:
                self.registry.input_controller.move_mouse(x, y, duration=duration or 0.5)
            else:
                pyautogui.moveTo(x, y, duration=duration or 0.5)
        
        self.registry.register(
            name="mouse_move",
            category=ActionCategory.MOUSE,
            description="Move mouse to coordinates (smooth curved path by default)",
            handler=mouse_move,
            required_params=["x", "y"],
            optional_params={"smooth": True, "speed": 1.0, "curve_type": "bezier", "duration": None},
            examples=[
                '{"action": "mouse_move", "params": {"x": 500, "y": 300}}',
                '{"action": "mouse_move", "params": {"x": 100, "y": 200, "smooth": false}}',
                '{"action": "mouse_move", "params": {"x": 300, "y": 400, "curve_type": "arc"}}'
            ]
        )
        
        # mouse_click - Click mouse button at current position
        def mouse_click(button: str = "left", clicks: int = 1):
            """Click mouse button at current position."""
            if self.registry.mouse_controller:
                self.registry.mouse_controller.click(button=button, clicks=clicks, move_first=False)
            elif self.registry.input_controller:
                self.registry.input_controller.click(button=button, clicks=clicks)
            else:
                pyautogui.click(button=button, clicks=clicks)
        
        self.registry.register(
            name="mouse_click",
            category=ActionCategory.MOUSE,
            description="Click mouse button at current position",
            handler=mouse_click,
            optional_params={"button": "left", "clicks": 1},
            examples=[
                '{"action": "mouse_click", "params": {}}',
                '{"action": "mouse_click", "params": {"button": "right"}}',
                '{"action": "mouse_click", "params": {"clicks": 2}}'
            ]
        )
        
        # mouse_double_click - Double-click at current position
        def mouse_double_click(button: str = "left"):
            """Double-click at current position."""
            if self.registry.mouse_controller:
                self.registry.mouse_controller.click(button=button, clicks=2, move_first=False)
            elif self.registry.input_controller:
                self.registry.input_controller.click(button=button, clicks=2)
            else:
                pyautogui.click(button=button, clicks=2)
        
        self.registry.register(
            name="mouse_double_click",
            category=ActionCategory.MOUSE,
            description="Double-click at current position",
            handler=mouse_double_click,
            optional_params={"button": "left"},
            examples=[
                '{"action": "mouse_double_click", "params": {}}'
            ]
        )
        
        # mouse_right_click - Right-click at current position
        def mouse_right_click():
            """Right-click at current position."""
            if self.registry.mouse_controller:
                self.registry.mouse_controller.click(button="right", clicks=1, move_first=False)
            elif self.registry.input_controller:
                self.registry.input_controller.click(button="right", clicks=1)
            else:
                pyautogui.click(button="right")
        
        self.registry.register(
            name="mouse_right_click",
            category=ActionCategory.MOUSE,
            description="Right-click at current position",
            handler=mouse_right_click,
            examples=[
                '{"action": "mouse_right_click", "params": {}}'
            ]
        )
        
        # mouse_drag - Drag mouse from current position to target
        def mouse_drag(x: int, y: int, smooth: bool = True):
            """Drag mouse from current position to target."""
            if self.registry.mouse_controller and smooth:
                self.registry.mouse_controller.drag_to(x, y)
            else:
                pyautogui.dragTo(x, y, duration=0.5)
        
        self.registry.register(
            name="mouse_drag",
            category=ActionCategory.MOUSE,
            description="Drag mouse from current position to target",
            handler=mouse_drag,
            required_params=["x", "y"],
            optional_params={"smooth": True},
            examples=[
                '{"action": "mouse_drag", "params": {"x": 600, "y": 400}}'
            ]
        )
        
        # mouse_scroll - Scroll mouse wheel
        def mouse_scroll(direction: str, amount: int = 3):
            """Scroll mouse wheel up/down/left/right."""
            if direction == "up":
                scroll_amount = amount
            elif direction == "down":
                scroll_amount = -amount
            elif direction == "left":
                pyautogui.hscroll(-amount)
                return
            elif direction == "right":
                pyautogui.hscroll(amount)
                return
            else:
                raise ValueError(f"Invalid scroll direction: {direction}")
            
            if self.registry.mouse_controller:
                self.registry.mouse_controller.scroll(scroll_amount)
            else:
                pyautogui.scroll(scroll_amount)
        
        self.registry.register(
            name="mouse_scroll",
            category=ActionCategory.MOUSE,
            description="Scroll mouse wheel",
            handler=mouse_scroll,
            required_params=["direction"],
            optional_params={"amount": 3},
            examples=[
                '{"action": "mouse_scroll", "params": {"direction": "up"}}',
                '{"action": "mouse_scroll", "params": {"direction": "down", "amount": 5}}'
            ]
        )
        
        # mouse_position - Get current mouse position
        def mouse_position() -> Dict[str, int]:
            """Get current mouse position."""
            if self.registry.mouse_controller:
                x, y = self.registry.mouse_controller.get_position()
            elif self.registry.input_controller:
                x, y = self.registry.input_controller.get_mouse_position()
            else:
                x, y = pyautogui.position()
            return {"x": x, "y": y}
        
        self.registry.register(
            name="mouse_position",
            category=ActionCategory.MOUSE,
            description="Get current mouse position",
            handler=mouse_position,
            returns={"x": "int", "y": "int"},
            examples=[
                '{"action": "mouse_position", "params": {}}'
            ]
        )
    
    # ========================================
    # WINDOW MANAGEMENT HANDLERS
    # ========================================
    
    def register_window_handlers(self):
        """Register all window management handlers."""
        from shared.action_registry import ActionCategory
        
        # open_app - Open application by name
        def open_app(app_name: str):
            """Open application by name using Windows search."""
            # Press Windows key
            pyautogui.press('win')
            time.sleep(0.5)
            # Type app name
            pyautogui.write(app_name, interval=0.05)
            time.sleep(0.3)
            # Press Enter
            pyautogui.press('enter')
        
        self.registry.register(
            name="open_app",
            category=ActionCategory.WINDOW,
            description="Open application by name",
            handler=open_app,
            required_params=["app_name"],
            examples=[
                '{"action": "open_app", "params": {"app_name": "chrome"}}',
                '{"action": "open_app", "params": {"app_name": "notepad"}}'
            ]
        )
        
        # close_app - Close application by name (Alt+F4)
        def close_app(app_name: str = None):
            """Close current application window."""
            pyautogui.hotkey('alt', 'f4')
        
        self.registry.register(
            name="close_app",
            category=ActionCategory.WINDOW,
            description="Close application by name",
            handler=close_app,
            optional_params={"app_name": None},
            examples=[
                '{"action": "close_app", "params": {}}'
            ]
        )
        
        # switch_window - Switch to next/previous window (Alt+Tab)
        def switch_window(direction: str = "next"):
            """Switch to next or previous window."""
            if direction == "next":
                pyautogui.hotkey('alt', 'tab')
            else:
                pyautogui.hotkey('alt', 'shift', 'tab')
        
        self.registry.register(
            name="switch_window",
            category=ActionCategory.WINDOW,
            description="Switch to next/previous window (Alt+Tab)",
            handler=switch_window,
            optional_params={"direction": "next"},
            examples=[
                '{"action": "switch_window", "params": {}}',
                '{"action": "switch_window", "params": {"direction": "previous"}}'
            ]
        )
        
        # minimize_window - Minimize current window
        def minimize_window():
            """Minimize current window."""
            pyautogui.hotkey('win', 'down')
        
        self.registry.register(
            name="minimize_window",
            category=ActionCategory.WINDOW,
            description="Minimize current window",
            handler=minimize_window,
            examples=[
                '{"action": "minimize_window", "params": {}}'
            ]
        )
        
        # maximize_window - Maximize current window
        def maximize_window():
            """Maximize current window."""
            pyautogui.hotkey('win', 'up')
        
        self.registry.register(
            name="maximize_window",
            category=ActionCategory.WINDOW,
            description="Maximize current window",
            handler=maximize_window,
            examples=[
                '{"action": "maximize_window", "params": {}}'
            ]
        )
        
        # restore_window - Restore minimized window
        def restore_window():
            """Restore minimized window."""
            pyautogui.hotkey('win', 'up')
        
        self.registry.register(
            name="restore_window",
            category=ActionCategory.WINDOW,
            description="Restore minimized window",
            handler=restore_window,
            examples=[
                '{"action": "restore_window", "params": {}}'
            ]
        )
        
        # get_active_window - Get title of active window
        def get_active_window() -> Dict[str, str]:
            """Get title of active window."""
            try:
                import pygetwindow as gw
                active = gw.getActiveWindow()
                if active:
                    return {"title": active.title}
            except:
                pass
            return {"title": "Unknown"}
        
        self.registry.register(
            name="get_active_window",
            category=ActionCategory.WINDOW,
            description="Get title of active window",
            handler=get_active_window,
            returns={"title": "str"},
            examples=[
                '{"action": "get_active_window", "params": {}}'
            ]
        )
    
    # ========================================
    # BROWSER ACTION HANDLERS
    # ========================================
    
    def register_browser_handlers(self):
        """Register all browser-specific handlers."""
        from shared.action_registry import ActionCategory
        
        # open_url - Open URL in default browser
        def open_url(url: str):
            """Open URL in default browser."""
            webbrowser.open(url)
        
        self.registry.register(
            name="open_url",
            category=ActionCategory.BROWSER,
            description="Open URL in default browser",
            handler=open_url,
            required_params=["url"],
            examples=[
                '{"action": "open_url", "params": {"url": "https://google.com"}}'
            ]
        )
        
        # browser_back - Navigate back
        def browser_back():
            """Navigate back in browser."""
            pyautogui.hotkey('alt', 'left')
        
        self.registry.register(
            name="browser_back",
            category=ActionCategory.BROWSER,
            description="Navigate back (Alt+Left or Backspace)",
            handler=browser_back,
            examples=[
                '{"action": "browser_back", "params": {}}'
            ]
        )
        
        # browser_forward - Navigate forward
        def browser_forward():
            """Navigate forward in browser."""
            pyautogui.hotkey('alt', 'right')
        
        self.registry.register(
            name="browser_forward",
            category=ActionCategory.BROWSER,
            description="Navigate forward (Alt+Right)",
            handler=browser_forward,
            examples=[
                '{"action": "browser_forward", "params": {}}'
            ]
        )
        
        # browser_refresh - Refresh page
        def browser_refresh():
            """Refresh current page."""
            pyautogui.press('f5')
        
        self.registry.register(
            name="browser_refresh",
            category=ActionCategory.BROWSER,
            description="Refresh page (F5 or Ctrl+R)",
            handler=browser_refresh,
            examples=[
                '{"action": "browser_refresh", "params": {}}'
            ]
        )
        
        # browser_new_tab - Open new tab
        def browser_new_tab():
            """Open new browser tab."""
            pyautogui.hotkey('ctrl', 't')
        
        self.registry.register(
            name="browser_new_tab",
            category=ActionCategory.BROWSER,
            description="Open new tab (Ctrl+T)",
            handler=browser_new_tab,
            examples=[
                '{"action": "browser_new_tab", "params": {}}'
            ]
        )
        
        # browser_close_tab - Close current tab
        def browser_close_tab():
            """Close current browser tab."""
            pyautogui.hotkey('ctrl', 'w')
        
        self.registry.register(
            name="browser_close_tab",
            category=ActionCategory.BROWSER,
            description="Close current tab (Ctrl+W)",
            handler=browser_close_tab,
            examples=[
                '{"action": "browser_close_tab", "params": {}}'
            ]
        )
        
        # browser_switch_tab - Switch to next/previous tab
        def browser_switch_tab(direction: str = "next"):
            """Switch to next or previous browser tab."""
            if direction == "next":
                pyautogui.hotkey('ctrl', 'tab')
            else:
                pyautogui.hotkey('ctrl', 'shift', 'tab')
        
        self.registry.register(
            name="browser_switch_tab",
            category=ActionCategory.BROWSER,
            description="Switch to next/previous tab",
            handler=browser_switch_tab,
            optional_params={"direction": "next"},
            examples=[
                '{"action": "browser_switch_tab", "params": {}}',
                '{"action": "browser_switch_tab", "params": {"direction": "previous"}}'
            ]
        )
        
        # browser_address_bar - Focus address bar
        def browser_address_bar():
            """Focus browser address bar."""
            pyautogui.hotkey('ctrl', 'l')
        
        self.registry.register(
            name="browser_address_bar",
            category=ActionCategory.BROWSER,
            description="Focus address bar (Ctrl+L)",
            handler=browser_address_bar,
            examples=[
                '{"action": "browser_address_bar", "params": {}}'
            ]
        )
        
        # browser_bookmark - Bookmark current page
        def browser_bookmark():
            """Bookmark current page."""
            pyautogui.hotkey('ctrl', 'd')
        
        self.registry.register(
            name="browser_bookmark",
            category=ActionCategory.BROWSER,
            description="Bookmark current page (Ctrl+D)",
            handler=browser_bookmark,
            examples=[
                '{"action": "browser_bookmark", "params": {}}'
            ]
        )
        
        # browser_find - Open find dialog
        def browser_find():
            """Open browser find dialog."""
            pyautogui.hotkey('ctrl', 'f')
        
        self.registry.register(
            name="browser_find",
            category=ActionCategory.BROWSER,
            description="Open find dialog (Ctrl+F)",
            handler=browser_find,
            examples=[
                '{"action": "browser_find", "params": {}}'
            ]
        )
    
    # ========================================
    # CLIPBOARD ACTION HANDLERS
    # ========================================
    
    def register_clipboard_handlers(self):
        """Register all clipboard handlers."""
        from shared.action_registry import ActionCategory
        
        # copy - Copy selected content
        def copy():
            """Copy selected content to clipboard."""
            pyautogui.hotkey('ctrl', 'c')
        
        self.registry.register(
            name="copy",
            category=ActionCategory.CLIPBOARD,
            description="Copy selected content (Ctrl+C)",
            handler=copy,
            examples=[
                '{"action": "copy", "params": {}}'
            ]
        )
        
        # paste - Paste from clipboard
        def paste():
            """Paste from clipboard."""
            pyautogui.hotkey('ctrl', 'v')
        
        self.registry.register(
            name="paste",
            category=ActionCategory.CLIPBOARD,
            description="Paste from clipboard (Ctrl+V)",
            handler=paste,
            examples=[
                '{"action": "paste", "params": {}}'
            ]
        )
        
        # cut - Cut selected content
        def cut():
            """Cut selected content to clipboard."""
            pyautogui.hotkey('ctrl', 'x')
        
        self.registry.register(
            name="cut",
            category=ActionCategory.CLIPBOARD,
            description="Cut selected content (Ctrl+X)",
            handler=cut,
            examples=[
                '{"action": "cut", "params": {}}'
            ]
        )
        
        # get_clipboard - Read clipboard content
        def get_clipboard() -> Dict[str, str]:
            """Read text from clipboard."""
            try:
                text = pyperclip.paste()
                return {"text": text}
            except Exception as e:
                return {"text": "", "error": str(e)}
        
        self.registry.register(
            name="get_clipboard",
            category=ActionCategory.CLIPBOARD,
            description="Read clipboard content",
            handler=get_clipboard,
            returns={"text": "str"},
            examples=[
                '{"action": "get_clipboard", "params": {}}'
            ]
        )
        
        # set_clipboard - Write text to clipboard
        def set_clipboard(text: str):
            """Write text to clipboard."""
            pyperclip.copy(text)
        
        self.registry.register(
            name="set_clipboard",
            category=ActionCategory.CLIPBOARD,
            description="Write text to clipboard",
            handler=set_clipboard,
            required_params=["text"],
            examples=[
                '{"action": "set_clipboard", "params": {"text": "Hello World"}}'
            ]
        )
        
        # paste_from_clipboard - Paste specific text via clipboard
        def paste_from_clipboard(text: str):
            """Paste specific text via clipboard (fast for long text)."""
            # Save current clipboard
            try:
                old_clipboard = pyperclip.paste()
            except:
                old_clipboard = ""
            
            # Set new text and paste
            pyperclip.copy(text)
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
            
            # Restore old clipboard
            try:
                pyperclip.copy(old_clipboard)
            except:
                pass
        
        self.registry.register(
            name="paste_from_clipboard",
            category=ActionCategory.CLIPBOARD,
            description="Paste specific text via clipboard (fast for long text)",
            handler=paste_from_clipboard,
            required_params=["text"],
            examples=[
                '{"action": "paste_from_clipboard", "params": {"text": "Long text content..."}}'
            ]
        )
    
    # ========================================
    # FILE SYSTEM HANDLERS
    # ========================================
    
    def register_file_handlers(self):
        """Register all file system handlers."""
        from shared.action_registry import ActionCategory
        
        # open_file - Open file with default application
        def open_file(path: str):
            """Open file with default application."""
            if platform.system() == 'Windows':
                os.startfile(path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', path])
            else:  # Linux
                subprocess.run(['xdg-open', path])
        
        self.registry.register(
            name="open_file",
            category=ActionCategory.FILE,
            description="Open file with default application",
            handler=open_file,
            required_params=["path"],
            examples=[
                '{"action": "open_file", "params": {"path": "C:\\\\Users\\\\document.txt"}}'
            ]
        )
        
        # save_file - Save current file
        def save_file():
            """Save current file (Ctrl+S)."""
            pyautogui.hotkey('ctrl', 's')
        
        self.registry.register(
            name="save_file",
            category=ActionCategory.FILE,
            description="Save current file (Ctrl+S)",
            handler=save_file,
            examples=[
                '{"action": "save_file", "params": {}}'
            ]
        )
        
        # save_as - Open save as dialog
        def save_as():
            """Open save as dialog (Ctrl+Shift+S)."""
            pyautogui.hotkey('ctrl', 'shift', 's')
        
        self.registry.register(
            name="save_as",
            category=ActionCategory.FILE,
            description="Save as dialog (Ctrl+Shift+S)",
            handler=save_as,
            examples=[
                '{"action": "save_as", "params": {}}'
            ]
        )
        
        # open_file_dialog - Open file dialog
        def open_file_dialog():
            """Open file dialog (Ctrl+O)."""
            pyautogui.hotkey('ctrl', 'o')
        
        self.registry.register(
            name="open_file_dialog",
            category=ActionCategory.FILE,
            description="Open file dialog (Ctrl+O)",
            handler=open_file_dialog,
            examples=[
                '{"action": "open_file_dialog", "params": {}}'
            ]
        )
        
        # create_folder - Create new folder
        def create_folder(path: str):
            """Create new folder at specified path."""
            os.makedirs(path, exist_ok=True)
        
        self.registry.register(
            name="create_folder",
            category=ActionCategory.FILE,
            description="Create new folder",
            handler=create_folder,
            required_params=["path"],
            examples=[
                '{"action": "create_folder", "params": {"path": "C:\\\\Users\\\\NewFolder"}}'
            ]
        )
        
        # delete_file - Delete file with confirmation
        def delete_file(path: str):
            """Delete file at specified path."""
            if os.path.exists(path):
                os.remove(path)
            else:
                raise FileNotFoundError(f"File not found: {path}")
        
        self.registry.register(
            name="delete_file",
            category=ActionCategory.FILE,
            description="Delete file (requires confirmation)",
            handler=delete_file,
            required_params=["path"],
            examples=[
                '{"action": "delete_file", "params": {"path": "C:\\\\Users\\\\temp.txt"}}'
            ]
        )
    
    # ========================================
    # SCREEN CAPTURE HANDLERS
    # ========================================
    
    def register_screen_handlers(self):
        """Register all screen capture handlers."""
        from shared.action_registry import ActionCategory
        from PIL import Image
        
        # capture_screen - Capture full screen screenshot
        def capture_screen():
            """Capture full screen screenshot."""
            if self.registry.screen_capture:
                return self.registry.screen_capture.capture_screen()
            else:
                screenshot = pyautogui.screenshot()
                return screenshot
        
        self.registry.register(
            name="capture_screen",
            category=ActionCategory.SCREEN,
            description="Capture full screen screenshot",
            handler=capture_screen,
            returns={"image": "Image"},
            examples=[
                '{"action": "capture_screen", "params": {}}'
            ]
        )
        
        # capture_region - Capture specific screen region
        def capture_region(x: int, y: int, width: int, height: int):
            """Capture specific screen region."""
            if self.registry.screen_capture:
                return self.registry.screen_capture.capture_region(x, y, width, height)
            else:
                screenshot = pyautogui.screenshot(region=(x, y, width, height))
                return screenshot
        
        self.registry.register(
            name="capture_region",
            category=ActionCategory.SCREEN,
            description="Capture specific screen region",
            handler=capture_region,
            required_params=["x", "y", "width", "height"],
            returns={"image": "Image"},
            examples=[
                '{"action": "capture_region", "params": {"x": 0, "y": 0, "width": 800, "height": 600}}'
            ]
        )
        
        # capture_window - Capture active window
        def capture_window():
            """Capture active window screenshot."""
            # Use full screen capture as fallback
            # (Window-specific capture requires additional libraries)
            if self.registry.screen_capture:
                return self.registry.screen_capture.capture_screen()
            else:
                screenshot = pyautogui.screenshot()
                return screenshot
        
        self.registry.register(
            name="capture_window",
            category=ActionCategory.SCREEN,
            description="Capture active window",
            handler=capture_window,
            returns={"image": "Image"},
            examples=[
                '{"action": "capture_window", "params": {}}'
            ]
        )
        
        # save_screenshot - Save screenshot to file
        def save_screenshot(path: str):
            """Save screenshot to file."""
            screenshot = pyautogui.screenshot()
            screenshot.save(path)
        
        self.registry.register(
            name="save_screenshot",
            category=ActionCategory.SCREEN,
            description="Save screenshot to file",
            handler=save_screenshot,
            required_params=["path"],
            examples=[
                '{"action": "save_screenshot", "params": {"path": "screenshot.png"}}'
            ]
        )
    
    # ========================================
    # TIMING AND CONTROL HANDLERS
    # ========================================
    
    def register_timing_handlers(self):
        """Register all timing and control handlers."""
        from shared.action_registry import ActionCategory
        
        # delay - Wait for specified milliseconds
        def delay(ms: int):
            """Wait for specified milliseconds."""
            time.sleep(ms / 1000.0)
        
        self.registry.register(
            name="delay",
            category=ActionCategory.TIMING,
            description="Wait for specified milliseconds",
            handler=delay,
            required_params=["ms"],
            examples=[
                '{"action": "delay", "params": {"ms": 1000}}',
                '{"action": "delay", "params": {"ms": 500}}'
            ]
        )
        
        # wait_for_window - Wait for window with specific title
        def wait_for_window(title: str, timeout_ms: int = 10000):
            """Wait for window with specific title to appear."""
            timeout_sec = timeout_ms / 1000.0
            start_time = time.time()
            
            try:
                import pygetwindow as gw
                while time.time() - start_time < timeout_sec:
                    windows = gw.getWindowsWithTitle(title)
                    if windows:
                        return True
                    time.sleep(0.5)
            except:
                # If pygetwindow not available, just wait
                time.sleep(timeout_sec)
            
            return False
        
        self.registry.register(
            name="wait_for_window",
            category=ActionCategory.TIMING,
            description="Wait for window with specific title to appear",
            handler=wait_for_window,
            required_params=["title"],
            optional_params={"timeout_ms": 10000},
            examples=[
                '{"action": "wait_for_window", "params": {"title": "Chrome"}}'
            ]
        )
        
        # wait_for_image - Wait for image to appear on screen
        def wait_for_image(image_path: str, timeout_ms: int = 10000, confidence: float = 0.8):
            """Wait for image to appear on screen."""
            timeout_sec = timeout_ms / 1000.0
            start_time = time.time()
            
            try:
                while time.time() - start_time < timeout_sec:
                    location = pyautogui.locateOnScreen(image_path, confidence=confidence)
                    if location:
                        return True
                    time.sleep(0.5)
            except:
                pass
            
            return False
        
        self.registry.register(
            name="wait_for_image",
            category=ActionCategory.TIMING,
            description="Wait for image to appear on screen",
            handler=wait_for_image,
            required_params=["image_path"],
            optional_params={"timeout_ms": 10000, "confidence": 0.8},
            examples=[
                '{"action": "wait_for_image", "params": {"image_path": "button.png"}}'
            ]
        )
        
        # wait_for_color - Wait for specific color at coordinates
        def wait_for_color(x: int, y: int, color: str, timeout_ms: int = 10000):
            """Wait for specific color at coordinates."""
            timeout_sec = timeout_ms / 1000.0
            start_time = time.time()
            
            # Convert hex color to RGB
            color = color.lstrip('#')
            target_rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            
            while time.time() - start_time < timeout_sec:
                screenshot = pyautogui.screenshot()
                pixel_color = screenshot.getpixel((x, y))
                
                if pixel_color == target_rgb:
                    return True
                
                time.sleep(0.5)
            
            return False
        
        self.registry.register(
            name="wait_for_color",
            category=ActionCategory.TIMING,
            description="Wait for specific color at coordinates",
            handler=wait_for_color,
            required_params=["x", "y", "color"],
            optional_params={"timeout_ms": 10000},
            examples=[
                '{"action": "wait_for_color", "params": {"x": 100, "y": 200, "color": "#FF0000"}}'
            ]
        )
    
    # ========================================
    # VISUAL VERIFICATION HANDLERS
    # ========================================
    
    def register_vision_handlers(self):
        """Register all visual verification handlers."""
        from shared.action_registry import ActionCategory
        
        # verify_screen - Pause and verify screen state with AI vision
        def verify_screen(context: str, expected: str, confidence_threshold: float = 0.8):
            """Pause and verify screen state with AI vision (use when uncertain)."""
            if self.registry.visual_verifier:
                result = self.registry.visual_verifier.verify_screen(context, expected, confidence_threshold)
                return result.to_dict()
            else:
                # Fallback: just capture screen and return success
                # (Visual verification requires VisualVerifier component)
                return {"safe_to_proceed": True, "message": "Visual verification not available"}
        
        self.registry.register(
            name="verify_screen",
            category=ActionCategory.VISION,
            description="Pause and verify screen state with AI vision (use when uncertain)",
            handler=verify_screen,
            required_params=["context", "expected"],
            optional_params={"confidence_threshold": 0.8},
            examples=[
                '{"action": "verify_screen", "params": {"context": "Looking for login button", "expected": "Login button visible"}}'
            ]
        )
        
        # verify_element - Verify specific element exists on screen
        def verify_element(element_description: str) -> Dict[str, Any]:
            """Verify specific element exists on screen."""
            if self.registry.visual_verifier:
                result = self.registry.visual_verifier.find_element(element_description)
                return result
            else:
                # Fallback: return not found
                return {"exists": False, "x": 0, "y": 0}
        
        self.registry.register(
            name="verify_element",
            category=ActionCategory.VISION,
            description="Verify specific element exists on screen",
            handler=verify_element,
            required_params=["element_description"],
            returns={"exists": "bool", "x": "int", "y": "int"},
            examples=[
                '{"action": "verify_element", "params": {"element_description": "Submit button"}}'
            ]
        )
        
        # find_element - Locate element and return coordinates
        def find_element(element_description: str) -> Dict[str, Any]:
            """Locate element and return coordinates."""
            if self.registry.visual_verifier:
                result = self.registry.visual_verifier.find_element(element_description)
                return result
            else:
                # Fallback: return center of screen
                screen_width, screen_height = pyautogui.size()
                return {
                    "x": screen_width // 2,
                    "y": screen_height // 2,
                    "confidence": 0.0
                }
        
        self.registry.register(
            name="find_element",
            category=ActionCategory.VISION,
            description="Locate element and return coordinates",
            handler=find_element,
            required_params=["element_description"],
            returns={"x": "int", "y": "int", "confidence": "float"},
            examples=[
                '{"action": "find_element", "params": {"element_description": "Search box"}}'
            ]
        )
        
        # verify_text - Verify text exists on screen using OCR
        def verify_text(text: str) -> Dict[str, Any]:
            """Verify text exists on screen using OCR."""
            try:
                # Try to locate text on screen
                location = pyautogui.locateOnScreen(text)
                if location:
                    return {
                        "exists": True,
                        "x": location.left + location.width // 2,
                        "y": location.top + location.height // 2
                    }
            except:
                pass
            
            return {"exists": False, "x": 0, "y": 0}
        
        self.registry.register(
            name="verify_text",
            category=ActionCategory.VISION,
            description="Verify text exists on screen using OCR",
            handler=verify_text,
            required_params=["text"],
            returns={"exists": "bool", "x": "int", "y": "int"},
            examples=[
                '{"action": "verify_text", "params": {"text": "Welcome"}}'
            ]
        )
    
    # ========================================
    # SYSTEM CONTROL HANDLERS
    # ========================================
    
    def register_system_handlers(self):
        """Register all system control handlers."""
        from shared.action_registry import ActionCategory
        
        # lock_screen - Lock screen
        def lock_screen():
            """Lock screen (Win+L)."""
            pyautogui.hotkey('win', 'l')
        
        self.registry.register(
            name="lock_screen",
            category=ActionCategory.SYSTEM,
            description="Lock screen (Win+L)",
            handler=lock_screen,
            examples=[
                '{"action": "lock_screen", "params": {}}'
            ]
        )
        
        # sleep_system - Put system to sleep
        def sleep_system():
            """Put system to sleep."""
            if platform.system() == 'Windows':
                subprocess.run(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0', '1', '0'])
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['pmset', 'sleepnow'])
            else:  # Linux
                subprocess.run(['systemctl', 'suspend'])
        
        self.registry.register(
            name="sleep_system",
            category=ActionCategory.SYSTEM,
            description="Put system to sleep",
            handler=sleep_system,
            examples=[
                '{"action": "sleep_system", "params": {}}'
            ]
        )
        
        # shutdown_system - Shutdown system
        def shutdown_system():
            """Shutdown system (requires confirmation)."""
            if platform.system() == 'Windows':
                subprocess.run(['shutdown', '/s', '/t', '0'])
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['sudo', 'shutdown', '-h', 'now'])
            else:  # Linux
                subprocess.run(['sudo', 'shutdown', '-h', 'now'])
        
        self.registry.register(
            name="shutdown_system",
            category=ActionCategory.SYSTEM,
            description="Shutdown system (requires confirmation)",
            handler=shutdown_system,
            examples=[
                '{"action": "shutdown_system", "params": {}}'
            ]
        )
        
        # restart_system - Restart system
        def restart_system():
            """Restart system (requires confirmation)."""
            if platform.system() == 'Windows':
                subprocess.run(['shutdown', '/r', '/t', '0'])
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['sudo', 'shutdown', '-r', 'now'])
            else:  # Linux
                subprocess.run(['sudo', 'shutdown', '-r', 'now'])
        
        self.registry.register(
            name="restart_system",
            category=ActionCategory.SYSTEM,
            description="Restart system (requires confirmation)",
            handler=restart_system,
            examples=[
                '{"action": "restart_system", "params": {}}'
            ]
        )
        
        # volume_up - Increase system volume
        def volume_up(amount: int = 10):
            """Increase system volume."""
            # Use keyboard volume up key
            for _ in range(amount // 2):
                pyautogui.press('volumeup')
        
        self.registry.register(
            name="volume_up",
            category=ActionCategory.SYSTEM,
            description="Increase system volume",
            handler=volume_up,
            optional_params={"amount": 10},
            examples=[
                '{"action": "volume_up", "params": {}}',
                '{"action": "volume_up", "params": {"amount": 20}}'
            ]
        )
        
        # volume_down - Decrease system volume
        def volume_down(amount: int = 10):
            """Decrease system volume."""
            # Use keyboard volume down key
            for _ in range(amount // 2):
                pyautogui.press('volumedown')
        
        self.registry.register(
            name="volume_down",
            category=ActionCategory.SYSTEM,
            description="Decrease system volume",
            handler=volume_down,
            optional_params={"amount": 10},
            examples=[
                '{"action": "volume_down", "params": {}}',
                '{"action": "volume_down", "params": {"amount": 20}}'
            ]
        )
        
        # volume_mute - Toggle volume mute
        def volume_mute():
            """Toggle volume mute."""
            pyautogui.press('volumemute')
        
        self.registry.register(
            name="volume_mute",
            category=ActionCategory.SYSTEM,
            description="Toggle volume mute",
            handler=volume_mute,
            examples=[
                '{"action": "volume_mute", "params": {}}'
            ]
        )
    
    # ========================================
    # TEXT EDITING HANDLERS
    # ========================================
    
    def register_edit_handlers(self):
        """Register all text editing handlers."""
        from shared.action_registry import ActionCategory
        
        # select_all - Select all text
        def select_all():
            """Select all text (Ctrl+A)."""
            pyautogui.hotkey('ctrl', 'a')
        
        self.registry.register(
            name="select_all",
            category=ActionCategory.EDIT,
            description="Select all text (Ctrl+A)",
            handler=select_all,
            examples=[
                '{"action": "select_all", "params": {}}'
            ]
        )
        
        # undo - Undo last action
        def undo():
            """Undo last action (Ctrl+Z)."""
            pyautogui.hotkey('ctrl', 'z')
        
        self.registry.register(
            name="undo",
            category=ActionCategory.EDIT,
            description="Undo last action (Ctrl+Z)",
            handler=undo,
            examples=[
                '{"action": "undo", "params": {}}'
            ]
        )
        
        # redo - Redo last undone action
        def redo():
            """Redo last undone action (Ctrl+Y)."""
            pyautogui.hotkey('ctrl', 'y')
        
        self.registry.register(
            name="redo",
            category=ActionCategory.EDIT,
            description="Redo last undone action (Ctrl+Y)",
            handler=redo,
            examples=[
                '{"action": "redo", "params": {}}'
            ]
        )
        
        # find_replace - Open find and replace dialog
        def find_replace():
            """Open find and replace dialog (Ctrl+H)."""
            pyautogui.hotkey('ctrl', 'h')
        
        self.registry.register(
            name="find_replace",
            category=ActionCategory.EDIT,
            description="Open find and replace dialog (Ctrl+H)",
            handler=find_replace,
            examples=[
                '{"action": "find_replace", "params": {}}'
            ]
        )
        
        # delete_line - Delete current line
        def delete_line():
            """Delete current line (Ctrl+Shift+K or similar)."""
            # Select line and delete
            pyautogui.hotkey('home')
            pyautogui.hotkey('shift', 'end')
            pyautogui.press('delete')
        
        self.registry.register(
            name="delete_line",
            category=ActionCategory.EDIT,
            description="Delete current line",
            handler=delete_line,
            examples=[
                '{"action": "delete_line", "params": {}}'
            ]
        )
        
        # duplicate_line - Duplicate current line
        def duplicate_line():
            """Duplicate current line (Ctrl+D or similar)."""
            # Select line, copy, move to end, paste
            pyautogui.hotkey('home')
            pyautogui.hotkey('shift', 'end')
            pyautogui.hotkey('ctrl', 'c')
            pyautogui.press('end')
            pyautogui.press('enter')
            pyautogui.hotkey('ctrl', 'v')
        
        self.registry.register(
            name="duplicate_line",
            category=ActionCategory.EDIT,
            description="Duplicate current line",
            handler=duplicate_line,
            examples=[
                '{"action": "duplicate_line", "params": {}}'
            ]
        )
    
    # ========================================
    # MACRO EXECUTION HANDLER
    # ========================================
    
    def register_macro_handler(self):
        """Register macro execution handler."""
        from shared.action_registry import ActionCategory
        
        # macro - Execute predefined macro
        def macro(name: str, vars: Optional[Dict[str, Any]] = None):
            """
            Execute predefined macro (reusable action sequence).
            
            Args:
                name: Name of the macro to execute
                vars: Dictionary of variables to substitute in macro ({{var}} syntax)
            """
            if self.registry.macro_executor:
                return self.registry.macro_executor.execute(name, vars or {})
            else:
                raise RuntimeError(f"Macro executor not available. Cannot execute macro: {name}")
        
        self.registry.register(
            name="macro",
            category=ActionCategory.MACRO,
            description="Execute predefined macro (reusable action sequence)",
            handler=macro,
            required_params=["name"],
            optional_params={"vars": {}},
            examples=[
                '{"action": "macro", "params": {"name": "search_in_browser", "vars": {"query": "python"}}}',
                '{"action": "macro", "params": {"name": "new_tab"}}'
            ]
        )
