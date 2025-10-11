#!/usr/bin/env python3
"""
Unified AI Automation Assistant Launcher
Runs both AI Brain and Automation Engine in a single terminal with voice input support.
"""
import os
import sys
import threading
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if running in venv
if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("⚠️  Warning: Not running in virtual environment!")
    print("   Run: venv\\Scripts\\activate.bat (Windows) or source venv/bin/activate (Linux/Mac)")
    print()

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

# Import components
try:
    from ai_brain.gemini_client import GeminiClient
    from ai_brain.workflow_generator import WorkflowGenerator
    from automation_engine.executor import AutomationExecutor
    from shared.communication import MessageBroker
    from shared.data_models import ExecutionResult
except ImportError as e:
    console.print(f"[red]Error importing modules: {e}[/red]")
    console.print("[yellow]Run: pip install -r requirements.txt[/yellow]")
    sys.exit(1)

# Try to import voice recognition (optional)
try:
    import speech_recognition as sr
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False


class UnifiedAssistant:
    """Unified AI Assistant with voice and text input."""
    
    def __init__(self):
        self.console = Console()
        self.running = False
        self.voice_enabled = False
        
        # Components
        self.gemini_client = None
        self.workflow_generator = None
        self.executor = None
        self.message_broker = None
        
        # Voice recognition
        if VOICE_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
        
    def initialize(self):
        """Initialize all components."""
        self.console.print(Panel.fit(
            "[bold cyan]AI Automation Assistant[/bold cyan]\n"
            "Unified Interface with Voice & Text Input",
            border_style="cyan"
        ))
        
        # Check API key
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            self.console.print("[red]Error: GEMINI_API_KEY not found in .env file![/red]")
            return False
        
        try:
            # Initialize AI Brain
            self.console.print("✓ Initializing AI Brain...")
            self.gemini_client = GeminiClient(api_key=api_key)
            
            # Load config
            import json
            try:
                with open('config.json', 'r') as f:
                    config = json.load(f)
            except:
                config = {}
            
            self.workflow_generator = WorkflowGenerator(
                gemini_client=self.gemini_client,
                config=config
            )
            
            # Initialize Automation Engine
            self.console.print("✓ Initializing Automation Engine...")
            self.executor = AutomationExecutor(dry_run=False)
            
            # Initialize Communication
            self.console.print("✓ Initializing Communication...")
            self.message_broker = MessageBroker()
            
            # Check voice support
            if VOICE_AVAILABLE:
                self.console.print("✓ Voice input available")
                self.voice_enabled = True
            else:
                self.console.print("[yellow]⚠ Voice input not available (install: pip install SpeechRecognition pyaudio)[/yellow]")
            
            self.console.print("[green]✓ All systems ready![/green]\n")
            return True
            
        except Exception as e:
            self.console.print(f"[red]Initialization failed: {e}[/red]")
            return False
    
    def listen_voice(self):
        """Listen for voice input."""
        if not VOICE_AVAILABLE:
            return None
        
        try:
            with self.microphone as source:
                self.console.print("[dim]🎤 Listening... (speak now)[/dim]")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            self.console.print("[dim]🔄 Processing...[/dim]")
            text = self.recognizer.recognize_google(audio)
            return text
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            self.console.print("[yellow]Could not understand audio[/yellow]")
            return None
        except sr.RequestError as e:
            self.console.print(f"[red]Voice recognition error: {e}[/red]")
            return None
        except Exception as e:
            return None
    
    def get_input(self):
        """Get input from user (voice or text)."""
        if self.voice_enabled:
            self.console.print("\n[bold]Enter command[/bold] (type or press [cyan]V[/cyan] for voice):")
            choice = Prompt.ask("", default="")
            
            if choice.lower() == 'v':
                command = self.listen_voice()
                if command:
                    self.console.print(f"[green]🎤 Heard:[/green] {command}")
                    return command
                else:
                    return self.get_input()  # Try again
            else:
                return choice
        else:
            return Prompt.ask("\n[bold cyan]Enter command[/bold cyan]", default="")
    
    def process_command(self, user_input):
        """Process a command and execute it."""
        if not user_input.strip():
            return
        
        # Handle special commands
        if user_input.lower() in ['exit', 'quit', 'q']:
            self.running = False
            return
        elif user_input.lower() in ['help', 'h', '?']:
            self.show_help()
            return
        elif user_input.lower() == 'voice':
            self.toggle_voice()
            return
        
        try:
            # Parse command
            self.console.print(f"\n[dim]Processing: {user_input}[/dim]")
            intent = self.gemini_client.process_command(user_input)
            
            # Debug: Show parsed intent
            self.console.print(f"[dim]Action: {intent.action}, Target: {intent.target}[/dim]")
            if intent.parameters.get('open_first_result'):
                self.console.print(f"[dim]Will open first result[/dim]")
            
            if intent.confidence < 0.5:
                self.console.print(f"[yellow]Low confidence ({intent.confidence:.0%})[/yellow]")
                if intent.action == 'error':
                    self.console.print(f"[red]Error: {intent.parameters.get('error')}[/red]")
                    return
            
            # Generate workflow
            self.console.print("→ Generating workflow...")
            
            # Handle complex workflows
            complexity = intent.parameters.get('complexity', 'simple')
            if complexity == 'complex':
                self._handle_complex(intent, user_input)
            else:
                workflow = self.workflow_generator.create_workflow(intent)
                self._execute_workflow(workflow)
            
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")
    
    def _handle_complex(self, intent, user_input):
        """Handle complex workflow with content generation."""
        # Check requirements
        requires_content = intent.parameters.get('requires_content_generation', False)
        requires_research = intent.parameters.get('requires_research', False)
        
        # Generate content if needed
        if requires_content:
            self.console.print("→ Generating content...")
            topic = self._extract_topic(intent, user_input)
            content = self.gemini_client.generate_content(
                topic=topic,
                content_type='tweet',
                parameters={'length': 'short', 'style': 'engaging'}
            )
            self.console.print(f"[green]✓ Content:[/green] {content}")
            intent.parameters['generated_content'] = content
        
        # Research if needed
        if requires_research:
            self.console.print("→ Researching...")
            query = self._extract_query(intent, user_input)
            results = self.gemini_client.search_web_direct(query)
            self.console.print(f"[green]✓ Research complete[/green]")
            intent.parameters['search_results'] = results
        
        # Generate and execute workflow
        workflow = self.workflow_generator.create_workflow(intent)
        
        # Add generated content to metadata
        if requires_content:
            workflow.metadata['generated_content'] = content
        
        self._execute_workflow(workflow)
    
    def _execute_workflow(self, workflow):
        """Execute a workflow."""
        self.console.print(f"→ Executing {len(workflow.steps)} steps...")
        
        # Execute directly (no separate process)
        result = self.executor.execute_workflow(workflow)
        
        # Show result
        if result.status == 'success':
            self.console.print(f"[green]✓ Success![/green] ({result.duration_ms}ms)")
        else:
            self.console.print(f"[red]✗ {result.status}[/red]")
            if result.error:
                self.console.print(f"  Error: {result.error}")
    
    def _extract_topic(self, intent, user_input):
        """Extract topic from intent."""
        sub_tasks = intent.parameters.get('sub_tasks', [])
        for task in sub_tasks:
            if task.get('action') == 'generate_content':
                return task.get('parameters', {}).get('topic', intent.target)
        return intent.target
    
    def _extract_query(self, intent, user_input):
        """Extract search query from intent."""
        sub_tasks = intent.parameters.get('sub_tasks', [])
        for task in sub_tasks:
            if task.get('action') == 'search_web':
                return task.get('parameters', {}).get('query', intent.target)
        return intent.target
    
    def toggle_voice(self):
        """Toggle voice input on/off."""
        if not VOICE_AVAILABLE:
            self.console.print("[yellow]Voice input not available[/yellow]")
            self.console.print("Install: pip install SpeechRecognition pyaudio")
            return
        
        self.voice_enabled = not self.voice_enabled
        status = "enabled" if self.voice_enabled else "disabled"
        self.console.print(f"[cyan]Voice input {status}[/cyan]")
    
    def show_help(self):
        """Show help message."""
        help_text = """
[bold cyan]Commands:[/bold cyan]

[bold]Voice Input:[/bold]
  v, voice     - Use voice input for next command
  
[bold]Text Commands:[/bold]
  Just type naturally:
  • "Click the submit button"
  • "Search for AI trends and post to X"
  • "Type hello world"
  
[bold]Special:[/bold]
  help, h, ?   - Show this help
  voice        - Toggle voice input
  exit, quit   - Exit application
  
[bold]Tips:[/bold]
  • Voice: Press V, then speak clearly
  • Text: Just type and press Enter
  • Complex commands work automatically
"""
        self.console.print(Panel(help_text, border_style="cyan"))
    
    def run(self):
        """Main run loop."""
        if not self.initialize():
            return
        
        # Show welcome
        self.console.print(Panel(
            "[bold]Welcome to AI Automation Assistant![/bold]\n\n"
            "• Type commands naturally\n"
            "• Press [cyan]V[/cyan] for voice input\n"
            "• Type [cyan]help[/cyan] for commands\n"
            "• Type [cyan]exit[/cyan] to quit",
            border_style="green"
        ))
        
        self.running = True
        
        while self.running:
            try:
                command = self.get_input()
                if command:
                    self.process_command(command)
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Interrupted[/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
        
        self.console.print("\n[cyan]Goodbye![/cyan]")


def main():
    """Entry point."""
    assistant = UnifiedAssistant()
    assistant.run()


if __name__ == "__main__":
    main()
