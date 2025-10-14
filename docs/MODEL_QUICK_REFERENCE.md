# Model Selection - Quick Reference

## 🎯 One Rule to Remember

**DEV MODE = NO PRO MODEL**

## 📊 Quick Matrix

```
┌─────────────┬─────────────┬──────────────────────────┬────────┐
│ Mode        │ Task Type   │ Model Used               │ Speed  │
├─────────────┼─────────────┼──────────────────────────┼────────┤
│ Dev         │ Simple      │ gemini-flash-lite-latest │ ⚡⚡⚡   │
│ Dev         │ Complex     │ gemini-2.5-flash         │ ⚡⚡    │
│ Normal      │ Simple      │ gemini-2.5-flash         │ ⚡⚡    │
│ Normal      │ Complex     │ gemini-2.5-pro           │ ⚡     │
└─────────────┴─────────────┴──────────────────────────┴────────┘
```

## 🚀 Quick Commands

### Start Dev Mode (Fast)
```bash
start_dev_mode.bat
```

### Start Normal Mode (Quality)
```bash
run.bat
```

## 👀 What You'll See

### Dev Mode
```
⚡⚡⚡ DEV MODE - Simple task: Using gemini-flash-lite-latest
⚡⚡ DEV MODE - Complex task: Using gemini-2.5-flash
```

### Normal Mode
```
Switched to simple model: gemini-2.5-flash
Switched to complex model: gemini-2.5-pro
```

## ✅ Correct / ❌ Wrong

### ✅ Correct
```
Dev + Simple  → gemini-flash-lite-latest  ✅
Dev + Complex → gemini-2.5-flash          ✅
Normal + Simple  → gemini-2.5-flash       ✅
Normal + Complex → gemini-2.5-pro         ✅
```

### ❌ Wrong
```
Dev + Complex → gemini-2.5-pro            ❌ NEVER!
```

## 📈 Speed Comparison

```
Dev Mode:    2-4 seconds   ⚡⚡⚡ (no pro)
Normal Mode: 6-12 seconds  ⚡   (with pro)

Dev is 3-4x faster!
```

## 🎓 Remember

- 🚀 **Dev** = Speed (no pro)
- 🎯 **Normal** = Quality (with pro)
- ⚡⚡⚡ Ultra-fast for dev simple
- ⚡⚡ Fast for dev complex
- ⚡ Pro for normal complex only

---

**Rule**: Dev mode NEVER uses gemini-2.5-pro  
**Why**: Speed > Quality during development  
**Benefit**: 3-4x faster iteration
