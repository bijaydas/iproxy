from pydantic import BaseModel


class UserProfile(BaseModel):
    name: str | None
    email: str
