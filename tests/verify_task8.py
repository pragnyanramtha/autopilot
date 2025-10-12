"""
Verification script for Task 8: Replace workflow generator with protocol generator
"""
import sys
from unittest.mock import Mock

print("=" * 60)
print("Task 8 Verification: Protocol Generator")
print("=" * 60)

# Test 1: Import ProtocolGenerator
print("\n1. Testing ProtocolGenerator import...")
try:
    from ai_brain.protocol_generator import ProtocolGenerator
    print("   ✓ ProtocolGenerator imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import ProtocolGenerator: {e}")
    sys.exit(1)

# Test 2: Initialize ProtocolGenerator
print("\n2. Testing ProtocolGenerator initialization...")
try:
    generator = ProtocolGenerator()
    assert generator.gemini_client is None
    assert generator.config == {}
    print("   ✓ ProtocolGenerator initialized successfully")
except Exception as e:
    print(f"   ✗ Failed to initialize: {e}")
    sys.exit(1)

# Test 3: Test with config
print("\n3. Testing ProtocolGenerator with config...")
try:
    config = {'test': 'value'}
    generator = ProtocolGenerator(config=config)
    assert generator.config == config
    print("   ✓ Config passed correctly")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    sys.exit(1)

# Test 4: Test create_protocol requires GeminiClient
print("\n4. Testing create_protocol requires GeminiClient...")
try:
    from ai_brain.gemini_client import CommandIntent
    generator = ProtocolGenerator()
    intent = CommandIntent(action='test', target='test', parameters={}, confidence=1.0)
    
    try:
        generator.create_protocol(intent)
        print("   ✗ Should have raised ValueError")
        sys.exit(1)
    except ValueError as e:
        if "GeminiClient is required" in str(e):
            print("   ✓ Correctly raises ValueError when GeminiClient is missing")
        else:
            print(f"   ✗ Wrong error message: {e}")
            sys.exit(1)
except Exception as e:
    print(f"   ✗ Unexpected error: {e}")
    sys.exit(1)

# Test 5: Test create_protocol with mocked GeminiClient
print("\n5. Testing create_protocol with mocked GeminiClient...")
try:
    mock_client = Mock()
    mock_protocol = {
        'version': '1.0',
        'metadata': {'id': 'test-123'},
        'actions': [
            {'action': 'open_app', 'params': {'app_name': 'chrome'}, 'wait_after_ms': 2000}
        ]
    }
    mock_client.generate_protocol.return_value = mock_protocol
    
    generator = ProtocolGenerator(gemini_client=mock_client)
    intent = CommandIntent(action='open_app', target='chrome', parameters={}, confidence=1.0)
    
    protocol = generator.create_protocol(intent, 'open chrome')
    
    assert protocol == mock_protocol
    assert mock_client.generate_protocol.called
    print("   ✓ create_protocol works with GeminiClient")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    sys.exit(1)

# Test 6: Test validate_protocol
print("\n6. Testing validate_protocol...")
try:
    mock_client = Mock()
    generator = ProtocolGenerator(gemini_client=mock_client)
    
    valid_protocol = {
        'version': '1.0',
        'metadata': {'id': 'test-123'},
        'actions': [
            {'action': 'press_key', 'params': {'key': 'enter'}, 'wait_after_ms': 100}
        ]
    }
    
    result = generator.validate_protocol(valid_protocol)
    
    assert 'valid' in result
    assert 'issues' in result
    assert 'warnings' in result
    print("   ✓ validate_protocol returns correct structure")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    sys.exit(1)

# Test 7: Check ai_brain/main.py uses ProtocolGenerator
print("\n7. Checking ai_brain/main.py uses ProtocolGenerator...")
try:
    with open('ai_brain/main.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'from ai_brain.protocol_generator import ProtocolGenerator' in content:
            print("   ✓ main.py imports ProtocolGenerator")
        else:
            print("   ✗ main.py does not import ProtocolGenerator")
            sys.exit(1)
        
        if 'self.protocol_generator' in content:
            print("   ✓ main.py uses protocol_generator")
        else:
            print("   ✗ main.py does not use protocol_generator")
            sys.exit(1)
        
        if 'WorkflowGenerator' in content:
            print("   ✗ main.py still references WorkflowGenerator")
            sys.exit(1)
        else:
            print("   ✓ main.py no longer references WorkflowGenerator")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    sys.exit(1)

# Test 8: Check run.py uses ProtocolGenerator
print("\n8. Checking run.py uses ProtocolGenerator...")
try:
    with open('run.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'from ai_brain.protocol_generator import ProtocolGenerator' in content:
            print("   ✓ run.py imports ProtocolGenerator")
        else:
            print("   ✗ run.py does not import ProtocolGenerator")
            sys.exit(1)
        
        if 'self.protocol_generator' in content:
            print("   ✓ run.py uses protocol_generator")
        else:
            print("   ✗ run.py does not use protocol_generator")
            sys.exit(1)
        
        if 'WorkflowGenerator' in content:
            print("   ✗ run.py still references WorkflowGenerator")
            sys.exit(1)
        else:
            print("   ✓ run.py no longer references WorkflowGenerator")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    sys.exit(1)

# Test 9: Check MessageBroker has protocol support
print("\n9. Checking MessageBroker has protocol support...")
try:
    with open('shared/communication.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'def send_protocol' in content:
            print("   ✓ MessageBroker has send_protocol method")
        else:
            print("   ✗ MessageBroker missing send_protocol method")
            sys.exit(1)
        
        if 'def receive_protocol' in content:
            print("   ✓ MessageBroker has receive_protocol method")
        else:
            print("   ✗ MessageBroker missing receive_protocol method")
            sys.exit(1)
        
        if 'self.protocol_dir' in content:
            print("   ✓ MessageBroker has protocol_dir")
        else:
            print("   ✗ MessageBroker missing protocol_dir")
            sys.exit(1)
except Exception as e:
    print(f"   ✗ Failed: {e}")
    sys.exit(1)

# Test 10: Check workflow_generator.py still exists (for backward compatibility)
print("\n10. Checking backward compatibility...")
try:
    import os
    if os.path.exists('ai_brain/workflow_generator.py'):
        print("   ✓ workflow_generator.py still exists (backward compatibility)")
    else:
        print("   ℹ workflow_generator.py removed (full replacement)")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ All Task 8 verification tests passed!")
print("=" * 60)
print("\nSummary:")
print("  • ProtocolGenerator class created")
print("  • ai_brain/main.py updated to use ProtocolGenerator")
print("  • run.py updated to use ProtocolGenerator")
print("  • MessageBroker extended with protocol support")
print("  • All command processing now uses protocol format")
print("=" * 60)
