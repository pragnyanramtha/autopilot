"""
Test script for AI Brain main application.
Tests initialization and basic functionality without requiring API key.
"""
import os
import sys
import json
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_brain.main import AIBrainApp


def test_config_loading():
    """Test configuration loading."""
    print("Testing configuration loading...")
    
    # Test with default config
    app = AIBrainApp()
    assert app.config is not None
    assert "gemini" in app.config
    assert "automation" in app.config
    
    print("✓ Configuration loading works")


def test_initialization_without_api_key():
    """Test that initialization fails gracefully without API key."""
    print("\nTesting initialization without API key...")
    
    # Clear any existing API key
    old_key = os.environ.get("GEMINI_API_KEY")
    if old_key:
        del os.environ["GEMINI_API_KEY"]
    
    app = AIBrainApp()
    result = app.initialize()
    
    # Should fail without API key
    assert result == False
    print("✓ Initialization correctly fails without API key")
    
    # Restore old key if it existed
    if old_key:
        os.environ["GEMINI_API_KEY"] = old_key


def test_app_structure():
    """Test that app has required methods and attributes."""
    print("\nTesting app structure...")
    
    app = AIBrainApp()
    
    # Check required methods exist
    assert hasattr(app, 'initialize')
    assert hasattr(app, 'run')
    assert hasattr(app, '_process_command')
    assert hasattr(app, '_display_intent')
    assert hasattr(app, '_display_workflow')
    assert hasattr(app, '_wait_for_result')
    assert hasattr(app, '_display_result')
    
    # Check attributes
    assert hasattr(app, 'console')
    assert hasattr(app, 'config')
    assert hasattr(app, 'gemini_client')
    assert hasattr(app, 'workflow_generator')
    assert hasattr(app, 'message_broker')
    
    print("✓ App structure is correct")


def test_command_processing_mock():
    """Test command processing with mocked components."""
    print("\nTesting command processing with mocks...")
    
    app = AIBrainApp()
    
    # Mock the components
    app.gemini_client = Mock()
    app.workflow_generator = Mock()
    app.message_broker = Mock()
    
    # Mock intent
    from ai_brain.gemini_client import CommandIntent
    mock_intent = CommandIntent(
        action="click",
        target="button",
        parameters={},
        confidence=0.9
    )
    app.gemini_client.process_command.return_value = mock_intent
    
    # Mock workflow
    from shared.data_models import Workflow, WorkflowStep
    mock_workflow = Workflow(
        id="test-123",
        steps=[
            WorkflowStep(type="click", coordinates=(100, 200), delay_ms=100)
        ],
        metadata={}
    )
    app.workflow_generator.create_workflow.return_value = mock_workflow
    app.workflow_generator.validate_workflow.return_value = {
        'valid': True,
        'issues': [],
        'warnings': []
    }
    
    # Mock result
    from shared.data_models import ExecutionResult
    mock_result = ExecutionResult(
        workflow_id="test-123",
        status="success",
        steps_completed=1,
        duration_ms=500
    )
    app.message_broker.receive_status.return_value = mock_result
    
    # Test with mocked prompt (auto-confirm)
    with patch('ai_brain.main.Prompt.ask', return_value='y'):
        try:
            app._process_command("click the button")
            print("✓ Command processing works with mocked components")
        except Exception as e:
            print(f"✗ Command processing failed: {e}")
            raise


def main():
    """Run all tests."""
    print("=" * 60)
    print("AI Brain Main Application Tests")
    print("=" * 60)
    
    try:
        test_config_loading()
        test_initialization_without_api_key()
        test_app_structure()
        test_command_processing_mock()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
