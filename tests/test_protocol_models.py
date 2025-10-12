"""
Tests for JSON Instruction Protocol Data Models
"""

import pytest
import json
from shared.protocol_models import (
    ProtocolSchema,
    ActionStep,
    MacroDefinition,
    Metadata,
    ValidationError
)


class TestMetadata:
    """Tests for Metadata class"""
    
    def test_valid_metadata(self):
        """Test valid metadata creation"""
        metadata = Metadata(
            description="Test workflow",
            complexity="medium",
            uses_vision=True,
            estimated_duration_seconds=30
        )
        metadata.validate()
        assert metadata.description == "Test workflow"
        assert metadata.complexity == "medium"
    
    def test_empty_description(self):
        """Test that empty description raises error"""
        metadata = Metadata(description="")
        with pytest.raises(ValidationError, match="description cannot be empty"):
            metadata.validate()
    
    def test_invalid_complexity(self):
        """Test that invalid complexity raises error"""
        metadata = Metadata(description="Test", complexity="invalid")
        with pytest.raises(ValidationError, match="Invalid complexity"):
            metadata.validate()


class TestActionStep:
    """Tests for ActionStep class"""
    
    def test_valid_action(self):
        """Test valid action creation"""
        action = ActionStep(
            action="press_key",
            params={"key": "enter"},
            wait_after_ms=100,
            description="Press enter key"
        )
        valid_actions = {"press_key", "type", "shortcut"}
        action.validate(valid_actions)
        assert action.action == "press_key"
    
    def test_invalid_action_name(self):
        """Test that invalid action name raises error"""
        action = ActionStep(action="invalid_action", params={})
        valid_actions = {"press_key", "type"}
        with pytest.raises(ValidationError, match="Invalid action"):
            action.validate(valid_actions)
    
    def test_negative_wait_time(self):
        """Test that negative wait time raises error"""
        action = ActionStep(action="press_key", params={}, wait_after_ms=-100)
        valid_actions = {"press_key"}
        with pytest.raises(ValidationError, match="must be non-negative"):
            action.validate(valid_actions)
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        action = ActionStep(
            action="type",
            params={"text": "hello"},
            wait_after_ms=50,
            description="Type hello"
        )
        result = action.to_dict()
        assert result["action"] == "type"
        assert result["params"]["text"] == "hello"
        assert result["wait_after_ms"] == 50
        assert result["description"] == "Type hello"
    
    def test_from_dict(self):
        """Test creation from dictionary"""
        data = {
            "action": "mouse_move",
            "params": {"x": 100, "y": 200},
            "wait_after_ms": 300,
            "description": "Move mouse"
        }
        action = ActionStep.from_dict(data)
        assert action.action == "mouse_move"
        assert action.params["x"] == 100
        assert action.wait_after_ms == 300


class TestMacroDefinition:
    """Tests for MacroDefinition class"""
    
    def test_valid_macro(self):
        """Test valid macro creation"""
        actions = [
            ActionStep(action="press_key", params={"key": "ctrl"}),
            ActionStep(action="press_key", params={"key": "c"})
        ]
        macro = MacroDefinition(name="copy", actions=actions)
        valid_actions = {"press_key"}
        macro.validate(valid_actions)
        assert macro.name == "copy"
        assert len(macro.actions) == 2
    
    def test_empty_macro_name(self):
        """Test that empty macro name raises error"""
        actions = [ActionStep(action="press_key", params={"key": "enter"})]
        macro = MacroDefinition(name="", actions=actions)
        with pytest.raises(ValidationError, match="Macro name cannot be empty"):
            macro.validate({"press_key"})
    
    def test_empty_actions(self):
        """Test that macro with no actions raises error"""
        macro = MacroDefinition(name="empty", actions=[])
        with pytest.raises(ValidationError, match="has no actions"):
            macro.validate({"press_key"})
    
    def test_circular_dependency_self(self):
        """Test that macro calling itself raises error"""
        actions = [
            ActionStep(action="macro", params={"name": "recursive"})
        ]
        macro = MacroDefinition(name="recursive", actions=actions)
        with pytest.raises(ValidationError, match="Circular dependency"):
            macro.validate({"macro"}, {"recursive"})
    
    def test_from_dict(self):
        """Test creation from dictionary"""
        actions_data = [
            {"action": "type", "params": {"text": "test"}, "wait_after_ms": 100}
        ]
        macro = MacroDefinition.from_dict("test_macro", actions_data)
        assert macro.name == "test_macro"
        assert len(macro.actions) == 1
        assert macro.actions[0].action == "type"


class TestProtocolSchema:
    """Tests for ProtocolSchema class"""
    
    def test_valid_protocol(self):
        """Test valid protocol creation and validation"""
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(description="Test protocol"),
            actions=[
                ActionStep(action="open_app", params={"app_name": "chrome"})
            ]
        )
        valid_actions = {"open_app", "macro"}
        protocol.validate(valid_actions)
        assert protocol.version == "1.0"
    
    def test_empty_version(self):
        """Test that empty version raises error"""
        protocol = ProtocolSchema(
            version="",
            metadata=Metadata(description="Test"),
            actions=[ActionStep(action="press_key", params={"key": "enter"})]
        )
        with pytest.raises(ValidationError, match="version cannot be empty"):
            protocol.validate({"press_key"})
    
    def test_no_actions(self):
        """Test that protocol with no actions raises error"""
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(description="Test"),
            actions=[]
        )
        with pytest.raises(ValidationError, match="must have at least one action"):
            protocol.validate({"press_key"})
    
    def test_undefined_macro(self):
        """Test that using undefined macro raises error"""
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(description="Test"),
            actions=[
                ActionStep(action="macro", params={"name": "undefined_macro"})
            ]
        )
        with pytest.raises(ValidationError, match="not defined"):
            protocol.validate({"macro"})
    
    def test_circular_macro_dependencies(self):
        """Test detection of circular macro dependencies"""
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
        with pytest.raises(ValidationError, match="Circular dependency"):
            protocol.validate({"macro"})
    
    def test_serialization_deserialization(self):
        """Test full serialization and deserialization cycle"""
        original = ProtocolSchema(
            version="1.0",
            metadata=Metadata(
                description="Test workflow",
                complexity="medium",
                uses_vision=True
            ),
            macros={
                "test_macro": MacroDefinition(
                    name="test_macro",
                    actions=[
                        ActionStep(action="type", params={"text": "hello"}, wait_after_ms=100)
                    ]
                )
            },
            actions=[
                ActionStep(action="open_app", params={"app_name": "chrome"}, wait_after_ms=2000),
                ActionStep(action="macro", params={"name": "test_macro", "vars": {"key": "value"}})
            ]
        )
        
        # Serialize to JSON
        json_str = original.to_json()
        
        # Deserialize from JSON
        restored = ProtocolSchema.from_json(json_str)
        
        # Verify
        assert restored.version == original.version
        assert restored.metadata.description == original.metadata.description
        assert len(restored.actions) == len(original.actions)
        assert len(restored.macros) == len(original.macros)
        assert restored.actions[0].action == "open_app"
        assert restored.actions[1].params["name"] == "test_macro"
    
    def test_from_dict_missing_fields(self):
        """Test that missing required fields raise errors"""
        # Missing version
        with pytest.raises(ValidationError, match="must have 'version'"):
            ProtocolSchema.from_dict({"metadata": {}, "actions": []})
        
        # Missing metadata
        with pytest.raises(ValidationError, match="must have 'metadata'"):
            ProtocolSchema.from_dict({"version": "1.0", "actions": []})
        
        # Missing actions
        with pytest.raises(ValidationError, match="must have 'actions'"):
            ProtocolSchema.from_dict({"version": "1.0", "metadata": {}})
    
    def test_invalid_json(self):
        """Test that invalid JSON raises error"""
        with pytest.raises(ValidationError, match="Invalid JSON"):
            ProtocolSchema.from_json("{invalid json}")
    
    def test_macro_vars_validation(self):
        """Test that macro vars must be a dictionary"""
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(description="Test"),
            macros={
                "test": MacroDefinition(
                    name="test",
                    actions=[ActionStep(action="type", params={"text": "{{var}}"})]
                )
            },
            actions=[
                ActionStep(action="macro", params={"name": "test", "vars": "not_a_dict"})
            ]
        )
        with pytest.raises(ValidationError, match="must be a dictionary"):
            protocol.validate({"macro", "type"})


class TestComplexScenarios:
    """Tests for complex protocol scenarios"""
    
    def test_nested_macros(self):
        """Test protocol with nested macros (macro calling another macro)"""
        macro_inner = MacroDefinition(
            name="inner",
            actions=[ActionStep(action="type", params={"text": "inner"})]
        )
        macro_outer = MacroDefinition(
            name="outer",
            actions=[
                ActionStep(action="macro", params={"name": "inner"}),
                ActionStep(action="type", params={"text": "outer"})
            ]
        )
        protocol = ProtocolSchema(
            version="1.0",
            metadata=Metadata(description="Nested macros test"),
            macros={"inner": macro_inner, "outer": macro_outer},
            actions=[ActionStep(action="macro", params={"name": "outer"})]
        )
        valid_actions = {"type", "macro"}
        protocol.validate(valid_actions)
        assert len(protocol.macros) == 2
    
    def test_complex_protocol_with_vision(self):
        """Test complex protocol with visual verification"""
        protocol_dict = {
            "version": "1.0",
            "metadata": {
                "description": "Complex workflow with vision",
                "complexity": "complex",
                "uses_vision": True,
                "estimated_duration_seconds": 45
            },
            "macros": {
                "search": [
                    {"action": "shortcut", "params": {"keys": ["ctrl", "l"]}, "wait_after_ms": 200},
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
        valid_actions = {"open_app", "verify_screen", "macro", "mouse_move", "shortcut", "type", "press_key"}
        protocol.validate(valid_actions)
        
        assert protocol.metadata.uses_vision is True
        assert protocol.metadata.complexity == "complex"
        assert len(protocol.actions) == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
