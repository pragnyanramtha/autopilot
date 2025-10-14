# Dev Mode - No Pro Model Rule

## 🚨 Critical Rule

**DEV MODE NEVER USES `gemini-2.5-pro`**

This is enforced in the code and verified by tests.

## Why This Rule Exists

### Speed vs Quality Trade-off
- **Pro model**: 5-10 seconds per request (too slow for dev)
- **Flash model**: 1.5-3 seconds per request (fast enough)
- **Ultra-fast model**: 0.5-1 second per request (perfect for simple tasks)

### Development Needs
- Fast iteration cycles
- Quick feedback
- Rapid testing
- Cost efficiency
- Good enough quality

## Implementation

### Code Location
**File**: `ai_brain/gemini_client.py`  
**Method**: `_switch_model()`

### Logic
```python
if self.use_ultra_fast:  # Dev mode
    if complexity == 'complex':
        target_model = self.SIMPLE_MODEL  # gemini-2.5-flash (NOT PRO!)
    else:
        target_model = self.ULTRA_FAST_MODEL  # gemini-flash-lite-latest
```

### Key Points
1. Dev mode checks `self.use_ultra_fast`
2. Complex tasks use `SIMPLE_MODEL` (gemini-2.5-flash)
3. Simple tasks use `ULTRA_FAST_MODEL` (gemini-flash-lite-latest)
4. `COMPLEX_MODEL` (gemini-2.5-pro) is NEVER referenced in dev mode

## Verification

### Automated Test
```bash
python tests/test_dev_mode_models.py
```

**Test checks**:
- ✓ Dev mode does NOT use COMPLEX_MODEL
- ✓ Dev mode does NOT use gemini-2.5-pro
- ✓ Dev mode uses SIMPLE_MODEL for complex tasks
- ✓ Dev mode uses ULTRA_FAST_MODEL for simple tasks

### Manual Verification
```bash
# Start dev mode
start_dev_mode.bat

# Try complex command
> post about weather on X

# Should see:
⚡⚡ DEV MODE - Complex task: Using gemini-2.5-flash

# Should NEVER see:
❌ Using gemini-2.5-pro  # This would be wrong!
```

## Model Matrix

| Mode | Task | Model | Speed | Use |
|------|------|-------|-------|-----|
| Dev | Simple | gemini-flash-lite-latest | ⚡⚡⚡ | Development |
| Dev | Complex | gemini-2.5-flash | ⚡⚡ | Development |
| Normal | Simple | gemini-2.5-flash | ⚡⚡ | Production |
| Normal | Complex | gemini-2.5-pro | ⚡ | Production |

## Performance Impact

### Dev Mode (No Pro)
```
Simple task:  0.5-1.0s   (ultra-fast model)
Complex task: 1.5-3.0s   (flash model, NOT pro)
Total:        2.0-4.0s   ⚡⚡⚡ FAST
```

### Normal Mode (With Pro)
```
Simple task:  1.5-2.5s   (flash model)
Complex task: 5.0-10.0s  (pro model)
Total:        6.5-12.5s  ⚡ SLOW
```

**Dev mode is 3-4x faster!**

## When You Need Pro Model

Switch to normal mode for:
- ✅ Production deployments
- ✅ Final quality testing
- ✅ Critical business workflows
- ✅ Maximum accuracy required
- ✅ Complex reasoning tasks

## Documentation

- `docs/MODEL_USAGE_RULES.md` - Complete model usage rules
- `docs/DEV_MODE_MODEL_SELECTION.md` - Dev mode model selection details
- `tests/test_dev_mode_models.py` - Automated verification test

## Summary

### The Rule
> Dev mode prioritizes SPEED over maximum quality
> 
> Therefore: **NO PRO MODEL IN DEV MODE**

### Enforcement
- ✅ Enforced in code (`ai_brain/gemini_client.py`)
- ✅ Verified by tests (`tests/test_dev_mode_models.py`)
- ✅ Documented clearly (this file and others)

### Result
- 🚀 3-4x faster development iteration
- 💰 Lower API costs during development
- ⚡ Still maintains good quality with flash model
- 🎯 Pro model reserved for production only

---

**Status**: ✅ Implemented and Verified  
**Rule**: Dev mode NEVER uses gemini-2.5-pro  
**Reason**: Speed > Quality during development  
**Benefit**: 3-4x faster iteration cycles
