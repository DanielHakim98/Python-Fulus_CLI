"""CLI commands for 'Users'"""
import typer
import re
from config import Config
from fulus_cli import __app_name__, __version__, ERRORS
from fulus_cli.sql_orm import db, models

app = typer.Typer()
database = db.DBConnection(Config.SQLALCHEMY_DATABASE_URI)


@app.command()
def create(
    username: str = typer.Argument(..., help="The name of the user to be created"),
    email: str = typer.Argument(..., help="The email of the user"),
) -> None:
    """Create a new user"""

    # Check if the username is an empty string
    if not username.strip():
        typer.secho("Username or Email cannot be empty", fg=typer.colors.RED)
        raise typer.Exit(1)

    # Check if the email is invalid
    if not re.fullmatch(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+",
        email.strip(),
    ):
        typer.secho("Email must be a valid email address", fg=typer.colors.RED)
        raise typer.Exit(1)

    user = models.User(name=username.strip(), email=email.strip())
    status_code = database.create(user)

    if status_code != 0:
        typer.secho(
            f"User can't be created. Error: {ERRORS[status_code]}", fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"User '{username}' has been created", fg=typer.colors.GREEN)


@app.command()
def list() -> None:
    """List all users"""
    result, status_code = database.read(models.User)
    if status_code != 0:
        typer.secho(
            f"Failed while retriveing users. Error: {ERRORS[status_code]}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho("------------------")
        typer.secho("id | name | email")
        typer.secho("------------------")
        for row in result:
            typer.secho(" | ".join([str(row.id), row.name, row.email]))


@app.command()
def delete(
    username: str = typer.Argument(..., help="The name of the user to be removed"),
) -> None:
    """Remove existing user"""

    user, status_code = database.get_id(models.User(name=username, email=""))
    if status_code != 0:
        typer.secho(
            f"User can't be retrieved. Error: {ERRORS[status_code]}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    elif len(user) < 1:
        typer.secho("User does not exist", fg=typer.colors.RED)
    user_id = user[0].id

    status_code = database.delete(models.User, user_id)
    if status_code != 0:
        typer.secho(
            f"User can't be removed. Error: {ERRORS[status_code]}", fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"User '{username}' has been removed", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
