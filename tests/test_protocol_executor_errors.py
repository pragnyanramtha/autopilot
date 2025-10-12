"""
Tests for ProtocolExecutor error handling and recovery (Task 4.3)
"""

import sys
from unittest.mock import Mock

sys.path.insert(0, '.')

from shared.protocol_executor import ProtocolExecutor, ExecutionError
from shared.protocol_models import ProtocolSchema, ActionStep, Metadata
from shared.action_registry import ActionRegistry


def test_structured_error_response():
    """Test that errors are captured with structured information."""
    print("Testing structured error response...")
    
    mock_registry = Mock(spec=ActionRegistry)
    mock_registry.execute.side_effect = [
        None,  # First action succeeds
        ValueError("Invalid parameter"),  # Second action fails
        None   # Third action (should not be reached)
    ]
    
    executor = ProtocolExecutor(mock_registry, dry_run=False)
    
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(description="Error test"),
        actions=[
            ActionStep(action="action1", params={"key": "a"}),
            ActionStep(action="action2", params={"key": "b"}),
            ActionStep(action="action3", params={"key": "c"})
        ]
    )
    
    result = executor.execute_protocol(protocol)
    
    # Check basic result
    assert result.status == 'failed'
    assert result.actions_completed == 1
    assert "Invalid parameter" in result.error
    
    # Check structured error details
    assert result.error_details is not None
    error_dict = result.error_details.to_dict()
    
    assert error_dict['action_index'] == 1  # Second action (index 1)
    assert error_dict['action_name'] == 'action2'
    assert error_dict['error_type'] == 'ValueError'
    assert error_dict['error_message'] == 'Invalid parameter'
    assert 'timestamp' in error_dict
    assert error_dict['params'] == {'key': 'b'}
    
    print("✓ Structured error response passed")


def test_context_preservation_on_error():
    """Test that execution context is preserved when error occurs."""
    print("\nTesting context preservation on error...")
    
    mock_registry = Mock(spec=ActionRegistry)
    mock_registry.execute.side_effect = [
        "result1",
        "result2",
        RuntimeError("Execution failed"),
        None
    ]
    
    executor = ProtocolExecutor(mock_registry, dry_run=False)
    
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(description="Context preservation test"),
        actions=[
            ActionStep(action="action1", params={}),
            ActionStep(action="action2", params={}),
            ActionStep(action="action3", params={}),
            ActionStep(action="action4", params={})
        ]
    )
    
    result = executor.execute_protocol(protocol)
    
    assert result.status == 'failed'
    assert result.actions_completed == 2
    
    # Check context is preserved
    assert result.context is not None
    assert len(result.context['action_results']) == 3  # 2 successes + 1 error
    
    # Check successful results
    assert result.context['action_results'][0]['result'] == 'result1'
    assert result.context['action_results'][0]['error'] is None
    assert result.context['action_results'][1]['result'] == 'result2'
    assert result.context['action_results'][1]['error'] is None
    
    # Check error result
    assert result.context['action_results'][2]['result'] is None
    assert result.context['action_results'][2]['error'] is not None
    
    print("✓ Context preservation on error passed")


def test_error_in_macro():
    """Test error handling within macro execution."""
    print("\nTesting error in macro...")
    
    from shared.protocol_models import MacroDefinition
    
    mock_registry = Mock(spec=ActionRegistry)
    mock_registry.execute.side_effect = [
        None,  # First macro action succeeds
        Exception("Macro action failed"),  # Second macro action fails
        None   # Should not be reached
    ]
    
    executor = ProtocolExecutor(mock_registry, dry_run=False)
    
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(description="Macro error test"),
        macros={
            "test_macro": MacroDefinition(
                name="test_macro",
                actions=[
                    ActionStep(action="action1", params={}),
                    ActionStep(action="action2", params={}),
                    ActionStep(action="action3", params={})
                ]
            )
        },
        actions=[
            ActionStep(action="macro", params={"name": "test_macro"})
        ]
    )
    
    result = executor.execute_protocol(protocol)
    
    assert result.status == 'failed'
    assert "Macro action failed" in result.error
    
    # Error should be captured
    assert result.error_details is not None
    assert result.error_details.action_name == 'macro'
    
    print("✓ Error in macro passed")


def test_multiple_error_types():
    """Test handling of different error types."""
    print("\nTesting multiple error types...")
    
    test_cases = [
        (ValueError("Value error"), "ValueError"),
        (RuntimeError("Runtime error"), "RuntimeError"),
        (KeyError("Key error"), "KeyError"),
        (Exception("Generic error"), "Exception")
    ]
    
    for error, expected_type in test_cases:
        mock_registry = Mock(spec=ActionRegistry)
        mock_registry.execute.side_effect = error
        
        executor = ProtocolExecutor(mock_registry, dry_run=False)
        
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(description="Error type test"),
            actions=[
                ActionStep(action="test_action", params={})
            ]
        )
        
        result = executor.execute_protocol(protocol)
        
        assert result.status == 'failed'
        assert result.error_details is not None
        assert result.error_details.error_type == expected_type
    
    print("✓ Multiple error types passed")


def test_error_with_complex_params():
    """Test error capture with complex parameter structures."""
    print("\nTesting error with complex params...")
    
    mock_registry = Mock(spec=ActionRegistry)
    mock_registry.execute.side_effect = Exception("Failed")
    
    executor = ProtocolExecutor(mock_registry, dry_run=False)
    
    complex_params = {
        "text": "test",
        "options": {
            "speed": "fast",
            "retry": True
        },
        "coordinates": [100, 200]
    }
    
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(description="Complex params test"),
        actions=[
            ActionStep(action="complex_action", params=complex_params)
        ]
    )
    
    result = executor.execute_protocol(protocol)
    
    assert result.status == 'failed'
    assert result.error_details is not None
    assert result.error_details.params == complex_params
    
    print("✓ Error with complex params passed")


def test_error_recovery_information():
    """Test that error information is sufficient for recovery."""
    print("\nTesting error recovery information...")
    
    mock_registry = Mock(spec=ActionRegistry)
    mock_registry.execute.side_effect = [
        None,
        None,
        Exception("Action failed at step 3")
    ]
    
    executor = ProtocolExecutor(mock_registry, dry_run=False)
    
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(description="Recovery info test"),
        actions=[
            ActionStep(action="action1", params={"step": 1}),
            ActionStep(action="action2", params={"step": 2}),
            ActionStep(action="action3", params={"step": 3}),
            ActionStep(action="action4", params={"step": 4})
        ]
    )
    
    result = executor.execute_protocol(protocol)
    
    # Check we have enough information to resume from error point
    assert result.error_details is not None
    assert result.error_details.action_index == 2  # Failed at index 2
    assert result.context is not None
    assert result.context['current_action_index'] == 2
    
    # We know exactly where it failed and can potentially resume from index 3
    next_action_index = result.error_details.action_index + 1
    assert next_action_index == 3
    
    print("✓ Error recovery information passed")


def test_no_error_details_on_success():
    """Test that error_details is None on successful execution."""
    print("\nTesting no error details on success...")
    
    mock_registry = Mock(spec=ActionRegistry)
    mock_registry.execute = Mock(return_value=None)
    
    executor = ProtocolExecutor(mock_registry, dry_run=False)
    
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(description="Success test"),
        actions=[
            ActionStep(action="action1", params={}),
            ActionStep(action="action2", params={})
        ]
    )
    
    result = executor.execute_protocol(protocol)
    
    assert result.status == 'success'
    assert result.error is None
    assert result.error_details is None
    
    print("✓ No error details on success passed")


def test_error_serialization():
    """Test that error details can be serialized to dict."""
    print("\nTesting error serialization...")
    
    mock_registry = Mock(spec=ActionRegistry)
    mock_registry.execute.side_effect = Exception("Test error")
    
    executor = ProtocolExecutor(mock_registry, dry_run=False)
    
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(description="Serialization test"),
        actions=[
            ActionStep(action="test_action", params={"key": "value"})
        ]
    )
    
    result = executor.execute_protocol(protocol)
    
    # Convert to dict
    result_dict = result.to_dict()
    
    assert 'error' in result_dict
    assert 'error_details' in result_dict
    assert result_dict['error_details']['action_name'] == 'test_action'
    assert result_dict['error_details']['error_type'] == 'Exception'
    assert result_dict['error_details']['params'] == {"key": "value"}
    
    print("✓ Error serialization passed")


def run_all_tests():
    """Run all error handling tests."""
    print("=" * 60)
    print("Running ProtocolExecutor Error Handling Tests (Task 4.3)")
    print("=" * 60)
    
    try:
        test_structured_error_response()
        test_context_preservation_on_error()
        test_error_in_macro()
        test_multiple_error_types()
        test_error_with_complex_params()
        test_error_recovery_information()
        test_no_error_details_on_success()
        test_error_serialization()
        
        print("\n" + "=" * 60)
        print("✓ ALL ERROR HANDLING TESTS PASSED")
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
