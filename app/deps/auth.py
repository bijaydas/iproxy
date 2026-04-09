from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

import app.constants.log_messages as log_messages
from app.core.database import get_db
from app.core.logger import logger
from app.exceptions.auth import InvalidToken, Unauthorized
from app.schemas.general import UserSession
from app.services import JWTService, UserService
from app.utils.general import get_headers

bearer_schema = HTTPBearer()

def get_current_user(
    request: Request,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
    db: Session = Depends(get_db)
):
    request_data = get_headers(request)
    token = auth.credentials
    try:
        jwt_token = JWTService().verify(token)
        user_service = UserService()

        """Check if user is valid"""
        user = user_service.get_profile(jwt_token["email"], db)

        """Check if user is logged in"""
        user_service.is_logged_in(user.id, token, db)

        """Check if user is active"""
        if not user_service.is_active(user):
            logger.info(log_messages.AUTH_USER_INACTIVE.format(user_id=user.id, status=user.status))
            raise Unauthorized()

        return UserSession(
            id=str(user.id),
            email=jwt_token["email"],
            token=token,
        )
    except Unauthorized as e:
        logger.error("Unauthorized", exc_info=True, extra=request_data)
        raise Unauthorized(str(e))
    except Exception as e:
        logger.error(e, exc_info=True, extra=request_data)
        raise InvalidToken()
