# ⚡⚡⚡ Ultra-Fast Mode - Quick Start

## What is it?

Ultra-Fast Mode uses **gemini-2.0-flash-exp** for **2-3x faster** AI responses during development.

## Speed

- **Simple commands**: 0.5-0.8s (was 1.0-1.5s) ⚡⚡⚡
- **Complex commands**: 1.0-1.5s (was 2.5-4.0s) ⚡⚡⚡
- **Content generation**: 1.5-2.0s (was 2.0-4.0s) ⚡⚡⚡
- **Cached**: <0.001s (instant) ⚡⚡⚡

## How to Enable

### Quick Way (Recommended)

Edit `dev.bat`:
```batch
SET DEV_ULTRA_FAST_MODEL=true
```

Run:
```bash
dev.bat
```

### Alternative: Config File

Edit `config.json`:
```json
{
  "gemini": {
    "use_ultra_fast": true
  }
}
```

### Alternative: Code

```python
from ai_brain.gemini_client import GeminiClient

client = GeminiClient(use_ultra_fast=True)
```

## When to Use

✅ **Use for:**
- Development
- Testing
- Debugging
- Quick iteration

⚠️ **Don't use for:**
- Production
- Critical tasks
- Long-form content

## Example

```python
# Enable ultra-fast mode
client = GeminiClient(use_ultra_fast=True)

# Get ultra-fast response (~0.5s instead of 1.5s)
intent = client.process_command("Click the button")
# ⚡⚡⚡ 3x faster!
```

## Benefits

- ⚡ **2-3x faster** responses
- 💰 **Lower** API costs
- 🚀 **Rapid** iteration
- ✅ **Same** features
- 🔄 **Easy** to toggle

## Documentation

- **Complete Guide**: [docs/ULTRA_FAST_MODE.md](docs/ULTRA_FAST_MODE.md)
- **API Optimization**: [docs/API_PERFORMANCE_OPTIMIZATION.md](docs/API_PERFORMANCE_OPTIMIZATION.md)

---

**⚡⚡⚡ Develop faster with Ultra-Fast Mode! ⚡⚡⚡**
