# Content Generation and JSON Parsing Fix

## Problems Identified

### Problem 1: Content Generation Safety Blocks
When generating content for social media posts, the Gemini API was returning safety blocks (finish_reason: 2), causing the error:
```
Error generating content: Invalid operation: The `response.text` quick accessor requires the response to contain a valid `Part`, but none were returned.
```

### Problem 2: Malformed JSON in Protocol Generation
The AI was generating protocols with unterminated strings, causing JSON parsing errors:
```
Failed to parse protocol JSON: Unterminated string starting at: line 58 column 14 (char 1432)
```

## Solutions Implemented

### 1. Content Generation Safety Block Handling

**File**: `ai_brain/gemini_client.py` - `generate_content()` method

**Changes**:
- Added check for blocked responses before accessing `response.text`
- Implemented fallback content generation when safety blocks occur
- Added new method `_generate_fallback_content()` to create simple, safe content

**Code**:
```python
# Check if response was blocked by safety filters
if not response.candidates or not response.candidates[0].content.parts:
    print(f"  ⚠ Content generation blocked by safety filters")
    # Generate a simple fallback based on topic
    fallback_content = self._generate_fallback_content(topic, content_type)
    self._cache_response(cache_key, fallback_content)
    return fallback_content
```

**Fallback Content Examples**:
- Tweet/Post: "Sharing thoughts about {topic}! 🌟 What do you think? #trending #discussion"
- Article: "An exploration of {topic} and its implications in today's world."

### 2. JSON Parsing Improvements

**File**: `ai_brain/gemini_client.py` - `_parse_protocol_response()` method

**Changes**:
- Added `_fix_common_json_issues()` method to repair malformed JSON
- Improved error messages with context around the error location
- Shows character position and surrounding text for debugging

**JSON Fixes Applied**:
1. **Missing Closing Braces**: Adds `}` if `{` count > `}` count
2. **Missing Closing Brackets**: Adds `]` if `[` count > `]` count  
3. **Unterminated Strings**: Attempts to close unclosed quotes

### 3. Protocol Generation Retry Logic

**File**: `ai_brain/gemini_client.py` - `generate_protocol()` method

**Changes**:
- Added retry mechanism (up to 2 attempts)
- Detects safety blocks and retries with simpler prompt
- Added `_build_simpler_protocol_prompt()` for retry attempts
- Better error messages showing which attempt failed

**Retry Flow**:
```
Attempt 1: Full detailed prompt
  ↓ (if fails)
Attempt 2: Simpler, more focused prompt with example
  ↓ (if fails)
Error with detailed context
```

### 4. Simpler Protocol Prompt for Retries

**File**: `ai_brain/gemini_client.py` - `_build_simpler_protocol_prompt()` method

**Purpose**: Provides a minimal, example-based prompt when the detailed prompt fails

**Features**:
- Shows exact JSON format expected
- Includes complete example for X/Twitter posting
- Emphasizes "Return ONLY valid JSON"
- Warns about properly closing strings

## Testing

### Test Content Generation
```python
from ai_brain.gemini_client import GeminiClient

client = GeminiClient()
content = client.generate_content(
    topic="today's weather",
    content_type="post",
    parameters={'style': 'engaging'}
)
print(content)
# Should return either AI-generated content or fallback if blocked
```

### Test Protocol Generation
```bash
# Run the AI Brain
start_ai_fast.bat

# Try the command that was failing
post something on x about todays weather
```

**Expected Behavior**:
1. Content generation succeeds or uses fallback
2. Protocol generation succeeds (possibly after retry)
3. Complete protocol with all posting steps is generated

## Error Handling Improvements

### Before
```
Error generating content: Invalid operation: The `response.text` quick accessor...
Error processing command: Failed to generate protocol: Failed to parse protocol JSON: Unterminated string...
```

### After
```
⚠ Content generation blocked by safety filters
✓ Using fallback content
⚠ Protocol generation failed (attempt 1/2): Unterminated string at position 1432
⚡ Protocol generated in 3.45s (attempt 2)
```

## Files Modified
- `ai_brain/gemini_client.py`
  - `generate_content()` - Added safety block handling
  - `_generate_fallback_content()` - New method for fallback content
  - `generate_protocol()` - Added retry logic
  - `_parse_protocol_response()` - Improved error messages
  - `_fix_common_json_issues()` - New method to repair JSON
  - `_build_simpler_protocol_prompt()` - New method for retry prompts

## Related Issues
- Posting workflow bug (fixed in POSTING_WORKFLOW_FIX.md)
- Safety block handling (improved across all generation methods)
- JSON parsing robustness (now handles incomplete responses)

## Future Improvements
- Consider using JSON schema validation for stricter protocol checking
- Add telemetry to track which types of content trigger safety blocks
- Implement more sophisticated JSON repair algorithms
- Add user notification when fallback content is used
