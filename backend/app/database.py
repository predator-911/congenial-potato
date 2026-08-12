from collections.abc import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import get_settings


class Base(DeclarativeBase):
    pass

engine = create_engine(get_settings().database_url, connect_args={"check_same_thread": False} if get_settings().database_url.startswith("sqlite") else {})

@event.listens_for(engine, "connect")
def _fk_on(dbapi_connection, _):
    cur = dbapi_connection.cursor(); cur.execute("PRAGMA foreign_keys=ON"); cur.close()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
