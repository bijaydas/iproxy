from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.schemas.requests.auth import SignUpRequest
from app.schemas.responses.auth import SignUpResponse, SignUpResponseData
from app.services.user import UserService
from app.exceptions.auth import EmailAlreadyExists
from app.exceptions.common import FallbackException
from app.core.database import get_db

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
