from pydantic import BaseModel


class ApiSuccessResponse(BaseModel):
    message: str

class ApiSuccessDataResponse(BaseModel):
    data: dict
