# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.database.session import Base, engine
from app.api.v1.api import api_router

# Importamos os modelos aqui para que a Base os conheça
from app.models import agenda, slot_horario, agendamento

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia as tarefas de inicialização e desligamento da aplicação.
    """
    # Código a ser executado ANTES do servidor iniciar
    print("INFO:     Verificando e criando tabelas do banco de dados do serviço de agendamentos...")
    # O comando para criar as tabelas agora é executado aqui dentro.
    Base.metadata.create_all(bind=engine)
    print("INFO:     Tabelas do serviço de agendamentos prontas.")
    
    yield  # A aplicação roda aqui
    
    # Código a ser executado APÓS o servidor encerrar (não precisamos de nada aqui por enquanto)
    print("INFO:     Serviço de agendamentos encerrado.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan  # Conecta o evento de ciclo de vida ao app
)

# Incluindo o roteador principal com o prefixo da versão
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz para verificar a saúde do serviço."""
    return {"serviço": "Serviço de Agendamentos", "status": "operacional"}