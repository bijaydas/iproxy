from datetime import UTC, datetime, timedelta

import jwt

from app.core.settings import settings


class JWTService:
    def __init__(self):
        self.secret = settings.JWT_SECRET_KEY

    def create_access_token(self, user_id: str, extra_data=None):
        if extra_data is None:
            extra_data = {}

        payload = {
            "sub": user_id,
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
            **extra_data,
        }

        return jwt.encode(payload, self.secret, algorithm=settings.JWT_ALGORITHM)

    def verify(self, token: str):
        try:
            return jwt.decode(token, self.secret, algorithms=[settings.JWT_ALGORITHM])
        except Exception as e:
            raise e
