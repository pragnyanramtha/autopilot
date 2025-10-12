"""
Action Registry Demo

This example demonstrates how to use the ActionRegistry and ActionHandlers
to execute automation actions.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.action_registry import ActionRegistry, ActionCategory
from shared.action_handlers import ActionHandlers


def main():
    """Demonstrate action registry usage."""
    
    # Initialize registry and register all handlers
    print("Initializing Action Registry...")
    registry = ActionRegistry()
    handlers = ActionHandlers(registry)
    handlers.register_all()
    
    print(f"\n✓ Successfully registered {len(registry.list_actions())} actions\n")
    
    # List actions by category
    print("=" * 60)
    print("ACTIONS BY CATEGORY")
    print("=" * 60)
    
    for category in ActionCategory:
        actions = registry.list_actions(category)
        if actions:
            print(f"\n{category.value.upper()} ({len(actions)} actions):")
            for action in actions[:5]:  # Show first 5
                handler = registry.get_handler(action)
                print(f"  • {action}: {handler.description}")
            if len(actions) > 5:
                print(f"  ... and {len(actions) - 5} more")
    
    # Show detailed info for a specific action
    print("\n" + "=" * 60)
    print("DETAILED ACTION INFO: press_key")
    print("=" * 60)
    
    handler = registry.get_handler("press_key")
    print(f"Name: {handler.name}")
    print(f"Category: {handler.category.value}")
    print(f"Description: {handler.description}")
    print(f"Required params: {handler.required_params}")
    print(f"Optional params: {handler.optional_params}")
    print(f"Signature: {handler.get_signature()}")
    
    if handler.examples:
        print("\nExamples:")
        for example in handler.examples:
            print(f"  {example}")
    
    # Show action library for AI
    print("\n" + "=" * 60)
    print("ACTION LIBRARY FOR AI (Sample)")
    print("=" * 60)
    
    library = registry.get_action_library_for_ai()
    
    # Show a few actions
    sample_actions = ["press_key", "mouse_move", "delay", "verify_screen"]
    for action_name in sample_actions:
        if action_name in library:
            action_info = library[action_name]
            print(f"\n{action_name}:")
            print(f"  Category: {action_info['category']}")
            print(f"  Description: {action_info['description']}")
            print(f"  Required: {action_info['params']['required']}")
            print(f"  Optional: {action_info['params']['optional']}")
    
    # Demonstrate parameter validation
    print("\n" + "=" * 60)
    print("PARAMETER VALIDATION")
    print("=" * 60)
    
    # Valid parameters
    print("\n✓ Valid parameters for 'delay':")
    try:
        handler = registry.get_handler("delay")
        is_valid, error = handler.validate_params({"ms": 1000})
        print(f"  Result: {is_valid}, Error: {error}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Missing required parameter
    print("\n✗ Missing required parameter for 'press_key':")
    try:
        handler = registry.get_handler("press_key")
        is_valid, error = handler.validate_params({})
        print(f"  Result: {is_valid}, Error: {error}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Unknown parameter
    print("\n✗ Unknown parameter for 'delay':")
    try:
        handler = registry.get_handler("delay")
        is_valid, error = handler.validate_params({"ms": 1000, "unknown": "value"})
        print(f"  Result: {is_valid}, Error: {error}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Generate documentation
    print("\n" + "=" * 60)
    print("DOCUMENTATION GENERATION")
    print("=" * 60)
    
    # Generate docs for keyboard category
    docs = registry.generate_documentation(ActionCategory.KEYBOARD)
    print("\nKeyboard Actions Documentation (first 500 chars):")
    print(docs[:500] + "...")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print("\nThe ActionRegistry is ready to be used by the protocol executor!")
    print("Total actions available: " + str(len(registry.list_actions())))


if __name__ == "__main__":
    main()
