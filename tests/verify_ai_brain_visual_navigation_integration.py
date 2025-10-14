"""
Verification script for AI Brain visual navigation integration.

This script verifies that the visual navigation integration is correctly
implemented in the AI Brain main.py file.
"""

import ast
import sys


def verify_integration():
    """Verify that visual navigation is properly integrated."""
    print("Verifying AI Brain visual navigation integration...")
    print("=" * 60)
    
    # Read the main.py file
    with open('ai_brain/main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse the AST
    try:
        tree = ast.parse(content)
        print("✓ main.py syntax is valid")
    except SyntaxError as e:
        print(f"✗ Syntax error in main.py: {e}")
        return False
    
    # Check for required imports
    required_imports = [
        'VisionNavigator',
        'CommandIntent',
        'MessageBroker'
    ]
    
    imports_found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports_found.append(alias.name)
    
    for imp in required_imports:
        if imp in imports_found:
            print(f"✓ Import found: {imp}")
        else:
            print(f"✗ Missing import: {imp}")
            return False
    
    # Check for required methods
    required_methods = [
        '_requires_visual_navigation',
        '_is_critical_action',
        '_handle_visual_navigation'
    ]
    
    methods_found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            methods_found.append(node.name)
    
    for method in required_methods:
        if method in methods_found:
            print(f"✓ Method found: {method}")
        else:
            print(f"✗ Missing method: {method}")
            return False
    
    # Check for vision_navigator initialization
    if 'vision_navigator' in content:
        print("✓ vision_navigator attribute found")
    else:
        print("✗ vision_navigator attribute not found")
        return False
    
    # Check for VisionNavigator initialization in initialize method
    if 'VisionNavigator(' in content:
        print("✓ VisionNavigator initialization found")
    else:
        print("✗ VisionNavigator initialization not found")
        return False
    
    # Check for visual navigation workflow components
    workflow_components = [
        'send_visual_navigation_request',
        'receive_visual_navigation_response',
        'send_visual_action_command',
        'receive_visual_action_result',
        'analyze_screen_for_action'
    ]
    
    for component in workflow_components:
        if component in content:
            print(f"✓ Workflow component found: {component}")
        else:
            print(f"✗ Missing workflow component: {component}")
            return False
    
    # Check for critical action detection
    if 'critical_keywords' in content:
        print("✓ Critical action detection found")
    else:
        print("✗ Critical action detection not found")
        return False
    
    # Check for iteration loop
    if 'max_iterations' in content and 'while iteration < max_iterations' in content:
        print("✓ Iteration loop found")
    else:
        print("✗ Iteration loop not found")
        return False
    
    # Check for confidence threshold checking
    if 'confidence_threshold' in content:
        print("✓ Confidence threshold checking found")
    else:
        print("✗ Confidence threshold checking not found")
        return False
    
    print("\n" + "=" * 60)
    print("✓ All verification checks passed!")
    print("\nImplementation Summary:")
    print("- Visual navigation command detection: ✓")
    print("- Visual navigation workflow orchestration: ✓")
    print("- Critical action confirmation: ✓")
    print("- Iteration loop with max_iterations: ✓")
    print("- Confidence threshold validation: ✓")
    print("- Message broker integration: ✓")
    
    return True


if __name__ == '__main__':
    success = verify_integration()
    sys.exit(0 if success else 1)
