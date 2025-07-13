# main.py
from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated, List 
import uuid


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
    
    # CONDIÇÃO ATUALIZADA: Adicionamos a verificação 'not user.is_active'
    if not user or not security.verify_password(form_data.password, user.senha_hash) or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos, ou usuário inativo.",
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

# ==================
# ENDPOINTS PROTEGIDOS PARA PACIENTES
# ==================

@app.get("/pacientes/", response_model=List[schemas.PacientePublic], tags=["Pacientes"], summary="Lista todos os Pacientes")
def read_pacientes(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    """
    Retorna uma lista de pacientes.
    **Acesso restrito a administradores.**
    """
    if current_user.tipo_usuario != models.TipoUsuarioEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado."
        )
    pacientes = crud.get_pacientes(db, skip=skip, limit=limit)
    return pacientes


@app.get("/pacientes/{paciente_id}", response_model=schemas.PacientePublic, tags=["Pacientes"], summary="Busca um Paciente por ID")
def read_paciente(
    paciente_id: uuid.UUID, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    """
    Retorna os dados de um paciente específico.
    **Acesso: O próprio paciente ou administradores.**
    """
    db_paciente = crud.get_paciente(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    # Lógica de Autorização
    if (current_user.tipo_usuario != models.TipoUsuarioEnum.ADMIN and 
        current_user.id != db_paciente.usuario_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado."
        )
    return db_paciente


@app.put("/pacientes/{paciente_id}", response_model=schemas.PacientePublic, tags=["Pacientes"], summary="Atualiza um Paciente")
def update_paciente_data(
    paciente_id: uuid.UUID,
    paciente_update: schemas.PacienteUpdate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    """
    Atualiza os dados de um paciente.
    **Acesso: O próprio paciente ou administradores.**
    """
    db_paciente = crud.get_paciente(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    # Lógica de Autorização
    if (current_user.tipo_usuario != models.TipoUsuarioEnum.ADMIN and
        current_user.id != db_paciente.usuario_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado."
        )
    
    return crud.update_paciente(db=db, paciente=db_paciente, update_data=paciente_update)

@app.delete("/pacientes/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Pacientes"], summary="Deleta um Paciente (Soft Delete)")
def delete_paciente_data(
    paciente_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    """
    Realiza a exclusão lógica (soft delete) de um paciente, desativando sua conta.
    O registro não é removido do banco, apenas marcado como inativo.
    **Acesso: O próprio paciente ou administradores.**
    """
    db_paciente = crud.get_paciente(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    # Lógica de Autorização
    if (current_user.tipo_usuario != models.TipoUsuarioEnum.ADMIN and
            current_user.id != db_paciente.usuario_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado."
        )

    crud.delete_paciente(db=db, paciente=db_paciente)
    
    # Retorna uma resposta vazia com status 204
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ==================
# ENDPOINT DE HARD DELETE (ADMIN)
# ==================

@app.delete(
    "/admin/pacientes/{paciente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Admin"],
    summary="[ADMIN] Deleta permanentemente um Paciente (Hard Delete)"
)
def hard_delete_paciente_data(
    paciente_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    """
    **Atenção:** Realiza a exclusão física (hard delete) de um paciente e
    sua conta de usuário associada do sistema. Esta ação é irreversível.
    
    **Acesso restrito a administradores.**
    """
    # 1. Lógica de Autorização: Apenas Admins
    if current_user.tipo_usuario != models.TipoUsuarioEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado. Apenas administradores podem realizar esta operação."
        )

    # 2. Busca o paciente
    db_paciente = crud.get_paciente(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    # 3. Executa o hard delete
    crud.hard_delete_paciente(db=db, paciente=db_paciente)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

