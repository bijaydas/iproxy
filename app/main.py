from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette import status

from app.api.v1 import auth, general, profile, upload
from app.core.logger import LoggingMiddleware
from app.core.settings import settings
from app.core.startup import checks
from app.exceptions.common import BaseAppException


@asynccontextmanager
async def lifespan(app: FastAPI):
    checks()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    lifespan=lifespan,
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
def base_exception_handler(request: Request, exception: BaseAppException):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "error": exception.error,
        },
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    errors = []
    for error in exception.errors():
        ctx = error.get("ctx", {})
        if "error" in ctx:
            ctx = {
                "error": str(ctx["error"])
            }

        errors.append({
            "loc": error.get("loc"),
            "msg": error.get("msg"),
            "type": error.get("type"),
            "ctx": ctx
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "errors": errors,
        },
    )


app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(profile.router, prefix="/api/profile", tags=["profile"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(general.router, prefix="/api", tags=["general"])
