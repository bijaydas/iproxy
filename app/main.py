from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import auth
from app.core.logger import LoggingMiddleware
from app.core.settings import settings
from app.exceptions.common import BaseAppException
from app.schemas.responses.common import ApiErrorResponse

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(BaseAppException)
def base_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiErrorResponse(
            message=exc.message,
        ).model_dump(),
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(exc.errors())
    return JSONResponse(
        status_code=422,
        content=ApiErrorResponse(
            message=exc.errors()[-1]["msg"],
        ).model_dump(),
    )


app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
