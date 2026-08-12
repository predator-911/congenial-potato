import zipfile
from pathlib import Path

SIGNATURES = {
    ".pdf": ("application/pdf", "pdf", [b"%PDF-"]),
    ".png": ("image/png", "png", [b"\x89PNG\r\n\x1a\n"]),
    ".jpg": ("image/jpeg", "jpeg", [b"\xff\xd8\xff"]),
    ".jpeg": ("image/jpeg", "jpeg", [b"\xff\xd8\xff"]),
}


def _read_head(path: Path, limit: int = 8192) -> bytes:
    with path.open("rb") as handle:
        return handle.read(limit)


def _looks_text(data: bytes) -> bool:
    if b"\x00" in data:
        return False
    try:
        data.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def detect_file(path: Path, ext: str) -> tuple[str, str]:
    head = _read_head(path)
    if ext in SIGNATURES:
        mime, kind, sigs = SIGNATURES[ext]
        if not any(head.startswith(sig) for sig in sigs):
            raise ValueError("File signature does not match extension")
        return mime, kind
    if ext == ".docx":
        if not head.startswith(b"PK") or not zipfile.is_zipfile(path):
            raise ValueError("Invalid docx file")
        with zipfile.ZipFile(path) as zf:
            names = set(zf.namelist())
            if "[Content_Types].xml" not in names or not any(n.startswith("word/") for n in names):
                raise ValueError("Invalid docx structure")
        return "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "docx"
    if ext in {".txt", ".csv"}:
        if not _looks_text(head):
            raise ValueError("Text file contains invalid bytes")
        return ("text/csv" if ext == ".csv" else "text/plain", ext[1:])
    raise ValueError("Unsupported file extension")
