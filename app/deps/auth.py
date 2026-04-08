from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.logger import logger
from app.exceptions.auth import InvalidToken, Unauthorized
from app.schemas.general import UserSession
from app.services import JWTService
from app.utils.general import get_headers

bearer_schema = HTTPBearer()

def get_current_user(
    request: Request,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema)
):
    request_data = get_headers(request)
    try:
        jwt_token = JWTService().verify(auth.credentials)
        return UserSession(email=jwt_token["email"])
    except Unauthorized:
        logger.error("Unauthorized", exc_info=True, extra=request_data)
        raise Unauthorized()
    except Exception as e:
        logger.error(e, exc_info=True, extra=request_data)
        raise InvalidToken()
