"""
AI Automation Assistant - Command Line Interface

A unified CLI for managing the AI Brain and Automation Engine components.
Provides commands for starting/stopping automation and viewing status.

Requirements:
- 1.1: Accept natural language commands from users
- 7.5: Provide user-friendly interface for control
"""

import os
import sys
import subprocess
import signal
import time
import json
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich import print as rprint


class AutomationCLI:
    """
    Unified command-line interface for the AI Automation Assistant.
    Manages both AI Brain and Automation Engine processes.
    """
    
    def __init__(self):
        """Initialize the CLI."""
        self.console = Console()
        self.ai_brain_process: Optional[subprocess.Popen] = None
        self.automation_engine_process: Optional[subprocess.Popen] = None
        self.running = False
        
    def run(self):
        """Run the main CLI loop."""
        self.running = True
        self._print_banner()
        self._print_main_menu()
        
        while self.running:
            try:
                choice = Prompt.ask(
                    "\n[bold cyan]Select an option[/bold cyan]",
                    choices=["1", "2", "3", "4", "5", "6", "7", "8", "q"],
                    default="1"
                )
                
                if choice == "1":
                    self._start_ai_brain()
                elif choice == "2":
                    self._start_automation_engine()
                elif choice == "3":
                    self._start_both()
                elif choice == "4":
                    self._stop_ai_brain()
                elif choice == "5":
                    self._stop_automation_engine()
                elif choice == "6":
                    self._stop_both()
                elif choice == "7":
                    self._show_status()
                elif choice == "8":
                    self._show_help()
                elif choice.lower() == "q":
                    self._quit()
                    break
                    
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Interrupted by user[/yellow]")
                self._quit()
                break
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
    
    def _print_banner(self):
        """Print the application banner."""
        banner = """
[bold cyan]╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        AI AUTOMATION ASSISTANT - Control Center          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝[/bold cyan]
"""
        self.console.print(banner)
    
    def _print_main_menu(self):
        """Print the main menu."""
        menu = """
[bold]Main Menu:[/bold]

[cyan]Starting Components:[/cyan]
  [bold]1[/bold] - Start AI Brain (command processor)
  [bold]2[/bold] - Start Automation Engine (executor)
  [bold]3[/bold] - Start Both Components

[cyan]Stopping Components:[/cyan]
  [bold]4[/bold] - Stop AI Brain
  [bold]5[/bold] - Stop Automation Engine
  [bold]6[/bold] - Stop Both Components

[cyan]Information:[/cyan]
  [bold]7[/bold] - View Status
  [bold]8[/bold] - Help

[cyan]Exit:[/cyan]
  [bold]q[/bold] - Quit
"""
        self.console.print(Panel(menu, border_style="cyan", title="Options"))
    
    def _start_ai_brain(self):
        """Start the AI Brain component."""
        if self.ai_brain_process and self.ai_brain_process.poll() is None:
            self.console.print("[yellow]AI Brain is already running[/yellow]")
            return
        
        self.console.print("\n[cyan]Starting AI Brain...[/cyan]")
        
        # Check if API key is configured
        if not self._check_api_key():
            return
        
        try:
            # Start AI Brain in a new process
            if sys.platform == "win32":
                # Windows
                self.ai_brain_process = subprocess.Popen(
                    [sys.executable, "-m", "ai_brain.main"],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                # Unix-like systems
                self.ai_brain_process = subprocess.Popen(
                    [sys.executable, "-m", "ai_brain.main"],
                    start_new_session=True
                )
            
            time.sleep(1)  # Give it time to start
            
            if self.ai_brain_process.poll() is None:
                self.console.print("[green]✓ AI Brain started successfully[/green]")
                self.console.print(f"  PID: {self.ai_brain_process.pid}")
            else:
                self.console.print("[red]✗ AI Brain failed to start[/red]")
                self.ai_brain_process = None
                
        except Exception as e:
            self.console.print(f"[red]Error starting AI Brain: {e}[/red]")
            self.ai_brain_process = None
    
    def _start_automation_engine(self):
        """Start the Automation Engine component."""
        if self.automation_engine_process and self.automation_engine_process.poll() is None:
            self.console.print("[yellow]Automation Engine is already running[/yellow]")
            return
        
        self.console.print("\n[cyan]Starting Automation Engine...[/cyan]")
        
        # Ask about dry-run mode
        dry_run = Confirm.ask(
            "Start in dry-run mode (simulation only)?",
            default=False
        )
        
        try:
            # Start Automation Engine in a new process
            cmd = [sys.executable, "-m", "automation_engine.main"]
            if dry_run:
                cmd.append("--dry-run")
            
            if sys.platform == "win32":
                # Windows
                self.automation_engine_process = subprocess.Popen(
                    cmd,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                # Unix-like systems
                self.automation_engine_process = subprocess.Popen(
                    cmd,
                    start_new_session=True
                )
            
            time.sleep(1)  # Give it time to start
            
            if self.automation_engine_process.poll() is None:
                mode = "DRY-RUN" if dry_run else "LIVE"
                self.console.print(f"[green]✓ Automation Engine started successfully ({mode} mode)[/green]")
                self.console.print(f"  PID: {self.automation_engine_process.pid}")
            else:
                self.console.print("[red]✗ Automation Engine failed to start[/red]")
                self.automation_engine_process = None
                
        except Exception as e:
            self.console.print(f"[red]Error starting Automation Engine: {e}[/red]")
            self.automation_engine_process = None
    
    def _start_both(self):
        """Start both AI Brain and Automation Engine."""
        self.console.print("\n[bold cyan]Starting both components...[/bold cyan]\n")
        self._start_automation_engine()
        time.sleep(1)
        self._start_ai_brain()
        self.console.print("\n[green]✓ Both components started[/green]")
    
    def _stop_ai_brain(self):
        """Stop the AI Brain component."""
        if not self.ai_brain_process or self.ai_brain_process.poll() is not None:
            self.console.print("[yellow]AI Brain is not running[/yellow]")
            return
        
        self.console.print("\n[cyan]Stopping AI Brain...[/cyan]")
        
        try:
            self.ai_brain_process.terminate()
            self.ai_brain_process.wait(timeout=5)
            self.console.print("[green]✓ AI Brain stopped[/green]")
        except subprocess.TimeoutExpired:
            self.console.print("[yellow]Force killing AI Brain...[/yellow]")
            self.ai_brain_process.kill()
            self.console.print("[green]✓ AI Brain killed[/green]")
        except Exception as e:
            self.console.print(f"[red]Error stopping AI Brain: {e}[/red]")
        finally:
            self.ai_brain_process = None
    
    def _stop_automation_engine(self):
        """Stop the Automation Engine component."""
        if not self.automation_engine_process or self.automation_engine_process.poll() is not None:
            self.console.print("[yellow]Automation Engine is not running[/yellow]")
            return
        
        self.console.print("\n[cyan]Stopping Automation Engine...[/cyan]")
        
        try:
            self.automation_engine_process.terminate()
            self.automation_engine_process.wait(timeout=5)
            self.console.print("[green]✓ Automation Engine stopped[/green]")
        except subprocess.TimeoutExpired:
            self.console.print("[yellow]Force killing Automation Engine...[/yellow]")
            self.automation_engine_process.kill()
            self.console.print("[green]✓ Automation Engine killed[/green]")
        except Exception as e:
            self.console.print(f"[red]Error stopping Automation Engine: {e}[/red]")
        finally:
            self.automation_engine_process = None
    
    def _stop_both(self):
        """Stop both components."""
        self.console.print("\n[bold cyan]Stopping both components...[/bold cyan]\n")
        self._stop_ai_brain()
        self._stop_automation_engine()
        self.console.print("\n[green]✓ Both components stopped[/green]")
    
    def _show_status(self):
        """Show the status of all components."""
        self.console.print("\n")
        
        table = Table(title="System Status", show_header=True, header_style="bold cyan")
        table.add_column("Component", style="cyan", width=25)
        table.add_column("Status", style="white", width=15)
        table.add_column("PID", style="dim", width=10)
        table.add_column("Details", style="white")
        
        # AI Brain status
        if self.ai_brain_process and self.ai_brain_process.poll() is None:
            table.add_row(
                "AI Brain",
                "[green]● Running[/green]",
                str(self.ai_brain_process.pid),
                "Processing commands"
            )
        else:
            table.add_row(
                "AI Brain",
                "[red]○ Stopped[/red]",
                "-",
                "Not running"
            )
        
        # Automation Engine status
        if self.automation_engine_process and self.automation_engine_process.poll() is None:
            table.add_row(
                "Automation Engine",
                "[green]● Running[/green]",
                str(self.automation_engine_process.pid),
                "Waiting for workflows"
            )
        else:
            table.add_row(
                "Automation Engine",
                "[red]○ Stopped[/red]",
                "-",
                "Not running"
            )
        
        # Configuration status
        config_status = self._check_config_status()
        table.add_row(
            "Configuration",
            "[green]✓ Valid[/green]" if config_status else "[yellow]⚠ Issues[/yellow]",
            "-",
            "config.json"
        )
        
        # API Key status
        api_key_status = self._check_api_key(silent=True)
        table.add_row(
            "Gemini API Key",
            "[green]✓ Configured[/green]" if api_key_status else "[red]✗ Missing[/red]",
            "-",
            "Required for AI Brain"
        )
        
        self.console.print(table)
        
        # Show communication files status
        self._show_communication_status()
    
    def _show_communication_status(self):
        """Show the status of communication files."""
        self.console.print("\n")
        
        table = Table(title="Communication Status", show_header=True, header_style="bold cyan")
        table.add_column("File", style="cyan")
        table.add_column("Status", style="white")
        table.add_column("Messages", style="yellow", justify="right")
        
        # Check workflow queue
        workflow_file = Path("shared/workflow_queue.json")
        if workflow_file.exists():
            try:
                with open(workflow_file, 'r') as f:
                    data = json.load(f)
                    count = len(data.get("workflows", []))
                table.add_row(
                    "Workflow Queue",
                    "[green]✓ Ready[/green]",
                    str(count)
                )
            except:
                table.add_row(
                    "Workflow Queue",
                    "[yellow]⚠ Error reading[/yellow]",
                    "-"
                )
        else:
            table.add_row(
                "Workflow Queue",
                "[dim]○ Not created[/dim]",
                "0"
            )
        
        # Check status queue
        status_file = Path("shared/status_queue.json")
        if status_file.exists():
            try:
                with open(status_file, 'r') as f:
                    data = json.load(f)
                    count = len(data.get("statuses", []))
                table.add_row(
                    "Status Queue",
                    "[green]✓ Ready[/green]",
                    str(count)
                )
            except:
                table.add_row(
                    "Status Queue",
                    "[yellow]⚠ Error reading[/yellow]",
                    "-"
                )
        else:
            table.add_row(
                "Status Queue",
                "[dim]○ Not created[/dim]",
                "0"
            )
        
        self.console.print(table)
    
    def _show_help(self):
        """Show help information."""
        help_text = """
[bold cyan]AI Automation Assistant - Help[/bold cyan]

[bold]Overview:[/bold]
The AI Automation Assistant consists of two main components:

1. [cyan]AI Brain[/cyan] - Processes natural language commands and generates workflows
2. [cyan]Automation Engine[/cyan] - Executes workflows by controlling mouse/keyboard

[bold]Getting Started:[/bold]

1. Configure your Gemini API key:
   • Set environment variable: GEMINI_API_KEY=your_key_here
   • Or edit config.json

2. Start both components:
   • Option 3 from the main menu
   • Or start them individually (options 1 and 2)

3. Use the AI Brain console to give commands:
   • "Click the submit button"
   • "Type hello world"
   • "Open Chrome"

[bold]Safety Features:[/bold]
• Dry-run mode for testing without actual execution
• Confirmation required before executing workflows
• Emergency stop with Ctrl+C
• User interrupt detection

[bold]Troubleshooting:[/bold]
• If AI Brain won't start, check your API key configuration
• If Automation Engine won't start, check Python dependencies
• Use option 7 to view detailed status information
• Check the console windows for error messages

[bold]Requirements:[/bold]
• Python 3.10+
• Gemini API key
• Dependencies: google-generativeai, pyautogui, mss, pillow, rich

For more information, see README.md
"""
        self.console.print(Panel(help_text, border_style="cyan", title="Help"))
    
    def _check_api_key(self, silent: bool = False) -> bool:
        """
        Check if Gemini API key is configured.
        
        Args:
            silent: If True, don't print messages
            
        Returns:
            True if API key is configured, False otherwise
        """
        # Check environment variable
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and api_key != "YOUR_GEMINI_API_KEY_HERE":
            return True
        
        # Check config file
        try:
            with open("config.json", 'r') as f:
                config = json.load(f)
                api_key = config.get("gemini", {}).get("api_key", "")
                if api_key and api_key != "YOUR_GEMINI_API_KEY_HERE":
                    return True
        except:
            pass
        
        if not silent:
            self.console.print("[red]✗ Gemini API key not configured![/red]")
            self.console.print("\nPlease configure your API key:")
            self.console.print("  1. Set environment variable: GEMINI_API_KEY=your_key_here")
            self.console.print("  2. Or edit config.json and add your key")
        
        return False
    
    def _check_config_status(self) -> bool:
        """
        Check if configuration file is valid.
        
        Returns:
            True if config is valid, False otherwise
        """
        try:
            with open("config.json", 'r') as f:
                json.load(f)
            return True
        except:
            return False
    
    def _quit(self):
        """Quit the CLI and clean up."""
        self.console.print("\n[cyan]Shutting down...[/cyan]")
        
        # Stop any running processes
        if self.ai_brain_process and self.ai_brain_process.poll() is None:
            self.console.print("Stopping AI Brain...")
            self._stop_ai_brain()
        
        if self.automation_engine_process and self.automation_engine_process.poll() is None:
            self.console.print("Stopping Automation Engine...")
            self._stop_automation_engine()
        
        self.running = False
        self.console.print("[green]Goodbye![/green]")


def main():
    """Main entry point for the CLI."""
    cli = AutomationCLI()
    cli.run()


if __name__ == "__main__":
    main()
