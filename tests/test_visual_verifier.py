"""
Tests for Visual Verification System

This module tests the VisualVerifier class and its integration with
the protocol executor.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.visual_verifier import VisualVerifier, VerificationResult
from automation_engine.screen_capture import ScreenCapture
from dotenv import load_dotenv


def test_visual_verifier_initialization():
    """Test that VisualVerifier initializes correctly."""
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("⚠ GEMINI_API_KEY not found in .env file")
        print("  Skipping visual verifier tests")
        return False
    
    try:
        screen_capture = ScreenCapture()
        verifier = VisualVerifier(
            screen_capture=screen_capture,
            api_key=api_key,
            timeout_seconds=10
        )
        
        print("✓ VisualVerifier initialized successfully")
        print(f"  Primary model: {verifier.primary_model_name}")
        print(f"  Fallback model: {verifier.fallback_model_name}")
        print(f"  Timeout: {verifier.timeout_seconds}s")
        
        return True
    except Exception as e:
        print(f"✗ Failed to initialize VisualVerifier: {e}")
        return False


def test_visual_verification_live():
    """
    Test visual verification with a live screenshot.
    
    This test captures the current screen and verifies a simple condition.
    """
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("⚠ GEMINI_API_KEY not found - skipping live test")
        return False
    
    try:
        screen_capture = ScreenCapture()
        verifier = VisualVerifier(
            screen_capture=screen_capture,
            api_key=api_key,
            timeout_seconds=15
        )
        
        print("\n" + "="*60)
        print("LIVE VISUAL VERIFICATION TEST")
        print("="*60)
        
        # Test 1: Verify desktop is visible
        print("\nTest 1: Verify desktop/screen is visible")
        result = verifier.verify_screen(
            context="Looking at the current screen",
            expected="Desktop or application window is visible",
            confidence_threshold=0.5
        )
        
        print(f"\nResult:")
        print(f"  Safe to proceed: {result.safe_to_proceed}")
        print(f"  Confidence: {result.confidence:.2f}")
        print(f"  Analysis: {result.analysis}")
        print(f"  Model used: {result.model_used}")
        
        if result.updated_coordinates:
            print(f"  Coordinates: ({result.updated_coordinates['x']}, {result.updated_coordinates['y']})")
        
        # Test 2: Look for something that probably doesn't exist
        print("\n" + "-"*60)
        print("\nTest 2: Look for non-existent element (should fail)")
        result2 = verifier.verify_screen(
            context="Looking for a purple unicorn button",
            expected="Purple unicorn button is visible and clickable",
            confidence_threshold=0.7
        )
        
        print(f"\nResult:")
        print(f"  Safe to proceed: {result2.safe_to_proceed}")
        print(f"  Confidence: {result2.confidence:.2f}")
        print(f"  Analysis: {result2.analysis}")
        print(f"  Model used: {result2.model_used}")
        
        if result2.suggested_actions:
            print(f"  Suggested actions: {result2.suggested_actions}")
        
        # Print statistics
        print("\n" + "-"*60)
        print("\nStatistics:")
        stats = verifier.get_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        print("\n✓ Live visual verification tests completed")
        return True
        
    except Exception as e:
        print(f"\n✗ Live test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_verification_result_parsing():
    """Test that VerificationResult parses correctly."""
    result = VerificationResult(
        safe_to_proceed=True,
        confidence=0.95,
        analysis="Test analysis",
        updated_coordinates={'x': 100, 'y': 200},
        suggested_actions=["action1", "action2"],
        model_used="test-model"
    )
    
    result_dict = result.to_dict()
    
    assert result_dict['safe_to_proceed'] == True
    assert result_dict['confidence'] == 0.95
    assert result_dict['analysis'] == "Test analysis"
    assert result_dict['updated_coordinates'] == {'x': 100, 'y': 200}
    assert result_dict['suggested_actions'] == ["action1", "action2"]
    assert result_dict['model_used'] == "test-model"
    
    print("✓ VerificationResult parsing test passed")
    return True


def main():
    """Run all visual verifier tests."""
    print("="*60)
    print("VISUAL VERIFIER TESTS")
    print("="*60)
    
    tests = [
        ("Initialization", test_visual_verifier_initialization),
        ("Result Parsing", test_verification_result_parsing),
        ("Live Verification", test_visual_verification_live),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {name}")
        print('='*60)
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
