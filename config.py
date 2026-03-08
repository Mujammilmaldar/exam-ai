import os
from dotenv import load_dotenv

load_dotenv()

# AI Provider: "gemini" or "groq"
AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")

# Google Gemini settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Groq settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Directory where practicals are stored
PRACTICALS_DIR = os.getenv("PRACTICALS_DIR", os.path.join(os.path.dirname(__file__), "practicals"))

# Max files AI can generate per request
MAX_FILES = int(os.getenv("MAX_FILES", "10"))
