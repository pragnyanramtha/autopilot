"""
Simple test for ProtocolExecutor (no pytest dependency)
"""

import sys
import time
from unittest.mock import Mock

# Add parent directory to path
sys.path.insert(0, '.')

from shared.protocol_executor import ProtocolExecutor, ExecutionContext, ExecutionResult
from shared.protocol_models import ProtocolSchema, ActionStep, Metadata
from shared.action_registry import ActionRegistry


def test_execution_context():
    """Test ExecutionContext functionality."""
    print("Testing ExecutionContext...")
    
    context = ExecutionContext(protocol_id="test_protocol")
    assert context.protocol_id == "test_protocol"
    assert context.variables == {}
    assert context.action_results == []
    
    # Test adding results
    context.add_result("press_key", None)
    context.add_result("type", "typed text")
    assert len(context.action_results) == 2
    
    # Test variables
    context.set_variable("x", 100)
    assert context.get_variable("x") == 100
    assert context.get_variable("missing", "default") == "default"
    
    # Test serialization
    context_dict = context.to_dict()
    assert context_dict['protocol_id'] == "test_protocol"
    assert 'start_time' in context_dict
    
    print("✓ ExecutionContext tests passed")


def test_protocol_executor_basic():
    """Test basic ProtocolExecutor functionality."""
    print("\nTesting ProtocolExecutor basic functionality...")
    
    # Create mock registry
    mock_registry = Mock(spec=ActionRegistry)
    mock_registry.execute = Mock(return_value=None)
    
    # Create executor
    executor = ProtocolExecutor(mock_registry, dry_run=False)
    assert executor.action_registry == mock_registry
    assert executor.dry_run is False
    assert executor._is_running is False
    
    print("✓ ProtocolExecutor initialization passed")


def test_execute_simple_protocol():
    """Test executing a simple protocol."""
    print("\nTesting simple protocol execution...")
    
    # Create mock registry
    mock_registry = Mock(spec=ActionRegistry)
    mock_registry.execute = Mock(return_value=None)
    
    # Create executor
    executor = ProtocolExecutor(mock_registry, dry_run=False)
    
    # Create simple protocol
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(
            description="Test protocol",
            complexity="simple"
        ),
        actions=[
            ActionStep(action="press_key", params={"key": "enter"}, wait_after_ms=50),
            ActionStep(action="type", params={"text": "hello"}, wait_after_ms=50),
            ActionStep(action="delay", params={"ms": 100})
        ]
    )
    
    # Execute
    start_time = time.time()
    result = executor.execute_protocol(protocol)
    duration = time.time() - start_time
    
    # Verify results
    assert result.status == 'success', f"Expected success, got {result.status}"
    assert result.actions_completed == 3, f"Expected 3 actions, got {result.actions_completed}"
    assert result.total_actions == 3
    assert result.error is None
    assert mock_registry.execute.call_count == 3
    
    # Verify timing (50ms + 50ms = 100ms minimum)
    assert duration >= 0.09, f"Expected at least 90ms, got {duration * 1000}ms"
    
    print(f"✓ Simple protocol execution passed (duration: {duration * 1000:.0f}ms)")


def test_execute_protocol_dry_run():
    """Test dry run mode."""
    print("\nTesting dry run mode...")
    
    mock_registry = Mock(spec=ActionRegistry)
    mock_registry.execute = Mock(return_value=None)
    
    executor = ProtocolExecutor(mock_registry, dry_run=True)
    
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(description="Dry run test"),
        actions=[
            ActionStep(action="press_key", params={"key": "enter"}),
            ActionStep(action="type", params={"text": "test"})
        ]
    )
    
    result = executor.execute_protocol(protocol)
    
    assert result.status == 'success'
    assert result.actions_completed == 2
    # In dry run, execute should not be called
    assert mock_registry.execute.call_count == 0
    
    print("✓ Dry run mode passed")


def test_execute_protocol_with_error():
    """Test error handling."""
    print("\nTesting error handling...")
    
    mock_registry = Mock(spec=ActionRegistry)
    mock_registry.execute.side_effect = [
        None,  # First action succeeds
        Exception("Action failed"),  # Second action fails
        None   # Third action (should not be reached)
    ]
    
    executor = ProtocolExecutor(mock_registry, dry_run=False)
    
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
    
    # Check context preservation
    assert result.context is not None
    assert len(result.context['action_results']) == 2
    assert result.context['action_results'][1]['error'] is not None
    
    print("✓ Error handling passed")


def test_pause_resume_stop():
    """Test pause, resume, and stop controls."""
    print("\nTesting pause/resume/stop controls...")
    
    mock_registry = Mock(spec=ActionRegistry)
    executor = ProtocolExecutor(mock_registry, dry_run=False)
    
    # Test pause when not running
    assert executor.pause_execution() is False
    
    # Test resume when not running
    assert executor.resume_execution() is False
    
    # Test stop when not running
    assert executor.stop_execution() is False
    
    # Test status
    status = executor.get_execution_status()
    assert status['is_running'] is False
    assert status['is_paused'] is False
    assert status['dry_run'] is False
    
    print("✓ Pause/resume/stop controls passed")


def test_concurrent_execution_blocked():
    """Test that concurrent execution is blocked."""
    print("\nTesting concurrent execution blocking...")
    
    mock_registry = Mock(spec=ActionRegistry)
    
    def slow_execute(*args, **kwargs):
        time.sleep(0.2)
        return None
    
    mock_registry.execute.side_effect = slow_execute
    
    executor = ProtocolExecutor(mock_registry, dry_run=False)
    
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(description="Concurrent test"),
        actions=[
            ActionStep(action="action1", params={}),
            ActionStep(action="action2", params={})
        ]
    )
    
    # Start first execution in a thread
    import threading
    
    def run_protocol():
        executor.execute_protocol(protocol)
    
    thread = threading.Thread(target=run_protocol)
    thread.start()
    
    # Wait a bit then try to start another
    time.sleep(0.05)
    result = executor.execute_protocol(protocol)
    
    # Second execution should be rejected
    assert result.status == 'failed'
    assert 'already running' in result.error.lower()
    
    # Wait for first to complete
    thread.join(timeout=2.0)
    
    print("✓ Concurrent execution blocking passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running ProtocolExecutor Tests (Task 4.1)")
    print("=" * 60)
    
    try:
        test_execution_context()
        test_protocol_executor_basic()
        test_execute_simple_protocol()
        test_execute_protocol_dry_run()
        test_execute_protocol_with_error()
        test_pause_resume_stop()
        test_concurrent_execution_blocked()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
