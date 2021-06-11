from pydantic import BaseSettings
import logging

logger = logging.getLogger("uvicorn.error")


class Config(BaseSettings):
    class Config:
        env_prefix = "APP_"
        env_file = ".env"
        env_file_encoding = "utf-8"

    AUTH0_DOMAIN: str
    AUTH0_API_AUDIENCE: str
    AUTH0_APPLICATION_CLIENT_ID: str


config = Config()
logger.info(f"Current configuration: {repr(config)}")
