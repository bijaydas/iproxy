from starlette import status

from app.exceptions.common import BaseAppException


class EmailAlreadyExists(BaseAppException):
    def __init__(self, error: str = "Email already exists"):
        super().__init__(error)
