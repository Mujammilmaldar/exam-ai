import json
import re
import logging
from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL, MAX_FILES
from prompts import GENERATE_PROMPT, SEARCH_PROMPT, UPDATE_PROMPT

logger = logging.getLogger("ai_engine")
logging.basicConfig(level=logging.INFO)

# Initialize Gemini client
if not GEMINI_API_KEY or GEMINI_API_KEY == "your_api_key_here":
    logger.error("❌ GEMINI_API_KEY is not set! Edit your .env file.")
else:
    logger.info(f"✅ Gemini API Key loaded: {GEMINI_API_KEY[:8]}...")
    logger.info(f"✅ Using model: {GEMINI_MODEL}")

client = genai.Client(api_key=GEMINI_API_KEY)


def _clean_json_response(text: str) -> str:
    """Remove markdown code fences and clean up JSON response from Gemini."""
    text = text.strip()
    # Remove ```json ... ``` or ``` ... ``` wrappers
    text = re.sub(r'^```(?:json)?\s*\n?', '', text)
    text = re.sub(r'\n?```\s*$', '', text)
    return text.strip()


def _parse_json(text: str) -> dict:
    """Parse JSON from Gemini response, handling common issues."""
    cleaned = _clean_json_response(text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        logger.warning(f"Direct JSON parse failed: {e}")
        logger.warning(f"Cleaned text (first 300 chars): {cleaned[:300]}")
        # Try to find JSON object in the text
        match = re.search(r'\{[\s\S]*\}', cleaned)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        raise ValueError(f"Could not parse JSON from Gemini response:\n{text[:500]}")


def generate_practical(aim: str) -> dict:
    """
    Generate new practical code from an aim using Gemini.
    Returns: {"files": {"filename.py": "code"}, "description": "..."}
    """
    logger.info(f"🧠 GENERATE: aim='{aim}'")
    prompt = GENERATE_PROMPT.format(aim=aim, max_files=MAX_FILES)

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        logger.info(f"📥 Gemini response length: {len(response.text)} chars")
        logger.info(f"📥 Response preview: {response.text[:200]}...")
    except Exception as e:
        logger.error(f"❌ Gemini API call failed: {type(e).__name__}: {e}")
        raise

    result = _parse_json(response.text)

    # Validate structure
    if "files" not in result:
        logger.error(f"❌ Response missing 'files' key. Keys found: {list(result.keys())}")
        raise ValueError("Gemini response missing 'files' key")

    logger.info(f"✅ Generated {len(result['files'])} file(s): {list(result['files'].keys())}")
    return result


def search_matching_practical(aim: str, practicals: list[dict]) -> dict:
    """
    Use Gemini to semantically match an aim to existing practicals.
    Returns: {"match": "filename.py or NONE", "confidence": 0.0-1.0, "reason": "..."}
    """
    logger.info(f"🔍 SEARCH: aim='{aim}' among {len(practicals)} practicals")

    practicals_text = ""
    for p in practicals:
        preview = "\n".join(p["content"].split("\n")[:30])
        practicals_text += f"\n--- {p['filename']} ---\n{preview}\n"

    prompt = SEARCH_PROMPT.format(aim=aim, practicals_list=practicals_text)

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        logger.info(f"📥 Search response: {response.text[:200]}")
    except Exception as e:
        logger.error(f"❌ Search API call failed: {type(e).__name__}: {e}")
        raise

    result = _parse_json(response.text)
    logger.info(f"✅ Search result: match={result.get('match')}, confidence={result.get('confidence')}")
    return result


def update_practical(aim: str, existing_code: str) -> dict:
    """
    Ask Gemini to update existing code to match an aim.
    Returns: {"updated": bool, "code": "...", "changes": "..."}
    """
    logger.info(f"✏️ UPDATE: aim='{aim}', code_length={len(existing_code)}")
    prompt = UPDATE_PROMPT.format(aim=aim, existing_code=existing_code)

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        logger.info(f"📥 Update response length: {len(response.text)} chars")
    except Exception as e:
        logger.error(f"❌ Update API call failed: {type(e).__name__}: {e}")
        raise

    result = _parse_json(response.text)
    logger.info(f"✅ Update result: updated={result.get('updated')}, changes={result.get('changes', '')[:100]}")
    return result
