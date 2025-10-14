"""
Test the automation engine directly with a protocol file.
No AI Brain needed, no API calls!
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from shared.action_registry import ActionRegistry
from shared.mock_action_handlers import MockActionHandlers
from shared.protocol_executor import ProtocolExecutor
from shared.protocol_parser import JSONProtocolParser


def test_automation_engine():
    """Test automation engine with a pre-made protocol."""
    
    print("\n" + "="*60)
    print("TESTING AUTOMATION ENGINE (No API calls)")
    print("="*60)
    print("\nThis tests the automation engine directly using:")
    print("  ✓ Pre-made protocol (no AI generation)")
    print("  ✓ Mock actions (no actual automation)")
    print("  ✓ Zero API calls")
    print("\n" + "="*60 + "\n")
    
    # Initialize with mock actions
    action_registry = ActionRegistry()
    mock_handlers = MockActionHandlers(action_registry)
    mock_handlers.register_all_mock_actions()
    
    # Load a pre-made protocol
    parser = JSONProtocolParser()
    
    print("Loading protocol from: examples/protocols/simple_test.json")
    import json
    with open('examples/protocols/simple_test.json', 'r') as f:
        protocol_dict = json.load(f)
    protocol = parser.parse_dict(protocol_dict)
    
    print(f"\nProtocol loaded:")
    print(f"  Description: {protocol.metadata.description}")
    print(f"  Actions: {len(protocol.actions)}")
    print(f"  Macros: {len(protocol.macros)}")
    print(f"  Complexity: {protocol.metadata.complexity}")
    print(f"\n" + "="*60 + "\n")
    
    # Execute the protocol
    executor = ProtocolExecutor(action_registry, dry_run=False)
    
    print("Executing protocol...\n")
    result = executor.execute_protocol(protocol)
    
    # Print results
    print(f"\n" + "="*60)
    print("EXECUTION RESULT")
    print("="*60)
    print(f"Status: {result.status}")
    print(f"Actions completed: {result.actions_completed}/{len(protocol.actions)}")
    print(f"Duration: {result.duration_ms}ms ({result.duration_ms/1000:.2f}s)")
    if result.error:
        print(f"Error: {result.error}")
    print("="*60 + "\n")
    
    # Print execution summary
    mock_handlers.print_summary()
    
    # Print detailed log
    print("\n" + "="*60)
    print("DETAILED EXECUTION LOG")
    print("="*60)
    log = mock_handlers.get_execution_log()
    for i, entry in enumerate(log, 1):
        print(f"\n[{i}] {entry['action']}")
        print(f"    Params: {entry['params']}")
        if entry['result']:
            print(f"    Result: {entry['result']}")
    print("\n" + "="*60 + "\n")
    
    return result.status == 'success'


if __name__ == "__main__":
    print("\n" + "="*60)
    print("AUTOMATION ENGINE DIRECT TEST")
    print("="*60)
    print("\nThis script tests the automation engine without:")
    print("  ❌ AI Brain")
    print("  ❌ Protocol generation")
    print("  ❌ API calls")
    print("  ❌ Actual mouse/keyboard automation")
    print("\nIt uses:")
    print("  ✅ Pre-made protocol file")
    print("  ✅ Mock actions (simulated)")
    print("  ✅ Real protocol executor")
    print("  ✅ Real action registry")
    print("\n" + "="*60)
    
    try:
        success = test_automation_engine()
        
        if success:
            print("\n✅ SUCCESS! Automation engine is working correctly!")
            print("\nThe engine successfully:")
            print("  ✓ Loaded the protocol")
            print("  ✓ Parsed all actions")
            print("  ✓ Executed macros with variable substitution")
            print("  ✓ Completed all actions")
            print("  ✓ Provided detailed logging")
        else:
            print("\n❌ FAILED! Check the error messages above.")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("Test complete!")
    print("="*60 + "\n")
