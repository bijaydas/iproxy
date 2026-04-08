from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.constants.log_messages as log_messages
from app.core.database import get_db
from app.core.logger import logger
from app.deps.auth import get_current_user
from app.schemas.general import UserSession
from app.schemas.responses.common import ApiErrorResponse, ApiSuccessDataResponse
from app.schemas.responses.user import UserProfile
from app.services import UserService

router = APIRouter()

@router.get("/")
def get_profile(
    user_session: UserSession = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        user = UserService.get_profile(
            user_session.email,
            db,
        )

        user_data = UserProfile(email=user.email, name=user.name)

        logger.info(log_messages.PROFILE_VIEWED.format(user_id=user.id))

        return ApiSuccessDataResponse(data=user_data.model_dump())
    except Exception as e:
        logger.error(e, exc_info=True)
        return ApiErrorResponse()
