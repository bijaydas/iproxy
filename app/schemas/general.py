from pydantic import BaseModel


class UserSession(BaseModel):
    id: str
    email: str
    token: str
