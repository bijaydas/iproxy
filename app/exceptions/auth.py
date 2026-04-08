from fastapi import status

from app.exceptions.common import BaseAppException


class EmailAlreadyExists(BaseAppException):
    def __init__(self, error: str = "Email already exists"):
        super().__init__(error)

class InvalidUser(BaseAppException):
    def __init__(self, error: str = "Invalid user"):
        super().__init__(error)

class InvalidPassword(BaseAppException):
    def __init__(self, error: str = "Invalid password"):
        super().__init__(error)

class Unauthorized(BaseAppException):
    def __init__(self, error: str = "Unauthorized"):
        super().__init__(error, status.HTTP_401_UNAUTHORIZED)

class InvalidToken(BaseAppException):
    def __init__(self, error: str = "Invalid token"):
        super().__init__(error, status.HTTP_401_UNAUTHORIZED)
