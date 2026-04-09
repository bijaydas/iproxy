import json
import logging
import sys
import time
from pathlib import Path

from fastapi.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.settings import settings


class SetupLogger:
    """Directory where log files will be stored"""

    log_dir: Path

    """Full path to log file, including file name"""
    log_file: str

    log_format: str = "%(asctime)s - %(levelname)s - %(message)s"

    log_formatter = None

    _logger = None

    def __init__(self):
        self._create_log_dir()
        self._setup_log_file()
        self._setup_log_formatter()
        self._setup_logger()

    def _create_log_dir(self):
        self.log_dir = Path(settings.LOGS_PATH)
        self.log_dir.mkdir(exist_ok=True)

    def _setup_log_file(self):
        today = time.strftime("%Y-%m-%d")
        log_file_name = f"app_{today}.log"

        self.log_file = str(self.log_dir / log_file_name)

    def _setup_log_formatter(self):
        self.log_formatter = logging.Formatter(self.log_format, datefmt="%Y-%m-%d %H:%M:%S")
        self.log_formatter = logging.Formatter(self.log_format)

    def _setup_logger(self):
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.INFO)

    def _setup_console_logging(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.log_formatter)
        self._logger.addHandler(console_handler)

    def _setup_file_logging(self):
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(self.log_formatter)
        self._logger.addHandler(file_handler)

    def load(self):
        if settings.ENABLE_CONSOLE_LOGGING:
            self._setup_console_logging()

        if settings.ENABLE_FILE_LOGGING:
            self._setup_file_logging()

        return self._logger


logger = SetupLogger().load()


class LoggingMiddleware(BaseHTTPMiddleware):
    @classmethod
    def remove_sensitive_info(cls, data: dict) -> dict:
        if "password" in data:
            data["password"] = "****"
        if "confirm_password" in data:
            data["confirm_password"] = "****"
        return data

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        request_body = await request.body()

        if request_body:
            try:
                json_payload = json.loads(request_body)
                json_request_body = self.remove_sensitive_info(json_payload)
                logger.info(
                    f"Incoming request: {request.method} {request.url}"
                    f"Headers: {dict(request.headers)} Body: {json_request_body}"
                )
            except (json.JSONDecodeError, UnicodeDecodeError):
                # If JSON parsing fails, log as plain text
                logger.info(
                    f"Incoming request: {request.method} {request.url}"
                    f"Headers: {dict(request.headers)} Body: {request_body.decode('utf-8', errors='ignore')}"
                )
        else:
            logger.info(
                f"Incoming request: {request.method} {request.url} Headers: {dict(request.headers)} Body: <empty>"
            )

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        logger.info(f"Completed response: {response.status_code} in {process_time:.2f}ms")

        return response
