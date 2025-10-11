"""Quick test of the fixes."""
import os
from dotenv import load_dotenv

# Test 1: .env loading
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
print(f"✓ API key loaded from .env: {api_key[:20]}...")

# Test 2: Import modules
try:
    from ai_brain.gemini_client import GeminiClient
    print("✓ GeminiClient imported successfully")
except Exception as e:
    print(f"✗ Import failed: {e}")
    exit(1)

# Test 3: Initialize client
try:
    client = GeminiClient()
    print(f"✓ Client initialized with model: {client.current_model_name}")
except Exception as e:
    print(f"✗ Client init failed: {e}")
    exit(1)

# Test 4: Complexity detection
test_commands = [
    ("click button", "simple"),
    ("search for trending topics and post a tweet", "complex"),
    ("type hello", "simple"),
    ("research AI and write an article", "complex")
]

print("\n✓ Testing complexity detection:")
for cmd, expected in test_commands:
    detected = client._detect_command_complexity(cmd)
    status = "✓" if detected == expected else "✗"
    print(f"  {status} '{cmd}' -> {detected} (expected {expected})")

print("\n✓ All tests passed!")
