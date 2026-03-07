import os
from dotenv import load_dotenv

load_dotenv()

# Google Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Directory where practicals are stored
PRACTICALS_DIR = os.getenv("PRACTICALS_DIR", os.path.join(os.path.dirname(__file__), "practicals"))

# Max files Gemini can generate per request
MAX_FILES = int(os.getenv("MAX_FILES", "10"))

# Gemini model to use
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
