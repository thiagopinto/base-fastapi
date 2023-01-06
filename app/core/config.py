
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    APP_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    DBAPI: str
    USER_DATABASE: str
    PASS_DATABASE: str
    HOST_DATABASE: str
    PORT_DATABASE: str
    DATABASE_NAME: str
    TOKEN_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str
    REFRESH_TOKEN_EXPIRE_MINUTES: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
