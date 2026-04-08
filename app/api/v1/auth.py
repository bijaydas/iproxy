from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logger import logger
from app.exceptions.auth import EmailAlreadyExists, InvalidPassword, InvalidUser
from app.exceptions.common import FallbackException
from app.schemas.requests.auth import LoginRequest, SignUpRequest
from app.schemas.responses.auth import SignUpResponse, SignUpResponseData
from app.schemas.responses.common import ApiSuccessDataResponse
from app.services.user import UserService

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
