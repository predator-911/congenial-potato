from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class FileOut(BaseModel):
    id: str
    original_filename: str
    mime_type: str
    detected_file_type: str
    size_bytes: int
    visibility: Literal["private", "public"]
    checksum: str
    created_at: datetime
    updated_at: datetime

class FileListOut(BaseModel):
    items: list[FileOut]
    total: int
    storage_usage_bytes: int

class FilePatch(BaseModel):
    original_filename: str | None = Field(default=None, min_length=1, max_length=160)
    visibility: Literal["private", "public"] | None = None

class FileResponse(BaseModel):
    file: FileOut
