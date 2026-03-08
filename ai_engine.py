import json
import re
import time
import logging
from config import (
    AI_PROVIDER, GEMINI_API_KEY, GEMINI_MODEL,
    GROQ_API_KEY, GROQ_MODEL, MAX_FILES
)
from prompts import GENERATE_PROMPT, SEARCH_PROMPT, UPDATE_PROMPT

logger = logging.getLogger("ai_engine")
logging.basicConfig(level=logging.INFO)

# ── Initialize AI client based on provider ──
client = None

if AI_PROVIDER == "gemini":
    from google import genai
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_api_key_here":
        logger.error("❌ GEMINI_API_KEY is not set! Edit your .env file.")
    else:
        client = genai.Client(api_key=GEMINI_API_KEY)
        logger.info(f"✅ Gemini loaded: {GEMINI_API_KEY[:8]}... | model: {GEMINI_MODEL}")

elif AI_PROVIDER == "groq":
    from groq import Groq
    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_key_here":
        logger.error("❌ GROQ_API_KEY is not set! Edit your .env file.")
    else:
        client = Groq(api_key=GROQ_API_KEY)
        logger.info(f"✅ Groq loaded: {GROQ_API_KEY[:8]}... | model: {GROQ_MODEL}")

else:
    logger.error(f"❌ Unknown AI_PROVIDER: {AI_PROVIDER}. Use 'gemini' or 'groq'.")


# ── Retry config ──
MAX_RETRIES = 3
RETRY_DELAYS = [5, 10, 20]


def _call_ai(prompt: str, label: str = "API") -> str:
    """Call AI provider with automatic retry on rate limit errors."""
    if client is None:
        raise Exception("AI client not initialized. Check your .env file.")

    for attempt in range(MAX_RETRIES):
        try:
            if AI_PROVIDER == "gemini":
                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt
                )
                return response.text

            elif AI_PROVIDER == "groq":
                response = client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=4096
                )
                return response.choices[0].message.content

        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "rate_limit" in error_str.lower():
                delay = RETRY_DELAYS[min(attempt, len(RETRY_DELAYS) - 1)]
                logger.warning(f"⏳ {label}: Rate limited. Retry {attempt+1}/{MAX_RETRIES} in {delay}s...")
                time.sleep(delay)
            else:
                logger.error(f"❌ {label}: API failed: {type(e).__name__}: {e}")
                raise

    raise Exception(f"{label}: Rate limit exceeded after {MAX_RETRIES} retries. Try again later.")


def _clean_json_response(text: str) -> str:
    """Remove markdown code fences and clean up JSON response."""
    text = text.strip()
    text = re.sub(r'^```(?:json)?\s*\n?', '', text)
    text = re.sub(r'\n?```\s*$', '', text)
    return text.strip()


def _parse_json(text: str) -> dict:
    """Parse JSON from AI response, handling common issues."""
    cleaned = _clean_json_response(text)

    # Try parsing methods in order of strictness
    for attempt_text in [cleaned]:
        # 1. Normal parse
        try:
            return json.loads(attempt_text)
        except json.JSONDecodeError:
            pass

        # 2. Lenient parse (allows newlines in strings — common with code)
        try:
            return json.loads(attempt_text, strict=False)
        except json.JSONDecodeError:
            pass

        # 3. Extract JSON object from text
        match = re.search(r'\{[\s\S]*\}', attempt_text)
        if match:
            try:
                return json.loads(match.group(), strict=False)
            except json.JSONDecodeError:
                pass

    logger.warning(f"JSON parse failed for: {cleaned[:300]}")
    raise ValueError(f"Could not parse JSON from AI response:\n{text[:500]}")


def generate_practical(aim: str) -> dict:
    """Generate new practical code from an aim."""
    logger.info(f"🧠 GENERATE [{AI_PROVIDER}]: aim='{aim}'")
    prompt = GENERATE_PROMPT.format(aim=aim, max_files=MAX_FILES)

    response_text = _call_ai(prompt, "GENERATE")
    logger.info(f"📥 Response: {len(response_text)} chars")

    result = _parse_json(response_text)

    if "files" not in result:
        logger.error(f"❌ Missing 'files' key. Keys: {list(result.keys())}")
        raise ValueError("AI response missing 'files' key")

    logger.info(f"✅ Generated {len(result['files'])} file(s): {list(result['files'].keys())}")
    return result


def search_matching_practical(aim: str, practicals: list[dict]) -> dict:
    """Semantically match an aim to existing practicals."""
    logger.info(f"🔍 SEARCH [{AI_PROVIDER}]: aim='{aim}' among {len(practicals)} files")

    practicals_text = ""
    for p in practicals:
        preview = "\n".join(p["content"].split("\n")[:30])
        practicals_text += f"\n--- {p['filename']} ---\n{preview}\n"

    prompt = SEARCH_PROMPT.format(aim=aim, practicals_list=practicals_text)

    response_text = _call_ai(prompt, "SEARCH")
    logger.info(f"📥 Search response: {response_text[:200]}")

    result = _parse_json(response_text)
    logger.info(f"✅ Match: {result.get('match')}, confidence: {result.get('confidence')}")
    return result


def update_practical(aim: str, existing_code: str) -> dict:
    """Update existing code to match an aim."""
    logger.info(f"✏️ UPDATE [{AI_PROVIDER}]: aim='{aim}'")
    prompt = UPDATE_PROMPT.format(aim=aim, existing_code=existing_code)

    response_text = _call_ai(prompt, "UPDATE")
    logger.info(f"📥 Update: {len(response_text)} chars")

    result = _parse_json(response_text)
    logger.info(f"✅ Updated: {result.get('updated')}, changes: {result.get('changes', '')[:100]}")
    return result
