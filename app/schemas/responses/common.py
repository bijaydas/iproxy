from pydantic import BaseModel


class ApiSuccessResponse(BaseModel):
    message: str

class ApiSuccessDataResponse(BaseModel):
    data: dict

class ApiErrorResponse(BaseModel):
    error: str = "Please try again later."
