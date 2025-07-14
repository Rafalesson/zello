# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Gerencia as configurações e variáveis de ambiente para o serviço de agendamentos.
    """
    PROJECT_NAME: str = "Serviço de Agendamentos Zello"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()