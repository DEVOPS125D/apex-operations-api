import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Apex Operations API"
    APP_VERSION: str = os.getenv("APP_VERSION", "v1.0.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "db")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

    class Config:
        env_file = ".env"


settings = Settings()