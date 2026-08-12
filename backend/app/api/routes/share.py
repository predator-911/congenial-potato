from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session as Db

from ...database import get_db
from ...schemas.share import PublicFileOut
from ...services.file_service import provider
from ...services.share_service import public_file_for_token

router = APIRouter(prefix="/share", tags=["share"])
@router.get("/{token}", response_model=PublicFileOut)
def meta(token: str, db: Db=Depends(get_db)):
    f=public_file_for_token(db, token); return {"original_filename":f.original_filename,"mime_type":f.mime_type,"detected_file_type":f.detected_file_type,"size_bytes":f.size_bytes,"created_at":f.created_at,"download_url":f"/api/share/{token}/download"}
@router.get("/{token}/download")
def download(token: str, db: Db=Depends(get_db)):
    f=public_file_for_token(db, token); return FileResponse(provider().object_path(f.storage_filename), media_type=f.mime_type, filename=f.original_filename, headers={"X-Content-Type-Options":"nosniff","Content-Length":str(f.size_bytes)})
