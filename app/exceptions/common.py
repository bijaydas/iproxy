from starlette import status


class BaseAppException(Exception):
    def __init__(self, error: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        self.error = error
        self.status_code = status_code
        super().__init__(error)

class FallbackException(BaseAppException):
    def __init__(self, error: str = "Fallback", status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(error, status_code)

class LLMLimitExceededException(BaseAppException):
    def __init__(
        self,
        error: str = "Reach out to me@bijaydas.com to make more request",
        status_code: int = status.HTTP_400_BAD_REQUEST
    ):
        super().__init__(error, status_code)
