"""
Quick test script — run on server to check if AI provider works.
Usage: python test_gemini.py
"""
from config import AI_PROVIDER, GEMINI_API_KEY, GEMINI_MODEL, GROQ_API_KEY, GROQ_MODEL

print(f"Provider: {AI_PROVIDER}")
if AI_PROVIDER == "gemini":
    print(f"API Key: {GEMINI_API_KEY[:10]}...{GEMINI_API_KEY[-4:]}")
    print(f"Model: {GEMINI_MODEL}")
elif AI_PROVIDER == "groq":
    print(f"API Key: {GROQ_API_KEY[:10]}...{GROQ_API_KEY[-4:]}")
    print(f"Model: {GROQ_MODEL}")
print()

# ── Test based on provider ──
if AI_PROVIDER == "gemini":
    try:
        from google import genai
        print("✅ google-genai imported OK")
        client = genai.Client(api_key=GEMINI_API_KEY)
        print("✅ Client created OK")
        print("\n🧠 Testing API call...")
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents="Reply with exactly: HELLO WORKING"
        )
        print(f"✅ Response: {response.text}")
    except Exception as e:
        print(f"❌ Failed: {type(e).__name__}: {e}")

elif AI_PROVIDER == "groq":
    try:
        from groq import Groq
        print("✅ groq imported OK")
        client = Groq(api_key=GROQ_API_KEY)
        print("✅ Client created OK")
        print("\n🧠 Testing API call...")
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": "Reply with exactly: HELLO WORKING"}],
            max_tokens=50
        )
        print(f"✅ Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ Failed: {type(e).__name__}: {e}")

# ── Test JSON generation ──
print("\n🧠 Testing code generation with JSON output...")
try:
    test_prompt = '''Generate a simple Python hello world script.
Return ONLY this JSON (no markdown, no code fences):
{"files": {"hello.py": "print('Hello World')"}, "description": "hello world"}'''

    if AI_PROVIDER == "gemini":
        response = client.models.generate_content(model=GEMINI_MODEL, contents=test_prompt)
        text = response.text
    elif AI_PROVIDER == "groq":
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": test_prompt}],
            max_tokens=200
        )
        text = response.choices[0].message.content

    print(f"✅ Raw response:\n{text}")

    import json, re
    text = text.strip()
    text = re.sub(r'^```(?:json)?\s*\n?', '', text)
    text = re.sub(r'\n?```\s*$', '', text)
    result = json.loads(text.strip())
    print(f"\n✅ JSON parsed OK: {list(result.keys())}")
    print("\n🎉 Everything is working! Your AI Practical Generator should work fine.")

except Exception as e:
    print(f"❌ Failed: {type(e).__name__}: {e}")
