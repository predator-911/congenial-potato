from app.database import SessionLocal
from app.models.session import Session
from app.utils.time import utcnow

from .conftest import register


def test_expired_session_rejected(client):
    register(client)
    db=SessionLocal(); s=db.query(Session).first(); s.expires_at=utcnow(); db.commit(); db.close()
    assert client.get('/api/auth/me').status_code==401
