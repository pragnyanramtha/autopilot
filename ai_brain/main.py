"""
AI Brain main application.
Provides command loop for accepting user commands, generating workflows,
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
from ai_brain.workflow_generator import WorkflowGenerator
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
        self.workflow_generator: Optional[WorkflowGenerator] = None
        self.message_broker: Optional[MessageBroker] = None
        
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
            
            # Initialize workflow generator
            self.console.print("✓ Initializing workflow generator...")
            self.workflow_generator = WorkflowGenerator(
                gemini_client=self.gemini_client,
                config=self.config
            )
            
            # Initialize message broker
            self.console.print("✓ Initializing communication layer...")
            self.message_broker = MessageBroker()
            
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
        Process a user command and generate workflow.
        
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
            
            # Check if complex workflow requires additional processing
            complexity = intent.parameters.get('complexity', 'simple')
            if complexity == 'complex':
                self._handle_complex_workflow(intent, user_input)
            else:
                self._handle_simple_workflow(intent)
            
        except CommunicationError as e:
            self.console.print(f"[red]Communication error: {e}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error processing command: {e}[/red]")
    
    def _handle_simple_workflow(self, intent: CommandIntent):
        """Handle a simple single-action workflow."""
        # Step 2: Generate workflow
        self.console.print("\n→ Generating workflow...")
        workflow = self.workflow_generator.create_workflow(intent)
        
        # Validate workflow
        validation = self.workflow_generator.validate_workflow(workflow)
        if not validation['valid']:
            self.console.print(f"[red]Workflow validation failed:[/red]")
            for issue in validation['issues']:
                self.console.print(f"  • {issue}")
            return
        
        if validation['warnings']:
            self.console.print("[yellow]Warnings:[/yellow]")
            for warning in validation['warnings']:
                self.console.print(f"  • {warning}")
        
        # Display workflow
        self._display_workflow(workflow)
        
        # Step 3: Confirm execution
        confirm = Prompt.ask(
            "\n[bold]Send workflow to automation engine?[/bold]",
            choices=["y", "n"],
            default="y"
        )
        
        if confirm.lower() != 'y':
            self.console.print("[yellow]Workflow cancelled[/yellow]")
            return
        
        # Step 4: Send workflow
        self.console.print("\n→ Sending workflow to automation engine...")
        self.message_broker.send_workflow(workflow)
        self.console.print(f"[green]✓ Workflow sent (ID: {workflow.id})[/green]")
        
        # Step 5: Wait for execution result
        self._wait_for_result(workflow.id)
    
    def _handle_complex_workflow(self, intent: CommandIntent, user_input: str):
        """Handle a complex multi-step workflow with additional processing."""
        self.console.print("\n[bold cyan]Complex Multi-Step Workflow Detected[/bold cyan]")
        
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
            if hasattr(self, '_workflow_context') and 'search_results' in self._workflow_context:
                search_data = self._workflow_context['search_results']
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
            
            # Store in intent and workflow context
            intent.parameters['generated_content'] = generated_content
            if not hasattr(self, '_workflow_context'):
                self._workflow_context = {}
            self._workflow_context['generated_content'] = generated_content
        
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
            
            # Store in intent and workflow metadata
            intent.parameters['research_data'] = search_results
            intent.parameters['search_results'] = search_results
            
            # Also store for workflow execution
            if not hasattr(self, '_workflow_context'):
                self._workflow_context = {}
            self._workflow_context['search_results'] = search_results
        
        # Generate workflow
        self.console.print("\n→ Generating complex workflow...")
        workflow = self.workflow_generator.create_workflow(intent)
        
        # Validate workflow
        validation = self.workflow_generator.validate_workflow(workflow)
        if not validation['valid']:
            self.console.print(f"[red]Workflow validation failed:[/red]")
            for issue in validation['issues']:
                self.console.print(f"  • {issue}")
            return
        
        if validation['warnings']:
            self.console.print("[yellow]Warnings:[/yellow]")
            for warning in validation['warnings']:
                self.console.print(f"  • {warning}")
        
        # Display workflow
        self._display_workflow(workflow)
        
        # Warn about manual steps
        if requires_auth:
            self.console.print("\n[bold yellow]Note:[/bold yellow] This workflow requires authentication.")
            self.console.print("You may need to manually log in when prompted.")
        
        # Confirm execution
        confirm = Prompt.ask(
            "\n[bold]Execute this complex workflow?[/bold]",
            choices=["y", "n"],
            default="y"
        )
        
        if confirm.lower() != 'y':
            self.console.print("[yellow]Workflow cancelled[/yellow]")
            return
        
        # Add generated content to workflow metadata
        if hasattr(self, '_workflow_context'):
            if 'generated_content' in self._workflow_context:
                workflow.metadata['generated_content'] = self._workflow_context['generated_content']
            if 'search_results' in self._workflow_context:
                workflow.metadata['search_results'] = self._workflow_context['search_results']
        
        # Send workflow
        self.console.print("\n→ Sending workflow to automation engine...")
        self.message_broker.send_workflow(workflow)
        self.console.print(f"[green]✓ Workflow sent (ID: {workflow.id})[/green]")
        
        # Wait for execution result
        self._wait_for_result(workflow.id, timeout=60.0)  # Longer timeout for complex workflows
    
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
    
    def _display_workflow(self, workflow):
        """Display workflow steps."""
        table = Table(title=f"Workflow Steps ({len(workflow.steps)} steps)", show_header=True, header_style="bold green")
        table.add_column("#", style="dim", width=4)
        table.add_column("Type", style="cyan")
        table.add_column("Details", style="white")
        table.add_column("Delay", style="yellow", justify="right")
        
        for i, step in enumerate(workflow.steps, 1):
            details = []
            if step.coordinates:
                details.append(f"coords: {step.coordinates}")
            if step.data:
                details.append(f"data: {step.data}")
            
            table.add_row(
                str(i),
                step.type,
                ", ".join(details) if details else "-",
                f"{step.delay_ms}ms"
            )
        
        self.console.print(table)
    
    def _wait_for_result(self, workflow_id: str, timeout: float = 30.0):
        """
        Wait for execution result from automation engine.
        
        Args:
            workflow_id: ID of the workflow to wait for
            timeout: Maximum time to wait in seconds
        """
        self.console.print(f"\n→ Waiting for execution result (timeout: {timeout}s)...")
        
        with self.console.status("[bold green]Executing workflow...") as status:
            result = self.message_broker.receive_status(workflow_id, timeout=timeout)
        
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
Now with support for complex multi-step workflows!

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
  • You'll be asked to confirm before executing workflows
  • For tasks requiring login, you may need to authenticate manually
"""
        self.console.print(Panel(help_text, border_style="cyan"))
    
    def _show_status(self):
        """Show system status."""
        table = Table(title="System Status", show_header=True, header_style="bold cyan")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="white")
        
        table.add_row("Gemini Client", "[green]✓ Connected[/green]" if self.gemini_client else "[red]✗ Not initialized[/red]")
        table.add_row("Workflow Generator", "[green]✓ Ready[/green]" if self.workflow_generator else "[red]✗ Not initialized[/red]")
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
