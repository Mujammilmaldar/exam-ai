"""
Quick test script — run this on your server to check if Gemini API works.
Usage: python test_gemini.py
"""
from config import GEMINI_API_KEY, GEMINI_MODEL

print(f"API Key: {GEMINI_API_KEY[:10]}...{GEMINI_API_KEY[-4:]}")
print(f"Model: {GEMINI_MODEL}")
print()

# Step 1: Test import
try:
    from google import genai
    print("✅ google-genai imported OK")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("   Run: pip install google-genai")
    exit(1)

# Step 2: Test client creation
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
    print("✅ Client created OK")
except Exception as e:
    print(f"❌ Client creation failed: {e}")
    exit(1)

# Step 3: Test simple generation
print("\n🧠 Testing Gemini API call...")
try:
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents="Reply with exactly: HELLO WORKING"
    )
    print(f"✅ API response: {response.text}")
except Exception as e:
    print(f"❌ API call failed: {type(e).__name__}: {e}")
    exit(1)

# Step 4: Test code generation with JSON output
print("\n🧠 Testing code generation with JSON output...")
try:
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents='''Generate a simple Python hello world script.
Return ONLY this JSON (no markdown, no code fences):
{"files": {"hello.py": "print('Hello World')"}, "description": "hello world"}'''
    )
    print(f"✅ Raw response:\n{response.text}")

    import json
    import re
    text = response.text.strip()
    text = re.sub(r'^```(?:json)?\s*\n?', '', text)
    text = re.sub(r'\n?```\s*$', '', text)
    result = json.loads(text.strip())
    print(f"\n✅ JSON parsed OK: {list(result.keys())}")
    if "files" in result:
        print(f"✅ Files: {list(result['files'].keys())}")
    print("\n🎉 Everything is working! Your AI Practical Generator should work fine.")

except json.JSONDecodeError as e:
    print(f"⚠️ API works but JSON parsing failed: {e}")
    print("   The AI response wasn't valid JSON — this is a prompt issue, not an API issue")
except Exception as e:
    print(f"❌ Failed: {type(e).__name__}: {e}")
