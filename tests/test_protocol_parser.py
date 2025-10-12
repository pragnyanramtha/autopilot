"""
Tests for JSON Protocol Parser

Tests validation of:
- Schema validation
- Action parameters
- Macro validation
- Circular dependencies
- Variable substitution
- Timing validation
- Coordinate validation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.protocol_parser import JSONProtocolParser, validate_protocol_json, ValidationError
from shared.protocol_models import ProtocolSchema


def test_valid_protocol():
    """Test parsing a valid protocol"""
    json_str = """
    {
        "version": "1.0",
        "metadata": {
            "description": "Test protocol",
            "complexity": "simple"
        },
        "actions": [
            {"action": "open_app", "params": {"app_name": "chrome"}, "wait_after_ms": 2000}
        ]
    }
    """
    
    result = validate_protocol_json(json_str)
    assert result.is_valid, f"Expected valid protocol, got errors: {result.errors}"
    print("✓ Valid protocol test passed")


def test_invalid_action():
    """Test detection of invalid action name"""
    json_str = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "actions": [
            {"action": "invalid_action", "params": {}}
        ]
    }
    """
    
    result = validate_protocol_json(json_str)
    assert not result.is_valid, "Expected invalid protocol"
    assert any("invalid_action" in error.lower() for error in result.errors)
    print("✓ Invalid action test passed")


def test_missing_required_param():
    """Test detection of missing required parameters"""
    json_str = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "actions": [
            {"action": "open_app", "params": {}}
        ]
    }
    """
    
    result = validate_protocol_json(json_str)
    assert not result.is_valid, "Expected invalid protocol"
    assert any("app_name" in error for error in result.errors)
    print("✓ Missing required parameter test passed")


def test_macro_existence():
    """Test detection of undefined macro"""
    json_str = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "actions": [
            {"action": "macro", "params": {"name": "undefined_macro"}}
        ]
    }
    """
    
    result = validate_protocol_json(json_str)
    assert not result.is_valid, "Expected invalid protocol"
    assert any("undefined_macro" in error for error in result.errors)
    print("✓ Macro existence test passed")


def test_circular_dependency_simple():
    """Test detection of simple circular dependency (macro calls itself)"""
    json_str = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "macros": {
            "recursive": [
                {"action": "macro", "params": {"name": "recursive"}}
            ]
        },
        "actions": [
            {"action": "macro", "params": {"name": "recursive"}}
        ]
    }
    """
    
    result = validate_protocol_json(json_str)
    assert not result.is_valid, "Expected invalid protocol"
    assert any("circular" in error.lower() for error in result.errors)
    print("✓ Simple circular dependency test passed")


def test_circular_dependency_complex():
    """Test detection of complex circular dependency (A -> B -> C -> A)"""
    json_str = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "macros": {
            "macro_a": [
                {"action": "macro", "params": {"name": "macro_b"}}
            ],
            "macro_b": [
                {"action": "macro", "params": {"name": "macro_c"}}
            ],
            "macro_c": [
                {"action": "macro", "params": {"name": "macro_a"}}
            ]
        },
        "actions": [
            {"action": "macro", "params": {"name": "macro_a"}}
        ]
    }
    """
    
    result = validate_protocol_json(json_str)
    assert not result.is_valid, "Expected invalid protocol"
    assert any("circular" in error.lower() for error in result.errors)
    print("✓ Complex circular dependency test passed")


def test_variable_substitution_valid():
    """Test valid variable substitution"""
    json_str = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "macros": {
            "search": [
                {"action": "type", "params": {"text": "{{query}}"}}
            ]
        },
        "actions": [
            {"action": "macro", "params": {"name": "search", "vars": {"query": "test"}}}
        ]
    }
    """
    
    result = validate_protocol_json(json_str)
    assert result.is_valid, f"Expected valid protocol, got errors: {result.errors}"
    print("✓ Valid variable substitution test passed")


def test_variable_substitution_missing():
    """Test detection of missing variables"""
    json_str = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "macros": {
            "search": [
                {"action": "type", "params": {"text": "{{query}}"}}
            ]
        },
        "actions": [
            {"action": "macro", "params": {"name": "search", "vars": {}}}
        ]
    }
    """
    
    result = validate_protocol_json(json_str)
    # Should have warning about missing variable
    assert any("query" in warning.lower() for warning in result.warnings)
    print("✓ Missing variable substitution test passed")


def test_coordinate_validation():
    """Test coordinate bounds validation"""
    json_str = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "actions": [
            {"action": "mouse_move", "params": {"x": 5000, "y": 5000}}
        ]
    }
    """
    
    result = validate_protocol_json(json_str, screen_width=1920, screen_height=1080)
    # Should have warnings about coordinates out of bounds
    assert len(result.warnings) > 0
    assert any("coordinate" in warning.lower() for warning in result.warnings)
    print("✓ Coordinate validation test passed")


def test_timing_validation():
    """Test timing consistency validation"""
    json_str = """
    {
        "version": "1.0",
        "metadata": {
            "description": "Test",
            "estimated_duration_seconds": 10
        },
        "actions": [
            {"action": "delay", "params": {"ms": 1000}, "wait_after_ms": 0}
        ]
    }
    """
    
    result = validate_protocol_json(json_str)
    # Should have warning about timing inconsistency
    assert any("timing" in warning.lower() for warning in result.warnings)
    print("✓ Timing validation test passed")


def test_shortcut_keys_validation():
    """Test that shortcut action requires keys as list"""
    json_str = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "actions": [
            {"action": "shortcut", "params": {"keys": "ctrl+t"}}
        ]
    }
    """
    
    result = validate_protocol_json(json_str)
    assert not result.is_valid, "Expected invalid protocol"
    assert any("list" in error.lower() for error in result.errors)
    print("✓ Shortcut keys validation test passed")


def test_mouse_button_validation():
    """Test mouse button value validation"""
    json_str = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "actions": [
            {"action": "mouse_click", "params": {"button": "invalid"}}
        ]
    }
    """
    
    result = validate_protocol_json(json_str)
    assert not result.is_valid, "Expected invalid protocol"
    assert any("button" in error.lower() for error in result.errors)
    print("✓ Mouse button validation test passed")


def test_scroll_direction_validation():
    """Test scroll direction validation"""
    json_str = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "actions": [
            {"action": "mouse_scroll", "params": {"direction": "invalid", "amount": 5}}
        ]
    }
    """
    
    result = validate_protocol_json(json_str)
    assert not result.is_valid, "Expected invalid protocol"
    assert any("direction" in error.lower() for error in result.errors)
    print("✓ Scroll direction validation test passed")


if __name__ == "__main__":
    print("Running protocol parser tests...\n")
    
    test_valid_protocol()
    test_invalid_action()
    test_missing_required_param()
    test_macro_existence()
    test_circular_dependency_simple()
    test_circular_dependency_complex()
    test_variable_substitution_valid()
    test_variable_substitution_missing()
    test_coordinate_validation()
    test_timing_validation()
    test_shortcut_keys_validation()
    test_mouse_button_validation()
    test_scroll_direction_validation()
    
    print("\n✓ All tests passed!")
