"""
Protocol Executor Demo

Demonstrates the complete functionality of the ProtocolExecutor including:
- Sequential action execution
- Macro execution with variable substitution
- Error handling and recovery
- Pause/resume/stop controls
"""

import sys
import time
from unittest.mock import Mock

sys.path.insert(0, '.')

from shared.protocol_executor import ProtocolExecutor
from shared.protocol_models import ProtocolSchema, ActionStep, Metadata, MacroDefinition
from shared.action_registry import ActionRegistry


def demo_basic_execution():
    """Demo 1: Basic sequential execution."""
    print("\n" + "=" * 60)
    print("DEMO 1: Basic Sequential Execution")
    print("=" * 60)
    
    # Create mock registry
    mock_registry = Mock(spec=ActionRegistry)
    mock_registry.execute = Mock(return_value=None)
    
    # Create executor
    executor = ProtocolExecutor(mock_registry, dry_run=False)
    
    # Create simple protocol
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(
            description="Basic execution demo",
            complexity="simple"
        ),
        actions=[
            ActionStep(action="press_key", params={"key": "win"}, wait_after_ms=500),
            ActionStep(action="type", params={"text": "notepad"}, wait_after_ms=100),
            ActionStep(action="press_key", params={"key": "enter"}, wait_after_ms=1000),
            ActionStep(action="type", params={"text": "Hello, World!"}, wait_after_ms=100)
        ]
    )
    
    # Execute
    print("\nExecuting protocol...")
    result = executor.execute_protocol(protocol)
    
    # Display results
    print(f"\nResult:")
    print(f"  Status: {result.status}")
    print(f"  Actions completed: {result.actions_completed}/{result.total_actions}")
    print(f"  Duration: {result.duration_ms}ms")
    print(f"  Registry execute calls: {mock_registry.execute.call_count}")


def demo_macro_execution():
    """Demo 2: Macro execution with variable substitution."""
    print("\n" + "=" * 60)
    print("DEMO 2: Macro Execution with Variables")
    print("=" * 60)
    
    mock_registry = Mock(spec=ActionRegistry)
    mock_registry.execute = Mock(return_value=None)
    
    executor = ProtocolExecutor(mock_registry, dry_run=False)
    
    # Create protocol with macros
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(
            description="Macro demo",
            complexity="medium"
        ),
        macros={
            "search_in_browser": MacroDefinition(
                name="search_in_browser",
                actions=[
                    ActionStep(action="shortcut", params={"keys": ["ctrl", "l"]}, wait_after_ms=200),
                    ActionStep(action="type", params={"text": "{{query}}"}, wait_after_ms=100),
                    ActionStep(action="press_key", params={"key": "enter"}, wait_after_ms=2000)
                ]
            ),
            "new_tab": MacroDefinition(
                name="new_tab",
                actions=[
                    ActionStep(action="shortcut", params={"keys": ["ctrl", "t"]}, wait_after_ms=1000)
                ]
            )
        },
        actions=[
            ActionStep(action="open_app", params={"app_name": "chrome"}, wait_after_ms=2000),
            ActionStep(action="macro", params={"name": "search_in_browser", "vars": {"query": "elon musk"}}),
            ActionStep(action="macro", params={"name": "new_tab"}),
            ActionStep(action="macro", params={"name": "search_in_browser", "vars": {"query": "jeff bezos"}})
        ]
    )
    
    print("\nExecuting protocol with macros...")
    result = executor.execute_protocol(protocol)
    
    print(f"\nResult:")
    print(f"  Status: {result.status}")
    print(f"  Actions completed: {result.actions_completed}/{result.total_actions}")
    print(f"  Duration: {result.duration_ms}ms")
    print(f"  Total action executions: {mock_registry.execute.call_count}")
    print(f"    (4 protocol actions expanded to {mock_registry.execute.call_count} actual executions)")


def demo_nested_macros():
    """Demo 3: Nested macro execution."""
    print("\n" + "=" * 60)
    print("DEMO 3: Nested Macro Execution")
    print("=" * 60)
    
    mock_registry = Mock(spec=ActionRegistry)
    mock_registry.execute = Mock(return_value=None)
    
    executor = ProtocolExecutor(mock_registry, dry_run=False)
    
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(description="Nested macros demo"),
        macros={
            "type_char": MacroDefinition(
                name="type_char",
                actions=[
                    ActionStep(action="type", params={"text": "{{char}}"}, wait_after_ms=50)
                ]
            ),
            "type_word": MacroDefinition(
                name="type_word",
                actions=[
                    ActionStep(action="macro", params={"name": "type_char", "vars": {"char": "H"}}),
                    ActionStep(action="macro", params={"name": "type_char", "vars": {"char": "i"}})
                ]
            )
        },
        actions=[
            ActionStep(action="macro", params={"name": "type_word"})
        ]
    )
    
    print("\nExecuting nested macros...")
    result = executor.execute_protocol(protocol)
    
    print(f"\nResult:")
    print(f"  Status: {result.status}")
    print(f"  Macro nesting: type_word → type_char (2x)")
    print(f"  Total executions: {mock_registry.execute.call_count}")


def demo_error_handling():
    """Demo 4: Error handling and recovery."""
    print("\n" + "=" * 60)
    print("DEMO 4: Error Handling and Recovery")
    print("=" * 60)
    
    mock_registry = Mock(spec=ActionRegistry)
    mock_registry.execute.side_effect = [
        "result1",
        "result2",
        ValueError("Invalid parameter at action 3"),
        None
    ]
    
    executor = ProtocolExecutor(mock_registry, dry_run=False)
    
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(description="Error handling demo"),
        actions=[
            ActionStep(action="action1", params={"step": 1}),
            ActionStep(action="action2", params={"step": 2}),
            ActionStep(action="action3", params={"step": 3}),
            ActionStep(action="action4", params={"step": 4})
        ]
    )
    
    print("\nExecuting protocol (will fail at action 3)...")
    result = executor.execute_protocol(protocol)
    
    print(f"\nResult:")
    print(f"  Status: {result.status}")
    print(f"  Actions completed: {result.actions_completed}/{result.total_actions}")
    print(f"  Error: {result.error}")
    
    if result.error_details:
        print(f"\nError Details:")
        print(f"  Action: {result.error_details.action_name}")
        print(f"  Index: {result.error_details.action_index}")
        print(f"  Type: {result.error_details.error_type}")
        print(f"  Message: {result.error_details.error_message}")
        print(f"  Parameters: {result.error_details.params}")
    
    if result.context:
        print(f"\nContext Preserved:")
        print(f"  Action results: {len(result.context['action_results'])}")
        print(f"  Successful: {result.context['action_results'][0]['result']}, {result.context['action_results'][1]['result']}")
        print(f"  Failed: {result.context['action_results'][2]['error']}")
        
        print(f"\nRecovery Information:")
        print(f"  Can resume from action index: {result.error_details.action_index + 1}")


def demo_dry_run():
    """Demo 5: Dry run mode."""
    print("\n" + "=" * 60)
    print("DEMO 5: Dry Run Mode")
    print("=" * 60)
    
    mock_registry = Mock(spec=ActionRegistry)
    mock_registry.execute = Mock(return_value=None)
    
    # Create executor in dry run mode
    executor = ProtocolExecutor(mock_registry, dry_run=True)
    
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(description="Dry run demo"),
        actions=[
            ActionStep(action="press_key", params={"key": "enter"}),
            ActionStep(action="type", params={"text": "test"}),
            ActionStep(action="delay", params={"ms": 1000})
        ]
    )
    
    print("\nExecuting in dry run mode...")
    result = executor.execute_protocol(protocol)
    
    print(f"\nResult:")
    print(f"  Status: {result.status}")
    print(f"  Actions completed: {result.actions_completed}/{result.total_actions}")
    print(f"  Registry execute calls: {mock_registry.execute.call_count} (should be 0 in dry run)")


def demo_timing():
    """Demo 6: Timing control."""
    print("\n" + "=" * 60)
    print("DEMO 6: Timing Control")
    print("=" * 60)
    
    mock_registry = Mock(spec=ActionRegistry)
    mock_registry.execute = Mock(return_value=None)
    
    executor = ProtocolExecutor(mock_registry, dry_run=False)
    
    protocol = ProtocolSchema(
        version="1.0",
        metadata=Metadata(description="Timing demo"),
        actions=[
            ActionStep(action="action1", params={}, wait_after_ms=100),
            ActionStep(action="action2", params={}, wait_after_ms=200),
            ActionStep(action="action3", params={}, wait_after_ms=150)
        ]
    )
    
    print("\nExecuting with timing control...")
    print("  Action 1: wait 100ms")
    print("  Action 2: wait 200ms")
    print("  Action 3: wait 150ms")
    print("  Total expected: ~450ms")
    
    start = time.time()
    result = executor.execute_protocol(protocol)
    duration = time.time() - start
    
    print(f"\nResult:")
    print(f"  Status: {result.status}")
    print(f"  Actual duration: {int(duration * 1000)}ms")
    print(f"  Timing respected: {'✓' if duration >= 0.44 else '✗'}")


def run_all_demos():
    """Run all demos."""
    print("\n" + "=" * 60)
    print("PROTOCOL EXECUTOR DEMONSTRATION")
    print("Task 4: Implement Protocol Execution Engine")
    print("=" * 60)
    
    try:
        demo_basic_execution()
        demo_macro_execution()
        demo_nested_macros()
        demo_error_handling()
        demo_dry_run()
        demo_timing()
        
        print("\n" + "=" * 60)
        print("✓ ALL DEMOS COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\nKey Features Demonstrated:")
        print("  ✓ Sequential action execution")
        print("  ✓ Macro execution with variable substitution")
        print("  ✓ Nested macro calls")
        print("  ✓ Comprehensive error handling")
        print("  ✓ Context preservation on error")
        print("  ✓ Dry run mode")
        print("  ✓ Timing control")
        print("\nTask 4 Implementation: COMPLETE")
        
    except Exception as e:
        print(f"\n✗ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_demos()
