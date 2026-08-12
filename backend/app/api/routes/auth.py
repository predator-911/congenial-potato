from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session as Db

from ...api.deps import current_user
from ...config import get_settings
from ...database import get_db
from ...models.user import User
from ...schemas.auth import AuthRequest, AuthResponse
from ...services import auth_service
from ...services.csrf_service import require_csrf
from ...services.session_service import delete_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=201)
def register(body: AuthRequest, request: Request, response: Response, db: Db = Depends(get_db)):
    user = auth_service.register(db, request, response, body.email, body.password)
    return {"user": user}


@router.post("/login", response_model=AuthResponse)
def login(body: AuthRequest, request: Request, response: Response, db: Db = Depends(get_db)):
    user = auth_service.login(db, request, response, body.email, body.password)
    return {"user": user}


@router.post("/logout", status_code=204)
def logout(request: Request, response: Response, db: Db = Depends(get_db)):
    require_csrf(request)
    settings = get_settings()
    delete_session(db, request.cookies.get(settings.session_cookie_name))
    response.delete_cookie(settings.session_cookie_name, path="/")
    response.delete_cookie(settings.csrf_cookie_name, path="/")


@router.get("/me", response_model=AuthResponse)
def me(user: User = Depends(current_user)):
    return {"user": user}
