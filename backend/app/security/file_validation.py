from pathlib import Path

from .filenames import sanitize_filename
from .mime_detection import detect_file


def validate_uploaded_file(path: Path, original_name: str) -> tuple[str, str, str, str]:
    safe = sanitize_filename(original_name)
    ext = Path(safe).suffix.lower()
    mime, kind = detect_file(path, ext)
    return safe, ext, mime, kind
