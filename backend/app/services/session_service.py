from fastapi import Response
from sqlalchemy.orm import Session as Db

from ..config import get_settings
from ..models.session import Session
from ..models.user import User
from ..security.tokens import new_token, token_hash
from ..utils.time import days_from_now, utcnow


def create_session(db: Db, user: User, response: Response) -> str:
    settings = get_settings(); raw = new_token()
    sess = Session(user_id=user.id, token_hash=token_hash(raw), expires_at=days_from_now(settings.session_days))
    db.add(sess); db.commit()
    response.set_cookie(settings.session_cookie_name, raw, httponly=True, samesite="lax", secure=settings.secure_cookies, max_age=settings.session_days*86400, path="/")
    return raw

def get_user_for_token(db: Db, raw: str | None) -> User | None:
    if not raw: return None
    sess = db.query(Session).filter(Session.token_hash == token_hash(raw), Session.expires_at > utcnow()).first()
    if not sess: return None
    return db.get(User, sess.user_id)

def delete_session(db: Db, raw: str | None) -> None:
    if raw:
        db.query(Session).filter(Session.token_hash == token_hash(raw)).delete(); db.commit()
