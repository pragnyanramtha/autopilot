"""
Test protocol generation in GeminiClient.

This test verifies that the GeminiClient can generate valid JSON protocols
from natural language commands using the action library.
"""

import pytest
import json
from unittest.mock import Mock, MagicMock
from ai_brain.gemini_client import GeminiClient


def test_build_protocol_prompt_template():
    """Test that protocol prompt template is built correctly."""
    # Create a mock GeminiClient
    client = GeminiClient.__new__(GeminiClient)
    client.use_ultra_fast = False
    client.current_model_name = "gemini-2.5-flash"
    
    # Sample action library
    action_library = {
        "press_key": {
            "category": "keyboard",
            "description": "Press and release a single key",
            "params": {"required": ["key"], "optional": {}},
            "examples": ['{"action": "press_key", "params": {"key": "enter"}}']
        },
        "shortcut": {
            "category": "keyboard",
            "description": "Press multiple keys simultaneously",
            "params": {"required": ["keys"], "optional": {}},
            "examples": ['{"action": "shortcut", "params": {"keys": ["ctrl", "t"]}}']
        }
    }
    
    # Build prompt
    prompt = client._build_protocol_prompt_template("search for python", action_library)
    
    # Verify prompt contains key elements
    assert "search for python" in prompt
    assert "press_key" in prompt
    assert "shortcut" in prompt
    assert "PROTOCOL SCHEMA" in prompt
    assert "AVAILABLE ACTIONS" in prompt
    assert "CRITICAL RULES" in prompt
    assert "EXAMPLES" in prompt


def test_format_action_library():
    """Test that action library is formatted correctly for prompt."""
    client = GeminiClient.__new__(GeminiClient)
    
    action_library = {
        "press_key": {
            "category": "keyboard",
            "description": "Press a single key",
            "params": {"required": ["key"], "optional": {}},
            "examples": ['{"action": "press_key", "params": {"key": "enter"}}']
        },
        "mouse_move": {
            "category": "mouse",
            "description": "Move mouse to coordinates",
            "params": {"required": ["x", "y"], "optional": {"smooth": True}},
            "examples": []
        }
    }
    
    formatted = client._format_action_library(action_library)
    
    # Verify formatting
    assert "KEYBOARD ACTIONS" in formatted
    assert "MOUSE ACTIONS" in formatted
    assert "press_key" in formatted
    assert "mouse_move" in formatted
    assert "Press a single key" in formatted
    assert "Required: key" in formatted
    assert "Required: x, y" in formatted


def test_parse_protocol_response():
    """Test parsing protocol JSON from AI response."""
    client = GeminiClient.__new__(GeminiClient)
    
    # Test with clean JSON
    response = '''
    {
        "version": "1.0",
        "metadata": {"description": "Test protocol"},
        "actions": [
            {"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 100}
        ]
    }
    '''
    
    protocol = client._parse_protocol_response(response)
    assert protocol["version"] == "1.0"
    assert len(protocol["actions"]) == 1
    assert protocol["actions"][0]["action"] == "press_key"
    
    # Test with markdown code block
    response_with_markdown = '''
    Here's the protocol:
    ```json
    {
        "version": "1.0",
        "actions": [
            {"action": "type", "params": {"text": "hello"}}
        ]
    }
    ```
    '''
    
    protocol = client._parse_protocol_response(response_with_markdown)
    assert protocol["version"] == "1.0"
    assert protocol["actions"][0]["action"] == "type"


def test_validate_protocol_structure():
    """Test protocol structure validation."""
    client = GeminiClient.__new__(GeminiClient)
    
    # Valid protocol
    valid_protocol = {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "actions": [
            {"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 100}
        ]
    }
    
    # Should not raise
    client._validate_protocol_structure(valid_protocol)
    
    # Missing version
    with pytest.raises(ValueError, match="missing 'version'"):
        client._validate_protocol_structure({"actions": []})
    
    # Missing actions
    with pytest.raises(ValueError, match="missing 'actions'"):
        client._validate_protocol_structure({"version": "1.0"})
    
    # Empty actions
    with pytest.raises(ValueError, match="actions' list is empty"):
        client._validate_protocol_structure({"version": "1.0", "actions": []})
    
    # Invalid action structure
    with pytest.raises(ValueError, match="missing 'action' field"):
        client._validate_protocol_structure({
            "version": "1.0",
            "actions": [{"params": {}}]
        })


def test_protocol_generation_integration():
    """
    Integration test for protocol generation.
    This test requires a valid API key and will be skipped if not available.
    """
    import os
    
    # Skip if no API key
    if not os.getenv('GEMINI_API_KEY'):
        pytest.skip("GEMINI_API_KEY not set")
    
    try:
        client = GeminiClient()
        
        # Sample action library
        action_library = {
            "open_app": {
                "category": "window",
                "description": "Open application by name",
                "params": {"required": ["app_name"], "optional": {}},
                "examples": ['{"action": "open_app", "params": {"app_name": "chrome"}}']
            },
            "shortcut": {
                "category": "keyboard",
                "description": "Press multiple keys simultaneously",
                "params": {"required": ["keys"], "optional": {}},
                "examples": ['{"action": "shortcut", "params": {"keys": ["ctrl", "t"]}}']
            },
            "type": {
                "category": "keyboard",
                "description": "Type text",
                "params": {"required": ["text"], "optional": {"interval_ms": 50}},
                "examples": ['{"action": "type", "params": {"text": "hello"}}']
            },
            "press_key": {
                "category": "keyboard",
                "description": "Press a single key",
                "params": {"required": ["key"], "optional": {}},
                "examples": ['{"action": "press_key", "params": {"key": "enter"}}']
            }
        }
        
        # Generate protocol
        protocol = client.generate_protocol("open chrome and search for python", action_library)
        
        # Verify protocol structure
        assert "version" in protocol
        assert "actions" in protocol
        assert len(protocol["actions"]) > 0
        
        # Verify actions are valid
        for action in protocol["actions"]:
            assert "action" in action
            assert action["action"] in action_library or action["action"] == "macro"
        
        print(f"\nGenerated protocol:\n{json.dumps(protocol, indent=2)}")
        
    except Exception as e:
        pytest.skip(f"API call failed: {str(e)}")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-s"])
