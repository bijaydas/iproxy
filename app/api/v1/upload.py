from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logger import logger
from app.deps.auth import get_current_user
from app.schemas.general import UserSession
from app.schemas.responses.common import ApiErrorResponse, ApiSuccessResponse
from app.services import UploadService

router = APIRouter()


@router.post("/job-description")
def upload_job_description(
    file: UploadFile = File(...),
    session: UserSession = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        upload_service = UploadService()
        upload = upload_service.job_description(file, int(session.id), db)

        print(upload)

        return ApiSuccessResponse()
    except Exception as e:
        logger.error(e)
        return ApiErrorResponse(error=str(e))
