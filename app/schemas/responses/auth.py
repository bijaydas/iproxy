from pydantic import BaseModel

from app.schemas.responses.common import ApiSuccessResponse


class SignUpResponse(BaseModel):
    email: str

class SignUpResponseData(ApiSuccessResponse):
    message: str = "success"
    data: SignUpResponse
