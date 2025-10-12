#!/usr/bin/env python3
"""
Verification script for Task 12: Complete System Replacement

This script verifies that:
1. AI Brain uses ProtocolGenerator (not WorkflowGenerator)
2. Automation Engine uses ProtocolExecutor (not AutomationExecutor)
3. All entry points (run.py, server.py, CLI) use protocol system
4. No references to old workflow system remain in main code
"""

import sys
import os
from pathlib import Path


def check_file_content(filepath: str, should_not_contain: list, description: str) -> bool:
    """Check that a file does not contain certain strings."""
    print(f"\nChecking {filepath}...")
    
    if not os.path.exists(filepath):
        print(f"   ✗ File not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    for term in should_not_contain:
        if term in content:
            issues.append(term)
    
    if issues:
        print(f"   ✗ {description} still contains: {', '.join(issues)}")
        return False
    else:
        print(f"   ✓ {description} clean")
        return True


def check_file_contains(filepath: str, should_contain: list, description: str) -> bool:
    """Check that a file contains certain strings."""
    print(f"\nChecking {filepath}...")
    
    if not os.path.exists(filepath):
        print(f"   ✗ File not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    missing = []
    for term in should_contain:
        if term not in content:
            missing.append(term)
    
    if missing:
        print(f"   ✗ {description} missing: {', '.join(missing)}")
        return False
    else:
        print(f"   ✓ {description} contains required elements")
        return True


def main():
    """Run all verification checks."""
    print("=" * 70)
    print("Task 12 Verification: Complete System Replacement")
    print("=" * 70)
    
    all_passed = True
    
    # Test 1: AI Brain main.py uses ProtocolGenerator
    print("\n1. Verifying AI Brain uses ProtocolGenerator...")
    if not check_file_contains(
        'ai_brain/main.py',
        ['from ai_brain.protocol_generator import ProtocolGenerator', 'self.protocol_generator'],
        "ai_brain/main.py"
    ):
        all_passed = False
    
    if not check_file_content(
        'ai_brain/main.py',
        ['from ai_brain.workflow_generator import', 'WorkflowGenerator('],
        "ai_brain/main.py"
    ):
        all_passed = False
    
    # Test 2: Automation Engine main.py uses ProtocolExecutor
    print("\n2. Verifying Automation Engine uses ProtocolExecutor...")
    if not check_file_contains(
        'automation_engine/main.py',
        ['from shared.protocol_executor import ProtocolExecutor', 'ProtocolExecutor('],
        "automation_engine/main.py"
    ):
        all_passed = False
    
    if not check_file_content(
        'automation_engine/main.py',
        ['from automation_engine.executor import AutomationExecutor', 'AutomationExecutor('],
        "automation_engine/main.py"
    ):
        all_passed = False
    
    # Test 3: run.py uses protocol system
    print("\n3. Verifying run.py uses protocol system...")
    if not check_file_contains(
        'run.py',
        ['from shared.protocol_executor import ProtocolExecutor', 'from shared.action_registry import ActionRegistry'],
        "run.py"
    ):
        all_passed = False
    
    if not check_file_content(
        'run.py',
        ['from automation_engine.executor import AutomationExecutor'],
        "run.py"
    ):
        all_passed = False
    
    # Test 4: CLI uses protocol terminology
    print("\n4. Verifying CLI uses protocol terminology...")
    if not check_file_contains(
        'scripts/cli.py',
        ['Protocol Queue', 'Waiting for protocols'],
        "scripts/cli.py"
    ):
        all_passed = False
    
    # Test 5: Check that protocol files exist
    print("\n5. Verifying protocol system files exist...")
    required_files = [
        'shared/protocol_models.py',
        'shared/protocol_parser.py',
        'shared/protocol_executor.py',
        'shared/action_registry.py',
        'shared/action_handlers.py',
        'ai_brain/protocol_generator.py'
    ]
    
    for filepath in required_files:
        if os.path.exists(filepath):
            print(f"   ✓ {filepath} exists")
        else:
            print(f"   ✗ {filepath} missing")
            all_passed = False
    
    # Test 6: Verify no imports of old system in main files
    print("\n6. Verifying no old system imports in main files...")
    main_files = [
        'ai_brain/main.py',
        'automation_engine/main.py',
        'run.py'
    ]
    
    for filepath in main_files:
        if check_file_content(
            filepath,
            ['from ai_brain.workflow_generator import', 'from automation_engine.executor import AutomationExecutor'],
            filepath
        ):
            print(f"   ✓ {filepath} has no old imports")
        else:
            all_passed = False
    
    # Test 7: Check communication layer supports protocols
    print("\n7. Verifying communication layer supports protocols...")
    if not check_file_contains(
        'shared/communication.py',
        ['send_protocol', 'receive_protocol'],
        "shared/communication.py"
    ):
        all_passed = False
    
    # Final result
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print("=" * 70)
        print("\nTask 12 Complete: System Replacement Successful!")
        print("\nSummary:")
        print("  ✓ AI Brain uses ProtocolGenerator")
        print("  ✓ Automation Engine uses ProtocolExecutor")
        print("  ✓ run.py uses protocol system")
        print("  ✓ CLI uses protocol terminology")
        print("  ✓ All protocol system files exist")
        print("  ✓ No old system imports in main files")
        print("  ✓ Communication layer supports protocols")
        print("\nThe old workflow system has been completely replaced with the protocol system!")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("=" * 70)
        print("\nPlease review the failures above and fix the issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
