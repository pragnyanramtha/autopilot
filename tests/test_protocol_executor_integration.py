"""
Integration tests for ProtocolExecutor with AutomationEngine.
Tests the complete flow from protocol reception to execution.
"""

import pytest
import time
from pathlib import Path

from shared.protocol_models import ProtocolSchema, ActionStep, Metadata, MacroDefinition
from shared.protocol_executor import ProtocolExecutor
from shared.action_registry import ActionRegistry
from shared.communication import MessageBroker


class TestProtocolExecutorIntegration:
    """Test ProtocolExecutor integration with communication layer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.action_registry = ActionRegistry()
        self.executor = ProtocolExecutor(
            action_registry=self.action_registry,
            dry_run=True
        )
        self.message_broker = MessageBroker()
        
        # Clear any existing messages
        self.message_broker.clear_messages()
    
    def teardown_method(self):
        """Clean up after tests."""
        self.message_broker.clear_messages()
    
    def test_send_and_receive_protocol(self):
        """Test sending and receiving a protocol through MessageBroker."""
        # Create a simple protocol
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(
                description="Test protocol",
                complexity="simple",
                uses_vision=False
            ),
            macros={},
            actions=[
                ActionStep(
                    action="press_key",
                    params={"key": "enter"},
                    wait_after_ms=0
                )
            ]
        )
        
        # Convert to dict and send
        protocol_dict = protocol.to_dict()
        self.message_broker.send_protocol(protocol_dict)
        
        # Receive protocol
        received = self.message_broker.receive_protocol(timeout=1.0)
        
        assert received is not None
        assert received['version'] == "1.0"
        assert received['metadata']['description'] == "Test protocol"
        assert len(received['actions']) == 1
    
    def test_execute_protocol_and_send_status(self):
        """Test executing a protocol and sending status back."""
        # Create a protocol
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(
                description="Test execution",
                complexity="simple",
                uses_vision=False
            ),
            macros={},
            actions=[
                ActionStep(
                    action="press_key",
                    params={"key": "a"},
                    wait_after_ms=50,
                    description="Press key A"
                ),
                ActionStep(
                    action="press_key",
                    params={"key": "b"},
                    wait_after_ms=50,
                    description="Press key B"
                )
            ]
        )
        
        # Execute protocol
        result = self.executor.execute_protocol(protocol)
        
        # Verify result
        assert result.status == "success"
        assert result.actions_completed == 2
        assert result.total_actions == 2
        assert result.error is None
        
        # Send status
        self.message_broker.send_protocol_status(result)
        
        # Receive status
        received_status = self.message_broker.receive_protocol_status(
            protocol_id="Test execution",
            timeout=1.0
        )
        
        assert received_status is not None
        assert received_status['status'] == "success"
        assert received_status['actions_completed'] == 2
    
    def test_protocol_with_error_sends_error_status(self):
        """Test that protocol errors are properly communicated."""
        # Create a protocol with an invalid action
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(
                description="Test error handling",
                complexity="simple",
                uses_vision=False
            ),
            macros={},
            actions=[
                # This will fail because it's not a registered action
                ActionStep(
                    action="nonexistent_action_xyz",
                    params={},
                    wait_after_ms=0
                )
            ]
        )
        
        # Execute protocol in live mode (will fail on unregistered action)
        live_executor = ProtocolExecutor(
            action_registry=self.action_registry,
            dry_run=False
        )
        result = live_executor.execute_protocol(protocol)
        
        # Verify error result
        assert result.status == "failed"
        assert result.error is not None
        assert "nonexistent_action_xyz" in result.error
        
        # Send status
        self.message_broker.send_protocol_status(result)
        
        # Receive status
        received_status = self.message_broker.receive_protocol_status(
            protocol_id="Test error handling",
            timeout=1.0
        )
        
        assert received_status is not None
        assert received_status['status'] == "failed"
        assert received_status['error'] is not None
    
    def test_pause_resume_stop_controls(self):
        """Test pause/resume/stop controls work with ProtocolExecutor."""
        # Create a protocol with multiple actions
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(
                description="Test controls",
                complexity="simple",
                uses_vision=False
            ),
            macros={},
            actions=[
                ActionStep(
                    action="press_key",
                    params={"key": "a"},
                    wait_after_ms=100
                )
                for _ in range(5)
            ]
        )
        
        # Test pause
        assert not self.executor.is_running()
        assert not self.executor.pause_execution()  # Can't pause when not running
        
        # Test status
        status = self.executor.get_execution_status()
        assert status['is_running'] is False
        assert status['is_paused'] is False
        assert status['dry_run'] is True
    
    def test_dry_run_mode(self):
        """Test that dry-run mode doesn't execute actual actions."""
        # Create a protocol
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(
                description="Test dry run",
                complexity="simple",
                uses_vision=False
            ),
            macros={},
            actions=[
                ActionStep(
                    action="press_key",
                    params={"key": "enter"},
                    wait_after_ms=0
                )
            ]
        )
        
        # Execute in dry-run mode
        result = self.executor.execute_protocol(protocol)
        
        # Should succeed without actually pressing keys
        assert result.status == "success"
        assert result.actions_completed == 1
    
    def test_protocol_with_macros(self):
        """Test protocol execution with macros."""
        # Create a protocol with macros
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(
                description="Test macros",
                complexity="medium",
                uses_vision=False
            ),
            macros={
                "test_macro": MacroDefinition(
                    name="test_macro",
                    actions=[
                        ActionStep(
                            action="press_key",
                            params={"key": "x"},
                            wait_after_ms=50
                        ),
                        ActionStep(
                            action="press_key",
                            params={"key": "y"},
                            wait_after_ms=50
                        )
                    ]
                )
            },
            actions=[
                ActionStep(
                    action="macro",
                    params={"name": "test_macro"},
                    wait_after_ms=0
                )
            ]
        )
        
        # Execute protocol
        result = self.executor.execute_protocol(protocol)
        
        # Should succeed
        assert result.status == "success"
        assert result.actions_completed == 1  # 1 macro action
    
    def test_multiple_protocols_sequential(self):
        """Test executing multiple protocols sequentially."""
        protocols = []
        
        for i in range(3):
            protocol = ProtocolSchema(
                version="1.0",
                metadata=Metadata(
                    description=f"Protocol {i}",
                    complexity="simple",
                    uses_vision=False
                ),
                macros={},
                actions=[
                    ActionStep(
                        action="press_key",
                        params={"key": "enter"},
                        wait_after_ms=50
                    )
                ]
            )
            protocols.append(protocol)
        
        # Execute all protocols
        results = []
        for protocol in protocols:
            result = self.executor.execute_protocol(protocol)
            results.append(result)
        
        # All should succeed
        for i, result in enumerate(results):
            assert result.status == "success"
            assert result.protocol_id == f"Protocol {i}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
