import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    SECRET_KEY: str
    EXPIRE_MINUTES = 60 * 24
    ALGORITHM = "HS256"

    SUPERUSER_NAME: str
    SUPERUSER_PASSWORD: str
    SUPERUSER_EMAIL: str

    class Config:
        if os.getenv("TEST"):
            env_file = '.test.env'
        elif os.getenv("PROD"):
            env_file = ".prod.env"
        else:
            env_file = '.dev.env'


def get_app_settings():
    return Settings()
