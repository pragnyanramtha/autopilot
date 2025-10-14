"""
Simple verification that the posting workflow fix is in place.
Checks the code changes without requiring full environment setup.
"""
import os
import sys


def verify_complexity_detection_fix():
    """Verify that _detect_command_complexity has posting keyword detection."""
    print("Checking complexity detection fix...")
    
    gemini_file = "ai_brain/gemini_client.py"
    with open(gemini_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for posting keyword detection
    required_code = [
        "posting_keywords = ['post on', 'post to', 'tweet about', 'publish to', 'share on']",
        "if any(keyword in user_input_lower for keyword in posting_keywords):",
        "return 'complex'"
    ]
    
    for code_snippet in required_code:
        if code_snippet in content:
            print(f"  ✓ Found: {code_snippet[:50]}...")
        else:
            print(f"  ✗ Missing: {code_snippet[:50]}...")
            return False
    
    print("  ✓ Complexity detection fix verified\n")
    return True


def verify_protocol_prompt_fix():
    """Verify that protocol generation prompt has complete workflow requirements."""
    print("Checking protocol generation prompt fix...")
    
    gemini_file = "ai_brain/gemini_client.py"
    with open(gemini_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for key requirements in prompt
    required_phrases = [
        "CRITICAL REQUIREMENTS:",
        "Complete Workflows",
        "Do NOT stop at just searching",
        "ENTIRE task from start to finish",
        "Content in Protocol",
        "FULL content text directly in the type action",
        "Social Media Posts",
        "Navigate to x.com",
        "Type the COMPLETE post content"
    ]
    
    all_found = True
    for phrase in required_phrases:
        if phrase in content:
            print(f"  ✓ Found: '{phrase}'")
        else:
            print(f"  ✗ Missing: '{phrase}'")
            all_found = False
    
    if all_found:
        print("  ✓ Protocol prompt fix verified\n")
    else:
        print("  ✗ Protocol prompt fix incomplete\n")
    
    return all_found


def main():
    print("=" * 70)
    print("POSTING WORKFLOW BUG FIX VERIFICATION")
    print("=" * 70)
    print()
    
    results = []
    
    # Verify complexity detection fix
    results.append(verify_complexity_detection_fix())
    
    # Verify protocol prompt fix
    results.append(verify_protocol_prompt_fix())
    
    # Summary
    print("=" * 70)
    if all(results):
        print("✓ ALL FIXES VERIFIED")
        print("=" * 70)
        print()
        print("The posting workflow bug has been fixed!")
        print()
        print("What was fixed:")
        print("  1. Posting commands (e.g., 'post on X') are now detected as complex")
        print("  2. Protocol generation now requires complete end-to-end workflows")
        print("  3. Protocols must include all steps: navigate → compose → type → post")
        print()
        print("To test:")
        print("  1. Run: start_ai.bat or start_ai_fast.bat")
        print("  2. Try: 'post about today's weather on X'")
        print("  3. Verify the protocol includes navigation, typing, and posting steps")
        return 0
    else:
        print("✗ SOME FIXES MISSING")
        print("=" * 70)
        print()
        print("Some fixes were not found in the code.")
        print("Please review the changes in ai_brain/gemini_client.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())
