"""
Comprehensive test demonstrating all protocol parser features
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.protocol_parser import validate_protocol_json


def test_comprehensive_protocol():
    """Test a comprehensive protocol with all features"""
    
    # Valid protocol with macros, variable substitution, and various actions
    valid_protocol = """
    {
        "version": "1.0",
        "metadata": {
            "description": "Comprehensive test protocol",
            "complexity": "medium",
            "uses_vision": true,
            "estimated_duration_seconds": 30
        },
        "macros": {
            "focus_address_bar": [
                {"action": "shortcut", "params": {"keys": ["ctrl", "l"]}, "wait_after_ms": 200}
            ],
            "search_and_navigate": [
                {"action": "macro", "params": {"name": "focus_address_bar"}},
                {"action": "type", "params": {"text": "{{url}}"}, "wait_after_ms": 100},
                {"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 3000}
            ]
        },
        "actions": [
            {
                "action": "open_app",
                "params": {"app_name": "chrome"},
                "wait_after_ms": 2000,
                "description": "Launch Chrome browser"
            },
            {
                "action": "verify_screen",
                "params": {
                    "context": "Chrome should be open",
                    "expected": "Chrome window visible"
                },
                "wait_after_ms": 500
            },
            {
                "action": "macro",
                "params": {
                    "name": "search_and_navigate",
                    "vars": {"url": "github.com"}
                },
                "wait_after_ms": 1000
            },
            {
                "action": "mouse_move",
                "params": {"x": 500, "y": 300, "smooth": true},
                "wait_after_ms": 200
            },
            {
                "action": "mouse_click",
                "params": {"button": "left", "clicks": 1},
                "wait_after_ms": 1000
            },
            {
                "action": "type",
                "params": {"text": "Hello, World!"},
                "wait_after_ms": 500
            },
            {
                "action": "shortcut",
                "params": {"keys": ["ctrl", "a"]},
                "wait_after_ms": 100
            },
            {
                "action": "copy",
                "params": {},
                "wait_after_ms": 100
            },
            {
                "action": "browser_new_tab",
                "params": {},
                "wait_after_ms": 1000
            },
            {
                "action": "paste",
                "params": {},
                "wait_after_ms": 500
            },
            {
                "action": "delay",
                "params": {"ms": 2000}
            }
        ]
    }
    """
    
    print("Testing comprehensive valid protocol...")
    result = validate_protocol_json(valid_protocol)
    
    if result.is_valid:
        print("✓ Protocol is valid!")
    else:
        print("✗ Protocol validation failed!")
        for error in result.errors:
            print(f"  ERROR: {error}")
        return False
    
    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"  WARNING: {warning}")
    
    print("\n" + "="*60)
    return True


def test_all_error_types():
    """Test detection of various error types"""
    
    print("\nTesting error detection...\n")
    
    # Test 1: Invalid action
    print("1. Testing invalid action detection...")
    invalid_action = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "actions": [{"action": "nonexistent_action", "params": {}}]
    }
    """
    result = validate_protocol_json(invalid_action)
    assert not result.is_valid
    print("   ✓ Invalid action detected")
    
    # Test 2: Missing required parameter
    print("2. Testing missing parameter detection...")
    missing_param = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "actions": [{"action": "type", "params": {}}]
    }
    """
    result = validate_protocol_json(missing_param)
    assert not result.is_valid
    print("   ✓ Missing parameter detected")
    
    # Test 3: Undefined macro
    print("3. Testing undefined macro detection...")
    undefined_macro = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "actions": [{"action": "macro", "params": {"name": "undefined"}}]
    }
    """
    result = validate_protocol_json(undefined_macro)
    assert not result.is_valid
    print("   ✓ Undefined macro detected")
    
    # Test 4: Circular dependency
    print("4. Testing circular dependency detection...")
    circular = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "macros": {
            "a": [{"action": "macro", "params": {"name": "b"}}],
            "b": [{"action": "macro", "params": {"name": "c"}}],
            "c": [{"action": "macro", "params": {"name": "a"}}]
        },
        "actions": [{"action": "macro", "params": {"name": "a"}}]
    }
    """
    result = validate_protocol_json(circular)
    assert not result.is_valid
    print("   ✓ Circular dependency detected")
    
    # Test 5: Invalid parameter type
    print("5. Testing invalid parameter type detection...")
    invalid_type = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "actions": [{"action": "shortcut", "params": {"keys": "not_a_list"}}]
    }
    """
    result = validate_protocol_json(invalid_type)
    assert not result.is_valid
    print("   ✓ Invalid parameter type detected")
    
    # Test 6: Invalid mouse button
    print("6. Testing invalid mouse button detection...")
    invalid_button = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "actions": [{"action": "mouse_click", "params": {"button": "invalid"}}]
    }
    """
    result = validate_protocol_json(invalid_button)
    assert not result.is_valid
    print("   ✓ Invalid mouse button detected")
    
    # Test 7: Invalid scroll direction
    print("7. Testing invalid scroll direction detection...")
    invalid_direction = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "actions": [{"action": "mouse_scroll", "params": {"direction": "invalid", "amount": 5}}]
    }
    """
    result = validate_protocol_json(invalid_direction)
    assert not result.is_valid
    print("   ✓ Invalid scroll direction detected")
    
    print("\n" + "="*60)


def test_all_warning_types():
    """Test detection of various warning types"""
    
    print("\nTesting warning detection...\n")
    
    # Test 1: Coordinate out of bounds
    print("1. Testing coordinate bounds warning...")
    out_of_bounds = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "actions": [{"action": "mouse_move", "params": {"x": 5000, "y": 5000}}]
    }
    """
    result = validate_protocol_json(out_of_bounds, screen_width=1920, screen_height=1080)
    assert len(result.warnings) > 0
    print("   ✓ Coordinate bounds warning generated")
    
    # Test 2: Timing inconsistency
    print("2. Testing timing inconsistency warning...")
    timing_issue = """
    {
        "version": "1.0",
        "metadata": {
            "description": "Test",
            "estimated_duration_seconds": 100
        },
        "actions": [{"action": "delay", "params": {"ms": 1000}}]
    }
    """
    result = validate_protocol_json(timing_issue)
    assert len(result.warnings) > 0
    print("   ✓ Timing inconsistency warning generated")
    
    # Test 3: Missing variable
    print("3. Testing missing variable warning...")
    missing_var = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "macros": {
            "test": [{"action": "type", "params": {"text": "{{missing_var}}"}}]
        },
        "actions": [{"action": "macro", "params": {"name": "test", "vars": {}}}]
    }
    """
    result = validate_protocol_json(missing_var)
    assert len(result.warnings) > 0
    print("   ✓ Missing variable warning generated")
    
    # Test 4: Unused variable
    print("4. Testing unused variable warning...")
    unused_var = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "macros": {
            "test": [{"action": "type", "params": {"text": "hello"}}]
        },
        "actions": [{"action": "macro", "params": {"name": "test", "vars": {"unused": "value"}}}]
    }
    """
    result = validate_protocol_json(unused_var)
    assert len(result.warnings) > 0
    print("   ✓ Unused variable warning generated")
    
    # Test 5: Unknown parameter
    print("5. Testing unknown parameter warning...")
    unknown_param = """
    {
        "version": "1.0",
        "metadata": {"description": "Test"},
        "actions": [{"action": "press_key", "params": {"key": "enter", "unknown_param": "value"}}]
    }
    """
    result = validate_protocol_json(unknown_param)
    assert len(result.warnings) > 0
    print("   ✓ Unknown parameter warning generated")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    print("="*60)
    print("COMPREHENSIVE PROTOCOL PARSER TEST")
    print("="*60)
    
    # Test valid comprehensive protocol
    success = test_comprehensive_protocol()
    
    if success:
        # Test all error types
        test_all_error_types()
        
        # Test all warning types
        test_all_warning_types()
        
        print("\n" + "="*60)
        print("✓ ALL COMPREHENSIVE TESTS PASSED!")
        print("="*60)
    else:
        print("\n✗ Comprehensive test failed!")
