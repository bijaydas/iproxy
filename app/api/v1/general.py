from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core import logger, settings, get_db
from app.deps.auth import get_current_user
from app.exceptions.common import FallbackException, LLMLimitExceededException
from app.schemas.requests.general import SearchRequest
from app.schemas.responses.common import ApiSuccessDataResponse, ApiSuccessResponse
from app.services import ChromaDBService, LLMService, UserService
from app.schemas.general import UserSession

router = APIRouter()


@router.get("/improvements")
async def improvements(
    user_session: UserSession = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        user = UserService()

        if not user.can_make_llm_calls(user_session.id, db):
            logger.info(f"User {user_session.id} cannot make LLM calls")
            raise LLMLimitExceededException()

        llm = LLMService()
        chroma = ChromaDBService()

        resume_data = chroma.get_collection(settings.COLLECTION_RESUME).get()["documents"]
        jd_data = chroma.get_collection(settings.COLLECTION_JOB_DESCRIPTION).get()["documents"]

        if len(resume_data) == 0:
            logger.info("No resume data")
            raise Exception("There is no resume data")

        if len(jd_data) == 0:
            logger.info("No jd data")
            raise Exception("There is no job description data")

        resume_content = "\n\n".join(resume_data)
        logger.info(f"Resume content: {resume_content}")

        jd_content = "\n\n".join(jd_data)
        logger.info(f"JD content: {jd_content}")

        llm_response = llm.resume_improvements(resume_content, jd_content)
        logger.info(f"Resume improvements: {llm_response}")
        user.consume_llm_calls(user_session.id, db)

        return ApiSuccessDataResponse(
            data={
                "response": llm_response,
            }
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        raise FallbackException(str(e))

@router.post("/interview")
async def interview(
    payload: SearchRequest,
    user_session: UserSession = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = payload.q
    try:
        user = UserService()

        if not user.can_make_llm_calls(user_session.id, db):
            logger.info(f"User {user_session.id} cannot make LLM calls")
            raise LLMLimitExceededException()

        llm = LLMService()
        chroma = ChromaDBService()

        resume_data = chroma.get_collection(settings.COLLECTION_RESUME).get()["documents"]
        jd_data = chroma.get_collection(settings.COLLECTION_JOB_DESCRIPTION).get()["documents"]

        if len(resume_data) == 0:
            logger.info("No resume data")
            raise Exception("There is no resume data")

        if len(jd_data) == 0:
            logger.info("No jd data")
            raise Exception("There is no job description data")

        resume_content = "\n\n".join(resume_data)
        logger.info(f"Resume content: {resume_content}")

        jd_content = "\n\n".join(jd_data)
        logger.info(f"JD content: {jd_content}")

        llm_response = llm.interview(resume_content, jd_content, query)
        user.consume_llm_calls(user_session.id, db)
        logger.info(f"interview: {llm_response}")

        return ApiSuccessDataResponse(
            data={
                "response": llm_response,
            }
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        raise FallbackException(str(e))
