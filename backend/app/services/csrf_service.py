from fastapi import Request, Response

from ..config import get_settings
from ..errors import error_response
from ..security.tokens import new_token


def set_csrf_cookie(response: Response) -> str:
    token = new_token(); s = get_settings()
    response.set_cookie(s.csrf_cookie_name, token, httponly=False, samesite="lax", secure=s.secure_cookies, path="/")
    return token

def require_csrf(request: Request) -> None:
    if request.method in {"GET", "HEAD", "OPTIONS"}: return
    s = get_settings(); cookie = request.cookies.get(s.csrf_cookie_name); header = request.headers.get("x-csrf-token")
    if not cookie or not header or cookie != header:
        raise error_response(403, "csrf_failed", "CSRF validation failed.")
