# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

# Importando todos os módulos do nosso pacote
from . import crud, models, schemas, security
from .database import engine, get_db

# Cria as tabelas no banco de dados (se não existirem)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Serviço de Usuários Zello",
    description="API para gerenciamento de usuários e autenticação.",
    version="1.0.0"
)

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz para verificar a saúde do serviço."""
    return {"serviço": "Serviço de Usuários", "status": "operacional"}

@app.post("/login", response_model=schemas.Token, tags=["Autenticação"])
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    """Autentica um usuário e retorna um token de acesso JWT."""
    user = crud.get_usuario_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/usuarios/me/", response_model=schemas.UsuarioPublic, tags=["Usuários"])
def read_users_me(
    current_user: models.Usuario = Depends(security.get_current_user)
):
    """Retorna os dados do usuário atualmente autenticado. Rota protegida."""
    return current_user

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
    """Cria um novo paciente e sua conta de usuário associada no sistema."""
    db_user = crud.get_usuario_by_email(db, email=paciente.usuario.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O e-mail fornecido já está em uso."
        )
    
    novo_paciente = crud.criar_paciente(db=db, paciente_data=paciente)
    return novo_paciente