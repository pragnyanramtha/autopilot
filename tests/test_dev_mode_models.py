"""
Test dev mode model selection.
Verifies that dev mode uses the correct models for simple and complex tasks.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_model_selection_logic():
    """Test that model selection logic is correct."""
    print("Testing model selection logic...")
    
    gemini_file = "ai_brain/gemini_client.py"
    with open(gemini_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for correct model selection in dev mode
    required_patterns = [
        "if self.use_ultra_fast:",
        "if complexity == 'complex':",
        "target_model = self.SIMPLE_MODEL  # gemini-2.5-flash for complex in dev mode",
        "target_model = self.ULTRA_FAST_MODEL  # gemini-flash-lite-latest for simple",
        "DEV MODE - Complex task",
        "DEV MODE - Simple task"
    ]
    
    all_found = True
    for pattern in required_patterns:
        if pattern in content:
            print(f"  ✓ Found: {pattern[:60]}...")
        else:
            print(f"  ✗ Missing: {pattern[:60]}...")
            all_found = False
    
    if all_found:
        print("  ✓ Model selection logic verified\n")
    else:
        print("  ✗ Model selection logic incomplete\n")
    
    return all_found


def test_no_pro_in_dev_mode():
    """Test that dev mode NEVER uses gemini-2.5-pro."""
    print("Testing that dev mode NEVER uses pro model...")
    
    gemini_file = "ai_brain/gemini_client.py"
    with open(gemini_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the _switch_model method
    method_start = content.find("def _switch_model(self, complexity: str = 'simple'):")
    method_end = content.find("\n    def ", method_start + 1)
    method_content = content[method_start:method_end]
    
    # Check that within use_ultra_fast block, COMPLEX_MODEL is never used
    ultra_fast_block_start = method_content.find("if self.use_ultra_fast:")
    ultra_fast_block_end = method_content.find("elif complexity == 'complex':")
    ultra_fast_block = method_content[ultra_fast_block_start:ultra_fast_block_end]
    
    # Verify COMPLEX_MODEL is NOT in the ultra_fast block
    if "COMPLEX_MODEL" in ultra_fast_block or "gemini-2.5-pro" in ultra_fast_block:
        print("  ✗ CRITICAL ERROR: Dev mode uses COMPLEX_MODEL (gemini-2.5-pro)!")
        print("  ✗ This violates the rule: Dev mode should NEVER use pro model")
        return False
    else:
        print("  ✓ Verified: Dev mode does NOT use COMPLEX_MODEL")
        print("  ✓ Verified: Dev mode does NOT use gemini-2.5-pro")
    
    # Verify it uses SIMPLE_MODEL for complex tasks in dev mode
    if "target_model = self.SIMPLE_MODEL  # gemini-2.5-flash for complex in dev mode" in ultra_fast_block:
        print("  ✓ Verified: Dev mode uses SIMPLE_MODEL for complex tasks")
    else:
        print("  ✗ Missing: Dev mode should use SIMPLE_MODEL for complex tasks")
        return False
    
    # Verify it uses ULTRA_FAST_MODEL for simple tasks in dev mode
    if "target_model = self.ULTRA_FAST_MODEL  # gemini-flash-lite-latest for simple" in ultra_fast_block:
        print("  ✓ Verified: Dev mode uses ULTRA_FAST_MODEL for simple tasks")
    else:
        print("  ✗ Missing: Dev mode should use ULTRA_FAST_MODEL for simple tasks")
        return False
    
    print("  ✓ Dev mode NEVER uses pro model - VERIFIED\n")
    return True


def test_model_constants():
    """Test that model constants are defined correctly."""
    print("Testing model constants...")
    
    gemini_file = "ai_brain/gemini_client.py"
    with open(gemini_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_constants = [
        "ULTRA_FAST_MODEL = 'gemini-flash-lite-latest'",
        "SIMPLE_MODEL = 'gemini-2.5-flash'",
        "COMPLEX_MODEL = 'gemini-2.5-pro'"
    ]
    
    all_found = True
    for constant in required_constants:
        if constant in content:
            print(f"  ✓ Found: {constant}")
        else:
            print(f"  ✗ Missing: {constant}")
            all_found = False
    
    if all_found:
        print("  ✓ Model constants verified\n")
    else:
        print("  ✗ Model constants incomplete\n")
    
    return all_found


def main():
    print("=" * 70)
    print("DEV MODE MODEL SELECTION VERIFICATION")
    print("=" * 70)
    print()
    
    results = []
    
    # Test model selection logic
    results.append(test_model_selection_logic())
    
    # Test that dev mode NEVER uses pro model (CRITICAL)
    results.append(test_no_pro_in_dev_mode())
    
    # Test model constants
    results.append(test_model_constants())
    
    # Summary
    print("=" * 70)
    if all(results):
        print("✓ ALL TESTS PASSED")
        print("=" * 70)
        print()
        print("Dev mode model selection is configured correctly!")
        print()
        print("Model Hierarchy:")
        print("  Normal Mode:")
        print("    - Simple tasks  → gemini-2.5-flash")
        print("    - Complex tasks → gemini-2.5-pro")
        print()
        print("  Dev Mode (Ultra-Fast) - NEVER USES PRO:")
        print("    - Simple tasks  → gemini-flash-lite-latest (⚡⚡⚡)")
        print("    - Complex tasks → gemini-2.5-flash (⚡⚡ NOT PRO!)")
        print()
        print("🚨 CRITICAL RULE: Dev mode NEVER uses gemini-2.5-pro")
        print("   Reason: Speed > Quality during development")
        print()
        print("To test:")
        print("  1. Run: start_dev_mode.bat")
        print("  2. Try simple: 'click at 500 300'")
        print("     Should see: ⚡⚡⚡ DEV MODE - Simple task")
        print("  3. Try complex: 'post about weather on X'")
        print("     Should see: ⚡⚡ DEV MODE - Complex task")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("=" * 70)
        print()
        print("Some tests failed. Please review the changes.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
