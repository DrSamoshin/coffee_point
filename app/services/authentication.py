import logging
import jwt

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.configs import settings

async def get_user_id_from_token(credential: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> str:
    token = credential.credentials
    try:
        payload = jwt.decode(token, settings.jwt_token.SECRET_KEY, algorithms=[settings.jwt_token.ALGORITHM])
        user_id = payload.get("sub")
        logging.info(f"user_id: {user_id}")
    except Exception as error:
        raise HTTPException(status_code=401, detail=str(error))
    else:
        return user_id

