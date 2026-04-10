from pydantic import BaseModel


class SearchRequest(BaseModel):
    q: str