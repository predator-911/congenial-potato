from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Secure File Storage Service"
    database_url: str = "sqlite:///./secure_files.sqlite3"
    storage_root: Path = Path("../storage")
    max_upload_bytes: int = 250 * 1024 * 1024
    session_cookie_name: str = "sfs_session"
    csrf_cookie_name: str = "sfs_csrf"
    session_days: int = 7
    secure_cookies: bool = False
    frontend_origin: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_prefix="SFS_", env_file=None)

@lru_cache
def get_settings() -> Settings:
    return Settings()
