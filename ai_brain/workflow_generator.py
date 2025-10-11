"""
Workflow generator that converts CommandIntent into executable Workflows.
"""
import uuid
from datetime import datetime
from typing import Optional
import mss
from PIL import Image

from shared.data_models import Workflow, WorkflowStep
from ai_brain.gemini_client import CommandIntent, ScreenAnalysis, GeminiClient
from shared.browser_shortcuts import BrowserShortcutHelper
from shared.website_navigation import WebsiteNavigator


class WorkflowGenerator:
    """Converts CommandIntent into executable Workflow with steps."""
    
    def __init__(self, gemini_client: Optional[GeminiClient] = None, config: Optional[dict] = None):
        """
        Initialize the workflow generator.
        
        Args:
            gemini_client: Optional GeminiClient for screen analysis
            config: Optional configuration dictionary
        """
        self.gemini_client = gemini_client
        self.config = config or {}
        self.screen_width = 1920  # Default, will be updated from actual screen
        self.screen_height = 1080
        self._update_screen_dimensions()
        
        # Initialize browser shortcut helper
        import platform
        system = platform.system().lower()
        if 'darwin' in system:
            platform_name = 'mac'
        elif 'linux' in system:
            platform_name = 'linux'
        else:
            platform_name = 'windows'
        self.browser_shortcuts = BrowserShortcutHelper(platform_name)
        
        # Initialize website navigator
        self.website_nav = WebsiteNavigator()
        
        # Social media posting configuration
        social_config = self.config.get('social_media', {})
        self.twitter_strategy = social_config.get('posting_strategy', 'keyboard_shortcut')
        # Keep backward compatibility
        if 'twitter' in self.config:
            self.twitter_strategy = self.config['twitter'].get('posting_strategy', self.twitter_strategy)
        self.twitter_tab_count = 22  # Default for X/Twitter
    
    def _update_screen_dimensions(self):
        """Update screen dimensions from actual display."""
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]  # Primary monitor
                self.screen_width = monitor['width']
                self.screen_height = monitor['height']
        except Exception:
            pass  # Keep defaults if unable to detect
    
    def create_workflow(self, intent: CommandIntent, screen_analysis: Optional[ScreenAnalysis] = None) -> Workflow:
        """
        Create a workflow from a CommandIntent.
        
        Args:
            intent: The parsed command intent
            screen_analysis: Optional screen analysis for coordinate detection
            
        Returns:
            Workflow with executable steps
        """
        workflow_id = str(uuid.uuid4())
        steps = []
        
        # Check if this is a complex multi-step command
        complexity = intent.parameters.get('complexity', 'simple')
        
        if complexity == 'complex' or intent.action == 'multi_step':
            steps = self._generate_complex_workflow(intent)
        else:
            # Generate steps based on action type (simple commands)
            if intent.action == 'click':
                steps = self._generate_click_steps(intent, screen_analysis)
            elif intent.action == 'type':
                steps = self._generate_type_steps(intent)
            elif intent.action == 'open_app':
                steps = self._generate_open_app_steps(intent)
            elif intent.action == 'move_mouse':
                steps = self._generate_move_mouse_steps(intent, screen_analysis)
            elif intent.action == 'search' or intent.action == 'search_web':
                steps = self._generate_search_steps(intent)
            elif intent.action == 'double_click':
                steps = self._generate_double_click_steps(intent, screen_analysis)
            elif intent.action == 'right_click':
                steps = self._generate_right_click_steps(intent, screen_analysis)
            elif intent.action == 'navigate_to_url':
                steps = self._generate_navigate_steps(intent)
            elif intent.action == 'login':
                steps = self._generate_login_steps(intent)
            elif intent.action == 'fill_form':
                steps = self._generate_fill_form_steps(intent)
            elif intent.action == 'generate_content':
                steps = self._generate_content_generation_steps(intent)
            elif intent.action == 'post_to_social':
                steps = self._generate_social_post_steps(intent)
            else:
                # Unknown action - create a placeholder
                steps = [WorkflowStep(
                    type='wait',
                    delay_ms=100,
                    data=f"Unknown action: {intent.action}"
                )]
        
        return Workflow(
            id=workflow_id,
            steps=steps,
            metadata={
                'intent': {
                    'action': intent.action,
                    'target': intent.target,
                    'parameters': intent.parameters,
                    'confidence': intent.confidence
                },
                'created_by': 'workflow_generator',
                'complexity': complexity,
                'screen_dimensions': {
                    'width': self.screen_width,
                    'height': self.screen_height
                }
            },
            created_at=datetime.now()
        )
    
    def _generate_click_steps(self, intent: CommandIntent, screen_analysis: Optional[ScreenAnalysis]) -> list[WorkflowStep]:
        """Generate steps for a click action."""
        steps = []
        
        # Get coordinates from screen analysis or parameters
        coords = self._get_coordinates(intent, screen_analysis)
        
        if coords:
            # Move to target
            steps.append(WorkflowStep(
                type='mouse_move',
                coordinates=coords,
                delay_ms=300
            ))
            
            # Click
            steps.append(WorkflowStep(
                type='click',
                coordinates=coords,
                data='left',
                delay_ms=100
            ))
        else:
            # Capture screen for analysis if no coordinates
            steps.append(WorkflowStep(
                type='capture',
                delay_ms=100,
                data=f"Need to locate: {intent.target}"
            ))
        
        return steps
    
    def _generate_double_click_steps(self, intent: CommandIntent, screen_analysis: Optional[ScreenAnalysis]) -> list[WorkflowStep]:
        """Generate steps for a double-click action."""
        steps = []
        coords = self._get_coordinates(intent, screen_analysis)
        
        if coords:
            steps.append(WorkflowStep(
                type='mouse_move',
                coordinates=coords,
                delay_ms=300
            ))
            steps.append(WorkflowStep(
                type='click',
                coordinates=coords,
                data='left',
                delay_ms=50
            ))
            steps.append(WorkflowStep(
                type='click',
                coordinates=coords,
                data='left',
                delay_ms=100
            ))
        
        return steps
    
    def _generate_right_click_steps(self, intent: CommandIntent, screen_analysis: Optional[ScreenAnalysis]) -> list[WorkflowStep]:
        """Generate steps for a right-click action."""
        steps = []
        coords = self._get_coordinates(intent, screen_analysis)
        
        if coords:
            steps.append(WorkflowStep(
                type='mouse_move',
                coordinates=coords,
                delay_ms=300
            ))
            steps.append(WorkflowStep(
                type='click',
                coordinates=coords,
                data='right',
                delay_ms=100
            ))
        
        return steps
    
    def _generate_type_steps(self, intent: CommandIntent) -> list[WorkflowStep]:
        """Generate steps for typing text."""
        text = intent.parameters.get('text', intent.target)
        
        return [
            WorkflowStep(
                type='type',
                data=text,
                delay_ms=50
            )
        ]
    
    def _generate_open_app_steps(self, intent: CommandIntent) -> list[WorkflowStep]:
        """Generate steps for opening an application."""
        app_name = intent.target
        steps = []
        
        # Press Windows key (or Cmd on Mac)
        steps.append(WorkflowStep(
            type='press_key',
            data='win',
            delay_ms=500
        ))
        
        # Type app name
        steps.append(WorkflowStep(
            type='type',
            data=app_name,
            delay_ms=1000
        ))
        
        # Press Enter
        steps.append(WorkflowStep(
            type='press_key',
            data='enter',
            delay_ms=100
        ))
        
        return steps
    
    def _generate_move_mouse_steps(self, intent: CommandIntent, screen_analysis: Optional[ScreenAnalysis]) -> list[WorkflowStep]:
        """Generate steps for moving the mouse."""
        coords = self._get_coordinates(intent, screen_analysis)
        
        if coords:
            return [
                WorkflowStep(
                    type='mouse_move',
                    coordinates=coords,
                    delay_ms=300
                )
            ]
        return []
    
    def _generate_search_steps(self, intent: CommandIntent) -> list[WorkflowStep]:
        """Generate steps for performing a search in browser."""
        query = intent.parameters.get('query', intent.target)
        open_first = intent.parameters.get('open_first_result', False)
        
        steps = []
        
        # Always use browser for search (so user can see results)
        # Open browser (Chrome)
        steps.extend(self._generate_open_app_steps(
            CommandIntent(action='open_app', target='Chrome', parameters={}, confidence=1.0)
        ))
        
        # Wait for browser to open
        steps.append(WorkflowStep(
            type='wait',
            delay_ms=2000
        ))
        
        # Focus address bar
        steps.append(WorkflowStep(
            type='press_key',
            data='ctrl+l',
            delay_ms=300
        ))
        
        # Type search query
        steps.append(WorkflowStep(
            type='type',
            data=query,
            delay_ms=500
        ))
        
        # Press Enter to search
        steps.append(WorkflowStep(
            type='press_key',
            data='enter',
            delay_ms=3000  # Wait for search results to load
        ))
        
        # If user wants to open first result
        if open_first:
            # Tab twice to reach first result link
            steps.append(WorkflowStep(
                type='press_key',
                data='tab',
                delay_ms=200
            ))
            steps.append(WorkflowStep(
                type='press_key',
                data='tab',
                delay_ms=200
            ))
            # Press Enter to open first result
            steps.append(WorkflowStep(
                type='press_key',
                data='enter',
                delay_ms=2000
            ))
        
        return steps
    
    def _generate_complex_workflow(self, intent: CommandIntent) -> list[WorkflowStep]:
        """
        Generate a complex multi-step workflow from sub-tasks.
        
        Args:
            intent: CommandIntent with sub_tasks in parameters
            
        Returns:
            List of workflow steps
        """
        steps = []
        sub_tasks = intent.parameters.get('sub_tasks', [])
        
        # Add initial context step
        steps.append(WorkflowStep(
            type='wait',
            delay_ms=500,
            data=f"Starting complex workflow: {intent.target}"
        ))
        
        # Process each sub-task
        for i, sub_task in enumerate(sub_tasks):
            action = sub_task.get('action', '')
            target = sub_task.get('target', '')
            params = sub_task.get('parameters', {})
            description = sub_task.get('description', '')
            
            # Add a marker for this sub-task
            steps.append(WorkflowStep(
                type='wait',
                delay_ms=100,
                data=f"Sub-task {i+1}: {description}"
            ))
            
            # Generate steps for this sub-task
            sub_intent = CommandIntent(
                action=action,
                target=target,
                parameters=params,
                confidence=intent.confidence
            )
            
            sub_steps = self._generate_steps_for_action(sub_intent)
            steps.extend(sub_steps)
            
            # Add delay between sub-tasks
            steps.append(WorkflowStep(
                type='wait',
                delay_ms=1000
            ))
        
        return steps
    
    def _generate_steps_for_action(self, intent: CommandIntent) -> list[WorkflowStep]:
        """
        Generate steps for a specific action (helper for complex workflows).
        
        Args:
            intent: CommandIntent for a single action
            
        Returns:
            List of workflow steps
        """
        action = intent.action
        
        if action == 'search_web':
            return self._generate_search_steps(intent)
        elif action == 'navigate_to_url':
            return self._generate_navigate_steps(intent)
        elif action == 'login':
            return self._generate_login_steps(intent)
        elif action == 'fill_form':
            return self._generate_fill_form_steps(intent)
        elif action == 'generate_content':
            return self._generate_content_generation_steps(intent)
        elif action == 'post_to_social':
            return self._generate_social_post_steps(intent)
        elif action == 'open_app':
            return self._generate_open_app_steps(intent)
        elif action == 'click':
            return self._generate_click_steps(intent, None)
        elif action == 'type':
            return self._generate_type_steps(intent)
        elif action == 'wait':
            delay = intent.parameters.get('delay_ms', 1000)
            return [WorkflowStep(type='wait', delay_ms=delay)]
        else:
            return [WorkflowStep(
                type='wait',
                delay_ms=100,
                data=f"Unsupported action in complex workflow: {action}"
            )]
    
    def _generate_navigate_steps(self, intent: CommandIntent) -> list[WorkflowStep]:
        """Generate steps for navigating to a URL using keyboard shortcuts."""
        # Get URL from parameters first (more specific), then target
        url = intent.parameters.get('url', '') or intent.target
        
        # If URL doesn't start with http, assume it needs https://
        if url and not url.startswith('http'):
            # Check if it's a domain-like string
            if '.' in url or url.lower() in ['x', 'twitter', 'facebook', 'linkedin']:
                # Map common names to URLs
                url_map = {
                    'x': 'https://x.com',
                    'twitter': 'https://twitter.com',
                    'facebook': 'https://facebook.com',
                    'linkedin': 'https://linkedin.com'
                }
                url = url_map.get(url.lower(), f'https://{url}.com')
        
        steps = []
        
        # First, open Chrome if not already open
        steps.extend(self._generate_open_app_steps(
            CommandIntent(action='open_app', target='Chrome', parameters={}, confidence=1.0)
        ))
        
        # Wait for Chrome to open
        steps.append(WorkflowStep(
            type='wait',
            delay_ms=2000
        ))
        
        # Now navigate to URL using keyboard shortcuts
        shortcut_steps = self.browser_shortcuts.navigate_to_url(url)
        for step_data in shortcut_steps:
            steps.append(WorkflowStep(
                type=step_data['action'],
                data=step_data.get('data'),
                delay_ms=step_data.get('delay_ms', 100)
            ))
        
        return steps
    
    def _generate_login_steps(self, intent: CommandIntent) -> list[WorkflowStep]:
        """Generate steps for logging into a service."""
        service = intent.parameters.get('service', intent.target)
        steps = []
        
        # Add placeholder steps for login
        # In a real implementation, this would need credentials management
        steps.append(WorkflowStep(
            type='wait',
            delay_ms=1000,
            data=f"Login to {service} - requires manual authentication or credential management"
        ))
        
        # Capture screen to find login elements
        steps.append(WorkflowStep(
            type='capture',
            delay_ms=500,
            data="Analyzing login page"
        ))
        
        return steps
    
    def _generate_fill_form_steps(self, intent: CommandIntent) -> list[WorkflowStep]:
        """Generate steps for filling out a form."""
        form_data = intent.parameters.get('form_data', {})
        steps = []
        
        for field_name, field_value in form_data.items():
            # Tab to next field
            steps.append(WorkflowStep(
                type='press_key',
                data='tab',
                delay_ms=200
            ))
            
            # Type value
            steps.append(WorkflowStep(
                type='type',
                data=str(field_value),
                delay_ms=300
            ))
        
        return steps
    
    def _generate_content_generation_steps(self, intent: CommandIntent) -> list[WorkflowStep]:
        """Generate steps for content generation."""
        topic = intent.parameters.get('topic', intent.target)
        content_type = intent.parameters.get('content_type', 'article')
        
        steps = []
        
        # Add a step to indicate content generation
        steps.append(WorkflowStep(
            type='ai_generate',
            data=topic,
            delay_ms=500,
            validation={
                'content_type': content_type,
                'topic': topic,
                'parameters': intent.parameters
            }
        ))
        
        return steps
    
    def _generate_user_input_steps(self, intent: CommandIntent) -> list[WorkflowStep]:
        """Generate steps for requesting user input."""
        prompt_text = intent.parameters.get('prompt', 'Please provide input')
        input_type = intent.parameters.get('input_type', 'text')
        
        steps = []
        
        steps.append(WorkflowStep(
            type='user_input',
            data=prompt_text,
            delay_ms=100,
            validation={
                'input_type': input_type,
                'prompt': prompt_text
            }
        ))
        
        return steps
    
    def _generate_social_post_steps(self, intent: CommandIntent) -> list[WorkflowStep]:
        """Generate steps for posting to social media using website-specific navigation."""
        platform = intent.parameters.get('platform', 'x')
        content_source = intent.parameters.get('content_source', 'generated')
        
        steps = []
        
        # Map platform to URL
        platform_urls = {
            'x': 'https://x.com',
            'twitter': 'https://twitter.com',
            'facebook': 'https://facebook.com',
            'linkedin': 'https://linkedin.com',
            'instagram': 'https://instagram.com',
            'reddit': 'https://reddit.com'
        }
        
        url = platform_urls.get(platform.lower(), 'https://x.com')
        
        # Get website-specific navigation
        website_info = self.website_nav.get_website_info(url)
        
        if website_info:
            # Use website-specific strategy
            if self.twitter_strategy == 'tab_navigation' or not website_info.get('shortcuts', {}).get('new_post'):
                # Use Tab navigation
                compose_steps = self.website_nav.get_compose_steps(url, strategy='tab_navigation')
            else:
                # Use keyboard shortcut
                compose_steps = self.website_nav.get_compose_steps(url, strategy='shortcut')
            
            # Convert to WorkflowSteps
            for step_data in compose_steps:
                steps.append(WorkflowStep(
                    type=step_data['action'],
                    data=step_data.get('data'),
                    delay_ms=step_data.get('delay_ms', 100),
                    validation={'description': step_data.get('description', '')}
                ))
            
            # Type content
            steps.append(WorkflowStep(
                type='type',
                data='[GENERATED_CONTENT]',
                delay_ms=1000
            ))
            
            # Post
            post_steps = self.website_nav.get_post_steps(url)
            for step_data in post_steps:
                steps.append(WorkflowStep(
                    type=step_data['action'],
                    data=step_data.get('data'),
                    delay_ms=step_data.get('delay_ms', 100),
                    validation={'description': step_data.get('description', '')}
                ))
        else:
            # Fallback for unsupported platforms - use generic approach
            steps.append(WorkflowStep(
                type='wait',
                delay_ms=100,
                data=f"No navigation strategy for {platform}, using generic approach"
            ))
            
            # Try to find compose button using accessibility
            fallback_steps = self.browser_shortcuts.accessibility_fallback_interact('compose')
            for step_data in fallback_steps:
                steps.append(WorkflowStep(
                    type=step_data['action'],
                    data=step_data.get('data'),
                    delay_ms=step_data.get('delay_ms', 100)
                ))
            
            # Type content
            steps.append(WorkflowStep(
                type='type',
                data='[GENERATED_CONTENT]',
                delay_ms=1000
            ))
            
            # Try to find and click post button
            post_fallback = self.browser_shortcuts.accessibility_fallback_interact('post')
            for step_data in post_fallback:
                steps.append(WorkflowStep(
                    type=step_data['action'],
                    data=step_data.get('data'),
                    delay_ms=step_data.get('delay_ms', 100)
                ))
        
        return steps
    
    def _generate_twitter_tab_navigation_steps(self, tab_count: int = 22) -> list[WorkflowStep]:
        """
        Generate steps to navigate to Twitter compose field using Tab key.
        
        Args:
            tab_count: Number of times to press Tab (default 22 for X.com)
            
        Returns:
            List of workflow steps
        """
        steps = []
        
        # Press Tab multiple times to reach the compose field
        for i in range(tab_count):
            steps.append(WorkflowStep(
                type='press_key',
                data='tab',
                delay_ms=100,
                validation={'tab_index': i + 1, 'description': f'Tab {i+1}/{tab_count}'}
            ))
        
        # Type content
        steps.append(WorkflowStep(
            type='type',
            data='[GENERATED_CONTENT]',
            delay_ms=1000
        ))
        
        # Post (Ctrl+Enter or Tab to Post button and Enter)
        steps.append(WorkflowStep(
            type='press_key',
            data='ctrl+enter',
            delay_ms=2000
        ))
        
        return steps
    
    def _generate_smart_twitter_post_steps(self) -> list[WorkflowStep]:
        """
        Generate smart Twitter posting steps with multiple fallback strategies.
        Uses screen capture to verify each step.
        
        Returns:
            List of workflow steps
        """
        steps = []
        
        # Strategy 1: Try 'N' shortcut
        steps.append(WorkflowStep(
            type='wait',
            delay_ms=100,
            data='Strategy 1: Trying N shortcut'
        ))
        steps.append(WorkflowStep(
            type='press_key',
            data='n',
            delay_ms=1000
        ))
        
        # Capture screen to verify compose dialog opened
        steps.append(WorkflowStep(
            type='capture',
            delay_ms=500,
            data='Verify compose dialog opened'
        ))
        
        # Type content
        steps.append(WorkflowStep(
            type='type',
            data='[GENERATED_CONTENT]',
            delay_ms=1000
        ))
        
        # Post
        steps.append(WorkflowStep(
            type='press_key',
            data='ctrl+enter',
            delay_ms=2000
        ))
        
        # Verify post succeeded
        steps.append(WorkflowStep(
            type='capture',
            delay_ms=1000,
            data='Verify post succeeded'
        ))
        
        return steps
    
    def _get_coordinates(self, intent: CommandIntent, screen_analysis: Optional[ScreenAnalysis]) -> Optional[tuple[int, int]]:
        """
        Get coordinates for an action from various sources.
        
        Priority:
        1. Explicit coordinates in parameters
        2. Screen analysis results
        3. Default/estimated coordinates
        """
        # Check for explicit coordinates
        if 'x' in intent.parameters and 'y' in intent.parameters:
            return (intent.parameters['x'], intent.parameters['y'])
        
        # Check screen analysis
        if screen_analysis and screen_analysis.elements:
            # Find matching element
            target_lower = intent.target.lower()
            for element in screen_analysis.elements:
                label = element.get('label', '').lower()
                if target_lower in label or label in target_lower:
                    coords_data = element.get('coordinates', {})
                    x_percent = coords_data.get('x_percent', 50)
                    y_percent = coords_data.get('y_percent', 50)
                    
                    # Convert percentage to pixels
                    x = int(self.screen_width * x_percent / 100)
                    y = int(self.screen_height * y_percent / 100)
                    return (x, y)
        
        # Return None if no coordinates found
        return None
    
    def optimize_steps(self, workflow: Workflow) -> Workflow:
        """
        Optimize workflow steps by removing redundant operations.
        
        Args:
            workflow: The workflow to optimize
            
        Returns:
            Optimized workflow
        """
        if len(workflow.steps) <= 1:
            return workflow
        
        optimized_steps = []
        prev_step = None
        
        for step in workflow.steps:
            # Skip redundant mouse moves to same location
            if (prev_step and 
                step.type == 'mouse_move' and 
                prev_step.type == 'mouse_move' and
                step.coordinates == prev_step.coordinates):
                continue
            
            optimized_steps.append(step)
            prev_step = step
        
        workflow.steps = optimized_steps
        return workflow
    
    def validate_workflow(self, workflow: Workflow) -> dict:
        """
        Validate a workflow for potential issues.
        
        Args:
            workflow: The workflow to validate
            
        Returns:
            Dictionary with validation results
        """
        issues = []
        warnings = []
        
        # Check if workflow has steps
        if not workflow.steps:
            issues.append("Workflow has no steps")
        
        # Check for coordinates out of bounds
        for i, step in enumerate(workflow.steps):
            if step.coordinates:
                x, y = step.coordinates
                if x < 0 or x > self.screen_width or y < 0 or y > self.screen_height:
                    warnings.append(f"Step {i}: Coordinates ({x}, {y}) may be out of screen bounds")
        
        # Check for very long delays
        for i, step in enumerate(workflow.steps):
            if step.delay_ms > 10000:
                warnings.append(f"Step {i}: Very long delay ({step.delay_ms}ms)")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }
