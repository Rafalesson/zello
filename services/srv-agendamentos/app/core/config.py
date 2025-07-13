# app/core/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Gerencia as configurações e variáveis de ambiente para o serviço de agendamentos.
    """
    PROJECT_NAME: str = "Serviço de Agendamentos Zello"
    API_V1_STR: str = "/api/v1"

    # Configuração do banco de dados, lida do ambiente Docker
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    class Config:
        case_sensitive = True

settings = Settings()