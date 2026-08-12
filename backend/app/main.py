from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import app.models  # noqa: F401

from .api.routes import auth, files, health, share
from .config import get_settings
from .database import Base, engine
from .errors import install_error_handlers


def create_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)
    app = FastAPI(title=get_settings().app_name)
    app.add_middleware(CORSMiddleware, allow_origins=[get_settings().frontend_origin], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    install_error_handlers(app)
    app.include_router(health.router, prefix="/api")
    app.include_router(auth.router, prefix="/api")
    app.include_router(files.router, prefix="/api")
    app.include_router(share.router, prefix="/api")
    static = Path(__file__).resolve().parents[2] / "frontend_dist"
    if static.exists(): app.mount("/", StaticFiles(directory=static, html=True), name="frontend")
    return app
app = create_app()
