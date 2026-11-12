from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt

from app.core.config import settings


def create_access_token(subject: str, claims: dict[str, Any] | None = None) -> str:
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "exp": expires_at, **(claims or {})}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
