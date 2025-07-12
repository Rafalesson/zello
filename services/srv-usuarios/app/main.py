# main.py

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine, get_db

# Esta linha cria as tabelas no banco de dados, se elas não existirem.
# É executada quando a aplicação inicia.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Serviço de Usuários Zello",
    description="API para gerenciamento de usuários (pacientes e médicos)",
    version="0.1.0"
)

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raiz que retorna o status do serviço.
    """
    return {"servico": "Serviço de Usuários", "status": "operacional"}


@app.post("/pacientes/", response_model=schemas.PacientePublic, status_code=status.HTTP_201_CREATED, tags=["Pacientes"])
def criar_novo_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    """
    Cria um novo paciente no sistema.
    - **email**: O email deve ser único.
    - **senha**: Será armazenada de forma segura (hash).
    """
    # Lógica para verificar se o email já existe pode ser adicionada aqui
    # db_user = crud.get_user_by_email(db, email=paciente.email)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    novo_paciente = crud.criar_paciente(db=db, paciente=paciente)
    return novo_paciente