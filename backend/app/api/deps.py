from fastapi import Depends, Request
from sqlalchemy.orm import Session as Db

from ..config import get_settings
from ..database import get_db
from ..errors import error_response
from ..models.user import User
from ..services.session_service import get_user_for_token


def current_user(request: Request, db: Db = Depends(get_db)) -> User:
    user = get_user_for_token(db, request.cookies.get(get_settings().session_cookie_name))
    if not user:
        raise error_response(401, "unauthorized", "Authentication required.")
    return user
