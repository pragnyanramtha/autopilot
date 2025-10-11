"""
Browser keyboard shortcuts database.
Provides efficient keyboard-based browser control without relying on screen capture.
"""

# Platform-specific modifiers
PLATFORM_MODIFIERS = {
    'windows': {
        'cmd': 'ctrl',
        'option': 'alt'
    },
    'mac': {
        'cmd': 'cmd',
        'option': 'option'
    },
    'linux': {
        'cmd': 'ctrl',
        'option': 'alt'
    }
}

# Universal browser shortcuts (work in Chrome, Firefox, Edge, Safari)
BROWSER_SHORTCUTS = {
    # Tab management
    'new_tab': 'ctrl+t',
    'close_tab': 'ctrl+w',
    'reopen_tab': 'ctrl+shift+t',
    'next_tab': 'ctrl+tab',
    'prev_tab': 'ctrl+shift+tab',
    'tab_1': 'ctrl+1',
    'tab_2': 'ctrl+2',
    'tab_3': 'ctrl+3',
    'tab_4': 'ctrl+4',
    'tab_5': 'ctrl+5',
    'tab_6': 'ctrl+6',
    'tab_7': 'ctrl+7',
    'tab_8': 'ctrl+8',
    'last_tab': 'ctrl+9',
    
    # Navigation
    'address_bar': 'ctrl+l',
    'search_bar': 'ctrl+k',
    'back': 'alt+left',
    'forward': 'alt+right',
    'refresh': 'ctrl+r',
    'hard_refresh': 'ctrl+shift+r',
    'home': 'alt+home',
    'stop_loading': 'esc',
    
    # Page interaction
    'scroll_down': 'space',
    'scroll_up': 'shift+space',
    'page_down': 'pagedown',
    'page_up': 'pageup',
    'top_of_page': 'home',
    'bottom_of_page': 'end',
    'select_all': 'ctrl+a',
    'copy': 'ctrl+c',
    'paste': 'ctrl+v',
    'cut': 'ctrl+x',
    'undo': 'ctrl+z',
    'redo': 'ctrl+y',
    
    # Search and find
    'find_in_page': 'ctrl+f',
    'find_next': 'ctrl+g',
    'find_prev': 'ctrl+shift+g',
    
    # Window management
    'new_window': 'ctrl+n',
    'new_incognito': 'ctrl+shift+n',
    'close_window': 'ctrl+shift+w',
    'minimize': 'ctrl+m',
    'fullscreen': 'f11',
    
    # Bookmarks
    'bookmark_page': 'ctrl+d',
    'bookmarks_bar': 'ctrl+shift+b',
    'bookmark_manager': 'ctrl+shift+o',
    
    # Developer tools
    'dev_tools': 'ctrl+shift+i',
    'console': 'ctrl+shift+j',
    'view_source': 'ctrl+u',
    
    # Zoom
    'zoom_in': 'ctrl+plus',
    'zoom_out': 'ctrl+minus',
    'zoom_reset': 'ctrl+0',
    
    # Downloads
    'downloads': 'ctrl+j',
    
    # History
    'history': 'ctrl+h',
    
    # Print
    'print': 'ctrl+p',
    
    # Save
    'save_page': 'ctrl+s',
}

# Twitter/X specific shortcuts
TWITTER_SHORTCUTS = {
    'new_tweet': 'n',
    'search': '/',
    'go_home': 'g+h',
    'go_explore': 'g+e',
    'go_notifications': 'g+n',
    'go_messages': 'g+m',
    'go_profile': 'g+p',
    'like': 'l',
    'retweet': 't',
    'reply': 'r',
    'share': 's',
    'next_tweet': 'j',
    'prev_tweet': 'k',
}

# Common web form shortcuts
FORM_SHORTCUTS = {
    'next_field': 'tab',
    'prev_field': 'shift+tab',
    'submit': 'enter',
    'cancel': 'esc',
    'select_dropdown': 'alt+down',
    'checkbox_toggle': 'space',
}

# Accessibility shortcuts
ACCESSIBILITY_SHORTCUTS = {
    'select_all_text': 'ctrl+a',
    'read_selected': 'ctrl+shift+u',  # Screen reader
    'focus_address_bar': 'ctrl+l',
    'focus_search': 'ctrl+k',
    'skip_to_content': 'tab',  # Usually skips navigation
    'headings_list': 'h',  # In screen readers
    'links_list': 'insert+f7',  # NVDA
}


class BrowserShortcutHelper:
    """Helper class for browser keyboard shortcuts."""
    
    def __init__(self, platform: str = 'windows'):
        """
        Initialize the shortcut helper.
        
        Args:
            platform: Operating system ('windows', 'mac', 'linux')
        """
        self.platform = platform.lower()
        self.modifiers = PLATFORM_MODIFIERS.get(self.platform, PLATFORM_MODIFIERS['windows'])
    
    def get_shortcut(self, action: str, context: str = 'browser') -> str:
        """
        Get the keyboard shortcut for an action.
        
        Args:
            action: The action name (e.g., 'new_tab', 'address_bar')
            context: Context ('browser', 'twitter', 'form', 'accessibility')
            
        Returns:
            Keyboard shortcut string (e.g., 'ctrl+t')
        """
        shortcuts_map = {
            'browser': BROWSER_SHORTCUTS,
            'twitter': TWITTER_SHORTCUTS,
            'form': FORM_SHORTCUTS,
            'accessibility': ACCESSIBILITY_SHORTCUTS
        }
        
        shortcuts = shortcuts_map.get(context, BROWSER_SHORTCUTS)
        shortcut = shortcuts.get(action, '')
        
        # Adapt for platform
        if self.platform == 'mac':
            shortcut = shortcut.replace('ctrl', 'cmd')
            shortcut = shortcut.replace('alt', 'option')
        
        return shortcut
    
    def navigate_to_url(self, url: str) -> list[dict]:
        """
        Generate steps to navigate to a URL using keyboard.
        
        Args:
            url: The URL to navigate to
            
        Returns:
            List of step dictionaries
        """
        return [
            {'action': 'press_key', 'data': self.get_shortcut('address_bar'), 'description': 'Focus address bar'},
            {'action': 'wait', 'delay_ms': 300},
            {'action': 'type', 'data': url, 'description': f'Type URL: {url}'},
            {'action': 'press_key', 'data': 'enter', 'description': 'Navigate to URL'},
            {'action': 'wait', 'delay_ms': 2000, 'description': 'Wait for page load'}
        ]
    
    def open_new_tab(self) -> list[dict]:
        """Generate steps to open a new tab."""
        return [
            {'action': 'press_key', 'data': self.get_shortcut('new_tab'), 'description': 'Open new tab'},
            {'action': 'wait', 'delay_ms': 500}
        ]
    
    def close_current_tab(self) -> list[dict]:
        """Generate steps to close current tab."""
        return [
            {'action': 'press_key', 'data': self.get_shortcut('close_tab'), 'description': 'Close tab'},
            {'action': 'wait', 'delay_ms': 300}
        ]
    
    def search_in_page(self, query: str) -> list[dict]:
        """Generate steps to search within a page."""
        return [
            {'action': 'press_key', 'data': self.get_shortcut('find_in_page'), 'description': 'Open find'},
            {'action': 'wait', 'delay_ms': 300},
            {'action': 'type', 'data': query, 'description': f'Search for: {query}'},
            {'action': 'press_key', 'data': 'enter', 'description': 'Find next'}
        ]
    
    def select_all_and_interact(self) -> list[dict]:
        """
        Accessibility fallback: Select all content and interact.
        Useful when screen capture fails.
        """
        return [
            {'action': 'press_key', 'data': self.get_shortcut('select_all'), 'description': 'Select all content'},
            {'action': 'wait', 'delay_ms': 500, 'description': 'Wait for selection'},
            # Content is now selected and can be copied, read, or interacted with
        ]
    
    def twitter_compose_tweet(self) -> list[dict]:
        """Generate steps to compose a tweet on Twitter."""
        return [
            {'action': 'press_key', 'data': self.get_shortcut('new_tweet', 'twitter'), 'description': 'Open compose tweet'},
            {'action': 'wait', 'delay_ms': 1000, 'description': 'Wait for compose dialog'}
        ]
    
    def twitter_post_tweet(self) -> list[dict]:
        """Generate steps to post a tweet (after composing)."""
        return [
            {'action': 'press_key', 'data': 'ctrl+enter', 'description': 'Post tweet (Ctrl+Enter)'},
            {'action': 'wait', 'delay_ms': 2000, 'description': 'Wait for post confirmation'}
        ]
    
    def form_navigate_and_fill(self, fields: list[str]) -> list[dict]:
        """
        Generate steps to navigate and fill a form.
        
        Args:
            fields: List of field values to fill
            
        Returns:
            List of step dictionaries
        """
        steps = []
        for i, value in enumerate(fields):
            if i > 0:
                steps.append({
                    'action': 'press_key',
                    'data': self.get_shortcut('next_field', 'form'),
                    'description': 'Move to next field'
                })
                steps.append({'action': 'wait', 'delay_ms': 200})
            
            steps.append({
                'action': 'type',
                'data': value,
                'description': f'Fill field {i+1}'
            })
            steps.append({'action': 'wait', 'delay_ms': 300})
        
        return steps
    
    def accessibility_fallback_interact(self, target: str) -> list[dict]:
        """
        Accessibility fallback when screen capture fails.
        Uses keyboard navigation to find and interact with elements.
        
        Args:
            target: Description of what to find
            
        Returns:
            List of step dictionaries
        """
        return [
            {'action': 'press_key', 'data': self.get_shortcut('select_all'), 'description': 'Select all (accessibility)'},
            {'action': 'wait', 'delay_ms': 300},
            {'action': 'press_key', 'data': self.get_shortcut('find_in_page'), 'description': 'Open find'},
            {'action': 'wait', 'delay_ms': 300},
            {'action': 'type', 'data': target, 'description': f'Search for: {target}'},
            {'action': 'press_key', 'data': 'enter', 'description': 'Find element'},
            {'action': 'wait', 'delay_ms': 500},
            {'action': 'press_key', 'data': 'esc', 'description': 'Close find dialog'},
            {'action': 'press_key', 'data': 'enter', 'description': 'Interact with found element'}
        ]


def get_browser_shortcut(action: str, platform: str = 'windows') -> str:
    """
    Quick function to get a browser shortcut.
    
    Args:
        action: Action name
        platform: Operating system
        
    Returns:
        Keyboard shortcut string
    """
    helper = BrowserShortcutHelper(platform)
    return helper.get_shortcut(action)
