from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logger import logger
from app.deps.auth import get_current_user
from app.schemas.general import UserSession
from app.schemas.responses.common import ApiErrorResponse, ApiSuccessResponse
from app.services import ChromaDBService, UploadService

router = APIRouter()


@router.post("/job-description")
def upload_job_description(
    file: UploadFile = File(...),
    session: UserSession = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        upload_service = UploadService()
        filename = upload_service.job_description(file, int(session.id), db)

        chroma_service = ChromaDBService()
        chroma_service.embedd_job_description(filename, session.id)

        return ApiSuccessResponse()
    except Exception as e:
        logger.error(e)
        return ApiErrorResponse(error=str(e))

@router.post("/resume")
def upload_resume(
    file: UploadFile = File(...),
    session: UserSession = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        upload_service = UploadService()
        filename = upload_service.resume(file, int(session.id), db)

        chroma_service = ChromaDBService()
        chroma_service.embedd_resume(filename, session.id)

        return ApiSuccessResponse()
    except Exception as e:
        logger.error(e)
        return ApiErrorResponse(error=str(e))
