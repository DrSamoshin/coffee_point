import jwt
import logging
from datetime import datetime, timedelta, timezone
from app.core.configs import settings


def create_access_token(subject: str, expires_delta: timedelta = timedelta(days=300)):
    to_encode = {"sub": subject, "exp": datetime.now(timezone.utc) + expires_delta}
    encoded_jwt = jwt.encode(payload=to_encode, key=settings.jwt_token.JWT_SECRET_KEY, algorithm=settings.jwt_token.ALGORITHM)
    return encoded_jwt

if __name__ == "__main__":
    user_id = input("user_id: ")
    logging.info(settings.jwt_token.JWT_SECRET_KEY)
    token = create_access_token(subject=user_id)
    logging.info(token)