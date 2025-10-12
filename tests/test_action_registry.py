"""
Tests for Action Registry and Action Handlers
"""

import pytest
from shared.action_registry import ActionRegistry, ActionCategory
from shared.action_handlers import ActionHandlers


def test_action_registry_initialization():
    """Test that ActionRegistry initializes correctly."""
    registry = ActionRegistry()
    assert registry is not None
    assert len(registry._handlers) == 0


def test_register_action():
    """Test registering a simple action."""
    registry = ActionRegistry()
    
    def test_handler(param1: str):
        return f"Executed with {param1}"
    
    registry.register(
        name="test_action",
        category=ActionCategory.KEYBOARD,
        description="Test action",
        handler=test_handler,
        required_params=["param1"]
    )
    
    assert "test_action" in registry._handlers
    assert registry._handlers["test_action"].name == "test_action"


def test_execute_action():
    """Test executing a registered action."""
    registry = ActionRegistry()
    
    def test_handler(param1: str):
        return f"Result: {param1}"
    
    registry.register(
        name="test_action",
        category=ActionCategory.KEYBOARD,
        description="Test action",
        handler=test_handler,
        required_params=["param1"]
    )
    
    result = registry.execute("test_action", {"param1": "hello"})
    assert result == "Result: hello"


def test_execute_unknown_action():
    """Test executing an unknown action raises error."""
    registry = ActionRegistry()
    
    with pytest.raises(ValueError, match="Unknown action"):
        registry.execute("unknown_action", {})


def test_validate_required_params():
    """Test parameter validation for required params."""
    registry = ActionRegistry()
    
    def test_handler(param1: str):
        return "ok"
    
    registry.register(
        name="test_action",
        category=ActionCategory.KEYBOARD,
        description="Test action",
        handler=test_handler,
        required_params=["param1"]
    )
    
    # Missing required parameter
    with pytest.raises(ValueError, match="Missing required parameter"):
        registry.execute("test_action", {})


def test_optional_params():
    """Test optional parameters with defaults."""
    registry = ActionRegistry()
    
    def test_handler(param1: str, param2: int = 10):
        return f"{param1}-{param2}"
    
    registry.register(
        name="test_action",
        category=ActionCategory.KEYBOARD,
        description="Test action",
        handler=test_handler,
        required_params=["param1"],
        optional_params={"param2": 10}
    )
    
    # Without optional param
    result1 = registry.execute("test_action", {"param1": "test"})
    assert result1 == "test-10"
    
    # With optional param
    result2 = registry.execute("test_action", {"param1": "test", "param2": 20})
    assert result2 == "test-20"


def test_list_actions():
    """Test listing actions."""
    registry = ActionRegistry()
    
    registry.register(
        name="action1",
        category=ActionCategory.KEYBOARD,
        description="Action 1",
        handler=lambda: None
    )
    
    registry.register(
        name="action2",
        category=ActionCategory.MOUSE,
        description="Action 2",
        handler=lambda: None
    )
    
    all_actions = registry.list_actions()
    assert "action1" in all_actions
    assert "action2" in all_actions
    
    keyboard_actions = registry.list_actions(ActionCategory.KEYBOARD)
    assert "action1" in keyboard_actions
    assert "action2" not in keyboard_actions


def test_action_handlers_registration():
    """Test that ActionHandlers registers all handlers."""
    registry = ActionRegistry()
    handlers = ActionHandlers(registry)
    handlers.register_all()
    
    # Check that handlers are registered
    all_actions = registry.list_actions()
    
    # Should have keyboard actions
    assert "press_key" in all_actions
    assert "shortcut" in all_actions
    assert "type" in all_actions
    
    # Should have mouse actions
    assert "mouse_move" in all_actions
    assert "mouse_click" in all_actions
    
    # Should have browser actions
    assert "browser_new_tab" in all_actions
    assert "browser_address_bar" in all_actions
    
    # Should have clipboard actions
    assert "copy" in all_actions
    assert "paste" in all_actions
    
    # Should have timing actions
    assert "delay" in all_actions
    
    # Should have macro action
    assert "macro" in all_actions


def test_get_action_library_for_ai():
    """Test generating action library for AI."""
    registry = ActionRegistry()
    handlers = ActionHandlers(registry)
    handlers.register_keyboard_handlers()
    
    library = registry.get_action_library_for_ai()
    
    assert "press_key" in library
    assert library["press_key"]["category"] == "keyboard"
    assert "description" in library["press_key"]
    assert "params" in library["press_key"]


def test_generate_documentation():
    """Test documentation generation."""
    registry = ActionRegistry()
    
    registry.register(
        name="test_action",
        category=ActionCategory.KEYBOARD,
        description="Test action for docs",
        handler=lambda x: x,
        required_params=["param1"],
        optional_params={"param2": "default"}
    )
    
    docs = registry.generate_documentation()
    
    assert "test_action" in docs
    assert "Test action for docs" in docs
    assert "param1" in docs
    assert "param2" in docs


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
