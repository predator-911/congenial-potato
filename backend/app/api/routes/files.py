from fastapi import APIRouter, Depends, Request, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session as Db

from ...api.deps import current_user
from ...database import get_db
from ...models.user import User
from ...schemas.files import FileListOut, FilePatch
from ...schemas.files import FileResponse as FileBody
from ...schemas.share import ShareCreate, ShareResponse
from ...security.filenames import sanitize_filename
from ...services.csrf_service import require_csrf
from ...services.file_service import get_owned_file, list_files, provider, save_upload
from ...services.share_service import create_share, revoke_shares
from ...utils.time import utcnow

router = APIRouter(prefix="/files", tags=["files"])


@router.get("", response_model=FileListOut)
def files(
    search: str | None = None,
    visibility: str | None = None,
    type: str | None = None,
    sort: str = "date",
    direction: str = "desc",
    db: Db = Depends(get_db),
    user: User = Depends(current_user),
):
    items, total, usage = list_files(db, user.id, search, visibility, type, sort, direction)
    return {"items": items, "total": total, "storage_usage_bytes": usage}


@router.post("", response_model=FileBody, status_code=201)
async def upload(
    request: Request,
    file: UploadFile,
    db: Db = Depends(get_db),
    user: User = Depends(current_user),
):
    require_csrf(request)
    return {"file": await save_upload(db, user.id, file)}


@router.get("/{file_id}", response_model=FileBody)
def get_file(file_id: str, db: Db = Depends(get_db), user: User = Depends(current_user)):
    return {"file": get_owned_file(db, file_id, user.id)}


@router.patch("/{file_id}", response_model=FileBody)
def patch_file(
    file_id: str,
    body: FilePatch,
    request: Request,
    db: Db = Depends(get_db),
    user: User = Depends(current_user),
):
    require_csrf(request)
    file = get_owned_file(db, file_id, user.id)
    if body.original_filename is not None:
        file.original_filename = sanitize_filename(body.original_filename)
    if body.visibility is not None:
        file.visibility = body.visibility
    file.updated_at = utcnow()
    db.commit()
    db.refresh(file)
    return {"file": file}


@router.delete("/{file_id}", status_code=204)
def delete_file(
    file_id: str,
    request: Request,
    db: Db = Depends(get_db),
    user: User = Depends(current_user),
):
    require_csrf(request)
    file = get_owned_file(db, file_id, user.id)
    provider().delete(file.storage_filename)
    db.delete(file)
    db.commit()


@router.get("/{file_id}/download")
def download(file_id: str, db: Db = Depends(get_db), user: User = Depends(current_user)):
    file = get_owned_file(db, file_id, user.id)
    path = provider().object_path(file.storage_filename)
    return FileResponse(
        path,
        media_type=file.mime_type,
        filename=file.original_filename,
        headers={"X-Content-Type-Options": "nosniff", "Content-Length": str(file.size_bytes)},
    )


@router.post("/{file_id}/share", response_model=ShareResponse, status_code=201)
def share(
    file_id: str,
    body: ShareCreate,
    request: Request,
    db: Db = Depends(get_db),
    user: User = Depends(current_user),
):
    require_csrf(request)
    file = get_owned_file(db, file_id, user.id)
    link, url = create_share(db, file, body.expires_at, request)
    return {"share": {"url": url, "expires_at": link.expires_at, "created_at": link.created_at}}


@router.delete("/{file_id}/share", status_code=204)
def unshare(
    file_id: str,
    request: Request,
    db: Db = Depends(get_db),
    user: User = Depends(current_user),
):
    require_csrf(request)
    file = get_owned_file(db, file_id, user.id)
    revoke_shares(db, file)
