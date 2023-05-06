"""CLI commands for 'Categories'"""
import typer
import re
from config import Config
from fulus_cli import (
    __app_name__,
    __version__,
    ERRORS
)
from fulus_cli.sql_orm import db, models

app = typer.Typer()
database = db.DBConnection(Config.SQLALCHEMY_DATABASE_URI)

@app.command()
def create(
    title: str = typer.Argument(..., help="The name of the category")
) -> None:
    """Create a new category"""
    # Check if title is empty
    if not title.strip():
        typer.secho(
            "Name cannot be empty",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    # Check if the title is invalid (only characters and numbersa are allowed)
    if not re.fullmatch(
            r"[A-Za-z0-9]+",
            title.strip()):
        typer.secho(
            "Title must be a valid title",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    category = models.Category(
        title=title.strip()
    )
    status_code = database.create(category)
    if status_code != 0:
        typer.secho(
            f"Category creation failed. Error {ERRORS[status_code]}",
            fg=typer.colors.RED
        )
    else:
        typer.secho(
            f"Category '{title}' has been added",
            fg=typer.colors.GREEN
        )


@app.command()
def list() -> None:
    """List all categories"""
    result, status_code = database.read(models.Category)
    if status_code != 0:
        typer.secho(
            f"Failed while retriveing categories. Error: {ERRORS[status_code]}",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho("------------")
        typer.secho("id | title ")
        typer.secho("------------")
        for row in result:
            typer.secho(' | '.join([str(row.id), row.title]))

@app.command()
def update(
) -> None:
    pass

@app.command()
def delete(
    title: str = typer.Argument(..., help="The name of the category")
) -> None:
    """Remove existing category"""
    category, status_code = database.get_id(models.Category(title=title))
    if status_code != 0 or category is None:
        typer.secho(
            f"Category can't be removed. Error: {ERRORS[status_code]}",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    category_id = category[0].id
    status_code = database.delete(
        models.Category,
        category_id
    )
    if status_code != 0:
        typer.secho(
            f"Category can't be removed. Error: {ERRORS[status_code]}",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"Category '{title}' has been removed", fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()