from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.constants.log_messages as log_messages
from app.core.database import get_db
from app.core.logger import logger
from app.deps.auth import get_current_user
from app.exceptions.auth import EmailAlreadyExists, InvalidPassword, InvalidUser
from app.exceptions.common import FallbackException
from app.schemas.general import UserSession
from app.schemas.requests.auth import LoginRequest, ResetPasswordRequest, SignUpRequest
from app.schemas.responses.auth import SignUpResponse, SignUpResponseData
from app.schemas.responses.common import ApiSuccessDataResponse, ApiSuccessResponse
from app.services import UserService

router = APIRouter()

@router.post("/signup")
async def signup(payload: SignUpRequest, db: Session = Depends(get_db)):
    try:
        user = UserService().create(payload, db)

        logger.info(f"User created: {user.email}")

        return SignUpResponseData(
            data=SignUpResponse(
                email=user.email,
                name=user.name,
            )
        )
    except EmailAlreadyExists as e:
        logger.info(f"User already exists: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error during user signup: {str(e)}")
        raise FallbackException(str(e))

@router.post("/login")
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    try:
        response = UserService().login(payload, db)
        return ApiSuccessDataResponse(
            data=response,
        )
    except InvalidUser as e:
        logger.error(f"Invalid user: {e}")
        raise e
    except InvalidPassword as e:
        logger.error(f"Invalid password: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error during user login: {str(e)}")
        raise FallbackException(str(e))

@router.post("/logout")
def logout(
    user_session: UserSession = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        UserService().logout(
            user_session.id,
            user_session.token,
            db
        )
        logger.info(log_messages.USER_LOGOUT.format(user_id=user_session.id))
        return ApiSuccessResponse()
    except Exception as e:
        logger.error(f"Error during user logout: {str(e)}")
        raise FallbackException(str(e))

@router.post("/reset-password")
def reset_password(
    payload: ResetPasswordRequest,
    user_session: UserSession = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        UserService().reset_password(
            user_session.id,
            payload.current_password,
            payload.new_password,
            db,
        )
        logger.info(f"Password reset: {user_session.id}")
        return ApiSuccessResponse()
    except InvalidPassword as e:
        logger.error(f"Invalid password: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error during password reset: {str(e)}")
        raise FallbackException(str(e))
