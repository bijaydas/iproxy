from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Application"
    HOST: str = "localhost"
    PORT: int = 8000

    PROJECT_VERSION: str = "0.1.0"
    PROJECT_DESCRIPTION: str = "FastAPI application"
    DEBUG: bool = True

    DATABASE_URL: str

    # JWT settings
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    LOGS_PATH: str = "logs"
    ENABLE_CONSOLE_LOGGING: bool = False
    ENABLE_FILE_LOGGING: bool = True

    MAX_ACTIVE_SESSIONS_PER_USER: int = 9999999
    CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
