"""
Verification script for Task 7: Protocol Generation in GeminiClient

This script verifies that the protocol generation functionality has been
correctly implemented in the GeminiClient class.
"""

import json
from ai_brain.gemini_client import GeminiClient


def test_build_protocol_prompt_template():
    """Test that protocol prompt template is built correctly."""
    print("\n=== Test 1: Build Protocol Prompt Template ===")
    
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
    checks = [
        ("User command in prompt", "search for python" in prompt),
        ("press_key action included", "press_key" in prompt),
        ("shortcut action included", "shortcut" in prompt),
        ("PROTOCOL SCHEMA section", "PROTOCOL SCHEMA" in prompt),
        ("AVAILABLE ACTIONS section", "AVAILABLE ACTIONS" in prompt),
        ("CRITICAL RULES section", "CRITICAL RULES" in prompt),
        ("EXAMPLES section", "EXAMPLES" in prompt),
        ("press_key vs shortcut guidance", "press_key vs shortcut" in prompt),
        ("type action guidance", "type action for ANY length text" in prompt),
        ("Visual verification guidance", "Visual verification when uncertain" in prompt),
    ]
    
    all_passed = True
    for check_name, result in checks:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {check_name}")
        if not result:
            all_passed = False
    
    return all_passed


def test_format_action_library():
    """Test that action library is formatted correctly for prompt."""
    print("\n=== Test 2: Format Action Library ===")
    
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
    checks = [
        ("KEYBOARD ACTIONS header", "KEYBOARD ACTIONS" in formatted),
        ("MOUSE ACTIONS header", "MOUSE ACTIONS" in formatted),
        ("press_key action", "press_key" in formatted),
        ("mouse_move action", "mouse_move" in formatted),
        ("press_key description", "Press a single key" in formatted),
        ("Required parameters shown", "Required: key" in formatted),
        ("Multiple required params", "Required: x, y" in formatted),
    ]
    
    all_passed = True
    for check_name, result in checks:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {check_name}")
        if not result:
            all_passed = False
    
    return all_passed


def test_parse_protocol_response():
    """Test parsing protocol JSON from AI response."""
    print("\n=== Test 3: Parse Protocol Response ===")
    
    client = GeminiClient.__new__(GeminiClient)
    
    all_passed = True
    
    # Test 1: Clean JSON
    try:
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
        
        checks = [
            ("Parse clean JSON", protocol["version"] == "1.0"),
            ("Actions list parsed", len(protocol["actions"]) == 1),
            ("Action name correct", protocol["actions"][0]["action"] == "press_key"),
        ]
        
        for check_name, result in checks:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"  {status}: {check_name}")
            if not result:
                all_passed = False
    except Exception as e:
        print(f"  ✗ FAIL: Parse clean JSON - {str(e)}")
        all_passed = False
    
    # Test 2: Markdown code block
    try:
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
        
        checks = [
            ("Parse markdown JSON", protocol["version"] == "1.0"),
            ("Extract from code block", protocol["actions"][0]["action"] == "type"),
        ]
        
        for check_name, result in checks:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"  {status}: {check_name}")
            if not result:
                all_passed = False
    except Exception as e:
        print(f"  ✗ FAIL: Parse markdown JSON - {str(e)}")
        all_passed = False
    
    return all_passed


def test_validate_protocol_structure():
    """Test protocol structure validation."""
    print("\n=== Test 4: Validate Protocol Structure ===")
    
    client = GeminiClient.__new__(GeminiClient)
    
    all_passed = True
    
    # Test 1: Valid protocol
    try:
        valid_protocol = {
            "version": "1.0",
            "metadata": {"description": "Test"},
            "actions": [
                {"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 100}
            ]
        }
        
        client._validate_protocol_structure(valid_protocol)
        print("  ✓ PASS: Valid protocol accepted")
    except Exception as e:
        print(f"  ✗ FAIL: Valid protocol rejected - {str(e)}")
        all_passed = False
    
    # Test 2: Missing version
    try:
        client._validate_protocol_structure({"actions": [{"action": "test"}]})
        print("  ✗ FAIL: Missing version not detected")
        all_passed = False
    except ValueError as e:
        if "version" in str(e):
            print("  ✓ PASS: Missing version detected")
        else:
            print(f"  ✗ FAIL: Wrong error for missing version - {str(e)}")
            all_passed = False
    
    # Test 3: Missing actions
    try:
        client._validate_protocol_structure({"version": "1.0"})
        print("  ✗ FAIL: Missing actions not detected")
        all_passed = False
    except ValueError as e:
        if "actions" in str(e):
            print("  ✓ PASS: Missing actions detected")
        else:
            print(f"  ✗ FAIL: Wrong error for missing actions - {str(e)}")
            all_passed = False
    
    # Test 4: Empty actions
    try:
        client._validate_protocol_structure({"version": "1.0", "actions": []})
        print("  ✗ FAIL: Empty actions not detected")
        all_passed = False
    except ValueError as e:
        if "empty" in str(e):
            print("  ✓ PASS: Empty actions detected")
        else:
            print(f"  ✗ FAIL: Wrong error for empty actions - {str(e)}")
            all_passed = False
    
    # Test 5: Invalid action structure
    try:
        client._validate_protocol_structure({
            "version": "1.0",
            "actions": [{"params": {}}]
        })
        print("  ✗ FAIL: Missing action field not detected")
        all_passed = False
    except ValueError as e:
        if "action" in str(e):
            print("  ✓ PASS: Missing action field detected")
        else:
            print(f"  ✗ FAIL: Wrong error for missing action field - {str(e)}")
            all_passed = False
    
    return all_passed


def test_method_exists():
    """Test that generate_protocol method exists and has correct signature."""
    print("\n=== Test 5: Method Existence and Signature ===")
    
    all_passed = True
    
    # Check method exists
    if hasattr(GeminiClient, 'generate_protocol'):
        print("  ✓ PASS: generate_protocol method exists")
    else:
        print("  ✗ FAIL: generate_protocol method not found")
        all_passed = False
        return all_passed
    
    # Check method signature
    import inspect
    sig = inspect.signature(GeminiClient.generate_protocol)
    params = list(sig.parameters.keys())
    
    expected_params = ['self', 'user_input', 'action_library']
    if params == expected_params:
        print(f"  ✓ PASS: Method signature correct: {params}")
    else:
        print(f"  ✗ FAIL: Method signature incorrect. Expected {expected_params}, got {params}")
        all_passed = False
    
    # Check docstring
    if GeminiClient.generate_protocol.__doc__:
        print("  ✓ PASS: Method has docstring")
    else:
        print("  ✗ FAIL: Method missing docstring")
        all_passed = False
    
    return all_passed


def main():
    """Run all verification tests."""
    print("=" * 70)
    print("TASK 7 VERIFICATION: Protocol Generation in GeminiClient")
    print("=" * 70)
    
    results = []
    
    # Run all tests
    results.append(("Build Protocol Prompt Template", test_build_protocol_prompt_template()))
    results.append(("Format Action Library", test_format_action_library()))
    results.append(("Parse Protocol Response", test_parse_protocol_response()))
    results.append(("Validate Protocol Structure", test_validate_protocol_structure()))
    results.append(("Method Existence and Signature", test_method_exists()))
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED - Task 7 implementation verified!")
    else:
        print("✗ SOME TESTS FAILED - Please review the implementation")
    print("=" * 70)
    
    return all_passed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
