# app/core/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Serviço de Usuários Zello"
    API_V1_STR: str = "/api/v1"
    
    # É importante usar os valores default aqui para o Pydantic não reclamar
    # durante a importação inicial, antes do .env ser lido pelo Docker Compose.
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    class Config:
        case_sensitive = True

settings = Settings()