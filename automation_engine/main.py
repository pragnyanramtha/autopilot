"""
Automation Engine main application.
Polls for incoming workflows from AI Brain, executes them, and reports status back.

Requirements:
- 4.6: Provide real-time feedback on progress
- 7.4: Handle errors gracefully
- 8.6: Report results back to AI component
"""

import sys
import time
import signal
import json
from pathlib import Path

from automation_engine.executor import AutomationExecutor
from shared.communication import MessageBroker, CommunicationError


class AutomationEngineApp:
    """
    Main application for the Automation Engine.
    Continuously polls for workflows and executes them.
    """
    
    def __init__(self, config_path: str = "config.json", dry_run: bool = False):
        """
        Initialize the Automation Engine application.
        
        Args:
            config_path: Path to configuration file
            dry_run: If True, simulate execution without performing actual actions
        """
        self.config = self._load_config(config_path)
        self.dry_run = dry_run
        
        # Initialize components
        self.executor = AutomationExecutor(dry_run=dry_run)
        self.message_broker = MessageBroker()
        
        # Application state
        self.running = False
        self.poll_interval = 0.5  # seconds
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _load_config(self, config_path: str) -> dict:
        """
        Load configuration from JSON file.
        
        Args:
            config_path: Path to config file
            
        Returns:
            Configuration dictionary
        """
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Config file '{config_path}' not found. Using defaults.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in config file: {e}. Using defaults.")
            return {}
    
    def _signal_handler(self, signum, frame):
        """
        Handle interrupt signals for graceful shutdown.
        
        Args:
            signum: Signal number
            frame: Current stack frame
        """
        print("\n\nReceived interrupt signal. Shutting down gracefully...")
        
        # Stop any running workflow
        if self.executor.is_running():
            print("Stopping current workflow execution...")
            self.executor.stop_execution()
            time.sleep(0.5)  # Give it time to stop
        
        self.running = False
    
    def start(self):
        """
        Start the automation engine main loop.
        Continuously polls for workflows and executes them.
        
        Requirements:
        - 4.6: Provide real-time feedback on progress
        - 7.4: Handle errors gracefully
        - 8.6: Report results back to AI component
        """
        self.running = True
        
        print("=" * 60)
        print("Automation Engine Started")
        print("=" * 60)
        print(f"Mode: {'DRY RUN (simulation only)' if self.dry_run else 'LIVE EXECUTION'}")
        print(f"Poll interval: {self.poll_interval}s")
        print("Waiting for workflows from AI Brain...")
        print("Press Ctrl+C to stop")
        print("=" * 60)
        print()
        
        workflow_count = 0
        
        try:
            while self.running:
                try:
                    # Poll for incoming workflows
                    workflow = self.message_broker.receive_workflow(timeout=0)
                    
                    if workflow:
                        workflow_count += 1
                        print(f"\n{'='*60}")
                        print(f"Received Workflow #{workflow_count}: {workflow.id}")
                        print(f"{'='*60}")
                        print(f"Steps: {len(workflow.steps)}")
                        print(f"Metadata: {workflow.metadata}")
                        print()
                        
                        # Execute the workflow
                        result = self.executor.execute_workflow(workflow)
                        
                        # Report status back to AI Brain
                        print(f"\n{'='*60}")
                        print(f"Workflow Execution Complete")
                        print(f"{'='*60}")
                        print(f"Status: {result.status}")
                        print(f"Steps completed: {result.steps_completed}/{len(workflow.steps)}")
                        print(f"Duration: {result.duration_ms}ms")
                        if result.error:
                            print(f"Error: {result.error}")
                        print(f"{'='*60}")
                        print()
                        
                        try:
                            self.message_broker.send_status(result)
                            print("Status reported back to AI Brain")
                        except CommunicationError as e:
                            print(f"Warning: Failed to send status: {e}")
                        
                        print("\nWaiting for next workflow...")
                    
                    # Sleep before next poll
                    time.sleep(self.poll_interval)
                
                except CommunicationError as e:
                    print(f"Communication error: {e}")
                    print("Retrying in 5 seconds...")
                    time.sleep(5)
                
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    print("Continuing to poll for workflows...")
                    time.sleep(self.poll_interval)
        
        except KeyboardInterrupt:
            # Already handled by signal handler, but catch it here too
            pass
        
        finally:
            self._shutdown()
    
    def _shutdown(self):
        """Clean up resources and shut down gracefully."""
        print("\n" + "=" * 60)
        print("Automation Engine Shutting Down")
        print("=" * 60)
        
        # Stop any running workflow
        if self.executor.is_running():
            print("Stopping current workflow...")
            self.executor.stop_execution()
        
        print("Shutdown complete")
        print("=" * 60)


def main():
    """
    Main entry point for the Automation Engine.
    Parses command line arguments and starts the application.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Automation Engine - Executes workflows from AI Brain"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run in simulation mode without performing actual actions'
    )
    parser.add_argument(
        '--config',
        default='config.json',
        help='Path to configuration file (default: config.json)'
    )
    
    args = parser.parse_args()
    
    # Create and start the application
    app = AutomationEngineApp(
        config_path=args.config,
        dry_run=args.dry_run
    )
    
    try:
        app.start()
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
