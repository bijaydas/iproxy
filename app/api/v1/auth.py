from fastapi import APIRouter

from app.core.logger import logger
from app.schemas.requests.auth import SignUpRequest
from app.schemas.responses.auth import SignUpResponse, SignUpResponseData
from app.schemas.responses.common import ApiErrorResponse
from app.services.user import UserService

router = APIRouter()

@router.post("/signup")
async def signup(payload: SignUpRequest):
    try:
        user = UserService().create(payload)
        response_data = SignUpResponse(email=user.email)
        logger.info(f"User created successfully: {user.email}")
        return SignUpResponseData(data=response_data)
    except Exception as e:
        logger.error(f"Error during user signup: {str(e)}")
        return ApiErrorResponse(message=str(e))
