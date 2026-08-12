import os
import uuid
from pathlib import Path

from .provider import StorageProvider


class LocalStorageProvider(StorageProvider):
    def __init__(self, root: Path):
        self.root = root.resolve(); self.objects = self.root / "objects"; self.temp = self.root / "temp"
        self.objects.mkdir(parents=True, exist_ok=True); self.temp.mkdir(parents=True, exist_ok=True)
    def safe_join(self, base: Path, name: str) -> Path:
        path = (base / name).resolve()
        if base.resolve() not in path.parents and path != base.resolve():
            raise ValueError("Unsafe path")
        return path
    def temp_path(self) -> Path:
        return self.safe_join(self.temp, f"{uuid.uuid4()}.upload")
    def final_name(self, ext: str) -> str:
        return f"{uuid.uuid4()}{ext}"
    def object_path(self, storage_filename: str) -> Path:
        return self.safe_join(self.objects, storage_filename)
    def promote(self, temp: Path, storage_filename: str) -> Path:
        final = self.object_path(storage_filename); os.replace(temp, final); return final
    def delete(self, storage_filename: str) -> None:
        try: self.object_path(storage_filename).unlink()
        except FileNotFoundError: pass
    def exists(self, storage_filename: str) -> bool:
        return self.object_path(storage_filename).exists()
