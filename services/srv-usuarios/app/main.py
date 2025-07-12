# main.py

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine, get_db

# Esta linha garante que o SQLAlchemy crie todas as tabelas definidas em models.py
# no banco de dados quando a aplicação iniciar.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Serviço de Usuários Zello",
    description="API para gerenciamento de usuários (pacientes, médicos e admins)",
    version="1.0.0"
)

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz para verificar a saúde do serviço."""
    return {"serviço": "Serviço de Usuários", "status": "operacional"}

@app.post(
    "/pacientes/", 
    response_model=schemas.PacientePublic, 
    status_code=status.HTTP_201_CREATED, 
    tags=["Pacientes"],
    summary="Cria um novo Paciente e seu respectivo Usuário"
)
def criar_novo_paciente(
    paciente: schemas.PacienteCreate, 
    db: Session = Depends(get_db)
):
    """
    Cria um novo paciente e sua conta de usuário associada no sistema.

    - **Verificação de Duplicidade:** O e-mail do usuário deve ser único.
    - **Criação Atômica:** O usuário e o perfil do paciente são criados na mesma transação.
    """
    # Verifica se já existe um usuário com o mesmo e-mail
    db_user = crud.get_usuario_by_email(db, email=paciente.usuario.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O e-mail fornecido já está em uso."
        )
    
    # Chama a função do CRUD para criar o paciente e o usuário
    novo_paciente = crud.criar_paciente(db=db, paciente_data=paciente)
    return novo_paciente