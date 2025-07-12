# main.py
from fastapi import FastAPI

app = FastAPI(
    title="Serviço de Usuários",
    description="API para gerenciamento de usuários (pacientes e médicos)",
    version="0.1.0"
)

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raiz que retorna uma mensagem de boas-vindas.
    """
    return {"servico": "Serviço de Usuários", "status": "operacional"}