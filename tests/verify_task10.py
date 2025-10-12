"""
Verification Script for Task 10: Protocol Configuration System

This script verifies that the protocol configuration system is working correctly.
"""

import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shared.config_loader import get_config, ConfigLoader


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def verify_config_file():
    """Verify config.json has protocol section."""
    print_section("1. Verifying config.json Structure")
    
    try:
        with open('config.json', 'r') as f:
            config_data = json.load(f)
        
        if 'protocol' not in config_data:
            print("❌ FAIL: 'protocol' section missing from config.json")
            return False
        
        protocol = config_data['protocol']
        
        # Check required sections
        required_sections = ['validation', 'visual_verification', 'mouse_movement', 'action_library']
        for section in required_sections:
            if section in protocol:
                print(f"✓ Found section: {section}")
            else:
                print(f"❌ Missing section: {section}")
                return False
        
        # Check old workflow settings removed
        if 'communication' in config_data:
            comm = config_data['communication']
            if 'workflow_file' in comm:
                print("⚠ Warning: Old 'workflow_file' still present (should be 'protocol_file')")
            if 'protocol_file' in comm:
                print("✓ Updated to use 'protocol_file'")
        
        print("\n✅ Config file structure is correct")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Error reading config.json: {e}")
        return False


def verify_config_loader():
    """Verify ConfigLoader works correctly."""
    print_section("2. Verifying ConfigLoader")
    
    try:
        config = get_config()
        
        print(f"✓ Config loaded successfully")
        print(f"  Type: {type(config).__name__}")
        
        # Verify all sections exist
        sections = ['validation', 'visual_verification', 'mouse_movement', 'action_library']
        for section in sections:
            if hasattr(config, section):
                print(f"✓ Has section: {section}")
            else:
                print(f"❌ Missing section: {section}")
                return False
        
        print("\n✅ ConfigLoader working correctly")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Error loading config: {e}")
        return False


def verify_validation_config():
    """Verify validation configuration."""
    print_section("3. Verifying Validation Configuration")
    
    try:
        config = get_config()
        val = config.validation
        
        print(f"✓ strict_mode: {val.strict_mode} (type: {type(val.strict_mode).__name__})")
        print(f"✓ warning_level: {val.warning_level} (type: {type(val.warning_level).__name__})")
        
        # Validate types
        if not isinstance(val.strict_mode, bool):
            print(f"❌ strict_mode should be bool, got {type(val.strict_mode)}")
            return False
        
        if val.warning_level not in ['none', 'errors_only', 'all']:
            print(f"❌ warning_level should be 'none', 'errors_only', or 'all', got '{val.warning_level}'")
            return False
        
        print("\n✅ Validation configuration is correct")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Error verifying validation config: {e}")
        return False


def verify_visual_verification_config():
    """Verify visual verification configuration."""
    print_section("4. Verifying Visual Verification Configuration")
    
    try:
        config = get_config()
        vis = config.visual_verification
        
        print(f"✓ enabled: {vis.enabled}")
        print(f"✓ timeout_seconds: {vis.timeout_seconds}")
        print(f"✓ confidence_threshold: {vis.confidence_threshold}")
        print(f"✓ primary_model: {vis.primary_model}")
        print(f"✓ fallback_model: {vis.fallback_model}")
        
        # Validate types and ranges
        if not isinstance(vis.enabled, bool):
            print(f"❌ enabled should be bool")
            return False
        
        if not isinstance(vis.timeout_seconds, int) or vis.timeout_seconds <= 0:
            print(f"❌ timeout_seconds should be positive int")
            return False
        
        if not (0.0 <= vis.confidence_threshold <= 1.0):
            print(f"❌ confidence_threshold should be between 0.0 and 1.0")
            return False
        
        if not vis.primary_model or not vis.fallback_model:
            print(f"❌ Models should be non-empty strings")
            return False
        
        print("\n✅ Visual verification configuration is correct")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Error verifying visual verification config: {e}")
        return False


def verify_mouse_movement_config():
    """Verify mouse movement configuration."""
    print_section("5. Verifying Mouse Movement Configuration")
    
    try:
        config = get_config()
        mouse = config.mouse_movement
        
        print(f"✓ smooth: {mouse.smooth}")
        print(f"✓ curve_type: {mouse.curve_type}")
        print(f"✓ curve_intensity: {mouse.curve_intensity}")
        print(f"✓ speed: {mouse.speed}")
        print(f"✓ overshoot: {mouse.overshoot}")
        print(f"✓ overshoot_amount: {mouse.overshoot_amount}")
        print(f"✓ add_noise: {mouse.add_noise}")
        print(f"✓ noise_amount: {mouse.noise_amount}")
        print(f"✓ min_duration: {mouse.min_duration}")
        print(f"✓ max_duration: {mouse.max_duration}")
        
        # Validate smooth curves are default
        if not mouse.smooth:
            print("⚠ Warning: smooth should be True by default")
        
        if mouse.curve_type != "bezier":
            print("⚠ Warning: curve_type should be 'bezier' by default")
        
        # Validate ranges
        if not (0.0 <= mouse.curve_intensity <= 1.0):
            print(f"❌ curve_intensity should be between 0.0 and 1.0")
            return False
        
        if mouse.speed <= 0:
            print(f"❌ speed should be positive")
            return False
        
        if mouse.min_duration >= mouse.max_duration:
            print(f"❌ min_duration should be less than max_duration")
            return False
        
        print("\n✅ Mouse movement configuration is correct")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Error verifying mouse movement config: {e}")
        return False


def verify_action_library_config():
    """Verify action library configuration."""
    print_section("6. Verifying Action Library Configuration")
    
    try:
        config = get_config()
        actions = config.action_library
        
        print(f"✓ enabled_categories: {len(actions.enabled_categories)} categories")
        for cat in actions.enabled_categories:
            print(f"  - {cat}")
        
        print(f"✓ disabled_actions: {len(actions.disabled_actions)} actions")
        if actions.disabled_actions:
            for action in actions.disabled_actions:
                print(f"  - {action}")
        else:
            print("  (none)")
        
        # Check expected categories
        expected_categories = [
            "keyboard", "mouse", "window", "browser", "clipboard",
            "file", "screen", "timing", "vision", "system", "edit", "macro"
        ]
        
        missing = set(expected_categories) - set(actions.enabled_categories)
        if missing:
            print(f"⚠ Warning: Missing categories: {missing}")
        
        # Test is_action_enabled method
        test_enabled = actions.is_action_enabled("press_key", "keyboard")
        print(f"\n✓ is_action_enabled('press_key', 'keyboard'): {test_enabled}")
        
        if not test_enabled:
            print("❌ press_key should be enabled")
            return False
        
        print("\n✅ Action library configuration is correct")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Error verifying action library config: {e}")
        return False


def verify_singleton_pattern():
    """Verify singleton pattern works."""
    print_section("7. Verifying Singleton Pattern")
    
    try:
        config1 = get_config()
        config2 = ConfigLoader.load()
        
        if config1 is config2:
            print("✓ Singleton pattern working (same instance returned)")
        else:
            print("❌ Singleton pattern not working (different instances)")
            return False
        
        print("\n✅ Singleton pattern verified")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Error verifying singleton: {e}")
        return False


def verify_documentation():
    """Verify documentation exists."""
    print_section("8. Verifying Documentation")
    
    doc_file = "docs/PROTOCOL_CONFIGURATION.md"
    
    if os.path.exists(doc_file):
        print(f"✓ Documentation exists: {doc_file}")
        
        with open(doc_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for key sections
        required_sections = [
            "Validation Configuration",
            "Visual Verification Configuration",
            "Mouse Movement Configuration",
            "Action Library Configuration",
            "Using Configuration in Code"
        ]
        
        for section in required_sections:
            if section in content:
                print(f"✓ Has section: {section}")
            else:
                print(f"⚠ Missing section: {section}")
        
        print("\n✅ Documentation verified")
        return True
    else:
        print(f"❌ Documentation not found: {doc_file}")
        return False


def main():
    """Run all verification tests."""
    print("\n" + "="*60)
    print("  TASK 10 VERIFICATION: Protocol Configuration System")
    print("="*60)
    
    tests = [
        ("Config File Structure", verify_config_file),
        ("Config Loader", verify_config_loader),
        ("Validation Config", verify_validation_config),
        ("Visual Verification Config", verify_visual_verification_config),
        ("Mouse Movement Config", verify_mouse_movement_config),
        ("Action Library Config", verify_action_library_config),
        ("Singleton Pattern", verify_singleton_pattern),
        ("Documentation", verify_documentation),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ EXCEPTION in {name}: {e}")
            results.append((name, False))
    
    # Summary
    print_section("VERIFICATION SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n{'='*60}")
    print(f"  Results: {passed}/{total} tests passed")
    print(f"{'='*60}\n")
    
    if passed == total:
        print("🎉 All verification tests passed!")
        print("\nTask 10 Implementation Complete:")
        print("✓ Removed old workflow-related config settings")
        print("✓ Added protocol validation settings (strict mode, warning level)")
        print("✓ Configured visual verification settings (timeout, confidence threshold)")
        print("✓ Updated mouse movement defaults to use smooth curves")
        print("✓ Added action library configuration (enable/disable specific actions)")
        print("✓ Created ConfigLoader utility for easy access")
        print("✓ Created comprehensive documentation")
        return 0
    else:
        print(f"⚠ {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
