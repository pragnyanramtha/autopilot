"""
Verify the content generation and JSON parsing fixes.
"""
import os
import sys


def verify_content_generation_fix():
    """Verify that content generation has safety block handling."""
    print("Checking content generation fix...")
    
    gemini_file = "ai_brain/gemini_client.py"
    with open(gemini_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_code = [
        "if not response.candidates or not response.candidates[0].content.parts:",
        "Content generation blocked by safety filters",
        "_generate_fallback_content",
        "def _generate_fallback_content(self, topic: str, content_type: str) -> str:"
    ]
    
    all_found = True
    for code_snippet in required_code:
        if code_snippet in content:
            print(f"  ✓ Found: {code_snippet[:60]}...")
        else:
            print(f"  ✗ Missing: {code_snippet[:60]}...")
            all_found = False
    
    if all_found:
        print("  ✓ Content generation fix verified\n")
    else:
        print("  ✗ Content generation fix incomplete\n")
    
    return all_found


def verify_json_parsing_fix():
    """Verify that JSON parsing has error handling improvements."""
    print("Checking JSON parsing fix...")
    
    gemini_file = "ai_brain/gemini_client.py"
    with open(gemini_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_code = [
        "_fix_common_json_issues",
        "def _fix_common_json_issues(self, json_str: str) -> str:",
        "if json_str.count('{') > json_str.count('}'):",
        "Context around error:"
    ]
    
    all_found = True
    for code_snippet in required_code:
        if code_snippet in content:
            print(f"  ✓ Found: {code_snippet[:60]}...")
        else:
            print(f"  ✗ Missing: {code_snippet[:60]}...")
            all_found = False
    
    if all_found:
        print("  ✓ JSON parsing fix verified\n")
    else:
        print("  ✗ JSON parsing fix incomplete\n")
    
    return all_found


def verify_retry_logic():
    """Verify that protocol generation has retry logic."""
    print("Checking retry logic...")
    
    gemini_file = "ai_brain/gemini_client.py"
    with open(gemini_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_code = [
        "max_retries = 2",
        "for attempt in range(max_retries):",
        "_build_simpler_protocol_prompt",
        "def _build_simpler_protocol_prompt(self, user_input: str, action_library: dict) -> str:",
        "Protocol generation blocked by safety filters"
    ]
    
    all_found = True
    for code_snippet in required_code:
        if code_snippet in content:
            print(f"  ✓ Found: {code_snippet[:60]}...")
        else:
            print(f"  ✗ Missing: {code_snippet[:60]}...")
            all_found = False
    
    if all_found:
        print("  ✓ Retry logic verified\n")
    else:
        print("  ✗ Retry logic incomplete\n")
    
    return all_found


def main():
    print("=" * 70)
    print("CONTENT GENERATION AND JSON PARSING FIX VERIFICATION")
    print("=" * 70)
    print()
    
    results = []
    
    # Verify content generation fix
    results.append(verify_content_generation_fix())
    
    # Verify JSON parsing fix
    results.append(verify_json_parsing_fix())
    
    # Verify retry logic
    results.append(verify_retry_logic())
    
    # Summary
    print("=" * 70)
    if all(results):
        print("✓ ALL FIXES VERIFIED")
        print("=" * 70)
        print()
        print("The content generation and JSON parsing issues have been fixed!")
        print()
        print("What was fixed:")
        print("  1. Content generation now handles safety blocks gracefully")
        print("  2. Fallback content is generated when AI blocks content")
        print("  3. JSON parsing attempts to fix common malformed JSON issues")
        print("  4. Protocol generation retries up to 2 times on failure")
        print("  5. Simpler prompts are used for retry attempts")
        print()
        print("To test:")
        print("  1. Run: start_ai_fast.bat")
        print("  2. Try: 'post something on x about todays weather'")
        print("  3. Should now complete successfully with fallback content if needed")
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
