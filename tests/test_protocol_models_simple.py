"""
Simple tests for JSON Instruction Protocol Data Models (no pytest required)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.protocol_models import (
    ProtocolSchema,
    ActionStep,
    MacroDefinition,
    Metadata,
    ValidationError
)


def test_metadata():
    """Test Metadata validation"""
    print("Testing Metadata...")
    
    # Valid metadata
    metadata = Metadata(description="Test", complexity="medium", uses_vision=True)
    metadata.validate()
    print("  ✓ Valid metadata passes")
    
    # Empty description
    try:
        metadata = Metadata(description="")
        metadata.validate()
        print("  ✗ Empty description should fail")
        return False
    except ValidationError:
        print("  ✓ Empty description raises error")
    
    # Invalid complexity
    try:
        metadata = Metadata(description="Test", complexity="invalid")
        metadata.validate()
        print("  ✗ Invalid complexity should fail")
        return False
    except ValidationError:
        print("  ✓ Invalid complexity raises error")
    
    return True


def test_action_step():
    """Test ActionStep validation"""
    print("\nTesting ActionStep...")
    
    # Valid action
    action = ActionStep(action="press_key", params={"key": "enter"}, wait_after_ms=100)
    action.validate({"press_key", "type"})
    print("  ✓ Valid action passes")
    
    # Invalid action name
    try:
        action = ActionStep(action="invalid", params={})
        action.validate({"press_key"})
        print("  ✗ Invalid action name should fail")
        return False
    except ValidationError:
        print("  ✓ Invalid action name raises error")
    
    # Negative wait time
    try:
        action = ActionStep(action="press_key", params={}, wait_after_ms=-100)
        action.validate({"press_key"})
        print("  ✗ Negative wait time should fail")
        return False
    except ValidationError:
        print("  ✓ Negative wait time raises error")
    
    # Test to_dict and from_dict
    action = ActionStep(action="type", params={"text": "hello"}, wait_after_ms=50)
    action_dict = action.to_dict()
    restored = ActionStep.from_dict(action_dict)
    assert restored.action == "type"
    assert restored.params["text"] == "hello"
    print("  ✓ Serialization/deserialization works")
    
    return True


def test_macro_definition():
    """Test MacroDefinition validation"""
    print("\nTesting MacroDefinition...")
    
    # Valid macro
    actions = [
        ActionStep(action="press_key", params={"key": "ctrl"}),
        ActionStep(action="press_key", params={"key": "c"})
    ]
    macro = MacroDefinition(name="copy", actions=actions)
    macro.validate({"press_key"})
    print("  ✓ Valid macro passes")
    
    # Empty name
    try:
        macro = MacroDefinition(name="", actions=actions)
        macro.validate({"press_key"})
        print("  ✗ Empty macro name should fail")
        return False
    except ValidationError:
        print("  ✓ Empty macro name raises error")
    
    # No actions
    try:
        macro = MacroDefinition(name="empty", actions=[])
        macro.validate({"press_key"})
        print("  ✗ Empty actions should fail")
        return False
    except ValidationError:
        print("  ✓ Empty actions raises error")
    
    # Circular dependency (self-reference)
    try:
        actions = [ActionStep(action="macro", params={"name": "recursive"})]
        macro = MacroDefinition(name="recursive", actions=actions)
        macro.validate({"macro"}, {"recursive"})
        print("  ✗ Circular dependency should fail")
        return False
    except ValidationError:
        print("  ✓ Circular dependency raises error")
    
    return True


def test_protocol_schema():
    """Test ProtocolSchema validation"""
    print("\nTesting ProtocolSchema...")
    
    # Valid protocol
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(description="Test protocol"),
        actions=[ActionStep(action="open_app", params={"app_name": "chrome"})]
    )
    protocol.validate({"open_app", "macro"})
    print("  ✓ Valid protocol passes")
    
    # Empty version
    try:
        protocol = ProtocolSchema(
            version="",
            metadata=Metadata(description="Test"),
            actions=[ActionStep(action="press_key", params={"key": "enter"})]
        )
        protocol.validate({"press_key"})
        print("  ✗ Empty version should fail")
        return False
    except ValidationError:
        print("  ✓ Empty version raises error")
    
    # No actions
    try:
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(description="Test"),
            actions=[]
        )
        protocol.validate({"press_key"})
        print("  ✗ No actions should fail")
        return False
    except ValidationError:
        print("  ✓ No actions raises error")
    
    # Undefined macro
    try:
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(description="Test"),
            actions=[ActionStep(action="macro", params={"name": "undefined"})]
        )
        protocol.validate({"macro"})
        print("  ✗ Undefined macro should fail")
        return False
    except ValidationError:
        print("  ✓ Undefined macro raises error")
    
    return True


def test_circular_macro_dependencies():
    """Test circular macro dependency detection"""
    print("\nTesting circular macro dependencies...")
    
    # Create two macros that call each other
    macro_a = MacroDefinition(
        name="macro_a",
        actions=[ActionStep(action="macro", params={"name": "macro_b"})]
    )
    macro_b = MacroDefinition(
        name="macro_b",
        actions=[ActionStep(action="macro", params={"name": "macro_a"})]
    )
    
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(description="Test"),
        macros={"macro_a": macro_a, "macro_b": macro_b},
        actions=[ActionStep(action="macro", params={"name": "macro_a"})]
    )
    
    try:
        protocol.validate({"macro"})
        print("  ✗ Circular macro dependency should fail")
        return False
    except ValidationError as e:
        print(f"  ✓ Circular macro dependency detected: {e}")
    
    return True


def test_serialization():
    """Test full serialization/deserialization cycle"""
    print("\nTesting serialization/deserialization...")
    
    # Create a complex protocol
    original = ProtocolSchema(
        version="1.0",
        metadata=Metadata(
            description="Test workflow",
            complexity="medium",
            uses_vision=True,
            estimated_duration_seconds=30
        ),
        macros={
            "search": MacroDefinition(
                name="search",
                actions=[
                    ActionStep(action="shortcut", params={"keys": ["ctrl", "l"]}, wait_after_ms=200),
                    ActionStep(action="type", params={"text": "{{query}}"}, wait_after_ms=100)
                ]
            )
        },
        actions=[
            ActionStep(action="open_app", params={"app_name": "chrome"}, wait_after_ms=2000),
            ActionStep(action="macro", params={"name": "search", "vars": {"query": "test"}})
        ]
    )
    
    # Serialize to JSON
    json_str = original.to_json()
    print(f"  ✓ Serialized to JSON ({len(json_str)} chars)")
    
    # Deserialize from JSON
    restored = ProtocolSchema.from_json(json_str)
    print("  ✓ Deserialized from JSON")
    
    # Verify data integrity
    assert restored.version == original.version
    assert restored.metadata.description == original.metadata.description
    assert restored.metadata.complexity == original.metadata.complexity
    assert restored.metadata.uses_vision == original.metadata.uses_vision
    assert len(restored.actions) == len(original.actions)
    assert len(restored.macros) == len(original.macros)
    assert restored.actions[0].action == "open_app"
    assert restored.actions[0].params["app_name"] == "chrome"
    assert restored.actions[1].action == "macro"
    assert restored.actions[1].params["name"] == "search"
    print("  ✓ Data integrity verified")
    
    # Validate restored protocol
    valid_actions = {"open_app", "macro", "shortcut", "type"}
    restored.validate(valid_actions)
    print("  ✓ Restored protocol validates successfully")
    
    return True


def test_complex_protocol():
    """Test complex protocol with nested macros"""
    print("\nTesting complex protocol...")
    
    protocol_dict = {
        "version": "1.0",
        "metadata": {
            "description": "Complex workflow with vision",
            "complexity": "complex",
            "uses_vision": True,
            "estimated_duration_seconds": 45
        },
        "macros": {
            "focus_address_bar": [
                {"action": "shortcut", "params": {"keys": ["ctrl", "l"]}, "wait_after_ms": 200}
            ],
            "search": [
                {"action": "macro", "params": {"name": "focus_address_bar"}},
                {"action": "type", "params": {"text": "{{query}}"}, "wait_after_ms": 100},
                {"action": "press_key", "params": {"key": "enter"}, "wait_after_ms": 3000}
            ]
        },
        "actions": [
            {"action": "open_app", "params": {"app_name": "chrome"}, "wait_after_ms": 2000},
            {"action": "verify_screen", "params": {"context": "Chrome opened", "expected": "Address bar visible"}},
            {"action": "macro", "params": {"name": "search", "vars": {"query": "test"}}},
            {"action": "mouse_move", "params": {"x": 500, "y": 300}, "wait_after_ms": 200}
        ]
    }
    
    protocol = ProtocolSchema.from_dict(protocol_dict)
    print("  ✓ Complex protocol loaded from dict")
    
    valid_actions = {"open_app", "verify_screen", "macro", "mouse_move", "shortcut", "type", "press_key"}
    protocol.validate(valid_actions)
    print("  ✓ Complex protocol validates successfully")
    
    assert protocol.metadata.uses_vision is True
    assert protocol.metadata.complexity == "complex"
    assert len(protocol.actions) == 4
    assert len(protocol.macros) == 2
    print("  ✓ Complex protocol structure verified")
    
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("Running Protocol Models Tests")
    print("=" * 60)
    
    tests = [
        test_metadata,
        test_action_step,
        test_macro_definition,
        test_protocol_schema,
        test_circular_macro_dependencies,
        test_serialization,
        test_complex_protocol
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ✗ Test failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())
