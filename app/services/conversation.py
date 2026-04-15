from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models import Conversation as ConversationModel


class ConversationSchema(BaseModel):
    user_id: str
    user_query: str | None
    ai_response: str | None

class ConversationService:
    _db: Session

    def __init__(self, db: Session):
        self._db = db

    def create(self, payload: ConversationSchema) -> ConversationModel:
        conversation = ConversationModel(
            user_id = payload.user_id,
            user_query = payload.user_query,
            ai_response = payload.ai_response
        )

        self._db.add(conversation)
        self._db.commit()
        self._db.refresh(conversation)

        return conversation
