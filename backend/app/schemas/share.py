from datetime import datetime

from pydantic import BaseModel


class ShareCreate(BaseModel):
    expires_at: datetime | None = None

class ShareOut(BaseModel):
    url: str
    expires_at: datetime | None
    created_at: datetime

class ShareResponse(BaseModel):
    share: ShareOut

class PublicFileOut(BaseModel):
    original_filename: str
    mime_type: str
    detected_file_type: str
    size_bytes: int
    created_at: datetime
    download_url: str
