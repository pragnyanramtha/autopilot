# Model Usage Rules - Quick Reference

## 🚨 Critical Rule

**DEV MODE NEVER USES `gemini-2.5-pro`**

Dev mode is optimized for speed, not maximum quality. The pro model is too slow for rapid development iteration.

## Model Hierarchy

### 📊 Complete Model Matrix

| Mode | Task Type | Model Used | Speed | When |
|------|-----------|------------|-------|------|
| **Normal** | Simple | `gemini-2.5-flash` | ⚡⚡ Fast | Production |
| **Normal** | Complex | `gemini-2.5-pro` | ⚡ Slow | Production |
| **Dev** | Simple | `gemini-flash-lite-latest` | ⚡⚡⚡ Ultra-Fast | Development |
| **Dev** | Complex | `gemini-2.5-flash` | ⚡⚡ Fast | Development |

## 🎯 Model Selection Logic

```python
if dev_mode:
    if simple_task:
        use "gemini-flash-lite-latest"  # ⚡⚡⚡
    else:  # complex_task
        use "gemini-2.5-flash"          # ⚡⚡ (NOT PRO!)
else:  # normal_mode
    if simple_task:
        use "gemini-2.5-flash"          # ⚡⚡
    else:  # complex_task
        use "gemini-2.5-pro"            # ⚡ (production only)
```

## ✅ Correct Usage

### Dev Mode
```bash
start_dev_mode.bat

# Simple command
> click at 500 300
⚡⚡⚡ DEV MODE - Simple task: Using gemini-flash-lite-latest

# Complex command
> post about weather on X
⚡⚡ DEV MODE - Complex task: Using gemini-2.5-flash
```

### Normal Mode
```bash
run.bat

# Simple command
> click at 500 300
Switched to simple model: gemini-2.5-flash

# Complex command
> post about weather on X
Switched to complex model: gemini-2.5-pro
```

## ❌ What You'll NEVER See

```bash
# This will NEVER happen in dev mode:
⚡⚡ DEV MODE - Complex task: Using gemini-2.5-pro  # ❌ WRONG!
```

## 🎨 Visual Indicators

### Dev Mode Indicators
- `⚡⚡⚡ DEV MODE - Simple task` = gemini-flash-lite-latest
- `⚡⚡ DEV MODE - Complex task` = gemini-2.5-flash (NOT pro)

### Normal Mode Indicators
- `Switched to simple model` = gemini-2.5-flash
- `Switched to complex model` = gemini-2.5-pro

## 📈 Performance Impact

### Dev Mode (Fast Iteration)
```
Simple:  0.5-1.0s  (gemini-flash-lite-latest)
Complex: 1.5-3.0s  (gemini-2.5-flash)
Total:   2.0-4.0s  ⚡⚡⚡ FAST
```

### Normal Mode (Production Quality)
```
Simple:  1.5-2.5s  (gemini-2.5-flash)
Complex: 5.0-10.0s (gemini-2.5-pro)
Total:   6.5-12.5s ⚡ SLOWER
```

**Dev mode is 3-4x faster for complex workflows!**

## 🔍 Why This Rule?

### Reasons Dev Mode Avoids Pro Model

1. **Speed**: Pro model is 3-5x slower than flash
2. **Iteration**: Need fast feedback during development
3. **Cost**: Pro model is more expensive
4. **Quality**: Flash is good enough for development
5. **Testing**: Want to test quickly, not perfectly

### When You Need Pro Model

- ✅ Production deployments
- ✅ Final testing before release
- ✅ Critical business workflows
- ✅ Maximum quality required
- ✅ Complex reasoning tasks

### When Flash is Fine

- ✅ Development and testing
- ✅ Rapid prototyping
- ✅ Debugging issues
- ✅ Learning the system
- ✅ Most automation tasks

## 🛠️ Code Implementation

**File**: `ai_brain/gemini_client.py`

```python
def _switch_model(self, complexity: str = 'simple'):
    if self.use_ultra_fast:
        # Dev mode: NEVER use pro model
        if complexity == 'complex':
            target_model = self.SIMPLE_MODEL  # gemini-2.5-flash
        else:
            target_model = self.ULTRA_FAST_MODEL  # gemini-flash-lite-latest
    elif complexity == 'complex':
        target_model = self.COMPLEX_MODEL  # gemini-2.5-pro (normal mode only)
    else:
        target_model = self.SIMPLE_MODEL  # gemini-2.5-flash
```

## 📋 Checklist

### Before Starting Development
- [ ] Using `start_dev_mode.bat`?
- [ ] See `⚡⚡⚡ DEV MODE` in output?
- [ ] Simple tasks use `gemini-flash-lite-latest`?
- [ ] Complex tasks use `gemini-2.5-flash`?
- [ ] NEVER see `gemini-2.5-pro` in dev mode?

### Before Production Deployment
- [ ] Using `run.bat` (normal mode)?
- [ ] Simple tasks use `gemini-2.5-flash`?
- [ ] Complex tasks use `gemini-2.5-pro`?
- [ ] Tested with production models?
- [ ] Performance acceptable?

## 🎓 Summary

### The Golden Rule
> **Dev mode prioritizes SPEED over maximum quality**
> 
> Therefore: **NO PRO MODEL IN DEV MODE**

### Model Assignments
- **Ultra-Fast** (`gemini-flash-lite-latest`) → Dev simple tasks
- **Fast** (`gemini-2.5-flash`) → Dev complex tasks + Normal simple tasks
- **Pro** (`gemini-2.5-pro`) → Normal complex tasks ONLY

### Remember
- 🚀 Dev mode = Fast iteration
- 🎯 Normal mode = Production quality
- ⚡⚡⚡ Ultra-fast for simple dev tasks
- ⚡⚡ Fast for complex dev tasks
- ⚡ Pro for complex production tasks

---

**Status**: ✅ Enforced in code  
**Rule**: Dev mode NEVER uses gemini-2.5-pro  
**Reason**: Speed > Quality during development
