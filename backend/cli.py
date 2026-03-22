import typing as t

import typer

from src.db.session import SessionLocal
from src.services.user_service import create_user

app = typer.Typer()


@app.command()
def create_admin(
    username: str,
    password: str,
    is_admin: t.Annotated[bool, typer.Option("--admin")] = False,
) -> None:
    """Create an admin user"""
    with SessionLocal() as session:
        user = create_user(
            session,
            username=username,
            password=password,
            is_admin=is_admin,
        )

    typer.echo(f"✅ Admin created: {user.username}")


if __name__ == "__main__":
    app()
