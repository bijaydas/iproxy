
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
