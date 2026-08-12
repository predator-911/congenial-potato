from datetime import timedelta

from sqlalchemy.orm import Session as Db

from ..errors import error_response
from ..models.rate_limit import RateLimitEvent
from ..utils.time import utcnow


def check_rate_limit(db: Db, key: str, action: str, limit: int, window_seconds: int) -> None:
    since = utcnow() - timedelta(seconds=window_seconds)
    count = db.query(RateLimitEvent).filter(RateLimitEvent.key == key, RateLimitEvent.action == action, RateLimitEvent.created_at >= since).count()
    if count >= limit:
        raise error_response(429, "rate_limited", "Too many attempts. Please try again later.")
    db.add(RateLimitEvent(key=key, action=action)); db.commit()
