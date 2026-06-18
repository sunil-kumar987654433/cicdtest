from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import  SecretStr




class Settings(BaseSettings):
    DATABASE_URL: str
    SYNC_DATABASE_URL: str
    REDIS_HOST: str
    REDIS_PORT: int
    CELERY_BROKER_URL: str
    CELERY_BACKEND_URL: str
    
    JWT_SECRET: SecretStr
    JWT_ALGORITHAM: SecretStr
    ACCESS_TOKEN_EXPIRED: int
    REFRESH_TOKEN_EXPIRED: int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra='ignore'
    )


Config = Settings()