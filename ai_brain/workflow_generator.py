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


class WorkflowGenerator:
    """Converts CommandIntent into executable Workflow with steps."""
    
    def __init__(self, gemini_client: Optional[GeminiClient] = None):
        """
        Initialize the workflow generator.
        
        Args:
            gemini_client: Optional GeminiClient for screen analysis
        """
        self.gemini_client = gemini_client
        self.screen_width = 1920  # Default, will be updated from actual screen
        self.screen_height = 1080
        self._update_screen_dimensions()
    
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
        """Generate steps for performing a search."""
        query = intent.parameters.get('query', intent.target)
        steps = []
        
        # Open browser (assuming Chrome)
        steps.extend(self._generate_open_app_steps(
            CommandIntent(action='open_app', target='Chrome', parameters={}, confidence=1.0)
        ))
        
        # Wait for browser to open
        steps.append(WorkflowStep(
            type='wait',
            delay_ms=2000
        ))
        
        # Type search query in address bar
        steps.append(WorkflowStep(
            type='type',
            data=query,
            delay_ms=500
        ))
        
        # Press Enter
        steps.append(WorkflowStep(
            type='press_key',
            data='enter',
            delay_ms=100
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
        """Generate steps for navigating to a URL."""
        url = intent.target or intent.parameters.get('url', '')
        steps = []
        
        # Focus address bar (Ctrl+L)
        steps.append(WorkflowStep(
            type='press_key',
            data='ctrl+l',
            delay_ms=300
        ))
        
        # Type URL
        steps.append(WorkflowStep(
            type='type',
            data=url,
            delay_ms=500
        ))
        
        # Press Enter
        steps.append(WorkflowStep(
            type='press_key',
            data='enter',
            delay_ms=2000  # Wait for page load
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
            type='wait',
            delay_ms=500,
            data=f"Generating {content_type} about: {topic}"
        ))
        
        # In a real implementation, this would call the Gemini API
        # and store the generated content for later use
        steps.append(WorkflowStep(
            type='wait',
            delay_ms=2000,
            data="Content generation complete (stored in context)"
        ))
        
        return steps
    
    def _generate_social_post_steps(self, intent: CommandIntent) -> list[WorkflowStep]:
        """Generate steps for posting to social media."""
        platform = intent.parameters.get('platform', 'x')
        content_source = intent.parameters.get('content_source', 'generated')
        
        steps = []
        
        # Find and click the compose/post button
        steps.append(WorkflowStep(
            type='capture',
            delay_ms=500,
            data=f"Looking for compose button on {platform}"
        ))
        
        # Wait for compose dialog
        steps.append(WorkflowStep(
            type='wait',
            delay_ms=1000
        ))
        
        # Type content (placeholder - would use generated content)
        steps.append(WorkflowStep(
            type='type',
            data=f"[Content from {content_source}]",
            delay_ms=1000
        ))
        
        # Find and click post button
        steps.append(WorkflowStep(
            type='capture',
            delay_ms=500,
            data="Looking for post/submit button"
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
