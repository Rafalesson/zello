# app/cli.py
import typer
from contextlib import contextmanager
from sqlalchemy.orm import Session
import uuid

from app.database.session import SessionLocal
from app.crud import crud_usuario
from app.models.usuario import TipoUsuarioEnum, Usuario
from app.models.especialidade import Especialidade
from app.core.security import get_password_hash


# Cria a aplicação Typer
app = typer.Typer()

@contextmanager
def get_db_session():
    """Context manager para garantir que a sessão do DB seja sempre fechada."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.command()
def promote_user(
    email: str = typer.Argument(..., help="O e-mail do usuário a ser promovido."),
    role: TipoUsuarioEnum = typer.Option(
        TipoUsuarioEnum.ADMIN, 
        "--role", "-r", 
        help="O novo papel a ser atribuído ao usuário."
    )
):
    """Promove ou altera o papel (role) de um usuário existente no sistema."""
    with get_db_session() as db:
        typer.echo(f"Buscando usuário com e-mail: {email}")
        user = crud_usuario.get_by_email(db, email=email)
        
        if not user:
            typer.secho(f"Erro: Usuário com e-mail '{email}' não encontrado.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        
        old_role = user.tipo_usuario
        user.tipo_usuario = role
        db.commit()
        
        typer.secho(
            f"Sucesso! Usuário '{email}' foi atualizado do papel '{old_role.value}' para '{role.value}'.",
            fg=typer.colors.GREEN
        )

@app.command()
def create_superuser(
    email: str = typer.Option(..., "--email", help="E-mail do superusuário."),
    password: str = typer.Option(
        ..., 
        "--password",
        prompt=True,
        hide_input=True,
        confirmation_prompt=True,
        help="Senha do superusuário."
    )
):
    """Cria um novo superusuário (ADMIN) no sistema."""
    with get_db_session() as db:
        user = crud_usuario.get_by_email(db, email=email)
        if user:
            typer.secho(f"Erro: Usuário com e-mail '{email}' já existe.", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        hashed_password = get_password_hash(password)
        new_admin = Usuario(
            id=uuid.uuid4(),
            email=email,
            senha_hash=hashed_password,
            tipo_usuario=TipoUsuarioEnum.ADMIN,
            is_active=True
        )
        db.add(new_admin)
        db.commit()

        typer.secho(f"Superusuário '{email}' criado com sucesso!", fg=typer.colors.GREEN)

@app.command()
def seed_specialties():
    """Popula a tabela de especialidades com dados iniciais."""
    with get_db_session() as db:
        initial_specialties = [
            "Cardiologia", "Dermatologia", "Ortopedia", "Pediatria",
            "Ginecologia", "Neurologia", "Psiquiatria", "Urologia"
        ]
        
        typer.echo("Verificando especialidades existentes...")
        count = db.query(Especialidade).count()
        
        if count > 0:
            typer.secho(f"{count} especialidades já existem. Nenhuma ação tomada.", fg=typer.colors.YELLOW)
            return

        typer.echo("Populando a tabela de especialidades...")
        for spec_name in initial_specialties:
            db_spec = Especialidade(nome=spec_name)
            db.add(db_spec)
        
        db.commit()
        typer.secho(f"{len(initial_specialties)} especialidades criadas com sucesso!", fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()