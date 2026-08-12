import re
import unicodedata
from pathlib import PurePath

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".txt", ".csv", ".docx"}
DANGEROUS_EXTENSIONS = {".exe", ".bat", ".cmd", ".com", ".sh", ".php", ".js", ".html", ".svg", ".msi", ".dll", ".ps1"}
SAFE_NAME = re.compile(r"[^A-Za-z0-9._ -]")

def sanitize_filename(name: str) -> str:
    if not name or "\x00" in name:
        raise ValueError("Invalid filename")
    if name.startswith(("/", "\\")) or ".." in PurePath(name).parts or "/" in name or "\\" in name:
        raise ValueError("Path components are not allowed")
    base = unicodedata.normalize("NFKC", PurePath(name).name).strip().strip(".")
    if not base or base.startswith("."):
        raise ValueError("Hidden or empty filenames are not allowed")
    base = SAFE_NAME.sub("_", base)[:160]
    parts = [p.lower() for p in PurePath(base).suffixes]
    if not parts or parts[-1] not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file extension")
    if any(ext in DANGEROUS_EXTENSIONS for ext in parts[:-1]):
        raise ValueError("Dangerous double extension")
    if len(parts) > 1 and parts[-2] not in {".tar"} and parts[-2] not in ALLOWED_EXTENSIONS:
        raise ValueError("Suspicious double extension")
    return base
