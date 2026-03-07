import json
import re
from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL, MAX_FILES
from prompts import GENERATE_PROMPT, SEARCH_PROMPT, UPDATE_PROMPT

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


def _clean_json_response(text: str) -> str:
    """Remove markdown code fences and clean up JSON response from Gemini."""
    # Remove ```json ... ``` or ``` ... ``` wrappers
    text = text.strip()
    text = re.sub(r'^```(?:json)?\s*\n?', '', text)
    text = re.sub(r'\n?```\s*$', '', text)
    return text.strip()


def _parse_json(text: str) -> dict:
    """Parse JSON from Gemini response, handling common issues."""
    cleaned = _clean_json_response(text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
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
    prompt = GENERATE_PROMPT.format(aim=aim, max_files=MAX_FILES)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    result = _parse_json(response.text)

    # Validate structure
    if "files" not in result:
        raise ValueError("Gemini response missing 'files' key")

    return result


def search_matching_practical(aim: str, practicals: list[dict]) -> dict:
    """
    Use Gemini to semantically match an aim to existing practicals.
    Returns: {"match": "filename.py or NONE", "confidence": 0.0-1.0, "reason": "..."}
    """
    # Build practicals list string
    practicals_text = ""
    for p in practicals:
        # Send first 30 lines of each file for context
        preview = "\n".join(p["content"].split("\n")[:30])
        practicals_text += f"\n--- {p['filename']} ---\n{preview}\n"

    prompt = SEARCH_PROMPT.format(aim=aim, practicals_list=practicals_text)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return _parse_json(response.text)


def update_practical(aim: str, existing_code: str) -> dict:
    """
    Ask Gemini to update existing code to match an aim.
    Returns: {"updated": bool, "code": "...", "changes": "..."}
    """
    prompt = UPDATE_PROMPT.format(aim=aim, existing_code=existing_code)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return _parse_json(response.text)
