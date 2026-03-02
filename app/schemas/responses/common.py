from pydantic import BaseModel


class ApiSuccessResponse(BaseModel):
    success: bool = True
    message: str


class ApiErrorResponse(BaseModel):
    success: bool = False
    message: str


class ApiSuccessDataResponse(BaseModel):
    success: bool = True
    message: str
    data: dict
