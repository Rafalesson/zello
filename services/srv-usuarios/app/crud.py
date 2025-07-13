from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from typing import List, Optional
import uuid

# Configuração para hashing de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Retorna o hash de uma senha em texto plano."""
    return pwd_context.hash(password)

def get_usuario_by_email(db: Session, email: str) -> models.Usuario | None:
    """Busca um usuário pelo seu e-mail."""
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def criar_paciente(db: Session, paciente_data: schemas.PacienteCreate) -> models.Paciente:
    """
    Cria um novo registro de Usuário e um registro de Paciente associado.
    Tudo dentro de uma única transação.
    """
    # Extrai os dados do usuário do schema aninhado
    usuario_data = paciente_data.usuario
    
    # Cria o hash da senha
    hashed_senha = get_password_hash(usuario_data.senha)
    
    # Cria a instância do modelo de Usuário
    db_usuario = models.Usuario(
        email=usuario_data.email,
        senha_hash=hashed_senha,
        tipo_usuario=usuario_data.tipo_usuario,
    )

    # Cria a instância do modelo de Paciente
    db_paciente = models.Paciente(
        id=uuid.uuid4(),  # Gerar um UUID para o paciente
        nome_completo=paciente_data.nome_completo,
        data_nascimento=paciente_data.data_nascimento,
        telefone=paciente_data.telefone,
        # Associa o perfil do paciente ao usuário
        usuario=db_usuario
    )

    db.add(db_paciente) # Adicionar o paciente também adiciona o usuário devido ao 'cascade'
    db.commit()
    db.refresh(db_paciente)
    
    return db_paciente

def get_paciente(db: Session, paciente_id: uuid.UUID) -> models.Paciente | None:
    """Busca um paciente específico pelo seu ID."""
    return db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()

def get_pacientes(db: Session, skip: int = 0, limit: int = 100) -> List[models.Paciente]:
    """Busca uma lista de pacientes com paginação."""
    return db.query(models.Paciente).offset(skip).limit(limit).all()

def update_paciente(db: Session, paciente: models.Paciente, update_data: schemas.PacienteUpdate) -> models.Paciente:
    """Atualiza os dados de um paciente."""
    # Converte o Pydantic model para um dicionário, excluindo valores não setados
    update_dict = update_data.model_dump(exclude_unset=True)

    # Atualiza os campos do paciente
    for key, value in update_dict.items():
        if key != "usuario": # Trata o campo 'usuario' separadamente
            setattr(paciente, key, value)
    
    # Atualiza os campos do usuário associado, se houver
    if "usuario" in update_dict and update_dict["usuario"]:
        for key, value in update_dict["usuario"].items():
            setattr(paciente.usuario, key, value)

    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente

def delete_paciente(db: Session, paciente: models.Paciente) -> models.Paciente:
    """
    Realiza a exclusão lógica (soft delete) de um paciente,
    desativando seu usuário correspondente.
    """
    # A 'exclusão' é feita desativando o usuário.
    # A cascata de relacionamento não é usada aqui, pois é uma atualização.
    usuario = paciente.usuario
    usuario.is_active = False
    
    db.add(usuario)
    db.commit()
    db.refresh(paciente) # Refresh no paciente para carregar o estado atualizado do usuário
    
    return paciente

def hard_delete_paciente(db: Session, paciente: models.Paciente):
    """
    Realiza a exclusão física (hard delete) de um paciente e seu
    usuário associado do banco de dados. Operação destrutiva.
    """
    # A configuração 'cascade="all, delete-orphan"' no relacionamento
    # no models.py garante que ao deletar o paciente, o usuário
    # associado também seja deletado.
    db.delete(paciente)
    db.commit()
    # Não há objeto para dar refresh, pois ele foi deletado.
    return