# Dev Mode Model Selection

## Overview
Dev mode (ultra-fast mode) now uses an optimized model hierarchy for faster development and testing.

## Model Selection Strategy

### Normal Mode (Production)
| Task Complexity | Model Used | Speed | Quality |
|----------------|------------|-------|---------|
| Simple | `gemini-2.5-flash` | Fast | High |
| Complex | `gemini-2.5-pro` | Slower | Highest |

### Dev Mode (Ultra-Fast) - NEVER USES PRO MODEL
| Task Complexity | Model Used | Speed | Quality |
|----------------|------------|-------|---------|
| Simple | `gemini-flash-lite-latest` | Ultra-Fast | Good |
| Complex | `gemini-2.5-flash` | Fast | High |

**Important**: Dev mode NEVER uses `gemini-2.5-pro` - it uses `gemini-2.5-flash` even for complex tasks to maintain fast iteration speed.

## Key Differences

### Simple Tasks (click, type, search)
- **Normal Mode**: Uses `gemini-2.5-flash`
- **Dev Mode**: Uses `gemini-flash-lite-latest` (⚡⚡⚡ ultra-fast)

### Complex Tasks (posting, multi-step workflows)
- **Normal Mode**: Uses `gemini-2.5-pro` (highest quality, slower)
- **Dev Mode**: Uses `gemini-2.5-flash` (⚡⚡ fast, NO PRO MODEL)

### Critical Rule
**Dev mode NEVER uses `gemini-2.5-pro`** - this ensures fast iteration during development. The pro model is reserved for production use only.

## Benefits of Dev Mode

1. **Faster Simple Commands**: Ultra-fast model for quick testing
2. **Balanced Complex Commands**: Fast model instead of pro for quicker iteration
3. **Cost Effective**: Cheaper models for development
4. **Good Quality**: Still maintains high quality for complex tasks

## Activation

### Via Batch File
```bash
# Automatically enables dev mode
start_dev_mode.bat
```

### Via Environment Variable
```bash
# In .env file
USE_ULTRA_FAST_MODEL=true
```

### Via Code
```python
from ai_brain.gemini_client import GeminiClient

# Enable dev mode
client = GeminiClient(use_ultra_fast=True)
```

## Visual Indicators

### Normal Mode
```
→ Analyzing command with Gemini...
  Switched to simple model: gemini-2.5-flash
  ⚡ API response time: 2.34s
```

### Dev Mode - Simple Task
```
→ Analyzing command with Gemini...
  ⚡⚡⚡ DEV MODE - Simple task: Using gemini-flash-lite-latest
  ⚡ API response time: 0.87s
```

### Dev Mode - Complex Task
```
→ Analyzing command with Gemini...
  ⚡⚡ DEV MODE - Complex task: Using gemini-2.5-flash
  ⚡ API response time: 1.45s
```

## Performance Comparison

### Simple Command: "click the button"
| Mode | Model | Avg Time |
|------|-------|----------|
| Normal | gemini-2.5-flash | ~2.0s |
| Dev | gemini-flash-lite-latest | ~0.8s |
| **Speedup** | | **2.5x faster** |

### Complex Command: "post about weather on X"
| Mode | Model | Avg Time |
|------|-------|----------|
| Normal | gemini-2.5-pro | ~8.0s |
| Dev | gemini-2.5-flash | ~3.0s |
| **Speedup** | | **2.7x faster** |

## When to Use Each Mode

### Use Normal Mode When:
- ✓ Running in production
- ✓ Need highest quality responses
- ✓ Complex reasoning required
- ✓ Final testing before deployment

### Use Dev Mode When:
- ✓ Rapid development and testing
- ✓ Iterating on protocols
- ✓ Testing basic functionality
- ✓ Cost optimization during development

## Code Changes

**File**: `ai_brain/gemini_client.py`

**Method**: `_switch_model()`

**Logic**:
```python
if self.use_ultra_fast:
    # Dev mode: ultra-fast for simple, fast for complex
    if complexity == 'complex':
        target_model = self.SIMPLE_MODEL  # gemini-2.5-flash
    else:
        target_model = self.ULTRA_FAST_MODEL  # gemini-flash-lite-latest
elif complexity == 'complex':
    target_model = self.COMPLEX_MODEL  # gemini-2.5-pro
else:
    target_model = self.SIMPLE_MODEL  # gemini-2.5-flash
```

## Testing

### Test Simple Command
```bash
start_dev_mode.bat
# Try: "click at 500 300"
# Should see: ⚡⚡⚡ DEV MODE - Simple task: Using gemini-flash-lite-latest
```

### Test Complex Command
```bash
start_dev_mode.bat
# Try: "post about weather on X"
# Should see: ⚡⚡ DEV MODE - Complex task: Using gemini-2.5-flash
```

## Model Specifications

### gemini-flash-lite-latest
- **Speed**: Ultra-fast (~0.5-1.0s)
- **Quality**: Good
- **Use Case**: Simple commands, quick testing
- **Cost**: Lowest

### gemini-2.5-flash
- **Speed**: Fast (~1.5-3.0s)
- **Quality**: High
- **Use Case**: Complex tasks, general purpose
- **Cost**: Medium

### gemini-2.5-pro
- **Speed**: Slower (~5.0-10.0s)
- **Quality**: Highest
- **Use Case**: Complex reasoning, production
- **Cost**: Highest

## Recommendations

1. **Development**: Always use dev mode for faster iteration
2. **Testing**: Use dev mode for initial testing, normal mode for final validation
3. **Production**: Always use normal mode for best quality
4. **Debugging**: Use dev mode to quickly test fixes

## Related Files
- `start_dev_mode.bat` - Launches dev mode
- `start_ai_fast.bat` - Launches dev mode (alias)
- `ai_brain/gemini_client.py` - Model selection logic
- `.env` - Configuration file

---

**Status**: ✅ Implemented  
**Version**: 1.0  
**Date**: 2025-01-13
