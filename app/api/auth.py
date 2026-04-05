from fastapi import APIRouter

from app.core.logger import logger
from app.schemas.requests.auth import SignUpRequest
from app.schemas.responses.auth import SignUpResponse, SignUpResponseData
from app.services.user import UserService
from app.exceptions.auth import EmailAlreadyExists
from app.exceptions.common import FallbackException

router = APIRouter()

@router.post("/signup")
async def signup(payload: SignUpRequest):
    try:
        user = UserService().create(payload)
        response_data = SignUpResponse(email=user.email)
        logger.info(f"User created: {user.email}")
        return SignUpResponseData(data=response_data)
    except EmailAlreadyExists as e:
        logger.info(f"User already exists: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error during user signup: {str(e)}")
        raise FallbackException(str(e))
