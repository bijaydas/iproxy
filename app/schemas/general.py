from pydantic import BaseModel


class UserSession(BaseModel):
    email: str
