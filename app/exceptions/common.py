from starlette import status


class BaseAppException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class GeneralAppException(BaseAppException):
    def __init__(self, message: str = "An error occurred"):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)
