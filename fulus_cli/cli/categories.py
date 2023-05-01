"""CLI commands for 'Categories'"""
import typer
import re
from config import Config
from fulus_cli import (
    __app_name__,
    __version__,
    ERRORS
)
from fulus_cli.sql_orm import db

app = typer.Typer()

@app.command()
def create() -> None:
    pass

@app.command()
def list() -> None:
    pass

@app.command()
def update() -> None:
    pass

@app.command()
def delete() -> None:
    pass

if __name__ == "__main__":
    app()