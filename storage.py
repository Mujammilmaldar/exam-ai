import os
from config import PRACTICALS_DIR


def ensure_dir():
    """Make sure the practicals directory exists."""
    os.makedirs(PRACTICALS_DIR, exist_ok=True)


def list_practicals() -> list[dict]:
    """Return list of all .py files with their content."""
    ensure_dir()
    practicals = []
    for filename in sorted(os.listdir(PRACTICALS_DIR)):
        if filename.endswith(".py"):
            filepath = os.path.join(PRACTICALS_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            practicals.append({
                "filename": filename,
                "content": content,
                "size": len(content)
            })
    return practicals


def get_practical(filename: str) -> str | None:
    """Read and return content of a specific practical file."""
    filepath = os.path.join(PRACTICALS_DIR, filename)
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def save_practical(filename: str, code: str) -> str:
    """Save code to a file and return the full path."""
    ensure_dir()
    # Sanitize filename
    filename = filename.replace(" ", "_").replace("/", "_").replace("\\", "_")
    if not filename.endswith(".py"):
        filename += ".py"
    filepath = os.path.join(PRACTICALS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    return filepath


def search_by_keyword(aim: str) -> str | None:
    """Quick keyword search across filenames."""
    aim_words = [w.lower() for w in aim.split() if len(w) > 2]
    ensure_dir()
    for filename in os.listdir(PRACTICALS_DIR):
        if filename.endswith(".py"):
            name_lower = filename.lower()
            matches = sum(1 for word in aim_words if word in name_lower)
            if matches >= 2 or (matches >= 1 and len(aim_words) <= 3):
                return filename
    return None


def delete_practical(filename: str) -> bool:
    """Delete a practical file. Returns True if deleted."""
    filepath = os.path.join(PRACTICALS_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False
