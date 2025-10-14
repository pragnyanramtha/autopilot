# Posting Workflow Bug Fix

## Problem
When users requested "post about today's weather on X" or similar social media posting commands, the system was only generating search protocols instead of complete posting workflows.

## Root Cause
The protocol generation prompt in `gemini_client.py` wasn't explicit enough about generating COMPLETE workflows for posting/publishing tasks. The AI would generate protocols that stopped at the research/search phase without including the actual posting steps.

## Solution

### 1. Enhanced Complexity Detection
Modified `_detect_command_complexity()` to ALWAYS treat posting/publishing commands as complex:

```python
# ALWAYS complex: posting/publishing to social media
posting_keywords = ['post on', 'post to', 'tweet about', 'publish to', 'share on']
if any(keyword in user_input_lower for keyword in posting_keywords):
    return 'complex'
```

This ensures commands like "post about X on Twitter" are properly identified as complex multi-step workflows.

### 2. Improved Protocol Generation Prompt
Enhanced the prompt template with explicit requirements for complete workflows:

**Key additions:**
- **Complete Workflows**: Explicitly requires ALL steps from opening browser to clicking post button
- **Content in Protocol**: Requires full content text, not placeholders
- **Social Media Posts**: Detailed step-by-step requirements for X/Twitter posts:
  1. Open browser
  2. Navigate to x.com
  3. Find and click compose area (with verify_screen)
  4. Type complete post content
  5. Find and click Post button (with verify_screen)
  6. Verify post was published

## Files Modified
- `ai_brain/gemini_client.py`
  - `_detect_command_complexity()` - Added posting keyword detection
  - `_build_protocol_prompt_template()` - Enhanced with complete workflow requirements

## Testing
To test the fix:
1. Run `start_ai.bat` or `start_ai_fast.bat`
2. Try command: "post about today's weather on X"
3. Verify the generated protocol includes:
   - Opening Chrome
   - Navigating to x.com
   - Finding compose area with verify_screen
   - Typing complete weather post content
   - Finding and clicking Post button
   - Verification step

## Expected Behavior
The system should now generate complete end-to-end protocols for posting commands that:
- Include all navigation steps
- Use visual verification for UI elements
- Type the complete generated content
- Click the post/publish button
- Verify successful posting

## Related Files
- `examples/protocols/twitter_post.json` - Example of correct posting protocol
- `ai_brain/main.py` - Handles complex protocol execution with content generation
- `ai_brain/protocol_generator.py` - Creates protocols from intents
