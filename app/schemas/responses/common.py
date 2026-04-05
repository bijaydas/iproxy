from pydantic import BaseModel


class ApiSuccessResponse(BaseModel):
    success: bool = True
    message: str

class ApiSuccessDataResponse(BaseModel):
    success: bool = True
    message: str
    data: dict
