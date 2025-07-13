# app/main.py
from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings
from app.database.session import Base, engine

# Cria as tabelas no banco de dados (se não existirem) ao iniciar
# Esta linha é importante para que o SQLAlchemy crie a estrutura do DB
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Inclui o roteador principal da API, com o prefixo /api/v1
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz para verificar a saúde geral da aplicação."""
    return {"message": f"Bem-vindo à API do {settings.PROJECT_NAME}!"}