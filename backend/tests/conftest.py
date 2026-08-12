import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(monkeypatch):
    tmp = tempfile.TemporaryDirectory(); db = Path(tmp.name)/"test.sqlite3"; storage=Path(tmp.name)/"storage"
    monkeypatch.setenv("SFS_DATABASE_URL", f"sqlite:///{db}"); monkeypatch.setenv("SFS_STORAGE_ROOT", str(storage)); monkeypatch.setenv("SFS_MAX_UPLOAD_BYTES", str(2*1024*1024))
    from app.config import get_settings; get_settings.cache_clear()
    import app.database as database
    database.engine.dispose(); database.engine = database.create_engine(get_settings().database_url, connect_args={"check_same_thread": False}); database.SessionLocal.configure(bind=database.engine)
    from app.models import User  # noqa
    database.Base.metadata.create_all(bind=database.engine)
    from app.main import create_app
    with TestClient(create_app()) as c: yield c
    tmp.cleanup()

def csrf(c): return c.cookies.get("sfs_csrf")
def register(c,email="a@example.com",password="longpassword1"):
    return c.post('/api/auth/register', json={'email':email,'password':password})
def login(c,email="a@example.com",password="longpassword1"):
    return c.post('/api/auth/login', json={'email':email,'password':password})
def pdf_bytes(): return b"%PDF-1.4\n%test\n"
def upload_pdf(c,name="secret.pdf"):
    return c.post('/api/files', files={'file':(name,pdf_bytes(),'application/pdf')}, headers={'X-CSRF-Token':csrf(c)})
