from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.deps.auth import get_current_user
from app.schemas.responses.common import ApiErrorResponse, ApiSuccessDataResponse, ApiSuccessResponse
from app.services import ChromaDBService, LLMService
from app.schemas.requests.general import SearchRequest

router = APIRouter()

@router.post("/search")
async def search(
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
        return ApiErrorResponse(error=str(e))
