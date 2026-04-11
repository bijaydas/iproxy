from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core import logger, settings
from app.deps.auth import get_current_user
from app.exceptions.common import FallbackException
from app.schemas.requests.general import SearchRequest
from app.schemas.responses.common import ApiSuccessDataResponse, ApiSuccessResponse
from app.services import ChromaDBService, LLMService

router = APIRouter()

@router.post("/ask")
async def ask(
    payload: SearchRequest,
    user_session: Session = Depends(get_current_user),
):
    query = payload.q
    try:
        chroma_db = ChromaDBService()
        llm = LLMService()

        """Classifying about the query type"""
        collection_type = llm.classify_query_source(query)

        collection = chroma_db.get_collection(collection_type)

        document_results = collection.similarity_search(
            query,
            k=3,
        )

        if len(document_results) == 0:
            return ApiSuccessResponse()

        answer = llm.answer_query(query, document_results)

        logger.info(f"Query: {query} | Type: {collection_type} | Answer: {answer}")

        return ApiSuccessDataResponse(
            data={
                "answer": answer,
            }
        )
    except Exception as e:
        logger.error(e)
        return FallbackException(error=str(e))

@router.get("/improvements")
async def improvements(
    user_session: Session = Depends(get_current_user),
):
    try:
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
    user_session: Session = Depends(get_current_user),
):
    query = payload.q
    try:
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
        logger.info(f"interview: {llm_response}")

        return ApiSuccessDataResponse(
            data={
                "response": llm_response,
            }
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        raise FallbackException(str(e))
