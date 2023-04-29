import typer
from config import Config
from typing import Optional
from financial_manager import (
    __app_name__,
    __version__,
    ERRORS,
    database
)

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        print(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(version: Optional[bool] = typer.Option(
    None,
    "--version",
    "-v",
    help="Show the application's version and exit.",
    callback=_version_callback, is_eager=True
)) -> None:
    return

@app.command()
def init(
        db_path: str = typer.Option(
        Config.SQLALCHEMY_DATABASE_URI,
        "--db-path",
        "-db",
        prompt = "Use default database location? Tap [Enter] to use default location. Otherwise, enter custom location.\n",
    )
) -> None:
    """Initialize the to-do database."""

    status_code = database.init_database(db_path)
    if status_code != 0:
        typer.secho(
            f'Creating Database file failed with "{ERRORS[status_code]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The finance cli database is {db_path}", fg=typer.colors.GREEN)

@app.command()
def create_user(
    username: str = typer.Argument(..., help="The name of the user to be created"),
    email: str = typer.Argument(..., help="The email of the user")
) -> None:
    """Create a new user"""
    status_code = database.create_user(
        Config.SQLALCHEMY_DATABASE_URI,
        username,
        email
    )
    if status_code != 0:
        typer.secho(
            f"User can't be created. Error {ERRORS[status_code]}",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"User '{username}' has been created", fg=typer.colors.GREEN)

@app.command()
def remove_user(
    username: str = typer.Argument(..., help="The name of the user to be removed"),
    email: str = typer.Argument(..., help="The email of the user")
) -> None:
    """Remove existing user"""
    status_code = database.remove_user(
        Config.SQLALCHEMY_DATABASE_URI,
        username,
        email
    )

    if status_code != 0:
        typer.secho(
            f"User can't be removed. Error {ERRORS[status_code]}",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"User '{username}' has been removed", fg=typer.colors.GREEN)

@app.command()
def list_users() -> None:
    pass