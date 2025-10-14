"""
Test the automation engine with REAL actions.
⚠️ WARNING: This will actually move your mouse and type!
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from shared.action_registry import ActionRegistry
from shared.action_handlers import ActionHandlers
from shared.protocol_executor import ProtocolExecutor
from shared.protocol_parser import JSONProtocolParser


def test_automation_engine_real():
    """Test automation engine with REAL actions."""
    
    print("\n" + "="*60)
    print("⚠️  TESTING AUTOMATION ENGINE WITH REAL ACTIONS ⚠️")
    print("="*60)
    print("\n🚨 WARNING: This will actually:")
    print("  • Move your mouse")
    print("  • Click buttons")
    print("  • Type on your keyboard")
    print("  • Open applications")
    print("\n" + "="*60 + "\n")
    
    # Ask for confirmation
    response = input("Do you want to continue? (yes/no): ").strip().lower()
    if response != 'yes':
        print("\n❌ Cancelled. Use test_automation_engine_only.py for mock testing.")
        return False
    
    print("\n" + "="*60)
    print("Starting in 3 seconds...")
    print("Move your mouse to interrupt!")
    print("="*60 + "\n")
    
    import time
    time.sleep(3)
    
    # Initialize with REAL actions
    action_registry = ActionRegistry()
    real_handlers = ActionHandlers(action_registry)
    real_handlers.register_all()
    
    print("✓ Real action handlers registered")
    
    # Load a pre-made protocol
    parser = JSONProtocolParser()
    
    print("Loading protocol from: examples/protocols/comprehensive_test.json")
    import json
    with open('examples/protocols/comprehensive_test.json', 'r') as f:
        protocol_dict = json.load(f)
    protocol = parser.parse_dict(protocol_dict)
    
    print(f"\nProtocol loaded:")
    print(f"  Description: {protocol.metadata.description}")
    print(f"  Actions: {len(protocol.actions)}")
    print(f"  Macros: {len(protocol.macros)}")
    print(f"  Complexity: {protocol.metadata.complexity}")
    print(f"\n" + "="*60 + "\n")
    
    # Execute the protocol with REAL actions
    executor = ProtocolExecutor(action_registry, dry_run=False)
    
    print("🚀 Executing protocol with REAL actions...\n")
    print("⚠️  Your mouse will move and keyboard will type!\n")
    
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
    
    return result.status == 'success'


if __name__ == "__main__":
    print("\n" + "="*60)
    print("AUTOMATION ENGINE REAL TEST")
    print("="*60)
    print("\n⚠️  WARNING: This uses REAL automation!")
    print("\nThis script will:")
    print("  ✅ Use real action handlers")
    print("  ✅ Actually move your mouse")
    print("  ✅ Actually type on keyboard")
    print("  ✅ Actually open applications")
    print("\nIt does NOT:")
    print("  ❌ Use AI Brain")
    print("  ❌ Generate protocols with AI")
    print("  ❌ Make API calls")
    print("\n" + "="*60)
    
    try:
        success = test_automation_engine_real()
        
        if success:
            print("\n✅ SUCCESS! Automation engine executed real actions!")
            print("\nThe engine successfully:")
            print("  ✓ Loaded the protocol")
            print("  ✓ Executed all actions")
            print("  ✓ Moved mouse and typed text")
            print("  ✓ Completed the workflow")
        else:
            print("\n❌ Test was cancelled or failed.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("Test complete!")
    print("="*60 + "\n")
