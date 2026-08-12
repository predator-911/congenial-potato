import hashlib
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy import func
from sqlalchemy.orm import Session as Db

from ..config import get_settings
from ..errors import error_response
from ..models.file import StoredFile
from ..security.file_validation import validate_uploaded_file
from ..security.filenames import sanitize_filename
from ..storage.local import LocalStorageProvider

CHUNK = 1024 * 1024


def provider() -> LocalStorageProvider:
    return LocalStorageProvider(get_settings().storage_root)


def get_owned_file(db: Db, file_id: str, owner_id: str) -> StoredFile:
    file = db.query(StoredFile).filter(StoredFile.id == file_id, StoredFile.owner_id == owner_id).first()
    if not file:
        raise error_response(404, "file_not_found", "File not found.")
    return file


async def save_upload(db: Db, owner_id: str, upload: UploadFile) -> StoredFile:
    if not upload.filename:
        raise error_response(400, "missing_filename", "Uploaded file is missing a filename.")
    try:
        safe_name = sanitize_filename(upload.filename)
    except ValueError as exc:
        raise error_response(415, "invalid_filename", str(exc)) from exc

    store = provider()
    temp = store.temp_path()
    size = 0
    sha = hashlib.sha256()
    max_bytes = get_settings().max_upload_bytes
    final_written = False

    try:
        with temp.open("wb") as out:
            while True:
                chunk = await upload.read(CHUNK)
                if not chunk:
                    break
                size += len(chunk)
                if size > max_bytes:
                    raise error_response(
                        413,
                        "file_too_large",
                        "The selected file exceeds the maximum allowed size.",
                    )
                sha.update(chunk)
                out.write(chunk)

        if size == 0:
            raise error_response(422, "empty_file", "Empty files are not allowed.")

        try:
            safe_name, ext, mime, kind = validate_uploaded_file(temp, safe_name)
        except ValueError as exc:
            raise error_response(415, "unsupported_media_type", str(exc)) from exc

        storage_filename = store.final_name(ext)
        store.promote(temp, storage_filename)
        final_written = True
        row = StoredFile(
            owner_id=owner_id,
            original_filename=safe_name,
            storage_filename=storage_filename,
            storage_path=str(Path("objects") / storage_filename),
            mime_type=mime,
            detected_file_type=kind,
            size_bytes=size,
            visibility="private",
            checksum=sha.hexdigest(),
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return row
    except Exception:
        temp.unlink(missing_ok=True)
        if final_written:
            store.delete(storage_filename)
        raise


def list_files(
    db: Db,
    owner_id: str,
    search: str | None,
    visibility: str | None,
    type_: str | None,
    sort: str,
    direction: str,
):
    query = db.query(StoredFile).filter(StoredFile.owner_id == owner_id)
    if search:
        query = query.filter(StoredFile.original_filename.ilike(f"%{search}%"))
    if visibility in {"private", "public"}:
        query = query.filter(StoredFile.visibility == visibility)
    if type_:
        query = query.filter(StoredFile.detected_file_type == type_)

    sort_columns = {
        "name": StoredFile.original_filename,
        "size": StoredFile.size_bytes,
        "date": StoredFile.created_at,
    }
    column = sort_columns.get(sort, StoredFile.created_at)
    query = query.order_by(column.asc() if direction == "asc" else column.desc())
    items = query.all()
    usage = (
        db.query(func.coalesce(func.sum(StoredFile.size_bytes), 0))
        .filter(StoredFile.owner_id == owner_id)
        .scalar()
    )
    return items, len(items), int(usage or 0)
