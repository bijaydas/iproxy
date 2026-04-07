from pydantic import BaseModel


class SignUpResponse(BaseModel):
    name: str | None
    email: str

class SignUpResponseData(BaseModel):
    data: SignUpResponse
