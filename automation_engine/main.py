"""
Automation Engine main application.
Polls for incoming protocols from AI Brain, executes them, and reports status back.

Requirements:
- 4.6: Provide real-time feedback on progress
- 7.4: Handle errors gracefully
- 8.6: Report results back to AI component
"""

import sys
import time
import signal
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from shared.protocol_executor import ProtocolExecutor
from shared.protocol_models import ProtocolSchema
from shared.action_registry import ActionRegistry
from shared.communication import MessageBroker, CommunicationError


class AutomationEngineApp:
    """
    Main application for the Automation Engine.
    Continuously polls for protocols and executes them.
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
        
        # Initialize core components
        self.action_registry = ActionRegistry()
        
        # Initialize dependencies for action handlers
        from automation_engine.input_controller import InputController
        from automation_engine.mouse_controller import MouseController
        from automation_engine.screen_capture import ScreenCapture
        from automation_engine.visual_navigation_handler import VisualNavigationHandler
        from shared.visual_verifier import VisualVerifier
        
        input_controller = InputController()
        mouse_controller = MouseController()
        screen_capture = ScreenCapture()
        
        # Initialize visual verifier with Gemini API key
        import os
        api_key = os.getenv('GEMINI_API_KEY')
        visual_verifier = None
        if api_key:
            try:
                visual_verifier = VisualVerifier(
                    api_key=api_key,
                    screen_capture=screen_capture
                )
                print("✓ Visual verifier initialized")
            except Exception as e:
                print(f"⚠ Visual verifier initialization failed: {e}")
                print("  Vision-based actions will use fallback behavior")
        else:
            print("⚠ GEMINI_API_KEY not found - vision features disabled")
        
        # Initialize message broker first (needed for visual_navigate)
        self.message_broker = MessageBroker()
        
        # Inject dependencies into action registry
        self.action_registry.inject_dependencies(
            input_controller=input_controller,
            mouse_controller=mouse_controller,
            screen_capture=screen_capture,
            visual_verifier=visual_verifier,
            message_broker=self.message_broker
        )
        
        # Register all action handlers
        from shared.action_handlers import ActionHandlers
        action_handlers = ActionHandlers(self.action_registry)
        action_handlers.register_all()
        
        self.executor = ProtocolExecutor(
            action_registry=self.action_registry,
            dry_run=dry_run
        )
        
        # Initialize visual navigation handler (message_broker already initialized above)
        self.visual_handler = VisualNavigationHandler(
            screen_capture=screen_capture,
            mouse_controller=mouse_controller,
            message_broker=self.message_broker
        )
        
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
        
        # Stop any running protocol
        if self.executor.is_running():
            print("Stopping current protocol execution...")
            self.executor.stop_execution()
            time.sleep(0.5)  # Give it time to stop
        
        self.running = False
    
    def start(self):
        """
        Start the automation engine main loop.
        Continuously polls for protocols and executes them.
        
        Requirements:
        - 4.6: Provide real-time feedback on progress
        - 7.4: Handle errors gracefully
        - 8.6: Report results back to AI component
        """
        self.running = True
        
        print("=" * 60)
        print("Automation Engine Started (Protocol System)")
        print("=" * 60)
        print(f"Mode: {'DRY RUN (simulation only)' if self.dry_run else 'LIVE EXECUTION'}")
        print(f"Poll interval: {self.poll_interval}s")
        print(f"Registered actions: {len(self.action_registry.list_actions())}")
        print("Waiting for protocols from AI Brain...")
        print("Press Ctrl+C to stop")
        print("=" * 60)
        print()
        
        protocol_count = 0
        
        try:
            while self.running:
                try:
                    # Check for visual navigation requests
                    visual_request = self.message_broker.receive_visual_navigation_request(timeout=0)
                    if visual_request:
                        self.visual_handler.handle_visual_navigation_request(visual_request)
                        continue
                    
                    # Check for visual action commands
                    action_command = self.message_broker.receive_visual_action_command(timeout=0)
                    if action_command:
                        result = self.visual_handler.execute_visual_action(action_command)
                        self.message_broker.send_visual_action_result(result)
                        continue
                    
                    # Poll for incoming protocols
                    protocol_data = self.message_broker.receive_protocol(timeout=0)
                    
                    if protocol_data:
                        protocol_count += 1
                        
                        # Parse protocol
                        try:
                            protocol = ProtocolSchema.from_dict(protocol_data)
                        except Exception as parse_error:
                            print(f"\n{'='*60}")
                            print(f"Protocol Parse Error #{protocol_count}")
                            print(f"{'='*60}")
                            print(f"Error: {parse_error}")
                            print(f"{'='*60}")
                            print()
                            continue
                        
                        print(f"\n{'='*60}")
                        print(f"Received Protocol #{protocol_count}: {protocol.metadata.description}")
                        print(f"{'='*60}")
                        print(f"Actions: {len(protocol.actions)}")
                        print(f"Macros: {len(protocol.macros)}")
                        print(f"Complexity: {protocol.metadata.complexity}")
                        print(f"Uses vision: {protocol.metadata.uses_vision}")
                        print()
                        
                        # Execute the protocol
                        result = self.executor.execute_protocol(protocol)
                        
                        # Report status back to AI Brain
                        print(f"\n{'='*60}")
                        print(f"Protocol Execution Complete")
                        print(f"{'='*60}")
                        print(f"Status: {result.status}")
                        print(f"Actions completed: {result.actions_completed}/{result.total_actions}")
                        print(f"Duration: {result.duration_ms}ms")
                        if result.error:
                            print(f"Error: {result.error}")
                        if result.error_details:
                            print(f"Error details: {result.error_details.to_dict()}")
                        print(f"{'='*60}")
                        print()
                        
                        try:
                            # Send result as status
                            self.message_broker.send_protocol_status(result)
                            print("Status reported back to AI Brain")
                        except CommunicationError as e:
                            print(f"Warning: Failed to send status: {e}")
                        
                        print("\nWaiting for next protocol...")
                    
                    # Sleep before next poll
                    time.sleep(self.poll_interval)
                
                except CommunicationError as e:
                    print(f"Communication error: {e}")
                    print("Retrying in 5 seconds...")
                    time.sleep(5)
                
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    import traceback
                    traceback.print_exc()
                    print("Continuing to poll for protocols...")
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
        
        # Stop any running protocol
        if self.executor.is_running():
            print("Stopping current protocol...")
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
        description="Automation Engine - Executes protocols from AI Brain"
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
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
