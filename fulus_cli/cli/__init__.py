import typer
from fulus_cli.cli import users

app = typer.Typer()
app.add_typer(users.app, name="users")