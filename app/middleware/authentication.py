import jwt
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.configs import settings
from app.core.responses import response as response_error


EXCLUDE_PATHS = [
    "/docs", "/health", "/openapi.json", "/users"
]

class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if any(path.startswith(p) for p in EXCLUDE_PATHS):
            response = await call_next(request)
            return response

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return response_error("missing or invalid authorization header", 401, status="error")

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, settings.jwt_token.SECRET_KEY, algorithms=[settings.jwt_token.ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                return response_error("invalid token payload", 401, status="error")
        except jwt.PyJWTError:
            return response_error("invalid token", 401, status="error")

        response = await call_next(request)
        return response