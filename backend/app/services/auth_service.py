from fastapi import Request, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as Db

from ..errors import error_response
from ..models.user import User
from ..security.passwords import hash_password, verify_password
from .csrf_service import set_csrf_cookie
from .rate_limit_service import check_rate_limit
from .session_service import create_session


def _ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def register(db: Db, request: Request, response: Response, email: str, password: str) -> User:
    normalized_email = email.lower().strip()
    check_rate_limit(db, f"ip:{_ip(request)}", "register", 5, 3600)
    user = User(email=normalized_email, password_hash=hash_password(password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise error_response(
            409,
            "email_exists",
            "An account with this email already exists.",
        ) from exc
    db.refresh(user)
    create_session(db, user, response)
    set_csrf_cookie(response)
    return user


def login(db: Db, request: Request, response: Response, email: str, password: str) -> User:
    normalized_email = email.lower().strip()
    check_rate_limit(db, f"ip:{_ip(request)}:email:{normalized_email}", "login", 5, 900)
    user = db.query(User).filter(User.email == normalized_email).first()
    if not user or not verify_password(password, user.password_hash):
        raise error_response(401, "invalid_credentials", "Invalid email or password.")
    create_session(db, user, response)
    set_csrf_cookie(response)
    return user
