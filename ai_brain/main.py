"""
AI Brain main application.
Provides command loop for accepting user commands, generating protocols,
and coordinating with the automation engine.
"""
import os
import sys
import json
import time
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from ai_brain.gemini_client import GeminiClient, CommandIntent
from ai_brain.protocol_generator import ProtocolGenerator
from ai_brain.vision_navigator import VisionNavigator
from shared.communication import MessageBroker, CommunicationError
from shared.data_models import ExecutionResult

# Load environment variables from .env file
load_dotenv()


class AIBrainApp:
    """Main AI Brain application."""
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize the AI Brain application.
        
        Args:
            config_path: Path to configuration file
        """
        self.console = Console()
        self.config = self._load_config(config_path)
        self.running = False
        
        # Initialize components
        self.gemini_client: Optional[GeminiClient] = None
        self.protocol_generator: Optional[ProtocolGenerator] = None
        self.message_broker: Optional[MessageBroker] = None
        self.vision_navigator: Optional[VisionNavigator] = None
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.console.print(f"[yellow]Warning: Config file not found at {config_path}[/yellow]")
            return self._get_default_config()
        except json.JSONDecodeError as e:
            self.console.print(f"[red]Error parsing config file: {e}[/red]")
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """Get default configuration."""
        return {
            "gemini": {
                "api_key": os.getenv("GEMINI_API_KEY", ""),
                "model": "gemini-2.5-flash",
                "temperature": 0.7
            },
            "automation": {
                "safety_delay_ms": 100,
                "screenshot_quality": 85,
                "enable_safety_monitor": True
            },
            "communication": {
                "method": "file"
            }
        }
    
    def initialize(self) -> bool:
        """
        Initialize all components.
        
        Returns:
            True if initialization successful, False otherwise
        """
        self.console.print(Panel.fit(
            "[bold cyan]AI Automation Assistant - AI Brain[/bold cyan]\n"
            "Initializing components...",
            border_style="cyan"
        ))
        
        try:
            # Initialize Gemini client (reads from .env file)
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                self.console.print("[red]Error: Gemini API key not found![/red]")
                self.console.print("[yellow]Please create a .env file with:[/yellow]")
                self.console.print("GEMINI_API_KEY=your_api_key_here")
                self.console.print("\n[dim]Get your API key from: https://makersuite.google.com/app/apikey[/dim]")
                return False
            
            self.console.print("✓ Initializing Gemini client (from .env)...")
            self.gemini_client = GeminiClient(api_key=api_key)
            
            # Initialize protocol generator
            self.console.print("✓ Initializing protocol generator...")
            self.protocol_generator = ProtocolGenerator(
                gemini_client=self.gemini_client,
                config=self.config
            )
            
            # Initialize message broker
            self.console.print("✓ Initializing communication layer...")
            self.message_broker = MessageBroker()
            
            # Initialize vision navigator if enabled
            visual_nav_config = self.config.get('visual_navigation', {})
            if visual_nav_config.get('enabled', True):
                self.console.print("✓ Initializing vision navigator...")
                self.vision_navigator = VisionNavigator(
                    gemini_client=self.gemini_client,
                    config=self.config
                )
            
            self.console.print("[green]✓ All components initialized successfully![/green]\n")
            return True
            
        except Exception as e:
            self.console.print(f"[red]Error during initialization: {e}[/red]")
            return False
    
    def run(self):
        """Run the main command loop."""
        if not self.initialize():
            return
        
        self.running = True
        self._print_welcome()
        
        while self.running:
            try:
                # Get user command
                command = Prompt.ask("\n[bold cyan]Enter command[/bold cyan]", default="")
                
                if not command.strip():
                    continue
                
                # Handle special commands
                if command.lower() in ['exit', 'quit', 'q']:
                    self._handle_exit()
                    break
                elif command.lower() in ['help', 'h', '?']:
                    self._print_help()
                    continue
                elif command.lower() == 'clear':
                    self.console.clear()
                    continue
                elif command.lower() == 'status':
                    self._show_status()
                    continue
                
                # Process automation command
                self._process_command(command)
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Interrupted by user[/yellow]")
                self._handle_exit()
                break
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
    
    def _process_command(self, user_input: str):
        """
        Process a user command and generate protocol.
        
        Args:
            user_input: The user's natural language command
        """
        self.console.print(f"\n[dim]Processing: {user_input}[/dim]")
        
        try:
            # Step 1: Parse command intent
            self.console.print("→ Analyzing command with Gemini...")
            intent = self.gemini_client.process_command(user_input)
            
            # Check confidence
            if intent.confidence < 0.5:
                self.console.print(f"[yellow]Warning: Low confidence ({intent.confidence:.2f})[/yellow]")
                if intent.action == 'error':
                    self.console.print(f"[red]Error: {intent.parameters.get('error', 'Unknown error')}[/red]")
                    return
            
            # Display parsed intent
            self._display_intent(intent)
            
            # Check if visual navigation is needed
            if self._requires_visual_navigation(intent, user_input):
                self._handle_visual_navigation(intent, user_input)
                return
            
            # Check if complex protocol requires additional processing
            complexity = intent.parameters.get('complexity', 'simple')
            if complexity == 'complex':
                self._handle_complex_protocol(intent, user_input)
            else:
                self._handle_simple_protocol(intent)
            
        except CommunicationError as e:
            self.console.print(f"[red]Communication error: {e}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error processing command: {e}[/red]")
    
    def _requires_visual_navigation(self, intent: CommandIntent, user_input: str) -> bool:
        """
        Determine if a command requires visual navigation.
        
        Args:
            intent: Parsed command intent
            user_input: Original user input
            
        Returns:
            True if visual navigation should be used, False otherwise
        """
        # Check if visual navigation is enabled
        if not self.vision_navigator:
            return False
        
        # Check for explicit visual navigation keywords
        visual_keywords = ['find', 'locate', 'look for', 'search for', 'click on', 'click the']
        user_lower = user_input.lower()
        
        # If user explicitly mentions visual elements without coordinates
        has_visual_keyword = any(keyword in user_lower for keyword in visual_keywords)
        has_coordinates = intent.parameters.get('x') is not None or intent.parameters.get('coordinates') is not None
        
        # Use visual navigation if:
        # 1. User mentions visual elements AND no coordinates provided
        # 2. Intent explicitly requests visual navigation
        # 3. Action is 'click' or 'double_click' without specific coordinates
        if has_visual_keyword and not has_coordinates:
            return True
        
        if intent.parameters.get('use_visual_navigation', False):
            return True
        
        if intent.action in ['click', 'double_click', 'right_click'] and not has_coordinates:
            # Check if target description suggests visual search
            target = intent.target or ''
            if any(word in target.lower() for word in ['button', 'link', 'icon', 'menu', 'tab']):
                return True
        
        return False
    
    def _handle_visual_navigation(self, intent: CommandIntent, user_input: str):
        """
        Handle visual navigation workflow.
        
        Args:
            intent: Parsed command intent
            user_input: Original user input
        """
        import uuid
        import base64
        from io import BytesIO
        
        self.console.print("\n[bold cyan]Visual Navigation Mode Activated[/bold cyan]")
        
        # Extract task description and goal
        task_description = intent.target or user_input
        workflow_goal = intent.parameters.get('goal', task_description)
        
        # Get max iterations from config
        visual_nav_config = self.config.get('visual_navigation', {})
        max_iterations = visual_nav_config.get('max_iterations', 10)
        iteration_timeout = visual_nav_config.get('iteration_timeout_seconds', 30)
        
        self.console.print(f"  Task: {task_description}")
        self.console.print(f"  Max iterations: {max_iterations}")
        
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        
        # Send initial visual navigation request
        self.console.print("\n→ Requesting screenshot from automation engine...")
        self.message_broker.send_visual_navigation_request({
            "request_id": request_id,
            "task_description": task_description,
            "workflow_goal": workflow_goal,
            "iteration": 0,
            "max_iterations": max_iterations
        })
        
        # Wait for screenshot response
        response = self.message_broker.receive_visual_navigation_response(
            request_id=request_id,
            timeout=iteration_timeout
        )
        
        if not response:
            self.console.print("[red]Error: No response from automation engine (timeout)[/red]")
            self.console.print("[yellow]Make sure the automation engine is running[/yellow]")
            return
        
        self.console.print("[green]✓ Screenshot received[/green]")
        
        # Decode screenshot
        screenshot_base64 = response.get('screenshot_base64', '')
        screenshot_data = base64.b64decode(screenshot_base64)
        screenshot = Image.open(BytesIO(screenshot_data))
        
        mouse_position = response.get('mouse_position', {})
        current_mouse_pos = (mouse_position.get('x', 0), mouse_position.get('y', 0))
        
        screen_size_dict = response.get('screen_size', {})
        screen_size = (screen_size_dict.get('width', 1920), screen_size_dict.get('height', 1080))
        
        # Iteration loop: analyze → execute → verify
        iteration = 0
        actions_taken = []
        
        # Reset action history for loop detection
        self.vision_navigator.reset_action_history()
        
        with self.console.status("[bold green]Executing visual navigation workflow...") as status:
            while iteration < max_iterations:
                iteration += 1
                status.update(f"[bold green]Iteration {iteration}/{max_iterations}...")
                
                self.console.print(f"\n[cyan]→ Iteration {iteration}: Analyzing screen...[/cyan]")
                
                # Analyze screenshot with AI
                try:
                    result = self.vision_navigator.analyze_screen_for_action(
                        screenshot=screenshot,
                        current_mouse_pos=current_mouse_pos,
                        task_description=task_description,
                        screen_size=screen_size
                    )
                except Exception as e:
                    self.console.print(f"[red]Error analyzing screen: {e}[/red]")
                    break
                
                # Display result
                self.console.print(f"  Action: {result.action}")
                if result.coordinates:
                    self.console.print(f"  Coordinates: {result.coordinates}")
                self.console.print(f"  Confidence: {result.confidence:.2%}")
                self.console.print(f"  Reasoning: {result.reasoning}")
                
                # Check if workflow is complete
                if result.action == 'complete':
                    self.console.print("\n[green]✓ Workflow complete![/green]")
                    break
                
                # Check if no action needed
                if result.action == 'no_action':
                    self.console.print("\n[yellow]No action needed[/yellow]")
                    break
                
                # Check for loop detection (repeated clicks on same coordinates)
                if result.coordinates:
                    loop_detected, loop_warning = self.vision_navigator.detect_loop(result.coordinates)
                    if loop_detected:
                        self.console.print(f"\n[bold red]⚠ LOOP DETECTED ⚠[/bold red]")
                        self.console.print(f"[red]{loop_warning}[/red]")
                        self.console.print("[yellow]Halting execution to prevent infinite loop[/yellow]")
                        break
                
                # Check for critical actions and require confirmation
                is_critical, matched_keywords = self.vision_navigator.is_critical_action(
                    result.reasoning, 
                    result.action
                )
                if is_critical:
                    self.console.print("\n[bold red]⚠ CRITICAL ACTION DETECTED ⚠[/bold red]")
                    self.console.print(f"[red]Matched keywords: {', '.join(matched_keywords)}[/red]")
                    self.console.print(f"[yellow]The AI wants to: {result.reasoning}[/yellow]")
                    self.console.print(f"[yellow]Action: {result.action} at {result.coordinates}[/yellow]")
                    
                    confirm = Prompt.ask(
                        "[bold]This action may be destructive. Continue?[/bold]",
                        choices=["y", "n"],
                        default="n"
                    )
                    
                    if confirm.lower() != 'y':
                        self.console.print("[yellow]Critical action cancelled by user[/yellow]")
                        break
                
                # Check confidence threshold
                confidence_threshold = visual_nav_config.get('confidence_threshold', 0.6)
                if result.confidence < confidence_threshold:
                    self.console.print(f"[yellow]Warning: Low confidence ({result.confidence:.2%})[/yellow]")
                    confirm = Prompt.ask(
                        "Continue with this action?",
                        choices=["y", "n"],
                        default="n"
                    )
                    if confirm.lower() != 'y':
                        self.console.print("[yellow]Action skipped by user[/yellow]")
                        break
                
                # Store action for history
                actions_taken.append({
                    'iteration': iteration,
                    'action': result.action,
                    'coordinates': result.coordinates,
                    'confidence': result.confidence,
                    'reasoning': result.reasoning
                })
                
                # Send action command to automation engine
                self.console.print(f"\n→ Executing {result.action}...")
                self.message_broker.send_visual_action_command({
                    "request_id": request_id,
                    "action": result.action,
                    "coordinates": {"x": result.coordinates[0], "y": result.coordinates[1]} if result.coordinates else None,
                    "text": result.text_to_type,
                    "request_followup": result.requires_followup
                })
                
                # Wait for action result
                action_result = self.message_broker.receive_visual_action_result(
                    request_id=request_id,
                    timeout=iteration_timeout
                )
                
                if not action_result:
                    self.console.print("[red]Error: No action result received (timeout)[/red]")
                    break
                
                if action_result.get('status') != 'success':
                    error = action_result.get('error', 'Unknown error')
                    self.console.print(f"[red]Error executing action: {error}[/red]")
                    break
                
                self.console.print("[green]✓ Action executed[/green]")
                
                # Add action to history for loop detection
                if result.coordinates:
                    self.vision_navigator.add_action_to_history(result.action, result.coordinates)
                
                # If followup requested, get new screenshot
                if result.requires_followup:
                    self.console.print("→ Capturing new screenshot...")
                    
                    # Decode new screenshot from action result
                    new_screenshot_base64 = action_result.get('screenshot_base64', '')
                    if new_screenshot_base64:
                        screenshot_data = base64.b64decode(new_screenshot_base64)
                        screenshot = Image.open(BytesIO(screenshot_data))
                        
                        new_mouse_pos = action_result.get('mouse_position', {})
                        current_mouse_pos = (new_mouse_pos.get('x', 0), new_mouse_pos.get('y', 0))
                        
                        self.console.print("[green]✓ New screenshot captured[/green]")
                    else:
                        self.console.print("[yellow]Warning: No new screenshot in response[/yellow]")
                        break
                else:
                    # Workflow complete without followup
                    break
        
        # Determine final status
        if iteration >= max_iterations:
            final_status = 'timeout'
            error_msg = f'Maximum iterations ({max_iterations}) reached'
            # Log timeout warning with partial results
            self.console.print(f"\n[bold yellow]⚠ Workflow Timeout[/bold yellow]")
            self.console.print(f"[yellow]Maximum iterations ({max_iterations}) reached[/yellow]")
            self.console.print(f"[yellow]Partial results: {len(actions_taken)} actions completed[/yellow]")
            if actions_taken:
                self.console.print("[yellow]Last action:[/yellow]")
                last_action = actions_taken[-1]
                self.console.print(f"  {last_action['action']} at {last_action['coordinates']}")
                self.console.print(f"  Reasoning: {last_action['reasoning']}")
        elif actions_taken and actions_taken[-1]['action'] == 'complete':
            final_status = 'success'
            error_msg = None
        elif not actions_taken:
            final_status = 'failed'
            error_msg = 'No actions taken'
        else:
            final_status = 'success'
            error_msg = None
        
        # Send final result back to protocol executor (if it's waiting)
        final_result = {
            'request_id': request_id,
            'status': final_status,
            'actions_taken': actions_taken,
            'iterations': iteration,
            'final_coordinates': current_mouse_pos,
            'error': error_msg
        }
        
        try:
            self.message_broker.send_visual_navigation_result(final_result)
        except Exception as e:
            # If sending fails, it's likely because no one is waiting for it
            # (e.g., user initiated visual navigation directly, not via protocol)
            pass
        
        # Display summary
        self.console.print(f"\n[bold cyan]Visual Navigation Summary[/bold cyan]")
        self.console.print(f"  Status: {final_status}")
        self.console.print(f"  Total iterations: {iteration}")
        self.console.print(f"  Actions taken: {len(actions_taken)}")
        
        if actions_taken:
            self.console.print("\n[bold]Actions:[/bold]")
            for action in actions_taken:
                self.console.print(f"  {action['iteration']}. {action['action']} at {action['coordinates']} (confidence: {action['confidence']:.2%})")
    
    def _handle_simple_protocol(self, intent: CommandIntent):
        """Handle a simple single-action protocol."""
        # Step 2: Generate protocol
        self.console.print("\n→ Generating protocol...")
        
        # Extract the actual query/text from parameters if available
        user_input_for_protocol = intent.target
        if intent.parameters:
            # For search commands, use the actual query
            if 'query' in intent.parameters:
                user_input_for_protocol = f"search for {intent.parameters['query']}"
            # For type commands, use the actual text
            elif 'text' in intent.parameters:
                user_input_for_protocol = f"type {intent.parameters['text']}"
        
        protocol = self.protocol_generator.create_protocol(intent, user_input_for_protocol)
        
        # Validate protocol
        validation = self.protocol_generator.validate_protocol(protocol)
        if not validation['valid']:
            self.console.print(f"[red]Protocol validation failed:[/red]")
            for issue in validation['issues']:
                self.console.print(f"  • {issue}")
            return
        
        if validation['warnings']:
            self.console.print("[yellow]Warnings:[/yellow]")
            for warning in validation['warnings']:
                self.console.print(f"  • {warning}")
        
        # Display protocol
        self._display_protocol(protocol)
        
        # Step 3: Confirm execution
        confirm = Prompt.ask(
            "\n[bold]Send protocol to automation engine?[/bold]",
            choices=["y", "n"],
            default="y"
        )
        
        if confirm.lower() != 'y':
            self.console.print("[yellow]Protocol cancelled[/yellow]")
            return
        
        # Step 4: Send protocol
        self.console.print("\n→ Sending protocol to automation engine...")
        # Use description as protocol_id (same as executor uses)
        protocol_id = protocol.get('metadata', {}).get('description', 'unknown')
        self.message_broker.send_protocol(protocol)
        self.console.print(f"[green]✓ Protocol sent (ID: {protocol_id})[/green]")
        
        # Step 5: Wait for execution result
        self._wait_for_result(protocol_id)
    
    def _handle_complex_protocol(self, intent: CommandIntent, user_input: str):
        """Handle a complex multi-step protocol with additional processing."""
        self.console.print("\n[bold cyan]Complex Multi-Step Protocol Detected[/bold cyan]")
        
        # Show sub-tasks
        sub_tasks = intent.parameters.get('sub_tasks', [])
        if sub_tasks:
            self.console.print(f"\n[bold]Breakdown of {len(sub_tasks)} sub-tasks:[/bold]")
            for i, task in enumerate(sub_tasks, 1):
                self.console.print(f"  {i}. {task.get('description', task.get('action', 'Unknown'))}")
        
        # Check for special requirements
        requires_research = intent.parameters.get('requires_research', False)
        requires_auth = intent.parameters.get('requires_authentication', False)
        requires_content = intent.parameters.get('requires_content_generation', False)
        
        if requires_research or requires_auth or requires_content:
            self.console.print("\n[bold yellow]Special Requirements:[/bold yellow]")
            if requires_research:
                self.console.print("  • Web research needed")
            if requires_auth:
                self.console.print("  • Authentication required (may need manual login)")
            if requires_content:
                self.console.print("  • Content generation required")
        
        # Handle content generation if needed
        generated_content = None
        if requires_content:
            self.console.print("\n→ Generating content with Gemini...")
            
            # Extract topic and parameters from sub-tasks
            topic = self._extract_content_topic(intent, user_input)
            content_params = self._extract_content_parameters(intent)
            
            # Use search results if available for context
            context = ""
            if hasattr(self, '_protocol_context') and 'search_results' in self._protocol_context:
                search_data = self._protocol_context['search_results']
                if search_data.get('trending_topics'):
                    context = f"Trending topics: {', '.join(search_data['trending_topics'][:3])}"
            
            # Generate content with context
            generated_content = self.gemini_client.generate_content(
                topic=topic,
                content_type=content_params.get('content_type', 'tweet'),
                parameters={
                    'length': content_params.get('length', 'short'),
                    'style': content_params.get('style', 'engaging'),
                    'context': context,
                    'goal': content_params.get('goal', 'engagement')
                }
            )
            self.console.print(f"[green]✓ Content generated ({len(generated_content)} characters)[/green]")
            self.console.print(f"\n[bold cyan]Generated Content:[/bold cyan]")
            self.console.print(f"[white]{generated_content}[/white]")
            
            # Store in intent and protocol context
            intent.parameters['generated_content'] = generated_content
            if not hasattr(self, '_protocol_context'):
                self._protocol_context = {}
            self._protocol_context['generated_content'] = generated_content
        
        # Handle research if needed
        if requires_research:
            self.console.print("\n→ Researching topic with Gemini...")
            query = self._extract_research_query(intent, user_input)
            
            # Use direct web search
            self.console.print(f"  Searching: {query}")
            search_results = self.gemini_client.search_web_direct(query)
            
            self.console.print(f"[green]✓ Search complete[/green]")
            
            # Display search results
            if search_results.get('summary'):
                self.console.print(f"\n[bold]Search Results:[/bold]")
                self.console.print(f"  {search_results['summary'][:200]}...")
            
            if search_results.get('key_findings'):
                self.console.print(f"\n[bold]Key Findings:[/bold]")
                for i, finding in enumerate(search_results['key_findings'][:5], 1):
                    self.console.print(f"  {i}. {finding}")
            
            if search_results.get('trending_topics'):
                self.console.print(f"\n[bold]Trending Topics:[/bold]")
                for topic in search_results['trending_topics'][:5]:
                    self.console.print(f"  • {topic}")
            
            # Store in intent and protocol metadata
            intent.parameters['research_data'] = search_results
            intent.parameters['search_results'] = search_results
            
            # Also store for protocol execution
            if not hasattr(self, '_protocol_context'):
                self._protocol_context = {}
            self._protocol_context['search_results'] = search_results
        
        # Generate protocol
        self.console.print("\n→ Generating complex protocol...")
        protocol = self.protocol_generator.create_protocol(intent, user_input)
        
        # Validate protocol
        validation = self.protocol_generator.validate_protocol(protocol)
        if not validation['valid']:
            self.console.print(f"[red]Protocol validation failed:[/red]")
            for issue in validation['issues']:
                self.console.print(f"  • {issue}")
            return
        
        if validation['warnings']:
            self.console.print("[yellow]Warnings:[/yellow]")
            for warning in validation['warnings']:
                self.console.print(f"  • {warning}")
        
        # Display protocol
        self._display_protocol(protocol)
        
        # Warn about manual steps
        if requires_auth:
            self.console.print("\n[bold yellow]Note:[/bold yellow] This protocol requires authentication.")
            self.console.print("You may need to manually log in when prompted.")
        
        # Confirm execution
        confirm = Prompt.ask(
            "\n[bold]Execute this complex protocol?[/bold]",
            choices=["y", "n"],
            default="y"
        )
        
        if confirm.lower() != 'y':
            self.console.print("[yellow]Protocol cancelled[/yellow]")
            return
        
        # Add generated content to protocol metadata
        if hasattr(self, '_protocol_context'):
            if 'generated_content' in self._protocol_context:
                if 'metadata' not in protocol:
                    protocol['metadata'] = {}
                protocol['metadata']['generated_content'] = self._protocol_context['generated_content']
            if 'search_results' in self._protocol_context:
                if 'metadata' not in protocol:
                    protocol['metadata'] = {}
                protocol['metadata']['search_results'] = self._protocol_context['search_results']
        
        # Send protocol
        self.console.print("\n→ Sending protocol to automation engine...")
        # Use description as protocol_id (same as executor uses)
        protocol_id = protocol.get('metadata', {}).get('description', 'unknown')
        self.message_broker.send_protocol(protocol)
        self.console.print(f"[green]✓ Protocol sent (ID: {protocol_id})[/green]")
        
        # Wait for execution result
        self._wait_for_result(protocol_id, timeout=60.0)  # Longer timeout for complex protocols
    
    def _extract_content_topic(self, intent: CommandIntent, user_input: str) -> str:
        """Extract the topic for content generation from intent or user input."""
        # Check sub-tasks for generate_content action
        sub_tasks = intent.parameters.get('sub_tasks', [])
        for task in sub_tasks:
            if task.get('action') == 'generate_content':
                return task.get('parameters', {}).get('topic', intent.target)
        
        # Fallback to parsing user input
        # Simple heuristic: look for "about X" or "on X"
        lower_input = user_input.lower()
        if 'about ' in lower_input:
            return lower_input.split('about ')[1].split(' and ')[0].strip()
        elif 'on ' in lower_input:
            return lower_input.split('on ')[1].split(' and ')[0].strip()
        
        return intent.target
    
    def _extract_research_query(self, intent: CommandIntent, user_input: str) -> str:
        """Extract the research query from intent or user input."""
        # Check sub-tasks for search_web action
        sub_tasks = intent.parameters.get('sub_tasks', [])
        for task in sub_tasks:
            if task.get('action') == 'search_web':
                return task.get('parameters', {}).get('query', task.get('target', ''))
        
        return self._extract_content_topic(intent, user_input)
    
    def _extract_content_parameters(self, intent: CommandIntent) -> dict:
        """Extract content generation parameters from intent."""
        # Check sub-tasks for generate_content action
        sub_tasks = intent.parameters.get('sub_tasks', [])
        for task in sub_tasks:
            if task.get('action') == 'generate_content':
                params = task.get('parameters', {})
                # Determine content type from target
                target = task.get('target', '').lower()
                if 'tweet' in target:
                    params['content_type'] = 'tweet'
                    params['length'] = 'short'
                elif 'article' in target:
                    params['content_type'] = 'article'
                    params['length'] = 'medium'
                elif 'post' in target:
                    params['content_type'] = 'post'
                    params['length'] = 'short'
                return params
        
        return {'content_type': 'text', 'length': 'medium', 'style': 'engaging'}
    
    def _display_intent(self, intent: CommandIntent):
        """Display parsed command intent."""
        table = Table(title="Parsed Intent", show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Action", intent.action)
        table.add_row("Target", intent.target or "(none)")
        table.add_row("Parameters", json.dumps(intent.parameters, indent=2) if intent.parameters else "(none)")
        table.add_row("Confidence", f"{intent.confidence:.2%}")
        
        self.console.print(table)
    
    def _display_protocol(self, protocol):
        """Display protocol actions."""
        actions = protocol.get('actions', [])
        macros = protocol.get('macros', {})
        
        # Display macros if any
        if macros:
            self.console.print(f"\n[bold cyan]Macros defined: {len(macros)}[/bold cyan]")
            for macro_name in macros.keys():
                self.console.print(f"  • {macro_name}")
        
        # Display actions
        table = Table(title=f"Protocol Actions ({len(actions)} actions)", show_header=True, header_style="bold green")
        table.add_column("#", style="dim", width=4)
        table.add_column("Action", style="cyan")
        table.add_column("Parameters", style="white")
        table.add_column("Wait", style="yellow", justify="right")
        
        for i, action in enumerate(actions, 1):
            action_name = action.get('action', 'unknown')
            params = action.get('params', {})
            wait_ms = action.get('wait_after_ms', 0)
            
            # Format parameters
            param_str = json.dumps(params, indent=None) if params else "-"
            if len(param_str) > 50:
                param_str = param_str[:47] + "..."
            
            table.add_row(
                str(i),
                action_name,
                param_str,
                f"{wait_ms}ms"
            )
        
        self.console.print(table)
    
    def _wait_for_result(self, protocol_id: str, timeout: float = 30.0):
        """
        Wait for execution result from automation engine.
        
        Args:
            protocol_id: ID of the protocol to wait for
            timeout: Maximum time to wait in seconds
        """
        self.console.print(f"\n→ Waiting for execution result (timeout: {timeout}s)...")
        
        with self.console.status("[bold green]Executing protocol...") as status:
            result = self.message_broker.receive_status(protocol_id, timeout=timeout)
        
        if result:
            self._display_result(result)
        else:
            self.console.print("[yellow]No result received (timeout or automation engine not running)[/yellow]")
    
    def _display_result(self, result: ExecutionResult):
        """Display execution result."""
        status_color = {
            "success": "green",
            "failed": "red",
            "interrupted": "yellow"
        }.get(result.status, "white")
        
        self.console.print(f"\n[bold {status_color}]Execution {result.status.upper()}[/bold {status_color}]")
        self.console.print(f"  Steps completed: {result.steps_completed}")
        self.console.print(f"  Duration: {result.duration_ms}ms")
        
        if result.error:
            self.console.print(f"  [red]Error: {result.error}[/red]")
    
    def _print_welcome(self):
        """Print welcome message."""
        welcome_text = """
[bold cyan]Welcome to AI Automation Assistant![/bold cyan]

I can help you automate tasks using natural language commands.
Now with support for complex multi-step protocols!

[bold]Simple Examples:[/bold]
  • "Click the submit button"
  • "Type hello world"
  • "Open Chrome"
  • "Search for Python tutorials"

[bold]Complex Examples:[/bold]
  • "Write an article about AI and post to X"
  • "Research Python best practices and create a summary"
  • "Open Gmail, compose email, and send to team"

[bold]Special commands:[/bold]
  • help - Show this help message
  • status - Show system status
  • clear - Clear the screen
  • exit/quit - Exit the application
"""
        self.console.print(Panel(welcome_text, border_style="cyan"))
    
    def _print_help(self):
        """Print help message."""
        help_text = """
[bold cyan]AI Automation Assistant - Help[/bold cyan]

[bold]Natural Language Commands:[/bold]
You can give commands in plain English. The AI will understand and execute them.

[bold]Simple Actions:[/bold]
  • Click - "Click the OK button", "Click at 100, 200"
  • Type - "Type hello world", "Type my email address"
  • Open App - "Open Chrome", "Launch Notepad"
  • Move Mouse - "Move mouse to center"
  • Search - "Search for Python tutorials"
  • Double Click - "Double click the file icon"
  • Right Click - "Right click the desktop"

[bold]Complex Multi-Step Commands:[/bold]
  • Research & Write - "Research AI trends and write an article"
  • Post to Social - "Write an article about AI and post to X"
  • Web Automation - "Go to example.com, login, and fill the form"
  • Content Generation - "Generate a blog post about Python"

[bold]Special Commands:[/bold]
  • help, h, ? - Show this help
  • status - Show system status
  • clear - Clear the screen
  • exit, quit, q - Exit the application

[bold]Tips:[/bold]
  • Be specific about what you want to click or interact with
  • The AI can see your screen to find elements
  • Complex commands are automatically broken down into steps
  • You'll be asked to confirm before executing protocols
  • For tasks requiring login, you may need to authenticate manually
"""
        self.console.print(Panel(help_text, border_style="cyan"))
    
    def _show_status(self):
        """Show system status."""
        table = Table(title="System Status", show_header=True, header_style="bold cyan")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="white")
        
        table.add_row("Gemini Client", "[green]✓ Connected[/green]" if self.gemini_client else "[red]✗ Not initialized[/red]")
        table.add_row("Protocol Generator", "[green]✓ Ready[/green]" if self.protocol_generator else "[red]✗ Not initialized[/red]")
        table.add_row("Message Broker", "[green]✓ Ready[/green]" if self.message_broker else "[red]✗ Not initialized[/red]")
        
        self.console.print(table)
    
    def _handle_exit(self):
        """Handle application exit."""
        self.console.print("\n[cyan]Shutting down AI Brain...[/cyan]")
        self.running = False
        self.console.print("[green]Goodbye![/green]")


def main():
    """Main entry point."""
    app = AIBrainApp()
    app.run()


if __name__ == "__main__":
    main()
