"""
Website-specific navigation strategies.
Contains Tab counts and keyboard shortcuts for popular websites.
"""

# Website navigation strategies
# Format: {
#   'url_pattern': {
#     'compose_tab_count': number of tabs to reach compose/post field,
#     'shortcuts': {action: key},
#     'login_tab_count': number of tabs to reach login fields,
#     'submit_tab_count': number of tabs from last field to submit button
#   }
# }

WEBSITE_NAVIGATION = {
    # Social Media
    'x.com': {
        'name': 'X (Twitter)',
        'compose_tab_count': 22,
        'shortcuts': {
            'new_post': 'n',
            'search': '/',
            'home': 'g+h',
            'notifications': 'g+n',
            'messages': 'g+m',
            'post': 'ctrl+enter'
        },
        'login_tab_count': 8,
        'submit_tab_count': 1
    },
    'twitter.com': {
        'name': 'Twitter',
        'compose_tab_count': 22,
        'shortcuts': {
            'new_post': 'n',
            'search': '/',
            'home': 'g+h',
            'post': 'ctrl+enter'
        },
        'login_tab_count': 8,
        'submit_tab_count': 1
    },
    'facebook.com': {
        'name': 'Facebook',
        'compose_tab_count': 15,
        'shortcuts': {
            'new_post': 'alt+m',
            'search': 'alt+/',
            'home': 'alt+1',
            'notifications': 'alt+4',
            'messages': 'alt+5'
        },
        'login_tab_count': 2,
        'submit_tab_count': 1
    },
    'linkedin.com': {
        'name': 'LinkedIn',
        'compose_tab_count': 18,
        'shortcuts': {
            'new_post': 'alt+shift+c',
            'search': 'alt+/',
            'home': 'alt+h',
            'notifications': 'alt+n',
            'messages': 'alt+m'
        },
        'login_tab_count': 3,
        'submit_tab_count': 2
    },
    'instagram.com': {
        'name': 'Instagram',
        'compose_tab_count': 12,
        'shortcuts': {
            'new_post': 'c',
            'search': '/',
            'home': 'h',
            'notifications': 'n',
            'messages': 'm'
        },
        'login_tab_count': 4,
        'submit_tab_count': 1
    },
    'reddit.com': {
        'name': 'Reddit',
        'compose_tab_count': 10,
        'shortcuts': {
            'new_post': 'c',
            'search': '/',
            'home': 'h'
        },
        'login_tab_count': 5,
        'submit_tab_count': 1
    },
    
    # Email
    'gmail.com': {
        'name': 'Gmail',
        'compose_tab_count': 8,
        'shortcuts': {
            'compose': 'c',
            'search': '/',
            'inbox': 'g+i',
            'sent': 'g+t',
            'send': 'ctrl+enter',
            'to_field': 'tab',
            'subject_field': 'tab+tab',
            'body_field': 'tab+tab+tab'
        },
        'login_tab_count': 3,
        'submit_tab_count': 1
    },
    'outlook.com': {
        'name': 'Outlook',
        'compose_tab_count': 12,
        'shortcuts': {
            'compose': 'n',
            'search': 'alt+q',
            'send': 'ctrl+enter'
        },
        'login_tab_count': 4,
        'submit_tab_count': 1
    },
    
    # Productivity
    'docs.google.com': {
        'name': 'Google Docs',
        'compose_tab_count': 5,
        'shortcuts': {
            'new_doc': 'ctrl+alt+shift+d',
            'search': 'ctrl+alt+shift+f',
            'share': 'ctrl+alt+shift+s'
        },
        'login_tab_count': 3,
        'submit_tab_count': 1
    },
    'notion.so': {
        'name': 'Notion',
        'compose_tab_count': 8,
        'shortcuts': {
            'new_page': 'ctrl+n',
            'search': 'ctrl+k',
            'quick_find': 'ctrl+p'
        },
        'login_tab_count': 3,
        'submit_tab_count': 1
    },
    'slack.com': {
        'name': 'Slack',
        'compose_tab_count': 6,
        'shortcuts': {
            'new_message': 'ctrl+n',
            'search': 'ctrl+k',
            'quick_switcher': 'ctrl+k'
        },
        'login_tab_count': 4,
        'submit_tab_count': 1
    },
    
    # Developer
    'github.com': {
        'name': 'GitHub',
        'compose_tab_count': 14,
        'shortcuts': {
            'search': '/',
            'new_issue': 'c',
            'new_repo': 'ctrl+k'
        },
        'login_tab_count': 3,
        'submit_tab_count': 1
    },
    'stackoverflow.com': {
        'name': 'Stack Overflow',
        'compose_tab_count': 16,
        'shortcuts': {
            'search': '/',
            'ask_question': 'a'
        },
        'login_tab_count': 4,
        'submit_tab_count': 1
    },
    
    # E-commerce
    'amazon.com': {
        'name': 'Amazon',
        'compose_tab_count': 10,
        'shortcuts': {
            'search': 'alt+s',
            'cart': 'alt+c'
        },
        'login_tab_count': 3,
        'submit_tab_count': 1
    },
    
    # Video
    'youtube.com': {
        'name': 'YouTube',
        'compose_tab_count': 8,
        'shortcuts': {
            'search': '/',
            'upload': 'u',
            'play_pause': 'k',
            'fullscreen': 'f'
        },
        'login_tab_count': 3,
        'submit_tab_count': 1
    }
}


class WebsiteNavigator:
    """Helper class for website-specific navigation."""
    
    def __init__(self):
        """Initialize the website navigator."""
        self.navigation_db = WEBSITE_NAVIGATION
    
    def get_website_info(self, url: str) -> dict:
        """
        Get navigation info for a website.
        
        Args:
            url: The website URL
            
        Returns:
            Dictionary with navigation info, or empty dict if not found
        """
        # Extract domain from URL
        domain = self._extract_domain(url)
        
        # Check if we have navigation info for this domain
        for pattern, info in self.navigation_db.items():
            if pattern in domain:
                return info
        
        return {}
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        # Remove protocol
        domain = url.replace('https://', '').replace('http://', '')
        # Remove path
        domain = domain.split('/')[0]
        # Remove www
        domain = domain.replace('www.', '')
        return domain.lower()
    
    def get_compose_steps(self, url: str, strategy: str = 'shortcut') -> list[dict]:
        """
        Get steps to reach compose/post field on a website.
        
        Args:
            url: The website URL
            strategy: 'shortcut' or 'tab_navigation'
            
        Returns:
            List of step dictionaries
        """
        info = self.get_website_info(url)
        if not info:
            return []
        
        steps = []
        
        if strategy == 'shortcut' and 'shortcuts' in info and 'new_post' in info['shortcuts']:
            # Use keyboard shortcut
            shortcut = info['shortcuts']['new_post']
            steps.append({
                'action': 'press_key',
                'data': shortcut,
                'delay_ms': 1000,
                'description': f"Open compose with {shortcut}"
            })
        elif strategy == 'tab_navigation' and 'compose_tab_count' in info:
            # Use Tab navigation
            tab_count = info['compose_tab_count']
            for i in range(tab_count):
                steps.append({
                    'action': 'press_key',
                    'data': 'tab',
                    'delay_ms': 100,
                    'description': f"Tab {i+1}/{tab_count}"
                })
        
        return steps
    
    def get_post_steps(self, url: str) -> list[dict]:
        """
        Get steps to post/submit content.
        
        Args:
            url: The website URL
            
        Returns:
            List of step dictionaries
        """
        info = self.get_website_info(url)
        if not info:
            return []
        
        steps = []
        
        # Check for post shortcut
        if 'shortcuts' in info and 'post' in info['shortcuts']:
            shortcut = info['shortcuts']['post']
            steps.append({
                'action': 'press_key',
                'data': shortcut,
                'delay_ms': 2000,
                'description': f"Post with {shortcut}"
            })
        elif 'shortcuts' in info and 'send' in info['shortcuts']:
            shortcut = info['shortcuts']['send']
            steps.append({
                'action': 'press_key',
                'data': shortcut,
                'delay_ms': 2000,
                'description': f"Send with {shortcut}"
            })
        else:
            # Default: Ctrl+Enter
            steps.append({
                'action': 'press_key',
                'data': 'ctrl+enter',
                'delay_ms': 2000,
                'description': "Post with Ctrl+Enter"
            })
        
        return steps
    
    def get_login_steps(self, url: str, username: str = '', password: str = '') -> list[dict]:
        """
        Get steps to login to a website.
        
        Args:
            url: The website URL
            username: Username/email (optional)
            password: Password (optional)
            
        Returns:
            List of step dictionaries
        """
        info = self.get_website_info(url)
        if not info:
            return []
        
        steps = []
        tab_count = info.get('login_tab_count', 3)
        
        # Tab to username field
        for i in range(tab_count):
            steps.append({
                'action': 'press_key',
                'data': 'tab',
                'delay_ms': 100,
                'description': f"Tab to login field {i+1}"
            })
        
        # Type username if provided
        if username:
            steps.append({
                'action': 'type',
                'data': username,
                'delay_ms': 300,
                'description': "Enter username"
            })
            steps.append({
                'action': 'press_key',
                'data': 'tab',
                'delay_ms': 200,
                'description': "Tab to password field"
            })
        
        # Type password if provided
        if password:
            steps.append({
                'action': 'type',
                'data': password,
                'delay_ms': 300,
                'description': "Enter password"
            })
        
        # Submit
        submit_tabs = info.get('submit_tab_count', 1)
        for i in range(submit_tabs):
            steps.append({
                'action': 'press_key',
                'data': 'tab',
                'delay_ms': 100,
                'description': f"Tab to submit button"
            })
        
        steps.append({
            'action': 'press_key',
            'data': 'enter',
            'delay_ms': 2000,
            'description': "Submit login"
        })
        
        return steps
    
    def list_supported_websites(self) -> list[str]:
        """Get list of supported websites."""
        return [info['name'] for info in self.navigation_db.values()]
    
    def get_all_shortcuts(self, url: str) -> dict:
        """Get all keyboard shortcuts for a website."""
        info = self.get_website_info(url)
        return info.get('shortcuts', {})
