"""
Test visual_navigate protocol action integration.

This test verifies that the visual_navigate action can be executed
from a protocol and properly integrates with the visual navigation system.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from shared.protocol_executor import ProtocolExecutor
from shared.action_registry import ActionRegistry
from shared.protocol_models import ProtocolSchema, ActionStep, Metadata


def test_visual_navigate_action_parsing():
    """Test that visual_navigate action parameters are parsed correctly."""
    # Create mock action registry with message broker
    action_registry = Mock(spec=ActionRegistry)
    action_registry.message_broker = Mock()
    action_registry.message_broker.send_visual_navigation_request = Mock()
    action_registry.message_broker.receive_visual_navigation_result = Mock(return_value={
        'status': 'success',
        'actions_taken': [],
        'iterations': 1
    })
    
    # Create protocol executor
    executor = ProtocolExecutor(action_registry, dry_run=False)
    
    # Create visual_navigate action
    action = ActionStep(
        action='visual_navigate',
        params={
            'task': 'Click the submit button',
            'goal': 'Submit the form',
            'max_iterations': 5,
            'fallback_coordinates': [500, 300],
            'timeout': 30
        },
        wait_after_ms=0
    )
    
    # Execute action
    result = executor._execute_visual_navigate(action)
    
    # Verify request was sent with correct parameters
    action_registry.message_broker.send_visual_navigation_request.assert_called_once()
    call_args = action_registry.message_broker.send_visual_navigation_request.call_args[0][0]
    
    assert call_args['task_description'] == 'Click the submit button'
    assert call_args['workflow_goal'] == 'Submit the form'
    assert call_args['max_iterations'] == 5
    assert 'request_id' in call_args
    
    # Verify result
    assert result['status'] == 'success'


def test_visual_navigate_fallback_on_failure():
    """Test that fallback coordinates are used when visual navigation fails."""
    # Create mock action registry
    action_registry = Mock(spec=ActionRegistry)
    action_registry.message_broker = Mock()
    action_registry.message_broker.send_visual_navigation_request = Mock()
    action_registry.message_broker.receive_visual_navigation_result = Mock(return_value={
        'status': 'failed',
        'error': 'Could not find target element'
    })
    action_registry.execute = Mock(return_value={'status': 'success'})
    
    # Create protocol executor
    executor = ProtocolExecutor(action_registry, dry_run=False)
    
    # Create visual_navigate action with fallback
    action = ActionStep(
        action='visual_navigate',
        params={
            'task': 'Click the submit button',
            'fallback_coordinates': [500, 300]
        },
        wait_after_ms=0
    )
    
    # Execute action
    result = executor._execute_visual_navigate(action)
    
    # Verify fallback was used
    assert result['status'] == 'fallback_success'
    assert result['action'] == 'click'
    assert result['coordinates'] == {'x': 500, 'y': 300}
    
    # Verify click action was executed
    action_registry.execute.assert_called_once_with('click', {'x': 500, 'y': 300})


def test_visual_navigate_fallback_on_timeout():
    """Test that fallback coordinates are used when visual navigation times out."""
    # Create mock action registry
    action_registry = Mock(spec=ActionRegistry)
    action_registry.message_broker = Mock()
    action_registry.message_broker.send_visual_navigation_request = Mock()
    action_registry.message_broker.receive_visual_navigation_result = Mock(return_value=None)  # Timeout
    action_registry.execute = Mock(return_value={'status': 'success'})
    
    # Create protocol executor
    executor = ProtocolExecutor(action_registry, dry_run=False)
    
    # Create visual_navigate action with fallback
    action = ActionStep(
        action='visual_navigate',
        params={
            'task': 'Click the submit button',
            'fallback_coordinates': [500, 300],
            'timeout': 1  # Short timeout for test
        },
        wait_after_ms=0
    )
    
    # Execute action
    result = executor._execute_visual_navigate(action)
    
    # Verify fallback was used
    assert result['status'] == 'fallback_success'
    action_registry.execute.assert_called_once_with('click', {'x': 500, 'y': 300})


def test_visual_navigate_no_fallback_on_timeout():
    """Test that timeout error is returned when no fallback coordinates provided."""
    # Create mock action registry
    action_registry = Mock(spec=ActionRegistry)
    action_registry.message_broker = Mock()
    action_registry.message_broker.send_visual_navigation_request = Mock()
    action_registry.message_broker.receive_visual_navigation_result = Mock(return_value=None)  # Timeout
    
    # Create protocol executor
    executor = ProtocolExecutor(action_registry, dry_run=False)
    
    # Create visual_navigate action without fallback
    action = ActionStep(
        action='visual_navigate',
        params={
            'task': 'Click the submit button',
            'timeout': 1  # Short timeout for test
        },
        wait_after_ms=0
    )
    
    # Execute action
    result = executor._execute_visual_navigate(action)
    
    # Verify timeout error
    assert result['status'] == 'timeout'
    assert 'timed out' in result['error'].lower()


def test_visual_navigate_missing_task_parameter():
    """Test that error is raised when task parameter is missing."""
    # Create mock action registry
    action_registry = Mock(spec=ActionRegistry)
    action_registry.message_broker = Mock()
    
    # Create protocol executor
    executor = ProtocolExecutor(action_registry, dry_run=False)
    
    # Create visual_navigate action without task
    action = ActionStep(
        action='visual_navigate',
        params={},
        wait_after_ms=0
    )
    
    # Execute action and expect error
    with pytest.raises(ValueError, match="requires 'task' parameter"):
        executor._execute_visual_navigate(action)


def test_visual_navigate_dry_run():
    """Test that visual_navigate action works in dry run mode."""
    # Create mock action registry
    action_registry = Mock(spec=ActionRegistry)
    
    # Create protocol executor in dry run mode
    executor = ProtocolExecutor(action_registry, dry_run=True)
    
    # Create visual_navigate action
    action = ActionStep(
        action='visual_navigate',
        params={
            'task': 'Click the submit button'
        },
        wait_after_ms=0
    )
    
    # Execute action
    result = executor._execute_visual_navigate(action)
    
    # Verify dry run result
    assert result['status'] == 'dry_run'
    assert result['task'] == 'Click the submit button'


def test_visual_navigate_in_protocol():
    """Test that visual_navigate action can be executed as part of a protocol."""
    # Create mock action registry
    action_registry = Mock(spec=ActionRegistry)
    action_registry.message_broker = Mock()
    action_registry.message_broker.send_visual_navigation_request = Mock()
    action_registry.message_broker.receive_visual_navigation_result = Mock(return_value={
        'status': 'success',
        'actions_taken': [{'action': 'click', 'coordinates': [500, 300]}],
        'iterations': 1
    })
    
    # Create protocol with visual_navigate action
    protocol = ProtocolSchema(
        version='1.0',
        metadata=Metadata(
            description='Test visual navigation protocol',
            complexity='simple',
            estimated_duration_seconds=5
        ),
        actions=[
            ActionStep(
                action='visual_navigate',
                params={
                    'task': 'Click the login button',
                    'goal': 'Navigate to login page',
                    'max_iterations': 5
                },
                wait_after_ms=0,
                description='Use AI vision to find and click login button'
            )
        ],
        macros={}
    )
    
    # Create protocol executor
    executor = ProtocolExecutor(action_registry, dry_run=False)
    
    # Execute protocol
    result = executor.execute_protocol(protocol)
    
    # Verify execution
    assert result.status == 'success'
    assert result.actions_completed == 1
    assert result.total_actions == 1
    
    # Verify visual navigation request was sent
    action_registry.message_broker.send_visual_navigation_request.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
