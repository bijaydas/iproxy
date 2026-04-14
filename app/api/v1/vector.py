from fastapi import APIRouter, Depends

from app.core import logger
from app.schemas.general import UserSession
from app.deps.auth import get_current_user
from app.exceptions.common import FallbackException
from app.schemas.responses.common import ApiSuccessDataResponse
from app.services import ChromaDBService
from app.core.settings import settings


router = APIRouter()


@router.get("/{vector_type}")
async def get_vector(
    vector_type: str,
    user_session: UserSession = Depends(get_current_user),
):
    try:
        if vector_type.lower() not in ["resume", "jd"]:
            raise Exception("Invalid vector type")

        chroma = ChromaDBService()
        collection = chroma.get_collection(settings.COLLECTION_RESUME)

        if vector_type.lower() == "jd":
            collection = chroma.get_collection(settings.COLLECTION_JOB_DESCRIPTION)

        response_data = collection.get(
            where={
                "user_id": user_session.id
            }
        )

        logger.info(response_data)

        return ApiSuccessDataResponse(
            data=response_data
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        raise FallbackException(str(e))