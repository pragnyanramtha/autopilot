# Remaining Bugs to Fix

## Status: 🔍 Identifying and Fixing

### ✅ FIXED BUGS
1. ✅ Missing action_library parameter
2. ✅ Protocol validation error
3. ✅ No actions registered in automation engine
4. ✅ Variable substitution type conversion (int vs string)
5. ✅ .env file not loaded in automation engine
6. ✅ Protocol ID mismatch (using description instead of id)

### 🐛 ACTIVE BUGS

#### Bug #7: Gemini Uses Literal "query" Instead of Actual Search Term
**Status**: ✅ FIXED

**Symptom**:
```
Parameters: {'text': 'query'}
```
Instead of:
```
Parameters: {'text': 'pragnyan ramtha'}
```

**Root Cause**: The prompt examples in `gemini_client.py` show "query" as a placeholder, and Gemini was copying it literally instead of substituting the actual user input.

**Location**: `ai_brain/gemini_client.py` - `_build_protocol_prompt_template` method

**Fix Applied**: 
1. Added critical warning at top of prompt: "Use the ACTUAL content from the user command, NOT placeholders!"
2. Updated examples to show where values come from
3. Added explicit note that values are from user command, not placeholders

**Test**: Restart AI Brain and try "search for pragnyan ramtha" - should now use actual name.

---

#### Bug #8: Variable Substitution Still Shows Template in Error
**Status**: 🟡 MEDIUM

**Symptom**:
```
Error details: {'params': {'x': '{{verified_x}}', 'y': '{{verified_y}}'}}
```

The error message shows the original template variables, not the substituted values. This makes debugging confusing.

**Root Cause**: Error is captured before substitution happens, or the error handler is showing the original params.

**Location**: `shared/protocol_executor.py` - Error handling in `_execute_action`

---

#### Bug #9: Complex Protocols Use Vision When Not Needed
**Status**: 🟡 MEDIUM

**Symptom**: Simple searches trigger vision verification unnecessarily, slowing down execution.

**Root Cause**: Gemini is being too cautious and adding `verify_screen` actions even for straightforward tasks.

**Fix Required**: Update prompts to discourage vision for simple, deterministic actions.

---

### 📋 POTENTIAL BUGS (Need Verification)

#### Potential Bug #10: Communication Timeout
**Symptom**: AI Brain sometimes shows "No result received" even when automation engine completes successfully.

**Needs Investigation**: Check if there's a race condition or timing issue.

---

#### Potential Bug #11: Protocol Description Too Generic
**Symptom**: Descriptions like "Performs a search for the term 'query'" are not helpful.

**Fix**: Make descriptions more specific with actual user intent.

---

## Fix Priority

1. 🔴 **CRITICAL** - Bug #7: Fix "query" literal issue
2. 🟡 **MEDIUM** - Bug #8: Fix error message showing templates
3. 🟡 **MEDIUM** - Bug #9: Reduce unnecessary vision checks
4. 🟢 **LOW** - Bug #10: Investigate communication timing
5. 🟢 **LOW** - Bug #11: Improve protocol descriptions

## Next Steps

1. Fix Bug #7 immediately (query literal issue)
2. Test with simple commands
3. Move to Bug #8 and #9
4. Document all fixes
