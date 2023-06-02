import typer
from fulus_cli.config import Config
from typing import Optional
from fulus_cli.sql_orm import db
from fulus_cli import (
    __app_name__,
    __version__,
    ERRORS,
)

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        print(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


# @app.command()
def init(
    db_path: str = typer.Option(
        Config.SQLALCHEMY_DATABASE_URI,
        "--db-path",
        "-db",
        prompt="Use default database location? Tap [Enter] to use default location. Otherwise, enter custom location.\n",
    )
) -> None:
    """Initialize the to-do database."""

    status_code = db.init_database(db_path)
    if status_code != 0:
        typer.secho(
            f'Creating Database file failed with "{ERRORS[status_code]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The finance cli database is {db_path}", fg=typer.colors.GREEN)
