from fastapi import Request
from sqlalchemy.orm import Session as Db

from ..errors import error_response
from ..models.file import StoredFile
from ..models.share_link import ShareLink
from ..security.tokens import new_token, token_hash
from ..utils.time import utcnow


def create_share(db: Db, file: StoredFile, expires_at, request: Request):
    if file.visibility != "public": raise error_response(409, "file_private", "Make the file public before creating a share link.")
    raw = new_token(); link = ShareLink(file_id=file.id, token_hash=token_hash(raw), expires_at=expires_at)
    db.add(link); db.commit(); db.refresh(link)
    origin = str(request.base_url).rstrip("/")
    return link, f"{origin}/share/{raw}"

def revoke_shares(db: Db, file: StoredFile) -> None:
    for link in db.query(ShareLink).filter(ShareLink.file_id == file.id, ShareLink.revoked_at.is_(None)).all():
        link.revoked_at = utcnow()
    db.commit()

def public_file_for_token(db: Db, token: str) -> StoredFile:
    link = db.query(ShareLink).filter(ShareLink.token_hash == token_hash(token), ShareLink.revoked_at.is_(None)).first()
    if not link or (link.expires_at and link.expires_at <= utcnow()):
        raise error_response(404, "share_not_found", "Share link not found.")
    file = db.get(StoredFile, link.file_id)
    if not file or file.visibility != "public": raise error_response(404, "share_not_found", "Share link not found.")
    return file
