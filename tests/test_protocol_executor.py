"""
Tests for ProtocolExecutor

Tests sequential execution, context management, timing, and control flow.
"""

import pytest
import time
from unittest.mock import Mock, MagicMock

from shared.protocol_executor import ProtocolExecutor, ExecutionContext, ExecutionResult
from shared.protocol_models import ProtocolSchema, ActionStep, Metadata
from shared.action_registry import ActionRegistry, ActionCategory


class TestExecutionContext:
    """Test ExecutionContext functionality."""
    
    def test_context_initialization(self):
        """Test context is initialized correctly."""
        context = ExecutionContext(protocol_id="test_protocol")
        
        assert context.protocol_id == "test_protocol"
        assert context.variables == {}
        assert context.action_results == []
        assert context.current_action_index == 0
    
    def test_add_result(self):
        """Test adding action results."""
        context = ExecutionContext(protocol_id="test")
        
        context.add_result("press_key", None)
        context.add_result("type", "typed text")
        
        assert len(context.action_results) == 2
        assert context.action_results[0]['action'] == "press_key"
        assert context.action_results[1]['result'] == "typed text"
    
    def test_add_result_with_error(self):
        """Test adding action result with error."""
        context = ExecutionContext(protocol_id="test")
        
        context.add_result("invalid_action", None, error="Action not found")
        
        assert len(context.action_results) == 1
        assert context.action_results[0]['error'] == "Action not found"
    
    def test_get_last_result(self):
        """Test retrieving last result."""
        context = ExecutionContext(protocol_id="test")
        
        assert context.get_last_result() is None
        
        context.add_result("action1", "result1")
        assert context.get_last_result() == "result1"
        
        context.add_result("action2", "result2")
        assert context.get_last_result() == "result2"
    
    def test_variables(self):
        """Test variable storage and retrieval."""
        context = ExecutionContext(protocol_id="test")
        
        context.set_variable("x", 100)
        context.set_variable("y", 200)
        
        assert context.get_variable("x") == 100
        assert context.get_variable("y") == 200
        assert context.get_variable("z") is None
        assert context.get_variable("z", "default") == "default"
    
    def test_to_dict(self):
        """Test context serialization."""
        context = ExecutionContext(protocol_id="test")
        context.set_variable("var1", "value1")
        context.add_result("action1", "result1")
        
        context_dict = context.to_dict()
        
        assert context_dict['protocol_id'] == "test"
        assert 'start_time' in context_dict
        assert context_dict['variables'] == {"var1": "value1"}
        assert len(context_dict['action_results']) == 1


class TestProtocolExecutor:
    """Test ProtocolExecutor functionality."""
    
    @pytest.fixture
    def mock_registry(self):
        """Create a mock action registry."""
        registry = Mock(spec=ActionRegistry)
        registry.execute = Mock(return_value=None)
        return registry
    
    @pytest.fixture
    def executor(self, mock_registry):
        """Create a ProtocolExecutor instance."""
        return ProtocolExecutor(mock_registry, dry_run=False)
    
    @pytest.fixture
    def simple_protocol(self):
        """Create a simple test protocol."""
        return ProtocolSchema(
            version="1.0",
            metadata=Metadata(
                description="Test protocol",
                complexity="simple"
            ),
            actions=[
                ActionStep(action="press_key", params={"key": "enter"}, wait_after_ms=100),
                ActionStep(action="type", params={"text": "hello"}, wait_after_ms=50),
                ActionStep(action="delay", params={"ms": 500})
            ]
        )
    
    def test_executor_initialization(self, mock_registry):
        """Test executor initializes correctly."""
        executor = ProtocolExecutor(mock_registry, dry_run=True)
        
        assert executor.action_registry == mock_registry
        assert executor.dry_run is True
        assert executor._is_running is False
        assert executor._is_paused is False
        assert executor._should_stop is False
    
    def test_execute_simple_protocol(self, executor, mock_registry, simple_protocol):
        """Test executing a simple protocol."""
        result = executor.execute_protocol(simple_protocol)
        
        assert result.status == 'success'
        assert result.actions_completed == 3
        assert result.total_actions == 3
        assert result.error is None
        assert mock_registry.execute.call_count == 3
    
    def test_execute_protocol_with_timing(self, executor, mock_registry, simple_protocol):
        """Test that wait_after_ms timing is respected."""
        start_time = time.time()
        result = executor.execute_protocol(simple_protocol)
        duration = time.time() - start_time
        
        # Total wait time: 100ms + 50ms + 0ms = 150ms = 0.15s
        # Allow some tolerance for execution overhead
        assert duration >= 0.14  # At least 140ms
        assert result.status == 'success'
    
    def test_execute_protocol_dry_run(self, mock_registry):
        """Test dry run mode doesn't execute actions."""
        executor = ProtocolExecutor(mock_registry, dry_run=True)
        
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(description="Dry run test"),
            actions=[
                ActionStep(action="press_key", params={"key": "enter"})
            ]
        )
        
        result = executor.execute_protocol(protocol)
        
        assert result.status == 'success'
        assert result.actions_completed == 1
        # In dry run, execute should not be called
        assert mock_registry.execute.call_count == 0
    
    def test_execute_protocol_with_error(self, executor, mock_registry):
        """Test protocol execution handles errors."""
        mock_registry.execute.side_effect = [
            None,  # First action succeeds
            Exception("Action failed"),  # Second action fails
            None   # Third action (should not be reached)
        ]
        
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(description="Error test"),
            actions=[
                ActionStep(action="action1", params={}),
                ActionStep(action="action2", params={}),
                ActionStep(action="action3", params={})
            ]
        )
        
        result = executor.execute_protocol(protocol)
        
        assert result.status == 'failed'
        assert result.actions_completed == 1  # Only first action completed
        assert result.total_actions == 3
        assert "Action failed" in result.error
        assert mock_registry.execute.call_count == 2  # Stopped after error
    
    def test_pause_resume_execution(self, executor, mock_registry):
        """Test pause and resume controls."""
        # Make execution slow so we can pause it
        def slow_execute(*args, **kwargs):
            time.sleep(0.1)
            return None
        
        mock_registry.execute.side_effect = slow_execute
        
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(description="Pause test"),
            actions=[
                ActionStep(action="action1", params={}),
                ActionStep(action="action2", params={}),
                ActionStep(action="action3", params={})
            ]
        )
        
        # Start execution in a thread
        import threading
        result_holder = []
        
        def run_protocol():
            result = executor.execute_protocol(protocol)
            result_holder.append(result)
        
        thread = threading.Thread(target=run_protocol)
        thread.start()
        
        # Wait a bit then pause
        time.sleep(0.15)
        assert executor.pause_execution() is True
        assert executor.is_running() is True
        
        # Check status
        status = executor.get_execution_status()
        assert status['is_paused'] is True
        
        # Resume
        time.sleep(0.1)
        assert executor.resume_execution() is True
        
        # Wait for completion
        thread.join(timeout=2.0)
        
        assert len(result_holder) == 1
        assert result_holder[0].status == 'success'
    
    def test_stop_execution(self, executor, mock_registry):
        """Test emergency stop."""
        def slow_execute(*args, **kwargs):
            time.sleep(0.1)
            return None
        
        mock_registry.execute.side_effect = slow_execute
        
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(description="Stop test"),
            actions=[
                ActionStep(action="action1", params={}),
                ActionStep(action="action2", params={}),
                ActionStep(action="action3", params={})
            ]
        )
        
        # Start execution in a thread
        import threading
        result_holder = []
        
        def run_protocol():
            result = executor.execute_protocol(protocol)
            result_holder.append(result)
        
        thread = threading.Thread(target=run_protocol)
        thread.start()
        
        # Wait a bit then stop
        time.sleep(0.15)
        assert executor.stop_execution() is True
        
        # Wait for completion
        thread.join(timeout=2.0)
        
        assert len(result_holder) == 1
        result = result_holder[0]
        assert result.status == 'stopped'
        assert result.actions_completed < 3  # Should not complete all actions
        assert "stopped by user" in result.error.lower()
    
    def test_concurrent_execution_blocked(self, executor, mock_registry, simple_protocol):
        """Test that concurrent execution is blocked."""
        def slow_execute(*args, **kwargs):
            time.sleep(0.2)
            return None
        
        mock_registry.execute.side_effect = slow_execute
        
        # Start first execution in a thread
        import threading
        
        def run_protocol():
            executor.execute_protocol(simple_protocol)
        
        thread = threading.Thread(target=run_protocol)
        thread.start()
        
        # Wait a bit then try to start another
        time.sleep(0.05)
        result = executor.execute_protocol(simple_protocol)
        
        # Second execution should be rejected
        assert result.status == 'failed'
        assert 'already running' in result.error.lower()
        
        # Wait for first to complete
        thread.join(timeout=2.0)
    
    def test_get_execution_status(self, executor, simple_protocol):
        """Test getting execution status."""
        # Before execution
        status = executor.get_execution_status()
        assert status['is_running'] is False
        assert status['is_paused'] is False
        
        # During execution (we'll check in dry run for simplicity)
        executor_dry = ProtocolExecutor(Mock(), dry_run=True)
        
        import threading
        def run():
            executor_dry.execute_protocol(simple_protocol)
        
        thread = threading.Thread(target=run)
        thread.start()
        
        time.sleep(0.05)
        status = executor_dry.get_execution_status()
        
        # May or may not be running depending on timing
        # Just check the structure
        assert 'is_running' in status
        assert 'is_paused' in status
        assert 'dry_run' in status
        
        thread.join(timeout=2.0)
    
    def test_context_preservation(self, executor, mock_registry):
        """Test that context is preserved and returned."""
        mock_registry.execute.side_effect = [
            "result1",
            "result2",
            Exception("Error in action 3")
        ]
        
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(description="Context test"),
            actions=[
                ActionStep(action="action1", params={}),
                ActionStep(action="action2", params={}),
                ActionStep(action="action3", params={})
            ]
        )
        
        result = executor.execute_protocol(protocol)
        
        assert result.status == 'failed'
        assert result.context is not None
        assert len(result.context['action_results']) == 3
        
        # Check results
        assert result.context['action_results'][0]['result'] == "result1"
        assert result.context['action_results'][1]['result'] == "result2"
        assert result.context['action_results'][2]['error'] is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
