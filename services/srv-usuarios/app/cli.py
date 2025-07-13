# cli.py
import typer
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, models
import uuid # Adicionando import uuid que pode ser útil no futuro

# Cria a aplicação Typer
app = typer.Typer()

@app.command()
def promote_user(
    email: str = typer.Argument(..., help="O e-mail do usuário a ser promovido."),
    role: models.TipoUsuarioEnum = typer.Option(
        models.TipoUsuarioEnum.ADMIN, 
        "--role", "-r", 
        help="O novo papel a ser atribuído ao usuário."
    )
):
    """
    Promove ou altera o papel (role) de um usuário existente no sistema.
    """
    db: Session = SessionLocal()
    
    typer.echo(f"Buscando usuário com e-mail: {email}")
    user = crud.get_usuario_by_email(db, email=email)
    
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
    db.close()

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
    db: Session = SessionLocal()

    user = crud.get_usuario_by_email(db, email=email)
    if user:
        typer.secho(f"Erro: Usuário com e-mail '{email}' já existe.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    hashed_password = crud.get_password_hash(password)
    new_admin = models.Usuario(
        id=uuid.uuid4(),
        email=email,
        senha_hash=hashed_password,
        tipo_usuario=models.TipoUsuarioEnum.ADMIN,
        is_active=True
    )
    db.add(new_admin)
    db.commit()

    typer.secho(f"Superusuário '{email}' criado com sucesso!", fg=typer.colors.GREEN)
    db.close()

if __name__ == "__main__":
    app()