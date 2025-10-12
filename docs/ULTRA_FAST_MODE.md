# ⚡⚡⚡ Ultra-Fast Mode

## Overview

Ultra-Fast Mode uses Google's **gemini-2.0-flash-exp** model for maximum speed during development.

## Speed Comparison

| Mode | Model | Speed | Use Case |
|------|-------|-------|----------|
| **Ultra-Fast** | gemini-2.0-flash-exp | ⚡⚡⚡ Fastest | Development, testing |
| Normal | gemini-2.5-flash | ⚡⚡ Fast | Production, simple tasks |
| Complex | gemini-2.5-pro | ⚡ Smart | Complex reasoning |

## Performance

### Ultra-Fast Mode
```
Simple command:     0.5-0.8 seconds ⚡⚡⚡
Complex command:    1.0-1.5 seconds ⚡⚡⚡
Content generation: 1.5-2.0 seconds ⚡⚡⚡
Cached command:     <0.001 seconds ⚡⚡⚡
```

### Normal Mode (for comparison)
```
Simple command:     1.0-1.5 seconds ⚡⚡
Complex command:    2.5-4.0 seconds ⚡
Content generation: 2.0-4.0 seconds ⚡
Cached command:     <0.001 seconds ⚡⚡⚡
```

**Result: 2-3x faster than normal mode!**

## How to Enable

### Method 1: Developer Mode (Recommended)

Edit `dev.bat`:
```batch
REM Enable ultra-fast mode
SET DEV_ULTRA_FAST_MODEL=true
```

Then run:
```bash
dev.bat
```

### Method 2: Config File

Edit `config.json`:
```json
{
  "gemini": {
    "use_ultra_fast": true,
    "ultra_fast_model": "gemini-2.0-flash-exp"
  }
}
```

### Method 3: Environment Variable

Set environment variable:
```bash
# Windows (CMD)
set USE_ULTRA_FAST_MODEL=true

# Windows (PowerShell)
$env:USE_ULTRA_FAST_MODEL="true"

# Linux/Mac
export USE_ULTRA_FAST_MODEL=true
```

### Method 4: Code

```python
from ai_brain.gemini_client import GeminiClient

# Enable ultra-fast mode
client = GeminiClient(use_ultra_fast=True)

# Use normally
intent = client.process_command("Click the button")
# ⚡⚡⚡ Ultra-fast response!
```

## When to Use

### ✅ Use Ultra-Fast Mode For:
- **Development** - Fast iteration
- **Testing** - Quick feedback
- **Debugging** - Rapid testing
- **Simple commands** - Click, type, etc.
- **Prototyping** - Quick experiments

### ⚠️ Consider Normal Mode For:
- **Production** - More reliable
- **Complex reasoning** - Better quality
- **Content generation** - Better writing
- **Critical tasks** - More accurate

### ❌ Don't Use Ultra-Fast For:
- **Final production** - Use normal mode
- **High-stakes tasks** - Use complex model
- **Long-form content** - Use complex model

## Features

### What Works in Ultra-Fast Mode
- ✅ All basic commands (click, type, etc.)
- ✅ Simple workflows
- ✅ Search commands
- ✅ Navigation
- ✅ Short content generation
- ✅ Response caching
- ✅ All optimizations

### What's Different
- ⚡ Much faster responses
- 📉 Slightly lower accuracy (still good)
- 🎯 Best for simple tasks
- 💰 Lower API costs

## Examples

### Example 1: Simple Command
```python
client = GeminiClient(use_ultra_fast=True)

# Ultra-fast response (~0.5s)
intent = client.process_command("Click the submit button")
```

### Example 2: Search Command
```python
client = GeminiClient(use_ultra_fast=True)

# Ultra-fast search (~0.8s)
intent = client.process_command("Search for Python tutorials")
```

### Example 3: Short Content
```python
client = GeminiClient(use_ultra_fast=True)

# Ultra-fast generation (~1.5s)
content = client.generate_content(
    "AI trends",
    content_type="tweet"
)
```

## Configuration

### dev.bat Settings
```batch
REM ========================================
REM ULTRA-FAST MODE CONFIGURATION
REM ========================================

REM Enable/Disable Ultra-Fast Mode
SET DEV_ULTRA_FAST_MODEL=true

REM Model Selection (if ultra-fast is disabled)
SET DEV_SIMPLE_MODEL=gemini-2.5-flash
SET DEV_COMPLEX_MODEL=gemini-2.5-pro

REM Other settings...
SET DEV_TEMPERATURE=0.7
SET DEV_SPEED=1.0
```

### config.json Settings
```json
{
  "gemini": {
    "use_ultra_fast": true,
    "ultra_fast_model": "gemini-2.0-flash-exp",
    "simple_model": "gemini-2.5-flash",
    "complex_model": "gemini-2.5-pro",
    "temperature": 0.7
  }
}
```

## Workflow

### Development Workflow
```
1. Enable ultra-fast mode in dev.bat
2. Run: dev.bat
3. Test commands quickly
4. Iterate rapidly
5. Switch to normal mode for production
```

### Testing Workflow
```
1. Enable ultra-fast mode
2. Test basic functionality
3. Verify commands work
4. Check edge cases
5. Switch to normal mode for final testing
```

## Performance Tips

### 1. Combine with Caching
```python
client = GeminiClient(use_ultra_fast=True)

# First request: ~0.5s
client.process_command("Click button")

# Cached request: <0.001s
client.process_command("Click button")
```

### 2. Use for Rapid Iteration
```python
# Test multiple variations quickly
commands = [
    "Click submit",
    "Click the submit button",
    "Press submit",
]

for cmd in commands:
    intent = client.process_command(cmd)
    print(f"{cmd} -> {intent.action}")
    # Each takes ~0.5s instead of 1.5s
```

### 3. Batch Testing
```python
# Test 10 commands in ~5 seconds instead of 15
test_commands = [...]
for cmd in test_commands:
    result = client.process_command(cmd)
    # Ultra-fast processing
```

## Monitoring

### Check Current Mode
```python
client = GeminiClient(use_ultra_fast=True)

if client.use_ultra_fast:
    print("⚡⚡⚡ Ultra-Fast Mode Active")
    print(f"Model: {client.current_model_name}")
```

### Performance Stats
```python
stats = client.get_performance_stats()

print(f"Average time: {stats['avg_response_time']:.2f}s")
print(f"Total requests: {stats['total_requests']}")
print(f"Cache size: {stats['cache_size']}")
```

## Troubleshooting

### Issue: Not Fast Enough
**Check:**
1. Ultra-fast mode enabled?
2. Internet connection speed
3. API quota limits
4. Cache working?

**Solution:**
```python
# Verify mode
print(f"Ultra-fast: {client.use_ultra_fast}")
print(f"Model: {client.current_model_name}")

# Clear cache and retry
client.clear_cache()
```

### Issue: Lower Accuracy
**Expected:** Ultra-fast model trades some accuracy for speed

**Solution:**
- Use normal mode for critical tasks
- Use complex model for important content
- Ultra-fast is best for development

### Issue: Model Not Available
**Error:** Model not found or unavailable

**Solution:**
1. Check model name: `gemini-2.0-flash-exp`
2. Verify API access
3. Try fallback: `gemini-2.5-flash`

## Comparison Table

| Feature | Ultra-Fast | Normal | Complex |
|---------|-----------|--------|---------|
| Speed | ⚡⚡⚡ | ⚡⚡ | ⚡ |
| Accuracy | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Cost | 💰 | 💰💰 | 💰💰💰 |
| Use Case | Dev/Test | Production | Complex |
| Response Time | 0.5-0.8s | 1.0-1.5s | 2.5-4.0s |

## Best Practices

### 1. Development Phase
```
✅ Use ultra-fast mode
✅ Iterate quickly
✅ Test basic functionality
✅ Debug issues rapidly
```

### 2. Testing Phase
```
⚠️ Use normal mode
✅ Verify accuracy
✅ Test edge cases
✅ Validate results
```

### 3. Production Phase
```
✅ Use normal mode
✅ Enable caching
✅ Monitor performance
✅ Use complex for important tasks
```

## Summary

### What is Ultra-Fast Mode?
- Uses gemini-2.0-flash-exp model
- 2-3x faster than normal mode
- Best for development and testing

### How to Enable?
- Set `DEV_ULTRA_FAST_MODEL=true` in dev.bat
- Or set `use_ultra_fast: true` in config.json
- Or use `GeminiClient(use_ultra_fast=True)`

### When to Use?
- ✅ Development
- ✅ Testing
- ✅ Debugging
- ⚠️ Not for production

### Performance?
- Simple commands: 0.5-0.8s (2-3x faster)
- Complex commands: 1.0-1.5s (2-3x faster)
- Cached: <0.001s (instant)

---

**⚡⚡⚡ Enjoy ultra-fast development! ⚡⚡⚡**
