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
from rich.markdown import Markdown
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from datetime import datetime

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
        
        # Chat history
        self.chat_history = []
        
        # Voice recognition
        if VOICE_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
    
    def add_message(self, role: str, content: str, status: str = ""):
        """Add a message to chat history."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_history.append({
            'role': role,
            'content': content,
            'status': status,
            'timestamp': timestamp
        })
    
    def print_chat_message(self, role: str, content: str, status: str = ""):
        """Print a chat message with styling."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if role == "user":
            # User message - cyan bubble
            self.console.print()
            self.console.print(f"[dim]{timestamp}[/dim] [bold cyan]You:[/bold cyan]")
            self.console.print(Panel(
                content,
                border_style="cyan",
                padding=(0, 2)
            ))
        elif role == "assistant":
            # Assistant message - green bubble
            self.console.print()
            self.console.print(f"[dim]{timestamp}[/dim] [bold green]🤖 Assistant:[/bold green]")
            self.console.print(Panel(
                content,
                border_style="green",
                padding=(0, 2)
            ))
        elif role == "system":
            # System message - yellow
            self.console.print(f"[dim]{timestamp}[/dim] [yellow]⚙️  {content}[/yellow]")
        elif role == "success":
            # Success message - bright green
            self.console.print(f"[dim]{timestamp}[/dim] [bold green]✓ {content}[/bold green]")
        elif role == "error":
            # Error message - red
            self.console.print(f"[dim]{timestamp}[/dim] [bold red]✗ {content}[/bold red]")
        elif role == "info":
            # Info message - blue
            self.console.print(f"[dim]{timestamp}[/dim] [blue]ℹ️  {content}[/blue]")
        
    def initialize(self):
        """Initialize all components."""
        # Clear screen
        self.console.clear()
        
        # Show banner
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     🤖  AI AUTOMATION ASSISTANT  🤖                       ║
║                                                           ║
║     Your intelligent automation companion                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
        self.console.print(banner, style="bold cyan")
        
        # Check API key
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            self.print_chat_message("error", "GEMINI_API_KEY not found in .env file!")
            return False
        
        try:
            # Initialize AI Brain
            self.print_chat_message("system", "Initializing AI Brain...")
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
            self.print_chat_message("system", "Initializing Automation Engine...")
            self.executor = AutomationExecutor(dry_run=False)
            
            # Initialize Communication
            self.print_chat_message("system", "Initializing Communication...")
            self.message_broker = MessageBroker()
            
            # Check voice support
            if VOICE_AVAILABLE:
                self.print_chat_message("success", "Voice input available! Press 'V' to speak")
                self.voice_enabled = True
            else:
                self.print_chat_message("info", "Voice input not available (optional)")
            
            self.print_chat_message("success", "All systems ready! 🚀")
            return True
            
        except Exception as e:
            self.print_chat_message("error", f"Initialization failed: {e}")
            return False
    
    def listen_voice(self):
        """Listen for voice input."""
        if not VOICE_AVAILABLE:
            return None
        
        try:
            with self.microphone as source:
                self.print_chat_message("info", "🎤 Listening... Speak now!")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            self.print_chat_message("system", "🔄 Processing audio...")
            text = self.recognizer.recognize_google(audio)
            return text
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            self.print_chat_message("error", "Could not understand audio")
            return None
        except sr.RequestError as e:
            self.print_chat_message("error", f"Voice recognition error: {e}")
            return None
        except Exception as e:
            return None
    
    def get_input(self):
        """Get input from user (voice or text)."""
        self.console.print()
        self.console.print("─" * 60, style="dim")
        
        if self.voice_enabled:
            prompt_text = "💬 [bold cyan]You:[/bold cyan] (type or press [yellow]V[/yellow] for voice)"
        else:
            prompt_text = "💬 [bold cyan]You:[/bold cyan]"
        
        choice = Prompt.ask(prompt_text, default="")
        
        if self.voice_enabled and choice.lower() == 'v':
            command = self.listen_voice()
            if command:
                self.print_chat_message("user", f"🎤 {command}")
                return command
            else:
                return self.get_input()  # Try again
        else:
            if choice:
                self.print_chat_message("user", choice)
            return choice
    
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
            self.print_chat_message("system", "🧠 Analyzing your command...")
            intent = self.gemini_client.process_command(user_input)
            
            if intent.confidence < 0.5:
                self.print_chat_message("error", f"Low confidence ({intent.confidence:.0%})")
                if intent.action == 'error':
                    self.print_chat_message("error", intent.parameters.get('error'))
                    return
            
            # Show what we understood
            action_desc = {
                'search_web': '🔍 Searching',
                'click': '🖱️ Clicking',
                'type': '⌨️ Typing',
                'open_app': '📱 Opening app',
                'navigate_to_url': '🌐 Navigating',
                'post_to_social': '📤 Posting'
            }.get(intent.action, f'🎯 {intent.action}')
            
            self.print_chat_message("assistant", f"{action_desc}: {intent.target}")
            
            if intent.parameters.get('open_first_result'):
                self.print_chat_message("info", "Will open first search result")
            
            # Check if we need to generate content BEFORE creating workflow
            requires_content = intent.parameters.get('requires_content_generation', False)
            generated_content = None
            
            if requires_content:
                self.print_chat_message("system", "✍️ Generating content first...")
                topic = self._extract_topic(intent, user_input)
                generated_content = self.gemini_client.generate_content(
                    topic=topic,
                    content_type='tweet',
                    parameters={'length': 'short', 'style': 'engaging'}
                )
                self.print_chat_message("assistant", f"📝 Generated:\n{generated_content}")
            
            # Generate workflow
            self.print_chat_message("system", "⚙️ Generating workflow...")
            
            # Handle complex workflows
            complexity = intent.parameters.get('complexity', 'simple')
            if complexity == 'complex':
                self._handle_complex(intent, user_input, generated_content)
            else:
                workflow = self.workflow_generator.create_workflow(intent)
                if generated_content:
                    workflow.metadata['generated_content'] = generated_content
                self._execute_workflow(workflow)
            
        except Exception as e:
            self.print_chat_message("error", f"Error: {e}")
    
    def _handle_complex(self, intent, user_input, generated_content=None):
        """Handle complex workflow with content generation."""
        # Check requirements
        requires_research = intent.parameters.get('requires_research', False)
        
        # Research if needed (for complex workflows that need it)
        if requires_research:
            self.print_chat_message("system", "🔍 Researching...")
            query = self._extract_query(intent, user_input)
            results = self.gemini_client.search_web_direct(query)
            self.print_chat_message("success", "Research complete!")
            intent.parameters['search_results'] = results
        
        # Generate workflow
        workflow = self.workflow_generator.create_workflow(intent)
        
        # CRITICAL: Add generated content to workflow metadata BEFORE execution
        if generated_content:
            workflow.metadata['generated_content'] = generated_content
            self.print_chat_message("info", f"✓ Content added to workflow ({len(generated_content)} chars)")
        
        self._execute_workflow(workflow)
    
    def _execute_workflow(self, workflow):
        """Execute a workflow."""
        self.print_chat_message("system", f"🚀 Executing {len(workflow.steps)} steps...")
        
        # Execute directly (no separate process)
        result = self.executor.execute_workflow(workflow)
        
        # Show result
        if result.status == 'success':
            self.print_chat_message("success", f"Done! Completed in {result.duration_ms}ms ⚡")
        else:
            self.print_chat_message("error", f"Failed: {result.status}")
            if result.error:
                self.print_chat_message("error", f"Error: {result.error}")
    
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
        welcome = """
👋 Welcome! I'm your AI automation assistant.

I can help you:
  🔍 Search the web
  🖱️ Control your mouse and keyboard  
  📝 Generate content
  📤 Post to social media
  🌐 Navigate websites

Just tell me what you want to do in plain English!

💡 Tips:
  • Type naturally: "search for Python tutorials"
  • Press V for voice input
  • Type 'help' for more commands
  • Type 'exit' to quit
"""
        self.print_chat_message("assistant", welcome)
        
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
        
        self.console.print()
        self.print_chat_message("assistant", "👋 Goodbye! Thanks for using AI Automation Assistant!")


def main():
    """Entry point."""
    assistant = UnifiedAssistant()
    assistant.run()


if __name__ == "__main__":
    main()
