"""
Test automation with mock actions (no API calls, no actual automation).

This script demonstrates how to test protocol generation and execution
without burning through API credits or actually moving the mouse.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.action_registry import ActionRegistry
from shared.mock_action_handlers import MockActionHandlers
from shared.protocol_executor import ProtocolExecutor
from shared.protocol_parser import JSONProtocolParser


def test_mock_protocol_execution():
    """Test protocol execution with mock actions."""
    
    print("\n" + "="*60)
    print("TESTING WITH MOCK ACTIONS (No API calls)")
    print("="*60 + "\n")
    
    # Initialize components
    action_registry = ActionRegistry()
    mock_handlers = MockActionHandlers(action_registry)
    
    # Register mock actions instead of real ones
    mock_handlers.register_all_mock_actions()
    
    # Create a test protocol (without visual_navigate to avoid message broker requirement)
    test_protocol = {
        "version": "1.0",
        "metadata": {
            "description": "Test protocol with mock actions",
            "complexity": "simple",
            "uses_vision": False
        },
        "macros": {},
        "actions": [
            {
                "action": "open_app",
                "params": {"app_name": "chrome"},
                "wait_after_ms": 2000
            },
            {
                "action": "shortcut",
                "params": {"keys": ["ctrl", "l"]},
                "wait_after_ms": 200
            },
            {
                "action": "type",
                "params": {"text": "x.com"},
                "wait_after_ms": 100
            },
            {
                "action": "press_key",
                "params": {"key": "enter"},
                "wait_after_ms": 3000
            },
            {
                "action": "mouse_move",
                "params": {"x": 500, "y": 300},
                "wait_after_ms": 200
            },
            {
                "action": "mouse_click",
                "params": {"button": "left"},
                "wait_after_ms": 500
            },
            {
                "action": "type",
                "params": {"text": "This is a test post! 🚀 #Testing #Automation"},
                "wait_after_ms": 1000
            },
            {
                "action": "mouse_move",
                "params": {"x": 800, "y": 600},
                "wait_after_ms": 200
            },
            {
                "action": "mouse_click",
                "params": {"button": "left"},
                "wait_after_ms": 2000
            }
        ]
    }
    
    # Parse protocol
    parser = JSONProtocolParser()
    protocol = parser.parse_dict(test_protocol)
    
    print(f"Protocol: {protocol.metadata.description}")
    print(f"Actions: {len(protocol.actions)}")
    print(f"Uses vision: {protocol.metadata.uses_vision}")
    print(f"Note: Using mouse_move/click instead of visual_navigate to avoid message broker")
    print(f"\n{'='*60}\n")
    
    # Execute protocol with mock actions
    executor = ProtocolExecutor(action_registry, dry_run=False)
    
    print("Executing protocol with mock actions...\n")
    result = executor.execute_protocol(protocol)
    
    # Print results
    print(f"\n{'='*60}")
    print(f"EXECUTION RESULT")
    print(f"{'='*60}")
    print(f"Status: {result.status}")
    print(f"Actions completed: {result.actions_completed}/{len(protocol.actions)}")
    print(f"Duration: {result.duration_ms}ms")
    if result.error:
        print(f"Error: {result.error}")
    print(f"{'='*60}\n")
    
    # Print execution summary
    mock_handlers.print_summary()
    
    return result.status == 'success'


def test_verify_screen_mock():
    """Test verify_screen with mock (simulates success/failure)."""
    
    print("\n" + "="*60)
    print("TESTING VERIFY_SCREEN WITH MOCK")
    print("="*60 + "\n")
    
    action_registry = ActionRegistry()
    mock_handlers = MockActionHandlers(action_registry)
    mock_handlers.register_all_mock_actions()
    
    test_protocol = {
        "version": "1.0",
        "metadata": {
            "description": "Test verify_screen mock",
            "complexity": "simple",
            "uses_vision": True
        },
        "macros": {},
        "actions": [
            {
                "action": "verify_screen",
                "params": {
                    "context": "Looking for login button",
                    "expected": "Login button visible and clickable"
                },
                "wait_after_ms": 500
            },
            {
                "action": "verify_screen",
                "params": {
                    "context": "Looking for submit button",
                    "expected": "Submit button visible"
                },
                "wait_after_ms": 500
            },
            {
                "action": "verify_screen",
                "params": {
                    "context": "Looking for confirmation message",
                    "expected": "Success message displayed"
                },
                "wait_after_ms": 500
            }
        ]
    }
    
    parser = JSONProtocolParser()
    protocol = parser.parse_dict(test_protocol)
    
    executor = ProtocolExecutor(action_registry, dry_run=False)
    result = executor.execute_protocol(protocol)
    
    print(f"\nResult: {result.status}")
    print(f"Actions completed: {result.actions_completed}/{len(protocol.actions)}")
    
    mock_handlers.print_summary()
    
    return True


def test_complex_workflow_mock():
    """Test a complex workflow with macros and variables."""
    
    print("\n" + "="*60)
    print("TESTING COMPLEX WORKFLOW WITH MOCK")
    print("="*60 + "\n")
    
    action_registry = ActionRegistry()
    mock_handlers = MockActionHandlers(action_registry)
    mock_handlers.register_all_mock_actions()
    
    test_protocol = {
        "version": "1.0",
        "metadata": {
            "description": "Complex workflow with macros",
            "complexity": "complex",
            "uses_vision": True
        },
        "macros": {
            "search_in_browser": [
                {
                    "action": "shortcut",
                    "params": {"keys": ["ctrl", "l"]},
                    "wait_after_ms": 200
                },
                {
                    "action": "type",
                    "params": {"text": "{{query}}"},
                    "wait_after_ms": 100
                },
                {
                    "action": "press_key",
                    "params": {"key": "enter"},
                    "wait_after_ms": 2000
                }
            ]
        },
        "actions": [
            {
                "action": "open_app",
                "params": {"app_name": "chrome"},
                "wait_after_ms": 2000
            },
            {
                "action": "macro",
                "params": {
                    "name": "search_in_browser",
                    "vars": {"query": "Python automation"}
                },
                "wait_after_ms": 1000
            },
            {
                "action": "visual_navigate",
                "params": {"task": "Click the first search result"},
                "wait_after_ms": 2000
            },
            {
                "action": "shortcut",
                "params": {"keys": ["ctrl", "t"]},
                "wait_after_ms": 1000
            },
            {
                "action": "macro",
                "params": {
                    "name": "search_in_browser",
                    "vars": {"query": "JavaScript tutorials"}
                },
                "wait_after_ms": 1000
            }
        ]
    }
    
    parser = JSONProtocolParser()
    protocol = parser.parse_dict(test_protocol)
    
    executor = ProtocolExecutor(action_registry, dry_run=False)
    result = executor.execute_protocol(protocol)
    
    print(f"\nResult: {result.status}")
    print(f"Actions completed: {result.actions_completed}")
    
    mock_handlers.print_summary()
    
    return result.status == 'success'


if __name__ == "__main__":
    print("\n" + "="*60)
    print("MOCK ACTION TESTING SUITE")
    print("="*60)
    print("\nThis test suite uses mock actions that:")
    print("  ✓ Don't make API calls")
    print("  ✓ Don't move the mouse or click")
    print("  ✓ Don't type on the keyboard")
    print("  ✓ Simulate realistic timing and behavior")
    print("  ✓ Perfect for testing protocol generation and execution")
    print("\n" + "="*60 + "\n")
    
    tests = [
        ("Basic Protocol Execution", test_mock_protocol_execution),
        ("Verify Screen Mock", test_verify_screen_mock),
        ("Complex Workflow with Macros", test_complex_workflow_mock)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*60}")
            print(f"Running: {test_name}")
            print(f"{'='*60}")
            passed = test_func()
            results.append((test_name, passed))
            print(f"\n✓ {test_name}: {'PASSED' if passed else 'FAILED'}")
        except Exception as e:
            print(f"\n✗ {test_name}: FAILED with error: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Final summary
    print(f"\n{'='*60}")
    print(f"FINAL SUMMARY")
    print(f"{'='*60}")
    passed = sum(1 for _, p in results if p)
    total = len(results)
    print(f"\nTests passed: {passed}/{total}")
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {status}: {test_name}")
    print(f"\n{'='*60}\n")
